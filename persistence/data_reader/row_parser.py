import re

class CRISParser:

    def __init__(self, row):
        self.row = row
        
    def parse_full_name(self):
        name = remove_parameters(self.row['fullName'])
        parts = name.split(', ')
        return {'firstName': parts[1], 'lastName': parts[0]}
    
    def parse_scholar_url(self):
        # FIXME: typo in generated xls: double 'o' in Scholar.
        return extract_url(self.row['GoogleSchoolar'])

    def parse_research_gate_url(self):
        return extract_url(self.row['researchgate'])

    def parse_uuid(self):
        return self.row['UUID']

    def parse_crisid(self):
        return self.row['CRISID']

    def parse_orcid(self):
        return remove_parameters(self.row['orcid'])

# Utils
def extract_url(text):
    if type(text) is not str: return None

    m = re.search('(?P<url>https?://[^\s]+)\](?!\])', text)
    return m.group('url') if m else None

def remove_parameters(text):
    return re.sub('\[.*\]', "", text) if type(text) is str else None


