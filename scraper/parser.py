import time
import logging
import json
from concurrent.futures import ThreadPoolExecutor

from lxml.html import fromstring
from redis import Redis, from_url


class Parser:

    def __init__(self, redis_uri, limit):
        self.redis_uri = redis_uri
        self.limit = int(limit)

        self.thread_pool: ThreadPoolExecutor = None
        self.redis: Redis = None
        self.pubsub: Redis.pubsub = None

    def run(self):
        self.thread_pool = ThreadPoolExecutor(self.limit)
        self.redis = from_url(self.redis_uri)
        self.pubsub = self.redis.pubsub(ignore_subscribe_messages=True)
        self.pubsub.subscribe('channel:downloader')

        self.__dequeue_redis()

        self.thread_pool.shutdown(wait=True)

        # publish message in the redis that
        # the parser has finished working
        self.redis.publish('channel:parser', 'finished')
        self.redis.close()

        logging.info('Parser completes its work.')

    def __dequeue_redis(self):
        while True:
            message = self.pubsub.get_message()

            if not message:
                time.sleep(0.25)
                continue

            if message['data'].decode(encoding='utf-8') == 'finished':
                break

            self.thread_pool.submit(self.__parse_content, message['data'])

    def __parse_content(self, text):
        html = fromstring(text)

        title = html.find('.//h1/a[@class="question-hyperlink"]').text
        created = html.find('.//time').get('datetime')
        answers_count = int(
            html.find('.//h2[@data-answercount]').get('data-answercount'))

        data = {
            'title': title,
            'created': created,
            'answers_count': answers_count
        }
        logging.info(f'Parsed data: <{data}>')

        self.redis.publish('channel:parser', json.dumps(data))
