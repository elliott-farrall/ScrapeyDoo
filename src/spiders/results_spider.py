from scrapy import Spider, Request, signals
from spiders.product_spider import ProductSpider

from datetime import datetime



class ResultsSpider(Spider):
    name = 'results-spider'

    custom_settings = {
        'FEED_URI': f'scraps/scrap_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
        'FEED_FORMAT': 'csv',
    }

    def __init__(self, query, progress_bar=None):
        self.progress_bar = progress_bar
        self.progress = {
            'results found': 0,
            'results scraped': 0,
            'results pages': 1,
        }

        self.progress_bar.update(text="Searching...")
        self.start_urls = [self.search(query)]

    def search(self, query):
        base_url = 'https://www.amazon.co.uk/s/ref=sr_adv_b?search-alias=stripbooks&unfiltered=1&__mk_en_GB=%C3%85M%C3%85Z%C3%95%C3%91&'
        url_parts = []

        default_query = {
            'field-keywords': '',
            'field-author': '',
            'field-title': '',
            'field-isbn': '',
            'field-publisher': '',
            'node': 'Any Subject',
            'field-binding_browse-bin': 'Any Format',
            'field-subject': 'Any Age',
            'emi': '',
            'p_46': 'All Dates',
            'p_45': '',
            'p_47': '',
            'sort': '',
        }

        for key, value in query.items():
            default_value = default_query.get(key)
            if value != default_value:
                url_part = f'{key}={value}'
                url_parts.append(url_part)
        url = base_url + '&'.join(url_parts) + '&Adv-Srch-Books-Submit.x=43&Adv-Srch-Books-Submit.y=11'
        
        return url

    def parse(self, response):
        PRODUCT_PAGE_SELECTOR = '[data-asin] h2 a::attr("href")'

        product_pages = response.css(PRODUCT_PAGE_SELECTOR).extract()
        self.progress['results found'] += len(product_pages)
        self.progress_bar.update(value=(self.progress['results scraped']/self.progress['results found'] if self.progress['results found'] != 0 else 0), text=f"Pages: {self.progress['results pages']} | Scraped: {self.progress['results scraped']}/{self.progress['results found']}")

        for product_page in product_pages:
            yield Request(
                response.urljoin(product_page),
                callback=self.product_spider.parse
            )

        NEXT_PAGE_SELECTOR = '[data-asin]  span  a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator::attr("href")' 
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield Request(
                response.urljoin(next_page),
                callback=self.parse
            )

            self.progress['results pages'] += 1
            self.progress_bar.update(value=(self.progress['results scraped']/self.progress['results found'] if self.progress['results found'] != 0 else 0), text=f"Pages: {self.progress['results pages']} | Scraped: {self.progress['results scraped']}/{self.progress['results found']}")

    @property
    def product_spider(self):
        return ProductSpider()
    
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.item_scraped, signal=signals.item_scraped)
        return spider
    
    def item_scraped(self, item, response, spider):
        self.progress['results scraped'] += 1
        self.progress_bar.update(value=(self.progress['results scraped']/self.progress['results found'] if self.progress['results found'] != 0 else 0), text=f"Pages: {self.progress['results pages']} | Scraped: {self.progress['results scraped']}/{self.progress['results found']}")
