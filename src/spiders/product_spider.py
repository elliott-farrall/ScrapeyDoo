from scrapy import Spider, Request

# ---------------------------------------------------------------------------- #
#                                Product Spider                                #
# ---------------------------------------------------------------------------- #

class ProductSpider(Spider):
    name = 'product-spider'

    def parse(self, response):
        TITLE_SELECTOR = '#productTitle::text'
        AUTHOR_SELECTOR = '#bylineInfo > span > a::text'
        DESCRIPTION_SELECTOR = '#bookDescription_feature_div > div > div.a-expander-content.a-expander-partial-collapse-content > span::text'
        PRICE_WHOLE_SELECTOR = '#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center.aok-relative > span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay > span:nth-child(2) > span.a-price-whole::text'
        PRICE_FRACTION_SELECTOR = '#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center.aok-relative > span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay > span:nth-child(2) > span.a-price-fraction::text'
        ISBN_10_SELECTOR = '#rpi-attribute-book_details-isbn10 > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span::text'
        ISBN_13_SELECTOR = '#rpi-attribute-book_details-isbn13 > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span::text'
        EDITION_SELECTOR = '#rpi-attribute-book_details-edition > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span::text'
        PUBLISHER_SELECTOR = '#rpi-attribute-book_details-publisher > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span::text'
        PUBLICATION_DATE_SELECTOR = '#rpi-attribute-book_details-publication_date > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span::text'
        LANGUAGE_SELECTOR = '#rpi-attribute-language > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span::text'
        DIMENSIONS_SELECTOR = '#rpi-attribute-book_details-dimensions > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span::text'
        PRINT_LENGTH_SELECTOR = '#rpi-attribute-book_details-fiona_pages > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span::text'

        data = {
            'title': response.css(TITLE_SELECTOR).extract_first(),
            'author': response.css(AUTHOR_SELECTOR).extract_first(),
            'description': response.css(DESCRIPTION_SELECTOR).extract_first(),
            'price_whole': response.css(PRICE_WHOLE_SELECTOR).extract_first(),
            'price_fraction': response.css(PRICE_FRACTION_SELECTOR).extract_first(),
            'isbn_10': response.css(ISBN_10_SELECTOR).extract_first(),
            'isbn_13': response.css(ISBN_13_SELECTOR).extract_first(),
            'edition': response.css(EDITION_SELECTOR).extract_first(),
            'publisher': response.css(PUBLISHER_SELECTOR).extract_first(),
            'publication_date': response.css(PUBLICATION_DATE_SELECTOR).extract_first(),
            'language': response.css(LANGUAGE_SELECTOR).extract_first(),
            'dimensions': response.css(DIMENSIONS_SELECTOR).extract_first(),
            'print_length': response.css(PRINT_LENGTH_SELECTOR).extract_first(),
        }

        if all(not value for value in data.values()):
            yield Request(url=response.url, callback=self.parse, dont_filter=True)
        else:
            yield data