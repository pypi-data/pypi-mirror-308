from typing import Union
import aiohttp
import asyncio
import nest_asyncio
from datetime import datetime
from itertools import dropwhile

from music_report.single_view.client import AsyncSingleViewClient
from reportal_model import AvWork, MusicWork
from yle_reportal.common.client_custom_values import SINGLE_VIEW_ROLES_MAPPING, ENRICHMENT_PARAMS, reporting_tool_custom_values

from scripts.utils.common import str_to_base_64

nest_asyncio.apply()

REPORTAL_URL = "https://yle-reportal.bmat.com/"
SV_API = "http://sv-api.data.bmat.com/"
DEFAULT_START_TIME = datetime(2022, 1, 25)
CONTRIBUTOR_AUTHOR_ROLES = [
    "author",
    "composer",
    # YLE-1868 - Rita said YLE only cared about author and composer roles being missing
    # "lyricist",
    # "arranger",
]
CONTRIBUTOR_INTERPRETER_ROLES = [
    "interpreter",
]


async def get_sr_work_info_sound_recording(single_view_id: str, source: str, service_id: str) -> tuple:
    """Helper method to recover the SR_WORK_INFO and the Sound Recording from SV API.

    Uses YLE's client custom values.

    :return: sr_work_info and the sound_recording
    """
    session = aiohttp.ClientSession()
    async with session:
        client = AsyncSingleViewClient(session=session, base_url=SV_API)

        if single_view_id:
            get_recording_method = client.sound_recording_by_id
            params = {
                "sound_recording_id": single_view_id,
                "enhance": ENRICHMENT_PARAMS.get("enhance"),
                "links": ENRICHMENT_PARAMS.get("links"),
                "only_latin_chars": ENRICHMENT_PARAMS.get("only_latin_chars"),
            }
        else:
            get_recording_method = client.get_sound_recording
            params = {
                "source": source,
                "service_id": service_id,
                "suggest": ENRICHMENT_PARAMS.get("suggest"),
                "enhance": ENRICHMENT_PARAMS.get("enhance"),
                "links": ENRICHMENT_PARAMS.get("links"),
                "only_latin_chars": ENRICHMENT_PARAMS.get("only_latin_chars")
            }

        sr_work_info, sound_recording = await asyncio.gather(
            client.sr_work_territory(
                source=source,
                service_id=service_id,
                territory=reporting_tool_custom_values["country_code"],
                discard_no_role_contributors=ENRICHMENT_PARAMS.get('discard_no_role_contributors', None),
            ),
            get_recording_method(**params),
        )
        return sr_work_info, sound_recording


def contributor_with_role_exists_in_sv(
    single_view_id: str,
    source: str,
    service_id: str,
    roles_to_check: list[str],
) -> Union[str, bool]:
    """Method to check if contributor has any of the roles_to_check for the SR specified.

    It fetches the SR from SV API, gets the possible SV roles from YLE mappings and checks if
    any contributor role matches any of them.

    :return str | bool - True if contributor with role exists in SV, else False.
    """
    sr_work_info, sound_recording = asyncio.get_event_loop().run_until_complete(get_sr_work_info_sound_recording(single_view_id, source, service_id))

    if not sound_recording:
        return "True (could be previous to latin filter)"

    sv_roles_to_check = set(
        role_mapping[0]
        for role_mapping in SINGLE_VIEW_ROLES_MAPPING.items()
        if role_mapping[1] in roles_to_check
    )

    contributor_with_role_exists_in_sr_work_info = any(
        getattr(contributor, "role", None) in sv_roles_to_check
        for contributor in getattr(sr_work_info, "work_contributors", [])
    )

    contributor_with_role_exists_in_sr = any(
        getattr(contributor, "role", None) in sv_roles_to_check
        for contributor in getattr(sound_recording, "work_contributors", [])
    )

    return contributor_with_role_exists_in_sr_work_info or contributor_with_role_exists_in_sr


def get_reportal_cuesheet_url(av_work: AvWork) -> str:
    """Returns YLE cuesheet URL for the specified AvWork."""
    return REPORTAL_URL + "cuesheets/view/" + str_to_base_64(f"AvWork:{str(av_work.id)}")


def check_music_work_contributors(music_work: MusicWork) -> tuple[bool, bool]:
    """
    Checks if author and interpreter are present in the music_work contributors.
    :param music_work:
    :return: 2 booleans. If it has author, and if it has interpreter.
    """
    author = list(dropwhile(lambda x: x.role not in CONTRIBUTOR_AUTHOR_ROLES, music_work.contributors))
    interpreter = list(dropwhile(lambda x: x.role not in CONTRIBUTOR_INTERPRETER_ROLES, music_work.contributors))

    return bool(author), bool(interpreter)
