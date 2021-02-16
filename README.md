# What is it?

It's an asynchronous scraper template. Yes it is.  
You don't need to think that this is a framework, this is something that needs to be modified to suit your needs in each specific case.  

If you need something ready-made than take [Scrapy](https://scrapy.org/).

## Dependencies

- [Redis](https://redis.io/) server.
- Python dependencies ([requirements.txt](requirements.txt))

## Installation

First of all download this repository.  
After that add the following values to the environment variables:

- REDIS_URI - link to connect to Redis. More details [here](https://github.com/lettuce-io/lettuce-core/wiki/Redis-URI-and-connection-details).
- OUTPUT_FILE_PATH - full path to file with parsed data result.
- DOWNLOAD_LIST_PATH - full path to json-file with array of urls which need to scrape.

    Example:

```json
[
    "https://stackoverflow.com/questions/66213583",
    "https://stackoverflow.com/questions/66213584",
    "https://stackoverflow.com/questions/66213578",
    "https://stackoverflow.com/questions/66213576"
]
```

- DOWNLOAD_LIMIT - ```integer``` limit of async download functions. Default: 5.
- PARSE_LIMIT - ```integer``` limit of parser threads. Default: 5.

You can just change the ```config.py``` and not bother with environment variables ¯\\\_(ツ)_/¯

After that just run ```app.py```. It's all.

## Customization

Remember that this is just a template, so you will need to write your own method for parsing the data. You can find it at file [scraper/parser.py](scraper/parser.py) where you need to modify ```__parse_content``` method.
