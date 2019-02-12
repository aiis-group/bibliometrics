from bs4 import BeautifulSoup
import urllib.request
import researcher

def get_scholar_stats(url):
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

def get_scholar_url(researcher):
        url = "https://scholar.google.es/citations?hl=es&view_op=search_authors&mauthors="
        url += "+".join(researcher.lower().split(" "))  
        url += "+ulpgc&btnG="
        html = get_html(url)

        researcher_panel = html.find('h3', {'class': "gsc_oai_name"})
        
        if (researcher_panel):
            scholar_url = researcher_panel.find('a')['href']
            return "https://scholar.google.es"+scholar_url

        return None


def get_html(url):
        with urllib.request.urlopen(url) as response:
                page = response.read()
        return BeautifulSoup(page, 'html.parser')

# print(get_scholar_url("Jose Miguel Santos"))