<a name="TOP"></a>

# Scripts for exporting and updating all ISO 3166-2 data

*  [`export_iso3166_2.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/export_iso3166_2.py) - main pipeline script for pulling and exporting the latest ISO 3166-2 data from the various data sources
* [`update_subdivisions.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/update_subdivisions.py) - script for adding, amending and or deleting subdivision data to the `iso3166-2` software and object
* [`local_other_names.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/local_other_names.py) - script for adding the data from the [`local_other_names.csv`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_resources/local_other_names.csv) dataset, including any validation checks on the data
* [`utils.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/utils.py) - script of utility functions used throughout the software, mainly used by the [`export_iso3166_2.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/export_iso3166_2.py) script
* [`language_lookup.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/language_lookup.py) - script containing the `LanguageLookup` class for extracting and working with the language lookup table and data
* [`export_iso3166_2_metadata.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/export_iso3166_2_metadata.py) - script that exports a plethora of useful and informative attributes and data about the iso366-2 dataset

<!-- Requirements (export_iso3166_2.py)
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
* [iso3166-2][iso3166_2] >= 1.5.5 -->


Usage: export_iso3166_2.py
-----------------------
The script `export_iso3166_2.py` is the full pipeline code for gathering and exporting subdivision data for ALL countries. It uses the [pycountry][pycountry] package as a baseline for the subdivison object and uses other libraries and datasets to gather additional subdivision related info, including the [iso3166-updates][iso3166-updates], [Googlemaps][googlemaps], [CountryStateCityAPI][country-state-city], [RestCountriesAPI][rest-countries-api] and the [local_other_names.csv](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_resources/local_other_names.csv). Calling the script using its default parameters will gather all the subdivision data for ALL countries in the ISO 3166, but the <i>alpha_codes</i> parameter can be set to pull the latest data for a specific list of one or more countries using their ISO 3166-1 alpha codes (alpha-2, alpha-3 or numeric codes). You can also export a range of alpha codes data via the <i>alpha_codes_range</i> parameter, with the code on the left being the starting alpha code and the latter being the end code e.g "AD-LY", "MA-PA" etc.

The primary keys/attributes that can be exported by default are <i>name, localName, type, parentCode, flag and latLng.</i> The <i>history</i> attribute can be exported via the [iso3166-updates][iso3166-updates] custom-built software via the <i>history</i> input parameter and stores the historical ISO 3166 updates per subdivision, if applicable. The [RestCountries API](https://restcountries.com/) allows for a plethora of additional country-level attributes to be appended to each subdivision, the fields supported are: idd, carSigns, carSide, continents, currencies, languages, postalCode, region, startOfWeek, subregion, timezones and tld. An explanation of each of these attributes can be seen on the [RestCountries](https://gitlab.com/restcountries/restcountries/-/blob/master/FIELDS.md) repo. These can be passed in as a string via the <i>rest_countries_keys</i> parameter. You can also get the city-level data per subdivision via the [CountryStateCityAPI][country-state-city] and setting the <i>state_city_data</i> parameter to True. 

To export the <i>latLng</i> attribute data you will have to set up a GoogleMaps API and get an API key. Similarly for the CountryStateCity API you will also have to set an API key.

By default, when running the script, the data will be exported to a <i>JSON</i> and a <i>CSV</i>, but you can also export to <i>XML</i> by setting the <i>export_xml</i> parameter to True.

To download all of the latest ISO 3166-2 subdivision data for all countries, from the main repo dir, run the `export_iso3166_2.py` in a terminal or command line below; (the script takes around **1 hour and 20 mins** to execute):
```bash
python3 scripts/export_iso3166_2.py --export_filename=iso3166_2.json --export_folder=iso3166_2 --verbose --export_csv

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
#extract_lat_lng: if set to 1 the coordinates data per subdivision will be included via the GoogleMaps API (default=False).
#save_each_iteration: if set to 1 the subdivision data will be saved on each iteration of the extract pipeline script (default=False).
#use_proxy: if set to 1 a proxy IP will be used when scraping the data from the data sources via requests library.
```

To download all of the latest ISO 3166-2 subdivision data for Germany, Portugal and Spain (the data will be exported to a JSON and CSV file called <em>iso3166_2_DE,ES,PT.json, iso3166_2_DE,ES,PT.csv</em>):
```bash
python3 scripts/export_iso3166_2.py --alpha_codes=DE,PT,ESP --export_filename=iso3166_2.json --verbose --export_csv
```

To download all of the latest ISO 3166-2 subdivision data for countries in the range FR-HU (the data will be exported to a JSON and CSV file called <em>iso3166_2_FR-HU.json, iso3166_2_FR-HU.csv, iso3166_2_FR-HU.xml</em>):
```bash
python3 scripts/export_iso3166_2.py --alpha_codes_range=FR-HU --export_filename=iso3166_2.json --verbose --export_csv --export_xml
```

To download all of the latest ISO 3166-2 subdivision data for all countries, additionally including the languages, subregion and tld attributes (from RestCountries API) for each subdivision:
```bash
python3 scripts/export_iso3166_2.py --export_filename=iso3166_2 --rest_countries_keys=languages,subregion,tld --verbose --export_csv
```

To download all of the latest ISO 3166-2 subdivision data for all countries, excluding the default attributes of lat_lng and flag:
```bash
python3 scripts/export_iso3166_2.py --export_filename=iso3166_2 --exclude_default_keys=lat_lng,flag --verbose --export_csv
```

To download all of the latest ISO 3166-2 subdivision data for all countries, saving the subdivision data per iteration:
```bash
python3 scripts/export_iso3166_2.py --export_filename=iso3166_2 --verbose --export_csv --save_each_iteration
```

<!-- Requirements (update_subdivisions.py)
-------------------------------------
* [python][python] >= 3.8
* [iso3166][iso3166] >= 2.1.1
* [natsort][natsort] >= 8.4.0
* [pandas][pandas] >= 1.4.3
* [numpy][numpy] >= 1.23.2 -->

Usage: update_subdivisions.py
-----------------------------

The script [`update_subdivisions.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/update_subdivisions.py) has the `update_subdivision()` function that was created to streamline the addition, amendment and or deletion to any of the subdivisions within the iso3166-2 data object. This is an important functionality due to the ever-changing landscape of the subdivision data and attributes regularly published by the ISO. The main function can accept an individual subdivision change by passing in all the required attribute values to the function directly. Alternatively, a <b>CSV</b> file with rows of the individual changes can be passed in, allowing for hundreds of changes to be made in one go (this is the recommended and fastest approach), as can be seen in the CSV [subdivision_updates.csv](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_resources/subdivision_updates.csv).

The primary input parameters to the `update_subdivision()` function are: <i>alpha_code, subdivision_code, name, local_name, type, lat_lng, parent_code, flag, history, custom_attributes</i> and <i>delete</i>. The first ten parameters represent the data to be added or changed to the specified country code and subdivision code (<i>alpha2_code, subdivision_code</i>) and <i>delete</i> is a boolean flag that should be set (0/1) if the input subdivision is to be deleted - by default this will be 0. For any addition, amendment and or deletion, the <i>country_code</i> and <i>subdivision_code</i> parameters are required, but the remainder of the parameters are optional. If these optional parameters are not input then they will be set to null for the subdivision, in the case of an addition or deletion, or remain as their previous value in the case of an amendment. You can also pass in custom attributes for a subdivision object e.g population, gini, gdp etc, via the <i>custom_attributes</i> parameter.  

As mentioned, you can also pass in a <b>CSV</b> with rows of all the changes to be made to the subdivision object e.g [subdivision_updates.csv](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_resources/subdivision_updates.csv). The <b>CSV</b> has the same columns as the aforementioned function parameters, but additionally has the <i>notes</i> and <i>dateIssued</i> columns. <i>notes</i> just contains a small description about the addition, amendment and or deletion being made and <i>dateIssued</i> is the date that the subdivision change was communicated by the ISO. 

```python
from scripts.update_subdivisions import *

#adding Timimoun Province of Algeria (DZ-49) to ISO 3166-2 object (from newsletter 2022-11-29)
update_subdivision("DZ", "DZ-49", name="Timimoun", local_name="ولاية تيميمون", type_="Province", lat_lng=[29.263, 0.241], parent_code=None, flag=None, history=None)

#adding Waterford County of Ireland (IE-WD) to ISO 3166-2 object - subdivision already present so no changes made
update_subdivision("IE", "IE-WD", "Waterford", local_name="Port Láirge", type_="County", lat_lng=[52.260, -7.110], parent_code="IE-M", flag="https://github.com/amckenna41/iso3166-flags/blob/main/iso3166-2-flagss/IE/IE-WD.png")
#iso.update_subdivision("IE", "IE-WD") - this will also work as only the first 2 params requried

#amending the subdivision name of subdivision FI-17 from Satakunda to Satakunta (from newsletter 2022-11-29)
update_subdivision("FI", "FI-17", name="Satakunta")

#deleting FR-GP (Guadeloupe) and (FR-MQ Martinique) subdivisions (from newsletter 2021-11-25)
update_subdivision("FR", "FR-GP", delete=1)
update_subdivision("FR", "FR-MQ", delete=1)

#error raised as both country_code and subdivision_code parameters required
update_subdivision(type_="region", lat_lng=[], parent_code=None)

#error raised as only one alpha code and subdivision code should be passed in - if multiple updates required pass in a CSV
update_subdivision("IE", "IE-WD,IE-WW")

#passing in a csv with rows of subdivision additions/updates/deletions
update_subdivision(subdivision_csv="new_subdivisions.csv")
```

<!-- The above commands can also be executed via the terminal/cmd line:

```bash
python3 scripts/update_subdivisions.py --alpha_code=DZ --subdivision_code=DZ-99 --name=Timimoun --local_name="ولاية تيميمون" --type_=Province --lat_lng="[29.263, 0.241]"
```

```bash
python3 scripts/update_subdivisions.py --alpha_code=IE --subdivision_code=IE-WD --name=Waterford --local_name="Port Láirge" --type_=County --lat_lng="[52.260, -7.110]" --parent_code=IE-M --flag="https://github.com/amckenna41/iso3166-flags/blob/main/iso3166-2-flagss/IE/IE-WD.png"
```

```bash
python3 scripts/update_subdivisions.py --alpha_code=FI --subdivision_code=FI-17 --name=Satakunta
```

```bash
python3 scripts/update_subdivisions.py --alpha_code=FR --subdivision_code=FR-GP --delete
python3 scripts/update_subdivisions.py --alpha_code=FR --subdivision_code=FR-MQ --delete
```

```bash
python3 scripts/update_subdivisions.py  --subdivision_csv=new_subdivisions.csv
``` -->

<!-- Requirements (local_other_names.py)
-----------------------------------
* [python][python] >= 3.9
* [pandas][pandas] >= 1.4.3
* [numpy][numpy] >= 1.23.2
* [pycountry][pycountry] >= 22.3.5 -->


Usage: local_other_names.py
---------------------------
The [`local_other_names.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/local_other_names.py) script is used for implementing the data from the [`local_other_names.csv`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_resources/local_other_names.csv) dataset. This dataset holds thousands of individual alternative names for each subdivision that are incorporated in the `localOtherName` attribute in the iso3166-2 dataset. The `add_local_other_names()` function streamlines the addition of all the local/other names data of each subdivision to the main iso3166-2 data object. Additionally, it also contains the `validate_local_other_names()` function that validates the local/other name data per subdivision, prior to being incorporated into the dataset. The final function `convert_iso_639_language_codes()` was a temporary auxillary function that converted all the language codes per local/other name into their offiical ISO 639 3 letter counterparts.

There are no individual usage examples for this function as it is meant to be used within the `export_iso3166_2` script and is not meant to be called on its own.


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

Usage: export_iso3166_2_metadata.py
-----------------------------------
The [`export_iso3166_2_metadata.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/export_iso3166_2_metadata.py) script exports a file containing a verbose collection of useful data attributes. These include:  


```bash
python3 scripts/export_iso3166_2_metadata.py --export_filename="iso3166_2_metadata.csv"
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
[rest-countries-api]: https://restcountries.com/
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