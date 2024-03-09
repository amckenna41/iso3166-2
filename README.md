# ISO 3166-2 🌎

[![iso3166_2](https://img.shields.io/pypi/v/iso3166-2)](https://pypi.org/project/iso3166-2/)
[![pytest](https://github.com/amckenna41/iso3166-2/workflows/Building%20and%20Testing/badge.svg)](https://github.com/amckenna41/iso3166-2/actions?query=workflowBuilding%20and%20Testing)
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/amckenna41/iso3166-2/tree/main.svg?style=svg&circle-token=b9d41c530558587fb44ade899c532158d885b193)](https://dl.circleci.com/status-badge/redirect/gh/amckenna41/iso3166-2/tree/main)
[![PythonV](https://img.shields.io/pypi/pyversions/iso3166-2?logo=2)](https://pypi.org/project/iso3166-2/)
[![Platforms](https://img.shields.io/badge/platforms-linux%2C%20macOS%2C%20Windows-green)](https://pypi.org/project/iso3166-2/)
[![Documentation Status](https://readthedocs.org/projects/iso3166-2/badge/?version=latest)](https://iso3166-2.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/github/license/amckenna41/iso3166-2)](https://opensource.org/licenses/MIT)
[![Issues](https://img.shields.io/github/issues/amckenna41/iso3166-2)](https://github.com/amckenna41/iso3166-2/issues)
[![Size](https://img.shields.io/github/repo-size/amckenna41/iso3166-2)](https://github.com/amckenna41/iso3166-2)
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
- [Introduction](#introduction)
- [Latest Updates](#latest-updates)
- [API](#api)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Usage](#usage-iso3166_2_scriptsupdate_subdivisionspy)
- [Directories](#directories)
- [Issues or Contributing](#issues-or-contributing)
- [Contact](#contact)
- [References](#references)
- [Support](#support)

Introduction
------------
The International Organisation for Standards defines codes for the names of countries, dependent territories, special areas of geographical interest, and their principal subdivisions [[1]](#references). The ISO 3166-2 defines codes for identifying the principal subdivisions (e.g. provinces, states, municipalities etc) of all countries coded in the ISO 3166-1. The official name of the standard is <i>"Codes for the representation of names of countries and their subdivisions – Part 2: Country subdivision code."</i> For some countries, codes are defined for more than one level of subdivisions. 

Currently, this package and accompanying API support subdivision data from **250** officially assigned code elements within the ISO 3166-1, with **200** of these countries having recognised subdivisions (50 entires have 0 subdivisions), totalling **5,039** subdivisions across the whole dataset. Transitional reservations are not included and only 4 of the exceptional reservations, that have now been officially assigned, are included: AX (Aland Islands), GG (Guernsey), IM (Isle of Man) and JE (Jersey) [[3]](#references). The ISO 3166-2 was first published in 1998 and as of **November 2023** there are **5,039** codes defined in it [[2]](#references).

The full list of subdivision data attributes supported are:

* Name (subdivsion name)
* Local name (subdivision name in local language)
* Code (subdivision code)
* Parent Code (subdivision parent code)
* Type (subdivision type, e.g. region, state, canton, parish etc)
* Latitude/Longitude (subdivision coordinates)
* Flag (subdivsion flag from [`iso3166-flag-icons`](https://github.com/amckenna41/iso3166-flag-icons) repo: this is another ISO 3166 related custom-built dataset)

The above 7 attributes were chosen as they are the most relevant and useful pieces of data for each subdivision. Other attributes are available in scattered data sources such as area, population, regional name translations, geonames ID, FIPS code etc but these are less relevant than the ones included, unless someone really desires the population of the Bhutan region of Bumthang (17,820 btw). It was an aim during development to make the package as lightweight as possible, therefore for example if the 5 aforementioned attributes were included for the existing **5,039** codes, this would significantly increase the size of the dataset from **~1.6MB to ~2.8MB**. 

Motivation
----------
The primary motivation for building this software was for use in my [`iso3166-flag-icons`](https://github.com/amckenna41/iso3166-flag-icons) project. When building the dataset of flags, I found that some existing projects/softwares were inaccurate, outdated and or not maintained. As mentioned the ISO 3166-2 is a dynamic and ever-changing standard therefore it can be difficult to maintain and keep up-to-date; although in the case for this software, that problem is largely alleviated thanks to the custom-built [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) package (see next section).

Furthermore, there are existing toolkits and datasets that offer a rich collection of regional attributes data, [geonames](https://www.geonames.org/) for example. Although, many of these datasets are very large in size and difficult to parse, with an abundance of unessential data attributes. Thus the aim during development was to build a lightweight ISO 3166-2 dataset with the most sought data attributes that can be easily packaged into a Python package.  

Latest Updates
--------------
An important thing to note about the ISO 3166-2 and its subdivision codes/names is that changes are made consistently to it, from a small subdivision name change to an addition/deletion of a whole subdivision. These changes can happen due for a variety of geopolitical and administrative reasons. Therefore, it's important that this library and its JSON have the most **up-to-date, accurate and reliable data**. To achieve this, the custom-built [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) repo was created.

The [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) repo is another open-source software package and accompanying API that pulls the latest updates and changes for any and all countries in the ISO 3166 from a variety of data sources including the ISO website itself. A script is called periodically to check for any updates/changes to the subdivisions, which are communicated via the ISO's Online Browsing Platform [[4]](#references), and will then be manually incorporated into this repo. Please visit the repository home page for more info about the purpose and process of the software and API - [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates).

The list of ISO 3166 updates was last updated on <strong>March 2024</strong>. A log of the latest ISO 3166 updates can be seen in the [UPDATES.md][updates_md] file.

API
---
The main API endpoint is:

> [https://iso3166-2-api.vercel.app/api](https://iso3166-2-api.vercel.app/api)

The other endpoints available in the API are:
* https://iso3166-2-api.vercel.app/api/all
* https://iso3166-2-api.vercel.app/api/alpha/<input_alpha>
* https://iso3166-2-api.vercel.app/api/country_name/<input_country_name>
* https://iso3166-2-api.vercel.app/api/subdivision/<input_subdivision>
* https://iso3166-2-api.vercel.app/api/name/<input_subdivision_name>

Five paths/endpoints are available in the API - `/api/all`, `/api/alpha`, `/api/country_name`, `/api/subdivision` and `/api/name`.

* The `/api/all` path/endpoint returns all of the ISO 3166 subdivision data for all countries.

* The `/api/alpha` endpoint accepts the 2 letter alpha-2, 3 letter alpha-3 and or numeric ISO 3166-1 country codes appended to the path/endpoint e.g. `/api/alpha/JP`. A single alpha-2, alpha-3 or numeric code or list of them can be passed to the API e.g. `/api/alpha/FR,DE,HU,ID,MA`, `/api/alpha/FRA,DEU,HUN,IDN,MAR` and `/api/alpha/428,504,638`. If an invalid country code is input then an error will be returned.

* The `/api/country_name` endpoint accepts the country/territory name as it is most commonly known in english, according to the ISO 3166-1 e.g. `/api/country_name/Denmark`. A single country name or list of them can be passed into the API e.g. `/api/country_name/France,Moldova,Benin`. A closeness function is utilised so the most approximate name from the input will be used e.g. Sweden will be used if input is `/api/country_name/Swede`. If no country is found from the closeness function or an invalid name is input then an error will be returned.

* The `/api/subdivision` endpoint accepts the ISO 3166-2 subdivision codes, e.g `/api/subdivision/GB-ABD`. You can also input a list of subdivision codes from the same and or different countries and the data for each will be returned e.g `/api/subdivision/IE-MO,FI-17,RO-AG`. If the input subdivision code is not in the correct format then an error will be raised. Similarly if an invalid subdivision code that doesn't exist is input then an error will be raised.

* The `/api/name/` endpoint accepts the ISO 3166-2 subdivision names, e.g `/api/name/Derry`. You can also input a list of subdivision name from the same or different countries and the data for each will be returned e.g `/api/name/Paris,Frankfurt,Rimini`. A closeness function is utilised to find the matching subdivision name, if no exact name match found then the most approximate subdivisions will be returned. Some subdivisions may have the same name, in this case each subdivision and its data will be returned e.g `/api/name/Saint George,Sucre`. This endpoint also has the likeness score (`?likeness=`) query string parameter that can be appended to the URL. This can be set between 1 - 100, representing a % of likeness to the input name the return subdivisions should be, e.g: a likeness score of 90 will return fewer potential matches whose name only match to a high degree compared to a score of 10 which will create a larger search space, thus returning more potential subdivision matches. A default likeness of 100 (exact match) is used, if no match found then this is reduced to 90. If an invalid subdivision name that doesn't match any is input then an error will be raised.

* The main API endpoint (`/` or `/api`) will return the homepage and API documentation.

The API documentation and usage with all useful commands and examples to the API is available on the [API.md][api_md] file. A demo of the software and API is available [here][demo].

Requirements
------------
* [python][python] >= 3.8
* [iso3166][iso3166] >= 2.1.1
* [natsort][natsort] >= 8.4.0
* [unidecode][unidecode] >= 1.3.8
* [thefuzz][thefuzz] >= 0.22.1

Installation
------------
Install the latest version of `iso3166-2` via [PyPi][PyPi] using pip:

```bash
pip install iso3166-2 --upgrade
```

Usage
-----
The main JSON <i>iso3166-2.json</i> contains each country's ISO 3166-2 subdivision data and attributes. The data can be accessed after creating an instance of the <i>ISO3166_2</i> class, with the instance being subscriptable such that data can be accessed via their ISO 3166-1 alpha-2, alpha-3 or numeric country codes.

**Import ISO3166_2 class and access the subdivision data:**
```python
from iso3166_2 import *

#create instance of ISO3166_2 class
iso = ISO3166_2()

#access all country's subdivision data
canada_iso3166_2 = iso["CA"]
denmark_iso3166_2 = iso["DK"]
estonia_iso3166_2 = iso["EST"]
peru_iso3166_2 = iso["PER"]
fiji_haiti_guyana_iso3166_2 = iso["FJ, HTI, 328"]
```

**Get a specific subdivision's info:**
```python
from iso3166_2 import *

#create instance of ISO3166_2 class
iso = ISO3166_2()

iso["CA"]['CA-AB'] #Alberta subdivision
iso["DK"]['DK-81'] #Nordjylland subdivision
iso["EST"]['EE-899'] #Viljandi subdivision
iso["FJI"]['FJ-03'] #Cakaudrove subdivision 
iso["604"]['PE-AMA'] #Amarumayu subdivision
```

**Get individual attribute values per subdivision:**
```python
from iso3166_2 import *

#create instance of ISO3166_2 class
iso = ISO3166_2()

iso["CA"]['CA-AB'].latLng #Alberta subdivision latitude/longitude
iso["DK"]['DK-81'].flagUrl #Nordjylland subdivision flag URL
iso["EST"]['EE-899'].name #Viljandi subdivision name
iso["FJI"]['FJ-03'].type #Cakaudrove subdivision type
iso["604"]['PE-AMA'].parentCode #Amarumayu subdivision
```

**Get all ISO 3166-2 data for all countries:**
```python
from iso3166_2 import *

#create instance of ISO3166_2 class
iso = ISO3166_2()

#get all subdivision data using all attribute
iso.all
```
**Searching for a specific subdivision via its subdivision name attribute: the search functionality will search over all subdivisions in the object, 
returning either a subdivision with the exact match or subdivisions whose 
names approximately match the sought input name according to the likeness 
input parameter:**
```python
from iso3166_2 import *

#searching for the Monaghan county in Ireland (IE-MN) - returning exact matching subdivision
iso.search("Monaghan")

#searching for any subdivisions that have "Southern" in their name, using a likeness score of 0.8
iso.country.search("Southern", likeness=0.8)
```

**Adding a custom subdivision to the iso3166-2 object: the context for this functionality is similar to that of the user-assigned 
code elements of the ISO 3166-1 standard. Custom subdivisions and subdivision 
codes can be used for in-house/bespoke applications that are using the 
iso3166-2 software but require additional custom subdivisions to be represented:**
```python
from iso3166_2 import *

#adding custom Belfast province to Ireland
iso.custom_subdivision("IE", "IE-BF", name="Belfast", local_name="Béal Feirste", type="province", lat_lng=[54.596, -5.931], parent_code=None, flag_url=None)

#deleting above custom subdivision from object
iso.custom_subdivision("IE", "IE-BF", delete=1)
```

Documentation
-------------
Documentation for installation and usage of the software and API is availble on the readthedocs platform:

<b>https://iso3166-2.readthedocs.io/en/latest/</b>


Usage (iso3166_2_scripts/update_subdivisions.py)
------------------------------------------------
The script [`iso3166_2_scripts/update_subdivisions.py`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_scripts/update_subdivisions.py) has the `update_subdivision()` function that was created to streamline the addition/amendment/deletion to any of the subdivisions in the data object. The function can accept an individual subdivision change by passing in all the required attribute values to the function directly. Alternatively, a <b>CSV</b> file with rows of the individual changes can be passed in, allowing for hundreds of changes to be made in one go. 

The primary input parameters to the `update_subdivision()` function are: <i>alpha2_code, subdivision_code, name, local_name, type, latLng, parent_code, flag_url</i> and <i>delete</i>. The first eight parameters represent the data to be added/changed to the specified country code and subdivision code (<i>alpha2_code, subdivision_code</i>) and <i>delete</i> is a boolean flag that should be set (0/1) if the input subdivision is to be deleted - by default this will be 0. For any addition, amendment or deletion, the <i>country_code</i> and <i>subdivision_code</i> parameters are required, but the remainder of the parameters are optional. If these optional parameters are not set then they will be set to null, in the case of an addition or deletion, or remain as their previous values in the case of an amendment.  

As mentioned, you can also pass in a <b>CSV</b> with rows of all the changes to be made to the subdivision object. The <b>CSV</b> has the same columns as the aforementioned function parameters, but additionally has the <i>localNameSame, notes</i> and <i>dateIssued</i> columns. <i>localNameSame</i> should be set to 1 if the subdivision local name is the same as its name, if the column is empty or 0 then the subdivision will take the value specified by the <i>localName</i> column. <i>notes</i> just contains a small description about the addition/amendment/deletion being made and <i>dateIssued</i> is the date that the subdivision change was communicated by the ISO. 

```python
from iso3166_2_scripts.update_subdivisions import *

#adding Timimoun Province of Algeria (DZ-49) to ISO 3166-2 object (date issued: 2022-11-29)
update_subdivision("DZ", "DZ-49", name="Timimoun", local_name="ولاية تيميمون", type="Province", latLng=[29.263, 0.241], parent_code=None, flag_url=None)

#adding Waterford County of Ireland (IE-WD) to ISO 3166-2 object - subdivision already present so no changes made
update_subdivision("IE", "IE-WD", "Waterford", local_name="Port Láirge", type="County", latLng=[52.260, -7.110], parent_code="IE-M", flag_url="https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/IE/IE-WD.png")
#iso.update_subdivision("IE", "IE-WD") - this will also work as only the first 2 parameters explicitly requried

#amending the subdivision name of subdivision FI-17 from Satakunda to Satakunta (date issued: 2022-11-29)
update_subdivision("FI", "FI-17", name="Satakunta")

#deleting FR-GP (Guadeloupe) and (FR-MQ Martinique) subdivisions (date issued: 2022-11-25)
update_subdivision("FR", "FR-GP", delete=1)
update_subdivision("FR", "FR-MQ", delete=1)

#error raised as both country_code and subdivision_code parameters required
update_subdivision(type="region", latLng=[], parent_code=None)

#passing in a csv with rows of subdivision additions/updates/deletions (iso3166_2_updates/subdivision_updates.csv)
update_subdivision(subdivision_csv="iso3166_2_updates/subdivision_updates.csv")
```

Directories
-----------
* `/iso3166_2` - source code for `iso3166-2` software.
* `/iso3166_2_scripts` - scripts for pulling all the ISO 3166 data and for adding/amending/deleting subdivisions to the dataset.
* `/iso3166_2_updates` - contains CSV file for listing any changes/updates to be made to the dataset (subdivision_updates.csv) via functionality in the /iso3166_2_scripts dir and a CSV of all subdivisions and their respective local names (local_names.csv).
* `/docs` - documentation for `iso3166-2`, available on [readthedocs](https://iso3166-2.readthedocs.io/en/latest/).
* `/tests` - unit and integration tests for `iso3166-2`
* `API.md` - info and useful commands/examples for this software's accompanying API - **iso3166-2-api**
* `UPDATES.md` - markdown file listing all of the additions, amendments and deletions to the ISO 3166-2 dataset (dating from 2022), exported via the [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) software.

Issues or Contributing
----------------------
Any issues, bugs or enhancements can be raised via the [Issues][issues] tab in the repository. If you would like to contribute any functional/feature changes to the project, please make a Pull Request.

Contact
-------
If you have any questions, comments or suggestions, please contact amckenna41@qub.ac.uk or raise an issue in the [Issues][issues] tab.  <br><br>
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
[unidecode]: https://pypi.org/project/Unidecode/
[thefuzz]: https://github.com/seatgeek/thefuzz/tree/master
[numpy]: https://numpy.org/
[PyPi]: https://pypi.org/project/iso3166-2/
[iso3166-updates]: https://github.com/amckenna41/iso3166-updates
[demo]: https://colab.research.google.com/drive/1btfEx23bgWdkUPiwdwlDqKkmUp1S-_7U?usp=sharing
[demo_get_iso3166_2]: https://colab.research.google.com/drive/1PXMhpazjsLXVr33RSLZ3w7Tq0RomwPol?usp=sharing
[api]: https://iso3166-2-api.vercel.app/
[api_md]: https://github.com/amckenna41/iso3166-2/API.md 
[flag_icons_repo]: https://github.com/amckenna41/iso3166-flag-icons
[issues]: https://github.com/amckenna41/iso3166-2/issues
[medium]: https://ajmckenna69.medium.com/iso3166-2-71a13d9157f7
[updates_md]: https://github.com/amckenna41/iso3166-2/blob/main/UPDATES.md