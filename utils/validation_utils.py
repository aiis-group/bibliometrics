import re

def is_valid_rg_profile_url(url):
    """ Valid url example:  https://www.researchgate.net/profile/Javier_Sanchez11
    :return: True or False if the url is valid or not, respectively. """
    return re.match('https://www.researchgate.net/profile/[^ /]+', url)


def is_valid_scholar_profile_url(url):
    """ Valid url example: https://scholar.google.es/citations?user=E6pJ7VAAAAAJ&hl=es
    :return: True or False if the url is valid or not, respectively. """
    return re.match('^https://scholar.google.es/citations\?user=.*', url)
