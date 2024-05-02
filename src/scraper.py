import tkinter as tk
from tkinter import ttk

import atexit
import os
import sys
import json

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.results_spider import ResultsSpider

# ---------------------------------------------------------------------------- #
#                                   Interface                                  #
# ---------------------------------------------------------------------------- #

class Progress(tk.Text):
    def __init__(self, master=None, colour='green'):
        if master is not None:
            super().__init__(master, state='disabled', height=1)
        else:
            super().__init__(state='disabled', height=1)
        self.tag_config('highlight', background=colour)

    def update(self, value=None, text=None):
        self.config(state='normal')

        self.delete('1.0', tk.END)
        if text is not None:
            self.insert(tk.END, f"{text : ^{self['width']}}")
        if value is not None:
            self.tag_add('highlight', '1.0', f"1.{int(value * self['width'])}")

        self.config(state='disabled')
        self.master.update()

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.draw()
        self.update()

        self.protocol("WM_DELETE_WINDOW", self.exit)
        atexit.register(self.exit)

        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'settings')
        self.process = CrawlerProcess(get_project_settings())
        self.process.crawl(ResultsSpider, query=query, progress_bar=self.progress_bar)
        self.process.start()

        self.destroy()

    def draw(self):
        self.progress_bar = Progress(self, colour='green')
        self.progress_bar.grid(row=0, column=0)

        self.cancel_button = ttk.Button(text="Cancel", command=self.exit)
        self.cancel_button.grid(row=1, column=0)

        self.title("ScrapeyDoor")
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.geometry("")
        self.resizable(False, False)

    def exit(self):
        os._exit(0)
        
# ---------------------------------------------------------------------------- #
#                                     Init                                     #
# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    query = json.loads(sys.argv[1])

    win = Window()
    win.mainloop()