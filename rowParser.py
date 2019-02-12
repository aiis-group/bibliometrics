import re

class CRISParser:
    @staticmethod
    def parse_full_name(row):
        name = _remove_parameters(row['fullName'])
        parts = name.split(', ')
        return {'firstName': parts[1], 'lastName': parts[0]}
    
    @staticmethod
    def parse_scholar_url(row):
        # FIXME: typo in generated xls: double 'o' in Scholar.
        return _extract_url(row['GoogleSchoolar'])

    @staticmethod
    def parse_research_gate_url(row):
        return _extract_url(row['researchgate'])

    @staticmethod
    def parse_uuid(row):
        return row['UUID']

    @staticmethod
    def parse_crisid(row):
        return row['CRISID']

    @staticmethod
    def parse_orcid(row):
        return _remove_parameters(row['orcid'])


# Utils
def _extract_url(text):
    if type(text) is not str: return None

    m = re.search('(?P<url>https?://[^\s]+)\](?!\])', text)
    return m.group('url') if m else None


def _remove_parameters(text):
    return re.sub('\[.*\]', "", text) if type(text) is str else None


