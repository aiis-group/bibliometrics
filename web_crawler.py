import scraper
import file_writer
import excel_crisdata_reader

if __name__== "__main__":
    researchers = excel_crisdata_reader.extract_researchers('dataCRIS.xls', 'main_entities')

    res_in_scholar = [r for r in researchers if r.scholar_url]
    size = len(res_in_scholar)
    for index, r in enumerate(res_in_scholar):
        print(f'\rScraping Google Scholar Stats... [{index}/{size}]', end='')
        r.scholar_stats = scraper.scholar_stats(r.scholar_url)

    print(f'\rScraping Google Scholar Stats... [{index}/{size}] Done!')
    file_writer.write_researchers_json(researchers)