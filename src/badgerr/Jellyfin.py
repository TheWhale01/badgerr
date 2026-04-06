import os
import base64
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
        self._tagname: str = os.getenv('BADGERR_TAGNAME', '')
        self._check_variables()
        self._http_session.headers.update({"X-MediaBrowser-Token": self._api_key})

    def _check_variables(self):
        if not self._url:
            raise BadgerEnvironmentVariableMissingException("JELLYFIN_URL environment variable is missing.")
        if not self._api_key:
            raise BadgerEnvironmentVariableMissingException("JELLYFIN_API_KEY environment variable is missing.")
        if not self._tagname:
            raise BadgerEnvironmentVariableMissingException("BADGERR_TAGNAME environment variable is missing.")

    def _get_item(self, id: str):
        response: Response = self._http_session.get(
            f'{self._url}/Items',
            params={
                'Ids': id,
                'Fields': 'Path,Genres,Studios,Overview,Taglines,SortName,ProviderIds,OfficialRating,CustomRating,CommunityRating,PremiereDate,ProductionYear,OriginalTitle,Tags'
            }
        )
        response.raise_for_status()
        item = response.json().get('Items', [])[0]
        return item

    def _add_tag(self, id: str):
        item = self._get_item(id)
        tags: list[str] = item.get('Tags', [])
        if self._tagname not in tags:
            tags.append(self._tagname)
            item['Tags'] = tags
            response: Response = self._http_session.post(
                f'{self._url}/Items/{id}',
                json=item,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            self._logger.info(f'added tag: {self._tagname} to item: {id}.')

    def _remove_tag(self, id: str):
        item = self._get_item(id)
        tags: list[str] = item.get('Tags', [])
        if self._tagname in tags:
            tags.remove(self._tagname)
            item['Tags'] = tags
            response: Response = self._http_session.post(
                f'{self._url}/Items/{id}',
                json=item,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            self._logger.info(f'removed tag: {self._tagname} from item: {id}.')

    def get_item_image(
        self,
        id: str,
        quality: int = 100,
        format: str = 'png',
        image_type: str = 'Primary',
        output_width: int = 2000,
        output_height: int = 3000
    ):
        response: Response = self._http_session.get(f"{self._url}/Items/{id}/Images/{image_type}", params={
            'format': format,
            'quality': quality,
            'width': output_width,
            'height': output_height
        })
        response.raise_for_status()
        return response.content

    def upload_image(self, id: str, image: bytes, image_type: str = "Primary"):
        self._add_tag(id)
        b64_image: str = base64.b64encode(image).decode('utf-8')
        response: Response = self._http_session.post(
            f'{self._url}/Items/{id}/Images/{image_type}/0',
            data=b64_image,
            headers={'Content-Type': 'image/png'}
        )
        response.raise_for_status()
        self._logger.info(f"New image uploaded for id: {id}")

    def restore_original_image(self, id: str, image_type: str = "Primary"):
        self._remove_tag(id)
        response: Response = self._http_session.post(
            f"{self._url}/Items/{id}/Refresh",
            params={
                "Recursive": "false",
                "ImageRefreshMode": "FullRefresh",
                "MetadataRefreshMode": "Default",
                "ReplaceAllImages": "true",
                "RegenerateTrickplay": "false",
                "ReplaceAllMetadata": "false"
            }
        )
        response.raise_for_status()
        self._logger.info(f"Successfully refreshed metadata for item: {id}")

    def get_tagged_items(self) -> set[str]:
        response: Response = self._http_session.get(f'{self._url}/Items', params={
            "Recursive": "true",
            "Tags": self._tagname,
            "Fields": "Id"
        })
        response.raise_for_status()
        data = response.json()
        return set(item.get('Id') for item in data.get("Items", []))
