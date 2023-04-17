# ISO3166-2

[![iso3166_updates](https://img.shields.io/pypi/v/iso3166-2)](https://pypi.org/project/iso3166-2/)
[![Build](https://img.shields.io/github/workflow/status/amckenna41/iso3166-2/Deploy%20to%20PyPI%20📦)](https://github.com/amckenna41/iso3166-2/actions)
[![Platforms](https://img.shields.io/badge/platforms-linux%2C%20macOS%2C%20Windows-green)](https://pypi.org/project/iso3166-2/)
[![License: MIT](https://img.shields.io/github/license/amckenna41/iso3166-2)](https://opensource.org/licenses/MIT)
[![Issues](https://img.shields.io/github/issues/amckenna41/iso3166-2)](https://github.com/amckenna41/iso3166-2/issues)
[![Size](https://img.shields.io/github/repo-size/amckenna41/iso3166-2)](https://github.com/amckenna41/iso3166-2)
[![Commits](https://img.shields.io/github/commit-activity/w/amckenna41/iso3166-2)](https://github.com/iso3166-2)
[![codecov](https://codecov.io/gh/amckenna41/pySAR/branch/master/graph/badge.svg?token=4PQDVGKGYN)](https://codecov.io/gh/amckenna41/pySAR)

<div alt="images" style="justify-content: center; display:flex; margin-left=10px;">
  <img src="https://upload.wikimedia.org/wikipedia/commons/3/3d/Flag-map_of_the_world_%282017%29.png" alt="globe" height="300" width="600"/>
  <!-- <img src="https://upload.wikimedia.org/wikipedia/commons/e/e3/ISO_Logo_%28Red_square%29.svg" alt="iso" height="300" width="400"/> -->
</div>

> Custom-built Python wrapper for RestCountries (https://restcountries.com/) API which includes an abundance of information about all ISO3166 countries. But this package also includes information about all countrys' ISO3166-2 subdivision codes & names, which is absent from RestCountries. Available via a Python software package; a demo is available [colab][here].

Table of Contents
-----------------
  * [Introduction](#introduction)
  * [Requirements](#requirements)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Issues](#Issues)
  * [Contact](#contact)
  * [References](#references)

Introduction
------------
iso3166-2 is a custom-built Python wrapper for RestCountries (https://restcountries.com/) API which includes an abundance of information about all ISO3166 countries. But this package also includes information about all countrys' ISO3166-2 subdivision codes & names, which is absent from RestCountries. The International Organisation for Standards defines codes for the names of countries, dependent territories, special areas of geographical interest, and their principal subdivisions [[1]](#references). This repo focuses on the ISO3166-2 standard.

The ISO 3166-2 defines codes for identifying the principal subdivisions (e.g., provinces, states, municipality etc) of all countries coded in ISO 3166-1. The official name of the standard is "Codes for the representation of names of countries and their subdivisions – Part 2: Country subdivision code." It was first published in 1998 [[2]](#references). As of 29 November 2022 there are 5,043 codes defined in ISO 3166-2. For some countries, codes are defined for more than one level of subdivisions.

Latest Updates
--------------
An important thing to note about the ISO3166-2 and its subdivision codes/names is that changes are made consistently to it, from a small subdivision name change to an addition/deletion of a subdivision. Therefore, it's important that this library and its jsons have the most up to date data. To achieve this, the [iso3166-updates][iso3166-updates] repo was created.

The iso3166-updates repo is another software pacakge and accompanying API that pulls the latest updates and changes for any and all countries in the ISO3166. The API is called every few months to check for any updates, which will then be manually incorporated into this repo. Similarly, the getISO3166_2.py script is called regularly to check for any updates for all country data using the restcountries API. 

Installaion
-----------
Install the latest version of iso3166-2 via [PyPi][PyPi] using pip:

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
Download all ISO3166-2 subdivision data using getISO3166_2.py script, export to two JSONs:
```bash
python3 getISO3166_2.py --json_filename=iso3166_2.json --output_folder=iso3166_2
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

Attributes
----------
You can check the [ATTRIBUTES.md][attributes] file to get a description for each attribute/field in the json exports.

Issues or Contributing
----------------------
Any issues, errors or bugs can be raised via the [Issues](https://github.com/amckenna41/iso3166_updates/issues) tab in the repository. Due to the nature of the ISO consistently updating the ISO3166-2 codes/names every year the data in the JSON's may slightly lag behind these changes. My [iso3166-updates][iso3166-updates] repo was created to check for these updates periodically and implement them in the relevant repo's. 

Contact
-------
If you have any questions or comments, please contact amckenna41@qub.ac.uk or raise an issue on the [Issues][Issues] tab. <br><br>
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/adam-mckenna-7a5b22151/)

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
[PyPi]: https://pypi.org/project/pysar/
[iso3166-updates]: https://github.com/amckenna41/iso3166-updates
[colab]: https://github.com/amckenna41/iso3166-updates
[attributes]: https://github.com/amckenna41/iso3166-2/ATTRIBUTES.md 

<!-- https://github.com/annexare/Countries -->

<!-- 
Look over below...
iso3166-updates is a repo that consists of a series of scripts that check for any updates/changes to the ISO3166-1 and ISO3166-2 country codes and naming conventions, as per the ISO3166 newsletter (https://www.iso.org/iso-3166-country-codes.html). The ISO3166 standard by the ISO defines codes for the names of countries, dependent territories, special areas of geographical interest, consolidated into the ISO3166-1 standard [[1]](#references), and their principal subdivisions (e.g., provinces, states, departments, regions), which compromise the ISO3166-2 standard [[2]](#references). 

**Problem Statement**

The ISO is a very dynamic organisation and regularly change/update/remove entries within its library of standards, this includes the ISO3166. Additions/changes/deletions to country/territorial codes in the ISO3166-1 are a lot less frequent, but changes are much more frequent for the ISO3166-2 codes due to there being thousands more entries, thus it can be difficult to keep up with any changes to these codes. These changes can occur for a variety of geopolitical and bureaucratic reasons and are usually communicated via Newsletters on the ISO platform or Online Browsing Platform or via a database, which usually costs money to subscribe to [[3]](#references), usually being released at the end of the year, with amendments and updates throughout the year. [[4]](#references)

This software and accompanying API makes it extremely easy to check for any new or historic updates to a country or set of countrys' ISO3166-2 codes for free with an easy to use interface and Python package.
This software is for anyone working on projects working directly with country codes and who want up-to-date and accurate ISO3166-2 codes and naming conventions.

**Intended Audience**
This software and accompanying API is for anyone working with country data at the ISO3166 level. It's of high importance that the data that data you are working with is correct and up-to-date, especially with consistent changes being posted every year since 2000 (except 2001 and 2006). iso3166-updates not only 
 
Also, it's aimed not just at developers of ISO3166 applications but for anyone working in that space, hence the creation of an easy to use API. 

<em> The earliest date for any ISO3166 updates is 2000-06-21, and the most recent is 2022-11-29 </em> -->
