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

#adding custom Mariehamn province to Aland Islands (AX)
iso.country.custom_subdivision("AX", "AX-M", name="Mariehamn", local_name="Maarianhamina", type="province", lat_lng=[60.0969, 19.934], parent_code=None, flag_url=None)
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