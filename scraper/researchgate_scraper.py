from .scraper import Scraper

class ResearchGateScraper(Scraper):

    def get_stats(self, url):
        html = self._get_html(url)

        if not html:
            return None

        about_section = html.find('div', {'id': "about"})

        if about_section:
            stats = html.findAll('div', {
                'class': "nova-e-text nova-e-text--size-xl nova-e-text--family-sans-serif nova-e-text--spacing-none nova-e-text--color-inherit"})
            if stats:
                stats = {
                    'researched_items': stats[0].get_text(),
                    'reads': stats[1].get_text(),
                    'citations': stats[2].get_text()
                }
            return stats

        return None

    def get_personal_data(self, url):
        html = self._get_html(url)
        personal_data = {}

        if not html:
            return None

        about_section = html.find('div', {'id': "about"})

        if not about_section:
            return None

        personal_info = html.find('div', {'class': "header-inner vcard"})

        if (personal_info):
            personal_info = personal_info.findAll('a')
            personal_data['university'] = personal_info[0].get_text()
            personal_data['department'] = personal_info[1].get_text()

        personal_info = html.find('div', {
            'class': "nova-o-grid__column nova-o-grid__column--width-4/12@xl-only nova-o-grid__column--width-5/12@m-up nova-o-grid__column--width-12/12@s-up"})

        if (personal_info):
            personal_info = personal_info.find('div', {
                'class': "nova-e-list__item nova-v-institution-item__info-section-list-item"})
            if personal_info:
                personal_data['position'] = personal_info.get_text()

        study_fields = html.findAll('a', {
            'class': "nova-e-badge nova-e-badge--color-grey nova-e-badge--display-block nova-e-badge--luminosity-medium nova-e-badge--size-l nova-e-badge--theme-ghost nova-e-badge--radius-full"})

        if (study_fields):
            study_fields = [study_field.get_text() for study_field in study_fields]

        if bool(personal_data) or study_fields:
            return {
                'personal_info': personal_data,
                'study_fields': study_fields
            }

        return None