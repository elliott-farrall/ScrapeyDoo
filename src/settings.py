from importlib.resources import files
import os
import sys

FROZEN = getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")
PLATFORM = sys.platform

def resource_path(relative_path):
    if FROZEN:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    else:
        base_path = str(files("src"))
    return os.path.join(base_path, relative_path)

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
RANDOM_UA_FILE = resource_path("resources/user_agents.txt")

PROXY_MODE = 0
PROXY_LIST = resource_path("resources/proxies.txt")
