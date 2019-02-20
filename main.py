import scraper.scholar_scraper as scraper
from persistence.data_writer import json_writer, csv_writer, xls_writer
from persistence.data_reader import cris_excel_reader as reader
import time
   
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

if __name__== "__main__":
    start = time.time()
    
    start_load = time.time()
    researchers = reader.load_researchers('./data/dataCRIS.xls', 'main_entities')
    end_load = time.time()

    start_scrap = time.time()
    researchers_in_scholar = [r for r in researchers if r.scholar_url]
    size = len(researchers_in_scholar)
    for index, researcher in enumerate(researchers_in_scholar):
        print(f'\rScraping Google Scholar Stats... [{index}/{size}]', end='')
        researcher.scholar_data = scraper.get_data(researcher.scholar_url)
    print(f'\rScraping Google Scholar Stats... [{index}/{size}] Done!')
    end_scrap = time.time()
    
    start_store = time.time()
    json_writer.store_researchers(researchers)
    csv_writer.store_researchers(researchers)
    xls_writer.store_researchers(researchers)
    end_store = time.time()

    end = time.time()
    
    print("\nTiempos: \n")
    print("Tiempo total: ", str(end - start))
    print("Tiempo de carga: ", str(end_load - start_load))
    print("Tiempo de scrap: ", str(end_scrap - start_scrap))
    print("Tiempo de guardado: ", str(end_store - start_store))

