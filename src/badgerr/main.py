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
        text="LEAVING SOON !",
        text_color="#FFFFFF",
        text_background_color="#E50914",
        position=Position.TOP,
        text_padding_x=40,
        text_padding_y=40,
        img_padding_x=50,
        img_padding_y=100,
        background_opacity=0,
        background_color="#000000"
    )
    img_engine: ImageProcess = ImageProcess()
    img_engine.get_font("https://github.com/ryanoasis/nerd-fonts/raw/refs/heads/master/patched-fonts/RobotoMono/SemiBold/RobotoMonoNerdFont-SemiBold.ttf", config)
    filename: str = "/home/hades/code/badgerr/test.png"
    try:
        for collection in maintainerr.get_collections():
            for media in maintainerr.get_items_in_collection(collection.get('id')):
                img: bytes = img_engine.apply_overlay(jellyfin.get_media_image(media.get('mediaServerId')), config)
                img_engine.write_img_file(img, filename)
                return
    except Exception:
        os.remove(filename)
