API 
====

The main API endpoint is: `https://iso3166-2-api.vercel.app/api <https://iso3166-2-api.vercel.app/api/>`_. This endpoint displays the API documentation and forms the
base URL for the 3 other endpoints.

The other endpoints available in the API are:

* https://iso3166-2-api.vercel.app/api/all
* https://iso3166-2-api.vercel.app/api/alpha2/<input_alpha2>
* https://iso3166-2-api.vercel.app/api/name/<input_name>

Three paths/endpoints are available in the API - `/api/all`, `/api/alpha2` and `/api/name`.

* The `/api/all` path/endpoint returns all of the ISO 3166 subdivision data for all countries.
* The `/api/alpha2` endpoint accepts the 2 letter alpha-2 country code appended to the path/endpoint e.g. */api/alpha2/JP*. A single alpha-2 code or list of them can be passed to the API e.g. */api/alpha2/FR,DE,HU,ID,MA*. For redundancy, the 3 letter alpha-3 counterpart for each country's alpha-2 code can also be appended to the path e.g. */api/alpha2/FRA,DEU,HUN,IDN,MAR*. If an invalid alpha-2 code is input then an error will be returned.
* The `/api/name` endpoint accepts the country/territory name as it is most commonly known in english, according to the ISO 3166-1. The name can similarly be appended to the **name** path/endpoint e.g. */api/name/Denmark*. A single country name or list of them can be passed into the API e.g. */name/France,Moldova,Benin*. A closeness function is utilised so the most approximate name from the input will be used e.g. Sweden will be used if input is */api/name/Swede*. If no country is found from the closeness function or an invalid name is input then an error will be returned.
* The main API endpoint (`/` or `/api`) will return the homepage and API documentation.

Getting all ISO 3166-2 subdivision data
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

Get all ISO 3166-2 subdivision data for a specific country, using its 2 letter alpha-2 code e.g FR, DE, HN
----------------------------------------------------------------------------------------------------------

Python Requests:

.. code-block:: python

    import requests

    base_url = "https://iso3166-2-api.vercel.app/api/"
    input_alpha2 = "FR" #DE, HN
    all_data = requests.get(base_url + f'/alpha2/{input_alpha2}').json()

    all_data["FR"] #subdivision data for France

curl::

    $ curl -i https://iso3166-2-api.vercel.app/api/alpha2/FR
    $ curl -i https://iso3166-2-api.vercel.app/api/alpha2/DE
    $ curl -i https://iso3166-2-api.vercel.app/api/alpha2/HN

Get all ISO 3166-2 subdivision data for a specific country, using country name, e.g. Tajikistan, Seychelles, Uganda 
-------------------------------------------------------------------------------------------------------------------

Python Requests:

.. code-block:: python

    import requests

    base_url = "https://iso3166-2-api.vercel.app/api/"
    input_name = "Tajikistan" #Seychelles, Uganda
    all_data = requests.get(base_url + f'/name/{input_name}').json()

    all_data["TJ"] #subdivision data for Tajikistan

curl::

    $ curl -i https://iso3166-2-api.vercel.app/api/name/Tajikistan
    $ curl -i https://iso3166-2-api.vercel.app/api/name/Seychelles
    $ curl -i https://iso3166-2-api.vercel.app/api/name/Uganda

.. note::
    A demo of the software and API is available `here <https://colab.research.google.com/drive/1btfEx23bgWdkUPiwdwlDqKkmUp1S-_7U?usp=sharing/>`_.