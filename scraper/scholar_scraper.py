from utils import utils
from .scraper import Scraper
from collections import OrderedDict


class ScholarScraper(Scraper):

    def get_stats(self, author_url, force_refresh=False):
        html = self.get_html(author_url, force_refresh)

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

    def get_personal_data(self, author_url, force_refresh=False):
        html = self.get_html(author_url, force_refresh)

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

    def get_articles(self, author_url, force_refresh=False):

        author_url += '&pagesize=100&cstart='
        articles_data = []

        for i in range(0, 15):
            
            idx = str(i)+'00'
            html = self.get_html(author_url + idx, force_refresh)

            if not html: return None

            articles_table = html.find('tbody', {'id': "gsc_a_b"})
            error_msg = articles_table.find('td', {'class': 'gsc_a_e'})

            if error_msg and error_msg.get_text() == "No hay ningún artículo en este perfil.":
                return articles_data

            if articles_table:
                for articles_row in articles_table.findAll('tr'):
                    article = articles_row.findAll("td")[0]
                    article_name = article.find('a').get_text()
                    citations = articles_row.findAll("td")[1]
                    year = articles_row.findAll("td")[2]

                    articles_data.append({
                            'name': article_name,
                            'authors': article.findAll('div')[0].get_text(),
                            'publisher': article.findAll('div')[1].get_text(),
                            'citations': citations.get_text(),
                            'published_at': year.get_text()
                        })


        return articles_data

    def get_researchers_from_search_result_page(self, url, force_refresh=False):
        html = self.get_html(url, force_refresh)

        authors = {}

        authors_elms = html.select('.gs_ai_t')
        if not authors_elms:
            raise Exception("captcha" if html.find(text="CAPTCHA") else "error")

        for author in authors_elms:
            scholar_url = author.select("h3 > a")[0]['href']
            scholar_id = utils.scholar_author_id_from_url(scholar_url)
            if scholar_id not in authors.keys():
                authors[scholar_id] = {
                    "name": author.select("h3 > a")[0].get_text(),
                    "affiliation": author.select(".gs_ai_aff")[0].get_text()
                }

        return authors
