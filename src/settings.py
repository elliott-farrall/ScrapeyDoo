LOG_LEVEL = 'DEBUG'
LOG_FILE = 'ScrapeyDoo.log'

REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'

COOKIES_ENABLED = False
ROBOTSTXT_OBEY = True

RETRY_TIMES = 2500
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408]

DOWNLOADER_MIDDLEWARES = {
    # Proxy
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy_proxies.RandomProxy': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    # User Agent
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}

RANDOM_UA_TYPE = 'desktop.random'
RANDOM_UA_PER_PROXY = True

PROXY_MODE = 0
PROXY_LIST = 'proxies.txt'