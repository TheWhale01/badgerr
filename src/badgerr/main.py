import sys
import logging
from badgerr.Badgerr import Badgerr
from dotenv import load_dotenv, find_dotenv

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    logger = logging.getLogger("badgerr:main")
    logger.info("Starting Badgerr")
    if not load_dotenv(find_dotenv(usecwd=True)):
        logger.warning("Could not find .env file.")
    badgerr: Badgerr = Badgerr()
    badgerr.run()
    # badgerr.full_cleanup()
