# Bibliometrics Scraper

Python script that reads ULPGC researcher data from a file and scraps information from Google 
Scholar or Research Gate if the url is given. Generates a new file with the collected information. 

## Features

- Several output file formats: JSON, CSV or XLS
- Scraps:
    - Researcher personal information
    - Researcher's Fields
    - Citations
    - i10 Index
    - h Index
    - Citations per year
- Data formatting

## Installation

### Requirements

Before using this python module you need to install the following Python setup:
- Python version: 3.7.2
- Python modules:
    - pandas: 0.24.1
    - xlrd: 1.2.0
    - xlwt: 1.3.0
    - urllib: 1.24.1
    - beautifulsoup4: 4.7.1

You can install it automatically using the installer:

```bash
cd ~/ProyectFolder/
./installer.sh 
```

Or you can install it manually doing:

```bash
pip install xlrd==1.2.0
pip install xlwt==1.3.0
pip install pandas==0.24.1
pip install urllib==1.24.1
pip install beautifulsoup4==4.7.1
```

## Usage

There are several options when calling the script, using 

```bash
py ./main.py [args]
```

`[-h | --help]`

Show help.

`[-i | --input] <input-file>`

Load all the data from the designed inputfile. It should be an .xls with the same format as 
the CRIS doc.
 
`[-o | --output-dir] <output-dir>`

Sets output dir for generated results. Default: `.\results`

`[-n | --output-name | --filename] <filename>`

Sets filename (without extension) Default: `researchers`

`[-f | --format] <"csv,json,xls">`

Output format/s. Default: `csv, json, xls` 

`[-l | --log] <filename>`

Enables logging and stores it in the specified path

`[-t | --target] <"[scholar, rg]">`

Selects scrap targets. All by default.

---

## Scraper integration and API

If you prefer to use only the scraper module in your project, you only need 
to install `urllib` and `beautifulsoup4`.


### Scraper abstract base class

- **get_personal_data ( url,  [force_refresh] )**: should returns a dictionary containing 
general personal information like *study fields*, *organization*, *department*, etc.

- **get_stats ( url, [force_refresh] )**: should returns a dictionary with specific 
bibliometric data like *publications*, *citations*, *indexes*, etc.

Two implementations of this abstract class are provided: 
`ScholarScraper` and `ResearchGateScraper`. 

### ScholarScraper implementation

#### get_personal_data(url, [force_refresh]):
##### Params
* **url**: *string* - Should be a Google Scholar profile URL. There is a URL checker in the
utils module, the `is_valid_scholar_profile_url` function from 
`./utils/validation_utils.py`. Check before is not strictly necessary.
* **force_refresh**: *boolean* - don't use cached html for this URL. False if not passed (recommended). 

##### Returns

Python dict with 2 keys: 
- `personal_info` whose value is the first *string* under researcher name in Scholar's profile, 
tipically it contains *organization name*, *department*, *job*, etc.
- `study_fields` whose value is a strings array with all study fields listed in the profile

###### Example
<pre>{
    personal_info: "Profesor de Física (ULPGC)"
    study_fields: ["plasma physics", "laboratory astrophysics"] 
}</pre>

#### get_stats(url, [force_refresh]):
##### Params
Same as get_personal_data
##### Returns

Python dict with multiple keys: 
- `citations` a dict of with 2 keys and integer values:
    - `total`: total of citations
    - `last5Years`: citations from the last 5 years.
- `hIndex` a dict of with 2 keys and integer values:
    - `total`: current h-index
    - `last5Years`: h-index calculated with citations from the last 5 years.
- `i10` a dict of with 2 keys and integer values:
    - `total`: current i10 index
    - `last5Years`: i10 calculated with citations from the last 5 years.
- `citations_per_year` a dict with year:citations pairs.
###### Example
<pre>{
    citations: {total: 13432, last5Years: 6224"},
    hIndex: {total: 66, last5Years: 47"},
    i10: {total: 169, last5Years: 147"},
    citations_per_year: {1999:7, 2000:0, 2001:36, ..., 2018:1160, 2019:253}
}</pre>

### ResearchGateScraper implementation
TODO...


## More examples
Check examples folder.




