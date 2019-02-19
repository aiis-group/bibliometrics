import scraper.scholar_scraper as scraper
from persistence.data_writer import json_writer, csv_writer, xls_writer
from persistence.data_reader import cris_excel_reader as reader

def load_researchers():
    researchers = reader.load_researchers('./data/dataCRIS.xls', 'main_entities')

    researchers_in_scholar = [r for r in researchers if r.scholar_url]

    return (researchers, researchers_in_scholar)

    
    # GET SCHOLAR URL
    # print("Previous Researchers with Scholar", len(researchers_in_scholar), end="\n\n")
    
    # index = 0
    # size = len(researchers)
    # for researcher in researchers:
    #     print(f'\rAdding Scholar URL to Researchers ... [{index+1}/{size}]', end='')
    #     if not researcher.scholar_url:
    #         researcher.scholar_url = scraper.get_url(researcher.search_name())
    #     index += 1

    # print(f'\nLoad Completed! {index} researchers extracted')
    # print("After Researchers with Scholar", len(researchers_in_scholar), end="\n\n")


def scrap_scholars(researchers_in_scholar):
    size = len(researchers_in_scholar)
    for index, researcher in enumerate(researchers_in_scholar):
        print(f'\rScraping Google Scholar Stats... [{index}/{size}]', end='')
        researcher.scholar_data = scraper.get_data(researcher.scholar_url)
    print(f'\rScraping Google Scholar Stats... [{index}/{size}] Done!')
    return researchers_in_scholar

if __name__== "__main__":
    (researchers, researchers_in_scholar) = load_researchers()
    researchers = scrap_scholars(researchers_in_scholar)
    json_writer.store_researchers(researchers)
    csv_writer.store_researchers(researchers)
    xls_writer.store_researchers(researchers)


