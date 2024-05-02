import tkinter as tk
from tkinter import ttk

import atexit
import os
import sys
import json

from subprocess import Popen

# ---------------------------------------------------------------------------- #
#                                     Main                                     #
# ---------------------------------------------------------------------------- #

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.scrapes = []

        self.protocol("WM_DELETE_WINDOW", self.exit)
        atexit.register(self.exit)

        self.draw()

    def draw(self):
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
            "Baby-3 Years",
            "4-8 Years",
            "9-12 Years",
            "Teen",
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
        self.pub_date_entry = ttk.Combobox(date_frame, width=8, values=self.pub_dates)
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

        # ---------------------------------- Submit Button --------------------------- #

        self.submit_button = ttk.Button(text="Submit", command=self.scrape)
        self.submit_button.grid(row=1, column=0)

        # ------------------------------ Window Settings ----------------------------- #

        self.title("ScrapeyDoor")
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.geometry("")
        self.resizable(False, False)

    def scrape(self):
        query = {
            'field-keywords': self.keywords_entry.get(),
            'field-author': self.author_entry.get(),
            'field-title': self.title_entry.get(),
            'field-isbn': self.isbns_entry.get(),
            'field-publisher': self.publisher_entry.get(),
            'node': self.subject_entry.get(),
            'field-binding_browse-bin': self.format_entry.get(),
            'field-subject': self.reader_age_entry.get(),
            'emi': self.seller_entry.get(),
            'p_46': self.pub_date_entry.get(),
            'p_45': self.month_entry.get(),
            'p_47': self.year_entry.get(),
            'sort': self.sort_results_by_entry.get(),
        }
        self.scrapes.append(Popen([sys.executable, "scraper.py", json.dumps(query)]))

    def exit(self):
        for scrape in self.scrapes:
            scrape.kill()
        os._exit(0)

# ---------------------------------------------------------------------------- #
#                                     Init                                     #
# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    log = "ScrapeyDoo.log"
    if os.path.exists(log):
        os.remove(log)

    app = App()
    app.mainloop()

