import json
import scraper

class Researcher:
    def __init__(self, first_name, last_name, crisid, orcid=None, scholar_url=None,
                 rg_url=None ):
        self.crisid = crisid
        self.first_name = first_name
        self.last_name = last_name
        self.search_name = self.first_name +" "+ self.last_name.split(" ")[0]
        self.search_name = self.search_name.translate(str.maketrans('áéíóúü','aeiouu'))
        self.rg_url = rg_url
        self.orcid = orcid

        if scholar_url:
            self.scholar_url = scholar_url
        else:
            self.scholar_url = scraper.get_scholar_url(self.search_name)

        # set after initialization.
        self.scholar_stats = None
        

    def to_json_dict(self):
        """ A representation of this Researcher as a dict following JSON
        naming conventions without None values (JSON-Compatible dict) """

        data = {
            'firstName': self.first_name,
            'lastName': self.last_name,
            'crisID': self.crisid
        }

        if self.scholar_url:   data['googleScholarURL'] = self.scholar_url
        if self.rg_url:        data['researchGateURL'] = self.rg_url
        if self.orcid:         data['orcid'] = self.orcid
        if self.scholar_stats: data['scholarStats'] = self.scholar_stats

        return data