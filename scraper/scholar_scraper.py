from bs4 import BeautifulSoup
import urllib.request
import logging


# Store the last url and html in order to evade multiple requests.
_last_petition = { "url": "", "html": ""}

def get_data(url):
    get_html(url)
    return {
        'personal_data': get_personal_data(url),
        'stats' : get_stats(url)
    }

def get_stats(url):
    html = get_html(url)

    if not html:
        return None

    stats_table = html.find('table', {'id': "gsc_rsb_st"})
    stats_hist = html.find('div', {'class': "gsc_md_hist_b"})

    if (stats_table):
        stats_row = stats_table.tbody.findAll('tr')
        cit = stats_row[0].findAll("td")
        hIndex = stats_row[1].findAll("td")
        i10 = stats_row[2].findAll("td")

        stats = {
            'citations': {'total': cit[1].get_text(),'last5Years': cit[2].get_text()},
            'hIndex': {'total': hIndex[1].get_text(), 'last5Years': hIndex[2].get_text()},
            'i10': {'total': i10[1].get_text(), 'last5Years': i10[2].get_text()}
        }

        # TODO Get the citations by year noticing the years with 0 citations (error: not in html)
        # if (stats_hist):
        #     hist_years = [year.get_text() for year in stats_hist.findAll('span', {'class': 'gsc_g_t'})]
        #     hist_stats = [year.get_text() for year in stats_hist.findAll('span', {'class': 'gsc_g_al'})]
        #     citations_hist = dict(zip(hist_years, hist_stats))

        #     stats["citationsByYear"] = citations_hist

        return stats 
    
    
    return None


def get_personal_data(url):
    html = get_html(url)

    if not html:
        return None

    personal_info = html.find('div', {'id': "gsc_prf_i"})
    personal_data = None
    
    if (personal_info):
        personal_info = personal_info.find('div', {'class':'gsc_prf_il'})
        if personal_info:
            personal_data = personal_info.get_text()

    study_fields = html.find('div', {'id': "gsc_prf_int"})

    if (study_fields):
        study_fields = [study_field.get_text() for study_field in study_fields.findAll('a')]
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


def get_html(url, cache_last=True):
    if _last_petition['url'] == url and cache_last:
        return _last_petition['html']

    request = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(request)
        html = BeautifulSoup(response.read(), 'html.parser')
        _last_petition["url"] = url
        _last_petition["html"] = html
        return html
    except urllib.error.HTTPError as err:
        print('\r', end='')
        logging.warning(err)