from .scraper import Scraper
from collections import OrderedDict

class ScholarScraper(Scraper):

    def get_stats(self, url, force_refresh=False):
        html = self._get_html(url, force_refresh)

        if not html: return None

        stats_table = html.find('table', {'id': "gsc_rsb_st"})
        stats_hist = html.find('div', {'class': "gsc_md_hist_b"})

        if stats_table:
            stats_row = stats_table.tbody.findAll('tr')
            cit = stats_row[0].findAll("td")
            hIndex = stats_row[1].findAll("td")
            i10 = stats_row[2].findAll("td")

            stats = {
                'citations': {'total': cit[1].get_text(), 'last5Years': cit[2].get_text()},
                'hIndex': {'total': hIndex[1].get_text(), 'last5Years': hIndex[2].get_text()},
                'i10': {'total': i10[1].get_text(), 'last5Years': i10[2].get_text()}
            }

            if stats_hist:
                last_year = int(stats_hist.findAll('span', {'class': 'gsc_g_t'})[-1].get_text()) + 1
                citations = stats_hist.findAll('a', {'class': 'gsc_g_a'})

                citations_per_year = {}

                # get all citations per year
                for a in citations:
                    z_index = int(a.get_attribute_list('style')[0].split(':')[-1])
                    citations_per_year[str(last_year - z_index)] = a.find("span").get_text()

                # add years with 0
                z_index = int(citations[0].get_attribute_list('style')[0].split(':')[-1])  # first year
                first_year = last_year - z_index

                for year in range(first_year, last_year, 1):
                    if str(year) not in citations_per_year:
                        citations_per_year[str(year)] = '0'

                stats["citationsPerYear"] = OrderedDict(sorted(citations_per_year.items()))

            return stats

        return None


    def get_personal_data(self, url, force_refresh=False):
        html = self._get_html(url, force_refresh)

        if not html:
            return None

        personal_info = html.find('div', {'id': "gsc_prf_i"})
        personal_data = None

        if (personal_info):
            personal_info = personal_info.find('div', {'class': 'gsc_prf_il'})
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




# TODO (Futuro) buscar la URL de Scholar del investigador/a si no tiene.
#       Requiere cuidado con captchas.
# def get_url(researcher_name):
#     url = "https://scholar.google.es/citations?hl=es&view_op=search_authors&mauthors="
#     url += "+".join(researcher_name.lower().split(" "))
#     url += "+ulpgc&btnG="
#     html = get_html(url)
#
#     if html != None:
#         researcher_panel = html.find('h3', {'class': "gsc_oai_name"})
#
#         if (researcher_panel):
#             scholar_url = researcher_panel.find('a')['href']
#             return "https://scholar.google.es"+scholar_url
#
#     return None
