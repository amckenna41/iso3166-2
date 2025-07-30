API 
====

.. The ISO 3166-2 API is a custom-built, open-source and free to use RESTful API that provides programmatic access to a plethora of subdivision data attributes 
.. for all ISO 3166-2 countries/territories. For each country, the API returns its subdivisions' codes, names, local names, types, parent codes, 
.. latitude/longitudes and flags. The API accepts the alpha-2, alpha-3 and numeric variations of the ISO 3166-1 country codes, this will return all the 
.. subdivision data for the sought country. The country name can also be used to search for the sought country's subdivision data. Finally, the ISO 3166-2 
.. subdivision name and code can be used to search for a sought subdivision.

The main API endpoint displays the API documentation and homepage and forms the base URL for the 6 other endpoints: |api_main_endpoint|

.. |api_main_endpoint| raw:: html

   <a href="https://iso3166-2-api.vercel.app/api" target="_blank">https://iso3166-2-api.vercel.app/api</a>

The other endpoints available in the API are:

* https://iso3166-2-api.vercel.app/api/all
* https://iso3166-2-api.vercel.app/api/alpha/<input_alpha>
* https://iso3166-2-api.vercel.app/api/subdivision/<input_subdivision>
* https://iso3166-2-api.vercel.app/api/country_name/<input_country_name>
* https://iso3166-2-api.vercel.app/api/search/<input_search>
* https://iso3166-2-api.vercel.app/api/list_subdivisions/<input_alpha>

.. Six paths/endpoints are available in the API - `/api/all`, `/api/alpha`, `/api/country_name`, `/api/subdivision`, `/api/search` and `/api/list_subdivisions`.

.. * `/api/all`: get all of the ISO 3166 subdivision data for all countries.

.. * `/api/alpha`: get all of the ISO 3166 subdivision data for 1 or more inputted ISO 3166-1 alpha-2, alpha-3 or numeric country codes, e.g. `/api/alpha/FR,DE,HU,ID,MA`, `/api/alpha/FRA,DEU,HUN,IDN,MAR` and `/api/alpha/428,504,638`. A comma separated list of multiple alpha codes can also be input. If an invalid country code is input then an error will be returned.

.. * `/api/subdivision`: get all of the ISO 3166 subdivision data for 1 or more ISO 3166-2 subdivision codes, e.g `/api/subdivision/GB-ABD`. You can also input a comma separated list of subdivision codes from the same and or different countries and the data for each will be returned e.g `/api/subdivision/IE-MO,FI-17,RO-AG`. If the input subdivision code is not in the correct format then an error will be raised. Similarly if an invalid subdivision code that doesn't exist is input then an error will be raised.

.. * `/api/country_name`: get all of the ISO 3166 subdivision data for 1 or more inputted ISO 3166-1 country names, as they are commonly known in English, e.g. `/api/country_name/France,Moldova,Benin`. A comma separated list of country names can also be input. A closeness function is utilised so the most approximate name from the input will be used e.g. Sweden will be used if input is `/api/country_name/Swede`. If no country is found from the closeness function or an invalid name is input then an error will be returned.

.. * `/api/search/`: get all of the ISO 3166 subdivision data for 1 or more ISO 3166-2 subdivision names or input search terms, e.g `/api/search/Derry`. You can also input a comma separated list of subdivision name from the same or different countries and the data for each will be returned e.g `/api/search/Paris,Frankfurt,Rimini`. A closeness function is utilised to find the matching subdivision name, if no exact name match found then the most approximate subdivisions will be returned. Some subdivisions may have the same name, in this case each subdivision and its data will be returned e.g `/api/search/Saint George` (this example returns 5 subdivisions). This endpoint also has the likeness score (`?likeness=`) query string parameter that can be appended to the URL. This can be set between 1 - 100, representing a % of likeness to the input name the return subdivisions should be, e.g: a likeness score of 90 will return fewer potential matches whose name only match to a high degree compared to a score of 10 which will create a larger search space, thus returning more potential subdivision matches. A default likeness of 100 (exact match) is used, if no matching subdivision is found then this is reduced to 90. If an invalid subdivision name that doesn't match any is input then an error will be raised.

.. * `/api/list_subdivisions`: get list of all the subdivision codes for all countries. 

.. * `/api`: main homepage and API documentation.


Query String Parameters
-----------------------
There are 3 main query string parameters available throughout the API that can be appended to your GET request:

* **likeness** - this is a parameter between 1 and 100 that increases or reduces the % of similarity/likeness that the inputted search terms have to match to the subdivision name/local other names. This can be used with the `/api/search`  and `/api/country_name` endpoints. Having a higher value should return more exact and less matches and having a lower value will return less exact but more matches, e.g `/api/search/Paris?likeness=50`, `/api/search/Louisianna?likeness=90` (**default=100**).
* **filterAttributes** - this parameter allows you to only include a subset of desired attributes per subdivision in the output. This can be used in any of the API endpoints, e.g `/api/alpha/AL,BA,CD?filterAttributes=name,type,parentCode`, `/api/subdivision/LV-112?filterAttributes=localOtherName,flag,history` etc.
* **excludeMatchScore** - this parameter allows you to exclude the *matchScore* attribute from the search results when using the `/api/search` endpoint. The match score is the % of a match each returned subdivision data data object is to the search terms, with 100% being an exact match. By default the match score is returned for each object, but setting this parameter to True will exclude the attribute and sort the results by country code, e.g `/api/search/Bernardo O'higgins?excludeMatchScore=1`, `/api/search/New York?excludeMatchScore=1` (**default=0**).


Get subdivision data for ALL countries
--------------------------------------
Return all available subdivision data for all countries via the `/api/all` endpoint.

Python Requests:

.. code-block:: python

    import requests

    base_url = "https://iso3166-2-api.vercel.app/api/"
    all_data = requests.get(f'{base_url}all').json()
    
    all_data["AD"] #subdivision data for Andorra
    all_data["IE"] #subdivision data for Ireland
    all_data["PW"] #subdivision data for Palau
    all_data["ZA"] #subdivision data for South Africa

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
    all_data = requests.get(f'{base_url}/alpha/{input_alpha}').json()

    all_data["FR"] #subdivision data for France
    #all_data["DE"] #subdivision data for Germany
    #all_data["GM"] #subdivision data for Gambia

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
    all_data = requests.get(f'{base_url}/alpha/{input_alpha}').json()

    all_data["GR"] #subdivision data for Greece
    #all_data["MX"] #subdivision data for Mexico
    #all_data["ME"] #subdivision data for Montenegro

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
    all_data = requests.get(f'{base_url}/alpha/{input_alpha}').json()

    all_data["NI"] #subdivision data for Nicaragua
    #all_data["PG"] #subdivision data for Papua New Guinea
    #all_data["QA"] #subdivision data for Qatar

curl::

    $ curl -i https://iso3166-2-api.vercel.app/api/alpha/558
    $ curl -i https://iso3166-2-api.vercel.app/api/alpha/598
    $ curl -i https://iso3166-2-api.vercel.app/api/alpha/634


Get all subdivision data for a specific subdivision, using its subdivision code 
-------------------------------------------------------------------------------
Get all subdivision data for a single or subset of subdivisions using their official ISO 3166-2
subdivision code. For example, accessing all subdivision data for LV-007 (Alūksnes novads), 
PA-3 (Colón) and ZA-NC (Northern Cape):

Python Requests:

.. code-block:: python

    import requests

    base_url = "https://iso3166-2-api.vercel.app/api/"
    input_subdivision = "LV-007" #PA-3, ZA-NC
    all_data = requests.get(f'{base_url}/subdivision/{input_subdivision}').json()

    all_data["LV-007"] #data for LV-007 subdivision
    #all_data["PA-3"] #data for PA-3 subdivision
    #all_data["ZA-NC"] #data for ZA-NC subdivision

curl::

    $ curl -i https://iso3166-2-api.vercel.app/api/subdivision/LV-007
    $ curl -i https://iso3166-2-api.vercel.app/api/subdivision/PA-3
    $ curl -i https://iso3166-2-api.vercel.app/api/subdivision/ZA-NC


Get all subdivision data for a specific country, using its name
---------------------------------------------------------------
Get all subdivision data using the officially recognized country name, as it is commonly known in English. 
For example, accessing all subdivision data for Tajikistan (TJ), Seychelles (SC) and Uganda (UG):

Python Requests:

.. code-block:: python

    import requests

    base_url = "https://iso3166-2-api.vercel.app/api/"
    input_country_name = "Tajikistan" #Seychelles, Uganda
    all_data = requests.get(f'{base_url}/country_name/{input_country_name}').json()

    all_data["TJ"] #subdivision data for Tajikistan
    #all_data["SC"] #subdivision data for Seychelles
    #all_data["UG"] #subdivision data for Uganda

curl::

    $ curl -i https://iso3166-2-api.vercel.app/api/country_name/Tajikistan
    $ curl -i https://iso3166-2-api.vercel.app/api/country_name/Seychelles
    $ curl -i https://iso3166-2-api.vercel.app/api/country_name/Uganda


Search for a specific subdivision, using its subdivision name or local/other names
----------------------------------------------------------------------------------
For this endpoint, there is an optional query parameter called *likeness*. This can be set between 1 - 100, representing a % of likeness to the input 
search term that the subdivisions name or local/other name should be, e.g: a *likeness* score of 90 will return fewer potential matches whose name only 
match to a high degree compared to a score of 10 which will create a larger search space, thus returning more potential subdivision matches. A default 
likeness of 100 (exact match) is used, if no matching subdivision is found then this is reduced to 90. If an invalid subdivision name that doesn't match 
any is input then an error will be raised.

The output will be sorted by an attributes called *matchScore* which is the % likeness that the subdivision name is to the input search terms. This 
attribute can be excluded via the *excludeMatchScore* query string parameter, which will cause the output to be sorted alphabetically as like the
other endpoints.

For example, accessing all subdivision data for Saarland (DE-SL), Brokopondo (SR-BR) and Delaware (US-DE):

Python Requests:

.. code-block:: python

    import requests

    base_url = "https://iso3166-2-api.vercel.app/api/"
    input_search = "Saarland, Brokopondo, Delaware" #DE-SL, SR-BR, US-DE
    all_data = requests.get(f'{base_url}/search/{input_search}').json()

    all_data["DE-SL"] #subdivision data for Saarland
    all_data["SR-BR"] #subdivision data for Brokopondo
    all_data["US-DE"] #subdivision data for Delaware

curl::

    $ curl -i https://iso3166-2-api.vercel.app/api/search/Saarland
    $ curl -i https://iso3166-2-api.vercel.app/api/search/Brokopondo
    $ curl -i https://iso3166-2-api.vercel.app/api/search/Delaware
    $ curl -i https://iso3166-2-api.vercel.app/api/search/Saarland,Brokopondo,Delaware

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
    input_search = "Northern" #Southern
    all_data = requests.get(f'{base_url}/search/{input_search}', params={"likeness": 80).json()

curl::

    $ curl -i https://iso3166-2-api.vercel.app/api/search/Northern?likeness=80
    $ curl -i https://iso3166-2-api.vercel.app/api/search/Southern?likeness=80


Accessing all subdivision's that have "Saint George" in them, excluding the *Match Score* attribute:

Python Requests:

.. code-block:: python

    import requests

    base_url = "https://iso3166-2-api.vercel.app/api/"
    input_search = "Saint George" 
    all_data = requests.get(f'{base_url}/search/{input_search}', params={"excludeMatchScore": 1).json()

curl::

    $ curl -i https://iso3166-2-api.vercel.app/api/search/Northern?likeness=80
    


Get list of all subdivision codes per country
---------------------------------------------
Return a list of all ISO 3166-2 subdivision codes for each country. You can get the list of
subdivisions per country by appending its ISO 3166-1 country code.

Python Requests:

.. code-block:: python

    import requests

    base_url = "https://iso3166-2-api.vercel.app/api/list_subdivisions"
    all_data = requests.get(base_url)

    all_data["DE"] #subdivision codes for Germany
    all_data["OM"] #subdivision data for Oman
    all_data["US"] #subdivision data for US

    #get specific subdivision list via country code
    base_url = "https://iso3166-2-api.vercel.app/api/list_subdivisions/DE"
    all_data = requests.get(base_url)

    base_url = "https://iso3166-2-api.vercel.app/api/list_subdivisions/OM"
    all_data = requests.get(base_url)

    base_url = "https://iso3166-2-api.vercel.app/api/list_subdivisions/US"
    all_data = requests.get(base_url)

curl::

    $ curl -i https://iso3166-2-api.vercel.app/api/list_subdivisions
    $ curl -i https://iso3166-2-api.vercel.app/api/list_subdivisions/DE
    $ curl -i https://iso3166-2-api.vercel.app/api/list_subdivisions/OM
    $ curl -i https://iso3166-2-api.vercel.app/api/list_subdivisions/US


.. note::
    A demo of the software and API is available |demo_link|.

.. |demo_link| raw:: html

   <a href="https://colab.research.google.com/drive/1btfEx23bgWdkUPiwdwlDqKkmUp1S-_7U?usp=sharing" target="_blank">here</a>