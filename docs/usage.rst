Usage
=====

Below are some usage examples for the various functionalities of the **iso3166-2** software.

.. _installation:

Installation
------------

To use **iso3166-2**, firstly install via ``pip``:

.. code-block:: console

   pip install iso3166-2

Get all subdivision data for all countries
------------------------------------------
Get ALL the subdivision data for ALL available countries, by accessing the ``all`` attribute within the object instance of the ``Subdivisions`` class. 
You can then access an individual country's subdivision data by passing in the sought **ISO 3166-1 2 letter alpha-2, 3 letter alpha-3 or numeric country code**.

.. code-block:: python

   from iso3166_2 import *

   #crete instance of Subdivisions class
   iso = Subdivisions()

   all_data = iso.all

   all_data["LU"] #all subdivision data for Luxembourg
   all_data["PW"] #all subdivision data for Palau
   all_data["TUV"] #all subdivision data for Tuvalu
   all_data["UKR"] #all subdivision data for Ukraine
   all_data["876"] #all subdivision data for Wallis & Futuna
   all_data["716"] #all subdivision data for Zimbabwe

Get all subdivision data for a country using its ISO 3166-1 alpha codes
-----------------------------------------------------------------------
Get all subdivision data for a given country by creating an instance of the ``Subdivisions`` class. This instance is subscriptable such that you can get 
the sought country subdivision data via its **ISO 3166-1 2 letter alpha-2, 3 letter alpha-3 or numeric country codes**. You can then get the individual
subdivision attributes via dot notation.

For example, accessing all Canadian (CA, CAN, 124) subdivision data:

.. code-block:: python

   from iso3166_2 import *
   
   #crete instance of Subdivisions class
   iso = Subdivisions()

   iso["CA"] 
   #{'CA-AB': {'name': 'Alberta', 'localOtherName': 'Alberta', 'type': 'Province', 'parentCode': None,...}

   #CA-AB Alberta
   ca_alberta = iso["CA"]["CA-AB"]
   ca_alberta.name #Alberta
   ca_alberta.type #Province
   ca_alberta.flag #https://raw.githubusercontent.com/amckenna41/iso3166-flag-icons/main/iso3166-2-icons/CA/CA-AB.svg

   #CA-MB Manitoba
   ca_manitoba = iso["CA"]["CA-MB"]
   ca_manitoba.name #Manitoba
   ca_manitoba.parentCode #null
   ca_manitoba.localOtherName #Manitoba

   #CA-NS Nova Scotia
   ca_nova_scotia = iso["CA"]["CA-NS"]
   ca_nova_scotia.name #Nova Scotia
   ca_nova_scotia.flag #https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/CA/CA-NS.svg
   ca_nova_scotia.history #None

Accessing all Danish (DK, DNK, 208) subdivision data:

.. code-block:: python

   iso["DNK"] 
   #{'DK-81': {'name': 'Nordjylland', 'localOtherName': 'Nordjylland', 'type': 'Region', 'parentCode': None,...}

   #DK-81 Nordjylland
   dk_nordjylland = iso["DNK"]["DK-81"]
   dk_nordjylland.name #Nordjylland
   dk_nordjylland.latLng #[56.831, 9.493]
   dk_nordjylland.type #Region

   #DK-84 Hovedstaden
   dk_hovedstaden = iso["DNK"]["DK-84"]
   dk_hovedstaden.name #Hovedstaden
   dk_hovedstaden.flag #https://raw.githubusercontent.com/amckenna41/iso3166-flag-icons/main/iso3166-2-icons/DK/DK-84.svg
   dk_hovedstaden.parentCode #null

   #DK-85 Sjælland
   dk_sjalland = iso["DK"]["DNK-85"]
   dk_sjalland.name #Sjælland
   dk_sjalland.type #Region
   dk_sjalland.flag #https://raw.githubusercontent.com/amckenna41/iso3166-flag-icons/main/iso3166-2-icons/DK/DK-85.svg

Accessing all Estonian (EE, EST, 233) subdivision data:

.. code-block:: python

   iso["233"]
   #{'EE-37': {'name': 'Harjumaa', 'localOtherName': 'Harjumaa', 'type': 'County', 'parentCode': None,...}

   #EE-39 Hiiumaa
   ee_hiiumaa = iso["233"]["EE-39"]
   ee_hiiumaa.name #Hiiumaa
   ee_hiiumaa.localOtherName #Hiiumaa
   ee_hiiumaa.latLng #[58.924, 22.592]

   #EE-130 Alutaguse
   ee_alutaguse = iso["233"]["EE-130"]
   ee_alutaguse.name #Alutaguse
   ee_alutaguse.parentCode #EE-45
   ee_alutaguse.flag #https://raw.githubusercontent.com/amckenna41/iso3166-flag-icons/main/iso3166-2-icons/EE/EE-130.svg

   #EE-338 Kose
   ee_kose = iso["233"]["EE-338"]
   ee_kose.name #Kose
   ee_kose.type #Rural municipality
   ee_kose.parentCode #EE-37


Get list of all subdivision codes
---------------------------------
Get the full list of subdivision codes for all countries or a subset of countries using their alpha codes. This 
is useful if you just need the list of supported subdivision codes and not their corresponding subdivision data.

Extract all subdivision codes for all countries:

.. code-block:: python

   from iso3166_2 import *
   
   #crete instance of Subdivisions class
   iso = Subdivisions()

   iso.subdivision_codes()

Extract all subdivision codes for Nigeria (NG, NGA, 566):

.. code-block:: python

   iso.subdivision_codes("NG")

Extract all subdivision codes for Saudi Arabia (SA, SAU, 682):

.. code-block:: python

   iso.subdivision_codes("SAU")

Extract all subdivision codes for Singapore (SG, SGP, 702), Somalia (SO, SOM, 706) and Togo (TG, TGO, 768):

.. code-block:: python

   iso.subdivision_codes("SG, SOM, 768")


Get list of all subdivision names
---------------------------------
Get the full list of subdivision names for all countries or a subset of countries using their alpha codes. This 
is useful if you just need the list of supported subdivision names and not their corresponding subdivision data.

Extract all subdivision names for all countries:

.. code-block:: python

   from iso3166_2 import *
   
   #crete instance of Subdivisions class
   iso = Subdivisions()

   iso.subdivision_names()

Extract all subdivision names for Cuba (CU, CUB, 192):

.. code-block:: python

   iso.subdivision_names("CU")

Extract all subdivision names for France (FR, FRA, 250):

.. code-block:: python

   iso.subdivision_names("FRA")

Extract all subdivision names for Georgia (GE, GEO, 268), Guinea (GN, GIN, 324) and Kenya (KE, KEN, 404):

.. code-block:: python

   iso.subdivision_names("GE, GIN, 404")


Searching for a subdivision
---------------------------
The ``search()`` function allows you to search for a specific subdivision via its subdivision name. The
search functionality uses a fuzzy search algorithm via *thefuzz* package, searching for subdivisions with
an exact name match or those with an approximate name match, according to a score via the *likeness* input
parameter. The *likeness* parameter accepts a value between 1 and 100, with 100 being an exact match and 
the values representing a percentage likeness that the subdivision name have to be to the input search terms. 
By default, the output will be sorted via the Match Score attribute which is the % likeness the subdivision
name is to the input search terms. To exclude this Match Score attribute, set the *excludeMatchScore*
attribute to False. By default the search functionality only uses the *name* data attribute 
but the search space can be expanded and use the *localOtherName* attribute in addition via the 
*local_other_name_search* parameter. A subset of sought data attributes can be returned from the search 
results via the *filter_attributes* parameter. 

.. code-block:: python

   from iso3166_2 import *

   #crete instance of Subdivisions class
   iso = Subdivisions()

   #searching for the Monaghan county in Ireland (IE-MN) - returning exact matching subdivision (likeness=100)
   iso.search("Monaghan")

   #searching for Castelo Branco district in Portugal (PT-05) - returning exact matching subdivision (likeness=100)
   iso.search("Castelo Branco")

   #searching for the Roche Caiman district in Seychelles (SC-25) - returning exact matching subdivision (likeness=100)
   iso.search("Roche Caiman")

   #searching for any subdivisions that have "Southern" in their name, using a likeness score of 70, exclude Match Score attribute
   iso.search("Southern", likeness=70, exclude_match_score=1)

   #searching for any subdivisions that have "City" in their name or localOtherName attributes, using a likeness score of 40
   iso.search("City", likeness=40, local_other_name_search=True)

   #searching for state of Texas and French Department Meuse - both subdivision objects will be returned, only including the subdivision type and name attributes
   iso.search("Texas, Meuse", filter_attributes="name,type") 

Adding custom subdivisions
--------------------------
Add or delete a custom subdivision to an existing country on the main **iso3166-2.json** object. The purpose of this functionality is similar to 
that of the user-assigned code elements of the ISO 3166-1 standard. Custom subdivisions and subdivision codes can be used for in-house/bespoke 
applications that are using the **iso3166-2** software but require additional custom subdivisions to be represented. If the input custom subdivision 
code already exists then an error will be raised, otherwise it will be appended to the object. If the input subdivision code already exists then
any differing attribute values you input will be used to amend the existing subdivision data.

If the added subdivision is required to be deleted from the object, then you can call the same function with the alpha-2 and subdivision codes' 
parameters but also setting the ``delete`` parameter to 1/True. This functionality works on the object that the software uses but you can create a copy 
of the object prior to adding/deleting a subdivision via the ``copy`` parameter, setting it to 1/True. Furthermore, you can also save the updated 
subdivision object to a new object via the ``save_new`` and ``save_new_filename`` parameters. 

You can also add custom attributes to the subdivision via the ``custom_attributes`` parameter, e.g the population, area, gdp per capita etc.

.. code-block:: python

   from iso3166_2 import *

   #crete instance of Subdivisions class
   iso = Subdivisions()
   
   #adding custom Belfast province to Ireland (IE)
   iso.custom_subdivision("IE", "IE-BF", name="Belfast", local_other_name="Béal Feirste", type_="province", lat_lng=[54.596, -5.931], parent_code=None, flag=None, history=None, copy=1)

   #adding custom Mariehamn province to Aland Islands (AX), export to new file
   iso.custom_subdivision("AX", "AX-M", name="Mariehamn", local_other_name="Maarianhamina", type_="province", lat_lng=[60.0969, 19.934], parent_code=None, flag=None, history=None, copy=1,
      save_new=1, save_new_filename="iso3166-2-AX-M.json")

   #adding custom Alaska province to Russia with additional population and area attribute values
   iso.custom_subdivision("RU", "RU-ASK", name="Alaska Oblast", local_other_name="Аляска", type_="Republic", lat_lng=[63.588, 154.493], parent_code=None, flag=None, 
      custom_attributes={"population": "733,583", "gini": "0.43", "gdpPerCapita": "71,996"})

   #deleting above custom subdivisions from object
   iso.custom_subdivision("IE", "IE-BF", delete=1)
   iso.custom_subdivision("AX", "AX-M", delete=1)
   iso.custom_subdivision("RU", "RU-ASK", delete=1)

.. warning::
    When adding a custom subdivision the software will be out of sync with the official ISO 3166-2 dataset, therefore its important to keep track
    of the custom subdivisions you add to the object.
    
    To return to the original dataset you can delete the added custom subdivision, as described above, or you could reinstall the software.


Get all subdivision data but with subset of available attributes
----------------------------------------------------------------
To access all subdivision data but only requiring a subset of the available default attributes, you need to create an instance of the ``Subdivisions`` class,
passing in a comma separated list of attributes to include in the output via the ``filter_attributes`` input parameter. 

.. code-block:: python

   from iso3166_2 import *

   #crete instance of Subdivisions class, filtering out all attributes but flag and type from subdivisions
   iso = Subdivisions(filter_attributes="flag,type")

   #crete instance of Subdivisions class, filtering out all attributes but name from subdivisions
   iso = Subdivisions(filter_attributes="name")

   #crete instance of Subdivisions class, filtering out all attributes but name,localOtherName,parentCode,type,flag,latLng from subdivisions
   iso = Subdivisions(filter_attributes="name,localOtherName,parentCode,type,flag,latLng")


Get the total number of subdivision objects
-------------------------------------------
Get the total number of individual ISO 3166-2 subdivision objects within the main JSON of the class, via the in-built ``len()`` function.

.. code-block:: python

   from iso3166_2 import *

   #create instance of Subdivisions class
   iso = Subdivisions()

   #get total number of subdivision objects via len()
   len(iso)


Check for the latest Subdivision data
------------------------------------
Pull the latest subdivision data object from the `iso3166-2` GitHub repo and compare data with that of the object currently installed. If
any changes are found then they will be output & it is advised that you upgrade or reinstall the software package to keep your data in sync
with that of the latest version. 

.. code-block:: python

   from iso3166_2 import *

   #create instance of Subdivisions class
   iso = Subdivisions()

   #compare latest subdivision data from repo
   iso.check_for_updates()


.. note::
    A demo of the software and API is available |demo_link|.

.. |demo_link| raw:: html

   <a href="https://colab.research.google.com/drive/1btfEx23bgWdkUPiwdwlDqKkmUp1S-_7U?usp=sharing" target="_blank">here</a>
