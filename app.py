import logging
import sys

from config import Config
from scraper import Downloader, Parser, Writer

logging.basicConfig(
    handlers=[
        logging.FileHandler('scraper.log', 'a', 'utf-8'),
        logging.StreamHandler(sys.stdout)
    ], 
    level=logging.INFO, 
    format='[%(asctime)s] [%(levelname)s]: %(message)s'
)
