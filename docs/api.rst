API 
====

The main API endpoint is: `https://iso3166-2-api.vercel.app/api <https://iso3166-2-api.vercel.app/api/>`_. This endpoint displays the API documentation and forms the
base URL for the 5 other endpoints.

The other endpoints available in the API are:

* https://iso3166-2-api.vercel.app/api/all
* https://iso3166-2-api.vercel.app/api/alpha/<input_alpha>
* https://iso3166-2-api.vercel.app/api/subdivision/<input_subdivision>
* https://iso3166-2-api.vercel.app/api/country_name/<input_country_name> 
* https://iso3166-2-api.vercel.app/api/name/<input_name>

Five paths/endpoints are available in the API - `/api/all`, `/api/alpha`, `/api/subdivision`, `/api/country_name` and `/api/name`.

* The `/api/all` path/endpoint returns all of the ISO 3166 subdivision data for all countries.
* The `/api/alpha` endpoint accepts the 2 letter alpha-2, 3 letter alpha-3 or numeric country codes appended to the path/endpoint e.g. */api/alpha/JP*. A single alpha code or list of them can be passed to the API e.g. */api/alpha2/FR,DEU,HUN,360,504*. If an invalid alpha code is input then an error will be returned.
* The `/api/subdivision` endpoint accepts the ISO 3166-2 subdivision codes, e.g */api/subd/GB-ABD*. You can also input a list of subdivision code and the data for each will be returned e.g */api/subd/IE-MO,FI-17,RO-AG*. If the input subdivision code is not in the correct format then an error will be raised. Similarly if an invalid subdivision code that doesn't exist is input then an error will be raised.
* The `/api/country_name` endpoint accepts the country/territory name as it is most commonly known in english, according to the ISO 3166-1 e.g `/api/country_name/Denmark`. A single country name or list of them can be passed into the API e.g. `/api/country_name/France,Moldova,Benin`. A closeness function is utilised so the most approximate name from the input will be used e.g. Sweden will be used if input is `/api/country_name/Swede`. If no country is found from the closeness function or an invalid name is input then an error will be returned.
* The `/api/name` endpoint accepts the ISO 3166-2 subdivision names, e.g `/api/name/Derry`. You can also input a list of subdivision name from the same or different countries and the data for each will be returned e.g `/api/name/Paris,Frankfurt,Rimini`. A closeness function is utilised to find the matching subdivision name, if no exact name match found then the most approximate subdivisions will be returned. Some subdivisions may have the same name, in this case each subdivision and its data will be returned e.g `/api/name/Saint George,Sucre`. This endpoint also has the likeness score (`?likeness=`) query string parameter that can be appended to the URL. This can be set between 1 - 100, representing a % of likeness to the input name the return subdivisions should be, e.g: a likeness score of 90 will return fewer potential matches whose name only match to a high degree compared to a score of 10 which will create a larger search space, thus returning more potential subdivision matches. A default likeness of 100 (exact match) is used, if no match found then this is reduced to 90. If an invalid subdivision name that doesn't match any is input then an error will be raised.
* The main API endpoint (`/` or `/api`) will return the homepage and API documentation.

Accessing subdivision data for all countries
--------------------------------------------

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

Accessing subdivision data per country, using its ISO 3166-1 alpha codes
------------------------------------------------------------------------

For example, accessing all subdivision data for France, Germany or Gambia (FR, DE, GM), via their **alpha-2 country code**:

Python Requests:

.. code-block:: python

    import requests

    base_url = "https://iso3166-2-api.vercel.app/api/"
    input_alpha2 = "FR" #DE, GM
    all_data = requests.get(base_url + f'/alpha/{input_alpha}').json()

    all_data["FR"] #subdivision data for France

curl::

    $ curl -i https://iso3166-2-api.vercel.app/api/alpha/FR
    $ curl -i https://iso3166-2-api.vercel.app/api/alpha/DE
    $ curl -i https://iso3166-2-api.vercel.app/api/alpha/GM


For example, accessing all subdivision data for Greece, Mexico or Montenegro (GRC, MEX, MNE), via their **alpha-3 country code**:

Python Requests:

.. code-block:: python

    import requests

    base_url = "https://iso3166-2-api.vercel.app/api/"
    input_alpha2 = "GRC" #MEX, MNE
    all_data = requests.get(base_url + f'/alpha/{input_alpha}').json()

    all_data["GR"] #subdivision data for Greece

curl::

    $ curl -i https://iso3166-2-api.vercel.app/api/alpha/GRC
    $ curl -i https://iso3166-2-api.vercel.app/api/alpha/MEX
    $ curl -i https://iso3166-2-api.vercel.app/api/alpha/MNE


For example, accessing all subdivision data for Nicaragua, Papa New Guinea or Qatar (558, 598, 634), via their **alpha numeric code**:

Python Requests:

.. code-block:: python

    import requests

    base_url = "https://iso3166-2-api.vercel.app/api/"
    input_alpha2 = "558" #598, 634 (NI, PG, QA)
    all_data = requests.get(base_url + f'/alpha/{input_alpha}').json()

    all_data["NI"] #subdivision data for Nicaragua

curl::

    $ curl -i https://iso3166-2-api.vercel.app/api/alpha/558
    $ curl -i https://iso3166-2-api.vercel.app/api/alpha/598
    $ curl -i https://iso3166-2-api.vercel.app/api/alpha/634


Accessing all subdivision data for a specific subdivision, using its subdivision code 
--------------------------------------------------------------------------------------

For example, accessing all subdivision data for Alūksnes novads, Colón and Northern Cape (LV-007, PA-3, ZA-NC):

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

Accessing all subdivision data for a specific country, using its name
---------------------------------------------------------------------

For example, accessing all subdivision data for Tajikistan, Seychelles, Uganda:

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

Accessing all subdivision data for a specific subdivision, using its subdivision name 
-------------------------------------------------------------------------------------

For example, accessing all subdivision data for Saarland, Brokopondo, Delaware:

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
..         path: "https://iso3166-2-api-amckenna41.vercel.app/api/alpha2/zz",
..         status: 400
..     }

.. note::
    A demo of the software and API is available `here <https://colab.research.google.com/drive/1btfEx23bgWdkUPiwdwlDqKkmUp1S-_7U?usp=sharing/>`_.