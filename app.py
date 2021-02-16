import logging
import sys
from multiprocessing import Process

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

# determine the source from which scraping will be
# only one source will be used. priority LIST > URL
source = None
if bool(Config.DOWNLOAD_LIST):
    source = Config.DOWNLOAD_LIST
elif Config.START_URL:
    source = Config.START_URL
else:
    logging.error(f'Source not specified for the scraper')
    sys.exit(-1)

downloader = Downloader(source, Config.REDIS_URI, Config.DOWNLOAD_LIMIT)
parser = Parser(Config.REDIS_URI, Config.PARSE_LIMIT)
writer = Writer(Config.OUTPUT_FILE_PATH, Config.REDIS_URI)

downloader_process = Process(target=downloader.run)
downloader_process.start()

parser_process = Process(target=parser.run)
parser_process.start()

writer_process = Process(target=writer.run)
writer_process.start()
writer_process.join()
