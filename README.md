# Bibliometrics Scraper

Python script that reads ULPGC researcher data from a file and scraps information from Google Scholar or Research Gate if the url is given. Generates a new file with the collected information. 

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

Shows the script information and options you can choose. Documented like man.

`[-i | --input] <input-file>`

Load all the data from the designed inputfile. It should be an .xls with the same format as the CRIS doc.
 
`[-o | --output-dir] <output-dir>`

Stores all the persistance docs generated into the designed folder.

`[-n | --output-name | --filename] <filename>`

Saves the info in a filename with the same name as the indicated.

`[-f | --format] <"csv,json,xls">`

Saves the collected data in the specified format or formats 

`[-l | --log] <filename>`

Enables logging and stores it in the specified path

`[-t | --target] <"[scholar, rg]">`

Selects which page to scrap, default is set to scrap both









