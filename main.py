from scraper.scholar_scraper import ScholarScraper
from persistence.data_writer import json_writer, csv_writer, xls_writer
from persistence.data_reader import cris_excel_reader as reader
import time, sys, os, argparse, logging
from utils.validation_utils import is_valid_rg_profile_url, is_valid_scholar_profile_url

_input_file = './data/dataCRIS.xls'
_output_dir = './results'
_log_file = None
_format = ['json', 'csv', 'xls']
_output_filename = 'researchers'
_target = ['scholar', 'rg']

def parseArgs():
    global _input_file, _output_dir, _format, _log_file, _target, _output_filename
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-i", "--input", required=False)
    parser.add_argument("-o", "--output", "--output-dir", required=False)
    parser.add_argument("-n", "--output-name", "--filename", required=False)
    parser.add_argument("-f", "--format", required=False)
    parser.add_argument("-h", "--help", required=False, action="store_true")
    parser.add_argument("-l", "--log", required=False)
    parser.add_argument("-t", "--target", required=False)
    args = parser.parse_args()

    if args.help:
        basename = os.path.basename(__file__)
        print("Use: %s [hifot]" % basename,
              "\n  [-h, --help] - show this help and exit.",

              "\n\n  [-i, --input] <input_file> - CRIS input file (only xls for now).",
              "\n      default: ./data/dataCRIS.xls",

              "\n\n  [-o, --output-dir] <output_dir> - output directory. Will be created if doesn't exist.",
              "\n      default: ./results",

              "\n\n  [-n, --output-name, --filename] <output_name> - output name of files (without extension). "
              "\n      default: \"researchers\""
              
              "\n\n  [-f, --format] [csv,json,xls] - output format. Multiple options allowed (comma separated).",
              "\n      default: \"csv,json,xls\"",

              "\n\n  [-l, --log] <filename> - enable logging and store it in the specified path.",

              "\n\n  [-t, --target] [scholar,rg] - Scrap targets. Multiple options allowed (comma separated)",
              "\n      scholar - Get personal data and stats from Google Scholar",
              "\n      stats - Get personal data and stats from Research Gate"
              "\n      default: all"
              )
        exit(0)
    if args.input: _input_file = args.input
    if args.output: _output_dir = args.output
    if args.output_name: _output_filename = args.output_name
    if args.log: _log_file = args.log
    if args.format: _format = [f.strip() for f in args.format.split(",")]
    if args.target: _target = [f.strip() for f in args.target.split(",")]


def configure_loggin():
    logging_handlers = [logging.StreamHandler()]
    if _log_file is not None:
        logging_handlers.append(logging.FileHandler(_log_file, 'w', 'utf-8'))

    logging.basicConfig(handlers=logging_handlers, level=logging.DEBUG, datefmt='%H:%M:%S',
                        format='%(asctime)s - %(message)s')


def check_rg_researchers_url(researchers):
    not_valid = [r for r in researchers if r.rg_url and not is_valid_rg_profile_url(r.rg_url)]

    for r in not_valid:
        wmsg = "[Not valid ResearchGate profile URL for %s - %s %s]: %s" \
               % (r.crisid, r.first_name, r.last_name, r.rg_url)
        logging.warning(wmsg)

    return not_valid


def scrap (researchers, url_attribute_name, data_attribute_name, scraper):
    size = len(researchers)
    for index, r in enumerate(researchers):
        url = getattr(r, url_attribute_name)
        print("\rScraping with %s [%s/%s]: %s " % (scraper.__class__.__name__, index+1, size, r.crisid), end='')

        data = {
            'personal_data': scraper.get_personal_data(url), 
            'stats': scraper.get_stats(url), 
            'articles': scraper.get_articles(url) 
        }

        if not data['personal_data'] and not data['stats'] and not data['articles']:
            wmessage = "[No data for %s - %s %s. Check if profile still exists] URL: %s" % \
                       (r.crisid, r.first_name, r.last_name, url)
            logging.warning(wmessage)
        else:
            setattr(r, data_attribute_name, data)

def store_results(researchers):
    if 'json' in _format:
        json_writer.store_researchers(researchers, _output_dir + "/" + _output_filename + ".json")
    if 'csv' in _format:
        csv_writer.store_researchers(researchers, _output_dir + "/" + _output_filename + ".csv")
    if 'xls' in _format:
        xls_writer.store_researchers(researchers, _output_dir + "/" + _output_filename + ".xls")


if __name__ == "__main__":
    parseArgs()

    configure_loggin()

    if not os.path.exists(_output_dir):
        os.makedirs(_output_dir)
        print("Created: " + os.path.abspath(_output_dir))

    start = time.time()

    # LOAD RESEARCHERS
    start_load = time.time()
    researchers = reader.load_researchers(_input_file, 'main_entities')
    end_load = time.time()

    # CHECK
    if 'rg' in _target: check_rg_researchers_url(researchers)

    # SCRAPING!
    start_scrap = time.time()

    if 'scholar' in _target:
        scrap([r for r in researchers if r.scholar_url and is_valid_scholar_profile_url(r.scholar_url)],
              "scholar_url", "scholar_data", ScholarScraper())

    # if 'rg' in _targets:
    #     scrap([r for r in researchers if r.rg_url and is_valid_rg_profile_url(r.rg_url)],
    #            "rg_url", "rg_data", ResearchGateScraper())
    end_scrap = time.time()

    # STORE
    start_store = time.time()
    store_results(researchers)
    end_store = time.time()

    end = time.time()
    
    print("\nTiempos: \n")
    print("Tiempo total: ", time.strftime("%H:%M:%S", time.gmtime(end - start)))
    print("Tiempo de carga: ", time.strftime("%H:%M:%S", time.gmtime(end_load - start_load)))
    print("Tiempo de scrap: ", time.strftime("%H:%M:%S", time.gmtime(end_scrap - start_scrap)))
    print("Tiempo de guardado: ", time.strftime("%H:%M:%S", time.gmtime(end_store - start_store)))