import os
import logging
import threading
from logging import Logger
from badgerr.Jellyfin import Jellyfin
from badgerr.Maintainerr import Maintainerr
from badgerr.ImageProcess import ImageProcess
from concurrent.futures import ThreadPoolExecutor
from badgerr.ImageConfig import ImageConfig, Position

class Badgerr:
    def __init__(self):
        self._maintainerr: Maintainerr = Maintainerr()
        self._jellyfin: Jellyfin = Jellyfin()
        self._logger: Logger = logging.getLogger('badger:Badger')
        self._config: ImageConfig = ImageConfig(
            text="Leaving Soon",
            text_color="#FFFFFF",
            text_background_color="#E50914",
            position=Position.TOP,
            text_padding_x=40,
            text_padding_y=40,
            img_padding_x=50,
            img_padding_y=100,
            background_opacity=0,
            font_size=150,
            background_color="#000000"
        )
        self._img_engine: ImageProcess = ImageProcess(os.getenv('FONT_URL', ''), self._config)
        self._local = threading.local()

    def _get_local_jellyfin(self):
        if not hasattr(self._local, "jellyfin"):
            self._local.jellyfin = Jellyfin()
        return self._local.jellyfin

    def _restore_item(self, item: str):
        jellyfin: Jellyfin = self._get_local_jellyfin()
        try:
            jellyfin.restore_original_image(item)
        except Exception as e:
            self._logger.error(f'Failed to restore the original poster for {item}: {e}')

    def _add_overlay(self, item: str):
        jellyfin: Jellyfin = self._get_local_jellyfin()
        try:
            new_image: bytes = self._img_engine.apply_overlay(jellyfin.get_item_image(item))
            jellyfin.upload_image(item, new_image)
        except Exception as e:
            self._logger.error(f'An error occured for item {item}: {e}. Restoring poster.')
            self._restore_item(item)

    def full_cleanup(self):
        badgerr_tagged_items: set[str] = self._jellyfin.get_tagged_items()
        maintainerr_tracked_items: set[str] = self._maintainerr.get_tracked_items()
        for item in (badgerr_tagged_items | maintainerr_tracked_items):
            self._restore_item(item)

    def run(self):
        badgerr_tagged_items: set[str] = self._jellyfin.get_tagged_items()
        maintainerr_tracked_items: set[str] = self._maintainerr.get_tracked_items()
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(self._restore_item, (badgerr_tagged_items - maintainerr_tracked_items))
            executor.map(self._add_overlay, (maintainerr_tracked_items - badgerr_tagged_items))
