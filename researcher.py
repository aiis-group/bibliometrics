import json

class Researcher:
    def __init__(self, first_name, last_name, crisid, orcid=None, scholar_url=None,
                 rg_url=None ):
        self.crisid = crisid
        self.first_name = first_name
        self.last_name = last_name
        self.scholar_url = scholar_url
        self.rg_url = rg_url
        self.orcid = orcid

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