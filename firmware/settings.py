BOT_NAME = "firmware"

SPIDER_MODULES = ["firmware.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"

ITEM_PIPELINES = {
    "firmware.pipelines.FirmwarePipeline" : 1,
}

FILES_STORE = "./output/"

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0
AUTOTHROTTLE_MAX_DELAY = 15
CONCURRENT_REQUESTS = 8

DOWNLOAD_TIMEOUT = 1200
DOWNLOAD_MAXSIZE = 0
DOWNLOAD_WARNSIZE = 0

ROBOTSTXT_OBEY = False
USER_AGENT = "FirmwareBot/1.0 (+https://github.com/firmadyne/scraper)"

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 300,
}

HTTPCACHE_ENABLED = True
HTTPCACHE_POLICY = 'scrapy.extensions.httpcache.DummyPolicy'
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

CLOSESPIDER_ERRORCOUNT = 1

#SQL_SERVER = "127.0.0.1"
