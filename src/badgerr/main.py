import sys
import logging
from badgerr.Badgerr import Badgerr
from dotenv import load_dotenv, find_dotenv
from argparse import ArgumentParser, Namespace

def parse_args() -> Namespace:
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
    args: Namespace = parse_args()
    if not load_dotenv(find_dotenv(usecwd=True)):
        logger.warning("Could not find .env file.")
    badgerr: Badgerr = Badgerr(args)
    badgerr.run()
