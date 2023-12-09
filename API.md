# ISO 3166-2 API 🌎

![Vercel](https://therealsujitk-vercel-badge.vercel.app/?app=iso3166-2)

The main API endpoint is:

> [https://iso3166-2-api.vercel.app/api](https://iso3166-2-api.vercel.app/api)

The other endpoints available in the API are:
* https://iso3166-2-api.vercel.app/api/all
* https://iso3166-2-api.vercel.app/api/alpha2/<input_alpha2>
* https://iso3166-2-api.vercel.app/api/name/<input_name>

Three paths/endpoints are available in the API - `/api/all`, `/api/alpha2` and `/api/name`.

* The `/api/all` path/endpoint returns all of the ISO 3166 subdivision data for all countries.

* The `/api/alpha2` endpoint accepts the 2 letter alpha-2 country code appended to the path/endpoint e.g. <i>/api/alpha2/JP</i>. A single alpha-2 code or list of them can be passed to the API e.g. <i>/api/alpha2/FR,DE,HU,ID,MA</i>. For redundancy, the 3 letter alpha-3 counterpart for each country's alpha-2 code can also be appended to the path e.g. <i>/api/alpha2/FRA,DEU,HUN,IDN,MAR</i>. If an invalid alpha-2 code is input then an error will be returned.

* The `/api/name` endpoint accepts the country/territory name as it is most commonly known in english, according to the ISO 3166-1. The name can similarly be appended to the **name** path/endpoint e.g. <i>/api/name/Denmark</i>. A single country name or list of them can be passed into the API e.g. <i>/name/France,Moldova,Benin</i>. A closeness function is utilised so the most approximate name from the input will be used e.g. Sweden will be used if input is <i>/api/name/Swede</i>. If no country is found from the closeness function or an invalid name is input then an error will be returned.

* The main API endpoint (`/` or `/api`) will return the homepage and API documentation.

A demo of the software and API is available [here][demo].

Get All ISO 3166-2 subdivision data for all countries
-----------------------------------------------------
### Request
`GET /api/all`

    curl -i https://iso3166-2-api.vercel.app/api/all

### Response
    HTTP/2 200 
    content-type: application/json
    date: Tue, 20 Dec 2022 17:29:39 GMT
    server: Vercel
    content-length: 837958

    {"AD":..., "AE":...}

### Python
```python
import requests

base_url = "https://iso3166-2-api.vercel.app/api/"

request_url = base_url + "all"

all_request = requests.get(request_url)
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

Get all ISO 3166-2 subdivision data for a specific country, using its 2 letter alpha-2 code e.g FR, DE, HN
----------------------------------------------------------------------------------------------------------

### Request
`GET /api/alpha2/FR`

    curl -i https://iso3166-2-api.vercel.app/api/alpha2/FR

### Response
    HTTP/2 200 
    content-type: application/json
    date: Tue, 20 Dec 2022 17:30:27 GMT
    server: Vercel
    content-length: 26298

    {"FR":{"FR-01":{...}}}

### Request
`GET /api/alpha2/DE`

    curl -i https://iso3166-2-api.vercel.app/api/alpha2/DE

### Response
    HTTP/2 200 
    content-type: application/json
    date: Tue, 20 Dec 2022 17:31:19 GMT
    server: Vercel
    content-length: 3053

    {"DE":{"DE-BB":{...}}}

### Request
`GET /api/alpha2/HN`

    curl -i https://iso3166-2-api.vercel.app/api/alpha2/HN

### Response
    HTTP/2 200 
    content-type: application/json
    date: Tue, 20 Dec 2022 17:31:53 GMT
    server: Vercel
    content-length: 2708

    {"HN":{"HN-AT":{...}}}

### Python
```python
import requests

base_url = "https://iso3166-2-api.vercel.app/api/"
input_alpha2 = "FR" #DE, HN

request_url = base_url + f"alpha2/{input_alpha2}"

all_request = requests.get(request_url)
all_request.json() 
```

### Javascript
```javascript
let input_alpha2 = "FR"; //DE, HN

function getData() {
  const response = 
    await fetch(`https://iso3166-2-api.vercel.app/api/alpha2/${input_alpha2}`); 
  const data = await response.json()
}

// Begin accessing JSON data here
var data = JSON.parse(this.response)
```

Get all ISO 3166-2 subdivision data for a specific country, using country name, e.g. Tajikistan, Seychelles, Uganda 
-------------------------------------------------------------------------------------------------------------------

### Request
`GET /api/name/Tajikistan`

    curl -i https://iso3166-2-api.vercel.app/api/name/Tajikistan

### Response
    HTTP/2 200 
    content-type: application/json
    date: Tue, 20 Dec 2022 17:40:19 GMT
    server: Vercel
    content-length: 701

    {"TJ":{"TJ-DU":{...}}}

### Request
`GET /api/name/Seychelles`

    curl -i https://iso3166-2-api.vercel.app/api/name/Seychelles

### Response
    HTTP/2 200 
    content-type: application/json
    date: Tue, 20 Dec 2022 17:41:53 GMT
    server: Vercel
    content-length: 5085

    {"SC":{"SC-01":{...}}}

### Request
`GET /api/name/Uganda`

    curl -i https://iso3166-2-api.vercel.app/api/name/Uganda

### Response
    HTTP/2 200 
    content-type: application/json
    date: Tue, 21 Dec 2022 19:43:19 GMT
    server: Vercel
    content-length: 14965

    {"UG":{"UG-101":{...}}}

### Python
```python
import requests

base_url = "https://iso3166-2-api.vercel.app/api/"
input_name = "Tajikistan" #Seychelles, Uganda

request_url = base_url + f"name/{input_name}"

all_request = requests.get(request_url)
all_request.json() 
```

### Javascript
```javascript
let input_name = "Tajikistan"; //Seychelles, Uganda

function getData() {
  const response = 
    await fetch(`https://iso3166-updates.com/api/name/${input_name}`); 
  const data = await response.json()
}

// Begin accessing JSON data here
var data = JSON.parse(this.response)
```

[Back to top](#TOP)

[demo]: https://colab.research.google.com/drive/1btfEx23bgWdkUPiwdwlDqKkmUp1S-_7U?usp=sharing