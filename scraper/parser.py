import time
import logging

import lxml
from redis import Redis, from_url


class Parser:

    def __init__(self, redis_uri, limit):
        self.redis_uri = redis_uri
        self.limit = limit

        self.redis: Redis = None
        self.pubsub: Redis.pubsub = None

    def run(self):
        self.redis = from_url(self.redis_uri)
        self.pubsub = self.redis.pubsub(ignore_subscribe_messages=True)
        self.pubsub.subscribe('channel:downloader')

        self.__dequeue_redis()

    def __dequeue_redis(self):
        while True:
            message = self.pubsub.get_message()

            if not message:
                time.sleep(0.25)
                continue

            if message['data'].decode(encoding='utf-8') == 'finished':
                logging.info('Parser completes its work.')

                # publish message in the redis that
                # the parser has finished working
                self.redis.publish('channel:parser', 'finished')

                break

            self.__parse_content(message['data'])

    def __parse_content(self, text):
        pass
