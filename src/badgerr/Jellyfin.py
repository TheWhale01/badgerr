import os
import logging
from logging import Logger
from requests import Session, Response
from badgerr.exceptions import BadgerEnvironmentVariableMissingException

class Jellyfin:
    def __init__(self):
        self._logger: Logger = logging.getLogger("badgerr:Jellyfin")
        self._http_session: Session = Session()
        self._url: str = os.getenv('JELLYFIN_URL', '')
        self._api_key: str = os.getenv('JELLYFIN_API_KEY', '')
        self._check_variables()
        self._http_session.headers.update({"X-Emby-Token": self._api_key})

    def _check_variables(self):
        if not self._url:
            raise BadgerEnvironmentVariableMissingException("JELLYFIN_URL environment variable is missing.")
        if not self._api_key:
            raise BadgerEnvironmentVariableMissingException("JELLYFIN_API_KEY environment variable is missing.")

    def get_media_image(self, id: str, quality: int = 100, format: str = 'png', image_type: str = 'Primary'):
        response: Response = self._http_session.get(f"{self._url}/Items/{id}/Images/{image_type}", params={
            'format': format,
            'quality': quality
        })
        response.raise_for_status()
        return response.content
