# Description: Simple web crawler
# Author: Dragos Petrut Marin
# Version: 1.0

import re
import requests
import urllib.request
from pywebcopy import save_webpage
from urllib.parse import urlparse


class SimpleCrawler:
    """Simple web crawler. It downloads webpages in the current folder.

    Attributes:
        source    The starting URL to begin with
        remained  The number of URLs left to be crawled
        visited   The URLs which have been visited so far
        queue     The URLs which have yet to be visited
        fetched   The number of URLs successfully fetched so far
        cnt       The number of URLS visited so far (including failures)
    """

    visited = []
    queue = []
    fetched = 0
    cnt = 0

    def __init__(self, source='https://news.ycombinator.com', remained=100):
        self.source = source
        self.remained = remained

    @staticmethod
    def download_webpage(url):
        """Downloads the webpage from the given URL.

        Parameters:
        url (str): The URL of the webpage
        """

        if (url[4] == 's'):
            start = 8
        else:
            start = 7

        modified_url = ""
        for i in range(start, len(url)):
            if (re.search("[\/:*?|<>]", url[i]) is not None):
                modified_url = modified_url + '%'
            else:
                modified_url = modified_url + url[i]

        modified_url = modified_url + ".html"
        r = requests.get(url, allow_redirects=True)
        open(modified_url, 'wb').write(r.content)

    @staticmethod
    def can_access(url):
        """Checks if a given URL can be accessed or not.
        """

        try:
            html = requests.get(url)
        except Exception as e:
            return False
        return True

    def get_new_urls(self, url):
        """Adds the unvisited webpages linked to from the given URL to queue
        """

        html = requests.get(url)
        parsed = html.content.decode('latin-1')
        links = re.findall('href=\"http(.*?)\"', parsed)
        for curr_link in links:
            curr_link = "http" + curr_link
            if curr_link not in self.visited:
                self.visited.append(curr_link)
                self.queue.append(curr_link)

    def crawl(self):
        """The actual crawling of the webpages.
        """

        self.queue.append(self.source)
        self.visited.append(self.source)
        while (self.remained > 0):
            curr_webpage = self.queue[self.cnt]
            self.cnt = self.cnt + 1

            if (self.can_access(curr_webpage) is True):
                self.download_webpage(curr_webpage)
                self.remained = self.remained - 1
                self.fetched = self.fetched + 1
                self.get_new_urls(curr_webpage)
                print (str(self.fetched) + ": " + curr_webpage)

            if (self.remained > 0 and self.cnt >= len(self.queue)):
                print("Too few URLs! Try with another source URL.")
                break


def readInput():
    source = str(input("Enter the starting URL: "))
    source = source.strip()

    while (SimpleCrawler.can_access(source) is False):
        source = str(input("Try another starting URL: "))
        source = source.strip()
    return source

source = readInput()
mycrawler = SimpleCrawler(source)
mycrawler.crawl()
input("Press enter to exit ...")
