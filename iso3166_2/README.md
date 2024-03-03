# iso3166-2 🌎
[![iso3166_2](https://img.shields.io/pypi/v/iso3166-2)](https://pypi.org/project/iso3166-2/)
[![pytest](https://github.com/amckenna41/iso3166-2/workflows/Building%20and%20Testing/badge.svg)](https://github.com/amckenna41/iso3166-2/actions?query=workflowBuilding%20and%20Testing)
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/amckenna41/iso3166-2/tree/main.svg?style=svg&circle-token=f399bc09886e183a1866efe27808ebecb21a5ea9)](https://dl.circleci.com/status-badge/redirect/gh/amckenna41/iso3166-2/tree/main)
[![PythonV](https://img.shields.io/pypi/pyversions/iso3166-2?logo=2)](https://pypi.org/project/iso3166-2/)
[![Platforms](https://img.shields.io/badge/platforms-linux%2C%20macOS%2C%20Windows-green)](https://pypi.org/project/iso3166-2/)
[![Documentation Status](https://readthedocs.org/projects/iso3166-2/badge/?version=latest)](https://iso3166-2.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/github/license/amckenna41/iso3166-2)](https://opensource.org/licenses/MIT)
[![Issues](https://img.shields.io/github/issues/amckenna41/iso3166-2)](https://github.com/amckenna41/iso3166-2/issues)

Documentation
-------------
Documentation for installation and usage of the software is availble on the readthedocs platform:

<b>https://iso3166-2.readthedocs.io/en/latest/</b>

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