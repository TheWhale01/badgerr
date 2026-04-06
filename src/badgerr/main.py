import os
import sys
import logging
from badgerr.Jellyfin import Jellyfin
from badgerr.Maintainerr import Maintainerr
from dotenv import load_dotenv, find_dotenv
from badgerr.ImageConfig import ImageConfig, Position
from badgerr.ImageProcess import ImageProcess

def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    logger = logging.getLogger("badgerr:main")
    logger.info("Starting application")
    if not load_dotenv(find_dotenv(usecwd=True)):
        logger.warning("Could not find .env file.")
    maintainerr: Maintainerr = Maintainerr()
    jellyfin: Jellyfin = Jellyfin()
    config: ImageConfig = ImageConfig(
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
    img_engine: ImageProcess = ImageProcess(os.getenv("FONT_URL", ""), config)
    badgerr_items: set[str] = jellyfin.get_tagged_items()
    maintainerr_items: set[str] = maintainerr.get_tracked_items()
    for item in (badgerr_items - maintainerr_items):
        try:
            jellyfin.restore_original_image(item)
        except Exception as e:
            logger.error(f'Failed to restore the original poster for {item}: {e}')
    for item in (maintainerr_items - badgerr_items):
        try:
            new_image: bytes = img_engine.apply_overlay(jellyfin.get_item_image(item))
            jellyfin.upload_image(item, new_image)
            break
        except Exception as e:
            logger.error(f'An error occured for item {item}: {e}. Restoring poster.')
            jellyfin.restore_original_image(item)
