import pytz
from datetime import datetime, timedelta
from bson import ObjectId
from dateutil.parser import parse
from lxml import objectify
from pathlib import Path
from typing import Iterator, Optional

from scripts.yle.restore_av_works_from_reports.config import Config
from scripts.utils.file_operations import download_bazaar_files

YLE_TIMEZONE = "Europe/Helsinki"

MUSIC_SOURCE = {
    "Commercial": "1",
    "Kaupallinen äänite": "1",
    "Kaupallinen musiikki": "1",
    "Kotimainen musiikkivideo": "10",
    "Ulkomainen musiikkivideo": "11",
    "YLEn tilaama näyttämöteosmusiikki(Suuret oikeudet)": "12",
    "YLEn tilaama näyttämöteosmusiikki inserteissä": "13",
    " - ": "14",
    "YLEn tilaama tunnusmusiikki EI erilliskorvaussop.": "15",
    "YLEn tilaama tunnusmusiikki ON erilliskorvaussop.": "16",
    "YLEn tilaama ohjelman sisäinen musiikki": "17",
    "Elävä musiikki (radion suorat lähetykset)": "2",
    "Kotim. mus.vid, uusinta sarjaohjelmassa": "20",
    "Kotim. mus.vid, muist. uus. 30 sarjaohjelmassa": "21",
    "Kotim. mus.vid, max 60 asia-/ajankoht.ohjelm.": "22",
    "Kotim. mus.vid, krtk. 48t asia-/ajankoht.ohjelm. ": "23",
    "Kotim. mus.vid, uutisohjelmassa": "24",
    "Kotim. mus.vid, erillissopimus": "25",
    "Kotim ulkom musiikkivideo nettijulkaisu": "26",
    "Katalogimusiikki EI Teosto+Gramex korvauksia": "27",
    "Creative Commons (CC)": "28",
    "Creative Commons Teosto (CC-Teosto)": "29",
    "YLEn kantanauha": "3",
    "YLEn oma tallenne (mm. ohjelmanauha)": "4",
    "Ulkom radioyht tuottama äänite (mm. EBU-vaihto)": "5",
    "Demo": "6",
    "Muu äänite / tallenne": "7",
    "Katalogimusiikki": "9",
}

REVERSE_MUSIC_SOURCE = {
    "1": "Kaupallinen äänite",
    "10": "Kotimainen musiikkivideo",
    "11": "Ulkomainen musiikkivideo",
    "12": "YLEn tilaama näyttämöteosmusiikki(Suuret oikeudet)",
    "13": "YLEn tilaama näyttämöteosmusiikki inserteissä",
    "14": " - ",
    "15": "YLEn tilaama tunnusmusiikki EI erilliskorvaussop.",
    "16": "YLEn tilaama tunnusmusiikki ON erilliskorvaussop.",
    "17": "YLEn tilaama ohjelman sisäinen musiikki",
    "2": "Elävä musiikki (radion suorat lähetykset)",
    "20": "Kotim. mus.vid, uusinta sarjaohjelmassa",
    "21": "Kotim. mus.vid, muist. uus. 30 sarjaohjelmassa",
    "22": "Kotim. mus.vid, max 60 asia-/ajankoht.ohjelm.",
    "23": "Kotim. mus.vid, krtk. 48t asia-/ajankoht.ohjelm. ",
    "24": "Kotim. mus.vid, uutisohjelmassa",
    "25": "Kotim. mus.vid, erillissopimus",
    "26": "Kotim ulkom musiikkivideo nettijulkaisu",
    "27": "Katalogimusiikki EI Teosto+Gramex korvauksia",
    "28": "Creative Commons (CC)",
    "29": "Creative Commons Teosto (CC-Teosto)",
    "3": "YLEn kantanauha",
    "4": "YLEn oma tallenne (mm. ohjelmanauha)",
    "5": "Ulkom radioyht tuottama äänite (mm. EBU-vaihto)",
    "6": "Demo",
    "7": "Muu äänite / tallenne",
    "9": "Katalogimusiikki",
}

REVERSE_DISC_NUMBER_MAP = {
    "A": "1",
    "B": "2",
    "C": "3",
    "D": "4",
    "E": "5",
    "F": "6",
    "G": "7",
    "H": "8",
    "I": "9",
    "J": "10",
    "K": "11",
    "L": "12",
    "M": "13",
    "N": "14",
    "O": "15",
    "P": "16",
    "Q": "17",
    "R": "18",
    "S": "19",
    "T": "20",
}


class Cue:
    """aanite"""

    def __init__(
        self,
        cue: objectify.ObjectifiedElement,
        cue_index: int,
        program_start_time: datetime,
        previous_cue_end_time: Optional[datetime],
    ) -> None:
        self._data = cue
        self._cue_index = cue_index
        # in finnish timezone, as in reports. Doesn't have second resolution
        self._program_start_time = program_start_time
        # used to avoid cue overlaps when calculating current cue start_time
        self._previous_cue_end_time = previous_cue_end_time

    def as_reportal(self) -> dict:
        """Parse XML and return a dict with the Cue as the model defined in reportal-model."""

        now = datetime.now(pytz.UTC)
        record_number = self._data.aanitenro.text
        album_title = self._data.aanite_nimi.text
        recording_country = self._data.teokset.teos.aanitysmaa.text
        music_work_duration = (
            self._parse_mmmss_to_seconds(self._data.teokset.teos.teos_kesto.text)
            if self._data.teokset.teos.teos_kesto.text
            else None
        )

        relative_cue_start_time = (self.cue_start_time - self._program_start_time).total_seconds()

        is_jingle = self._data.teokset.teos.jingle.text == "x"
        is_visual = self._data.teokset.teos.b_v.text == "1"
        is_theme = self._data.teokset.teos.tunnari.text == "x"

        def get_cue_use(is_jingle, is_visual, is_theme):
            return {
                (False, False, False): "Background instrumental",
                (False, False, True): "Tunnari",
                (False, True, False): "Visual",
                (False, True, True): "Tunnari+Visual",
                (True, False, False): "Jingle",
                (True, False, True): "Jingle+Tunnari",
                (True, True, False): "Jingle+Visual",
            }[(is_jingle, is_visual, is_theme)]

        disc_number_start = self._data.teokset.teos.aanite_teos.alku_sivu.text
        disc_number_end = self._data.teokset.teos.aanite_teos.loppu_sivu.text

        disc_number_start = REVERSE_DISC_NUMBER_MAP.get(disc_number_start, disc_number_start)
        disc_number_end = REVERSE_DISC_NUMBER_MAP.get(disc_number_end, disc_number_end)

        disc_number = f"{disc_number_start}-{disc_number_end}"

        track_number_start = self._data.teokset.teos.aanite_teos.alku_ura.text
        track_number_end = self._data.teokset.teos.aanite_teos.loppu_ura.text

        # I've seen this value being picked from 2 places and reported differently in 3 places
        track_number = (
            f"{track_number_start}-{track_number_end}" or
            self._data.teokset.teos.teosnro.text
        )

        # contributors
        # NOTE: performers are interpreters + performers, what should we do with them?
        # NOTE: we lost all role info for other_contributors, what should we do with them?
        contributors_dict = {
            "arranger": self._data.teokset.teos.sovittajat.text,
            "composer": self._data.teokset.teos.saveltajat.text,
            "interpreter": self._data.teokset.teos.esittajat.text,
            "lyricist": self._data.teokset.teos.sanoittajat.text,
            "other_contributor": self._data.teokset.teos.muut_tekijat.text,
        }

        contributors_list = []
        for role, contributors in contributors_dict.items():
            if not contributors:
                continue

            for contributor_name in contributors.split(". "):
                last_name, first_name = None, contributor_name

                if ", " in contributor_name:
                    last_name, *first_name = contributor_name.split(", ")
                    first_name = ", ".join(first_name)

                contributors_list.append({
                    "_id": ObjectId(),
                    "first_name": first_name,
                    "last_name": last_name,
                    "role": role,
                    "contributor_ids": {},
                    "extras": {},
                })

        # TODO: assert reversed(reversed(list)) == list
        # no va a ser una operacion lineal
        return {
            "_id": ObjectId(),
            "cue_index": self._cue_index,
            "relative_start_time": relative_cue_start_time,
            "reference_start_time": None,
            "duration": self.cue_duration,
            "use": get_cue_use(is_jingle, is_visual, is_theme),
            "cue_identifiers": {},
            "extras": {},
            "music_work": {
                "_id": ObjectId(self.music_work_id),
                "title": self.music_work_title,
                "source": REVERSE_MUSIC_SOURCE[self.music_work_source],
                "duration": music_work_duration,
                "contributors": contributors_list,
                "work_ids": {
                    "album_number": record_number,
                    "label": self._data.levymerkki.text,
                    "catalog_number": self._data.kaup_tunnus.text,
                    "album": album_title,
                    "radioman_album_name": album_title,
                    "custom_id": self.custom_id,
                    "isrc": self.isrc,
                    "side_number": disc_number,
                    "track_number": track_number,
                },
                "extras": {
                    "album_code": record_number,
                    "recording_country": recording_country,
                    "recording_country_code": recording_country,
                    "recording_year": self._data.teokset.teos.aanitysvuosi.text,
                    "finnish_content": self._data.teokset.teos.kotim.text,
                    "languages": self._data.teokset.teos.esityskieli.text,
                    "disc_number": disc_number,
                    "track_number": track_number,
                    "alku_jarjno": self._data.teokset.teos.aanite_teos.alku_jarjno.text,
                    "loppu_jarjno": self._data.teokset.teos.aanite_teos.loppu_jarjno.text,
                },
                "document_info": {
                    "created_at": now,
                    "updated_at": now,
                },
                "permissions": [],
                "aggregations": {},
            },
            "verified": False,
            "aggregations": {},
        }

    def _parse_mmmss_to_seconds(self, mmmss: str) -> int:
        ss = int(mmmss[-2:])
        mmm = int(mmmss[:-2])

        return mmm * 60 + ss

    @property
    def music_work_id(self) -> str:
        return self._data.reportal_teos_id.text

    @property
    def isrc(self) -> Optional[str]:
        return self._data.teokset.teos.isrc.text

    @property
    def custom_id(self) -> Optional[str]:
        return self._data.custom_id.text

    @property
    def music_work_title(self) -> str:
        return self._data.teokset.teos.teos_nimi.text

    @property
    def music_work_source(self) -> str:
        """
        local reports keep numbers
        prod and backup DB, use mapping to store numbers

        mapping:
        https://bitbucket.org/bmat-music/yle-reportal/src/06fcf747985eeb8b33f738cf4cb62f43caa0ec0d/yle_reportal/reports/common/maps.py#lines-123
        """

        return str(self._data.teokset.teos.aanitetyyppi)

    @property
    def cue_duration(self) -> int:
        """Cue duration in seconds."""

        return self._parse_mmmss_to_seconds(
            self._data.teokset.teos.aanite_teos.kesto.text
        )

    @property
    def cue_start_time(self) -> datetime:
        hhmm = datetime.strptime(self._data.teokset.teos.teos_aklo.text, "%H%M")
        cue_start_time = self._program_start_time.replace(hour=hhmm.hour, minute=hhmm.minute)

        if (
            self._previous_cue_end_time is not None and
            self._previous_cue_end_time.minute == cue_start_time.minute
        ):
            cue_start_time.replace(second=self._previous_cue_end_time.second)

        if cue_start_time.time() < self._program_start_time.time():
            cue_start_time += timedelta(days=1)

        return cue_start_time.astimezone(pytz.UTC)

    @property
    def cue_end_time(self) -> datetime:
        return self.cue_start_time + timedelta(seconds=self.cue_duration)


class Program:
    def __init__(self, program: objectify.ObjectifiedElement) -> None:
        self._data = program

    @property
    def title(self) -> str:
        """Program title."""
        return str(self._data.nimi)

    @property
    def yle_numerical_id(self) -> str:
        """Matches Reportal yle_numerical_id."""
        return str(self._data.rapnro)

    @property
    def report_date(self) -> str:
        """Reported date --> YYYY-MM-DD"""
        return str(parse(str(self._data.ajopvm)).date())

    @property
    def plasma_id(self) -> str:
        """Matches Reportal plasma_id
        - plasma_ohjelma_id --> non radio programs
        - car_id	car_ohjelma_id --> radio programs
        """
        if plasma_id := self._data.plasma_ohjelma_id:
            return str(plasma_id)

        # only radio
        return f"12-{self._data.car_id}-4-{self._data.car_ohjelma_id}"

    @property
    def is_filler(self) -> bool:
        return '-' in self._data.car_lahetys_id.text if self._data.car_lahetys_id else False

    @property
    def cues(self) -> Iterator[Cue]:
        try:
            cues = self._data.aanite
        except AttributeError:
            return []

        program_start_time = parse(f"{self._data.julk_pvm_a.text} {self._data.aklo.text}").replace(
            tzinfo=pytz.timezone(YLE_TIMEZONE)
        )

        previous_cue_end_time = None
        for cue_index, cue in enumerate(cues, 1):
            cue_obj = Cue(cue, cue_index, program_start_time, previous_cue_end_time)
            previous_cue_end_time = cue_obj.cue_end_time
            yield cue_obj


class ReportFile:
    def __init__(self, report_file: Path) -> None:
        self._data = report_file

    @property
    def name(self) -> str:
        return self._data.name

    @property
    def date(self) -> str:
        return str(parse(self.name.split("_")[-1].split(".")[0][:8]).date())

    @property
    def programs(self) -> Iterator[Program]:
        file_content = objectify.fromstring(self._data.read_bytes())

        programs = file_content.ohjelma_esitys

        for program in programs:
            yield Program(program)


class ProgramFinder:
    def __init__(self, config: Config) -> None:
        self._config = config
        config.xml_reports_dir.mkdir(parents=True, exist_ok=True)

        # download reports if requested
        if config.download_bazaar_files is True:
            self.download_from_bazaar()

    def download_from_bazaar(self):
        print("Downloading reports from bazaar, please wait...")
        download_bazaar_files(
            db_uri=self._config.bazaar_mongo_uri,
            storage_uri=self._config.bazaar_storage_uri,
            query={"namespace": "yle-reports-fortnightly"},
            local_dir=str(self._config.xml_reports_dir.absolute()),
        )
        print("ALL REPORT FILES DOWNLOADED FROM BAZAAR")
        print("#######################################")

    @property
    def report_files(self) -> Iterator[ReportFile]:
        for report_file in self._config.xml_reports_dir.iterdir():
            yield ReportFile(report_file)

    @property
    def total_report_files(self) -> int:
        return len(list(self._config.xml_reports_dir.iterdir()))
