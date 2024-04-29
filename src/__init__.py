import tkinter as tk
from tkinter import ttk

from threading import Thread
from queue import Queue

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

from time import sleep

import logging
import warnings

# ---------------------------------- Logging --------------------------------- #

logging.basicConfig(level=logging.ERROR)
selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
selenium_logger.setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=FutureWarning, module="soupsieve")

# -------------------------------- Parameters -------------------------------- #

HEADERS = headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8"
}

MAX_RETRIES = 5
MAX_THREADS = 2
MAX_PAGES = 2

# ---------------------------------------------------------------------------- #
#                               Helper Functions                               #
# ---------------------------------------------------------------------------- #

def get_soup(url):
    for _ in range(MAX_RETRIES): 
        try:
            response = requests.get(url, headers=HEADERS)
            return BeautifulSoup(response.text, "lxml")
        except requests.exceptions.ConnectionError:
            sleep(5)
    return

def search(query):
    search_page = "https://www.amazon.co.uk/advanced-search/books"

    display = Xvfb()
    display.start()
    driver = webdriver.Firefox()

    driver.get(search_page)
    for selector, value in query.items():
        driver.find_element(By.CSS_SELECTOR, selector).send_keys(value)
    button = driver.find_element(By.CSS_SELECTOR, "table#asMain input[name='Adv-Srch-Books-Submit']")
    driver.execute_script("arguments[0].click();", button)

    WebDriverWait(driver, 10).until(url_changes(search_page))
    url = driver.current_url

    driver.quit()
    display.stop()

    return url

# ---------------------------------------------------------------------------- #
#                                     Main                                     #
# ---------------------------------------------------------------------------- #

class MysteryMachine(tk.Tk):
    def __init__(self):
        super().__init__()

        try:
            self.data = read_csv('scraps.csv')
        except FileNotFoundError:
            self.data = DataFrame()

        self.scrapes = Queue()
        for _ in range(MAX_THREADS):
            Thread(target=self.scraper, daemon=True).start()

        self.scrape_num = 0

        # ---------------------------------------------------------------------------- #
        #                                  Query Frame                                 #
        # ---------------------------------------------------------------------------- #

        query_frame = ttk.LabelFrame(self, text="Query")
        query_frame.grid(row=0, column=0)

        # --------------------------------- Keywords --------------------------------- #

        ttk.Label(query_frame, text="Keywords").grid(row=0, column=0, sticky="e")
        self.keywords_entry = ttk.Entry(query_frame, width=16)
        self.keywords_entry.grid(row=0, column=1, sticky="ew")

        # ---------------------------------- Author ---------------------------------- #

        ttk.Label(query_frame, text="Author").grid(row=1, column=0, sticky="e")
        self.author_entry = ttk.Entry(query_frame, width=16)
        self.author_entry.grid(row=1, column=1, sticky="ew")

        # ----------------------------------- Title ---------------------------------- #

        ttk.Label(query_frame, text="Title").grid(row=2, column=0, sticky="e")
        self.title_entry = ttk.Entry(query_frame, width=16)
        self.title_entry.grid(row=2, column=1, sticky="ew")

        # ---------------------------------- ISBN(s) --------------------------------- #

        ttk.Label(query_frame, text="ISBN(s)").grid(row=3, column=0, sticky="e")
        self.isbns_entry = ttk.Entry(query_frame, width=16)
        self.isbns_entry.grid(row=3, column=1, sticky="ew")

        # --------------------------------- Publisher -------------------------------- #

        ttk.Label(query_frame, text="Publisher").grid(row=4, column=0, sticky="e")
        self.publisher_entry = ttk.Entry(query_frame, width=16)
        self.publisher_entry.grid(row=4, column=1, sticky="ew")

        # ---------------------------------- Subject --------------------------------- #

        ttk.Label(query_frame, text="Subject").grid(row=5, column=0, sticky="e")
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
        self.subject_entry = ttk.Combobox(query_frame, width=16, values=self.subjects)
        self.subject_entry.grid(row=5, column=1, sticky="ew")
        self.subject_entry.set(self.subjects[0])

        # ---------------------------------- Format ---------------------------------- #

        ttk.Label(query_frame, text="Format").grid(row=0, column=2, sticky="e")
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
        self.format_entry = ttk.Combobox(query_frame, width=16, values=self.formats)
        self.format_entry.grid(row=0, column=3, sticky="ew")
        self.format_entry.set(self.formats[0])

        # ---------------------------------- Reader Age ------------------------------ #

        ttk.Label(query_frame, text="Reader Age").grid(row=1, column=2, sticky="e")
        self.reader_ages = [
            "Any Age",
            "0-2 years",
            "3-5 years",
            "6-8 years",
            "9-11 years",
            "12-16 years",
            "16+ years",
        ]
        self.reader_age_entry = ttk.Combobox(query_frame, width=16, values=self.reader_ages)
        self.reader_age_entry.grid(row=1, column=3, sticky="ew")
        self.reader_age_entry.set(self.reader_ages[0])

        # ---------------------------------- Seller ---------------------------------- #

        ttk.Label(query_frame, text="Seller").grid(row=2, column=2, sticky="e")
        self.seller_entry = ttk.Entry(query_frame, width=16)
        self.seller_entry.grid(row=2, column=3, sticky="ew")

        # ---------------------------------- Pub Date -------------------------------- #

        ttk.Label(query_frame, text="Pub Date").grid(row=3, column=2, sticky="e")
        date_frame = ttk.Frame(query_frame)
        date_frame.grid(row=3, column=3)

        self.pub_dates = [
            "All Dates",
            "Before",
            "During",
            "After"
        ]
        self.pub_date_entry = ttk.Combobox(date_frame, width=8)
        self.pub_date_entry.grid(row=0, column=1, sticky="ew")
        self.pub_date_entry.set(self.pub_dates[0])

        ttk.Label(date_frame, text="Month").grid(row=0, column=2, sticky="e")
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
        self.month_entry = ttk.Combobox(date_frame, width=4, values=self.months)
        self.month_entry.grid(row=0, column=3, sticky="ew")
        self.month_entry.set(self.months[0])

        ttk.Label(date_frame, text="Year").grid(row=0, column=4, sticky="e")
        self.year_entry = ttk.Entry(date_frame, width=4)
        self.year_entry.grid(row=0, column=5, sticky="ew")

        # ---------------------------------- Sort Results By ------------------------- #

        ttk.Label(query_frame, text="Sort Results By").grid(row=4, column=2, sticky="e")
        self.sort_options = [
            "",
            "Bestselling",
            "Price: Low to High",
            "Price: High to Low",
            "Avg. Customer Review",
            "Publication Date",
        ]
        self.sort_results_by_entry = ttk.Combobox(query_frame, width=16, values=self.sort_options)
        self.sort_results_by_entry.grid(row=4, column=3, sticky="ew")
        self.sort_results_by_entry.set(self.sort_options[0])

        # ---------------------------------------------------------------------------- #
        #                                  Queue Frame                                 #
        # ---------------------------------------------------------------------------- #

        queue_frame = ttk.LabelFrame(self, text="Scrapes")
        queue_frame.grid(row=0, column=1, rowspan=2, sticky="ns")

        self.queue_text = tk.Text(queue_frame, width=30, height=10)
        self.queue_text.grid(row=0, column=0)
        self.queue_text.tag_config("highlight", background="green")
        self.queue_text.configure(state='disabled')

        # ---------------------------------- Submit Button --------------------------- #

        self.submit_button = ttk.Button(text="Submit", command=self.add_scrape)
        self.submit_button.grid(row=1, column=0)

        # ------------------------------ Window Settings ----------------------------- #

        self.title("ScrapeyDoor")
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.geometry("")
        self.resizable(False, False)

    def add_scrape(self):
        self.scrape_num += 1
        id = self.scrape_num

        query = {
            "table#asMain input[name='field-keywords']": self.keywords_entry.get(),
            "table#asMain input[name='field-author']": self.author_entry.get(),
            "table#asMain input[name='field-title']": self.title_entry.get(),
            "table#asMain input[name='field-isbn']": self.isbns_entry.get(),
            "table#asMain input[name='field-publisher']": self.publisher_entry.get(),
            "table#asMain select[name='node']": self.subject_entry.get(),
            "table#asMain select[name='field-binding_browse-bin']": self.format_entry.get(),
            "table#asMain select[name='field-subject']": self.reader_age_entry.get(),
            "table#asMain select[name='emi']": self.seller_entry.get(),
            "table#asMain select[name='p_46']": self.pub_date_entry.get(),
            "table#asMain select[name='p_45']": self.month_entry.get(),
            "table#asMain input[name='p_47']": self.year_entry.get(),
            "table#asMain select[name='sort']": self.sort_results_by_entry.get(),
        }

        self.queue_text.configure(state='normal')
        self.queue_text.insert(f"{id}.0", f"#{id} queued...\n")
        self.queue_text.configure(state='disabled')

        self.scrapes.put((id, query))

    def scraper(self):
        while True:
            id, query = self.scrapes.get()

            self.queue_text.configure(state='normal')
            self.queue_text.delete(f"{id}.0", f"{id}.end")
            self.queue_text.insert(f"{id}.0", f"#{id} searching...")
            self.queue_text.configure(state='disabled')

            results_page = search(query)

            for page_num in range(MAX_PAGES):
                line_text = f"#{id} scraping...\t\tPg: {page_num+1}/{MAX_PAGES}"
                padding = ' ' * (self.queue_text['width'] - len(line_text)) 
                
                self.queue_text.configure(state='normal')
                self.queue_text.delete(f"{id}.0", f"{id}.end")
                self.queue_text.insert(f"{id}.0", line_text + padding)
                self.queue_text.configure(state='disabled')

                soup = get_soup(results_page)

                results = soup.select("[data-asin] h2 a")
                for i, result in enumerate(results):
                    highlight_length = int((i + 1) / len(results) * self.queue_text['width']) - 1

                    self.queue_text.configure(state='normal')
                    self.queue_text.tag_add("highlight", f"{id}.0", f"{id}.{highlight_length}")
                    self.queue_text.configure(state='disabled')

                    product_page = urljoin(results_page, result.attrs.get("href"))
                    self.data = concat([self.data, self.scrape(product_page)], ignore_index=True)
                    self.save_scrape()

                next = soup.select_one("a:contains('Next')")
                if next:
                    results_page = urljoin(results_page, next.attrs.get("href"))
                else:
                    break

            self.queue_text.configure(state='normal')
            self.queue_text.delete(f"{id}.0", f"{id}.end")
            self.queue_text.insert(f"{id}.0", f"#{id} complete!")
            self.queue_text.configure(state='disabled')

            self.scrapes.task_done()
    
    def scrape(self, url):
        soup = get_soup(url)

        def pull(selector, placeholder=""):
            try:
                return soup.select_one(selector).get_text().strip()
            except AttributeError:
                return placeholder

        return DataFrame([{
            "Title":                pull("#productTitle"),
            "Author":               pull("#bylineInfo > span > a"),
            "Description":          pull("#bookDescription_feature_div > div > div.a-expander-content.a-expander-partial-collapse-content > p"),
            "Price":                pull("span.a-price-whole") + pull("span.a-price-fraction"),

            "ISBN-10":              pull("#rpi-attribute-book_details-isbn10 > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span"),
            "ISBN-13":              pull("#rpi-attribute-book_details-isbn13 > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span"),
            "Edition":              pull("#rpi-attribute-book_details-edition > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span"),
            "Publisher":            pull("#rpi-attribute-book_details-publisher > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span"),
            "Publication Date":     pull("#rpi-attribute-book_details-publication_date > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span"),
            "Language":             pull("#rpi-attribute-language > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span"),
            "Dimensions":           pull("#rpi-attribute-book_details-dimensions > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span"),
            "Print Length":         pull("#rpi-attribute-book_details-fiona_pages > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span")
        }])
    
    def save_scrape(self):
        self.data.to_csv("scraps.csv", index=False)

# ---------------------------------------------------------------------------- #
#                                     Init                                     #
# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    mm = MysteryMachine()
    mm.mainloop()
