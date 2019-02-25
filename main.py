import scraper.scholar_scraper as scraper
from persistence.data_writer import json_writer, csv_writer, xls_writer
from persistence.data_reader import cris_excel_reader as reader
import time, sys, os, argparse


_input_file = './data/dataCRIS.xls'
_output_dir = './results'
_format = ['json', 'csv', 'xls']

def parseArgs():
    global _input_file, _output_dir, _format
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-i", "--input", required=False)
    parser.add_argument("-o", "--output", required=False)
    parser.add_argument("-f", "--format", required=False)
    parser.add_argument("-h", "--help", required=False, action="store_true")
    args = parser.parse_args()

    if args.help:
        basename = os.path.basename(__file__)
        print(f"Use: {basename} [h, -i input_file, -o output_dir]"
              "\n  h - show this help and exit."
              "\n  i input_file - CRIS input file (only xls for now)."
              "\n      default: ./data/dataCRIS.xls"
              "\n  o output_dir - output directory. Will be created if doesn't exist."
              "\n      default: ./results"
              "\n  f format - output format. Can be csv json or xls. Multiple option"
              "\n      default: \"csv,json,xls\"")
        exit(0)
    if args.input: _input_file = args.input
    if args.output: _output_dir = args.output
    if args.format: _format = args.format.split(",")
    print(_format)

if __name__== "__main__":
    parseArgs()

    if not os.path.exists(_output_dir):
        os.makedirs(_output_dir)
        print("Created: " + os.path.abspath(_output_dir))

    start = time.time()
    
    start_load = time.time()
    researchers = reader.load_researchers(_input_file, 'main_entities')
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
    if 'json' in _format:
        json_writer.store_researchers(researchers, _output_dir + "/researchers.json")
    if 'csv' in _format:
        csv_writer.store_researchers(researchers, _output_dir + "/researchers.csv")
    if 'xls' in _format:
        xls_writer.store_researchers(researchers, _output_dir + "/researchers.json")
    end_store = time.time()

    end = time.time()
    
    print("\nTiempos: \n")
    print("Tiempo total: ", time.strftime("%H:%M:%S", time.gmtime(end - start)))
    print("Tiempo de carga: ", time.strftime("%H:%M:%S", time.gmtime(end_load - start_load)))
    print("Tiempo de scrap: ", time.strftime("%H:%M:%S", time.gmtime(end_scrap - start_scrap)))
    print("Tiempo de guardado: ", time.strftime("%H:%M:%S", time.gmtime(end_store - start_store)))

