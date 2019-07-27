import re


def is_valid_rg_profile_url(url):
    """ Valid url example:
        https://www.researchgate.net/profile/Javier_Sanchez11
    :return True or False if the url is valid or not, respectively. """
    return re.match('https://www\.researchgate\.net/profile/[^ /]+', url)


def is_valid_scholar_profile_url(url):
    """ Valid url example:
        https://scholar.google.es/citations?user=E6pJ7VAAAAAJ&hl=es
    :return True or False if the url is valid or not, respectively. """
    return re.match('^https://scholar\.google\..{2,4}/citations\?.*user=.*',
                    url)


def scholar_author_id_from_url(scholar_url):
    """ :return user arg from URL (author ID in scholar's URLs). """
    rematch = re.match(".*[?&]user=(.*?)($|&)", scholar_url)
    return rematch.group(1)
