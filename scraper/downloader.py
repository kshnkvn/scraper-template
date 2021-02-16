import logging
import asyncio

import aiohttp
import aioredis


class Downloader:

    def __init__(self, source, redis_uri, limit):
        self.source = source
        self.redis_uri = redis_uri
        self.limit = int(limit)

        self.semaphore: asyncio.Semaphore = None
        self.session: aiohttp.ClientSession = None
        self.redis: aioredis.create_redis = None

    def run(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.__main())

    async def __main(self):
        # initialization in event loop
        self.semaphore = asyncio.Semaphore(self.limit)
        self.session = aiohttp.ClientSession()
        self.redis = await aioredis.create_redis(self.redis_uri)

        # for the url list create a list of coroutines and run them together
        if type(self.source) is list:
            logging.info(
                f'An attempt will be made to load {len(self.source)} pages')
            tasks = [
                asyncio.create_task(self.__fetch(url)) for url in self.source]

            await asyncio.gather(*tasks)
        else:
            # TODO: implement start URL processing with handling next page
            logging.error(f'Start URL processing not implemented!')
            pass

        # publish message in the redis that
        # the downloader has finished working
        await self.redis.publish('channel:downloader', 'finished')

        await self.session.close()
        self.redis.close()

        logging.info('Downloader completes its work.')

    async def __fetch(self, url):
        async with self.semaphore:
            async with self.session.get(url) as response:
                # TODO: implement stopping the downloader in case of blocking
                if response.status != 200:
                    logging.error(f'Status: <{response.status}> URL: <{url}>')
                    return

                await self.__push_to_redis(url, await response.text())

    async def __push_to_redis(self, url, text):
        result = await self.redis.publish('channel:downloader', text)

        if result == 0:
            logging.error(f'Cant publish URL content <{url}> to redis')
            return

        logging.info(
            f'Published URL content <{url}> to redis with len <{len(text)}>')
