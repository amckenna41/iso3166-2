Usage
=====

.. _installation:

Installation
------------

To use **iso3166-2**, firstly install via ``pip``:

.. code-block:: console

   pip install iso3166-2

Alternatively, you can clone the repo and run ``setup.py``:

.. code-block:: console

   git clone -b master https://github.com/amckenna41/iso3166-2.git
   cd iso3166_2
   python3 setup.py install

Accessing subdivision data per country
--------------------------------------
To access all subdivision data for a given country you need to access the ``country`` object instance of the ``ISO3166_2`` class, 
and then passing in the sought 2 letter alpha-2 or 3 letter alpha-3 country code. You can then access a specific subdivision's 
data by passing in the subdivision's ISO 3166-2 code.

For example, accessing all Canadian (CA) subdivision data:

.. code-block:: python

   import iso3166_2 as iso
   
   iso.country["CA"] 
   #{'CA-AB': {'name': 'Alberta', 'localName': 'Alberta', 'type': 'Province', 'parentCode': None,...}

   #CA-AB Alberta
   ca_alberta = iso.country["CA"]["CA-AB"]
   ca_alberta.name #Alberta
   ca_alberta.type #Province
   ca_alberta.flag_url #https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/CA/CA-AB.svg

   #CA-MB Manitoba
   ca_manitoba = iso.country["CA"]["CA-MB"]
   ca_manitoba.name #Manitoba
   ca_manitoba.parentCode #null
   ca_manitoba.localName #Manitoba

   #CA-NS Nova Scotia
   ca_nova_scotia = iso.country["CA"]["CA-NS"]
   ca_nova_scotia.name #Nova Scotia
   ca_nova_scotia.type #Province
   ca_nova_scotia.flagUrl #https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/CA/CA-NS.svg

Accessing all Danish (DK) subdivision data:

.. code-block:: python

   import iso3166_2 as iso

   iso.country["DK"] 
   #{'DK-81': {'name': 'Nordjylland', 'localName': 'Nordjylland', 'type': 'Region', 'parentCode': None,...}

   #DK-81 Nordjylland
   dk_nordjylland = iso.country["DK"]["DK-81"]
   dk_nordjylland.name #Nordjylland
   dk_nordjylland.latLng #[56.831, 9.493]
   dk_nordjylland.type #Region

   #DK-84 Hovedstaden
   dk_hovedstaden = iso.country["DK"]["DK-84"]
   dk_hovedstaden.name #Hovedstaden
   dk_hovedstaden.flagUrl #https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/DK/DK-84.svg
   dk_hovedstaden.parentCode #null

   #DK-85 Sjælland
   dk_sjalland = iso.country["DK"]["DK-85"]
   dk_sjalland.name #Sjælland
   dk_sjalland.type #Region
   dk_sjalland.flagUrl #https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/DK/DK-85.svg

Accessing all Estonian (EE) subdivision data:

.. code-block:: python

   import iso3166_2 as iso

   iso.country["EE"]
   #{'EE-37': {'name': 'Harjumaa', 'localName': 'Harjumaa', 'type': 'County', 'parentCode': None,...}

   #EE-39 Hiiumaa
   ee_hiiumaa = iso.country["EE"]["EE-39"]
   ee_hiiumaa.name #Hiiumaa
   ee_hiiumaa.localName #Hiiumaa
   ee_hiiumaa.latLng #[58.924, 22.592]

   #EE-130 Alutaguse
   ee_alutaguse = iso.country["EE"]["EE-130"]
   ee_alutaguse.name #Alutaguse
   ee_alutaguse.parentCode #EE-45
   ee_alutaguse.flagUrl #https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/EE/EE-130.svg

   #EE-338 Kose
   ee_kose = iso.country["EE"]["EE-338"]
   ee_kose.name #Kose
   ee_kose.type #Rural municipality
   ee_kose.parentCode #EE-37

Accessing subdivision data for all countries
--------------------------------------------

To access ALL subdivision data for ALL available countries, you need to access the ``all`` attribute within the ``country`` object instance of the ``ISO3166_2`` class. You can then access an individual country's subdivisiond data by passing in the sought 2 letter alpha-2 or 3 letter alpha-3 country code.

.. code-block:: python

   import iso3166_2 as iso

   all_data = iso.country.all

   all_data["LU"] #all subdivision data for Luxembourg
   all_data["PW"] #all subdivision data for Palau
   all_data["TUV"] #all subdivision data for Tuvalu
   all_data["WLF"] #all subdivision data for Wallis & Futuna

Adding custom subdivisions
--------------------------

Add or delete a custom subdivision to an existing country on the main iso3166-2.json object. The purpose of this functionality is similar to 
that of the user-assigned code elements of the ISO 3166-1 standard. Custom subdivisions and subdivision codes can be used for in-house/bespoke 
applications that are using the **iso3166-2** software but require additional custom subdivisions to be represented. If the input custom subdivision 
code already exists then an error will be raised, otherwise it will be appended to the object.

If the added subdivision is required to be deleted from the object, then you can call the same function with the alpha-2 and subdivision codes' 
parameters but also setting the ``delete`` parameter to 1/True. 

.. code-block:: python

   import iso3166_2 as iso

   #adding custom Belfast province to Ireland (IE)
   iso.country.custom_subdivision("IE", "IE-BF", name="Belfast", local_name="Béal Feirste", type="province", lat_lng=[54.596, -5.931], parent_code=None, flag_url=None)

   #adding custom Mariehamn province to Aland Islands (AX)
   iso.country.custom_subdivision("AX", "AX-M", name="Mariehamn", local_name="Maarianhamina", type="province", lat_lng=[60.0969, 19.934], parent_code=None, flag_url=None)

.. warning::
    When adding a custom subdivision the software will be out of sync with the official ISO 3166-2 dataset, therefore its important to keep track
    of the custom subdivisions you add to the object. 
    
    To return to the original dataset you can delete the added custom subdivision, as described above, or you could reinstall the software. 

Searching for a subdivision
---------------------------
The ``search()`` function allows you to search for a specific subdivision via its subdivision name. The 
search functionality will search over all subdivisions in the object, returning either a subdivision 
with the exact match or subdivisions whose names approximately match the sought input name.

.. code-block:: python

   import iso3166_2 as iso

   #searching for the Monaghan county in Ireland (IE-MN) - returning exact matching subdivision
   iso.country.search("Monaghan", any=False)

   #searching for any subdivisions that have "Southern" in their name
   iso.country.search("Southern", any=True)

.. note::
    A demo of the software and API is available `here <https://colab.research.google.com/drive/1btfEx23bgWdkUPiwdwlDqKkmUp1S-_7U?usp=sharing/>`_.