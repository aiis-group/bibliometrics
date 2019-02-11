import re
import pandas as pd
from researcher import Researcher

def extract_researchers(file, sheet_name='main_entities'):
    df = pd.read_excel(file, sheet_name=sheet_name)

    researchers = []
    for index, row in df.iterrows():
        rp = _RowParser(row)
        name = rp.parse_full_name()
        rs = Researcher(name['firstName'], name['lastName'], rp.parse_crisid(),
                       scholar_url=rp.parse_scholar_url(), orcid=rp.parse_orcid(),
                       rg_url=rp.parse_research_gate_url())

        researchers.append(rs)

    return researchers


class _RowParser:
    def __init__(self, row):
        self.row = row

    def parse_full_name(self):
        name = _remove_parameters(self.row['fullName'])
        parts = name.split(', ')
        return {'firstName': parts[1], 'lastName': parts[0]}

    def parse_scholar_url(self):
        # FIXME: typo in generated xls: double 'o' in Scholar.
        return _extract_url(self.row['GoogleSchoolar'])

    def parse_research_gate_url(self):
        return _extract_url(self.row['researchgate'])

    def parse_uuid(self):
        return self.row['UUID']

    def parse_crisid(self):
        return self.row['CRISID']

    def parse_orcid(self):
        return _remove_parameters(self.row['orcid'])


# Utils
def _extract_url(text):
    if type(text) is not str: return None

    m = re.search('(?P<url>https?://[^\s]+)\](?!\])', text)
    return m.group('url') if m else None


def _remove_parameters(text):
    return re.sub('\[.*\]', "", text) if type(text) is str else None


