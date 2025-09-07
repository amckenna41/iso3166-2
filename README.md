<a name="TOP"></a>

# iso 3166-2 🌎

[![iso3166_2](https://img.shields.io/pypi/v/iso3166-2)](https://pypi.org/project/iso3166-2/)
[![status](https://img.shields.io/badge/status-stable-green)](https://github.com/amckenna41/iso3166-2)
[![pytest](https://github.com/amckenna41/iso3166-2/workflows/Building%20and%20Testing/badge.svg)](https://github.com/amckenna41/iso3166-2/actions?query=workflowBuilding%20and%20Testing)
<!-- [![CircleCI](https://dl.circleci.com/status-badge/img/gh/amckenna41/iso3166-2/tree/main.svg?style=svg&circle-token=b9d41c530558587fb44ade899c532158d885b193)](https://dl.circleci.com/status-badge/redirect/gh/amckenna41/iso3166-2/tree/main) -->
[![PythonV](https://img.shields.io/pypi/pyversions/iso3166-2?logo=2)](https://pypi.org/project/iso3166-2/)
[![Platforms](https://img.shields.io/badge/platforms-linux%2C%20macOS%2C%20Windows-green)](https://pypi.org/project/iso3166-2/)
[![Documentation Status](https://readthedocs.org/projects/iso3166-2/badge/?version=latest)](https://iso3166-2.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/amckenna41/iso3166-2/branch/main/graph/badge.svg)](https://codecov.io/gh/amckenna41/iso3166-2)
[![License: MIT](https://img.shields.io/github/license/amckenna41/iso3166-2)](https://opensource.org/licenses/MIT)
[![Issues](https://img.shields.io/github/issues/amckenna41/iso3166-2)](https://github.com/amckenna41/iso3166-2/issues)
<!-- [![Size](https://img.shields.io/github/repo-size/amckenna41/iso3166-2)](https://github.com/amckenna41/iso3166-2) -->
<!-- [![Commits](https://img.shields.io/github/commit-activity/w/amckenna41/iso3166-2)](https://github.com/iso3166-2) -->
<!-- [![codecov](https://codecov.io/gh/amckenna41/iso3166-2/branch/main/graph/badge.svg)](https://codecov.io/gh/amckenna41/iso3166-2) -->

<div alt="images" style="justify-content: center; display:flex; margin-left=10px;">
  <img src="https://upload.wikimedia.org/wikipedia/commons/3/3d/Flag-map_of_the_world_%282017%29.png" alt="globe" height="300" width="600"/>
  <!-- <img src="https://upload.wikimedia.org/wikipedia/commons/e/e3/ISO_Logo_%28Red_square%29.svg" alt="iso" height="300" width="400"/> -->
</div>

> `iso3166-2` is a structured lightweight custom-built Python package and dataset, and accompanying RESTful API, that can be used to access all of the world's ISO 3166-2 subdivision data. A plethora of data attributes are available per country and subdivision including: name, local/other name, code, parent code, type, lat/longitude, flag & history. Currently, the package and API supports data from 250 countries/territories and >5000 subdivisions, according to the ISO 3166-1 & ISO 3166-2 standards, respectively. The software uses another custom-built Python package called [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates/tree/main) to ensure all the subdivision data is accurate, reliable and up-to-date.

<!-- iso3166-2 Stats 🔢
------------------ -->


Quick Start 🏃
-------------
* A <b>demo</b> of the software and API is available [here][demo].
* The front-end <b>API</b> is available [here][api].
* The **documentation** for the software & API is available [here](https://iso3166-2.readthedocs.io/en/latest/).
* A <b>Medium</b> article that dives deeper into `iso3166-2` is available [here][medium].
<!-- * A <b>demo</b> of the script used to pull and export all the latest ISO 3166-2 data is available [here][demo_export_iso3166_2]. -->

Table of Contents
-----------------
- [Introduction](#introduction)
- [Bespoke Features](#bespoke-features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Latest Updates](#latest-updates)
- [API](#api)
- [Directories](#directories)
- [Issues or Contributing](#issues-or-contributing)
- [Other ISO 3166 repositories](#other-iso-3166-repositories)
- [Contact](#contact)
- [References](#references)
- [Support](#support)

## Introduction
The International Organisation for Standards defines codes for the names of countries, dependent territories, special areas of geographical interest, and their principal subdivisions [[1]](#references). The ISO 3166-2 defines codes for identifying the principal subdivisions (e.g. provinces, states, municipalities etc) of all countries coded in the ISO 3166-1. The official name of the standard is <i>"Codes for the representation of names of countries and their subdivisions – Part 2: Country subdivision code."</i> For some countries, codes are defined for more than one level of subdivisions. 

Currently, this package and accompanying API support subdivision data from **250** officially assigned code elements within the ISO 3166-1, with **200** of these countries having recognised subdivisions (50 entires have 0 subdivisions), totalling **5,049** subdivisions across the whole dataset. Transitional reservations are not included and only 4 of the exceptional reservations, that have now been officially assigned, are included: AX (Aland Islands), GG (Guernsey), IM (Isle of Man) and JE (Jersey) [[3]](#references). The ISO 3166-2 was first published in 1998 and as of **November 2024** there are **5,049** codes defined in it [[2]](#references).

The full list of subdivision data attributes supported are:

* **Code** - ISO 3166-2 subdivision code
* **Name** - subdivision name
* **Local/other name** - subdivision name in local language or any alternative name/nickname it is commonly known by
* **Parent Code** - subdivision parent code
* **Type** - subdivision type, e.g. region, state, canton, parish etc
* **Latitude/Longitude** - subdivision coordinates
* **Flag** - subdivision flag from [`iso3166-flags`](https://github.com/amckenna41/iso3166-flags) repo; this is another ISO 3166 related custom-built dataset of over **3500** regional/subdivision flags
* **History** - historical updates/changes to the subdivision code and naming conventions, as per the custom-built [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) repo.

<!-- The above 8 attributes were chosen as they are the most relevant and useful pieces of data for each subdivision. Other attributes are available in scattered data sources such as area, population, regional name translations, geonames ID, FIPS code etc, but these were deemed less relevant than the ones included... unless someone really desires the population of the Bhutan region of Bumthang (17,820 btw). It was an aim during development to make the package as lightweight as possible, therefore for example if the 5 aforementioned attributes were included for the existing **5,049** codes, this would significantly increase the size of the dataset from **~3MB to ~4MB**.  -->

### Motivation
The primary motivation for building this software was for use in my [`iso3166-flags`](https://github.com/amckenna41/iso3166-flags) project. When building the dataset of flags, I found that some existing projects/softwares were **inaccurate**, **outdated** and or **not maintained**. As mentioned, the ISO 3166-2 is a dynamic and ever-changing standard therefore it can be difficult to maintain and keep up-to-date; although in the case for this software, that problem is largely alleviated thanks to the custom-built [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) package (see below sections).

Furthermore, there are existing toolkits and datasets that offer a rich collection of regional attributes data, [geonames](https://www.geonames.org/) for example. Although, many of these datasets are very large in size and difficult to parse, with an abundance of unessential data attributes. 

Thus the aim during development was to build a **structured, lightweight and up-to-date ISO 3166-2 dataset with the most sought data attributes that can be easily packaged into a Python package.**  

<!-- ### Intended Audience
This package is particularly useful for developers and researchers building geographic information systems (GIS), global mapping tools, localization platforms, or projects involving geopolitical datasets. It’s designed to be easily integrated into Python applications with minimal overhead. -->

## Bespoke Features

There are three main attributes supported by the software that make it stand out and add a significant amount of value and data per subdivision, in comparison to some the other iso3166-2 datasets, these are the **local/other name**, **flag** and **history** attributes.

### Local/Other names
One of the most <b>important</b> and <b>bespoke</b> attributes that the software supports, that many others do not, is the **local/other name** attribute. This attribute is built from a custom dataset of local language variants and alternative names/nicknames  for the <b>over 5000</b> subdivisions. In total there are <b>>3700</b> local/other names for the <b>>5000</b> subdivisions. Primarily, the attribute contains local language translations for the subdivisions, but many also include <b>nicknames</b> and **alternative variants** that the subdivision may be known by, either locally or globally. 

For each local/other name, the ISO 639 3 letter language code is used to identify the language of the name. Some translations do not have available ISO 639 codes, therefore the [Glottolog](https://glottolog.org/) or other databases (e.g [IETF](https://support.elucidat.com/hc/en-us/articles/6068623875217-IETF-language-tags)) language codes are used. Some example local/other name entries are: 
* **Sindh (Pakistan PK-SD)**: "سِنْدھ (urd), Sindh (eng), SD (eng), Mehran/Gateway (eng), Bab-ul-Islam/Gateway of Islam (eng)"
* **Central Singapore (Singapore SG-01)**: "Pusat Singapura (msa), 新加坡中部 (zho), மத்திய சிங்கப்பூர் (tam)"
* **Bobonaro (East Timor TL-BO)**: "Bobonaru (tet), Buburnaru (tet), Tall eucalypt (eng)"
* **Wyoming (USA US-WY)** - "Equality State (eng), Cowboy State (eng), Big Wyoming (eng)"

The full dataset of local/other names is available in the repo here [`local_other_names.csv`](https://github.com/amckenna41/iso3166-2/iso3166_2_resources/local_other_names.csv)


### Flags
The other equally important and bespoke/unique attribute that the software package supports is the ``flag`` attribute, which is a link to the subdivision's flag on the [`iso3166-flags`](https://github.com/amckenna41/iso3166-flags) repo. This is another **custom-built** repository, (alongside [`iso3166-2`](https://github.com/amckenna41/iso3166-2) and [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates)) that stores a rich and comprehensive dataset of over **3500** individual subdivision flags. 

The flags repo uses the `iso3166-2` software to get the full list of ISO 3166-2 subdivision codes which is kept up-to-date and accurate via the `iso3166-updates` software. 

   <div align="center">❤️ iso3166-2 🤝 iso3166-updates 🤝 iso3166-flags ❤️</div>
   

### History
The `history` attribute has any applicable historical updates/changes to the individual subdivisions, if applicable. The data source for this is another custom-built software package previously mentioned [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates). This package keeps track of all the published changes that the ISO make to the ISO 3166 standard which include addition of new subdivisions, deletion of existing subdivisions or amendments to existing subdivisions. Thus [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) helps ensure that the data in the `iso3166-2` package is also kept up-to-date and accurate. If any updates are found for the subdivision a short description of the change, it's publication date as well as its source will be included.

   <div align="center">❤️ iso3166-2 🤝 iso3166-updates ❤️</div>


## Requirements
* [python][python] >= 3.9
* [iso3166][iso3166] >= 2.1.1
* [natsort][natsort] >= 8.4.0
* [thefuzz][thefuzz] >= 0.22.1
* [requests][requests] >= 2.28.1
<!-- * [unidecode][unidecode] >= 1.3.8 -->

## Installation
Install the latest version of `iso3166-2` via [PyPi][PyPi] using pip:

```bash
pip install iso3166-2 --upgrade
```

## Usage
All of the country's subdivision data and attributes are encapsulated into an instance of the *Subdivisions* class via the JSON object **iso3166-2.json**, which contains each country's ISO 3166-2 subdivision data. The data can be accessed after creating an instance of the <i>Subdivisions</i> class, with the instance being subscriptable such that data can be accessed via their ISO 3166-1 alpha-2, alpha-3 or numeric country codes. There also exist a plethora of additional functionalities around the subdivision data. Below are some usage examples for the software.

**Import and create instance of Subdivisions class:**
```python
from iso3166_2 import *

#create instance of Subdivisions class
iso = Subdivisions()
```

**Get all ISO 3166-2 data for all countries:**
```python
iso.all
```

**Get all subdivision data for a country, via their alpha-2, alpha-3 and numeric country codes:**
```python
canada_iso3166_2 = iso["CA"]
denmark_iso3166_2 = iso["DK"]
estonia_iso3166_2 = iso["EST"]
peru_iso3166_2 = iso["PER"]
fiji_haiti_iso3166_2 = iso["FJ, HT"]
fiji_haiti_guyana_iso3166_2 = iso["FJ, HTI, 328"]
```

**Get subdivision's data, via its subdivision code:**
```python
iso["CA"]['CA-AB'] #Alberta subdivision
iso["DK"]['DK-81'] #Nordjylland subdivision
iso["EST"]['EE-899'] #Viljandi subdivision
iso["FJI"]['FJ-03'] #Cakaudrove subdivision 
iso["PE"]["PE-LAL"] #La Libertad subdivision
iso["604"]['PE-AMA'] #Amarumayu subdivision
```

**Get individual attribute values per subdivision:**
```python
iso["CA"]['CA-AB'].latLng #Alberta subdivision latitude/longitude
iso["DK"]['DK-81'].flag #Nordjylland subdivision flag URL
iso["PE"]['PE-LAL'].history #La Libertad subdivision updates history
iso["EST"]['EE-899'].name #Viljandi subdivision name
iso["FJI"]['FJ-03'].type #Cakaudrove subdivision type
iso["604"]['PE-AMA'].parentCode #Amarumayu subdivision
```

**Get subset of subdivision attributes for all countries:**
```python
'''
If only a subset of the available default attributes are required per
subdivision, include them via the 'filter_attributes' input parameter
when creating an instance of the class. All attributes not included
in this list will be excluded.
'''
from iso3166_2 import *

#create instance of Subdivisions class
iso = Subdivisions(filter_attributes="flag,parentCode,type")
```

**Get list of subdivision codes for all or a subset of countries:**
```python
'''
The subdivision_codes(alpha_code="") function can be used to return
just a list of subdivision codes. If no code input then the codes for
all countries will be returned otherwise the input countries codes will
be returned.
'''
#get all codes
iso.subdivision_codes()

#get subset of codes
iso.subdivision_codes("DE")
iso.subdivision_codes("FO")
iso.subdivision_codes("LU,LV,WF")
```

**Get list of subdivision names for all or a subset of countries:**
```python
'''
The subdivision_names(alpha_code="") function can be used to return
just a list of subdivision names. If no code input then the names for
all countries will be returned otherwise the input countries names will
be returned.
'''
#get all names
iso.subdivision_names()

#get subset of names
iso.subdivision_names("DE")
iso.subdivision_names("FO")
iso.subdivision_names("LU,LV,WF")
```


**Searching for a specific subdivision via its subdivision name or local/other name attributes:**
```python
'''
The search functionality will search over all subdivisions in the object, 
returning either a subdivision with the exact match or subdivisions whose names 
approximately match the sought input name according to the likeness input parameter.
The likeness input parameter is a % similarity the input search terms have to be to 
the subdivision names, with 100% being an exact match, vice versa. Reducing this
value will thus increase the search space and return more like results. You can 
exclude the Match Score attribute in the search results by setting the excludeMatchScore
parameter to 1.
'''
#searching for the Monaghan county in Ireland (IE-MN) - returning exact matching subdivision (likeness=100)
iso.search("Monaghan")

#searching for Castelo Branco district in Portugal (PT-05) - returning exact matching subdivision (likeness=100)
iso.search("Castelo Branco", likeness=100)

#searching for the Roche Caiman district in Seychelles (SC-25) - returning exact matching subdivision (likeness=100)
iso.search("Roche Caiman")

#searching for any subdivisions that have "Southern" in their name, using a likeness score of 80, exclude Match Score attribute
iso.search("Southern", likeness_score=80, exclude_match_score=1)

#searching for any subdivisions that have "City" in their name or localOtherName attributes, using a likeness score of 40%
iso.search("City", likeness=40, local_other_name_search=True)

#searching for state of Texas and French Department Meuse - both subdivision objects will be returned, only including the subdivision type and name attributes
iso.search("Texas, Meuse", filter_attributes="name,type") 
```

**Adding a custom subdivision to the iso3166-2 object:**
```python
'''
The context for this functionality is similar to that of the user-assigned 
code elements of the ISO 3166-1 standard. Custom subdivisions and subdivision 
codes can be used for in-house/bespoke applications that are using the 
iso3166-2 software but require additional custom subdivisions to be represented.
You can also add custom attributes for the custom subdivision, e.g population,
area, gdp etc, via the custom_attribute parameter. You can save the custom
object with the new subdivision data added to a custom file via the save_new
and save_new_filename parameters.
'''
#adding custom Belfast province to Ireland
iso.custom_subdivision("IE", "IE-BF", name="Belfast", local_other_name="Béal Feirste", type_="province", lat_lng=[54.596, -5.931], parent_code=None, flag=None)

#adding custom Alaska province to Russia with additional population and area attribute values, save object to new file
iso.custom_subdivision("RU", "RU-ASK", name="Alaska Oblast", local_other_name="Аляска", type_="Republic", lat_lng=[63.588, 154.493], parent_code=None, flag=None, 
      custom_attributes={"population": "733,583", "gini": "0.43", "gdpPerCapita": "71,996"}, save_new=1, save_new_filename="ru-ask-custom.json")

#adding custom Republic of Molossia state to United States 
iso.custom_subdivision("US", "US-ML", name="Republic of Molossia", local_other_name="", type_="State", lat_lng=[39.236, -119.588], parent_code=None, flag="https://upload.wikimedia.org/wikipedia/commons/c/c3/Flag_of_the_Republic_of_Molossia.svg")

#deleting above custom subdivisions from object
iso.custom_subdivision("IE", "IE-BF", delete=1)
iso.custom_subdivision("US", "US-ML", delete=1)
iso.custom_subdivision("RU", "RU-ASK", delete=1)

```
**Check for the latest updates data from the repository:**
```python
'''
Compare the subdivision data in the current installed version of the 
iso3166-2 software with the most up-to-date and accurate version on
the repository. If there are any difference between these objects,
they will be output.
'''
iso.check_for_updates()
```

**Get total number of subdivisions in object:**
```python
len(iso)
```

**Get size of dataset in MB:**
```python
iso.__sizeof__()
```

## Documentation
Documentation for installation and usage of the software and API is available on the readthedocs platform:

<b>https://iso3166-2.readthedocs.io/en/latest/</b>

## Latest Updates
An important thing to note about the ISO 3166-2 and its subdivision codes/names is that changes are made consistently to it, from a small subdivision name change to an addition/deletion of a whole subdivision. These changes can happen due for a variety of geopolitical and administrative reasons. Therefore, it's important that this library and its JSON have the most **up-to-date, accurate and reliable data**. To achieve this, the custom-built [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) repo was created!

The [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) repo is another open-source software package and accompanying RESTful API that pulls the latest updates and changes for any and all countries in the ISO 3166 from a variety of data sources including the ISO website itself. A script is called periodically to check for any updates/changes to the subdivisions, which are communicated via the ISO's Online Browsing Platform [[4]](#references), and will then be manually incorporated into this repo. Please visit the repository home page for more info about the purpose and process of the software and API - [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates).

The list of ISO 3166 updates was last updated on <strong>November 2024</strong> (the last published ISO subdivision change). A log of the latest ISO 3166 updates can be seen in the [UPDATES.md][updates_md] file.

## API
The main API endpoint is:

> [https://iso3166-2-api.vercel.app/api](https://iso3166-2-api.vercel.app/api)

The other endpoints available in the API are:
* https://iso3166-2-api.vercel.app/api/all
* https://iso3166-2-api.vercel.app/api/alpha/<input_alpha>
* https://iso3166-2-api.vercel.app/api/subdivision/<input_subdivision>
* https://iso3166-2-api.vercel.app/api/search/<input_search_name>
* https://iso3166-2-api.vercel.app/api/country_name/<input_country_name>
* https://iso3166-2-api.vercel.app/api/list_subdivisions or https://iso3166-2-api.vercel.app/api/list_subdivisions/<input_alpha_code>

Six paths/endpoints are available in the API - `/api/all`, `/api/alpha`,  `/api/subdivision`, `/api/search`, `/api/country_name` and `/api/list_subdivisions`.

* `/api`: main homepage and API documentation.

* `/api/all`: get all of the ISO 3166 subdivision data for all countries.

* `/api/alpha`: get all of the ISO 3166 subdivision data for 1 or more inputted ISO 3166-1 alpha-2, alpha-3 or numeric country codes, e.g. `/api/alpha/FR,DE,HU,ID,MA`, `/api/alpha/FRA,DEU,HUN,IDN,MAR` and `/api/alpha/428,504,638`. A comma separated list of multiple alpha codes can also be input. If an invalid country code is input then an error will be returned.

* `/api/country_name`: get all of the ISO 3166 subdivision data for 1 or more inputted ISO 3166-1 country names, as they are commonly known in English, e.g. `/api/country_name/France,Moldova,Benin`. A comma separated list of country names can also be input. A closeness function is utilised so the most approximate name from the input will be used e.g. Sweden will be returned if the input is `/api/country_name/Swede`. If no country is found from the closeness function or an invalid name is input then an error will be returned. The `likeness` query string parameter can be used with this endpoint.

* `/api/search/`: get all of the ISO 3166 subdivision data for 1 or more ISO 3166-2 subdivision names that match the inputted search terms, e.g `/api/search/Derry`, `/api/search/Kimpala`. You can also input a comma separated list of subdivision name from the same or different countries and the data for each will be returned e.g `/api/name/Paris,Frankfurt,Rimini`. A closeness function is utilised to find the matching subdivision name, if no exact name match found then the most approximate subdivisions will be returned. Some subdivisions may have the same name, in this case each subdivision and its data will be returned e.g `/api/name/Saint George` (this example returns 5 subdivisions). If an invalid subdivision name that doesn't match any is input then an error will be raised. The `likeness` and `excludeMatchScore` query string parameters can be used with this endpoint. 

* `/api/subdivision`: get all of the ISO 3166 subdivision data for 1 or more ISO 3166-2 subdivision codes, e.g `/api/subdivision/GB-ABD`. You can also input a comma separated list of subdivision codes from the same and or different countries and the data for each will be returned e.g `/api/subdivision/IE-MO,FI-17,RO-AG`. If the input subdivision code is not in the correct format then an error will be raised. Similarly if an invalid subdivision code that doesn't exist is input then an error will be raised.

* `/api/list_subdivisions`: get list of all the subdivision codes for all countries. You can also get the list of subdivisions from a subset of 
countries via their ISO 3166-1 country code.

<!-- ### Attributes
There are 8 main default attributes supported for all subdivision objects that will be returned:

* **Code** - ISO 3166-2 subdivision code
* **Name** - subdivision name
* **Local/other name** - subdivision name in local language or any alternative name/nickname it is commonly known by
* **Parent Code** - subdivision parent code
* **Type** - subdivision type, e.g. region, state, canton, parish etc
* **Latitude/Longitude** - subdivision coordinates, from GoogleMaps API
* **Flag** - subdivision flag from the custom-built [`iso3166-flags`](https://github.com/amckenna41/iso3166-flags) repo; this is another ISO 3166 related custom-built dataset of over **3500** regional/subdivision flags
* **History** - historical updates/changes to the subdivision code and naming conventions, as per the custom-built [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) repo -->

### Query String Parameters
There are three main query string parameters that can be passed through several of the endpoints of the API:

* **likeness** - this is a value between 1 and 100 that increases or reduces the % of similarity/likeness that the 
inputted search terms have to match to the subdivision data in the subdivision code, name and local/other name attributes. This can be used with the `/api/search` and `/api_country_name` endpoints. Having a higher value should return more exact and less total matches and 
having a lower value will return less exact but more total matches, e.g ``/api/search/Paris?likeness=50``, 
``/api/country_name/Tajikist?likeness=90`` (default=100).
* **filterAttributes** - this is a list of the default supported attributes that you want to include in the output. By default all attributes will be returned but this parameter is useful if you only require a subset of attributes, e.g `api/alpha/DEU?filterAttributes=latLng,flag`, `api/subdivision/PL-02?filterAttributes=localOtherName`.
* **excludeMatchScore** - this allows you to exclude the matchScore attribute from the search results when using the `/api/search endpoint`. The match score is the % of a match each returned subdivision data object is to the search terms, with 100% being an exact match. By default the match score is returned for each object, e.g `/api/search/Bucharest?excludeMatchScore=1`, ``/api/search/Oregon?excludeMatchScore=1`` (default=0).


> The API documentation and usage with all useful commands and examples to the API is available on the [API.md][api_md] file. 

> A demo of the software and API is available [here][demo].


<!-- ## ISO 3166-2 Scripts
* [`scripts/export_iso3166_2.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts) - used for pulling and exporting the latest ISO 3166-2 data from the various data sources. In this script you can also export additional attributes for each country/subdivision via the RestCountries and CountryStateCity APIs.
* [`scripts/update_subdivisions.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts) - used for adding, amending and or deleting subdivisions to the `iso3166-2` software and object.
* [`scripts/local_other_names.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/local_other_names.py) - used for adding the data from the local_other_names.csv dataset, including any validation checks on the data.
* [`scripts/utils.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/utils.py) - a series of utility functions used throughout the `iso3166-2` project.
* [`scripts/language_lookup.py`](https://github.com/amckenna41/iso3166-2/blob/main/scripts/language_lookup.py) - uses the `local_other_names.csv` dataset to encapsulate and validate the hundreds of language code used throughout the dataset and project.


Please visit the [README](https://github.com/amckenna41/iso3166-2/blob/main/scripts) of the `scripts` folder for more in depth info about the usage and requirements of the above scripts that are <b>vital</b> to the `iso3166-2` software. -->

## Directories
* `/iso3166_2` - source code for `iso3166-2` software.
* `/scripts` - scripts for the full export pipeline for the ISO 3166-2 subdivision data.  -->
* `/iso3166_2_resources` - several resource/utility and dataset files required for the full export pipeline for the ISO 3166-2 subdivision data. 
* `/docs` - documentation for `iso3166-2`, available on [readthedocs](https://iso3166-2.readthedocs.io/en/latest/).
* `/tests` - unit and integration tests for `iso3166-2`
* `UPDATES.md` - markdown file listing all of the additions, amendments and deletions to the ISO 3166-2 dataset (dating from 2022), exported via the [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) software.

<!-- * `/scripts` - scripts for pulling all the ISO 3166 data (*export_iso3166_2.py*), for adding/amending/deleting subdivisions to the dataset (*update_subdivisions.py*), for adding/validating all the local/other name data in the local_other_names.csv (*local_other_names.py*) and for the various utility functions used throughout the project (*utils.py*).   -->
<!-- contains CSV file for listing any changes/updates to be made to the dataset (*subdivision_updates.csv*) via functionality in the /scripts dir, a CSV of all subdivisions and their respective local/other names (local_other_names.csv) and a language lookup file for all the language codes mentioned for any of the local/other names (language_lookup.md). -->
<!-- * `API.md` - info and useful commands/examples for this software's accompanying API - **iso3166-2-api** -->

## Issues or Contributing
Any issues, bugs or enhancements can be raised via the [Issues][issues] tab in the repository. If you would like to contribute any functional/feature changes to the project, please make a Pull Request.

<!-- Also, due to the large amount of data and attributes in the dataset, please raise an Issue if you spot any missing or erroneous data. When raising this Issue please include the current subdivision object attribute values as well as the corrected/new version of them in an easy-to-read format.  -->

## Contact
If you have any questions, comments or suggestions, please contact amckenna41@qub.ac.uk or raise an issue in the [Issues][issues] tab.  <br><br>
<!-- [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/adam-mckenna-7a5b22151/) -->

## Other ISO 3166 repositories
Below are some of my other **custom-built** repositories that relate to the ISO 3166 standard! ⚡

* [iso3166-2-api](https://github.com/amckenna41/iso3166-2-api): frontend RESTful API for iso3166-2.
<!-- * [iso3166-2-export](https://github.com/amckenna41/iso3166-2-export): scripts for full ISO 3166-2 subdivision data export. -->
* [iso3166-updates](https://github.com/amckenna41/iso3166-update): software and accompanying RESTful API that checks for any updates/changes to the ISO 3166-1 and ISO 3166-2 country codes and subdivision naming conventions, as per the ISO 3166 newsletter (https://www.iso.org/iso-3166-country-codes.html) and Online Browsing Platform (OBP) (https://www.iso.org/obp/ui).
* [iso3166-updates-api](https://github.com/amckenna41/iso3166-updates-api): frontend RESTful API for iso3166-updates.
* [iso3166-flags](https://github.com/amckenna41/iso3166-flags): a comprehensive library of over 3500 country and regional flags from the ISO 3166-1 and ISO 3166-2 standards.

## References
\[1\]: https://en.wikipedia.org/wiki/ISO_3166 <br>
\[2\]: https://en.wikipedia.org/wiki/ISO_3166-2 <br>
\[3\]: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2 <br>
\[4\]: https://www.iso.org/obp/ui/#

## Support
[<img src="https://img.shields.io/github/stars/amckenna41/iso3166-2?color=green&label=star%20it%20on%20GitHub" width="132" height="20" alt="Star it on GitHub">](https://github.com/amckenna41/iso3166-2)

<a href="https://www.buymeacoffee.com/amckenna41" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

[Back to top](#TOP)

[python]: https://www.python.org/downloads/release/python-360/
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
[requests]: https://requests.readthedocs.io/
[numpy]: https://numpy.org/
[PyPi]: https://pypi.org/project/iso3166-2/
[iso3166-updates]: https://github.com/amckenna41/iso3166-updates
[demo]: https://colab.research.google.com/drive/1btfEx23bgWdkUPiwdwlDqKkmUp1S-_7U?usp=sharing
[demo_export_iso3166_2]: https://colab.research.google.com/drive/1PXMhpazjsLXVr33RSLZ3w7Tq0RomwPol?usp=sharing
[api]: https://iso3166-2-api.vercel.app/
[api_md]: https://github.com/amckenna41/iso3166-2-api/API.md 
[issues]: https://github.com/amckenna41/iso3166-2/issues
[medium]: https://ajmckenna69.medium.com/iso3166-2-71a13d9157f7
[updates_md]: https://github.com/amckenna41/iso3166-2/blob/main/UPDATES.md