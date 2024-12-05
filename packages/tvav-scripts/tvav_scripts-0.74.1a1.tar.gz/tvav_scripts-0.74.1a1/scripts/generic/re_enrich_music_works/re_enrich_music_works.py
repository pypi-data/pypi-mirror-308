import aiohttp
import asyncio
import csv
import logging
from bson.objectid import ObjectId
from datetime import datetime
from dotenv import load_dotenv
from functools import cached_property
from mongoengine import connect
from music_report.report import run_interceptors
from tqdm import tqdm
from typing import Generator, Optional

from music_report.enrichment.autofill import from_single_view
from music_report.single_view.client import AsyncSingleViewClient
from reportal_model import AvWork, MusicWork, Schedule

from scripts.utils.slack_notifier import ClassWithSlackLogger
from scripts.generic.re_enrich_music_works.config import EnricherSettings
from scripts.generic.re_enrich_music_works.utils import (
    get_client_custom_values,
    get_cuesheet_url,
    get_interceptors_dict,
    get_music_report_cuesheet_from_repmod_av_work,
    init_reports,
    get_music_report_cue_from_repmod_cue,
    CueEnrichmentOptions,
)


class Enricher(ClassWithSlackLogger):
    """ This is the main class where the logic for re enrichment is implemented."""

    def __init__(self):
        load_dotenv()
        super().__init__()
        self.config = EnricherSettings()  # type: ignore

        # SV async client
        self.client = None
        # To not print everything to Slack channel
        self.logger_term = logging.getLogger(self.__class__.__name__ + "Term")
        self.logger_term.setLevel(logging.INFO)

        try:
            connect(host=self.config.mongodb.get_mongo_db_uri())
            self.custom_values = get_client_custom_values(self.config.custom_values_str)
            self.customer_name = self.custom_values.get("client", "client")
            self.interceptors = get_interceptors_dict(self.custom_values, self.customer_name)
        except Exception as exc:
            self.logger.error(str(exc))
            raise exc

        self.logger.info("Enricher initialized")

    def music_work_to_re_enrich(self, with_header: bool = True) -> Generator[MusicWork, None, None]:
        """Generator for music works selected to be re enriched from the CSV file.

        The same single_view_id can be shared among many MusicWorks (duplicates),
        so we have to re enrich them all. We are going to display a message for these cases

        :return:
        """
        with open(
            self.config.music_works_file, "r"
        ) as file_to_read, open(
            f"{self.customer_name}_single_view_ids_repeated.csv", "a"
        ) as single_view_ids_repeated_file, open(
            f"{self.customer_name}_music_works_updated.csv", "a"
        ) as music_works_updated_file, open(
            f"{self.customer_name}_av_works_affected.csv", "a"
        ) as av_works_affected_file:
            reader = csv.reader(file_to_read, delimiter="\t")

            mw_writer = csv.writer(music_works_updated_file)
            av_writer = csv.writer(av_works_affected_file)
            dup_sv_id_writer = csv.writer(single_view_ids_repeated_file)

            for i, line in enumerate(reader):
                if i == 0 and with_header or not line[0]:
                    continue

                music_work_query = (
                    MusicWork.objects.filter(id=ObjectId(line[0]))
                    if self.config.is_music_works_ids
                    else MusicWork.objects.filter(work_ids__single_view_id=line[0])
                )

                if len(music_work_query) > 1 and not self.config.is_music_works_ids:
                    dup_sv_id_writer.writerow(
                        [
                            line[0],
                            len(music_work_query),
                        ]
                    )

                for music_work in music_work_query:
                    mw_writer.writerow([
                        music_work.id,
                        music_work.title,
                        music_work.source,
                        music_work.work_ids.get("isrc", None),
                        music_work.work_ids.get("single_view_id", None),
                    ])

                    if (
                        av_work := AvWork.objects.filter(
                            cuesheet__cues__music_work=music_work.id
                        ).first()
                    ):
                        av_writer.writerow([
                            av_work.id,
                            get_cuesheet_url(
                                self.config.reportal_domain,
                                str(av_work.id)
                            ),
                            music_work.title,
                            music_work.source,
                            music_work.work_ids.get("isrc", None),
                            music_work.work_ids.get("single_view_id", None),
                        ])

                    yield music_work

    def enrich_the_existing_music_work(self, music_work: MusicWork, music_work_enriched: MusicWork) -> None:
        """
        As we do not want to overwrite the ID or other important fields for the existing music work,
        we update the values for it using the created (but not saved) music work that was enriched.
        :param music_work:
        :param music_work_enriched:
        :return:
        """
        contributors = []
        for contributor in music_work_enriched.contributors:
            contributors.append(contributor.dict())

        # Clean up null fields from the existing music work dict fields
        existing_work_ids = {k: v for k, v in music_work.work_ids.items() if v is not None}
        existing_extras = {k: v for k, v in music_work.extras.items() if v is not None}

        extras = {**existing_extras, **music_work_enriched.extras, "re_enriched": datetime.now()}
        work_ids = (
            {**music_work_enriched.work_ids}
            if self.config.replace_work_ids
            else {**music_work_enriched.work_ids, **existing_work_ids}
        )
        set_params = {
            "set__title": music_work_enriched.title,
            "set__work_ids": work_ids,
            "set__extras": extras,
            "set__contributors": contributors
        }
        if self.config.update_source and music_work.source != music_work_enriched.source:
            set_params["set__source"] = music_work_enriched.source

        if not self.config.dry_run:
            music_work.update(**set_params)

    async def get_music_work_enriched(self, sound_recording: dict) -> Optional[MusicWork]:
        """ From the sound recording metadata we enrich the music work and create
        one Music Work with the data enriched.

        :param sound_recording:
        :return:
        """
        if not sound_recording:
            return None

        return await from_single_view(
            single_view_client=self.client,  # type: ignore
            sv_id=sound_recording.get("_id"),  # type: ignore
            interceptors=self.interceptors,
            context={"client_custom_values": self.custom_values}
        )

    async def get_sound_recording(self, music_work: MusicWork):
        """Get the sound recording metadata.
        Depending on the parameters set in the music work it will go to one client method or to another.

        :param music_work:
        :return:
        """
        only_latin_chars = self.custom_values.get("enrichment_params", {}).get("only_latin_chars", True)

        service_id, source = self.get_service_id_and_source(music_work)
        single_view_id = music_work.work_ids.get("single_view_id", None)
        isrc = music_work.work_ids.get("isrc", None)
        custom_id = (
            music_work.work_ids.get("custom_id", None)
            if self.config.custom_id_field is not None
            else None
        )
        iswc = music_work.work_ids.get("iswc", None)

        if single_view_id and self.config.single_view_ids_still_valid:
            # OR you can use the below to query by SINGLE_VIEW_ID
            sound_recording = await self.client.sound_recording_by_id(sound_recording_id=single_view_id)  # type: ignore
        elif source and service_id:
            sound_recording = await self.client.get_sound_recording(  # type: ignore
                source=source,
                service_id=service_id,
                only_latin_chars=only_latin_chars,
            )
        elif isrc:
            sound_recording = await self.client.sound_recording_by_isrc(  # type: ignore
                isrc=isrc,
                only_latin_chars=only_latin_chars,
            )
        elif (
                custom_id and
                self.config.commissioned_music_crawler is not None and
                self.config.custom_id_field is not None
        ):
            sound_recording = None
            srs = await self.client.search_sound_recordings_by_internal_code(  # type: ignore
                crawler=f"crawler_{self.config.commissioned_music_crawler}",
                code_name=f"{self.config.custom_id_field}",
                code_value=custom_id
            )
            if len(srs) > 0:  # type: ignore
                sound_recording = await self.client.sound_recording_by_id(sound_recording_id=srs[0]["_id"])  # type: ignore
        elif iswc and self.config.commissioned_music_crawler is not None:
            sound_recording = None
            srs = await self.client.search_sound_recordings(  # type: ignore
                crawler=f"{self.config.commissioned_music_crawler}",
                query=iswc,
                only_latin_chars=only_latin_chars,
                size=1
            )
            if len(srs) > 0:
                sound_recording = await self.client.sound_recording_by_id(sound_recording_id=srs[0]["_id"])  # type: ignore
        else:
            raise Exception("No Source, ServiceID or Single View ID")

        if not sound_recording:
            self.logger_term.warning(f"Sound recording not found for sv id '{single_view_id}'")
        return sound_recording

    @staticmethod
    def get_service_id_and_source(music_work: MusicWork) -> tuple:
        """ This method will return the service_id and the source.

        At some point in the Match-importer history, we migrated from a model where match
        in extras was a list to a model that has more sense and was a dict.

        So just in case we get a music work with the last model we have to create the logic for both cases

        :param music_work:
        :return:
        """
        source = None
        service_id = None
        if (extras := music_work.extras) and (match := extras.get("match", None)):
            if not isinstance(match, list):
                service_id = match.get("reference_serviceid", None)
                source = match.get("reference_source_name", None)
                return service_id, source

            for match_key, match_value in match:
                if match_key != "reference":
                    continue

                for reference_key, reference_value in match_value:
                    if reference_key == "reference_source_name":
                        source = reference_value

                    if reference_key == "serviceid":
                        service_id = reference_value

                if source and service_id:
                    break
        return service_id, source

    @cached_property
    def total_music_works_to_re_enrich(self):
        """
        Return the total lines in the file so the total music works to re enrich
        :return:
        """
        with open(self.config.music_works_file, "r") as file_to_read:
            total_lines = len(file_to_read.readlines())

        if self.config.csv_with_header:
            total_lines -= 1
        return total_lines

    def run_cue_level_enrichments(self, music_work: MusicWork) -> None:
        """Runs cue level enrichers for the current MusicWork.

        Searches for all AvWorks containing the specified MusicWork.

        Finds the cues pointing to this MusicWork and uses the enrichers
        on "cue" level from client's interceptors.

        Then updates some fields from cue and music_work.

        This script adds most common MatchImporter.options.extras to both
        cuesheet.extras and context["options"].extras. If your enrichers
        depend on a value that does not exist in the ones defined in
        get_music_report_cuesheet_from_repmod_av_work, it will fail.
        """

        if len(self.interceptors.get("cue", ())) == 0:
            return

        if (av_works := AvWork.objects(cuesheet__cues__music_work=music_work)).count() == 0:
            return

        with open(
            f"{self.customer_name}_cue_level_enrichment.csv", "a"
        ) as cue_enrichment_report:
            cue_writer = csv.writer(cue_enrichment_report)

            # this progress bar won't be printed in Slack to avoid spam
            for av_work in tqdm(av_works, total=av_works.count()):
                schedule = next(
                    Schedule.objects(av_work=av_work, main_replica=True),
                    None
                )

                for cue in av_work.cuesheet.cues:
                    if cue.music_work != music_work:
                        continue

                    cuesheet = get_music_report_cuesheet_from_repmod_av_work(av_work, schedule)

                    enriched_cue = run_interceptors(
                        context={
                            "client_custom_values": self.custom_values,
                            # some clients use context["options"].extras
                            # Example:
                            # https://bitbucket.org/bmat-music/mediaset_it/src/aa7d62ed7a65908c92d04dc49917b243540ea9cc/mediaset_it/match_importer/enrichers.py#lines-287
                            #
                            # while others use cuesheet.extras
                            # Example:
                            # https://bitbucket.org/bmat-music/nrk/src/393dfdbd7416f093515d40e2f5ab013dd97005ce/nrk/match_importer/enrichers.py#lines-403
                            #
                            # So, until we agree on how to do it for all the customers,
                            # I am supporting both so cue enrichment does not fail here.
                            "options": CueEnrichmentOptions(extras=cuesheet.extras)
                        },
                        interceptors=self.interceptors,
                        event_type="cue",
                        intercepted_object=get_music_report_cue_from_repmod_cue(cue),
                        kwargs={"cuesheet": cuesheet},
                    )

                    # These are the values we usually update on cue level enrichers
                    cue.use = enriched_cue.use if enriched_cue else cue.use
                    cue.music_work.source = enriched_cue.music_work.source if enriched_cue else cue.music_work.source
                    # ccma
                    cue.music_work.extras = enriched_cue.extras if enriched_cue else cue.music_work.extras

                    cue_writer.writerow([
                        music_work.id,
                        music_work.title,
                        av_work.id,
                        av_work.titles.get("original_title", ""),
                        cue.cue_index,
                    ])

                if not self.config.dry_run:
                    av_work.save()

    async def re_enrich(self):
        """
        Main method to re enrich the selected music works from the file
        :return:
        """
        init_reports(self.customer_name)

        self.logger.info(
            "Running for customer %s (%s)" % (
                self.customer_name,
                "dry run mode" if self.config.dry_run else "no dry run mode"
            )
        )

        async with aiohttp.ClientSession() as session:
            self.client = AsyncSingleViewClient(session=session, base_url=self.config.single_view_url)

            for music_work in self.tqdm(
                self.music_work_to_re_enrich(with_header=self.config.csv_with_header),
                total=self.total_music_works_to_re_enrich
            ):
                try:
                    sound_recording = await self.get_sound_recording(music_work=music_work)
                    music_work_enriched = await self.get_music_work_enriched(sound_recording)  # type: ignore
                except Exception as e:
                    self.logger_term.error(f"Error while enriching music work {music_work.id}: {e}")
                    continue

                if not music_work_enriched:
                    continue

                self.enrich_the_existing_music_work(music_work=music_work, music_work_enriched=music_work_enriched)

                if self.config.do_cue_level_enrichment:
                    self.run_cue_level_enrichments(music_work=music_work)

        self.logger.info("Done!")


if __name__ == "__main__":
    enricher = Enricher()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(enricher.re_enrich())
