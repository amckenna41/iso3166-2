# Scripts for exporting and updating all ISO 3166-2 data

* The [`get_iso3166_2.py`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_scripts/get_iso3166_2.py) script is used for pulling and exporting the latest ISO 3166-2 data from the various data sources
* The [`update_subdivisions.py`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_scripts/update_subdivisions.py) script is used for adding, amending and or deleting subdivisions to the `iso3166-2` software and object.

Requirements (get_iso3166_2.py)
------------------------------
* [python][python] >= 3.8
* [iso3166-2][iso3166_2] >= 1.5.5
* [requests][requests] >= 2.28.1
* [iso3166][iso3166] >= 2.1.1
* [pycountry][pycountry] >= 22.3.5
* [googlemaps][googlemaps] >= 4.10.0
* [tqdm][tqdm] >= 4.64.0
* [natsort][natsort] >= 8.4.0
* [pandas][pandas] >= 1.4.3
* [numpy][numpy] >= 1.23.2

Usage (get_iso3166_2.py)
------------------------
The script `get_iso3166_2.py` is used for gathering and exporting subdivision data for ALL countries to the JSON object. It uses the [pycountry][pycountry] and [googlemaps][googlemaps] packages to gather and export all the required subdivision info. Calling the script using its default parameters will gather all the data for ALL countries in the ISO 3166, but the <i>alpha_codes</i> parameter can be set to pull the latest data for a specific list of one or more countries using their ISO 3166-1 alpha codes (alpha-2, alpha-3 or numeric codes).

There is additional functionality whereby you can include additional attributes/fields for each country's subdivision in the output object. These attributes are extracted using the [RestCountries API](https://restcountries.com/) and can be passed in via the <i>rest_countries_keys</i> parameter. Note that each attribute will be at the country level not subdivision. The following fields are supported: idd, carSigns, carSide, continents, currencies, languages, postalCode, region, startOfWeek, subregion, timezones and tld. An explanation of each of these attributes can be seen on the [RestCountries](https://gitlab.com/restcountries/restcountries/-/blob/master/FIELDS.md) repo.

By default when running this script the following default attributes are exported per subdivision: name, localName, type, parentCode, flag and lat_lng. If one or more of these are not required then they can be excluded by passing in the attribute name/names to the <i>exclude_default_keys</i> parameter.

To download all of the latest ISO 3166-2 subdivision data for all countries, from the main repo dir, run the `get_iso3166_2.py` in a terminal or command line below; (the script takes around **1 hour and 40 mins** to execute):
```bash
python3 iso3166_2_scripts/get_iso3166_2.py --export_filename=iso3166_2.json --export_folder=iso3166_2 --verbose --export_csv

#--alpha_codes: list of 1 or more ISO 3166-1 alpha country codes (if not specified then all country codes will be used).
#--export_filename: output filename for exported JSON object.
#--export_folder: output folder to store JSON object.
#--verbose: if set to 1 then the progress of the ISO 3166-2 data export will be output.
#--export_csv: if set to 1 then dataset will be exported to a CSV, JSON exported by default.
#--rest_countries_keys: list of additional fields/attributes from RestCountries API to be added to each subdivision object.
#--exclude_default_keys: list of default fields/attributes to be excluded from each country's subdivision object.
#--alpha_codes_start_from: beginning alpha code to start the export functionality from, alphabetically.
```

To download all of the latest ISO 3166-2 subdivision data for Germany, Portugal and Spain (the data will be exported to a JSON and CSV file called <em>iso3166_2-DE,ES,PT.json, iso3166_2-DE,ES,PT.csv</em>):
```bash
python3 iso3166_2_scripts/get_iso3166_2.py --alpha_codes=DE,PT,ESP --export_filename=iso3166_2.json --verbose --export_csv
```

To download all of the latest ISO 3166-2 subdivision data for all countries, additionally including the languages, subregion and tld attributes for each subdivision:
```bash
python3 iso3166_2_scripts/get_iso3166_2.py --export_filename=iso3166_2.json --rest_countries_keys=languages,subregion,tld --verbose --export_csv
```

To download all of the latest ISO 3166-2 subdivision data for all countries, excluding the default attributes of lat_lng and flag:
```bash
python3 iso3166_2_scripts/get_iso3166_2.py --export_filename=iso3166_2.json --exclude_default_keys=lat_lng,flag --verbose --export_csv
```

Requirements (update_subdivisions.py)
-------------------------------------
* [python][python] >= 3.8
* [iso3166][iso3166] >= 2.1.1
* [natsort][natsort] >= 8.4.0
* [pandas][pandas] >= 1.4.3
* [numpy][numpy] >= 1.23.2

Usage (update_subdivisions.py)
------------------------------
The script [`update_subdivisions.py`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_scripts/update_subdivisions.py) has the `update_subdivision()` function that was created to streamline the addition, amendment and or deletion to any of the subdivisions in the data object. The function can accept an individual subdivision change by passing in all the required attribute values to the function directly. Alternatively, a <b>CSV</b> file with rows of the individual changes can be passed in, allowing for hundreds of changes to be made in one go (this is the recommended and fastest approach). 

The primary input parameters to the `update_subdivision()` function are: <i>alpha_code, subdivision_code, name, local_name, type, lat_lng, parent_code, flag</i> and <i>delete</i>. The first eight parameters represent the data to be added or changed to the specified country code and subdivision code (<i>alpha2_code, subdivision_code</i>) and <i>delete</i> is a boolean flag that should be set (0/1) if the input subdivision is to be deleted - by default this will be 0. For any addition, amendment and or deletion, the <i>country_code</i> and <i>subdivision_code</i> parameters are required, but the remainder of the parameters are optional. If these optional parameters are not input then they will be set to null for the subdivision, in the case of an addition or deletion, or remain as their previous value in the case of an amendment.  

As mentioned, you can also pass in a <b>CSV</b> with rows of all the changes to be made to the subdivision object e.g [subdivision_updates.csv](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_updates/subdivision_updates.csv). The <b>CSV</b> has the same columns as the aforementioned function parameters, but additionally has the <i>localNameSame, notes</i> and <i>dateIssued</i> columns. <i>localNameSame</i> should be set to 1 if the subdivision local name is the same as its name, if the column is empty or 0 then the subdivision will take the value specified by the <i>localName</i> column. <i>notes</i> just contains a small description about the addition, amendment and or deletion being made and <i>dateIssued</i> is the date that the subdivision change was communicated by the ISO. 

```python
from iso3166_2_scripts.update_subdivisions import *

#adding Timimoun Province of Algeria (DZ-49) to ISO 3166-2 object (from newsletter 2022-11-29)
update_subdivision("DZ", "DZ-49", name="Timimoun", local_name="ولاية تيميمون", type_="Province", lat_lng=[29.263, 0.241], parent_code=None, flag=None)

#adding Waterford County of Ireland (IE-WD) to ISO 3166-2 object - subdivision already present so no changes made
update_subdivision("IE", "IE-WD", "Waterford", local_name="Port Láirge", type_="County", lat_lng=[52.260, -7.110], parent_code="IE-M", flag="https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/IE/IE-WD.png")
#iso.update_subdivision("IE", "IE-WD") - this will also work as only the first 2 params requried

#amending the subdivision name of subdivision FI-17 from Satakunda to Satakunta (from newsletter 2022-11-29)
update_subdivision("FI", "FI-17", name="Satakunta")

#deleting FR-GP (Guadeloupe) and (FR-MQ Martinique) subdivisions (from newsletter 2021-11-25)
update_subdivision("FR", "FR-GP", delete=1)
update_subdivision("FR", "FR-MQ", delete=1)

#error raised as both country_code and subdivision_code parameters required
update_subdivision(type_="region", lat_lng=[], parent_code=None)

#error raised as only one alpha code and subdivision code should be passed in
update_subdivision("IE", "IE-WD,IE-WW")

#passing in a csv with rows of subdivision additions/updates/deletions
update_subdivision(subdivision_csv="new_subdivisions.csv")
```

The above commands can also be executed via the terminal/cmd line:

```bash
python3 iso3166_2_scripts/update_subdivisions.py --alpha_code=DZ --subdivision_code=DZ-99 --name=Timimoun --local_name="ولاية تيميمون" --type_=Province --lat_lng="[29.263, 0.241]"
```

```bash
python3 iso3166_2_scripts/update_subdivisions.py --alpha_code=IE --subdivision_code=IE-WD --name=Waterford --local_name="Port Láirge" --type_=County --lat_lng="[52.260, -7.110]" --parent_code=IE-M --flag="https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/IE/IE-WD.png"
```

```bash
python3 iso3166_2_scripts/update_subdivisions.py --alpha_code=FI --subdivision_code=FI-17 --name=Satakunta
```

```bash
python3 iso3166_2_scripts/update_subdivisions.py --alpha_code=FR --subdivision_code=FR-GP --delete
python3 iso3166_2_scripts/update_subdivisions.py --alpha_code=FR --subdivision_code=FR-MQ --delete
```

```bash
python3 iso3166_2_scripts/update_subdivisions.py  --subdivision_csv=new_subdivisions.csv
```


[python]: https://www.python.org/downloads/release/python-360/
[requests]: https://requests.readthedocs.io/
[iso3166]: https://github.com/deactivated/python-iso3166
[iso3166_2]: https://github.com/amckenna41/iso3166-2
[pycountry]: https://github.com/flyingcircusio/pycountry
[rest]: https://restcountries.com/
[googlemaps]: https://github.com/googlemaps/google-maps-services-python
[tqdm]: https://github.com/tqdm/tqdm
[natsort]: https://pypi.org/project/natsort/
[pandas]: https://pandas.pydata.org/
[numpy]: https://numpy.org/
[iso3166-updates]: https://github.com/amckenna41/iso3166-updates
[flag_icons_repo]: https://github.com/amckenna41/iso3166-flag-icons