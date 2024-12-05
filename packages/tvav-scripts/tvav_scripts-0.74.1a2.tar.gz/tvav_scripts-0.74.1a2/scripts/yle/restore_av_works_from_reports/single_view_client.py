from typing import Optional
from requests import Session
from requests.models import HTTPError
from scripts.yle.restore_av_works_from_reports.config import Config


class SingleViewAPIClient:
    """
    SV API DOCS: http://sv-api.data.bmat.com/docs#
    """
    def __init__(self, config: Config) -> None:
        self.uri = config.single_view_uri
        self.session = Session()
        self.session.hooks = {
            "response": lambda r, *args, **kwargs: r.raise_for_status()
        }

    def get_sound_recording_by_single_view_id(self, single_view_id: str) -> Optional[dict]:
        try:
            return self.session.get(
                url=f"{self.uri}/sound-recording/{single_view_id}"
            ).json()
        except HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise e

    def get_sound_recording_by_isrc(self, isrc: str) -> Optional[dict]:
        try:
            return self.session.get(
                url=f"{self.uri}/sound-recording-isrc/{isrc}",
                params={
                    "only_latin_chars": True,
                }
            ).json()
        except HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise e


    def get_sound_recordings_by_internal_code(
        self,
        code_value: str,
        code_name: str,
        source: str
    ) -> list[dict]:
        try:
            return self.session.get(
                url=f"{self.uri}/sound-recordings-by-internal-code",
                params={
                    "code_value": code_value,
                    "code_name": code_name,
                    "source": source,
                },
            ).json()["results"]["sound_recordings"]
        except HTTPError as e:
            if e.response.status_code == 404:
                return []
            raise e

    def get_sound_recordings_by_q(self, q: str) -> list[dict]:
        try:
            return self.session.get(
                url=f"{self.uri}/sound-recordings",
                params={
                    "q": q,
                    "only_latin_chars": True,
                },
            ).json()["results"]["sound_recordings"]
        except HTTPError as e:
            if e.response.status_code == 404:
                return []
            raise e
