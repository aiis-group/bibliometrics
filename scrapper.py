from bs4 import BeautifulSoup
import urllib.request
import json
import sys


def getHTML(url):
        with urllib.request.urlopen(url) as response:
                page = response.read()
        return BeautifulSoup(page, 'html.parser')


def getStats(url):
        html = getHTML(url)
        stats = parseStats(html, 'table', {'id': "gsc_rsb_st"})
        return stats


def parseStats(html, item, attributes):
        stats = []

        stats = html.find_all(item, attrs=attributes)
        if len(stats) > 0:
                stats = stats[0].tbody
                stats = [getTD(stat) for stat in stats]
        return stats


def getTD(stat):
        text = [st.get_text() for st in stat]
        return { text[0]: {
                        "total" : text[1],
                        "last5Years": text[2]
                }
        }

