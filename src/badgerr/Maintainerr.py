import os
import logging
from typing_extensions import Any, Generator
from requests import Response, Session
from logging import Logger
from badgerr.exceptions import BadgerEnvironmentVariableMissingException

class Maintainerr:
    def __init__(self):
        self._logger: Logger = logging.getLogger("badgerr:Maintainerr")
        self._http_session: Session = Session()
        self._url: str = os.getenv('MAINTAINERR_URL', '')
        self._api_key: str = os.getenv('MAINTAINERR_API_KEY', '')
        self._check_variables()
        self._http_session.headers.update({"X-Api-Key": self._api_key})

    def _check_variables(self):
        if not self._url:
            raise BadgerEnvironmentVariableMissingException("MAINTAINERR_URL environment variable is missing.")
        if not self._api_key:
            raise BadgerEnvironmentVariableMissingException("MAINTAINERR_API_KEY environment variable is missing.")

    def get_collections(self) -> Generator[Any, Any, None]:
        response: Response = self._http_session.get(f'{self._url}/api/collections')
        response.raise_for_status()
        for item in response.json():
            yield item

    def get_items_in_collection(self, collection_id: str):
        response: Response = self._http_session.get(f'{self._url}/api/collections/media', params={
            'collectionId': collection_id
        })
        response.raise_for_status()
        for item in response.json():
            yield item
