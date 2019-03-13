from scraper.scholar_scraper import ScholarScraper

if __name__ == "__main__":
    # Scraper instantiation
    scraper = ScholarScraper()

    # URL to scrap.
    url = "https://scholar.google.es/citations?user=ZveNB-8AAAAJ&hl=es"

    # Scraptime!
    personal_data = scraper.get_personal_data(url)
    stats = scraper.get_stats(url) # using cached html ;)!

    print(personal_data)
    print(stats)