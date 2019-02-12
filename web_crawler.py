import scraper
import file_writer
import excel_crisdata_reader

def load_researchers():
    researchers = excel_crisdata_reader.extract_researchers('dataCRIS.xls', 'main_entities')

    researchers_in_scholar = [r for r in researchers if r.scholar_url]
    return (researchers, researchers_in_scholar)

def scrap_scholars(researchers_in_scholar):
    size = len(researchers_in_scholar)
    for index, researcher in enumerate(researchers_in_scholar):
        print(f'\rScraping Google Scholar Stats... [{index}/{size}]', end='')
        researcher.scholar_stats = scraper.get_scholar_stats(researcher.scholar_url)
        
        # # @TEST 
        # if index > 3:
        #     break

    print(f'\rScraping Google Scholar Stats... [{index}/{size}] Done!')

    # # @TEST
    # researchers = researchers[0:3]

if __name__== "__main__":
    (researchers, researchers_in_scholar) = load_researchers()
    print("\nResearchers with Scholar", len(researchers_in_scholar))
    # scrap_scholars(researchers_in_scholar)
    file_writer.write_researchers_json(researchers)


