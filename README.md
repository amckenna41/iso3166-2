# ISO3166-2

[![iso3166_2](https://img.shields.io/pypi/v/iso3166-2)](https://pypi.org/project/iso3166-2/)
[![pytest](https://github.com/amckenna41/iso3166-2/workflows/Building%20and%20Testing/badge.svg)](https://github.com/amckenna41/iso3166-2/actions?query=workflowBuilding%20and%20Testing)
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/amckenna41/iso3166-2/tree/main.svg?style=svg&circle-token=f399bc09886e183a1866efe27808ebecb21a5ea9)](https://dl.circleci.com/status-badge/redirect/gh/amckenna41/iso3166-2/tree/main)
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

> iso3166-2 is a lightweight custom-built Python wrapper, and accompanying API, for the RestCountries API (https://restcountries.com/) which includes an abundance of information about all ISO 3166 countries/territories. But this package also includes information about all countrys' ISO 3166-2 subdivision codes & names, which is absent from RestCountries. Currently, the package and API supports data from 250 countries/territories, according to the ISO 3166-1. Available via a Python software package or an API; a demo of both is available [here][demo].

Table of Contents
-----------------
  * [Introduction](#introduction)
  * [Requirements](#requirements)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Issues](#issuesorcontributing)
  * [Contact](#contact)
  * [References](#references)

Introduction
------------
`iso3166-2` is a custom-built Python wrapper for the RestCountries (https://restcountries.com/) API which includes an abundance of information about all ISO3166 countries/territories. But this package also includes information about all countrys' ISO 3166-2 subdivision codes & names, which is absent from RestCountries. The International Organisation for Standards defines codes for the names of countries, dependent territories, special areas of geographical interest, and their principal subdivisions [[1]](#references). This repo focuses on the ISO 3166-2 standard.

The ISO 3166-2 defines codes for identifying the principal subdivisions (e.g., provinces, states, municipality etc) of all countries coded in ISO 3166-1. The official name of the standard is "Codes for the representation of names of countries and their subdivisions – Part 2: Country subdivision code." It was first published in 1998 [[2]](#references). As of 29 November 2022 there are 5,043 codes defined in ISO 3166-2. For some countries, codes are defined for more than one level of subdivisions.

The full list of attributes/fields available in `iso3166-2` can be viewed in the [ATTRIBUTES.md][attributes] file.

Currently, this package and accompanying API supports data from 250 countries/territories, as listed in the ISO 3166-1.

Latest Updates
--------------
An important thing to note about the ISO 3166-2 and its subdivision codes/names is that changes are made consistently to it, from a small subdivision name change to an addition/deletion of a whole subdivision; these changes can happen due to a variety of geopolitical reasons. Therefore, it's important that this library and its JSONs have the most up-to-date data. To achieve this, the [iso3166-updates][iso3166-updates] repo was created.

The [iso3166-updates][iso3166-updates] repo is another open-source software package and accompanying API that pulls the latest updates and changes for any and all countries in the ISO 3166 from a variety of data sources including the ISO website itself. The API is called every few months to check for any updates, which are communicated and will then be manually incorporated into this repo. Please visit the repository home page for more info about the purpose and process of the software ([iso3166-updates][iso3166-updates]).

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

Requirements
------------
* [python][python] >= 3.8
* [requests][requests] >= 2.28.1
* [iso3166][iso3166] >= 2.1.1

Requirements (getISO3166_2.py)
------------------------------
* [python][python] >= 3.8
* [requests][requests] >= 2.28.1
* [iso3166][iso3166] >= 2.1.1
* [pycountry][pycountry] >= 22.3.5
* [googlemaps][googlemaps] >= 4.10.0
* [tqdm][tqdm] >= 4.64.0
* [natsort][natsort] >= 8.4.0

Usage
-----
There are two main JSONs that `iso3166-2` utilises, <i>iso3166-2.json</i> and <i>iso3166-2-min.json</i>. The first JSON contains all country information, including all data pulled from the restcountries API as well as the country's subdivision data, this file is <b>X MB</b>. The <i>iso3166-2-min.json</i> file is a minimised version of the first JSON, only containing each country's ISO3166-2 subdivision data, this file is <b>1.6 MB</b>. In the main module <i>iso3166_2.py</i>, all data from the <i>iso3166-2.json</i> is accessible via the `iso.country` object and all data from the <i>iso3166-2-min.json</i> is accessible via the `iso.subdivisions` object.

Import ISO3166_2 class and access the country and subdivision data:
```python
import iso3166_2 as iso

#access all country data
canada_iso3166_2 = iso.country["CA"]
denmark_iso3166_2 = iso.country["DK"]
estonia_iso3166_2 = iso.country["EE"]
fiji_haiti_guyana_iso3166_2 = iso.country["FJ, HT, GY"]

#access all country subdivision data
canada_iso3166_2 = iso.subdivisions["CA"]
denmark_iso3166_2 = iso.subdivisions["DK"]
estonia_iso3166_2 = iso.subdivisions["EE"]
fiji_haiti_guyana_iso3166_2 = iso.subdivisions["FJ, HT, GY"]
```

Get country data:
```python
import iso3166_2 as iso

canada_iso3166_2.name #country name
denmark_iso3166_2.currencies #country currencies
estonia_iso3166_2.capital #country capital 
fiji_iso3166_2.population #country population 
```

Get a specific subdivision's info:
```python
import iso3166_2 as iso

canada_iso3166_2.subdivisions['CA-AB'] #Alberta subdivision
denmark_iso3166_2.subdivisions['DK-81'] #Nordjylland subdivision
estonia_iso3166_2.subdivisions['EE-899'] #Viljandi subdivision
fiji_iso3166_2.subdivisions['FJ-03'] #Cakaudrove subdivision 
```

Usage (getISO3166_2.py)
-----------------------
The script `getISO3166_2.py` is used for gathering and exporting all country and subdivision data to the mentioned JSONs. It uses the [restcountries api][rest] as well as the [pycountry][pycountry] and [googlemaps][googlemaps] packages to gather and export all the required info. Calling the script using its default parameters will gather all the data for all countries, but the <i>alpha2_codes</i> parameter can be set to pull the updates for a specific list of one or more countries (the alpha-3 code can also be input, which is then converted into its 2 letter alpha-2 counterpart).

To download all of the latest ISO 3166-2 subdivision data for all countries, run the `getISO3166_2.py` in a terminal or cmd below; (the script takes around 2 hours to execute):

```bash
python3 getISO3166_2.py --json_filename=iso3166_2.json --output_folder=iso3166_2

--alpha2_codes: list of 1 or more 2 letter alpha-2 country codes.
--json_filename: output filename for exported JSONs.
--output_folder: output folder to store JSONs.
```

To download all of the latest ISO 3166-2 subdivision data for Germany, Portugal and Spain:
```bash
python3 getISO3166_2.py --alpha2_codes=DE,PT,ES
```

Issues or Contributing
----------------------
Any issues, errors, bugs or missing data can be raised via the [Issues][issues] tab in the repository.

Contact
-------
If you have any questions or comments, please contact amckenna41@qub.ac.uk or raise an issue in the [Issues][issues] tab.  <br><br>
<!-- [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/adam-mckenna-7a5b22151/) -->

References
----------
\[1\]: https://en.wikipedia.org/wiki/ISO_3166 <br>
\[2\]: https://en.wikipedia.org/wiki/ISO_3166-2 <br>

Support
-------
<a href="https://www.buymeacoffee.com/amckenna41" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

[Back to top](#TOP)

[python]: https://www.python.org/downloads/release/python-360/
[requests]: https://requests.readthedocs.io/
[iso3166]: https://github.com/deactivated/python-iso3166
[pycountry]: https://github.com/flyingcircusio/pycountry
[rest]: https://restcountries.com/
[google]: https://github.com/googlemaps/google-maps-services-python
[PyPi]: https://pypi.org/project/iso3166-2/
[iso3166-updates]: https://github.com/amckenna41/iso3166-updates
[demo]: https://colab.research.google.com/drive/1btfEx23bgWdkUPiwdwlDqKkmUp1S-_7U?usp=sharing
[attributes]: https://github.com/amckenna41/iso3166-2/ATTRIBUTES.md 
[issues]: https://github.com/amckenna41/iso3166-2/issues