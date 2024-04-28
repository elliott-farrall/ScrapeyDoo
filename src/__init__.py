import tkinter as tk
from tkinter import ttk

from urllib.parse import urljoin
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import url_changes

from bs4 import BeautifulSoup
from pandas import DataFrame, read_csv, concat

from xvfbwrapper import Xvfb

from tqdm import tqdm

from time import sleep

import logging
import warnings

logging.basicConfig(level=logging.ERROR)
selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
selenium_logger.setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=FutureWarning, module="soupsieve")



class MysteryMachine:

    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8"
    }

    max_retries = 5
    page_limit = 2

    def __init__(self):
        try:
            self.data = read_csv('scraps.csv')
        except FileNotFoundError:
            self.data = DataFrame()

    def get_soup(self, url):
        for _ in range(self.max_retries): 
            try:
                response = requests.get(url, headers=self.headers)
                break 
            except requests.exceptions.ConnectionError:
                sleep(5)
        return BeautifulSoup(response.text, "lxml")
    
    def scrape_product(self, product_url):
        soup = self.get_soup(product_url)

        def get_selector(selector, placeholder=""):
            try:
                return soup.select_one(selector).get_text().strip()
            except AttributeError:
                return placeholder

        return DataFrame([{
            "Title":                get_selector("#productTitle"),
            "Author":               get_selector("#bylineInfo > span > a"),
            "Description":          get_selector("#bookDescription_feature_div > div > div.a-expander-content.a-expander-partial-collapse-content > p"),
            "Price":                get_selector("span.a-price-whole") + get_selector("span.a-price-fraction"),

            "ISBN-10":              get_selector("#rpi-attribute-book_details-isbn10 > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span"),
            "ISBN-13":              get_selector("#rpi-attribute-book_details-isbn13 > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span"),
            "Edition":              get_selector("#rpi-attribute-book_details-edition > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span"),
            "Publisher":            get_selector("#rpi-attribute-book_details-publisher > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span"),
            "Publication Date":     get_selector("#rpi-attribute-book_details-publication_date > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span"),
            "Language":             get_selector("#rpi-attribute-language > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span"),
            "Dimensions":           get_selector("#rpi-attribute-book_details-dimensions > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span"),
            "Print Length":         get_selector("#rpi-attribute-book_details-fiona_pages > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span")
        }])
    
    def scrape_search(self, search_url, page=1):
        print(f"Scraping page {page} of {self.page_limit}...")

        soup = self.get_soup(search_url)

        results = soup.select("[data-asin] h2 a")
        for result in tqdm(results):
            product_url = urljoin(search_url, result.attrs.get("href"))
            self.data = concat([self.data, self.scrape_product(product_url)], ignore_index=True)
            self.save_data()

        next = soup.select_one("a:contains('Next')")
        if next:
            next_url = urljoin(search_url, next.attrs.get("href"))

        if page < self.page_limit:
            self.scrape_search(next_url, page=page+1)
        else:
            print("Srape complete!")
    
    def get_search_url(self, query):
        initial_url = "https://www.amazon.co.uk/advanced-search/books"

        display = Xvfb()
        display.start()
        driver = webdriver.Firefox()
        driver.get(initial_url)

        for selector, value in query.items():
            driver.find_element(By.CSS_SELECTOR, selector).send_keys(value)
        button = driver.find_element(By.CSS_SELECTOR, "table#asMain input[name='Adv-Srch-Books-Submit']")
        driver.execute_script("arguments[0].click();", button)

        WebDriverWait(driver, 10).until(url_changes(initial_url))
        search_url = driver.current_url

        driver.quit()
        display.stop()

        return search_url
    
    def save_data(self):
        self.data.to_csv("scraps.csv", index=False)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ScrapeyDoor")

        self.style = ttk.Style()
        self.style.theme_use('clam')


        ttk.Label(self, text="Keywords").grid(row=0, column=0, sticky="e")
        self.keywords_entry = ttk.Entry(self, width=16)
        self.keywords_entry.grid(row=0, column=1, sticky="ew")

        ttk.Label(self, text="Author").grid(row=1, column=0, sticky="e")
        self.author_entry = ttk.Entry(self, width=16)
        self.author_entry.grid(row=1, column=1, sticky="ew")

        ttk.Label(self, text="Title").grid(row=2, column=0, sticky="e")
        self.title_entry = ttk.Entry(self, width=16)
        self.title_entry.grid(row=2, column=1, sticky="ew")

        ttk.Label(self, text="ISBN(s)").grid(row=3, column=0, sticky="e")
        self.isbns_entry = ttk.Entry(self, width=16)
        self.isbns_entry.grid(row=3, column=1, sticky="ew")

        ttk.Label(self, text="Publisher").grid(row=4, column=0, sticky="e")
        self.publisher_entry = ttk.Entry(self, width=16)
        self.publisher_entry.grid(row=4, column=1, sticky="ew")

        ttk.Label(self, text="Subject").grid(row=5, column=0, sticky="e")
        self.subjects = [
            "Any Subject",
            "Antiquarian, Rare & Collectable",
            "Art, Architecture & Photography",
            "Audio CDs",
            "Audio Cassettes",
            "Biography",
            "Business, Finance & Law",
            "Calendars, Diaries, Annuals & More",
            "Children's Books",
            "Comics & Graphic Novels",
            "Computing & Internet",
            "Crime, Thrillers & Mystery",
            "Fiction",
            "Food & Drink",
            "Gay & Lesbian",
            "Health, Family & Lifestyle",
            "History",
            "Home & Garden",
            "Horror",
            "Humour",
            "Languages",
            "Mind, Body & Spirit",
            "Music, Stage & Screen",
            "Poetry, Drama & Criticism",
            "Reference",
            "Religion & Spirituality",
            "Romance",
            "Science & Nature",
            "Science Fiction & Fantasy",
            "Scientific, Technical & Medical",
            "Society, Politics & Philosophy",
            "Sports, Hobbies & Games",
            "Study Books",
            "Travel & Holiday",
        ]
        self.subject_combobox = ttk.Combobox(self, width=16, values=self.subjects)
        self.subject_combobox.grid(row=5, column=1, sticky="ew")
        self.subject_combobox.set(self.subjects[0]) 
        

        ttk.Label(self, text="Format").grid(row=0, column=2, sticky="e")
        self.formats = [
            "Any Format",
            "Hardcover",
            "Paperback",
            "Kindle Books",
            "Audiobook Downloads",
            "Books on CD",
            "Books on Cassette",
            "Books on MP3 CD",
            "Preloaded Digital Audio Players",
        ]
        self.format_combobox = ttk.Combobox(self, width=16, values=self.formats)
        self.format_combobox.grid(row=0, column=3, sticky="ew")
        self.format_combobox.set(self.formats[0]) 

        ttk.Label(self, text="Reader Age").grid(row=1, column=2, sticky="e")
        self.reader_ages = [
            "Any Age",
            "0-2 years",
            "3-5 years",
            "6-8 years",
            "9-11 years",
            "12-16 years",
            "16+ years",
        ]
        self.reader_age_combobox = ttk.Combobox(self, width=16, values=self.reader_ages)
        self.reader_age_combobox.grid(row=1, column=3, sticky="ew")
        self.reader_age_combobox.set(self.reader_ages[0])

        ttk.Label(self, text="Seller").grid(row=2, column=2, sticky="e")
        self.seller_entry = ttk.Entry(self, width=16)
        self.seller_entry.grid(row=2, column=3, sticky="ew")

        ttk.Label(text="Pub. Date").grid(row=3, column=2, sticky="e")
        pub_date_frame = ttk.Frame(self, width=16)
        pub_date_frame.grid(row=3, column=3, sticky="ew")

        self.pub_dates = [
            "All Dates",
            "Before",
            "During",
            "After"
        ]
        self.pub_date_combobox = ttk.Combobox(pub_date_frame, width=8, values=self.pub_dates)
        self.pub_date_combobox.grid(row=0, column=1, sticky="ew")
        self.pub_date_combobox.set(self.pub_dates[0])

        ttk.Label(pub_date_frame, text="Month").grid(row=0, column=2, sticky="e")
        self.months = [
            "",
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec"
        ]
        self.month_combobox = ttk.Combobox(pub_date_frame, width=4, values=self.months)
        self.month_combobox.grid(row=0, column=3, sticky="ew")
        self.month_combobox.set(self.months[0])

        ttk.Label(pub_date_frame, text="Year").grid(row=0, column=4, sticky="e")
        self.year_entry = ttk.Entry(pub_date_frame, width=4)
        self.year_entry.grid(row=0, column=5, sticky="ew")

        ttk.Label(self, text="Sort Results by").grid(row=4, column=2, sticky="e")
        self.sort_options = [
            "",
            "Bestselling",
            "Price: Low to High",
            "Price: High to Low",
            "Avg. Customer Review",
            "Publication Date",
        ]
        self.sort_results_by_combobox = ttk.Combobox(self, width=16, values=self.sort_options)
        self.sort_results_by_combobox.grid(row=4, column=3, sticky="ew")
        self.sort_results_by_combobox.set(self.sort_options[0])


        self.submit_button = ttk.Button(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=6, column=0, columnspan=4)


        self.resizable(False, False)
        self.geometry("")

    def submit(self):
        query = {
            "table#asMain input[name='field-keywords']": self.keywords_entry.get(),
            "table#asMain input[name='field-author']": self.author_entry.get(),
            "table#asMain input[name='field-title']": self.title_entry.get(),
            "table#asMain input[name='field-isbn']": self.isbns_entry.get(),
            "table#asMain input[name='field-publisher']": self.publisher_entry.get(),
            "table#asMain select[name='node']": self.subject_combobox.get(),

            "table#asMain select[name='field-binding_browse-bin']": self.format_combobox.get(),
            "table#asMain select[name='field-subject']": self.reader_age_combobox.get(),
            "table#asMain select[name='emi']": self.seller_entry.get(),
            "table#asMain select[name='p_46']": self.pub_date_combobox.get(),
            "table#asMain select[name='p_45']": self.month_combobox.get(),
            "table#asMain input[name='p_47']": self.year_entry.get(),
            "table#asMain select[name='sort']": self.sort_results_by_combobox.get(),
        }

        search_url = mm.get_search_url(query)
        mm.scrape_search(search_url)
        mm.save_data()



if __name__ == "__main__":
    mm = MysteryMachine()

    app = App()
    app.mainloop()
