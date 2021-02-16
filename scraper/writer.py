import time
import json
import logging
from os import path, makedirs
from json.decoder import JSONDecodeError

from redis import Redis, from_url


class Writer:

    def __init__(self, output_file_path, redis_uri):
        self.output_file_path = output_file_path
        self.redis_uri = redis_uri

        # create a folder for the file if it doesn't exist
        self.dir_path = path.dirname(self.output_file_path)
        if not path.exists(self.dir_path):
            makedirs(self.dir_path)

        # create a file if it doesn't exist
        if not path.exists(self.output_file_path):
            with open(self.output_file_path, 'a') as f:
                pass

        self.redis: Redis = None
        self.pubsub: Redis.pubsub = None

    def run(self):
        self.redis = from_url(self.redis_uri)
        self.pubsub = self.redis.pubsub(ignore_subscribe_messages=True)
        self.pubsub.subscribe('channel:parser')

        self.__dequeue_redis()

        self.redis.close()

        logging.info('Writer wrote down all data and finish work.')

    def __dequeue_redis(self):
        while True:
            message = self.pubsub.get_message()

            if not message:
                time.sleep(0.25)
                continue

            if message['data'].decode(encoding='utf-8') == 'finished':
                break

            self.__write_to_json(message['data'])

    def __write_to_json(self, json_str):
        file = open(self.output_file_path, 'r', encoding='utf-8')
        try:
            json_obj = json.load(file)
        except JSONDecodeError:
            json_obj = []
        finally:
            file.close()

        json_obj.append(json.loads(json_str))

        file = open(self.output_file_path, 'w', encoding='utf-8')
        json.dump(json_obj, file, indent=2)
        file.close()
