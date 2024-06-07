# ISO 3166-2 API 🌎

<!-- ![Vercel](https://therealsujitk-vercel-badge.vercel.app/?app=iso3166-2) -->
![Vercel](https://vercelbadge.vercel.app/api/amckenna41/iso3166-2-api)

The main API endpoint is:

> [https://iso3166-2-api.vercel.app/api](https://iso3166-2-api.vercel.app/api)

The other endpoints available in the API are:
* https://iso3166-2-api.vercel.app/api/all
* https://iso3166-2-api.vercel.app/api/alpha/<input_alpha>
* https://iso3166-2-api.vercel.app/api/country_name/<input_country_name>
* https://iso3166-2-api.vercel.app/api/subdivision/<input_subdivision>
* https://iso3166-2-api.vercel.app/api/name/<input_subdivision_name>

Six paths/endpoints are available in the API - `/api/all`, `/api/alpha`, `/api/country_name`, `/api/subdivision`, `/api/name` and `/api/list_subdivisions`.

* `/api/all`: get all of the ISO 3166 subdivision data for all countries.

* `/api/alpha`: get all of the ISO 3166 subdivision data for 1 or more inputted ISO 3166-1 alpha-2, alpha-3 or numeric country codes, e.g. `/api/alpha/FR,DE,HU,ID,MA`, `/api/alpha/FRA,DEU,HUN,IDN,MAR` and `/api/alpha/428,504,638`. A comma separated list of multiple alpha codes can also be input. If an invalid country code is input then an error will be returned.

* `/api/country_name`: get all of the ISO 3166 subdivision data for 1 or more inputted ISO 3166-1 country names, as they are commonly known in English, e.g. `/api/country_name/France,Moldova,Benin`. A comma separated list of country names can also be input. A closeness function is utilised so the most approximate name from the input will be used e.g. Sweden will be used if input is `/api/country_name/Swede`. If no country is found from the closeness function or an invalid name is input then an error will be returned.

* `/api/subdivision`: get all of the ISO 3166 subdivision data for 1 or more ISO 3166-2 subdivision codes, e.g `/api/subdivision/GB-ABD`. You can also input a comma separated list of subdivision codes from the same and or different countries and the data for each will be returned e.g `/api/subdivision/IE-MO,FI-17,RO-AG`. If the input subdivision code is not in the correct format then an error will be raised. Similarly if an invalid subdivision code that doesn't exist is input then an error will be raised.

* `/api/name/`: get all of the ISO 3166 subdivision data for 1 or more ISO 3166-2 subdivision names, e.g `/api/name/Derry`. You can also input a comma separated list of subdivision name from the same or different countries and the data for each will be returned e.g `/api/name/Paris,Frankfurt,Rimini`. A closeness function is utilised to find the matching subdivision name, if no exact name match found then the most approximate subdivisions will be returned. Some subdivisions may have the same name, in this case each subdivision and its data will be returned e.g `/api/name/Saint George` (this example returns 5 subdivisions). This endpoint also has the likeness score (`?likeness=`) query string parameter that can be appended to the URL. This can be set between 1 - 100, representing a % of likeness to the input name the return subdivisions should be, e.g: a likeness score of 90 will return fewer potential matches whose name only match to a high degree compared to a score of 10 which will create a larger search space, thus returning more potential subdivision matches. A default likeness of 100 (exact match) is used, if no matching subdivision is found then this is reduced to 90. If an invalid subdivision name that doesn't match any is input then an error will be raised.

* `/api/list_subdivisions`: get list of all the subdivision codes for all countries. 

* `/api`: main homepage and API documentation.

A demo of the software and API is available [here][demo].

Get ALL ISO 3166-2 subdivision data for ALL countries
-----------------------------------------------------
### Request
`GET /api/all`

    curl -i https://iso3166-2-api.vercel.app/api/all

### Response
    HTTP/2 200 
    content-type: application/json
    date: Wed, 20 Dec 2023 17:29:39 GMT
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
    date: Wed, 20 Dec 2023 17:30:27 GMT
    server: Vercel
    content-length: 26298

    {"FR":{"FR-01":{...}}}

### Request
`GET /api/alpha/DE`

    curl -i https://iso3166-2-api.vercel.app/api/alpha/DE

### Response
    HTTP/2 200 
    content-type: application/json
    date: Wed, 20 Dec 2023 17:31:19 GMT
    server: Vercel
    content-length: 3053

    {"DE":{"DE-BB":{...}}}

### Python
```python
import requests

base_url = "https://iso3166-2-api.vercel.app/api/alpha/"
input_alpha2 = "FR" #DE

request_url = base_url + input_alpha2

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
    date: Wed, 20 Dec 2023 17:42:24 GMT
    server: Vercel
    content-length: 14266

    {"CZ":{"CZ-10":{"..."}}}

### Request
`GET /api/alpha/HRV`

    curl -i https://iso3166-2-api.vercel.app/api/alpha/HRV

### Response
    HTTP/2 200 
    content-type: application/json
    date: Wed, 20 Dec 2023 17:46:12 GMT
    server: Vercel
    content-length: 5456

    {"HR":{"HR-01":{"..."}}}

### Python
```python
import requests

base_url = "https://iso3166-2-api.vercel.app/api/alpha/"
input_alpha3 = "CZE" #HRV

request_url = base_url + input_alpha3

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
    date: Fri, 22 Dec 2023 18:20:14 GMT
    server: Vercel
    content-length: 1899

    {"GE":{"GE-AB":{"..."}}}

### Request
`GET /api/alpha/398`

    curl -i https://iso3166-2-api.vercel.app/api/alpha/398

### Response
    HTTP/2 200 
    content-type: application/json
    date: Fri, 22 Dec 2023 19:40:10 GMT
    server: Vercel
    content-length: 2922

    {"KZ":{"KZ-10":{"..."}}}

### Python
```python
import requests

base_url = "https://iso3166-2-api.vercel.app/api/alpha/"
input_numeric = "268" #398

request_url = base_url + input_numeric

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
    date: Mon, 29 Jan 2024 11:25:52 GMT
    server: Vercel
    content-length: 244

    {"LV-007":{"flag":"https://github.com/amckenna41/...}}

### Request
`GET /api/subdivision/PA-3`

    curl -i https://iso3166-2-api.vercel.app/api/subdivision/PA-3

### Response
    HTTP/2 200 
    content-type: application/json
    date: Mon, 29 Jan 2024 11:28:02 GMT
    server: Vercel
    content-length: 214

    {"PA-3":{"flag":"https://github.com/amckenna41...}}

### Request
`GET /api/subdivision/ZA-NC`

    curl -i https://iso3166-2-api.vercel.app/api/subdivision/ZA-NC

### Response
    HTTP/2 200 
    content-type: application/json
    date: Mon, 29 Jan 2024 11:37:04 GMT
    server: Vercel
    content-length: 225

    {"ZA-NC":{"flag":"https://github.com/amckenna41...}}


Get all ISO 3166-2 subdivision data for a specific subdivision, using its subdivision name e.g Treviso (IT-TV), Nordland (NO-18), Musandam (OM-MU)
--------------------------------------------------------------------------------------------------------------------------------------------------

### Request
`GET /api/name/Treviso`

    curl -i https://iso3166-2-api.vercel.app/api/name/Treviso

### Response
    HTTP/2 200 
    content-type: application/json
    date: Mon, 29 Jan 2024 13:02:10 GMT
    server: Vercel
    content-length: 215

    {"IT-TV":{"flag":"}}

### Request
`GET /api/name/Nordland`

    curl -i https://iso3166-2-api.vercel.app/api/name/Nordland

### Response
    HTTP/2 200 
    content-type: application/json
    date: Mon, 29 Jan 2024 13:07:01 GMT
    server: Vercel
    content-length: 212

    {"NO-18":{"flag":"}}

### Request
`GET /api/name/Musandam`

    curl -i https://iso3166-2-api.vercel.app/api/name/Musandam

### Response
    HTTP/2 200 
    content-type: application/json
    date: Mon, 29 Jan 2024 13:11:09 GMT
    server: Vercel
    content-length: 132

    {"OM-MU":{"flag":}}

### Python
```python
import requests

base_url = "https://iso3166-2-api.vercel.app/api/name/"
input_subdivision_name = "Treviso" #Nordland, Musandam

request_url = base_url + input_subdivision_name
params={"likeness":"90"}

all_request = requests.get(request_url)
all_request.json() 
```

### Javascript
```javascript
let input_subdivision_name = "Treviso"; //Nordland, Musandam
let params = {"likeness": "90"}

function getData() {
  const response = 
    await fetch(`https://iso3166-updates.com/api/name/${input_subdivision_name}`, params); 
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
    date: Sat, 23 Dec 2023 14:01:19 GMT
    server: Vercel
    content-length: 701

    {"TJ":{"TJ-DU":{...}}}

### Request
`GET /api/country_name/Seychelles`

    curl -i https://iso3166-2-api.vercel.app/api/country_name/Seychelles

### Response
    HTTP/2 200 
    content-type: application/json
    date: Sat, 23 Dec 2023 14:15:53 GMT
    server: Vercel
    content-length: 5085

    {"SC":{"SC-01":{...}}}

### Request
`GET /api/country_name/Uganda`

    curl -i https://iso3166-2-api.vercel.app/api/country_name/Uganda

### Response
    HTTP/2 200 
    content-type: application/json
    date: Sat, 23 Dec 2023 14:17:39 GMT
    server: Vercel
    content-length: 14965

    {"UG":{"UG-101":{...}}}

### Python
```python
import requests

base_url = "https://iso3166-2-api.vercel.app/api/country_name/"
input_name = "Tajikistan" #Seychelles, Uganda

request_url = base_url + input_name

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

Get all ISO 3166-2 subdivision codes for all countries 
------------------------------------------------------

### Request
`GET /api/list_subdivisions/Tikistan`

    curl -i https://iso3166-2-api.vercel.app/api/list_subdivisions

### Response
    HTTP/2 200 
    content-type: application/json
    date: Sat, 03 Feb 2024 15:03:11 GMT
    server: Vercel
    content-length: 

    {"AD":{"AD-02","AD-03"...}}
    
### Python
```python
import requests

request_url = "https://iso3166-2-api.vercel.app/api/list_subdivisions/"

all_request = requests.get(request_url)
all_request.json() 
```

### Javascript
```javascript
function getData() {
  const response = 
    await fetch(`https://iso3166-updates.com/api/list_subdivisions`); 
  const data = await response.json()
}

// Begin accessing JSON data here
var data = JSON.parse(this.response)
```

[Back to top](#TOP)

[demo]: https://colab.research.google.com/drive/1btfEx23bgWdkUPiwdwlDqKkmUp1S-_7U?usp=sharing