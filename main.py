import scraper.scholar_scraper as scraper
from persistence.data_writer import json_writer, csv_writer, xls_writer
from persistence.data_reader import cris_excel_reader as reader
import time, sys, os, argparse, logging

_input_file = './data/dataCRIS.xls'
_output_dir = './results'
_log_file = None
_format = ['json', 'csv', 'xls']

def parseArgs():
    global _input_file, _output_dir, _format, _log_file
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-i", "--input", required=False)
    parser.add_argument("-o", "--output", required=False)
    parser.add_argument("-f", "--format", required=False)
    parser.add_argument("-h", "--help", required=False, action="store_true")
    parser.add_argument("-l", "--log", required=False)
    args = parser.parse_args()

    if args.help:
        basename = os.path.basename(__file__)
        print("Use: %s [h, -i input_file, -o output_dir]" % basename,
              "\n  [-h --help] - show this help and exit.",
              "\n  [-i --input] input_file - CRIS input file (only xls for now).",
              "\n      default: ./data/dataCRIS.xls",
              "\n  [-o --output] output_dir - output directory. Will be created if doesn't exist.",
              "\n      default: ./results",
              "\n  [-f --format] output_format - output format. Can be csv, json or xls. Multiple option",
              "\n      default: \"csv,json,xls\"",
              "\n  [-l --log] filename - output log file. FIle logging disabled by default")
        exit(0)
    if args.input: _input_file = args.input
    if args.output: _output_dir = args.output
    if args.log: _log_file = args.log
    if args.format: _format = [f.strip() for f in args.format.split(",")]


if __name__ == "__main__":
    parseArgs()

    logging_handlers = [logging.StreamHandler()]
    if _log_file is not None:
        logging_handlers.append(logging.FileHandler(_log_file, 'w', 'utf-8'))

    logging.basicConfig(handlers=logging_handlers, level=logging.DEBUG, datefmt='%H:%M:%S',
                        format='%(asctime)s %(levelname)s %(message)s')

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
        print("\rScraping Google Scholar Stats... [%s/%s]: %s" % (index + 1, size, researcher.last_name), end='')

        researcher.scholar_data = scraper.get_data(researcher.scholar_url)
        if not researcher.scholar_data['personal_data'] and not researcher.scholar_data['stats']:
            wmessage = str("Scholar URL Deprecated, please update: "+ researcher.first_name + " "+ researcher.last_name)
            logging.warning(wmessage)
            logging.getLogger().handlers[0].flush()

    print("\rScraping Google Scholar Stats... [%s/%s] Done!" % (index + 1, size), )

    end_scrap = time.time()
    
    start_store = time.time()

    if 'json' in _format:
        json_writer.store_researchers(researchers, _output_dir + "/researchers.json")
    if 'csv' in _format:
        csv_writer.store_researchers(researchers, _output_dir + "/researchers.csv")
    if 'xls' in _format:
        xls_writer.store_researchers(researchers, _output_dir + "/researchers.xls")
    end_store = time.time()

    end = time.time()
    
    print("\nTiempos: \n")
    print("Tiempo total: ", time.strftime("%H:%M:%S", time.gmtime(end - start)))
    print("Tiempo de carga: ", time.strftime("%H:%M:%S", time.gmtime(end_load - start_load)))
    print("Tiempo de scrap: ", time.strftime("%H:%M:%S", time.gmtime(end_scrap - start_scrap)))
    print("Tiempo de guardado: ", time.strftime("%H:%M:%S", time.gmtime(end_store - start_store)))


