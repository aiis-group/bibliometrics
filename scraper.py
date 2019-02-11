from bs4 import BeautifulSoup
import urllib.request

def scholar_stats(url):
        html = _get_html(url)
        stats_table = html.find('table', {'id': "gsc_rsb_st"})

        if (stats_table):
            stats_row = stats_table.tbody.findAll('tr')
            cit = stats_row[0].findAll("td")
            hIndex = stats_row[1].findAll("td")
            i10 = stats_row[2].findAll("td")

            return {
                'citations': {'total': cit[1].get_text(), 'last5Years': cit[2].get_text()},
                'hIndex': {'total': hIndex[1].get_text(), 'last5Years': hIndex[2].get_text()},
                'i10': {'total': i10[1].get_text(), 'last5Years': i10[2].get_text()}
            }

        return None

def _get_html(url):
        with urllib.request.urlopen(url) as response:
                page = response.read()
        return BeautifulSoup(page, 'html.parser')