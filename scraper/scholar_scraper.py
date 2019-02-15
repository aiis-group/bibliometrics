from bs4 import BeautifulSoup
import urllib.request
import model.researcher


def get_stats(url):
    html = get_html(url)
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


def get_personal_data(url):
    html = get_html(url)
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


def get_url(researcher_name):
    url = "https://scholar.google.es/citations?hl=es&view_op=search_authors&mauthors="
    url += "+".join(researcher_name.lower().split(" "))
    url += "+ulpgc&btnG="
    html = get_html(url)

    if html != None:
        researcher_panel = html.find('h3', {'class': "gsc_oai_name"})

        if (researcher_panel):
            scholar_url = researcher_panel.find('a')['href']
            return "https://scholar.google.es"+scholar_url

    return None


def get_html(url, headers=None):
    request = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(request)
        return BeautifulSoup(response.read(), 'html.parser')
    except urllib.error.HTTPError as err:
        print("\n", err)
