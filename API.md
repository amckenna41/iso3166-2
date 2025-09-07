<a name="TOP"></a>

# ISO 3166-2 API 🌎

<!-- ![Vercel](https://therealsujitk-vercel-badge.vercel.app/?app=iso3166-2) -->
![Vercel](https://vercelbadge.vercel.app/api/amckenna41/iso3166-2-api)

The main API endpoint is:

> [https://iso3166-2-api.vercel.app/api](https://iso3166-2-api.vercel.app/api)

The other endpoints available in the API are:
* https://iso3166-2-api.vercel.app/api/all
* https://iso3166-2-api.vercel.app/api/alpha/<input_alpha>
* https://iso3166-2-api.vercel.app/api/subdivision/<input_subdivision>
* https://iso3166-2-api.vercel.app/api/search/<input_search_name>
* https://iso3166-2-api.vercel.app/api/country_name/<input_country_name>
* https://iso3166-2-api.vercel.app/api/list_subdivisions

Six paths/endpoints are available in the API - `/api/all`, `/api/alpha`, `/api/subdivision`, `/api/search`, `/api/country_name`  and `/api/list_subdivisions`.

* `/api`: main homepage and API documentation.

* `/api/all`: get all of the ISO 3166 subdivision data for all countries.

* `/api/alpha`: get all of the ISO 3166 subdivision data for 1 or more inputted ISO 3166-1 alpha-2, alpha-3 or numeric country codes, e.g. `/api/alpha/FR,DE,HU,ID,MA`, `/api/alpha/FRA,DEU,HUN,IDN,MAR` and `/api/alpha/428,504,638`. A comma separated list of multiple alpha codes can also be input. If an invalid country code is input then an error will be returned.

* `/api/subdivision`: get all of the ISO 3166 subdivision data for 1 or more ISO 3166-2 subdivision codes, e.g `/api/subdivision/GB-ABD`. You can also input a comma separated list of subdivision codes from the same and or different countries and the data for each will be returned e.g `/api/subdivision/IE-MO,FI-17,RO-AG`. If the input subdivision code is not in the correct format then an error will be raised. Similarly if an invalid subdivision code that doesn't exist is input then an error will be raised.

* `/api/search/`: get all of the ISO 3166 subdivision data for 1 or more ISO 3166-2 subdivision names that match the inputted search terms, e.g `/api/search/Derry`, `/api/search/Kimpala`. You can also input a comma separated list of subdivision name from the same or different countries and the data for each will be returned e.g `/api/name/Paris,Frankfurt,Rimini`. A closeness function is utilised to find the matching subdivision name, if no exact name match found then the most approximate subdivisions will be returned. Some subdivisions may have the same name, in this case each subdivision and its data will be returned e.g `/api/name/Saint George` (this example returns 5 subdivisions). If an invalid subdivision name that doesn't match any is input then an error will be raised. The `likeness` and `excludeMatchScore` query string parameters can be used with this endpoint. 

* `/api/country_name`: get all of the ISO 3166 subdivision data for 1 or more inputted ISO 3166-1 country names, as they are commonly known in English, e.g. `/api/country_name/France,Moldova,Benin`. A comma separated list of country names can also be input. A closeness function is utilised so the most approximate name from the input will be used e.g. Sweden will be returned if the input is `/api/country_name/Swede`. If no country is found from the closeness function or an invalid name is input then an error will be returned. The `likeness` query string parameter can be used with this endpoint.

* `/api/list_subdivisions`: get list of all the subdivision codes for all countries. You can also get the list of subdivisions from a subset of 
countries via their ISO 3166-1 country code.

### Query String Parameters
There are three main query string parameters that can be passed through several of the endpoints of the API:

* **likeness** - this is a value between 1 and 100 that increases or reduces the % of similarity/likeness that the 
inputted search terms have to match to the subdivision data in the subdivision code, name and local/other name attributes. This can be used with the `/api/search` and `/api_country_name` endpoints. Having a higher value should return more exact and less total matches and 
having a lower value will return less exact but more total matches, e.g ``/api/search/Paris?likeness=50``, 
``/api/country_name/Tajikist?likeness=90`` (default=100).
* **filterAttributes** - this is a list of the default supported attributes that you want to include in the output. By default all attributes will be returned but this parameter is useful if you only require a subset of attributes, e.g `api/alpha/DEU?filter=latLng,flag`, `api/subdivision/PL-02?filter=localOtherName`.
* **excludeMatchScore** - this allows you to exclude the matchScore attribute from the search results when using the `/api/search endpoint`. The match score is the % of a match each returned subdivision data object is to the search terms, with 100% being an exact match. By default the match score is returned for each object, e.g `/api/search/Bucharest?excludeMatchScore=1`, ``/api/search/Oregon?excludeMatchScore=1`` (default=0).

> A demo of the software and API is available [here][demo].

Get ALL ISO 3166-2 subdivision data for ALL countries
-----------------------------------------------------
### Request
`GET /api/all`

    curl -i https://iso3166-2-api.vercel.app/api/all

### Response
    HTTP/2 200 
    content-type: application/json
    date: Wed, 20 Dec 2024 17:29:39 GMT
    server: Vercel
    content-length: 837958

    {"AD":..., "AE":...}

### Python
```python
import requests

request_url = "https://iso3166-2-api.vercel.app/api/all"

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

Get all ISO 3166-2 subdivision data for a specific country, using its 2 letter alpha-2 code e.g FR, DE
------------------------------------------------------------------------------------------------------
### Request
`GET /api/alpha/FR`

    curl -i https://iso3166-2-api.vercel.app/api/alpha/FR

### Response
    HTTP/2 200 
    content-type: application/json
    date: Wed, 20 Dec 2024 17:30:27 GMT
    server: Vercel
    content-length: 26298

    {"FR":{"FR-01":{...}}}

### Request
`GET /api/alpha/DE`

    curl -i https://iso3166-2-api.vercel.app/api/alpha/DE

### Response
    HTTP/2 200 
    content-type: application/json
    date: Wed, 20 Dec 2024 17:31:19 GMT
    server: Vercel
    content-length: 3053

    {"DE":{"DE-BB":{...}}}

### Python
```python
import requests

base_url = "https://iso3166-2-api.vercel.app/api/alpha/"
input_alpha2 = "FR" #DE

request_url = f'{base_url}{input_alpha2}'

all_request = requests.get(request_url)
all_request.json() 
```

### Javascript
```javascript
let input_alpha2 = "FR"; //DE

function getData() {
  const response = 
    await fetch(`https://iso3166-2-api.vercel.app/api/alpha/${input_alpha2}`); 
  const data = await response.json()
}

// Begin accessing JSON data here
var data = JSON.parse(this.response)
```

Get all ISO 3166-2 subdivision data for a specific country, using its 3 letter alpha-3 code e.g CZE, HRV
--------------------------------------------------------------------------------------------------------

### Request
`GET /api/alpha/CZE`

    curl -i https://iso3166-2-api.vercel.app/api/alpha/CZE

### Response
    HTTP/2 200 
    content-type: application/json
    date: Wed, 20 Dec 2024 17:42:24 GMT
    server: Vercel
    content-length: 14266

    {"CZ":{"CZ-10":{"..."}}}

### Request
`GET /api/alpha/HRV`

    curl -i https://iso3166-2-api.vercel.app/api/alpha/HRV

### Response
    HTTP/2 200 
    content-type: application/json
    date: Wed, 20 Dec 2024 17:46:12 GMT
    server: Vercel
    content-length: 5456

    {"HR":{"HR-01":{"..."}}}

### Python
```python
import requests

base_url = "https://iso3166-2-api.vercel.app/api/alpha/"
input_alpha3 = "CZE" #HRV

request_url = f'{base_url}{input_alpha3}'

all_request = requests.get(request_url)
all_request.json() 
```

### Javascript
```javascript
let input_alpha3 = "CZE"; //HRV

function getData() {
  const response = 
    await fetch(`https://iso3166-2-api.vercel.app/api/alpha/${input_alpha3}`); 
  const data = await response.json()
}

// Begin accessing JSON data here
var data = JSON.parse(this.response)
```

Get all ISO 3166-2 subdivision data for a specific country, using its numeric code e.g 268, 398
-----------------------------------------------------------------------------------------------

### Request
`GET /api/alpha/268`

    curl -i https://iso3166-2-api.vercel.app/api/alpha/268

### Response
    HTTP/2 200 
    content-type: application/json
    date: Fri, 22 Dec 2024 18:20:14 GMT
    server: Vercel
    content-length: 1899

    {"GE":{"GE-AB":{"..."}}}

### Request
`GET /api/alpha/398`

    curl -i https://iso3166-2-api.vercel.app/api/alpha/398

### Response
    HTTP/2 200 
    content-type: application/json
    date: Fri, 22 Dec 2024 19:40:10 GMT
    server: Vercel
    content-length: 2922

    {"KZ":{"KZ-10":{"..."}}}

### Python
```python
import requests

base_url = "https://iso3166-2-api.vercel.app/api/alpha/"
input_numeric = "268" #398

request_url = f'{base_url}{input_numeric}'

all_request = requests.get(request_url)
all_request.json() 
```

### Javascript
```javascript
let input_numeric = "268"; //398

function getData() {
  const response = 
    await fetch(`https://iso3166-2-api.vercel.app/api/alpha/${input_numeric}`); 
  const data = await response.json()
}

// Begin accessing JSON data here
var data = JSON.parse(this.response)
```

Get all ISO 3166-2 subdivision data for a specific subdivision, using its subdivision code e.g LV-007, PA-3, ZA-NC
------------------------------------------------------------------------------------------------------------------

### Request
`GET /api/subdivision/LV-007`

    curl -i https://iso3166-2-api.vercel.app/api/subdivision/LV-007

### Response
    HTTP/2 200 
    content-type: application/json
    date: Mon, 29 Jan 2025 11:25:52 GMT
    server: Vercel
    content-length: 244

    {"LV-007":{"flag":"https://github.com/amckenna41/...}}

### Request
`GET /api/subdivision/PA-3`

    curl -i https://iso3166-2-api.vercel.app/api/subdivision/PA-3

### Response
    HTTP/2 200 
    content-type: application/json
    date: Mon, 29 Jan 2025 11:28:02 GMT
    server: Vercel
    content-length: 214

    {"PA-3":{"flag":"https://github.com/amckenna41...}}

### Request
`GET /api/subdivision/ZA-NC`

    curl -i https://iso3166-2-api.vercel.app/api/subdivision/ZA-NC

### Response
    HTTP/2 200 
    content-type: application/json
    date: Mon, 29 Jan 2025 11:37:04 GMT
    server: Vercel
    content-length: 225

    {"ZA-NC":{"flag":"https://github.com/amckenna41...}}


Search for ISO 3166-2 subdivision data using its subdivision name or local/other name e.g Treviso (IT-TV), Nordland (NO-18), Musandam (OM-MU)
--------------------------------------------------------------------------------------------------------------------------------------------------

### Request
`GET /api/search/Treviso`

    curl -i https://iso3166-2-api.vercel.app/api/search/Treviso

### Response
    HTTP/2 200 
    content-type: application/json
    date: Mon, 29 Jan 2025 13:02:10 GMT
    server: Vercel
    content-length: 215

    {"IT-TV":{"flag":"}}

### Request
`GET /api/search/Nordland`

    curl -i https://iso3166-2-api.vercel.app/api/search/Nordland

### Response
    HTTP/2 200 
    content-type: application/json
    date: Mon, 29 Jan 2025 13:07:01 GMT
    server: Vercel
    content-length: 212

    {"NO-18":{"flag":"}}

### Request
`GET /api/search/Musandam`

    curl -i https://iso3166-2-api.vercel.app/api/search/Musandam

### Response
    HTTP/2 200 
    content-type: application/json
    date: Mon, 29 Jan 2025 13:11:09 GMT
    server: Vercel
    content-length: 132

    {"OM-MU":{"flag":}}

### Python
```python
import requests

base_url = "https://iso3166-2-api.vercel.app/api/search/"
input_subdivision_name = "Treviso" #Nordland, Musandam

request_url = f'{base_url}{input_subdivision_name}'
params={"likeness":"90"} #pass a likeness score of 90 to the request

all_request = requests.get(request_url, params=params)
all_request.json() 
```

### Javascript
```javascript
let input_subdivision_name = "Treviso"; //Nordland, Musandam
let params = {"likeness": "90"} //pass a likeness score of 90 to the request

function getData() {
  const response = 
    await fetch(`https://iso3166-updates.com/api/search/${input_subdivision_name}`, params); 
  const data = await response.json()
}

// Begin accessing JSON data here
var data = JSON.parse(this.response)
```

Get all ISO 3166-2 subdivision data for a specific country, using country name, e.g. Tajikistan (TJ), Seychelles (SC), Uganda (UG) 
----------------------------------------------------------------------------------------------------------------------------------

### Request
`GET /api/country_name/Tajikistan`

    curl -i https://iso3166-2-api.vercel.app/api/country_name/Tajikistan

### Response
    HTTP/2 200 
    content-type: application/json
    date: Sat, 23 Dec 2024 14:01:19 GMT
    server: Vercel
    content-length: 701

    {"TJ":{"TJ-DU":{...}}}

### Request
`GET /api/country_name/Seychelles`

    curl -i https://iso3166-2-api.vercel.app/api/country_name/Seychelles

### Response
    HTTP/2 200 
    content-type: application/json
    date: Sat, 23 Dec 2024 14:15:53 GMT
    server: Vercel
    content-length: 5085

    {"SC":{"SC-01":{...}}}

### Request
`GET /api/country_name/Uganda`

    curl -i https://iso3166-2-api.vercel.app/api/country_name/Uganda

### Response
    HTTP/2 200 
    content-type: application/json
    date: Sat, 23 Dec 2024 14:17:39 GMT
    server: Vercel
    content-length: 14965

    {"UG":{"UG-101":{...}}}

### Python
```python
import requests

base_url = "https://iso3166-2-api.vercel.app/api/country_name/"
input_name = "Tajikistan" #Seychelles, Uganda

request_url = f'{base_ur}{input_name}'

all_request = requests.get(request_url)
all_request.json() 
```

### Javascript
```javascript
let input_name = "Tajikistan"; //Seychelles, Uganda

function getData() {
  const response = 
    await fetch(`https://iso3166-updates.com/api/country_name/${input_name}`); 
  const data = await response.json()
}

// Begin accessing JSON data here
var data = JSON.parse(this.response)
```

Get all ISO 3166-2 subdivision codes for all countries, or subset of countries
-------------------------------------------------------------------

### Request
`GET /api/list_subdivisions`

    curl -i https://iso3166-2-api.vercel.app/api/list_subdivisions

### Response
    HTTP/2 200 
    content-type: application/json
    date: Sat, 03 Feb 2025 15:03:11 GMT
    server: Vercel
    content-length: 

    {"AD":{"AD-02","AD-03"...}}

### Request
`GET /api/list_subdivisions/LK`

    curl -i https://iso3166-2-api.vercel.app/api/list_subdivisions/LK

### Response
    HTTP/2 200 
    content-type: application/json
    date: Sat, 04 Feb 2025 15:01:12 GMT
    server: Vercel
    content-length: 

    {"LK":{"LK-1","LK-1"...}}

### Python
```python
import requests

request_url = "https://iso3166-2-api.vercel.app/api/list_subdivisions"
#request_url = "https://iso3166-2-api.vercel.app/api/list_subdivisions/LK"

all_request = requests.get(request_url)
all_request.json() 
```

### Javascript
```javascript
function getData() {
  const response = 
    await fetch(`https://iso3166-updates.com/api/list_subdivisions`); 
    // await fetch(`https://iso3166-updates.com/api/list_subdivisions/LK`); 
  const data = await response.json()
}

// Begin accessing JSON data here
var data = JSON.parse(this.response)
```

Get all ISO 3166-2 subdivision codes for all countries, filtering and only returning the name and localOtherName attributes
---------------------------------------------------------------------------------------------------------------------------
### Request
`GET /api/all`

    curl -i https://iso3166-2-api.vercel.app/api/all?filter=name,localOtherName

### Response
    HTTP/2 200 
    content-type: application/json
    date: Wed, 10 May 2025 14:22:31 GMT
    server: Vercel
    content-length: X

    {"AD":..., "AE":...}

### Python
```python
import requests

request_url = "https://iso3166-2-api.vercel.app/api/all"

all_request = requests.get(request_url, params={"filter": "name, localOtherName"})
all_request.json() 
```

### Javascript
```javascript
function getData() {
  const response = await fetch('https://iso3166-2-api.vercel.app/api/all?filter=name,localOtherName')
  const data = await response.json()
}

// Begin accessing JSON data here
var data = JSON.parse(this.response)
```

[Back to top](#TOP)

[demo]: https://colab.research.google.com/drive/1btfEx23bgWdkUPiwdwlDqKkmUp1S-_7U?usp=sharing