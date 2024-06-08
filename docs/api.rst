API 
====

.. The ISO 3166-2 API is a custom-built, open-source and free to use RESTful API that provides programmatic access to a plethora of subdivision data attributes 
.. for all ISO 3166-2 countries/territories. For each country, the API returns its subdivisions' codes, names, local names, types, parent codes, 
.. latitude/longitudes and flags. The API accepts the alpha-2, alpha-3 and numeric variations of the ISO 3166-1 country codes, this will return all the 
.. subdivision data for the sought country. The country name can also be used to search for the sought country's subdivision data. Finally, the ISO 3166-2 
.. subdivision name and code can be used to search for a sought subdivision.

The main API endpoint is: `https://iso3166-2-api.vercel.app/api <https://iso3166-2-api.vercel.app/api/>`_. This endpoint displays the API documentation and forms the
base URL for the 6 other endpoints.

The other endpoints available in the API are:

* https://iso3166-2-api.vercel.app/api/all
* https://iso3166-2-api.vercel.app/api/alpha/<input_alpha>
* https://iso3166-2-api.vercel.app/api/subdivision/<input_subdivision>
* https://iso3166-2-api.vercel.app/api/country_name/<input_country_name> 
* https://iso3166-2-api.vercel.app/api/name/<input_name>
* https://iso3166-2-api.vercel.app/api/list_subdivisions

Six paths/endpoints are available in the API - `/api/all`, `/api/alpha`, `/api/subdivision`, `/api/country_name`, `/api/name` and `/api/list_subdivisions`.

* `/api/all`: get all of the ISO 3166 subdivision data for all countries.

* `/api/alpha`: get all of the ISO 3166 subdivision data for 1 or more inputted ISO 3166-1 alpha-2, alpha-3 or numeric country codes, e.g. `/api/alpha/FR,DE,HU,ID,MA`, `/api/alpha/FRA,DEU,HUN,IDN,MAR` and `/api/alpha/428,504,638`. A comma separated list of multiple alpha codes can also be input. If an invalid country code is input then an error will be returned.

* `/api/country_name`: get all of the ISO 3166 subdivision data for 1 or more inputted ISO 3166-1 country names, as they are commonly known in English, e.g. `/api/country_name/France,Moldova,Benin`. A comma separated list of country names can also be input. A closeness function is utilized so the most approximate name from the input will be used e.g. Sweden will be used if input is `/api/country_name/Swede`. If no country is found from the closeness function or an invalid name is input then an error will be returned.

* `/api/subdivision`: get all of the ISO 3166 subdivision data for 1 or more ISO 3166-2 subdivision codes, e.g `/api/subdivision/GB-ABD`. You can also input a comma separated list of subdivision codes from the same and or different countries and the data for each will be returned e.g `/api/subdivision/IE-MO,FI-17,RO-AG`. If the input subdivision code is not in the correct format then an error will be raised. Similarly if an invalid subdivision code that doesn't exist is input then an error will be raised.

* `/api/name`: get all of the ISO 3166 subdivision data for 1 or more ISO 3166-2 subdivision names, e.g `/api/name/Derry`. You can also input a comma separated list of subdivision name from the same or different countries and the data for each will be returned e.g `/api/name/Paris,Frankfurt,Rimini`. A closeness function is utilized to find the matching subdivision name, if no exact name match found then the most approximate subdivisions will be returned. Some subdivisions may have the same name, in this case each subdivision and its data will be returned e.g `/api/name/Saint George` (this example returns 5 subdivisions). This endpoint also has the likeness score (`?likeness=`) query string parameter that can be appended to the URL. This can be set between 1 - 100, representing a % of likeness to the input name the return subdivisions should be, e.g: a likeness score of 90 will return fewer potential matches whose name only match to a high degree compared to a score of 10 which will create a larger search space, thus returning more potential subdivision matches. A default likeness of 100 (exact match) is used, if no matching subdivision is found then this is reduced to 90. If an invalid subdivision name that doesn't match any is input then an error will be raised.

* `/api/list_subdivisions`: get list of all subdivision codes per country.
  
* `/api`: main homepage and API documentation.

Get subdivision data for all countries
---------------------------------------

Python Requests:

.. code-block:: python

    import requests

    base_url = "https://iso3166-2-api.vercel.app/api/"
    all_data = requests.get(base_url + "all").json()
    
    all_data["AD"] #subdivision data for Andorra
    all_data["IE"] #subdivision data for Ireland
    all_data["PW"] #subdivision data for Palau

curl::
    
    $ curl -i https://iso3166-2-api.vercel.app/api/all

Get subdivision data per country, using its ISO 3166-1 alpha code (alpha-2, alpha-3, numeric)
---------------------------------------------------------------------------------------------
For example, accessing all subdivision data for France (FR,FRA,250), Germany (DE,DEU,276) or Gambia (GM,GMB,270), via their **alpha-2 country code**:

Python Requests:

.. code-block:: python

    import requests

    base_url = "https://iso3166-2-api.vercel.app/api/"
    input_alpha = "FR" #DE, GM
    all_data = requests.get(base_url + f'/alpha/{input_alpha}').json()

    all_data["FR"] #subdivision data for France

curl::

    $ curl -i https://iso3166-2-api.vercel.app/api/alpha/FR
    $ curl -i https://iso3166-2-api.vercel.app/api/alpha/DE
    $ curl -i https://iso3166-2-api.vercel.app/api/alpha/GM


For example, accessing all subdivision data for Greece (GR,GRC,300), Mexico (MX,MEX,484) or Montenegro (ME,MNE,499), via their **alpha-3 country code**:

Python Requests:

.. code-block:: python

    import requests

    base_url = "https://iso3166-2-api.vercel.app/api/"
    input_alpha = "GRC" #MEX, MNE
    all_data = requests.get(base_url + f'/alpha/{input_alpha}').json()

    all_data["GR"] #subdivision data for Greece

curl::

    $ curl -i https://iso3166-2-api.vercel.app/api/alpha/GRC
    $ curl -i https://iso3166-2-api.vercel.app/api/alpha/MEX
    $ curl -i https://iso3166-2-api.vercel.app/api/alpha/MNE


For example, accessing all subdivision data for Nicaragua (NI,NIC,558), Papa New Guinea (PG,PNG,598) or Qatar (QA,QAT,634) via their **alpha numeric country code**:

Python Requests:

.. code-block:: python

    import requests

    base_url = "https://iso3166-2-api.vercel.app/api/"
    input_alpha = "558" #598, 634 (NI, PG, QA)
    all_data = requests.get(base_url + f'/alpha/{input_alpha}').json()

    all_data["NI"] #subdivision data for Nicaragua

curl::

    $ curl -i https://iso3166-2-api.vercel.app/api/alpha/558
    $ curl -i https://iso3166-2-api.vercel.app/api/alpha/598
    $ curl -i https://iso3166-2-api.vercel.app/api/alpha/634


Get all subdivision data for a specific subdivision, using its subdivision code 
-------------------------------------------------------------------------------
For example, accessing all subdivision data for LV-007 (Alūksnes novads), PA-3 (Colón) and ZA-NC (Northern Cape):

Python Requests:

.. code-block:: python

    import requests

    base_url = "https://iso3166-2-api.vercel.app/api/"
    input_subdivision = "LV-007" #PA-3, ZA-NC
    all_data = requests.get(base_url + f'/subdivision/{input_subdivision}').json()

    all_data["LV-007"] #data for LV-007 subdivision

curl::

    $ curl -i https://iso3166-2-api.vercel.app/api/subdivision/LV-007
    $ curl -i https://iso3166-2-api.vercel.app/api/subdivision/PA-3
    $ curl -i https://iso3166-2-api.vercel.app/api/subdivision/ZA-NC

Get all subdivision data for a specific country, using its name
---------------------------------------------------------------
For example, accessing all subdivision data for Tajikistan (TJ), Seychelles (SC), Uganda (UG):

Python Requests:

.. code-block:: python

    import requests

    base_url = "https://iso3166-2-api.vercel.app/api/"
    input_country_name = "Tajikistan" #Seychelles, Uganda
    all_data = requests.get(base_url + f'/country_name/{input_country_name}').json()

    all_data["TJ"] #subdivision data for Tajikistan
    all_data["SC"] #subdivision data for Seychelles
    all_data["UG"] #subdivision data for Uganda

curl::

    $ curl -i https://iso3166-2-api.vercel.app/api/country_name/Tajikistan
    $ curl -i https://iso3166-2-api.vercel.app/api/country_name/Seychelles
    $ curl -i https://iso3166-2-api.vercel.app/api/country_name/Uganda

Get all subdivision data for a specific subdivision, using its subdivision name 
-------------------------------------------------------------------------------
For this endpoint, there is an optional query parameter called *likeness*. This can be set between 1 - 100, representing a % of likeness to the input 
name the return subdivisions should be, e.g: a *likeness* score of 90 will return fewer potential matches whose name only match to a high degree compared 
to a score of 10 which will create a larger search space, thus returning more potential subdivision matches. A default likeness of 100 (exact match) is 
used, if no matching subdivision is found then this is reduced to 90. If an invalid subdivision name that doesn't match any is input then an error will 
be raised.

For example, accessing all subdivision data for Saarland (DE-SL), Brokopondo (SR-BR), Delaware (US-DE):

Python Requests:

.. code-block:: python

    import requests

    base_url = "https://iso3166-2-api.vercel.app/api/"
    input_name = "Saarland" #Brokopondo, Delaware (DE-SL, SR-BR, US-DE)
    all_data = requests.get(base_url + f'/name/{input_name}').json()

    all_data["DE-SL"] #subdivision data for Saarland
    all_data["SR-BR"] #subdivision data for Brokopondo
    all_data["US-DE"] #subdivision data for Delaware

curl::

    $ curl -i https://iso3166-2-api.vercel.app/api/name/Saarland
    $ curl -i https://iso3166-2-api.vercel.app/api/name/Brokopondo
    $ curl -i https://iso3166-2-api.vercel.app/api/name/Delaware

.. **Error: Not Found Response**

..     {
..         message: "Invalid 2 letter alpha-2 code input: ZZ.",
..         path: "https://iso3166-2-api-amckenna41.vercel.app/api/alpha/zz",
..         status: 400
..     }

Accessing all subdivision's that have "Northern" or "Southern" in them using the *?likeness* query string parameter:

Python Requests:

.. code-block:: python

    import requests

    base_url = "https://iso3166-2-api.vercel.app/api/"
    input_name = "Northern" #Southern
    all_data = requests.get(base_url + f'/name/{input_name}', params={"likeness": 0.8).json()

curl::

    $ curl -i https://iso3166-2-api.vercel.app/api/name/Northern?likeness=0.8
    $ curl -i https://iso3166-2-api.vercel.app/api/name/Southern?likeness=0.8


Get list of all subdivision codes per country
---------------------------------------------
Return a list of all ISO 3166-2 subdivision codes for each country.

Python Requests:

.. code-block:: python

    import requests

    base_url = "https://iso3166-2-api.vercel.app/api/list_subdivisions"
    all_data = requests.get(base_url)

    all_data["DE"] #subdivision codes for Germany
    all_data["OM"] #subdivision data for Oman
    all_data["US"] #subdivision data for US

curl::

    $ curl -i https://iso3166-2-api.vercel.app/api/list_subdivisions


.. note::
    A demo of the software and API is available |demo_link|.

.. |demo_link| raw:: html

   <a href="https://colab.research.google.com/drive/1btfEx23bgWdkUPiwdwlDqKkmUp1S-_7U?usp=sharing" target="_blank">here</a>