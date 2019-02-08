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
        stats = stats[0].tbody

        stats = [getTD(stat) for stat in stats]

        print(stats)
        return stats


def getTD(stat):
        return [st.get_text() for st in stat]


# getProfiles('https://scholar.google.es/citations?view_op=view_org&hl=es&org=15669781497478426561&')

getStats('https://scholar.google.es/citations?user=fchj-TAAAAAJ&hl=es')
