# ISO 3166-2 🌎

[![iso3166_2](https://img.shields.io/pypi/v/iso3166-2)](https://pypi.org/project/iso3166-2/)
[![pytest](https://github.com/amckenna41/iso3166-2/workflows/Building%20and%20Testing/badge.svg)](https://github.com/amckenna41/iso3166-2/actions?query=workflowBuilding%20and%20Testing)
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/amckenna41/iso3166-2/tree/main.svg?style=svg&circle-token=b9d41c530558587fb44ade899c532158d885b193)](https://dl.circleci.com/status-badge/redirect/gh/amckenna41/iso3166-2/tree/main)
[![PythonV](https://img.shields.io/pypi/pyversions/iso3166-2?logo=2)](https://pypi.org/project/iso3166-2/)
[![Platforms](https://img.shields.io/badge/platforms-linux%2C%20macOS%2C%20Windows-green)](https://pypi.org/project/iso3166-2/)
[![License: MIT](https://img.shields.io/github/license/amckenna41/iso3166-2)](https://opensource.org/licenses/MIT)
[![Issues](https://img.shields.io/github/issues/amckenna41/iso3166-2)](https://github.com/amckenna41/iso3166-2/issues)
<!-- [![Size](https://img.shields.io/github/repo-size/amckenna41/iso3166-2)](https://github.com/amckenna41/iso3166-2) -->
<!-- [![Commits](https://img.shields.io/github/commit-activity/w/amckenna41/iso3166-2)](https://github.com/iso3166-2) -->
<!-- [![codecov](https://codecov.io/gh/amckenna41/pySAR/branch/master/graph/badge.svg?token=4PQDVGKGYN)](https://codecov.io/gh/amckenna41/pySAR) -->

<div alt="images" style="justify-content: center; display:flex; margin-left=10px;">
  <img src="https://upload.wikimedia.org/wikipedia/commons/3/3d/Flag-map_of_the_world_%282017%29.png" alt="globe" height="300" width="600"/>
  <!-- <img src="https://upload.wikimedia.org/wikipedia/commons/e/e3/ISO_Logo_%28Red_square%29.svg" alt="iso" height="300" width="400"/> -->
</div>

> `iso3166-2` is a lightweight custom-built Python package, and accompanying API, that can be used to access all of the world's ISO 3166-2 subdivision data. A plethora of data attributes are available per country and subdivision including: name, local name, code, parent code, type, lat/longitude and flag. Currently, the package and API supports data from 250 countries/territories, according to the ISO 3166-1 standard. The software uses another custom-built Python package called [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates/tree/main) to ensure all the subdivision data is accurate, reliable and up-to-date.

* The front-end <b>API</b> is available [here][api].
* A <b>demo</b> of the software and API is available [here][demo].
* A <b>demo</b> of the script used to pull and export all the latest ISO 3166-2 data is available [here][demo_get_iso3166_2].
* A <b>Medium</b> article that dives deeper into `iso3166-2` is available [here][medium].

Table of Contents
-----------------
  * [Introduction](#introduction)
  * [Latest Updates](#latestupdates)
  * [API](#api)
  * [Requirements](#requirements)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Issues](#issuesorcontributing)
  * [Contact](#contact)
  * [References](#references)

Introduction
------------
`iso3166-2` is a lightweight custom-built Python package, and accompanying API, that can be used to access all of the world's ISO 3166-2 subdivision data. Here, subdivision can be used interchangably with regions/states/provinces etc. Currently, the package and API supports data from 250 countries/territories, according to the ISO 3166-1 standard. The software uses another custom-built Python package called [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates/tree/main) to ensure all the subdivision data is accurate, reliable and up-to-date. The full list of subdivision data attributes supported are:

* Name (subdivsion name)
* Local name (subdivision name in local language)
* Code (subdivision code)
* Parent Code (subdivision parent code)
* Type (subdivision type, e.g. region, state, canton, parish etc)
* Latitude/Longitude (subdivision coordinates)
* Flag (subdivsion flag from [`iso3166-flag-icons`](https://github.com/amckenna41/iso3166-flag-icons) repo)

The International Organisation for Standards defines codes for the names of countries, dependent territories, special areas of geographical interest, and their principal subdivisions [[1]](#references). The ISO 3166-2 defines codes for identifying the principal subdivisions (e.g. provinces, states, municipality etc) of all countries coded in the ISO 3166-1. The official name of the standard is "Codes for the representation of names of countries and their subdivisions – Part 2: Country subdivision code." For some countries, codes are defined for more than one level of subdivisions. Currently, this package and accompanying API support 250 officially assigned code elements along with the user assigned code XK (Kosovo). Transitional reservations are not included and only 4 of the exceptional reservations, that have now been officially assigned, are included: AX (Aland Islands), GG (Guernsey), IM (Isle of Man) and JE (Jersey) [[3]](#references).

The ISO 3166-2 was first published in 1998 and as of November 2023 there are 5,039 codes defined in it [[2]](#references).

Latest Updates
--------------
An important thing to note about the ISO 3166-2 and its subdivision codes/names is that changes are made consistently to it, from a small subdivision name change to an addition/deletion of a whole subdivision. These changes can happen due for a variety of geopolitical and administrative reasons. Therefore, it's important that this library and its JSON have the most up-to-date, accurate and reliable data. To achieve this, the custom-built [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) repo was created.

The [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) repo is another open-source software package and accompanying API that pulls the latest updates and changes for any and all countries in the ISO 3166 from a variety of data sources including the ISO website itself. A script is called every few months to check for any updates/changes to the subdivisions, which are communicated via the ISO's Online Browsing Platform [[4]](#references), and will then be manually incorporated into this repo. Please visit the repository home page for more info about the purpose and process of the software and API - [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates).

The list of ISO 3166 updates was last updated on <strong>Nov 2023</strong>. A log of the latest ISO 3166 updates can be seen in the [UPDATES.md][updates_md] file.

API
---
The main API endpoint is:

> [https://iso3166-2-api.vercel.app/api](https://iso3166-2-api.vercel.app/api)

The other endpoints available in the API are:
* https://iso3166-2-api.vercel.app/api/all
* https://iso3166-2-api.vercel.app/api/alpha2/<input_alpha2>
* https://iso3166-2-api.vercel.app/api/name/<input_name>

Three paths/endpoints are available in the API - `/api/all`, `/api/alpha2` and `/api/name`.

* The `/api/all` path/endpoint returns all of the ISO 3166 subdivision data for all countries.

* The `/api/alpha2` endpoint accepts the 2 letter alpha-2 country code appended to the path/endpoint e.g. <i>/api/alpha2/JP</i>. A single alpha-2 code or list of them can be passed to the API e.g. <i>/api/alpha2/FR,DE,HU,ID,MA</i>. For redundancy, the 3 letter alpha-3 counterpart for each country's alpha-2 code can also be appended to the path e.g. <i>/api/alpha2/FRA,DEU,HUN,IDN,MAR</i>. If an invalid alpha-2 code is input then an error will be returned.

* The `/api/name` endpoint accepts the country/territory name as it is most commonly known in english, according to the ISO 3166-1. The name can similarly be appended to the **name** path/endpoint e.g. <i>/api/name/Denmark</i>. A single country name or list of them can be passed into the API e.g. <i>/name/France,Moldova,Benin</i>. A closeness function is utilised so the most approximate name from the input will be used e.g. Sweden will be used if input is <i>/api/name/Swede</i>. If no country is found from the closeness function or an invalid name is input then an error will be returned.

* The main API endpoint (`/` or `/api`) will return the homepage and API documentation.

The API documentation and usage with all useful commands and examples to the API is available on the [API.md][api_md] file. A demo of the software and API is available [here][demo].

Requirements
------------
* [python][python] >= 3.8
* [iso3166][iso3166] >= 2.1.1

Requirements (iso3166_2_scripts/get_iso3166_2.py)
-------------------------------------------------
* [python][python] >= 3.8
* [iso3166-2][iso3166_2] >= 1.5.0
* [requests][requests] >= 2.28.1
* [iso3166][iso3166] >= 2.1.1
* [pycountry][pycountry] >= 22.3.5
* [googlemaps][googlemaps] >= 4.10.0
* [tqdm][tqdm] >= 4.64.0
* [natsort][natsort] >= 8.4.0
* [pandas][pandas] >= 1.4.3
* [numpy][numpy] >= 1.23.2

Installation
------------
Install the latest version of `iso3166-2` via [PyPi][PyPi] using pip:

```bash
pip3 install iso3166-2 --upgrade
```

Installation from source:
```bash
git clone -b master https://github.com/amckenna41/iso3166-2.git
cd iso3166_2
python3 setup.py install
```

Usage
-----
The main JSON <i>iso3166-2.json</i> contains each country's ISO 3166-2 subdivision data and attributes. In the main module, <i>iso3166_2.py</i>, all data from the <i>iso3166-2.json</i> is accessible via the `iso.country` object.

Import ISO3166_2 class and access the subdivision data:
```python
import iso3166_2 as iso

#access all country's subdivision data
canada_iso3166_2 = iso.country["CA"]
denmark_iso3166_2 = iso.country["DK"]
estonia_iso3166_2 = iso.country["EE"]
fiji_haiti_guyana_iso3166_2 = iso.country["FJ, HT, GY"]
peru_iso3166_2 = iso.country["PE"]
```

Get a specific subdivision's info:
```python
import iso3166_2 as iso

canada_iso3166_2['CA-AB'] #Alberta subdivision
denmark_iso3166_2['DK-81'] #Nordjylland subdivision
estonia_iso3166_2['EE-899'] #Viljandi subdivision
fiji_haiti_guyana_iso3166_2['FJ-03'] #Cakaudrove subdivision 
peru_iso3166_2['PE-AMA'] #Amarumayu subdivision
```

Get individual attribute values per subdivision:
```python
import iso3166_2 as iso

canada_iso3166_2['CA-AB'].latLng #Alberta subdivision latitude/longitude
denmark_iso3166_2['DK-81'].flagUrl #Nordjylland subdivision flag URL
estonia_iso3166_2['EE-899'].name #Viljandi subdivision name
fiji_haiti_guyana_iso3166_2['FJ-03'].type #Cakaudrove subdivision type
peru_iso3166_2['PE-AMA'].parentCode #Amarumayu subdivision
```

Get all ISO 3166-2 data for all countries:
```python
import iso3166_2 as iso

#get all subdivision data using all attribute
iso.country.all
```

Adding a custom subdivision to the iso3166-2 object. The context for this
functionality is similar to that of the user-assigned code elements of the 
ISO 3166-1 standard. Custom subdivisions and subdivision codes can be used 
for in-house/bespoke applications that are using the iso3166-2 software but 
require additional custom subdivisions to be represented:
```python
import iso3166_2 as iso

#adding custom Belfast province to Ireland
iso.country.custom_subdivision("IE", "IE-BF", name="Belfast", local_name="Béal Feirste", type="province", lat_lng=[54.596, -5.931], parent_code=None, flag_url=None)
```

Searching for a specific subdivision via its subdivision name attribute. The 
search functionality will search over all subdivisions in the object, 
returning either a subdivision with the exact match or subdivisions whose 
names approximately match the sought input name:
```python
import iso3166_2 as iso

#searching for the Monaghan county in Ireland (IE-MN) - returning exact matching subdivision
iso.country.search("Monaghan", any=False)

#searching for any subdivisions that have "Southern" in their name
iso.country.search("Southern", any=True)
```

Usage (iso3166_2_scripts/get_iso3166_2.py)
------------------------------------------
The script [`iso3166_2_scripts/get_iso3166_2.py`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_scripts/get_iso3166_2.py) is used for gathering and exporting subdivision data for ALL countries to the JSON object. It uses the [pycountry][pycountry] and [googlemaps][googlemaps] packages to gather and export all the required subdivision info. Calling the script using its default parameters will gather all the data for ALL countries, but the <i>alpha2_codes</i> parameter can be set to pull the latest data for a specific list of one or more countries (the alpha-3 code can also be input, which is then converted into its 2 letter alpha-2 counterpart).

To download all of the latest ISO 3166-2 subdivision data for ALL countries, from the main repo dir, run the `get_iso3166_2.py` in a terminal or command line below; (the script takes around <em>1 hour and 40 mins</em> to execute):

```bash
python3 iso3166_2_scripts/get_iso3166_2.py --json_filename=iso3166_2.json --output_folder=iso3166_2 --verbose

#--alpha2_codes: list of 1 or more 2 letter alpha-2 country codes (if not specified then all country codes will be used).
#--json_filename: output filename for exported JSONs.
#--output_folder: output folder to store JSONs.
#--verbose: if set to 1 then the progress of the ISO 3166-2 data export will be output.
```

To download all of the latest ISO 3166-2 subdivision data for Germany, Portugal and Spain (the data will be exported to a JSON called iso3166_2-DE,ES,PT.json):
```bash
python3 iso3166_2_scripts/get_iso3166_2.py --alpha2_codes=DE,PT,ES --json_filename=iso3166_2.json 
```

Usage (iso3166_2_scripts/update_subdivisions.py)
------------------------------------------------
The script [`iso3166_2_scripts/update_subdivisions.py`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_scripts/update_subdivisions.py) has the `update_subdivision()` function that was created to streamline the addition/amendment/deletion to any of the subdivisions in the data object. The function can accept an individual subdivision change by passing in all the required attribute values to the function directly. Alternatively, a <b>CSV</b> file with rows of the individual changes can be passed in, allowing for hundreds of changes to be made in one go. 

The primary input parameters to the `update_subdivision()` function are: <i>alpha2_code, subdivision_code, name, local_name, type, latLng, parent_code, flag_url</i> and <i>delete</i>. The first eight parameters represent the data to be added/changed to the specified country code and subdivision code (<i>alpha2_code, subdivision_code</i>) and <i>delete</i> is a boolean flag that should be set (0/1) if the input subdivision is to be deleted - by default this will be 0. For any addition, amendment or deletion, the <i>country_code</i> and <i>subdivision_code</i> parameters are required, but the remainder of the parameters are optional. If these optional parameters are not set then they will be set null, in the case of an addition or deletion, or remain as their previous values in the case of an amendment.  

As mentioned, you can also pass in a <b>CSV</b> with rows of all the changes to be made to the subdivision object. The <b>CSV</b> has the same columns as the aforementioned function parameters, but additionally has the <i>localNameSpelling, notes</i> and <i>dateIssued</i> columns. <i>localNameSpelling</i> should be set to 1 if the subdivision local name is the same as its name, if the column is empty or 0 then the subdivision will take the value specified by the <i>localName</i> column. <i>notes</i> just contains a small description about the addition/amendment/deletion being made and <i>dateIssued</i> is the date that the subdivision change was communicated by the ISO. 

```python
from iso3166_2_scripts.update_subdivisions import *

#adding Timimoun Province of Algeria (DZ-49) to ISO 3166-2 object (from newsletter 2022-11-29)
update_subdivision("DZ", "DZ-49", name="Timimoun", local_name="ولاية تيميمون", type="Province", latLng=[29.263, 0.241], parent_code=None, flag_url=None)

#adding Waterford County of Ireland (IE-WD) to ISO 3166-2 object - subdivision already present so no changes made
update_subdivision("IE", "IE-WD", "Waterford", local_name="Port Láirge", type="County", latLng=[52.260, -7.110], parent_code="IE-M", flag_url="https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/IE/IE-WD.png")
#iso.update_subdivision("IE", "IE-WD") - this will also work as only the first 2 params requried

#amending the subdivision name of subdivision FI-17 from Satakunda to Satakunta (from newsletter 2022-11-29)
update_subdivision("FI", "FI-17", name="Satakunta")

#deleting FR-GP (Guadeloupe) and (FR-MQ Martinique) subdivisions 
update_subdivision("FR", "FR-GP", delete=1)
update_subdivision("FR", "FR-MQ", delete=1)

#error raised as both country_code and subdivision_code parameters required
update_subdivision(type="region", latLng=[], parent_code=None)

#passing in a csv with rows of subdivision additions/updates/deletions
update_subdivision(subdivision_csv="new_subdivisions.csv")
```

Issues or Contributing
----------------------
Any issues, bugs or enhancements can be raised via the [Issues][issues] tab in the repository. If you would like to contribute to this project, please make a PR.

Contact
-------
If you have any questions or comments, please contact amckenna41@qub.ac.uk or raise an issue in the [Issues][issues] tab.  <br><br>
<!-- [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/adam-mckenna-7a5b22151/) -->

References
----------
\[1\]: https://en.wikipedia.org/wiki/ISO_3166 <br>
\[2\]: https://en.wikipedia.org/wiki/ISO_3166-2 <br>
\[3\]: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2 <br>
\[4\]: https://www.iso.org/obp/ui/#

Support
-------
<a href="https://www.buymeacoffee.com/amckenna41" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

[Back to top](#TOP)

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
[PyPi]: https://pypi.org/project/iso3166-2/
[iso3166-updates]: https://github.com/amckenna41/iso3166-updates
[demo]: https://colab.research.google.com/drive/1btfEx23bgWdkUPiwdwlDqKkmUp1S-_7U?usp=sharing
[demo_get_iso3166_2]: https://colab.research.google.com/drive/1PXMhpazjsLXVr33RSLZ3w7Tq0RomwPol?usp=sharing
[api]: https://iso3166-2-api.vercel.app/
[api_md]: https://github.com/amckenna41/iso3166-2/API.md 
[flag_icons_repo]: https://github.com/amckenna41/iso3166-flag-icons
[issues]: https://github.com/amckenna41/iso3166-2/issues
[medium]: https://github.com/amckenna41/iso3166-2
[updates_md]: https://github.com/amckenna41/iso3166-2/blob/main/UPDATES.md