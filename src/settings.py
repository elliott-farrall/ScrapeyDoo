import os
import sys

FROZEN = getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")
PLATFORM = sys.platform

if FROZEN:
    APP_DIR = os.path.dirname(sys.argv[0])
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

# ------------------------------ Scrapy Settings ----------------------------- #

LOG_LEVEL = "DEBUG"
LOG_FILE = "ScrapeyDoo.log"

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"

COOKIES_ENABLED = False
ROBOTSTXT_OBEY = True

RETRY_TIMES = 2500
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408]

DOWNLOADER_MIDDLEWARES = {
    # Proxy
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": 90,
    "scrapy_proxies.RandomProxy": 100,
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 110,
    # User Agent
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    "scrapy_user_agents.middlewares.RandomUserAgentMiddleware": 400,
}

RANDOM_UA_TYPE = "desktop.random"
RANDOM_UA_PER_PROXY = False
RANDOM_UA_FILE = os.path.join(APP_DIR, "resources/user_agents.txt")

PROXY_MODE = 0
PROXY_LIST = os.path.join(APP_DIR, "resources/proxies.txt")
