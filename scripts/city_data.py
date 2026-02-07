import requests
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
from scripts.utils import convert_to_alpha2

BASE_URL = "https://api.countrystatecity.in/v1/countries/"
USER_AGENT_HEADER = {"User-Agent": "iso3166-2-exporter/1.0"}

def get_cities_for_subdivision(alpha2: str, subdivision_code: str, api_key: Optional[str] = None, proxy: Optional[dict] = None) -> List[Dict]:
    """
    Fetches a list of cities for a given country (alpha2) and subdivision code using the Country State City API.
    Returns a list of city dictionaries with name, latitude, and longitude.

    Parameters
    ==========
    :alpha2: str
        the ISO 3166-1 alpha-2 country code.
    :subdivision_code: str
        the ISO 3166-2 subdivision code (e.g., "US-CA" for California, USA).
    :api_key: str
        the API key for authenticating with the Country State City API.
    :proxy: Optional[dict]
        optional proxy settings for the requests.
    """
    #validate country code input, raise error if invalid
    alpha2 = convert_to_alpha2(alpha2)

    #extract subdivision part from full code
    subd_code = subdivision_code.split('-')[1] if '-' in subdivision_code else subdivision_code

    #construct the API request URL & headers
    url = f"{BASE_URL}{alpha2}/states/{subd_code}/cities"
    headers = USER_AGENT_HEADER.copy()

    # If api_key not provided, try to get from .env file first, then environment
    if not api_key:
        # Load from .env file if it exists
        load_dotenv()
        api_key = os.getenv("COUNTRY_STATE_CITY_API_KEY")
        if not api_key:
            raise ValueError("API key for Country State City API not provided and not found in .env file or environment variable COUNTRY_STATE_CITY_API_KEY.")
    headers["X-CSCAPI-KEY"] = api_key

    #make the API request, handle errors, and parse response
    try:
        resp = requests.get(url, headers=headers, proxies=proxy, timeout=15)
        resp.raise_for_status()
        cities = resp.json()
        return [
            {
                "name": city.get("name"),
                "latLng": [city.get("latitude"), city.get("longitude")]
            }
            for city in cities
        ]
    except Exception as e:
        print(f"Error fetching cities for {alpha2}-{subd_code}: {e}")
        return []