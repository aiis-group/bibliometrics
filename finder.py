# External modules
import urllib.request
from bs4 import BeautifulSoup
from firebase.database import DataBase

# Built-in modules
import logging, re, json, datetime
from datetime import datetime as dt
from os import rename, path

# Local
from scraper.scholar_scraper import ScholarScraper
from scraper.scraper import Scraper
from utils import utils
from firebase import finder_db_api

# Built-in
import argparse, os
from enum import Enum

class Finder:
    """This class provide methods to find new researchers in Scholar:
    1. Search by organization code
       (ie: 15669781497478426561 for University of Las Palmas).
    2. Search by keywords, like
       'ulpgc' or 'universidad de las palmas de gran canaria'
    About keywords: Google translate keywords to English when search
    (ie: universidad -> university) but not english to another language. So is
    better to use original language.
    """

    class Code(Enum):
        OK = "OK"

        SEARCH_FINISHED_ERROR = (
            "Can not resume a finished search. Start new search "
            "with new_search=True"
        )

        SEARCH_NOT_STARTED_ERROR = (
            "Can not resume. Search not started. Use search_by_keywords or "
            "search_by_organization_code first."
        )

        SEARCH_ACTIVE_ERROR = (
            "There is a search in progress. To start a new search and discard"
            " the current one, instantiate Finder with new_search=True."
        )

        WAIT_ERROR = ("Can't resume. There is a wait lock due to a pause in "
                      "previous session. Check wait_until.")

        LIMIT_REACHED = "Limit of pages to scrap reached"
        CAPTCHA_PROMPTED = "Captcha prompted during scrap"
        ERROR = "Unlisted error while scraping. See logs."

        def __str__(self):
            return self.name + ": " + self.value


    def __init__(self, new_search=False, current_ids=None,
                 pages_per_round=None, minutes_between_rounds=180):
        if not current_ids:
            self.current_ids = DataBase().getAllScholarIds()

        if new_search:
            finder_db_api.discardLast()

            self.current = {
                "created_at": dt.now().strftime("%d/%m/%Y %H:%M:%S"),
                "minutes_between_rounds": minutes_between_rounds,
                "current_page": 0,
                "scraped_pages": 0,
                "after_author": "",
                "status": "not_started",
                "wait_until": "01/01/1999 00:00:00",
                "total_researchers": 0,
                "new_researchers": {}
            }

            if pages_per_round: self.current['pages_per_round'] = pages_per_round

            finder_db_api.setCurrentSearch(self.current)

        else:
            self.current = finder_db_api.getCurrentSearch()

            if not self.current:
                raise Exception("There is not a search to resume.")

        self._scraper = ScholarScraper()

    def search_by_keywords(self, keywords):
        if self.current['status'] != "not_started":
            return Finder.Code.SEARCH_ACTIVE_ERROR

        self.current['search_by'] = "keywords"
        self.current['keywords'] = keywords
        self.current['current_keyword'] = keywords[0]
        self.current['status'] = "searching"
        return self.resume_search()

    def search_by_organization_code(self, organization_code):
        if self.current['status'] != "not_started":
            return Finder.Code.SEARCH_ACTIVE_ERROR

        self.current['search_by'] = "organization_code"
        self.current['organization_code'] = organization_code
        self.current['status'] = "searching"
        return self.resume_search()

    def batch_search(self):
        if self.current['status'] != "not_started":
            return Finder.Code.SEARCH_ACTIVE_ERROR

        self.current['search_by'] = "batch"
        self.current['status'] = "searching"
        return self.resume_search()

    def resume_search(self):

        ########################################################################
        #                           STATUS CHECK                               #
        ########################################################################
        # Finished?
        if self.current['status'] == "finished":
            return Finder.Code.SEARCH_FINISHED_ERROR

        # Not started?
        if self.current['status'] == "not_started":
            return Finder.Code.SEARCH_NOT_STARTED_ERROR

        # Waiting?
        wait_until = dt.strptime(self.current['wait_until'],"%d/%m/%Y %H:%M:%S")
        now = dt.now()
        if now < wait_until:
            return Finder.Code.WAIT_ERROR
        # -------------------------------------------------------------------- #

        # Can resume.
        # Reset pages_per_round counter if used and exceeded in last search.
        if ('pages_per_round' in self.current and
              self.current['scraped_pages'] >= self.current['pages_per_round']):
            self.current['scraped_pages'] = 0

        # TODO: split next if-else's content in 3 method calls.

        ########################################################################
        #                    RESUME SEARCH BY KEYWORDS                         #
        ########################################################################
        if self.current['search_by'] == 'keywords':
            current_kw_pos = self.current['keywords'].index(
                self.current['current_keyword']
            )

            for kw in self.current['keywords'][current_kw_pos:]:
                url_base = ("https://scholar.google.es/citations?"
                            "view_op=search_authors"
                            "&mauthors=%s") % kw.replace(" ", "+")

                self.current['current_keyword'] = kw
                res = self._search(url_base)

                if res != Finder.Code.OK:
                    print(res)
                    self._pause()

                    break

                self.current['current_page'] = 0
                self.current['after_author'] = ""

        ########################################################################
        #                 RESUME SEARCH ORGANIZATION CODE                      #
        ########################################################################
        elif self.current['search_by'] == 'organization_code':
            url_base = ("https://scholar.google.es/citations"
                        "?view_op=view_org"
                        "&org=" + self.current['organization_code'])

            self._search(url_base)

        ########################################################################
        #                      RESUME BATCH SEARCH                             #
        ########################################################################
        else:
            org_codes = finder_db_api.getOrganizationCodes()
            current_org_code_pos = (org_codes.index(
                self.current['current_organization_code']) if
                'current_organization_code' in self.current else 0)

            if "organization_results" not in self.current:
                self.current['organization_results'] = {}

            for org_code in org_codes[current_org_code_pos:]:
                url_base = ("https://scholar.google.es/citations"
                            "?view_op=view_org"
                            "&org=" + org_code)

                self.current['current_organization_code'] = org_code
                res = self._search(url_base)

                if res != Finder.Code.OK:
                    print(res)
                    self._pause()
                    break

                self.current["organization_results"][org_code] = {
                    "total_researchers": self.current['total_researchers'],
                    "new_researchers": self.current['new_researchers']
                }
                self.current['new_researchers'] = {}
                self.current['total_researchers'] = 0
                self.current['current_page'] = 0
                self.current['after_author'] = ""

            finder_db_api.updateCurrentSearch(self.current)

    def _pause(self):
        self.current['wait_until'] = (dt.now() + datetime.timedelta(
            minutes=self.current['minutes_between_rounds']
        )).strftime("%d/%m/%Y %H:%M:%S")

        print("Search paused. It can be resumed after " +
              self.current['wait_until'] +
              ". Resume can be forced using --force option.")
        finder_db_api.updateOnlyStatus(self.current)


    def _search(self, url_base):
        """ Search along pages. Require a base URL including
        search type parameters. Write in current['new_researchers']
        new researchers with scholar id as key and a dict as value. Dict format:
        {name: (...), affiliation: (...)}

        @:param url_base url containing ONLY search type parameters.
          · By keywords:
             > view_op=search_authors
             > mauthors=<keyword>

             Example:
               https://scholar.google.es/citations?view_op=search_authors&mauthors=ulpgc

          · By organization code:
             > view_op=view_org
             > org=<organization_code>

             Example
               https://scholar.google.es/citations?view_op=view_org&org=15669781497478426561

        @:return a Finder.Code.
        """
        # print("Searching by %s '%s'" %
        #       (st['search_by'],
        #        st['current_keyword'] if st['search_by'] == 'keywords'
        #                              else st['organization_code']))

        url = url_base
        if self.current['current_page'] != 0:
            url += "&after_author=" + self.current['after_author']
            url += "&astart=" + str(10*self.current['current_page'])

        codes = ("finished", "error", "captcha")
        page_limited = 'pages_per_round' in self.current

        # Scrap until finish, error or captcha. Additionally stop if scraped
        # pages counter reach the page per rounds limit (if set).
        res = self._scrap_page(url)
        while (res and res not in codes
               and (not page_limited or
                    self.current['scraped_pages'] < self.current['pages_per_round'])):

            self.current['current_page'] += 1
            self.current['scraped_pages'] += 1
            self.current['after_author'] = res
            url = (url_base
                   + "&after_author=" + res
                   + "&astart=" + str(10*self.current['current_page']))
            finder_db_api.updateOnlyStatus(self.current)
            res = self._scrap_page(url)

        if page_limited and self.current['scraped_pages'] >= self.current['pages_per_round']:
            return Finder.Code.LIMIT_REACHED

        if res in codes and res != "finished":
            return (Finder.Code.CAPTCHA_PROMPTED if res == "captcha"
                    else Finder.Code.ERROR)

        return Finder.Code.OK

    def _scrap_page(self, url):
        """ Scrap page. Add new researchers to current search dict.
        :returns a String with the after author token, a """
        print("\nCurrent page: %s    After author token: %s" %
              (self.current['current_page'], self.current['after_author']))

        html = self._scraper.get_html(url)
        if not html: return None
        try: authors = self._scraper.get_researchers_from_search_result_page(url)
        except Exception as e:
            return str(e)

        news = {}
        for scholar_id, author in authors.items():
            if (scholar_id not in self.current_ids
                    and scholar_id not in self.current['new_researchers']):
                news[scholar_id] = author
                self.current['new_researchers'][scholar_id] = author

        finder_db_api.addNewAuthors(news)
        self.current['total_researchers'] += len(authors.items())

        next_button = html.select(".gs_btnPR")[0]
        if not next_button.has_attr("disabled"):
            onclick = next_button['onclick']
            pattern = ".*after_author\\\\x3d(.*?)\\\\.*"
            match = re.match(pattern, onclick)
            if match:
                return match.group(1) # after_author

            return "error"

        return "finished"

def printHelp():
    basename = os.path.basename(__file__)
    print(
      "Use: %s" % basename,
      "\n[-h, --help] - show this help and exit."
      "\n\n[--batch] - start a batch search for every organization registered "
      "in the organizations collection"
      
      "\n\n[--repeat] <interval> - After finish an --auto search, repeat after "
      "interval minutes."
      
      "\n\n[--oc] <code> - Start new search by organization code discarding the"
      " current one if there is. If neither --oc nor --search-by "
      "options are used, try to resume current search if there is."
      
      "\n\n[--search-by] <terms> - Search for each quoted term."
      "\n Example: --search-by \"chronic pancreatitis ulpgc\" \"ull\""
      "\n NOTE: each quoted is treated independently and generates its own "
      "search. In the example, \"ull\" are not related with \"chronic "
      "pancreatitis ulpgc\""
      
      "\n\n[--pages] <pages> - Number of pages scraped before pause. No page "
      "limit if -1. By default use the last known value for current search if "
      "resume or -1 if new search."
      
      "\n\n[--wait-time] <minutes> - Wait time if error or captcha. If error "
      "the search can't not be resumed until <minutes> have passed. By default "
      "use the last known value for current search if resumed or 180 if new "
      "search."
      
      "\n[--force] - If there is a wait restriction when resume, ignore it."
      
      "\n[--max-tries] - How many consecutive times try to resume a search "
      "before discard it. By the default use the last known value for current "
      "search if resumed or 3 if new search."
    )


_mode = None
_org_code = None
_keywords = None

def parseArgs():
    global _mode, _org_code, _keywords
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "--help", required=False, action="store_true")
    parser.add_argument("--oc", required=False)
    parser.add_argument("--search-by", required=False)
    parser.add_argument("--batch", required=False, action="store_true")
    args = parser.parse_args()

    if args.oc:
        _mode = "by_organization_code"
        _org_code = args.oc

    elif args.search_by:
        _mode = "by_keywords"
        _keywords = [x.strip() for x in args.search_by.split(";;")]

    if args.help:
        printHelp()
        exit(0)

    if args.batch:
        _mode = "batch"

    # print(args.oc)


if __name__ == "__main__":
    parseArgs()

    # New search if mode selected. Resume if not.
    finder = Finder(new_search=(_mode is not None))

    result: Finder.Code
    if _mode is not None:
        finder = Finder(new_search=True)

        if _mode == 'batch':
            result = finder.batch_search()
        elif _mode == 'by_organization_code':
            result = finder.search_by_organization_code(_org_code)
        else:
            result = finder.search_by_keywords(_keywords)

    else:
        result = finder.resume_search()

    print(result)
    # finder = Finder(new_search=True)
    # finder.search_by_organization_code("15669781497478426561")



