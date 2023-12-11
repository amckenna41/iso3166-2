# iso3166-2 🌎
[![iso3166_2](https://img.shields.io/pypi/v/iso3166-2)](https://pypi.org/project/iso3166-2/)
[![pytest](https://github.com/amckenna41/iso3166-2/workflows/Building%20and%20Testing/badge.svg)](https://github.com/amckenna41/iso3166-2/actions?query=workflowBuilding%20and%20Testing)
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/amckenna41/iso3166-2/tree/main.svg?style=svg&circle-token=f399bc09886e183a1866efe27808ebecb21a5ea9)](https://dl.circleci.com/status-badge/redirect/gh/amckenna41/iso3166-2/tree/main)
[![PythonV](https://img.shields.io/pypi/pyversions/iso3166-2?logo=2)](https://pypi.org/project/iso3166-2/)
[![Platforms](https://img.shields.io/badge/platforms-linux%2C%20macOS%2C%20Windows-green)](https://pypi.org/project/iso3166-2/)
[![License: MIT](https://img.shields.io/github/license/amckenna41/iso3166-2)](https://opensource.org/licenses/MIT)
[![Issues](https://img.shields.io/github/issues/amckenna41/iso3166-2)](https://github.com/amckenna41/iso3166-2/issues)

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