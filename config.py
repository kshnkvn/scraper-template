import json
from os import path, getenv
from json.decoder import JSONDecodeError


class Config:

    BASE_DIR = path.abspath(path.dirname(__file__))

    # full path to output JSON-file
    OUTPUT_FILE_PATH = path.abspath(
        getenv('OUTPUT_FILE_PATH', path.join(BASE_DIR, 'output.json')))

    # full path to json-file with array of urls
    # which need to scrape
    DOWNLOAD_LIST_PATH = getenv('DOWNLOAD_LIST_PATH', None)
    DOWNLOAD_LIST: list = []

    if DOWNLOAD_LIST_PATH:
        try:
            DOWNLOAD_LIST = json.load(
                open(path.abspath(DOWNLOAD_LIST_PATH), 'r', encoding='utf-8'))
        except (FileNotFoundError, JSONDecodeError):
            print(
                'The specified download list does not exist,',
                'or incorrect JSON format')

    # if download list is not specified that needed
    # to specify start url and rework method of find next page
    # somewhere in scraper/downloader.py
    START_URL = getenv('START_URL', None)
    PAGE_COUN = getenv('PAGE_COUNT', 1)

    # limit of async download functions
    DOWNLOAD_LIMIT = getenv('DOWNLOAD_LIMIT', 5)

    # limit of parser threads
    PARSE_LIMIT = getenv('PARSE_LIMIT', 5)

    REDIS_URI = getenv('REDIS_URI', 'redis://127.0.0.1:6379')
