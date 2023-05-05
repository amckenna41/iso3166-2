# iso3166-2
[![iso3166_2](https://img.shields.io/pypi/v/iso3166-2)](https://pypi.org/project/iso3166-2/)
[![pytest](https://github.com/amckenna41/iso3166-2/workflows/Building%20and%20Testing/badge.svg)](https://github.com/amckenna41/iso3166-2/actions?query=workflowBuilding%20and%20Testing)
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/amckenna41/iso3166-2/tree/main.svg?style=svg&circle-token=f399bc09886e183a1866efe27808ebecb21a5ea9)](https://dl.circleci.com/status-badge/redirect/gh/amckenna41/iso3166-2/tree/main)
[![Platforms](https://img.shields.io/badge/platforms-linux%2C%20macOS%2C%20Windows-green)](https://pypi.org/project/iso3166-2/)
[![License: MIT](https://img.shields.io/github/license/amckenna41/iso3166-2)](https://opensource.org/licenses/MIT)
[![Issues](https://img.shields.io/github/issues/amckenna41/iso3166-2)](https://github.com/amckenna41/iso3166-2/issues)
<!-- [![Size](https://img.shields.io/github/repo-size/amckenna41/iso3166-2)](https://github.com/amckenna41/iso3166-2) -->
<!-- [![Commits](https://img.shields.io/github/commit-activity/w/amckenna41/iso3166-2)](https://github.com/iso3166-2) -->
<!-- [![codecov](https://codecov.io/gh/amckenna41/pySAR/branch/master/graph/badge.svg?token=4PQDVGKGYN)](https://codecov.io/gh/amckenna41/pySAR) -->

Usage
-----
There are two main JSONs that `iso3166-2` utilises, <i>iso3166-2.json</i> and <i>iso3166-2-min.json</i>. The first JSON contains all country information, including all data pulled from the restcountries API as well as the country's subdivision data, this file is <b>3.4 MB</b>. The <i>iso3166-2-min.json</i> file is a minimised version of the first JSON, only containing each country's ISO3166-2 subdivision data, this file is <b>1.6 MB</b>. In the main module <i>iso3166_2.py</i>, all data from the <i>iso3166-2.json</i> is accessible via the `iso.country` object and all data from the <i>iso3166-2-min.json</i> is accessible via the `iso.subdivisions` object.

The script `getISO3166_2.py` is used for gathering and exporting all country and subdivision data to the mentioned JSONs. It uses the [restcountries api][rest] as well as the [pycountry][pycountry] and [googlemaps][googlemaps] packages to gather and export all the required info. To download all of the latest ISO 3166-2 subdivision data, run the `getISO3166_2.py` in a terminal or cmd below; (the script takes around 2 hours to execute):
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