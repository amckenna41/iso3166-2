Usage
=====

Below are some usage examples for the various functionalities of the **iso3166-2** software.

.. _installation:

Installation
------------

To use **iso3166-2**, firstly install via ``pip``:

.. code-block:: console

   pip install iso3166-2

Get all subdivision data per country using its ISO 3166-1 alpha codes
---------------------------------------------------------------------
To access all subdivision data for a given country you need to create an instance of the ``ISO3166_2`` class. This instance is subscriptable such that you can get 
the sought country subdivision data via its **ISO 3166-1 2 letter alpha-2, 3 letter alpha-3 or numeric country codes**. You can also search for a specific subdivision
via its subdivision name.

For example, accessing all Canadian (CA, CAN, 124) subdivision data:

.. code-block:: python

   from iso3166_2 import *
   
   #crete instance of ISO3166_2 class
   iso = ISO3166_2()

   iso["CA"] 
   #{'CA-AB': {'name': 'Alberta', 'localName': 'Alberta', 'type': 'Province', 'parentCode': None,...}

   #CA-AB Alberta
   ca_alberta = iso["CA"]["CA-AB"]
   ca_alberta.name #Alberta
   ca_alberta.type #Province
   ca_alberta.flag #https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/CA/CA-AB.svg

   #CA-MB Manitoba
   ca_manitoba = iso["CA"]["CA-MB"]
   ca_manitoba.name #Manitoba
   ca_manitoba.parentCode #null
   ca_manitoba.localName #Manitoba

   #CA-NS Nova Scotia
   ca_nova_scotia = iso["CA"]["CA-NS"]
   ca_nova_scotia.name #Nova Scotia
   ca_nova_scotia.type #Province
   ca_nova_scotia.flag #https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/CA/CA-NS.svg

Accessing all Danish (DK, DNK, 208) subdivision data:

.. code-block:: python

   from iso3166_2 import *
   
   #crete instance of ISO3166_2 class
   iso = ISO3166_2()

   iso["DNK"] 
   #{'DK-81': {'name': 'Nordjylland', 'localName': 'Nordjylland', 'type': 'Region', 'parentCode': None,...}

   #DK-81 Nordjylland
   dk_nordjylland = iso["DNK"]["DK-81"]
   dk_nordjylland.name #Nordjylland
   dk_nordjylland.latLng #[56.831, 9.493]
   dk_nordjylland.type #Region

   #DK-84 Hovedstaden
   dk_hovedstaden = iso["DNK"]["DK-84"]
   dk_hovedstaden.name #Hovedstaden
   dk_hovedstaden.flag #https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/DK/DK-84.svg
   dk_hovedstaden.parentCode #null

   #DK-85 Sjælland
   dk_sjalland = iso["DK"]["DNK-85"]
   dk_sjalland.name #Sjælland
   dk_sjalland.type #Region
   dk_sjalland.flag #https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/DK/DK-85.svg

Accessing all Estonian (EE, EST, 233) subdivision data:

.. code-block:: python

   from iso3166_2 import *
   
   #crete instance of ISO3166_2 class
   iso = ISO3166_2()

   iso["233"]
   #{'EE-37': {'name': 'Harjumaa', 'localName': 'Harjumaa', 'type': 'County', 'parentCode': None,...}

   #EE-39 Hiiumaa
   ee_hiiumaa = iso["233"]["EE-39"]
   ee_hiiumaa.name #Hiiumaa
   ee_hiiumaa.localName #Hiiumaa
   ee_hiiumaa.latLng #[58.924, 22.592]

   #EE-130 Alutaguse
   ee_alutaguse = iso["233"]["EE-130"]
   ee_alutaguse.name #Alutaguse
   ee_alutaguse.parentCode #EE-45
   ee_alutaguse.flag #https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/EE/EE-130.svg

   #EE-338 Kose
   ee_kose = iso["233"]["EE-338"]
   ee_kose.name #Kose
   ee_kose.type #Rural municipality
   ee_kose.parentCode #EE-37

Get all subdivision data for all countries
------------------------------------------

To access ALL subdivision data for all available countries, you need to access the ``all`` attribute within the object instance of the ``ISO3166_2`` class. 
You can then access an individual country's subdivision data by passing in the sought **ISO 3166-1 2 letter alpha-2, 3 letter alpha-3 or numeric country code**.

.. code-block:: python

   from iso3166_2 import *

   #crete instance of ISO3166_2 class
   iso = ISO3166_2()

   all_data = iso.all

   all_data["LU"] #all subdivision data for Luxembourg
   all_data["PW"] #all subdivision data for Palau
   all_data["TUV"] #all subdivision data for Tuvalu
   all_data["UKR"] #all subdivision data for Ukraine
   all_data["876"] #all subdivision data for Wallis & Futuna
   all_data["716"] #all subdivision data for Zimbabwe

Adding custom subdivisions
--------------------------

Add or delete a custom subdivision to an existing country on the main **iso3166-2.json** object. The purpose of this functionality is similar to 
that of the user-assigned code elements of the ISO 3166-1 standard. Custom subdivisions and subdivision codes can be used for in-house/bespoke 
applications that are using the **iso3166-2** software but require additional custom subdivisions to be represented. If the input custom subdivision 
code already exists then an error will be raised, otherwise it will be appended to the object.

If the added subdivision is required to be deleted from the object, then you can call the same function with the alpha-2 and subdivision codes' 
parameters but also setting the ``delete`` parameter to 1/True. This functionality works on the object that the software uses but you can create a copy 
of the object prior to adding/deleting a subdivision via the ``copy`` parameter, setting it to 1/True.

.. code-block:: python

   from iso3166_2 import *

   #adding custom Belfast province to Ireland (IE)
   iso.custom_subdivision("IE", "IE-BF", name="Belfast", local_name="Béal Feirste", type_="province", lat_lng=[54.596, -5.931], parent_code=None, flag=None, copy=1)

   #adding custom Mariehamn province to Aland Islands (AX)
   iso.custom_subdivision("AX", "AX-M", name="Mariehamn", local_name="Maarianhamina", type_="province", lat_lng=[60.0969, 19.934], parent_code=None, flag=None, copy=1)

   #deleting above custom subdivisions from object
   iso.custom_subdivision("IE", "IE-BF", delete=1)
   iso.custom_subdivision("AX", "AX-M", delete=1)

.. warning::
    When adding a custom subdivision the software will be out of sync with the official ISO 3166-2 dataset, therefore its important to keep track
    of the custom subdivisions you add to the object. 
    
    To return to the original dataset you can delete the added custom subdivision, as described above, or you could reinstall the software. 

Searching for a subdivision
---------------------------
The ``search()`` function allows you to search for a specific subdivision via its subdivision name. The
search functionality uses a fuzzy search algorithm via *thefuzz* package, searching for subdivisions with
an exact name match or those with an approximate name match, according to a score via the *likeness* input
parameter. 

.. code-block:: python

   from iso3166_2 import *

   #searching for the Monaghan county in Ireland (IE-MN) - returning exact matching subdivision
   iso.search("Monaghan")

   #searching for any subdivisions that have "Southern" in their name, using a likeness score of 0.7
   iso.search("Southern", likeness=0.7)

   #searching for any subdivisions that have "City" in their name, using a likeness score of 0.4
   iso.search("City", likeness=0.4)

   #searching for state of Texas and French Department Meuse - both subdivision objects will be returned
   iso.search("Texas, Meuse") 

.. note::
    A demo of the software and API is available |demo_link|.

.. |demo_link| raw:: html

   <a href="https://colab.research.google.com/drive/1btfEx23bgWdkUPiwdwlDqKkmUp1S-_7U?usp=sharing" target="_blank">here</a>