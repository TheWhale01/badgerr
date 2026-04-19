import sys
import logging
from argparse import ArgumentParser
from badgerr.Badgerr import Badgerr
from dotenv import load_dotenv, find_dotenv

def parse_args():
    parser: ArgumentParser = ArgumentParser(description="Apply overlay to jellyfin media based on maintainerr collections.")
    parser.add_argument('-c', '--config', help="Yaml overlay configuration path")
    return parser.parse_args()

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    logger = logging.getLogger("badgerr:main")
    logger.info("Starting Badgerr")
    args = parse_args()
    if not load_dotenv(find_dotenv(usecwd=True)):
        logger.warning("Could not find .env file.")
    badgerr: Badgerr = Badgerr(args)
    badgerr.run()
