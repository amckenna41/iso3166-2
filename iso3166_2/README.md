<a name="TOP"></a>

# iso3166-2 🌎
[![iso3166_2](https://img.shields.io/pypi/v/iso3166-2)](https://pypi.org/project/iso3166-2/)
[![pytest](https://github.com/amckenna41/iso3166-2/workflows/Building%20and%20Testing/badge.svg)](https://github.com/amckenna41/iso3166-2/actions?query=workflowBuilding%20and%20Testing)
[![status](https://img.shields.io/badge/status-stable-green)](https://github.com/amckenna41/iso3166-2)
<!-- [![CircleCI](https://dl.circleci.com/status-badge/img/gh/amckenna41/iso3166-2/tree/main.svg?style=svg&circle-token=f399bc09886e183a1866efe27808ebecb21a5ea9)](https://dl.circleci.com/status-badge/redirect/gh/amckenna41/iso3166-2/tree/main) -->
[![PythonV](https://img.shields.io/pypi/pyversions/iso3166-2?logo=2)](https://pypi.org/project/iso3166-2/)
[![Platforms](https://img.shields.io/badge/platforms-linux%2C%20macOS%2C%20Windows-green)](https://pypi.org/project/iso3166-2/)
[![Documentation Status](https://readthedocs.org/projects/iso3166-2/badge/?version=latest)](https://iso3166-2.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/github/license/amckenna41/iso3166-2)](https://opensource.org/licenses/MIT)
[![Issues](https://img.shields.io/github/issues/amckenna41/iso3166-2)](https://github.com/amckenna41/iso3166-2/issues)

Documentation
-------------
Documentation for installation and usage of the software is available on the readthedocs platform:

<b>https://iso3166-2.readthedocs.io/en/latest/</b>

Usage
-----
All of the subdivision data and associated attributes are stored within the <i>iso3166-2.json</i> dataset, which is encapsulated via the <i>Subdivisions</i> class. Creating an instance of this class allows you to access each country's subdivision data, alongside a plethora of other useful functions. The instance is subscriptable, allowing the subdivisions to be accessed via their ISO 3166-1 alpha-2, alpha-3 or numeric country codes.

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
iso["604"]['PE-AMA'].parentCode #Amarumayu subdivision parent code
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

**Searching for a specific subdivision via its subdivision name or local/other name attributes:**
```python
'''
The search functionality will search over all subdivisions in the object, 
returning either a subdivision with the exact match or subdivisions whose names 
approximately match the sought input name according to the likeness input parameter.
The likeness input parameter is a % similarity the input search terms have to be to 
the subdivision names, with 100% being an exact match, vice versa. Reducing this
value will thus increase the search space and return more like results.
'''
#searching for the Monaghan county in Ireland (IE-MN) - returning exact matching subdivision (likeness=100)
iso.search("Monaghan")

#searching for Castelo Branco district in Portugal (PT-05) - returning exact matching subdivision (likeness=100)
iso.search("Castelo Branco", likeness=100)

#searching for the Roche Caiman district in Seychelles (SC-25) - returning exact matching subdivision (likeness=100)
iso.search("Roche Caiman")

#searching for any subdivisions that have "Southern" in their name, using a likeness score of 80, include the % match score name is to search terms
iso.search("Southern", likeness_score=80, exclude_match_score=0)

#searching for any subdivisions that have "City" in their name or localOtherName attributes, using a likeness score of 40%
iso.search("City", likeness=40, local_other_name_search=True)

#searching for state of Texas and French Department Meuse - both subdivision objects will be returned, only including the subdivision type and name attributes
iso.search("Texas, Meuse", filter_attributes="name,type") 
```

**Get list of all subdivision codes for one or more countries using alpha code:**
```python
#get list of all subdivision codes - returns a key value pair of country code and subdivision codess: {"AD": [...], "AE": [...], "AF": [...]}
iso.subdivision_codes()

#get list of all subdivision codes for HU, MY & NP
iso.subdivision_codes("HU,MY,NP")

#you can also call the subdivision_codes() function after subscripting a country code
iso["AD"].subdivision_codes()
```

**Get list of all subdivision names for one or more countries using alpha code:**
```python
#create instance of Subdivisions class
iso = Subdivisions()

#get list of all subdivision names - returns a key value pair of country code and subdivision names: {"AD": [...], "AE": [...], "AF": [...]}
iso.subdivision_names()

#get list of all subdivision names for PL, RW & ST
iso.subdivision_names("PL,RW,ST")

#you can also call the subdivision_names() function after subscripting a country code
iso["AL"].subdivision_names()
```

**Adding a custom subdivision to the iso3166-2 object:**
```python
'''
The context for this functionality is similar to that of the user-assigned 
code elements of the ISO 3166-1 standard. Custom subdivisions and subdivision 
codes can be used for in-house/bespoke applications that are using the 
iso3166-2 software but require additional custom subdivisions to be represented.
You can also add custom attributes for the custom subdivision, e.g population,
area, gdp etc, via the custom_attribute parameter.
'''
#adding custom Belfast province to Ireland
iso.custom_subdivision("IE", "IE-BF", name="Belfast", local_other_name="Béal Feirste", type_="province", lat_lng=[54.596, -5.931], parent_code=None, flag=None)

#adding custom Alaska province to Russia with additional population and area attribute values
iso.custom_subdivision("RU", "RU-ASK", name="Alaska Oblast", local_other_name="Аляска", type_="Republic", lat_lng=[63.588, 154.493], parent_code=None, flag=None, 
      custom_attributes={"population": "733,583", "gini": "0.43", "gdpPerCapita": "71,996"})

#adding custom Republic of Molossia state to United States, save to new output file
iso.custom_subdivision("US", "US-ML", name="Republic of Molossia", local_other_name="", type_="State", lat_lng=[39.236, -119.588], parent_code=None, flag="https://upload.wikimedia.org/wikipedia/commons/c/c3/Flag_of_the_Republic_of_Molossia.svg", save_new=1, save_new_filename="us-ml-custom-output.json")

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

[Back to top](#TOP)