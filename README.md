# ISO3166-2

[![iso3166_2](https://img.shields.io/pypi/v/iso3166-2)](https://pypi.org/project/iso3166-2/)
[![pytest](https://github.com/amckenna41/iso3166-2/workflows/Building%20and%20Testing%20%F0%9F%90%8D/badge.svg)](https://github.com/amckenna41/iso3166-2/actions?query=workflowBuilding%20and%20Testing%20%F0%9F%90%8D)
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

> Custom-built Python wrapper for RestCountries API (https://restcountries.com/) which includes an abundance of information about all ISO3166 countries. But this package also includes information about all countrys' ISO 3166-2 subdivision codes & names, which is absent from RestCountries. Available via a Python software package; a demo is available [here][demo].

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
`iso3166-2` is a custom-built Python wrapper for the RestCountries (https://restcountries.com/) API which includes an abundance of information about all ISO3166 countries. But this package also includes information about all countrys' ISO 3166-2 subdivision codes & names, which is absent from RestCountries. The International Organisation for Standards defines codes for the names of countries, dependent territories, special areas of geographical interest, and their principal subdivisions [[1]](#references). This repo focuses on the ISO 3166-2 standard.

The ISO 3166-2 defines codes for identifying the principal subdivisions (e.g., provinces, states, municipality etc) of all countries coded in ISO 3166-1. The official name of the standard is "Codes for the representation of names of countries and their subdivisions – Part 2: Country subdivision code." It was first published in 1998 [[2]](#references). As of 29 November 2022 there are 5,043 codes defined in ISO 3166-2. For some countries, codes are defined for more than one level of subdivisions.

The full list of attributes/fields available in `iso3166-2` can be viewed in the [ATTRIBUTES.md][attributes] file.

Latest Updates
--------------
An important thing to note about the ISO 3166-2 and its subdivision codes/names is that changes are made consistently to it, from a small subdivision name change to an addition/deletion of a whole subdivision. Therefore, it's important that this library and its JSONs have the most up to date data. To achieve this, the [iso3166-updates][iso3166-updates] repo was created.

The <b>iso3166-updates</b> repo is another software package and accompanying API that pulls the latest updates and changes for any and all countries in the ISO3166. The API is called every few months to check for any updates, which will then be manually incorporated into this repo. Similarly, the <i>getISO3166_2.py</i> script is called regularly to check for any updates for all country data using the restcountries API. 

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
* [python][python] >= 3.7
* [requests][requests] >= 2.28.1
* [iso3166][iso3166] >= 2.1.1

Usage
-----
There are two main JSONs that `iso3166-2` utilises, <i>iso3166-2.json</i> and <i>iso3166-2-min.json</i>. The first JSON contains all country information, including all data pulled from the restcountries API as well as the country's subdivision data, this file is <b>3.4 MB</b>. The <i>iso3166-2-min.json</i> file is a minimised version of the first JSON, only containing each country's ISO3166-2 subdivision data, this file is <b>1.6 MB</b>. In the main module <i>iso3166_2.py</i>, all data from the <i>iso3166-2.json</i> is accessible via the `iso.country` object and all data from the <i>iso3166-2-min.json</i> is accessible via the `iso.subdivisions` object.

The script `getISO3166_2.py` is used for gathering and exporting all country and subdivision data to the mentioned JSONs. It uses the restcountries api and pycountry package to assemble all of the data together. To download all of the latest ISO 3166-2 subdivision data, run the `getISO3166_2.py` in a terminal or cmd below; (the script takes around 2 hours to execute):
```
python3 getISO3166_2.py --json_filename=iso3166_2.json --output_folder=iso3166_2

--json_filename: output filename for exported JSONs.
--output_folder: output folder to store JSONs.
```

Import ISO3166_2 class and access the country and subdivision data:
```python
import iso3166_2 as iso

#access all country data
canada_iso3166_2 = iso.country["CA"]
denmark_iso3166_2 = iso.country["DK"]
estonia_iso3166_2 = iso.country["EE"]
fiji_iso3166_2 = iso.country["FJ"]

#access all country subdivision data
canada_iso3166_2 = iso.subdivisions["CA"]
denmark_iso3166_2 = iso.subdivisions["DK"]
estonia_iso3166_2 = iso.subdivisions["EE"]
fiji_iso3166_2 = iso.subdivisions["FJ"]
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

Issues or Contributing
----------------------
Any issues, errors or bugs can be raised via the [Issues][issues] tab in the repository. Due to the nature of the ISO consistently updating the ISO 3166-2 codes/names every year, the data in the JSONs may slightly lag behind these changes. My [iso3166-updates][iso3166-updates] repo was created to check for these updates periodically and implement them in the relevant repo's. Although, if you notice any out of date or missing subdivision info then please similarly raise an Issue in the [Issues][issues] tab.

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
[google-maps-api]: https://github.com/googlemaps/google-maps-services-python
[PyPi]: https://pypi.org/project/iso3166-2/
[iso3166-updates]: https://github.com/amckenna41/iso3166-updates
[demo]: https://colab.research.google.com/drive/1btfEx23bgWdkUPiwdwlDqKkmUp1S-_7U?usp=sharing
[attributes]: https://github.com/amckenna41/iso3166-2/ATTRIBUTES.md 
[issues]: https://github.com/amckenna41/iso3166-2/issues