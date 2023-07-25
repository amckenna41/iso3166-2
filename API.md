# ISO 3166-2 API

![Vercel](https://therealsujitk-vercel-badge.vercel.app/?app=iso3166-2-api)

As well as the Python software package, an API is also available to access all of the data available for all countries in the ISO 3166 via a URL endpoint. You can search for a particular country using its 2 letter alpha-2 code or 3 letter alpha-3 code (e.g EG, FR, DE or EGY, FRA, DEU) via the 'alpha2' query parameter appended to the API URL. Additionally, multiple countries can be input in a comma seperated list. Countries can also be searched for using the 'name' input parameter which is the name of the country as it is commonly known in english, according to the ISO 3166-1. The 'all' (https://iso3166-2-api.vercel.app/api/all) endpoint will return all data and fields for all countries in the ISO 3166. 

The main API endpoint is:

> https://iso3166-2-api.vercel.app/api/

The other endpoints available in the API are:
* https://iso3166-2-api.vercel.app/api/all
* https://iso3166-2-api.vercel.app/api/alpha2/<input_alpha2>
* https://iso3166-2-api.vercel.app/api/name/<input_name>

Requirements
------------
* [python][python] >= 3.8
* [flask][flask] >= 2.3.2
* [requests][requests] >= 2.28.1
* [iso3166][iso3166] >= 2.1.1
* [google-auth][google-auth] >= 2.17.3
* [google-cloud-storage][google-cloud-storage] >= 2.8.0
* [google-api-python-client][google-api-python-client] >= 2.86.0

Get All ISO 3166-2 updates for all countries
-------------------------------------------
### Request
`GET /`

    curl -i https://iso3166-2-api.vercel.app/api/all

### Response
    HTTP/2 200 
    content-type: application/json
    date: Tue, 20 Dec 2022 17:29:39 GMT
    server: Google Frontend
    content-length: 202273

    {"AD":..., "AE":...}

### Python
```python
import requests

base_url = "https://iso3166-2-api.vercel.app/api/all"

all_request = requests.get(base_url)
all_request.json() 
```

### Javascript
```javascript
function getData() {
  const response = await fetch('https://iso3166-2-api.vercel.app/api/all')
  const data = await response.json()
}

// Begin accessing JSON data here
var data = JSON.parse(this.response)
```

Get all country and ISO 3166-2 data for a specific country, using its 2 letter alpha-2 code e.g FR, DE, HN
----------------------------------------------------------------------------------------------------------

### Request
`GET /alpha2/FR`

    curl -i https://iso3166-2-api.vercel.app/api?alpha2=FR
    curl -i https://iso3166-2-api.vercel.app/api/alpha2/FR

### Response
    HTTP/2 200 
    content-type: application/json
    date: Tue, 20 Dec 2022 17:30:27 GMT
    server: Google Frontend
    content-length: 4513

    {"FR":[{"altSpellings":"", "area": "", "borders": ""...}

### Request
`GET /alpha2/DE`

    curl -i https://iso3166-2-api.vercel.app/api?alpha2=DE
    curl -i https://iso3166-2-api.vercel.app/api/alpha2/DE

### Response
    HTTP/2 200 
    content-type: application/json
    date: Tue, 20 Dec 2022 17:31:19 GMT
    server: Google Frontend
    content-length: 10

    {"DE":[{"altSpellings":"", "area": "", "borders": ""...}

### Request
`GET /alpha2/HN`

    curl -i https://iso3166-2-api.vercel.app/api?alpha2=HN
    curl -i https://iso3166-2-api.vercel.app/api/alpha2/HN

### Response
    HTTP/2 200 
    content-type: application/json
    date: Tue, 20 Dec 2022 17:31:53 GMT
    server: Google Frontend
    content-length: 479

    {"HN":[{"altSpellings":"", "area": "", "borders": ""...}

### Python
```python
import requests

base_url = "https://iso3166-2-api.vercel.app/api"

all_request = requests.get(base_url, params={"alpha2": "FR"})
# all_request = requests.get(base_url, params={"alpha2": "DE"})
# all_request = requests.get(base_url, params={"alpha2": "HN"})
all_request.json() 
```

### Javascript
```javascript
function getData() {
  const response = 
    await fetch('https://iso3166-2-api.vercel.app/api?' + 
        new URLSearchParams({
            alpha2: 'FR'
  }));
  const data = await response.json()
}

// Begin accessing JSON data here
var data = JSON.parse(this.response)
```
Get all country and ISO 3166-2 data for a specific country, using country name, e.g. Tajikistan, Seychelles, Uganda
-------------------------------------------------------------------------------------------------------------------

### Request
`GET /name/Tajikistan`

    curl -i https://iso3166-2-api.vercel.app/api?name=Tajikistan
    curl -i https://iso3166-2-api.vercel.app/api/name/Tajikistan

### Response
    HTTP/2 200 
    content-type: application/json
    date: Tue, 20 Dec 2022 17:40:19 GMT
    server: Google Frontend
    content-length: 10

    {"TJ":[{"altSpellings":"", "area": "", "borders": ""...}

### Request
`GET /name/Seychelles`

    curl -i https://iso3166-2-api.vercel.app/api?name=Seychelles
    curl -i https://iso3166-2-api.vercel.app/api/name/Seychelles

### Response
    HTTP/2 200 
    content-type: application/json
    date: Tue, 20 Dec 2022 17:41:53 GMT
    server: Google Frontend
    content-length: 479

    {"SC":[{"altSpellings":"", "area": "", "borders": ""...}

### Request
`GET /name/Uganda`

    curl -i https://iso3166-2-api.vercel.app/api?name=Ugandda
    curl -i https://iso3166-2-api.vercel.app/api/name/Uganda

### Response
    HTTP/2 200 
    content-type: application/json
    date: Tue, 21 Dec 2022 19:43:19 GMT
    server: Google Frontend
    content-length: 10

    {"UG":[{"altSpellings":"", "area": "", "borders": ""...}

### Python
```python
import requests

base_url = "https://iso3166-2-api.vercel.app/api"

all_request = requests.get(base_url, params={"name": "Tajikistan"})
# all_request = requests.get(base_url, params={"name": "Seychelles"})
# all_request = requests.get(base_url, params={"name": "Uganda"})
all_request.json() 
```

### Javascript
```javascript
function getData() {
  const response = 
    await fetch('https://iso3166-2-api.vercel.app/api?' + 
        new URLSearchParams({
            name: 'Tajikistan'
  }));
  const data = await response.json()
}

// Begin accessing JSON data here
var data = JSON.parse(this.response)
```

[flask]: https://flask.palletsprojects.com/en/2.3.x/
[python]: https://www.python.org/downloads/release/python-360/
[requests]: https://requests.readthedocs.io/
[iso3166]: https://github.com/deactivated/python-iso3166
[python-dateutil]: https://pypi.org/project/python-dateutil/
[google-auth]: https://cloud.google.com/python/docs/reference
[google-cloud-storage]: https://cloud.google.com/python/docs/reference
[google-api-python-client]: https://cloud.google.com/python/docs/reference