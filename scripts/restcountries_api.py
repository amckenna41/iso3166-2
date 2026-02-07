import requests
from typing import Optional, Dict, Any, List

RESTCOUNTRIES_BASE_URL = "https://restcountries.com/v3.1/"
USER_AGENT_HEADER = {"User-Agent": "iso3166-2-exporter/1.0"}

def get_rest_countries_country_data(alpha2: str, fields: Optional[List[str]] = None, proxy: Optional[dict] = None) -> Optional[Dict[str, Any]]:
    """
    Fetches country data from RestCountries API for a given alpha-2 code.
    Optionally filters for specific fields.

    Parameters
    ==========
    :alpha2: str
        the ISO 3166-1 alpha-2 country code.
    :fields: Optional[List[str]]
        list of specific fields to return. If None, returns all data.
    :proxy: Optional[dict]
        optional proxy settings for the requests.
    
    Returns
    =======
    :Optional[Dict[str, Any]]
        a dictionary of country data or None if not found/error.
    """
    url = f"{RESTCOUNTRIES_BASE_URL}alpha/{alpha2}"
    try:
        resp = requests.get(url, headers=USER_AGENT_HEADER, proxies=proxy, timeout=12)
        resp.raise_for_status()
        data = resp.json()
        if not data or not isinstance(data, list):
            return None
        country = data[0]
        if fields:
            # Only return requested fields
            return {field: country.get(field) for field in fields}
        return country
    except Exception as e:
        print(f"Error fetching RestCountries data for {alpha2} ({url}): {e}")
        return None

def get_supported_fields() -> List[str]:
    """
    Returns the list of supported fields/attributes from RestCountries API.

    Parameters
    ==========
    None
    
    Returns
    =======
    :List[str]
        list of supported field names.
    """
    return [
        "idd", "carSigns", "carSide", "continents", "currencies", "languages",
        "postalCode", "region", "startOfWeek", "subregion", "timezones", "tld", "unMember"
    ]