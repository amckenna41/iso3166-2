# iso3166-2

[![iso3166_2](https://img.shields.io/pypi/v/iso3166-2)](https://pypi.org/project/iso3166-2/)
[![Build](https://img.shields.io/github/workflow/status/amckenna41/iso3166-updates/Deploy%20to%20PyPI%20📦)](https://github.com/amckenna41/iso3166-2/actions)
[![Platforms](https://img.shields.io/badge/platforms-linux%2C%20macOS%2C%20Windows-green)](https://pypi.org/project/iso3166-2/)
[![License: MIT](https://img.shields.io/github/license/amckenna41/iso3166-2)](https://opensource.org/licenses/MIT)

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