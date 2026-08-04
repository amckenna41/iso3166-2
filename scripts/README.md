<a name="TOP"></a>

# Scripts for exporting and updating all ISO 3166-2 data

*  [`main.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/main.py) - main pipeline script for pulling and exporting the latest ISO 3166-2 data from the various data sources and scripts
* [`local_other_names.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/local_other_names.py) - script for adding the data from the [`local_other_names.csv`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_resources/local_other_names.csv) dataset, including any validation checks on the data
* [`utils.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/utils.py) - script of utility functions used throughout the software, mainly used by the [`main.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/main.py) script
* [`language_lookup.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/language_lookup.py) - script containing the `LanguageLookup` class for extracting and working with the language lookup table and data
* [`metadata.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/metadata.py) - script that exports a plethora of useful and informative attributes and data about the iso366-2 dataset
* [`geo.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/geo.py) - script for getting the geographical data per subdivision
<!-- * [`demographics.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/demographics.py) - script for getting the subdivision-level demographics data including population and area -->
* [`city_data.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/city_data.py) - script that exports the city-level subdivision data using CountryState API
* [`restcountries_api.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/restcountries_api.py) - script that exports the country-level attributes data via the RestCountries API
* [`history.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/history.py) - script that exports historical subdivision data via the custom iso3166-updates software


<!-- Requirements (main.py)
------------------------------
* [python][python] >= 3.9
* [iso3166-updates][iso3166-updates] >= 1.8.4
* [requests][requests] >= 2.28.1
* [iso3166][iso3166] >= 2.1.1
* [pycountry][pycountry] >= 22.3.5
* [googlemaps][googlemaps] >= 4.10.0
* [tqdm][tqdm] >= 4.64.0
* [natsort][natsort] >= 8.4.0
* [pandas][pandas] >= 1.4.3
* [numpy][numpy] >= 1.23.2
* [fake_useragent][fake_useragent] >= 1.5.0
* [emoji-country-flag][emoji-country-flag] >= 1.3.0
* [Unidecode][Unidecode] >= 1.3.8
* [dicttoxml][dicttoxml] >= 1.7.16
* [iso3166-2][iso3166_2] >= 1.5.5 
* [SPARQLWrapper][SPARQLWrapper] >= 2.0.0
* [shapely][shapely] >= 2.0.1
-->

Usage: main.py
--------------
The script `main.py` is the full pipeline code for gathering and exporting subdivision data for ALL countries. It uses the [pycountry][pycountry] package as a baseline for the subdivision object and uses other libraries and datasets to gather additional subdivision related info, including the [iso3166-updates][iso3166-updates], [OpenStreetMap][OpenStreetMap], [CountryStateCityAPI][country-state-city], [RestCountriesAPI][rest-countries-api], the [local_other_names.csv](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_resources/local_other_names.csv) and [Wikidata][Wikidata]. Calling the script using its default parameters will gather all the subdivision data for ALL countries in the ISO 3166, but the <i>alpha_codes</i> parameter can be set to pull the latest data for a specific list of one or more countries using their ISO 3166-1 alpha codes (alpha-2, alpha-3 or numeric codes). You can also export a range of alpha codes data via the <i>alpha_codes_range</i> parameter, with the code on the left being the starting alpha code and the latter being the end code e.g "AD-LY", "MA-PA" etc.

The primary keys/attributes that can be exported by default are <i>name, localName, type, parentCode, flag and latLng.</i> The <i>history</i> attribute can be exported via the [iso3166-updates][iso3166-updates] custom-built software via the <i>history</i> input parameter and stores the historical ISO 3166 updates per subdivision, if applicable. 

<!-- Demographics data including area and population can be exported via the <i>demographics</i> attribute via the [Wikidata][Wikidata] database. -->

The [RestCountries API](https://api.restcountries.com/countries/v5) allows for a plethora of additional country-level attributes to be appended to each subdivision, the fields supported are: idd, carSigns, carSide, continents, currencies, languages, postalCode, region, startOfWeek, subregion, timezones and tld. An explanation of each of these attributes can be seen on the [RestCountries](https://gitlab.com/restcountries/restcountries/-/blob/master/FIELDS.md) repo. These can be passed in as a string via the <i>rest_countries_keys</i> parameter. You can also get the city-level data per subdivision via the [CountryStateCityAPI][country-state-city] and setting the <i>state_city_data</i> parameter to True. To execute this you will need to set up an API key with the CountryStateCity API.

By default, when running the script, the data will be exported to a <i>JSON</i> and a <i>CSV</i>, but you can also export to <i>XML</i> by setting the <i>export_xml</i> parameter to True.

To download all of the latest ISO 3166-2 subdivision data for all countries, from the main repo dir, run the `main.py` in a terminal or command line below; (the script takes around **1 hour and 20 mins** to execute):
```bash
python3 scripts/main.py --export_filename=iso3166_2.json --export_folder=iso3166_2 --verbose --export_csv

#alpha_codes: list of 1 or more ISO 3166-1 alpha country codes (if not specified then all country codes will be used).
#export_filename: output filename for exported files.
#export_folder: output folder to store exported files.
#verbose: if set to 1 then the progress of the ISO 3166-2 data export will be output (default=True).
#export_csv: if set to 1 then dataset will be exported to a CSV (default=True).
#export_xml: if set to 1 then dataset will be exported to a XML (default=False).
#rest_countries_keys: list of additional fields/attributes from RestCountries API to be added to each subdivision object.
#exclude_default_keys: list of default fields/attributes to be excluded from each country's subdivision object.
#alpha_codes_range: range of country codes to export the subdivision data for. If a single country code input then this will act as the starting point.
#state_city_data: if set to 1 the city-level data per subdivision will be included from the CountryStateCity API (default=False).
#history: if set to 1 the historical updates data per subdivision will be included via the iso3166-updates software (default=True).
#demographics: if set to 1 the demographics data via the Wikidata database - area and population will be exported (default=True)
#save_each_iteration: if set to 1 the subdivision data will be saved on each iteration of the extract pipeline script (default=False).
#use_proxy: if set to 1 a proxy IP will be used when scraping the data from the data sources via requests library.
```

To download all of the latest ISO 3166-2 subdivision data for Germany, Portugal and Spain (the data will be exported to a JSON and CSV file called <em>iso3166_2_DE,ES,PT.json, iso3166_2_DE,ES,PT.csv</em>):
```bash
python3 scripts/main.py --alpha_codes=DE,PT,ESP --export_filename=iso3166_2.json --verbose --export_csv
```

To download all of the latest ISO 3166-2 subdivision data for countries in the range FR-HU (the data will be exported to a JSON and CSV file called <em>iso3166_2_FR-HU.json, iso3166_2_FR-HU.csv, iso3166_2_FR-HU.xml</em>):
```bash
python3 scripts/main.py --alpha_codes_range=FR-HU --export_filename=iso3166_2.json --verbose --export_csv --export_xml
```

To download all of the latest ISO 3166-2 subdivision data for all countries, additionally including the languages, subregion and tld attributes (from RestCountries API) for each subdivision:
```bash
python3 scripts/main.py --export_filename=iso3166_2 --rest_countries_keys=languages,subregion,tld --verbose --export_csv
```

To download all of the latest ISO 3166-2 subdivision data for all countries, excluding the default attributes of lat_lng and flag:
```bash
python3 scripts/main.py --export_filename=iso3166_2 --exclude_default_keys=lat_lng,flag --verbose --export_csv
```

To download all of the latest ISO 3166-2 subdivision data for all countries, saving the subdivision data per iteration:
```bash
python3 scripts/main.py --export_filename=iso3166_2 --verbose --export_csv --save_each_iteration
```

<!-- Requirements (local_other_names.py)
-----------------------------------
* [python][python] >= 3.9
* [pandas][pandas] >= 1.4.3
* [numpy][numpy] >= 1.23.2
* [pycountry][pycountry] >= 22.3.5 -->


Usage: local_other_names.py
---------------------------
The [`local_other_names.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/local_other_names.py) script is used for implementing the data from the [`local_other_names.csv`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_resources/local_other_names.csv) dataset. This dataset holds thousands of individual alternative names for each subdivision that are incorporated in the `localOtherName` attribute in the iso3166-2 dataset. The `add_local_other_names()` function streamlines the addition of all the local/other names data of each subdivision to the main iso3166-2 data object. Additionally, it also contains the `validate_local_other_names()` function that validates the local/other name data per subdivision, prior to being incorporated into the dataset. The final function `convert_iso_639_language_codes()` was a temporary auxiliary function that converted all the language codes per local/other name into their official ISO 639 3 letter counterparts.

There are no individual usage examples for this function as it is meant to be used within the `main` script and is not meant to be called on its own.


<!-- Requirements (language_lookup.py)
---------------------------------
* [python][python] >= 3.9
* [pandas][pandas] >= 1.4.3
* [pycountry][pycountry] >= 22.3.5
* [iso3166][iso3166] >= 2.1.1
* [thefuzz][thefuzz] >= 0.22.1
* [requests][requests] >= 2.28.1 
* [fake-user-agent][fake_user_agent] >= 2.2.0
* [beautifulsoup4][beautifulsoup4] >= 4.11.1  -->


Usage: language_lookup.py
-------------------------
The [`language_lookup.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/language_lookup.py) script exports the the [`language_lookup.md`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_resources/language_lookup.md) and [`language_lookup.json`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_resources/language_lookup.json) files. These files act as reference data for the over **3,700** local/other name variants within the [`local_other_names.csv`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_resources/local_other_names.csv) dataset, with each name having a referenced language code in brackets.  All of this language data is encapsulated within the `LanguageLookup` class that allows for access to the language data as well as additional functionality to add, delete, amend a language object, search and re-export the data.

```python
from scripts.language_lookup import *

#create instance of LanguageLookup class
lang_lookup = LanguageLookup()

#get all language data 
language_obj = LanguageLookup(language_lookup_filename="language_lookup.json")
language_lookup = language_obj.all_language_data

#get language data for Japanese (JPN), Kazakh (KAZ), Suriganon (SGD)
jpn = language_obj["JPN"]
kaz = language_obj["KAZ"]
sgd = language_obj["sgd"]

#filter all language data by type 
language_type_living = language_obj.filter_by_type("Living")
language_type_extinct = language_obj.filter_by_type("Extinct")
language_type_constructed = language_obj.filter_by_type("Constructed")

#filter all language data by scope 
language_scope_individual = language_obj.filter_by_scope("Individual")
language_scope_dialect = language_obj.filter_by_scope("Dialect")
language_scope_family = language_obj.filter_by_scope("Family")

#get list of countries (country codes) that have a subset of languages in their subdivisions
language_cn = language_obj.get_country_language_data("CN")
language_tw = language_obj.get_country_language_data("TW")
language_ve = language_obj.get_country_language_data("VE")

#search for specific language using its name
language_albanian = language_obj.search_language_lookup("Albanian")
language_norwegian = language_obj.search_language_lookup("Norwegian")
language_serbian_slovakian = language_obj.search_language_lookup("Serbian,Slovakian")

#add language code to lookup table
language_clingon = language_obj.add_language({'name': 'Clingon', 'scope': 'Individual', 'type': 'Artificial', 'countries': 'GB, IE', 'total': 0, 'source': ''}, export=False)

#delete language code from lookup table
language_obj.delete_language_code("deu")

#get total number of languages
len(language_obj)
```

Usage: geo.py
-------------
The [`geo.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/geo.py) script contains the `Geo` class that provides utilities for fetching and exporting geographical data from OpenStreetMap for ISO 3166-2 subdivisions. The class integrates with multiple data sources including the Overpass API, Nominatim, Wikidata SPARQL, and polygons.openstreetmap.fr to retrieve comprehensive geographic information about subdivisions.

The `Geo` class supports the following key methods:
- `get_relation_id()`: Gets the OSM relation ID for the subdivision using multiple fallback methods
- `get_centroid()`: Returns the (latitude, longitude) centroid coordinates
- `get_bounding_box()`: Returns the bounding box coordinates (minLat, maxLat, minLon, maxLon)
- `get_geojson()`: Fetches the GeoJSON geometry for the subdivision
- `export_geojson()`: Exports the GeoJSON to a file
- `get_visualisation_url()`: Returns the OpenStreetMap visualization URL
- `get_admin_level()`: Returns the administrative level tag
- `get_neighbors()`: Returns a list of neighboring subdivision relation IDs and names
- `get_hierarchy()`: Returns parent and child relations
- `get_perimeter_km()`: Calculates the perimeter in kilometers
- `get_relation_id_from_coords()`: Finds the OSM relation ID for coordinates
- `export_all()`: Exports all supported data/attributes for the subdivision

The class includes a `verbose` parameter at initialization that controls whether progress messages are printed during API calls. This can be set at the class level or overridden for individual method calls.

```python
from scripts.geo import Geo

# Create instance with verbose output enabled
geo = Geo("US-CA", verbose=True)

# Get centroid coordinates
centroid = geo.get_centroid()
print(f"Centroid: {centroid}")  # Returns (lat, lon) tuple

# Get bounding box
bbox = geo.get_bounding_box()
print(f"Bounding Box: {bbox}")  # Returns dict with minLat, maxLat, minLon, maxLon

# Get OpenStreetMap visualization URL
url = geo.get_visualisation_url()
print(f"OSM URL: {url}")

# Export GeoJSON to file
geo.export_geojson(out_path="california.geojson")

# Get neighboring subdivisions
neighbors = geo.get_neighbors()
print(f"Neighbors: {neighbors}")

# Get perimeter in kilometers
perimeter = geo.get_perimeter_km()
print(f"Perimeter: {perimeter} km")

# Find subdivision from coordinates
relation_id = geo.get_relation_id_from_coords(37.7749, -122.4194, admin_level=4)
print(f"Relation ID: {relation_id}")

# Export all geographic data
all_data = geo.export_all(out_geojson_path="california_full.geojson")
print(all_data)

# Override class-level verbose for specific method
geo_quiet = Geo("GB-ENG", verbose=False)
centroid = geo_quiet.get_centroid(verbose=True)  # This call will print verbose output
```

Usage: metadata.py
-----------------------------------
The [`metadata.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/metadata.py) script exports comprehensive metadata and statistics about the ISO 3166-2 dataset to a JSON file. The `export_metadata()` function analyzes the dataset and generates a summary including total countries/subdivisions, dataset size, unique attributes, null attribute counts, geographic distribution by hemisphere, total local/other name entries and attribute percentage completeness. 

To export metadata for the default ISO 3166-2 dataset:
```bash
python3 scripts/metadata.py --iso3166_2_filename="iso3166_2/iso3166-2.json" --export_filename="iso3166_2_metadata"
```

```python
from scripts.metadata import export_metadata

# Export metadata for a dataset
export_metadata(iso3166_2_filename="iso3166_2/iso3166-2.json", export_filename="iso3166_2_metadata")
```

[Back to top](#TOP)

[python]: https://www.python.org/downloads/release/python-360/
[requests]: https://requests.readthedocs.io/
[iso3166]: https://github.com/deactivated/python-iso3166
[iso3166_2]: https://github.com/amckenna41/iso3166-2
[beautifulsoup4]: https://pypi.org/project/beautifulsoup4/
[fake_useragent]: https://pypi.org/project/fake-useragent/
[emoji-country-flag]: https://pypi.org/project/emoji-country-flag/
[Unidecode]: https://pypi.org/project/Unidecode/
[dicttoxml]: https://pypi.org/project/dicttoxml/
[pycountry]: https://github.com/flyingcircusio/pycountry
[rest-countries-api]: https://api.restcountries.com/countries/v5
[googlemaps]: https://github.com/googlemaps/google-maps-services-python
[country-state-city]: https://countrystatecity.in/
[tqdm]: https://github.com/tqdm/tqdm
[natsort]: https://pypi.org/project/natsort/
[thefuzz]: https://pypi.org/project/thefuzz/
[pandas]: https://pandas.pydata.org/
[fake_user_agent]: https://pypi.org/project/fake-useragent/
[numpy]: https://numpy.org/
[iso3166-updates]: https://github.com/amckenna41/iso3166-updates
[flag_icons_repo]: https://github.com/amckenna41/iso3166-flags
[SPARQLWrapper]: https://pypi.org/project/SPARQLWrapper/
[OpenStreetMap]: https://www.openstreetmap.org/#map=7/53.531/-7.273
[shapely]: https://pypi.org/project/shapely/
[Wikidata]: https://www.wikidata.org/wiki/Wikidata:Main_Page