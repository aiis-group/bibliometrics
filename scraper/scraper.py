# External modules
import urllib.request
from bs4 import BeautifulSoup

# Built-in modules
import logging

class Scraper():
    """ Base class for Scrapers """
    def __init__(self):
        self._last_petition = {"url": "", "html": ""}


    def get_html(self, url, force_refresh=False):
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
