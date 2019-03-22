# External modules
import urllib.request
from bs4 import BeautifulSoup

# Built-in modules
import logging
from abc import ABC, abstractmethod


class Scraper(ABC):
    """Abstract Base Class for Scrapers"""
    def __init__(self):
        self._last_petition = {"url": "", "html": ""}

    @abstractmethod
    def get_stats(self, url, force_refresh=False):
        pass

    @abstractmethod
    def get_articles(self, force_refresh=False):
        pass

    def _get_html(self, url, force_refresh=False):
        if self._last_petition['url'] == url and not force_refresh:
            return self._last_petition['html']

        self._last_petition["url"] = url
        request = urllib.request.Request(url)
        try:
            response = urllib.request.urlopen(request)
            html = BeautifulSoup(response.read(), 'html.parser')
            self._last_petition["html"] = html
            return html
        except urllib.error.HTTPError as err:
            logging.warning(str(err) + " - " + url)
            self._last_petition["html"] = None

        return None

