from bs4 import BeautifulSoup
import urllib.request
import model.researcher


def get_data(url):
    return {
        'personal_data': get_personal_data(url),
        'stats' : get_stats(url)
    }

def get_stats(url):
    html = get_html(url)
    stats_table = html.find('table', {'id': "gsc_rsb_st"})

    if (stats_table):
        stats_row = stats_table.tbody.findAll('tr')
        cit = stats_row[0].findAll("td")
        hIndex = stats_row[1].findAll("td")
        i10 = stats_row[2].findAll("td")

        return {
            'citations': {'total': int(cit[1].get_text()), 'last5Years': int(cit[2].get_text())},
            'hIndex': {'total': int(hIndex[1].get_text()), 'last5Years': int(hIndex[2].get_text())},
            'i10': {'total': int(i10[1].get_text()), 'last5Years': int(i10[2].get_text())}
        }

    return None


def get_personal_data(url):
    html = get_html(url)

    personal_info = html.find('div', {'id': "gsc_prf_i"})
    personal_data = None
    
    if (personal_info):
        personal_info = personal_info.find('div', {'class':'gsc_prf_il'})
        if personal_info:
            personal_data = personal_info.get_text()

    study_fields = html.find('div', {'id': "gsc_prf_int"})

    if (study_fields):
        study_fields = [study_field.get_text().lower() for study_field in study_fields.findAll('a')]
        return {
            'personal_info': personal_data,
            'study_fields': study_fields
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