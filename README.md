# Bibliometrics Scraper

Python script to find researchers and scrap their data.

## Features

~~- Several output file formats: JSON, CSV or XLS.~~ Currently working on
Firebase Realtime Database.
- TODO - Find:
    - By keywords
    - By organization code.
    - Stoppable and resumable searchs in order to prevent ban and recover
      from it.
    - Configurable search limits and intervals.
    - Mail notification when new researchers are found.
    
- Scraps:
    - Researcher personal information
    - Researcher's Fields
    - Citations
    - i10 Index
    - h Index
    - Citations per year
    - Shallow articles info (dates, citations, title, authors short names...) 

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

Python dict of 2 keys: 
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
- `citations` a dict of 2 keys and integer values:
    - `total`: total of citations
    - `last5Years`: citations from the last 5 years.
- `hIndex` a dict of 2 keys and integer values:
    - `total`: current h-index
    - `last5Years`: h-index calculated with citations from the last 5 years.
- `i10` a dict of 2 keys and integer values:
    - `total`: current i10 index
    - `last5Years`: i10 calculated with citations from the last 5 years.
- `citationsPerYear` a dict of year:citations.
###### Example
<pre>{
    citations: {total: 13432, last5Years: 6224"},
    hIndex: {total: 66, last5Years: 47"},
    i10: {total: 169, last5Years: 147"},
    citationsPerYear: {1999:7, 2000:0, 2001:36, ..., 2018:1160, 2019:253}
}</pre>

### ResearchGateScraper implementation
TODO...


## More examples
Check examples folder.




