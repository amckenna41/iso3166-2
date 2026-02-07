import requests
from typing import Optional, Dict, Any, List
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import json
import math
import flag
import pandas as pd
from statistics import mean, median
import os
from pycountry import countries
from tqdm import tqdm
from wikidata.client import Client
from iso3166_2 import Subdivisions
from scripts.utils import convert_to_alpha2

# Nominatim API endpoints
NOMINATIM_API_URL = 'https://nominatim.openstreetmap.org/search'
NOMINATIM_REVERSE_API_URL = 'https://nominatim.openstreetmap.org/reverse'

class Geo:
    """
    A comprehensive utility class for getting a verbose collection of geographical data for ISO 3166-2 subdivisions.
    
    The Geo class provides tools to fetch and manage geographical data for the ISO 3166-2 subdivisions
    dataset. It uses several data sources including the OpenStreetMap (OSM) Nominatim API as well as
    Wikidata. The main attributes per subdivision that the class computes is:

    - latLng: Latitude/Longitude coordinates
    - boundingBox: Bounding box coordinates, rectangular area, defined by minimum and maximum coordinates 
    (like latitude/longitude or X/Y)
    - geojson: Full GeoJSON geometry defining the subdivision boundary
    - neighbours: List of neighboring subdivisions based on bounding box overlap
    - perimeter: Calculated perimeter distance in kilometers

    All of the above attributes have previously been exported via the fetch_all_country_geo_data() function,
    stored in the iso3166_2_resources/geo_cache.csv file, which is imported by default when importing the class
    to save on API calls. Another cache file was exported called iso3166_2_resources/geo_cache_min.csv which only
    contains the latLng data which is currently incorporated into the iso3166-2 dataset. 

    The class accepts the ISO 3166-1 country code as an optional parameter during initialization. If provided, 
    the instance is limited to that country's subdivisions. 

    Parameters
    ==========
    country_code : str, optional
        ISO 3166-1 alpha-2 (e.g., 'US'), alpha-3 (e.g., 'USA'), or numeric country code.
        If provided, the instance is limited to that country's subdivisions. If None, 
        the instance can query any country but without country-specific caching.
        Default is None.
    proxy : dict, optional
        Proxy configuration for HTTP requests. Should be formatted as a dict with 'http' 
        and/or 'https' keys mapping to proxy URLs. Example: 
        {'http': 'http://proxy.example.com:8080', 'https': 'https://proxy.example.com:8080'}
        Default is None (no proxy).
    verbose : bool, optional
        Enable verbose logging output to console. When True, provides detailed information
        about API calls, cache operations, and data processing progress. Default is False.
    use_retry : bool, optional
        Enable automatic retry mechanism for failed API requests. When True, failed requests
        will be retried with exponential backoff. Default is True.
    geo_cache_path : str, optional
        File path to a custom geo cache CSV file. If None, uses the default cache path at
        'iso3166_2_resources/geo_cache.csv'. Useful for maintaining separate caches or 
        testing. Default is None.
    export_to_cache : bool, optional
        Automatically export newly-fetched data to the cache file. When True, data retrieved
        from API calls is saved to cache for future use. Default is True.
    use_cache : bool, optional
        Use existing cached data when available before making API calls. When True, checks
        cache first and only queries the API for missing data. Default is True.
    
    Attributes
    ===========
    country_code : str or None
        The normalized ISO 3166-1 alpha-2 country code (if set during initialization).
    country_name : str or None
        The English name of the country (if country_code was provided).
    subdivisions : Subdivisions or None
        Instance of the Subdivisions class for accessing ISO 3166-2 data (if country_code was provided).
    subdivision_codes : list or None
        List of all ISO 3166-2 subdivision codes for the country (if country_code was provided).
    geo_cache : pd.DataFrame
        Pandas DataFrame containing the current cache with columns:
        - subdivisionCode: ISO 3166-2 code (e.g., 'US-CA')
        - latLng: Latitude and longitude as "lat,lon" string
        - bounding_box: Bounding box coordinates [minlat, maxlat, minlon, maxlon]
        - geojson: GeoJSON geometry object (Polygon or MultiPolygon)
        - perimeter: Calculated perimeter in kilometers
        - neighbours: List of neighboring subdivision codes
    
    Methods
    =======
    get_lat_lng(country_code=None, verbose=False, export=True) -> Dict[str, str]
        Retrieve latitude/longitude coordinates for subdivisions.
    get_bounding_box(country_code=None, verbose=False, export=True) -> Dict[str, List[float]]
        Retrieve bounding box coordinates for subdivisions.
    get_geojson(country_code=None, verbose=False, export=True, export_to_geojson=False) -> Dict[str, Dict]
        Retrieve GeoJSON boundary geometries for subdivisions.
    get_perimeter(country_code=None, verbose=False, export=True) -> Dict[str, float]
        Calculate and retrieve perimeter distances for subdivisions in kilometers.
    get_neighbours(country_code=None, verbose=False, export=True) -> Dict[str, List[str]]
        Identify neighboring subdivisions based on bounding box overlap.
    get_all(country_code=None, verbose=False, export=True, skip_geojson=True) -> Dict[str, Dict[str, Any]]
        Retrieve all available geographical data (coordinates, bbox, GeoJSON, perimeter, neighbours).
    get_statistics(geo_cache_filepath=None) -> Dict[str, Any]
        Generate comprehensive statistics about the cache including data completeness and coverage.
    _clear_cache() -> None
        Clear all cached data from memory and file.
    _load_cache() -> Optional[pd.DataFrame]
        Load the geo cache from disk or initialize an empty cache.
    _parse_country_codes(country_code=None) -> List[str]
        Normalize and parse comma-separated country codes into a list.
    _fetch_subdivision_data(subdivision_code, get_geojson=False) -> Optional[Dict[str, Any]]
        Fetch subdivision data from Nominatim and optionally include GeoJSON.
    _export_cache(custom_cache_export_path=None, verbose=False) -> None
        Export the in-memory cache to disk.
    _export_geojsons_to_file(geojsons, country_code) -> None
        Export GeoJSON FeatureCollections to a .geojson file.
    __repr__() -> str
        Return detailed representation of Geo instance.
    __str__() -> str
        Return user-friendly string representation of Geo instance.
    __len__() -> int
        Return the number of cached entries.
    
    Usage Examples
    ==============
    from geo import Geo
    
    # Create instance for a specific country
    geo_us = Geo("US")
    
    # Get coordinates for all US subdivisions
    coordinates = geo_us.get_lat_lng() # '37.2695,-119.3064'
    
    # Get all geographical data for a subset of countries
    geo_multi = Geo()
    all_data = geo_multi.get_all(country_code="US,CA,MX")
    
    # Get subdivision boundaries
    geojsons = geo_us.get_geojson(export_to_geojson=True)
    
    # Calculate perimeters
    perimeters = geo_us.get_perimeter()
    
    # Find neighboring subdivisions
    neighbours = geo_us.get_neighbours()
    
    # Check cache statistics
    stats = geo_us.get_statistics()
    
    # Get coordinates with custom cache path
    geo_custom = Geo("GB", geo_cache_path="/path/to/custom_cache.csv")
    uk_coords = geo_custom.get_lat_lng()
    
    References
    ==========
    [1]: OpenStreetMap - https://www.openstreetmap.org/
    [2]: Wikidata Query Service - https://query.wikidata.org/
    """

    def __init__(self, country_code: Optional[str] = None, proxy: Optional[dict] = None, verbose: bool = False,
                 use_retry: bool = True, geo_cache_path: Optional[str] = None, export_to_cache: bool = True, 
                 use_cache: bool = True):
        """Initialize Geo instance."""
        self.proxy = proxy
        self.verbose = verbose
        self.use_retry = use_retry
        self.geo_cache_path = geo_cache_path
        self.export_to_cache = export_to_cache
        self.use_cache = use_cache
        # Validate and set country code
        if country_code is not None:
            self.country_code = convert_to_alpha2(country_code)
            try:
                self.country_name = countries.get(alpha_2=self.country_code).name
            except (AttributeError, KeyError):
                self.country_name = None
            # create Subdivisions instance for the country, and get subdivision codes via country code
            self.subdivisions = Subdivisions()
            self.subdivision_codes = self.subdivisions.subdivision_codes(self.country_code)
        else:
            self.country_code = None
            self.country_name = None
            self.subdivisions = None
            self.subdivision_codes = None

        # Load or initialize cache
        self.geo_cache = self._load_cache()

    def get_lat_lng(self, country_code: Optional[str] = None, verbose: bool = False, export: bool = True) -> Dict[str, str]:
        """
        Get latLng for each ISO 3166-2 subdivision in the country or countries. Checks cache first, then fetches from 
        Nominatim API for missing subdivisions.
        
        Parameters
        ==========
        country_code : str, optional
            ISO 3166-1 alpha-2 or alpha-3 country code, or comma-separated list of codes (e.g., 'AD' or 'AD,DE,FR'). Default is None.
        verbose : bool, optional
            Enable verbose logging. Default is False.
        export : bool, optional
            Export newly-fetched data to cache. Default is True.
        
        Returns
        =======
        Dict[str, str]
            Dictionary mapping subdivision codes to latLng strings "lat,lon".
            Example: {'US-CA': '37.2695,-119.3064', 'US-DE': '39.3185,-75.5243', 'AD-01': '42.5000,1.5000'}
        
        Raises
        ======
        ValueError
            If country_code is not provided and instance was not initialized with a country code.
        """
        # Parse comma-separated country codes
        country_codes = self._parse_country_codes(country_code)
        
        # If multiple countries, process each and merge results
        if len(country_codes) > 1:
            latLngs = {}
            for cc in country_codes:
                result = self.get_lat_lng(country_code=cc, verbose=verbose, export=export)
                latLngs.update(result)
            if export:
                self._export_cache(verbose=verbose)
            return latLngs
        
        # Single country processing
        effective_country_code = country_codes[0]
        
        # Get subdivision codes - reuse self.subdivisions if country matches, otherwise create temp instance
        if country_code is not None and convert_to_alpha2(country_code if ',' not in str(country_code) else country_code.split(',')[0]) != self.country_code:
            subdivisions = Subdivisions()
            subdivision_codes = subdivisions.subdivision_codes(effective_country_code)
            try:
                # Get country name
                country_name = countries.get(alpha_2=effective_country_code).name
            except (AttributeError, KeyError):
                country_name = 'Unknown'
        else:
            subdivision_codes = self.subdivision_codes
            country_name = self.country_name
        
        # Verbose logging
        if verbose:
            flag_emoji = flag.flag(effective_country_code) if effective_country_code != "XK" else ""
            print(f"[START] Fetching latLngs for {len(subdivision_codes)} subdivisions in {country_name} {effective_country_code} {flag_emoji}...")
        
        # Wikidata fallback mapping for subdivisions without Nominatim coverage
        wikidata_fallback = {
            'BQ-BO': 'Q25396', 'BQ-SA': 'Q25528', 'BQ-SE': 'Q26180', 'ET-SN': 'Q203193',
            'MC-MU': 'Q13378485', 'MC-PH': 'Q7230673', 'MC-SP': 'Q13378480', 'MC-SR': 'Q55089',
            'UM-67': 'Q131008', 'UM-71': 'Q47863', 'UM-76': 'Q31968354', 'UM-79': 'Q43296',
            'UM-81': 'Q46879', 'UM-84': 'Q131305', 'UM-86': 'Q62218', 'UM-89': 'Q130895', 'UM-95': 'Q123076',
            'WF-AL': 'Q2734700', 'WF-SG': 'Q2554877', 'WF-UV': 'Q7903676'
        }
        
        latLngs = {}
        newly_fetched_codes = set()
        
        # Iterate over subdivision codes, checking cache and fetching as needed
        for subdivision_code in subdivision_codes:
            latLng = None
            
            # Check cache first
            if self.use_cache and self.geo_cache is not None and not self.geo_cache.empty:
                cached_row = self.geo_cache[self.geo_cache['subdivisionCode'] == subdivision_code]
                if not cached_row.empty and 'latLng' in self.geo_cache.columns:
                    cached_latLng = cached_row['latLng'].values[0]
                    if cached_latLng and pd.notna(cached_latLng) and str(cached_latLng).strip():
                        latLng = str(cached_latLng)
                        if verbose:
                            print(f"  [{subdivision_code}] LatLng found in cache: {latLng}")
            
            # Fetch from Nominatim API or Wikidata fallback if not in cache
            if latLng is None:
                data = None
                
                # Try Wikidata fallback for problematic subdivisions
                if subdivision_code in wikidata_fallback:
                    try:
                        client = Client()
                        entity = client.get(wikidata_fallback[subdivision_code], load=True)
                        # Extract coordinates from Wikidata
                        if 'claims' in entity.data and 'P625' in entity.data['claims']:
                            coords = entity.data['claims']['P625'][0]['mainsnak']['datavalue']['value']
                            data = {'latLng': (float(coords['latitude']), float(coords['longitude']))}
                    except (ImportError, Exception):
                        pass
                
                # Use Nominatim API if Wikidata not available or failed
                if data is None:
                    data = self._fetch_subdivision_data(subdivision_code, get_geojson=False)
                
                # Process fetched data
                if data and data.get('latLng'):
                    lat, lon = data['latLng']
                    latLng = f"{round(lat, 4)},{round(lon, 4)}"
                    newly_fetched_codes.add(subdivision_code)
                    
                    # Verbose logging
                    if verbose:
                        sub_name = self.subdivisions[effective_country_code][subdivision_code].name
                        print(f"  [{subdivision_code}] {sub_name} - Fetched latLng: {latLng}")
                    
                    # Update cache in memory
                    if self.geo_cache is None or self.geo_cache.empty:
                        self.geo_cache = pd.DataFrame(columns=['subdivisionCode', 'latLng', 'boundingBox', 'geojson', 'perimeter', 'neighbours'])
                    else:
                        if 'geojson' in self.geo_cache.columns and self.geo_cache['geojson'].dtype != object:
                            self.geo_cache['geojson'] = self.geo_cache['geojson'].astype('object')
                    
                    # Update or append to cache DataFrame
                    if subdivision_code in self.geo_cache['subdivisionCode'].values:
                        self.geo_cache.loc[self.geo_cache['subdivisionCode'] == subdivision_code, 'latLng'] = latLng
                    # Append new row if not in cache
                    else:
                        new_row = pd.DataFrame({
                            'subdivisionCode': [subdivision_code],
                            'latLng': [latLng],
                            'boundingBox': [None],
                            'geojson': [None],
                            'perimeter': [None]
                        })
                        if self.geo_cache is None or self.geo_cache.empty:
                            self.geo_cache = new_row
                        else:
                            self.geo_cache = pd.concat([self.geo_cache, new_row], ignore_index=True)
            
            # Store result if latLng found
            if latLng:
                latLngs[subdivision_code] = latLng
        
        # Export to cache if requested
        if export and newly_fetched_codes and self.export_to_cache:
            self._export_cache(verbose=verbose)
        
        # Verbose logging
        if verbose:
            successful = len([c for c in latLngs.values() if c])
            print(f"[END] Fetched latLngs for {successful}/{len(subdivision_codes)} subdivisions")
        
        return latLngs

    def get_bounding_box(self, country_code: Optional[str] = None, verbose: bool = False, export: bool = True) -> Dict[str, List[float]]:
        """
        Get bounding box for each ISO 3166-2 subdivision in the country or countries. Checks cache first, then fetches from Nominatim 
        API for missing subdivisions. If no country_code is provided, returns all bounding box data from cache (if available) or 
        fetches from API for all countries.
        
        Parameters
        ==========
        country_code : str, optional
            ISO 3166-1 alpha-2 or alpha-3 country code, or comma-separated list of codes (e.g., 'AD' or 'AD,DE,FR'). 
            If None, returns all available bounding box data. Default is None.
        verbose : bool, optional
            Enable verbose logging. Default is False.
        export : bool, optional
            Export newly-fetched data to cache. Default is True.
        
        Returns
        =======
        Dict[str, List[float]]
            Dictionary mapping subdivision codes to bounding boxes [minlat, maxlat, minlon, maxlon].
            Example: {'US-CA': [32.5, 42.0, -124.5, -114.1], 'AD-01': [42.4, 42.6, 1.4, 1.6]}
        
        Raises
        ======
        ValueError
            If country_code is not provided, instance has no country_code, and cache is not available.
        """
        # If no country_code provided in class or function, try to return all bounding box data from cache or fetch for all countries
        if country_code is None and self.country_code is None:
            # Try to return all bounding box data from cache
            if self.use_cache and self.geo_cache is not None and not self.geo_cache.empty:
                try:
                    if verbose:
                        print(f"[START] Loading ALL bounding boxes from cache...")
                    
                    bounding_boxes = {}
                    for _, row in self.geo_cache.iterrows():
                        if pd.notna(row.get('boundingBox')):
                            try:
                                bbox = json.loads(row['boundingBox']) if isinstance(row['boundingBox'], str) else row['boundingBox']
                                bounding_boxes[row['subdivisionCode']] = bbox
                            except (json.JSONDecodeError, TypeError):
                                pass
                    
                    if verbose:
                        print(f"[END] Loaded {len(bounding_boxes)} bounding boxes from cache for ALL countries/subdivisions")
                    
                    return bounding_boxes
                except Exception as e:
                    if verbose:
                        print(f"Error reading cache: {e}. Proceeding to fetch from API...")
            else:
                print("Cache not available. Fetching bounding box data for ALL countries/subdivisions from API...")
            
            # If cache not available or doesn't exist, fetch for all countries
            # Get all available country codes from Subdivisions
            # all_subdivisions = Subdivisions()
            all_country_codes = [country.alpha_2 for country in countries]
            
            print(f"Fetching bounding boxes for {len(all_country_codes)} countries from API...")
            
            bounding_boxes = {}
            for cc in all_country_codes:
                result = self.get_bounding_box(country_code=cc, verbose=verbose, export=export)
                bounding_boxes.update(result)
            
            # Export to cache if requested
            if export:
                self._export_cache(verbose=verbose)
            
            if verbose:
                print(f"[END] Fetched bounding boxes for {len(bounding_boxes)} total subdivisions across ALL countries")
            
            return bounding_boxes
        
        # Parse comma-separated country codes
        country_codes = self._parse_country_codes(country_code)
        
        # If multiple countries, process each and merge results
        if len(country_codes) > 1:
            bounding_boxes = {}
            for cc in country_codes:
                result = self.get_bounding_box(country_code=cc, verbose=verbose, export=export)
                bounding_boxes.update(result)
            if export:
                self._export_cache(verbose=verbose)
            return bounding_boxes
        
        # Single country processing
        effective_country_code = country_codes[0]
        
        #set subdivision-related function variables
        subdivisions = self.subdivisions
        subdivision_codes = self.subdivision_codes
        country_name = self.country_name

        # Get subdivision codes - reuse self.subdivisions if country matches, otherwise create temp instance
        if country_code is not None and convert_to_alpha2(country_code if ',' not in str(country_code) else country_code.split(',')[0]) != self.country_code:
            subdivisions = Subdivisions(country_code=effective_country_code) #only import subdivision data for current country
            subdivision_codes = subdivisions.subdivision_codes(effective_country_code)
            # Get country name, raise exception if invalid code
            try:
                country_name = countries.get(alpha_2=effective_country_code).name
            except (AttributeError, KeyError):
                country_name = 'Unknown'
        
        if verbose:
            flag_emoji = flag.flag(effective_country_code) if effective_country_code != "XK" else ""
            print(f"[START] Fetching bounding boxes for {len(subdivision_codes)} subdivisions in {country_name} {effective_country_code} {flag_emoji}...")
        
        bounding_boxes = {}
        newly_fetched_codes = set()
        
        # Iterate over subdivision codes, checking cache and fetching as needed
        for subdivision_code in subdivision_codes:
            bbox = None
            
            # Check cache first
            if self.use_cache and self.geo_cache is not None and not self.geo_cache.empty:
                cached_row = self.geo_cache[self.geo_cache['subdivisionCode'] == subdivision_code]
                if not cached_row.empty and 'boundingBox' in self.geo_cache.columns:
                    cached_bbox = cached_row['boundingBox'].values[0]
                    if cached_bbox and pd.notna(cached_bbox):
                        try:
                            bbox = json.loads(cached_bbox) if isinstance(cached_bbox, str) else cached_bbox
                            if verbose:
                                print(f"  [{subdivision_code}] Bounding box found in cache: {bbox}")
                        except (json.JSONDecodeError, TypeError):
                            bbox = None
            
            # Fetch from API if not in cache
            if bbox is None:
                data = self._fetch_subdivision_data(subdivision_code, get_geojson=False)
                if data and data.get('bounding_box'):
                    bbox = data['bounding_box']
                    # Round all 4 values to 4 decimal places [minlat, maxlat, minlon, maxlon]
                    # Convert to float to ensure proper JSON serialization without quotes
                    bbox = [float(round(float(val), 4)) for val in bbox]
                    newly_fetched_codes.add(subdivision_code)
                    
                    if verbose:
                        sub_name = subdivisions[effective_country_code][subdivision_code].name
                        print(f"  [{subdivision_code}] {sub_name} - Fetched bounding box from API: {bbox}")
                    
                    # Update cache in memory
                    if self.geo_cache is None or self.geo_cache.empty:
                        self.geo_cache = pd.DataFrame(columns=['subdivisionCode', 'latLng', 'boundingBox', 'geojson', 'perimeter', 'neighbours'])
                    
                    # Serialize bbox to JSON string for storage
                    bbox_json = json.dumps(bbox) if bbox else None
                    
                    # Update or append to cache DataFrame
                    if subdivision_code in self.geo_cache['subdivisionCode'].values:
                        self.geo_cache.loc[self.geo_cache['subdivisionCode'] == subdivision_code, 'boundingBox'] = bbox_json
                    else:
                        # Append new row if not in cache
                        new_row = pd.DataFrame({
                            'subdivisionCode': [subdivision_code],
                            'latLng': [None],
                            'boundingBox': [bbox_json],
                            'geojson': [None],
                            'perimeter': [None],
                            'neighbours': [None]
                        })
                        self.geo_cache = pd.concat([self.geo_cache, new_row], ignore_index=True)
                else:
                    if verbose:
                        sub_name = subdivisions[effective_country_code][subdivision_code].name
                        print(f"  [{subdivision_code}] {sub_name} - Failed to fetch bounding box from API")
            
            # Store result if bbox found
            if bbox:
                bounding_boxes[subdivision_code] = bbox
        
        # Export newly fetched bounding box data to cache if enabled
        if newly_fetched_codes and self.export_to_cache:
            self._export_cache(verbose=verbose)
        
        if verbose:
            successful = len([b for b in bounding_boxes.values() if b])
            print(f"[END] Fetched bounding boxes for {successful}/{len(subdivision_codes)} subdivisions")
        
        return bounding_boxes

    def get_geojson(self, country_code: Optional[str] = None, verbose: bool = False, export: bool = True, export_to_geojson: bool = False) -> Dict[str, Dict]:
        """
        Get GeoJSON for each ISO 3166-2 subdivision in the country or countries. Checks cache first, then fetches from 
        Nominatim API for missing subdivisions.
        
        Parameters
        ==========
        country_code : str, optional
            ISO 3166-1 alpha-2 or alpha-3 country code, or comma-separated list of codes (e.g., 'AD' or 'AD,DE,FR'). Default is None.
        verbose : bool, optional
            Enable verbose logging. Default is False.
        export : bool, optional
            Export newly-fetched data to cache. Default is True.
        export_to_geojson : bool, optional
            Export to GeoJSON file. Default is False.
        
        Returns
        =======
        Dict[str, Dict]
            Dictionary mapping subdivision codes to GeoJSON Feature dictionaries.
            Each GeoJSON contains full boundary geometry (Polygon or MultiPolygon).
        
        Raises
        ======
        ValueError
            If country_code is not provided and instance was not initialized with a country code.
        """
        # Parse comma-separated country codes
        country_codes = self._parse_country_codes(country_code)
        
        # If multiple countries, process each and merge results, then export if requested
        if len(country_codes) > 1:
            geojsons = {}
            for cc in country_codes:
                result = self.get_geojson(country_code=cc, verbose=verbose, export=export, export_to_geojson=export_to_geojson)
                geojsons.update(result)
            if export:
                self._export_cache(verbose=verbose)
            if export_to_geojson:
                # Export all geojsons to file for first country code
                self._export_geojsons_to_file(geojsons, country_codes[0])
            return geojsons
        
        # Single country processing
        effective_country_code = country_codes[0]
        
        # Get subdivision codes - reuse self.subdivisions if country matches, otherwise create temp instance
        if country_code is not None and convert_to_alpha2(country_code if ',' not in str(country_code) else country_code.split(',')[0]) != self.country_code:
            subdivisions = Subdivisions()
            subdivision_codes = subdivisions.subdivision_codes(effective_country_code)
            try:
                country_name = countries.get(alpha_2=effective_country_code).name
            except (AttributeError, KeyError):
                country_name = 'Unknown'
        else:
            subdivision_codes = self.subdivision_codes
            country_name = self.country_name
        
        # Verbose logging
        if verbose:
            flag_emoji = flag.flag(effective_country_code) if effective_country_code != "XK" else ""
            print(f"[START] Fetching GeoJSON for {len(subdivision_codes)} subdivisions in {country_name} {effective_country_code} {flag_emoji}...")
        
        geojsons = {}
        newly_fetched_codes = set()
        
        # Initialize geojsons dict with all subdivision codes (set to empty dict initially)
        for subdivision_code in subdivision_codes:
            geojsons[subdivision_code] = {}
        
        # Iterate over subdivision codes, checking cache and fetching as needed
        for subdivision_code in subdivision_codes:
            geojson_data = None
            
            # Check cache first
            if self.use_cache and self.geo_cache is not None and not self.geo_cache.empty:
                cached_row = self.geo_cache[self.geo_cache['subdivisionCode'] == subdivision_code]
                if not cached_row.empty and 'geojson' in self.geo_cache.columns:
                    cached_geojson = cached_row['geojson'].values[0]
                    if cached_geojson and pd.notna(cached_geojson):
                        try:
                            geojson_data = json.loads(cached_geojson)
                            if verbose:
                                print(f"  [{subdivision_code}] GeoJSON found in cache")
                        except (json.JSONDecodeError, TypeError):
                            geojson_data = None
            
            # Fetch from API if not in cache, and update cache
            if geojson_data is None:
                data = self._fetch_subdivision_data(subdivision_code, get_geojson=True)
                if data and data.get('geojson'):
                    geojson_data = data['geojson']
                    newly_fetched_codes.add(subdivision_code)
                    
                    # Verbose logging
                    if verbose:
                        sub_name = self.subdivisions[effective_country_code][subdivision_code].name
                        geom_type = geojson_data.get('type', 'Unknown') if geojson_data else 'None'
                        print(f"  [{subdivision_code}] {sub_name} - Fetched GeoJSON from API (type: {geom_type})")
                    
                    # Update cache in memory
                    if self.geo_cache is None or self.geo_cache.empty:
                        self.geo_cache = pd.DataFrame(columns=['subdivisionCode', 'latLng', 'boundingBox', 'geojson', 'perimeter', 'neighbours'])
                    
                    # Serialize geojson to JSON string for storage
                    geojson_json = json.dumps(geojson_data)
                    
                    # Update or append to cache DataFrame
                    if subdivision_code in self.geo_cache['subdivisionCode'].values:
                        self.geo_cache.loc[self.geo_cache['subdivisionCode'] == subdivision_code, 'geojson'] = geojson_json
                    else:
                        # Append new row if not in cache, with other fields as None
                        new_row = pd.DataFrame({
                            'subdivisionCode': [subdivision_code],
                            'latLng': [None],
                            'boundingBox': [None],
                            'geojson': [geojson_json],
                            'perimeter': [None],
                            'neighbours': [None]
                        })
                        self.geo_cache = pd.concat([self.geo_cache, new_row], ignore_index=True)
                else:
                    # Verbose logging for failure
                    if verbose:
                        sub_name = self.subdivisions[effective_country_code][subdivision_code].name
                        print(f"  [{subdivision_code}] {sub_name} - Failed to fetch GeoJSON from API")
            
            if geojson_data:
                # Wrap geometry in FeatureCollection with Feature containing subdivision code
                wrapped_geojson = {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "properties": {
                                "name": subdivision_code
                            },
                            "geometry": geojson_data
                        }
                    ]
                }
                geojsons[subdivision_code] = wrapped_geojson
        
        # Export to cache if requested
        if export and newly_fetched_codes and self.export_to_cache:
            self._export_cache(verbose=verbose)
        
        # Verbose logging
        if verbose:
            successful = len([g for g in geojsons.values() if g])
            print(f"[END] Fetched GeoJSON for {successful}/{len(subdivision_codes)} subdivisions")
        
        # Export to GeoJSON file if requested
        if export_to_geojson:
            self._export_geojsons_to_file(geojsons, effective_country_code)
        
        return geojsons

    def get_perimeter(self, country_code: Optional[str] = None, verbose: bool = False, export: bool = True) -> Dict[str, float]:
        """
        Calculate the perimeter of each ISO 3166-2 subdivision in the country or countries using GeoJSON 
        geometry. The perimeter is calculated using the haversine formula to compute geodesic distances
        between consecutive coordinate points in the polygon geometry.
        
        Parameters
        ==========
        country_code : str, optional
            ISO 3166-1 alpha-2 or alpha-3 country code, or comma-separated list of codes (e.g., 'AD' or 'AD,DE,FR'). Default is None.
        verbose : bool, optional
            Enable verbose logging. Default is False.
        export : bool, optional
            Export newly-fetched data to cache. Default is True.
        
        Returns
        =======
        Dict[str, float]
            Dictionary mapping subdivision codes to perimeter values in kilometers.
            Example: {'US-CA': 12456.78, 'US-DE': 3421.23, 'AD-01': 156.45}
        
        Raises
        ======
        ValueError
            If country_code is not provided and instance was not initialized with a country code.
        """
        # If no country_code provided in class or function, try to return all perimeter data from cache or fetch for all countries
        if country_code is None and self.country_code is None:
            # Try to return all perimeter data from cache
            if self.use_cache and self.geo_cache is not None and not self.geo_cache.empty:
                try:
                    if verbose:
                        print(f"[START] Loading ALL perimeters from cache...")
                    
                    perimeters = {}
                    for _, row in self.geo_cache.iterrows():
                        if pd.notna(row.get('perimeter')):
                            try:
                                perimeter = float(row['perimeter'])
                                perimeters[row['subdivisionCode']] = perimeter
                            except (ValueError, TypeError):
                                pass
                    
                    if verbose:
                        print(f"[END] Loaded {len(perimeters)} perimeters from cache for ALL countries/subdivisions")
                    
                    return perimeters
                except Exception as e:
                    if verbose:
                        print(f"Error reading cache: {e}. Proceeding to fetch from API...")
            else:
                print("Cache not available. Fetching perimeter data for ALL countries/subdivisions from API...")
            
            # If cache not available or doesn't exist, fetch for all countries
            # Get all available country codes from Subdivisions
            # all_subdivisions = Subdivisions()
            all_country_codes = [country.alpha_2 for country in countries]
            
            print(f"Fetching perimeters for {len(all_country_codes)} countries from API...")
            
            perimeters = {}
            for cc in all_country_codes:
                result = self.get_perimeter(country_code=cc, verbose=verbose, export=export)
                perimeters.update(result)
            
            # Export to cache if requested
            if export:
                self._export_cache(verbose=verbose)
            
            if verbose:
                print(f"[END] Fetched perimeters for {len(perimeters)} total subdivisions across ALL countries")
            
            return perimeters

        # Parse comma-separated country codes
        country_codes = self._parse_country_codes(country_code)
        
        # If multiple countries, process each and merge results
        if len(country_codes) > 1:
            perimeters = {}
            for cc in country_codes:
                result = self.get_perimeter(country_code=cc, verbose=verbose, export=export)
                perimeters.update(result)
            if export:
                self._export_cache(verbose=verbose)
            return perimeters
        
        # Single country processing
        effective_country_code = country_codes[0]
        
        #set subdivision-related function variables
        subdivisions = self.subdivisions
        subdivision_codes = self.subdivision_codes
        country_name = self.country_name

        # Get subdivision codes - reuse self.subdivisions if country matches, otherwise create temp instance
        if country_code is not None and convert_to_alpha2(country_code if ',' not in str(country_code) else country_code.split(',')[0]) != self.country_code:
            subdivisions = Subdivisions(country_code=effective_country_code) #only import subdivision data for current country
            subdivision_codes = subdivisions.subdivision_codes(effective_country_code)
            # Get country name, raise exception if invalid code
            try:
                country_name = countries.get(alpha_2=effective_country_code).name
            except (AttributeError, KeyError):
                country_name = 'Unknown'
        
        if verbose:
            flag_emoji = flag.flag(effective_country_code) if effective_country_code != "XK" else ""
            print(f"[START] Fetching perimeters for {len(subdivision_codes)} subdivisions in {country_name} ({effective_country_code}) {flag_emoji}...")

        def calculate_perimeter(geojson_data):
            """ Calculate perimeter from GeoJSON geometry using haversine formula. """
            # Validate GeoJSON structure
            if not geojson_data or 'type' not in geojson_data:
                return None
            
            def ring_perimeter(ring):
                """ Calculate perimeter of a single linear ring. """
                # Ensure ring is closed
                if len(ring) < 2:
                    return 0.0
                
                R = 6371  # Earth radius in kilometers
                perimeter = 0.0
                
                # Iterate over coordinate pairs, summing distances
                for i in range(len(ring) - 1):
                    lon1, lat1 = ring[i]
                    lon2, lat2 = ring[i + 1]
                    
                    # Haversine distance calculation
                    lat1_rad = math.radians(lat1)
                    lat2_rad = math.radians(lat2)
                    delta_lat = math.radians(lat2 - lat1)
                    delta_lon = math.radians(lon2 - lon1)
                    
                    # Haversine formula, computing distance
                    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
                    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                    perimeter += R * c
                
                return perimeter
            
            # Handle Polygon and MultiPolygon geometries
            total = 0.0
            geom_type = geojson_data.get('type')
            coordinates = geojson_data.get('coordinates', [])
            
            # Calculate perimeter based on geometry type, summing outer rings
            if geom_type == 'Polygon' and coordinates:
                total += ring_perimeter(coordinates[0])
            elif geom_type == 'MultiPolygon':
                for polygon_coords in coordinates:
                    if polygon_coords:
                        total += ring_perimeter(polygon_coords[0])
            
            return total if total > 0 else None
        
        perimeters = {}
        newly_fetched_codes = set()
        
        # Iterate over subdivision codes, checking cache and fetching as needed
        for subdivision_code in subdivision_codes:
            perimeter_km = None
            
            # Check cache first
            if self.use_cache and self.geo_cache is not None and not self.geo_cache.empty:
                cached_row = self.geo_cache[self.geo_cache['subdivisionCode'] == subdivision_code]
                if not cached_row.empty and 'perimeter' in self.geo_cache.columns:
                    cached_perimeter = cached_row['perimeter'].values[0]
                    if cached_perimeter and pd.notna(cached_perimeter):
                        try:
                            perimeter_km = float(cached_perimeter)
                            if verbose:
                                print(f"  [{subdivision_code}] Perimeter found in cache: {perimeter_km} km")
                        except (ValueError, TypeError):
                            perimeter_km = None
            
            # Fetch from API if not in cache
            if perimeter_km is None:
                data = self._fetch_subdivision_data(subdivision_code, get_geojson=True)
                if data and data.get('geojson'):
                    geojson_data = data['geojson']
                    perimeter_km = calculate_perimeter(geojson_data)
                    newly_fetched_codes.add(subdivision_code)
                    
                    if verbose:
                        sub_name = subdivisions[effective_country_code][subdivision_code].name
                        if perimeter_km is not None:
                            print(f"  [{subdivision_code}] {sub_name} - Fetched perimeter from API: {perimeter_km:.2f} km")
                        else:
                            api_url = f"{NOMINATIM_API_URL}?q={subdivision_code}&countrycode={subdivision_code.split('-')[0].lower()}&format=jsonv2&polygon_geojson=1&extratags=1&limit=1"
                            print(f"  [{subdivision_code}] - Failed to calculate perimeter. API URL: {api_url}")
                    
                    # Update cache in memory
                    if self.geo_cache is None or self.geo_cache.empty:
                        self.geo_cache = pd.DataFrame(columns=['subdivisionCode', 'latLng', 'boundingBox', 'geojson', 'perimeter', 'neighbours'])
                    
                    # Round perimeter to 2 decimal places for storage
                    perimeter_rounded = round(perimeter_km, 2) if perimeter_km is not None else None
                    
                    # Update or append to cache DataFrame
                    if subdivision_code in self.geo_cache['subdivisionCode'].values:
                        self.geo_cache.loc[self.geo_cache['subdivisionCode'] == subdivision_code, 'perimeter'] = perimeter_rounded
                    else:
                        # Append new row if not in cache
                        new_row = pd.DataFrame({
                            'subdivisionCode': [subdivision_code],
                            'latLng': [None],
                            'boundingBox': [None],
                            'geojson': [None],
                            'perimeter': [perimeter_rounded],
                            'neighbours': [None]
                        })
                        self.geo_cache = pd.concat([self.geo_cache, new_row], ignore_index=True)
                else:
                    if verbose:
                        sub_name = subdivisions[effective_country_code][subdivision_code].name
                        print(f"  [{subdivision_code}] {sub_name} - Failed to fetch GeoJSON from API")
            
            # Store result if perimeter found
            if perimeter_km is not None:
                perimeters[subdivision_code] = round(perimeter_km, 2)
        
        # Export newly fetched perimeter data to cache if enabled
        if newly_fetched_codes and self.export_to_cache:
            self._export_cache(verbose=verbose)
        
        if verbose:
            successful = len([p for p in perimeters.values() if p])
            print(f"[END] Fetched perimeters for {successful}/{len(subdivision_codes)} subdivisions\n")
        
        return perimeters

    def get_neighbours(self, country_code: Optional[str] = None, verbose: bool = False, export: bool = True) -> Dict[str, List[str]]:
        """
        Get bordering subdivisions for each subdivision in the country or countries. Uses bounding box overlap 
        as a simple proxy for adjacency. Subdivisions are considered neighbors if their bounding boxes overlap 
        or touch. Checks cache first for bounding box data before making API calls.
        
        Parameters
        ==========
        country_code : str, optional
            ISO 3166-1 alpha-2 or alpha-3 country code, or comma-separated list of codes (e.g., 'AD' or 'AD,DE,FR'). 
            If provided, only neighbors within those countries will be returned. Default is None (uses initialized country code).
        verbose : bool, optional
            Enable verbose logging. Default is False.
        export : bool, optional
            Export newly-fetched bounding box data to cache. Default is True.
        
        Returns
        =======
        Dict[str, List[str]]
            Dictionary mapping each subdivision code to a list of its neighboring subdivision codes.
            Example: {'US-CA': ['US-NV', 'US-OR', 'US-AZ'], 'US-NV': ['US-CA', 'US-UT', ...], 'AD-01': [...], ...}
        
        Raises
        ======
        ValueError
            If country_code is not provided and instance was not initialized with a country code.
        """
        # If no country_code provided in class or function, try to return all neighbour data from cache or fetch for all countries
        if country_code is None and self.country_code is None:
            # Try to return all neighbour data from cache
            if self.use_cache and self.geo_cache is not None and not self.geo_cache.empty:
                try:
                    if verbose:
                        print(f"[START] Loading ALL neighbours from cache...")
                    
                    neighbours = {}
                    for _, row in self.geo_cache.iterrows():
                        if pd.notna(row.get('neighbours')):
                            try:
                                neighbour = float(row['neighbours'])
                                neighbours[row['subdivisionCode']] = neighbour
                            except (ValueError, TypeError):
                                pass
                    
                    if verbose:
                        print(f"[END] Loaded {len(neighbours)} neighbours from cache for ALL countries/subdivisions")
                    
                    return neighbours
                except Exception as e:
                    if verbose:
                        print(f"Error reading cache: {e}. Proceeding to fetch from API...")
            else:
                print("Cache not available. Fetching neighbour data for ALL countries/subdivisions from API...")
            
            # If cache not available or doesn't exist, fetch for all countries
            # Get all available country codes from Subdivisions
            # all_subdivisions = Subdivisions()
            all_country_codes = [country.alpha_2 for country in countries]
            
            print(f"Fetching neighbours for {len(all_country_codes)} countries from API...")
            
            neighbours = {}
            for cc in all_country_codes:
                result = self.get_neighbours(country_code=cc, verbose=verbose, export=export)
                neighbours.update(result)
            
            # Export to cache if requested
            if export:
                self._export_cache(verbose=verbose)
            
            if verbose:
                print(f"[END] Fetched neighbours for {len(neighbours)} total subdivisions across ALL countries")
            
            return neighbours

        # Parse comma-separated country codes
        country_codes = self._parse_country_codes(country_code)
        
        # If multiple countries, process each and merge results
        if len(country_codes) > 1:
            neighbours = {}
            for cc in tqdm(country_codes, desc="Processing neighbours data for countries"):
                result = self.get_neighbours(country_code=cc, verbose=verbose, export=export)
                neighbours.update(result)
            if export:
                self._export_cache(verbose=verbose)
            return neighbours
        
        # Single country processing
        effective_country_code = country_codes[0]
        
        #set subdivision-related function variables
        subdivisions = self.subdivisions
        subdivision_codes = self.subdivision_codes
        country_name = self.country_name

        # Get subdivision codes - reuse self.subdivisions if country matches, otherwise create temp instance
        if country_code is not None and convert_to_alpha2(country_code if ',' not in str(country_code) else country_code.split(',')[0]) != self.country_code:
            subdivisions = Subdivisions(country_code=effective_country_code) #only import subdivision data for current country
            subdivision_codes = subdivisions.subdivision_codes(effective_country_code)
            # Get country name, raise exception if invalid code
            try:
                country_name = countries.get(alpha_2=effective_country_code).name
            except (AttributeError, KeyError):
                country_name = 'Unknown'
        
        if verbose:
            flag_emoji = flag.flag(effective_country_code) if effective_country_code != "XK" else ""
            print(f"[START] Fetching neighbours for {len(subdivision_codes)} subdivisions in {country_name} ({effective_country_code}) {flag_emoji}...")
        
        # Initialize neighbours dict with all subdivision codes (set to empty list initially)
        neighbours = {}
        for subdivision_code in subdivision_codes:
            neighbours[subdivision_code] = []
        
        # First, try to load bounding boxes from cache
        bounding_boxes = {}
        subdivision_codes_needing_fetch = []
        cache_hits = 0
        
        # Check cache for bounding boxes, collect codes needing fetch
        if self.use_cache and self.geo_cache is not None and not self.geo_cache.empty:
            for subdivision_code in subdivision_codes:
                cached_row = self.geo_cache[self.geo_cache['subdivisionCode'] == subdivision_code]
                # Check if bounding box exists in cache, use it if valid
                if not cached_row.empty and 'boundingBox' in self.geo_cache.columns:
                    cached_bbox = cached_row['boundingBox'].values[0]
                    # Validate and load cached bounding box
                    if cached_bbox and pd.notna(cached_bbox):
                        try:
                            bbox = json.loads(cached_bbox) if isinstance(cached_bbox, str) else cached_bbox
                            bounding_boxes[subdivision_code] = bbox
                            cache_hits += 1
                            if verbose:
                                print(f"  [CACHE HIT] {subdivision_code} - Bounding box found in cache file, API call skipped: {bbox}")
                            continue
                        except (json.JSONDecodeError, ValueError):
                            pass
                
                subdivision_codes_needing_fetch.append(subdivision_code)
        else:
            subdivision_codes_needing_fetch = list(subdivision_codes)
        
        # Fetch bounding boxes for subdivision codes not in cache
        if subdivision_codes_needing_fetch:
            fetched_bboxes = self.get_bounding_box(country_code=country_code, verbose=verbose, export=export)
            bounding_boxes.update(fetched_bboxes)
        
        # Calculate neighbours based on bounding box overlap, using simple rectangle overlap logic
        for subdivision_code in subdivision_codes:
            # Skip if bounding box not available
            if subdivision_code not in bounding_boxes:
                continue
            
            # Get bounding box for current subdivision
            bbox1 = bounding_boxes[subdivision_code]
            minlat1, maxlat1, minlon1, maxlon1 = bbox1
            
            # Compare with all other subdivisions in the same country
            for other_code in subdivision_codes:
                if other_code == subdivision_code or other_code not in bounding_boxes:
                    continue
                
                # Get bounding box for other subdivision
                bbox2 = bounding_boxes[other_code]
                minlat2, maxlat2, minlon2, maxlon2 = bbox2
                
                # Check if bounding boxes overlap or touch
                # Boxes overlap/touch if they don't have a gap between them
                if not (maxlon1 < minlon2 or maxlon2 < minlon1 or maxlat1 < minlat2 or maxlat2 < minlat1):
                    neighbours[subdivision_code].append(other_code)
            
            # Verbose logging of neighbours found
            if verbose:
                sub_name = subdivisions[effective_country_code][subdivision_code].name
                neighbor_names = [f"{code} ({subdivisions[effective_country_code][code].name})" for code in neighbours[subdivision_code]]
                print(f"  [{subdivision_code}] {sub_name} - Neighbors: {', '.join(neighbor_names)}")
        
        # Cache neighbours data - update cache with comma-separated neighbour lists
        for subdivision_code, neighbor_list in neighbours.items():
            neighbours_str = ','.join(neighbor_list) if neighbor_list else None
            
            # Update or append to cache DataFrame
            if self.geo_cache is not None and not self.geo_cache.empty:
                if subdivision_code in self.geo_cache['subdivisionCode'].values:
                    self.geo_cache.loc[self.geo_cache['subdivisionCode'] == subdivision_code, 'neighbours'] = neighbours_str
                else:
                    # Add new row with neighbours data
                    new_row = pd.DataFrame({
                        'subdivisionCode': [subdivision_code],
                        'latLng': [None],
                        'boundingBox': [None],
                        'geojson': [None],
                        'perimeter': [None],
                        'neighbours': [neighbours_str]
                    })
                    self.geo_cache = pd.concat([self.geo_cache, new_row], ignore_index=True)
        
        # Export to cache if export_to_cache is enabled
        if self.export_to_cache:
            self._export_cache(verbose=verbose)
        
        # Verbose logging
        if verbose:
            total_neighbors = sum(len(n) for n in neighbours.values())
            print(f"[END] Found {total_neighbors} total neighbor relationships")
        
        return neighbours
    
    def get_all(self, country_code: Optional[str] = None, verbose: bool = False, export: bool = True, skip_geojson: bool = True) -> Dict[str, Dict[str, Any]]:
        """
        Get all geographical data (latLng, bounding_box, geojson, perimeter, neighbours) for each ISO 3166-2 
        subdivision in the country or countries. Retrieves all attributes in a single call by delegating 
        to get_lat_lng(), get_bounding_box(), get_geojson(), get_perimeter(), and get_neighbours(). Checks 
        cache first for all attributes, then fetches missing data from Nominatim API. Due to the geojson
        export taking significant space, geojson fetching is skipped by default unless explicitly requested.
        
        Parameters
        ==========
        country_code : str, optional
            ISO 3166-1 alpha-2 or alpha-3 country code, or comma-separated list of codes (e.g., 'AD' or 'AD,DE,FR'). Default is None.
        verbose : bool, optional
            Enable verbose logging. Default is False.
        export : bool, optional
            Export newly-fetched data to cache. Default is True.
        skip_geojson : bool, optional
            Skip fetching and exporting GeoJSON data. When True, GeoJSON will be excluded from output.
            Default is True.
        
        Returns
        =======
        Dict[str, Dict[str, Any]]
            Dictionary mapping subdivision codes to dictionaries containing all attributes.
            Example: {
                'US-CA': {
                    'latLng': '37.2695,-119.3064',
                    'bounding_box': [32.5, 42.0, -124.5, -114.1],
                    'perimeter': 12456.78,
                    'geojson': {'type': 'Polygon', 'coordinates': [...]}
                },
                'US-DE': {
                    'latLng': '39.3185,-75.5243',
                    'bounding_box': [38.45, 39.84, -75.79, -75.05],
                    'perimeter': 3421.23,
                    'geojson': {'type': 'Polygon', 'coordinates': [...]}
                },
                'AD-01': {
                    'latLng': '42.5000,1.5000',
                    'bounding_box': [42.4, 42.6, 1.4, 1.6],
                    'perimeter': 156.45,
                    'geojson': {'type': 'Polygon', 'coordinates': [...]}
                },
                ...
            }
        """
        # Parse comma-separated country codes
        country_codes = self._parse_country_codes(country_code)
        
        # If multiple countries, process each and merge results
        if len(country_codes) > 1:
            all_geo_data = {}
            for cc in country_codes:
                result = self.get_all(country_code=cc, verbose=verbose, export=export, skip_geojson=skip_geojson)
                all_geo_data.update(result)
            if export:
                self._export_cache(verbose=verbose)
            return all_geo_data
        
        # Single country processing
        effective_country_code = country_codes[0]
        
        # Verbose logging
        if verbose:
            try:
                country_name = countries.get(alpha_2=effective_country_code).name
            except (AttributeError, KeyError):
                country_name = 'Unknown'
            flag_emoji = flag.flag(effective_country_code) if effective_country_code != "XK" else ""
            print(f"[START] Fetching all geographical data for {country_name} {effective_country_code} {flag_emoji}...")
        
        # Fetch all attributes using the respective methods
        latLngs = self.get_lat_lng(country_code=country_code, verbose=verbose, export=export)
        bounding_boxes = self.get_bounding_box(country_code=country_code, verbose=verbose, export=export)
        perimeters = self.get_perimeter(country_code=country_code, verbose=verbose, export=export)
        neighbours = self.get_neighbours(country_code=country_code, verbose=verbose, export=export)
        
        # Conditionally fetch GeoJSON if not skipping
        if not skip_geojson:
            geojsons = self.get_geojson(country_code=country_code, verbose=verbose, export=export)
        else:
            geojsons = {}
        
        # Combine all attributes into a single result dictionary
        all_geo_data = {}
        
        # Get subdivision codes - reuse self.subdivisions if country matches, otherwise create temp instance
        if country_code is not None and convert_to_alpha2(country_code) != self.country_code:
            subdivisions = Subdivisions()
            subdivision_codes = subdivisions.subdivision_codes(effective_country_code)
        else:
            subdivision_codes = self.subdivision_codes
        
        # Iterate over subdivision codes to assemble all data, skipping empty entries
        for subdivision_code in subdivision_codes:
            geo_entry = {}
            
            # Add latLng if available
            if subdivision_code in latLngs:
                geo_entry['latLng'] = latLngs[subdivision_code]
            
            # Add bounding box if available
            if subdivision_code in bounding_boxes:
                geo_entry['bounding_box'] = bounding_boxes[subdivision_code]
            
            # Add perimeter if available
            if subdivision_code in perimeters:
                geo_entry['perimeter'] = perimeters[subdivision_code]
            
            # Add neighbours if available
            if subdivision_code in neighbours:
                geo_entry['neighbours'] = neighbours[subdivision_code]
            
            # Add geojson if available and not skipped
            if not skip_geojson and subdivision_code in geojsons:
                geo_entry['geojson'] = geojsons[subdivision_code]
            
            # Only add to results if at least one attribute is present
            if geo_entry:
                all_geo_data[subdivision_code] = geo_entry
        
        # Export to cache if requested
        if export:
            self._export_cache(verbose=verbose)
        
        # Verbose logging of summary statistics
        if verbose:
            total_with_latLng = len([s for s in all_geo_data.keys() if 'latLng' in all_geo_data[s]])
            total_with_bbox = len([s for s in all_geo_data.keys() if 'bounding_box' in all_geo_data[s]])
            total_with_perimeter = len([s for s in all_geo_data.keys() if 'perimeter' in all_geo_data[s]])
            total_with_neighbours = len([s for s in all_geo_data.keys() if 'neighbours' in all_geo_data[s]])
            total_with_geojson = len([s for s in all_geo_data.keys() if 'geojson' in all_geo_data[s]])
            print(f"[END] Fetched all data for {len(subdivision_codes)} subdivisions:")
            print(f"      - LatLngs: {total_with_latLng}")
            print(f"      - Bounding boxes: {total_with_bbox}")
            print(f"      - Perimeters: {total_with_perimeter}")
            print(f"      - Neighbours: {total_with_neighbours}")
            if not skip_geojson:
                print(f"      - GeoJSON: {total_with_geojson}")
        
        return all_geo_data

    def get_statistics(self, geo_cache_filepath: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculate and return statistics from a geo cache file. Reads cached geographical 
        data (latLngs, bounding boxes, perimeters, neighbours, geojson) from a CSV file
        and computes comprehensive statistics without making any API calls. It captures:
        - Total number of cached subdivisions
        - Data completeness percentages for latLngs, bounding boxes, perimeters
        - Statistical measures (min, max, mean, median) for latitudes, longitudes,
            bounding box dimensions, and perimeters.

        Parameters
        ==========
        geo_cache_filepath : str, optional
            Path to geo cache CSV file. If not provided, uses the default cache path.
            Default is None.
        
        Returns
        =======
        Dict[str, Any]
            Dictionary containing comprehensive statistics.
        
        Raises
        ======
        FileNotFoundError
            If the specified cache file does not exist.
        """ 
        # Use provided filepath or default
        cache_path = geo_cache_filepath if geo_cache_filepath is not None else self.geo_cache_path
        
        # Check if file exists
        if not os.path.exists(cache_path):
            raise FileNotFoundError(f"Cache file not found: {cache_path}")
        
        # Read cache file
        try:
            cache_df = pd.read_csv(cache_path, dtype={'subdivisionCode': str})
            # subdivisionCode column is already in correct format
        except Exception as e:
            raise ValueError(f"Failed to read cache file {cache_path}: {str(e)}")
        
        # Extract data from cache
        lats = []
        lons = []
        bbox_widths = []
        bbox_heights = []
        bbox_areas = []
        perimeter_values = []
        
        latLngs_count = 0
        bounding_boxes_count = 0
        perimeters_count = 0
        complete_entries = 0  # Entries with all three data types
        empty_entries = 0  # Entries with no data
        
        # Iterate over cache rows to collect data, compute counts and statistics
        for _, row in cache_df.iterrows():
            has_latLng = False
            has_bbox = False
            has_perimeter = False
            
            # Process latLngs
            if pd.notna(row.get('latLng')):
                try:
                    lat, lon = map(float, str(row['latLng']).split(','))
                    lats.append(lat)
                    lons.append(lon)
                    latLngs_count += 1
                    has_latLng = True
                except (ValueError, AttributeError):
                    pass
            
            # Process bounding boxes
            if pd.notna(row.get('boundingBox')):
                try:
                    bbox = json.loads(str(row['boundingBox']))
                    minlat, maxlat, minlon, maxlon = bbox
                    width = maxlon - minlon
                    height = maxlat - minlat
                    area = width * height  # Calculate bounding box area
                    bbox_widths.append(width)
                    bbox_heights.append(height)
                    bbox_areas.append(area)
                    bounding_boxes_count += 1
                    has_bbox = True
                except (ValueError, json.JSONDecodeError, AttributeError):
                    pass
            
            # Process perimeters
            if pd.notna(row.get('perimeter')):
                try:
                    perimeter = float(row['perimeter'])
                    perimeter_values.append(perimeter)
                    perimeters_count += 1
                    has_perimeter = True
                except (ValueError, TypeError):
                    pass
            
            # Count complete and empty entries
            if has_latLng and has_bbox and has_perimeter:
                complete_entries += 1
            elif not has_latLng and not has_bbox and not has_perimeter:
                empty_entries += 1
        
        # Get cache file size with appropriate unit
        cache_size_bytes = os.path.getsize(cache_path)
        if cache_size_bytes < 1024:
            cache_size_str = f"{cache_size_bytes} B"
        elif cache_size_bytes < 1024 * 1024:
            cache_size_str = f"{round(cache_size_bytes / 1024, 2)} KB"
        else:
            cache_size_str = f"{round(cache_size_bytes / (1024 * 1024), 2)} MB"
        
        total_entries = len(cache_df)
        
        # Compile statistics
        stats = {
            'cache_file': cache_path,
            'cache_file_size': cache_size_str,
            # 'cache_file_size_bytes': cache_size_bytes,
            'total_entries': total_entries,
            'data_completeness': {
                'complete_entries': complete_entries,
                'complete_percentage': round(complete_entries / total_entries * 100, 2) if total_entries > 0 else 0,
                'empty_entries': empty_entries,
                'empty_percentage': round(empty_entries / total_entries * 100, 2) if total_entries > 0 else 0,
                'partial_entries': total_entries - complete_entries - empty_entries
            },
            'latLngs': {
                'count': latLngs_count,
                'percentage': round(latLngs_count / total_entries * 100, 2) if total_entries > 0 else 0,
                'stats': {
                    'lats': {
                        'min': round(min(lats), 4) if lats else None,
                        'max': round(max(lats), 4) if lats else None,
                        'mean': round(mean(lats), 4) if lats else None,
                        'median': round(median(lats), 4) if lats else None
                    },
                    'lons': {
                        'min': round(min(lons), 4) if lons else None,
                        'max': round(max(lons), 4) if lons else None,
                        'mean': round(mean(lons), 4) if lons else None,
                        'median': round(median(lons), 4) if lons else None
                    }
                }
            },
            'bounding_boxes': {
                'count': bounding_boxes_count,
                'percentage': round(bounding_boxes_count / total_entries * 100, 2) if total_entries > 0 else 0,
                'widths': {
                    'min': round(min(bbox_widths), 4) if bbox_widths else None,
                    'max': round(max(bbox_widths), 4) if bbox_widths else None,
                    'mean': round(mean(bbox_widths), 4) if bbox_widths else None,
                    'median': round(median(bbox_widths), 4) if bbox_widths else None
                },
                'heights': {
                    'min': round(min(bbox_heights), 4) if bbox_heights else None,
                    'max': round(max(bbox_heights), 4) if bbox_heights else None,
                    'mean': round(mean(bbox_heights), 4) if bbox_heights else None,
                    'median': round(median(bbox_heights), 4) if bbox_heights else None
                },
                'areas': {
                    'min': round(min(bbox_areas), 4) if bbox_areas else None,
                    'max': round(max(bbox_areas), 4) if bbox_areas else None,
                    'mean': round(mean(bbox_areas), 4) if bbox_areas else None,
                    'median': round(median(bbox_areas), 4) if bbox_areas else None
                }
            },
            'perimeters': {
                'count': perimeters_count,
                'percentage': round(perimeters_count / total_entries * 100, 2) if total_entries > 0 else 0,
                'stats': {
                    'min': round(min(perimeter_values), 2) if perimeter_values else None,
                    'max': round(max(perimeter_values), 2) if perimeter_values else None,
                    'mean': round(mean(perimeter_values), 2) if perimeter_values else None,
                    'median': round(median(perimeter_values), 2) if perimeter_values else None,
                    'total': round(sum(perimeter_values), 2) if perimeter_values else None
                }
            }
        }
        
        return stats

    def _clear_cache(self) -> None:
        """
        Clear the in-memory cache. Clears all cached geographical data from memory. 
        This does not affect the cache file on disk, only the in-memory representation.

        Parameters
        ==========
        None

        Returns
        =======
        None
        """
        self.geo_cache = None

    def _load_cache(self) -> Optional[pd.DataFrame]:
        """ 
        Load geo cache from filepath if use_cache is True. When use_cache is False, returns None.
        When use_cache is True and geo_cache_path is not provided or file doesn't exist, prints a message and returns None.

        Parameters
        ==========
        None

        Returns
        =======
        pd.DataFrame or None
            DataFrame containing the geo cache if use_cache is True and file exists,
            or None if use_cache is False or cache file not found.
        """
        # If use_cache is False, return None without loading cache
        if not self.use_cache:
            return None
        
        # If use_cache is True but no path provided, print message and return None
        if self.geo_cache_path is None:
            print("No cache path provided and use_cache is True. Geo cache set to None.")
            return None
        
        # Check if the cache file exists at the provided path
        if not os.path.exists(self.geo_cache_path):
            print(f"No cache found at path {self.geo_cache_path}. Geo cache set to None.")
            return None
        
        # Load the cache file
        try:
            # Read CSV with subdivisionCode as string to preserve leading zeros
            cache = pd.read_csv(self.geo_cache_path, dtype={'subdivisionCode': str})
            return cache
        except Exception as e:
            print(f"Error reading geo_cache CSV from {self.geo_cache_path}: {e}. Geo cache set to None.")
            return None

    def _parse_country_codes(self, country_code: Optional[str]) -> List[str]:
        """
        Parse a country code parameter that may contain comma-separated values.
        
        Parameters
        ==========
        country_code : str, optional
            Single country code or comma-separated list of country codes (e.g., 'AD' or 'AD,DE,FR')
        
        Returns
        =======
        List[str]
            List of normalized country codes
        
        Raises
        ======
        ValueError
            If country_code is not provided and instance was not initialized with a country code.
        """
        # If no country_code provided, use instance's country_code, else raise error
        if country_code is None:
            if self.country_code is None:
                raise ValueError("country_code is required. Provide it as a parameter or initialize Geo with a valid country code.")
            return [self.country_code]
        
        # Split by comma, strip whitespace, and convert each to alpha-2
        codes = [convert_to_alpha2(code.strip()) for code in country_code.split(',') if code.strip()]
        return codes
    
    def _fetch_subdivision_data(self, subdivision_code: str, get_geojson: bool = False) -> Optional[Dict[str, Any]]:
        """
        Fetch latLng, bounding box, and GeoJSON for a single subdivision from Nominatim API via its
        ISO 3166-2 code.
        
        Parameters
        ==========
        subdivision_code : str
            ISO 3166-2 subdivision code (e.g., 'US-CA')
        get_geojson : bool, optional
            If True, include polygon_geojson, extratags, and limit parameters in the API request
            for fetching full GeoJSON geometry. If False, use basic parameters only.
            Default is False.
        
        Returns
        =======
        dict or None
            Dictionary with keys:
            - 'latLng': tuple (lat, lon)
            - 'bounding_box': list [minlat, maxlat, minlon, maxlon]
            - 'geojson': dict with GeoJSON geometry
            Returns None if subdivision not found or API error
        """
        try:
            # Extract country code from subdivision code (e.g., 'US-CA' -> 'US')
            country_code = subdivision_code.split('-')[0]
            
            # Prepare Nominatim API request parameters
            params = {
                'q': subdivision_code,
                'countrycode': country_code.lower(),
                'format': 'jsonv2'
            }
            
            # Add additional parameters if fetching full GeoJSON data
            if get_geojson:
                params['polygon_geojson'] = 1
                params['extratags'] = 1
                params['limit'] = 1
            
            # Make the API request, with timeout and proxy if set
            user_agent = 'iso3166-2-python/1.0.0 (+https://github.com/amckenna41/iso3166-2)'
            resp = requests.get(
                NOMINATIM_API_URL,
                params=params,
                timeout=15,
                headers={'User-Agent': user_agent},
                proxies=self.proxy if self.proxy else None
            )

            # Raise exception for HTTP errors
            resp.raise_for_status()
            results = resp.json()
            
            # Check if any results were returned
            if not results or len(results) == 0:
                return None
            
            result = results[0]
            
            # Extract the three attributes from the Nominatim response
            data = {
                'subdivisionCode': subdivision_code,
                'latLng': (float(result.get('lat', 0)), float(result.get('lon', 0))),
                'bounding_box': result.get('boundingbox'),  # [minlat, maxlat, minlon, maxlon]
                'geojson': result.get('geojson'),
                'osm_id': result.get('osm_id'),
                'name': result.get('name')
            }

            return data
        
        # Handle exceptions and return None on failure
        except Exception as e:
            if self.verbose:
                print(f"Error fetching {subdivision_code}: {e}")
            return None
    
    def _export_cache(self, custom_cache_export_path: Optional[str] = None, verbose: bool = False) -> None:
        """
        Export in-memory cache to CSV file. Writes the current in-memory cache DataFrame 
        to a CSV file at the configured cache path or custom export path. Creates any 
        necessary parent directories if they don't exist.
        
        Parameters
        ==========
        custom_cache_export_path : str, optional
            Custom filepath for exporting the cache. If not provided, uses self.geo_cache_path.
            Default is None.
        verbose : bool, optional
            Enable verbose logging for the export operation. Default is False.
        
        Raises
        ======
        OSError
            If the cache file cannot be written due to permission or I/O errors.
        """
        # Skip export if cache is empty
        if self.geo_cache is None or self.geo_cache.empty:
            return
        
        # Use custom export path if provided, otherwise use instance cache path
        export_path = custom_cache_export_path if custom_cache_export_path is not None else self.geo_cache_path
        
        try:
            # Create parent directories if they don't exist
            cache_dir = os.path.dirname(export_path)
            if cache_dir and not os.path.exists(cache_dir):
                os.makedirs(cache_dir, exist_ok=True)
            
            # Write cache to CSV file
            self.geo_cache.to_csv(export_path, index=False)
            
            # Verbose logging
            if verbose:
                print(f"[EXPORT] Successfully exported geo cache to {export_path}")
        
        # Handle exceptions during export
        except Exception as e:
            if verbose:
                print(f"[EXPORT] Error: Failed to export geo cache: {e}")

    def _export_geojsons_to_file(self, geojsons: Dict[str, Dict], country_code: str) -> None:
        """
        Export GeoJSON data to a single GeoJSON FeatureCollection file.
        
        Parameters
        ==========
        geojsons : Dict[str, Dict]
            Dictionary mapping subdivision codes to GeoJSON data.
        country_code : str
            ISO 3166-1 alpha-2 country code used in the output filename.
        
        Raises
        ======
        OSError
            If the GeoJSON file cannot be written due to permission or I/O errors.
        """
        try:
            features = []
            # Aggregate all features from the geojsons, assuming each is a FeatureCollection
            for subdivision_code, geojson_data in geojsons.items():
                if geojson_data and 'features' in geojson_data:
                    # Extract features from FeatureCollection
                    features.extend(geojson_data['features'])
            
            # Create FeatureCollection
            feature_collection = {
                "type": "FeatureCollection",
                "features": features
            }
            
            # Write to file
            filename = f"{country_code}_geojson.geojson"
            with open(filename, 'w') as f:
                json.dump(feature_collection, f, indent=2)
            
            # Verbose logging
            if self.verbose:
                print(f"[EXPORT] Successfully exported {len(features)} GeoJSON features to {filename}")
        
        except Exception as e:
            if self.verbose:
                print(f"[EXPORT] Error exporting GeoJSON to file: {e}")

    def __repr__(self) -> str:
        """ Return detailed representation of Geo instance. """
        cache_loaded = self.geo_cache is not None and not self.geo_cache.empty
        cached_entries = len(self.geo_cache) if cache_loaded else 0
        return (f"Geo(country_code='{self.country_code}', country_name='{self.country_name}', "
                f"subdivisions={len(self.subdivision_codes) if self.subdivision_codes else 0}, "
                f"cached_entries={cached_entries}, cache_loaded={cache_loaded}, "
                f"verbose={self.verbose}, use_cache={self.use_cache}, "
                f"cache_path='{self.geo_cache_path}')")

    def __str__(self) -> str:
        """ Return user-friendly string representation of Geo instance. """
        if self.country_code is None:
            return "Geo(uninitialized - no country code)"
        return (f"Geo({self.country_name} [{self.country_code}]) - "
                f"{len(self.subdivision_codes) if self.subdivision_codes else 0} subdivisions")

    def __len__(self) -> int:
        """ Return the number of cached entries. """
        return len(self.geo_cache) if self.geo_cache is not None and not self.geo_cache.empty else 0


def fetch_all_country_geo_data(max_workers: int = 3, verbose: bool = False, country_codes: Optional[str] = None, 
                               geo_cache_path: Optional[str] = None, skip_attributes: str = 'geojson', export: bool = True):
    """
    Fetch all geographic data (latLngs, bounding boxes, perimeters, geojson & neighbours) for all country subdivisions
    in parallel using ThreadPoolExecutor via 1 or more workers. By default, ALL ~250 ISO 3166-1 countiries' 
    subdivisions are processed, but an individual or list of country codes can be input via the country_codes parameter. 

    You can skip fetching specific attributes (like GeoJSON) to save time and API calls by using the skip_attributes
    parameter. This is useful for large-scale data fetching where certain attributes may not be needed. The GeoJSON
    attribute is skipped by default to reduce API calls and processing time. The path to a custom geo cache CSV file
    can be provided via the geo_cache_path parameter, with any additional fetched geographical data appeneded to this file.

    If no geo_cache_path is provided, a timestamped cache file (geo_cache_YYYYMMDD_HHMM.csv) is created in the current 
    working directory.
    
    A detailed summary of the fetching process is printed to the console if verbose is enabled and an output
    statistics cache file is created at the end of the process to capture cache hits, API hits, and failures etc.
    This file is useful as if all attributes are captured for all countries/subdivisions, this will be a huge file
    with other 25,230 individual attrigutes (5,046 * 5), so understsanding the fetching stats is important.
    
    Parameters
    ==========
    max_workers : int, optional
        Number of parallel workers. Default is 3. Recommended: 3-5 to respect API rate limits.
    verbose : bool, optional
        Enable verbose logging. Default is False.
    country_codes : str, optional
        ISO 3166-1 alpha-2 or alpha-3 country code, or comma-separated list of codes (e.g., 'AD' or 'AD,DE,FR'). 
        If None, fetches for all countries. Default is None.
    geo_cache_path : str, optional
        Path to custom geo cache CSV file. Default is None.
    skip_attributes : str, optional
        Comma-separated list of geographical attributes to skip during processing.
        Acceptable values: latLng, boundingBox, geojson, perimeter, neighbours
        Example: 'geojson' or 'latLng,boundingBox,geojson'
        When an attribute is skipped, its function call is not executed but cached values remain intact.
        Default is 'geojson' (GeoJSON data is skipped by default).
    export : bool, optional
        Export newly-fetched data to cache. Default is True.
    
    Returns
    =======
    None

    Raises
    ======
    ValueError
        If invalid values are provided in skip_attributes.
    """
    # Parse skip_attributes into a set of lowercase attribute names
    skip_attrs = set(attr.strip().lower() for attr in skip_attributes.split(',') if attr.strip())
    
    # Validate skip_attributes values, raise error for invalid entries
    valid_attrs = {'latlng', 'boundingbox', 'geojson', 'perimeter', 'neighbours'}
    invalid_attrs = skip_attrs - valid_attrs
    if invalid_attrs:
        raise ValueError(f"Invalid skip_attributes values: {', '.join(invalid_attrs)}. Valid values are: {', '.join(valid_attrs)}")
    
    # Parse comma-separated country codes
    if country_codes is not None:
        all_countries = [convert_to_alpha2(cc.strip()) for cc in country_codes.split(',') if cc.strip()]
    else:
        # Get all country codes and sort alphabetically
        all_countries = sorted([country.alpha_2 for country in countries])
    
    print(f"Fetching geographic data for {len(all_countries)} countries...")
    fetching_attrs = valid_attrs - skip_attrs
    print(f"Fetching attributes: {', '.join(sorted(fetching_attrs)) if fetching_attrs else 'None'}, skipping attributes: {', '.join(sorted(skip_attrs)) if skip_attrs else 'None'}")
    
    # Create timestamped cache file in current directory 
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    cache_stats_file = os.path.join(os.getcwd(), f"geo_cache_{timestamp}.csv")
    
    results_list = []
    processed = 0
    keyboard_interrupted = False
    start_time = time.time()
    
    def fetch_country_data(cc: str) -> dict:
        """ Fetch all geo data for a single country. """
        # Create Geo instance for the country, reusing the provided cache path
        try:
            geo = Geo(cc, geo_cache_path=geo_cache_path, verbose=verbose)
            # get flag emoji for current country
            flag_emoji = flag.flag(cc) if cc != "XK" else ""
            print(f"\n Getting subdivision Geo data for {geo.country_name} ({cc}) {flag_emoji}...")

            # Only proceed if there are subdivisions, e.g AX, AQ has no subdivisions etc
            if geo.subdivision_codes:
                
                # Fetch LatLngs with detailed cache tracking
                lat_lngs = {}
                latLng_cache_hits = 0
                latLng_api_hits = 0

                # Only fetch latLng if not skipping
                if 'latlng' not in skip_attrs:
                    if verbose:
                        for sub_code in geo.subdivision_codes:
                            print(f"  [API] GET latLng: https://nominatim.openstreetmap.org/search?q={sub_code}&format=json")
                    lat_lngs = geo.get_lat_lng(verbose=verbose, export=export)
                    # Use vectorized pandas operations for capturing the cache hit total via O(1) 
                    if geo.use_cache and geo.geo_cache is not None and not geo.geo_cache.empty and 'latLng' in geo.geo_cache.columns:
                        cached_mask = (geo.geo_cache['subdivisionCode'].isin(geo.subdivision_codes)) & (geo.geo_cache['latLng'].notna())
                        latLng_cache_hits = len(geo.geo_cache[cached_mask])
                    # Calculate API hits, non-cached subdivisions, total latLng fetched and failed
                    latLng_api_hits = len(geo.subdivision_codes or []) - latLng_cache_hits
                    latLng_count = len([c for c in lat_lngs.values() if c])
                    latLng_failed = len(geo.subdivision_codes or []) - latLng_count
                else:
                    latLng_count = 0
                    latLng_failed = 0
                
                # Fetch Bounding Boxes with detailed cache tracking
                bounding_boxes = {}
                bbox_cache_hits = 0
                bbox_api_hits = 0

                # Only fetch bounding box if not skipping
                if 'boundingbox' not in skip_attrs:
                    if verbose:
                        for sub_code in geo.subdivision_codes:
                            print(f"  [API] GET boundingBox: https://nominatim.openstreetmap.org/search?q={sub_code}&format=json&boundingbox=1")
                    bounding_boxes = geo.get_bounding_box(verbose=verbose, export=export)
                    # Use vectorized pandas operations for capturing the cache hit total via O(1) 
                    if geo.use_cache and geo.geo_cache is not None and not geo.geo_cache.empty and 'boundingBox' in geo.geo_cache.columns:
                        cached_mask = (geo.geo_cache['subdivisionCode'].isin(geo.subdivision_codes)) & (geo.geo_cache['boundingBox'].notna())
                        bbox_cache_hits = len(geo.geo_cache[cached_mask])
                    # Calculate API hits, non-cached subdivisions, total bounding box fetched and failed
                    bbox_api_hits = len(geo.subdivision_codes or []) - bbox_cache_hits
                    bbox_count = len([b for b in bounding_boxes.values() if b])
                    bbox_failed = len(geo.subdivision_codes or []) - bbox_count
                else:
                    bbox_count = 0
                    bbox_failed = 0
                
                # Conditionally fetch GeoJSON if not skipping
                geojsons = {}
                geojson_cache_hits = 0
                geojson_api_hits = 0

                # Only fetch GeoJSON if not skipping
                if 'geojson' not in skip_attrs:
                    if verbose:
                        for sub_code in geo.subdivision_codes:
                            print(f"  [API] GET geojson: https://nominatim.openstreetmap.org/search?q={sub_code}&format=geojson")
                    geojsons = geo.get_geojson(verbose=verbose, export=export)
                    # Use vectorized pandas operations for capturing the cache hit total via O(1) 
                    if geo.use_cache and geo.geo_cache is not None and not geo.geo_cache.empty and 'geojson' in geo.geo_cache.columns:
                        cached_mask = (geo.geo_cache['subdivisionCode'].isin(geo.subdivision_codes)) & (geo.geo_cache['geojson'].notna())
                        geojson_cache_hits = len(geo.geo_cache[cached_mask])
                    # Calculate API hits, non-cached subdivisions, total GeoJSON fetched and failed
                    geojson_api_hits = len(geo.subdivision_codes or []) - geojson_cache_hits
                    geojson_count = len([g for g in geojsons.values() if g])
                    geojson_failed = len(geo.subdivision_codes or []) - geojson_count
                else:
                    geojson_count = 0
                    geojson_failed = 0
                
                # Fetch Perimeters with detailed cache tracking
                perimeters = {}
                perimeter_cache_hits = 0
                perimeter_api_hits = 0
                
                # Only fetch perimeter if not skipping
                if 'perimeter' not in skip_attrs:
                    if verbose:
                        for sub_code in geo.subdivision_codes:
                            print(f"  [API] CALC perimeter: Calculated from geojson boundaries for {sub_code}")
                    perimeters = geo.get_perimeter(verbose=verbose, export=export)
                    # Use vectorized pandas operations for capturing the cache hit total via O(1) 
                    if geo.use_cache and geo.geo_cache is not None and not geo.geo_cache.empty and 'perimeter' in geo.geo_cache.columns:
                        cached_mask = (geo.geo_cache['subdivisionCode'].isin(geo.subdivision_codes)) & (geo.geo_cache['perimeter'].notna())
                        perimeter_cache_hits = len(geo.geo_cache[cached_mask])
                    # Calculate API hits, non-cached subdivisions, total perimeter fetched and failed
                    perimeter_api_hits = len(geo.subdivision_codes or []) - perimeter_cache_hits
                    perimeter_count = len([p for p in perimeters.values() if p])
                    perimeter_failed = len(geo.subdivision_codes or []) - perimeter_count
                else:
                    perimeter_count = 0
                    perimeter_failed = 0

                
                # Fetch Neighbours with detailed cache tracking
                neighbours = {}
                neighbours_cache_hits = 0
                neighbours_api_hits = 0

                # Only fetch neighbours if not skipping
                if 'neighbours' not in skip_attrs:
                    if verbose:
                        for sub_code in geo.subdivision_codes:
                            print(f"  [API] GET neighbours: https://nominatim.openstreetmap.org/search?q={sub_code}&format=json")
                    neighbours = geo.get_neighbours(verbose=verbose)
                    # Use vectorized pandas operations for capturing the cache hit total via O(1) 
                    if geo.use_cache and geo.geo_cache is not None and not geo.geo_cache.empty and 'neighbours' in geo.geo_cache.columns:
                        cached_mask = (geo.geo_cache['subdivisionCode'].isin(geo.subdivision_codes)) & (geo.geo_cache['neighbours'].notna())
                        neighbours_cache_hits = len(geo.geo_cache[cached_mask])
                    # Calculate API hits, non-cached subdivisions, total neighbours fetched and failed
                    neighbours_api_hits = len(geo.subdivision_codes or []) - neighbours_cache_hits
                    neighbours_count = len([n for n in neighbours.values() if n])
                    neighbours_failed = len(geo.subdivision_codes or []) - neighbours_count
                else:
                    neighbours_count = 0
                    neighbours_failed = 0
                
                # Export fetched data to cache file
                if geo.geo_cache is not None and not geo.geo_cache.empty:
                    geo._export_cache(verbose=verbose)
                
                # Compile result dictionary for this country, including detailed stats per attribute
                result = {
                    'country_code': cc,
                    'total': len(geo.subdivision_codes) if geo.subdivision_codes else 0,
                    'latLngs': {
                        'successful': latLng_count if 'latlng' not in skip_attrs else 0,
                        'failed': latLng_failed if 'latlng' not in skip_attrs else 0,
                        'cache_hits': latLng_cache_hits if 'latlng' not in skip_attrs else 0,
                        'api_calls': latLng_api_hits if 'latlng' not in skip_attrs else 0,
                        'skipped': 'latlng' in skip_attrs
                    },
                    'bounding_boxes': {
                        'successful': bbox_count if 'boundingbox' not in skip_attrs else 0,
                        'failed': bbox_failed if 'boundingbox' not in skip_attrs else 0,
                        'cache_hits': bbox_cache_hits if 'boundingbox' not in skip_attrs else 0,
                        'api_calls': bbox_api_hits if 'boundingbox' not in skip_attrs else 0,
                        'skipped': 'boundingbox' in skip_attrs
                    },
                    'perimeters': {
                        'successful': perimeter_count if 'perimeter' not in skip_attrs else 0,
                        'failed': perimeter_failed if 'perimeter' not in skip_attrs else 0,
                        'cache_hits': perimeter_cache_hits if 'perimeter' not in skip_attrs else 0,
                        'api_calls': perimeter_api_hits if 'perimeter' not in skip_attrs else 0,
                        'skipped': 'perimeter' in skip_attrs
                    },
                    'neighbours': {
                        'successful': neighbours_count if 'neighbours' not in skip_attrs else 0,
                        'failed': neighbours_failed if 'neighbours' not in skip_attrs else 0,
                        'cache_hits': neighbours_cache_hits if 'neighbours' not in skip_attrs else 0,
                        'api_calls': neighbours_api_hits if 'neighbours' not in skip_attrs else 0,
                        'skipped': 'neighbours' in skip_attrs
                    },
                    'geojson': {
                        'successful': geojson_count if 'geojson' not in skip_attrs else 0,
                        'failed': geojson_failed if 'geojson' not in skip_attrs else 0,
                        'cache_hits': geojson_cache_hits if 'geojson' not in skip_attrs else 0,
                        'api_calls': geojson_api_hits if 'geojson' not in skip_attrs else 0,
                        'skipped': 'geojson' in skip_attrs
                    },
                    'error': None
                }
                
                return result
        except Exception as e:
            print(f"[ERROR] Exception in fetch_country_data for {cc}: {type(e).__name__}: {str(e)}")
            return {
                'country_code': cc,
                'total': 0,
                'latLngs': {'successful': 0, 'failed': 0, 'cache_hits': 0, 'api_calls': 0, 'skipped': False},
                'bounding_boxes': {'successful': 0, 'failed': 0, 'cache_hits': 0, 'api_calls': 0, 'skipped': False},
                'perimeters': {'successful': 0, 'failed': 0, 'cache_hits': 0, 'api_calls': 0, 'skipped': False},
                'neighbours': {'successful': 0, 'failed': 0, 'cache_hits': 0, 'api_calls': 0, 'skipped': False},
                'geojson': {'successful': 0, 'failed': 0, 'cache_hits': 0, 'api_calls': 0, 'skipped': False},
                'error': str(e)
            }
    
    try:
        # Use executor.map() for ordered, sequential execution (maintains submission order)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            with tqdm(total=len(all_countries), desc="Fetching geo data", disable=not verbose) as pbar:
                for result in executor.map(fetch_country_data, all_countries):
                    results_list.append(result)
                    processed += 1
                    pbar.update(1)
    
    # Handle keyboard interrupt gracefully, output stats for completed workers so far
    except KeyboardInterrupt:
        keyboard_interrupted = True
        if verbose:
            print("\nFetch interrupted by user.")
        processed = len(results_list)  # Count only what was actually processed
    
    # Calculate total elapsed time
    elapsed = time.time() - start_time
    
    # Summary statistics - both print to console and write to file
    if verbose or keyboard_interrupted:  # Always show summary if interrupted
        total_subdivisions = sum(r['total'] for r in results_list)
        latLngs_successful = sum(r['latLngs']['successful'] for r in results_list)
        latLngs_cache_hits = sum(r['latLngs'].get('cache_hits', 0) for r in results_list)
        latLngs_api_calls = sum(r['latLngs'].get('api_calls', 0) for r in results_list)
        latLngs_skipped = any(r['latLngs'].get('skipped', False) for r in results_list)
        
        bounding_boxes_successful = sum(r['bounding_boxes']['successful'] for r in results_list)
        bbox_cache_hits = sum(r['bounding_boxes'].get('cache_hits', 0) for r in results_list)
        bbox_api_calls = sum(r['bounding_boxes'].get('api_calls', 0) for r in results_list)
        bbox_skipped = any(r['bounding_boxes'].get('skipped', False) for r in results_list)
        
        perimeters_successful = sum(r['perimeters']['successful'] for r in results_list)
        perimeter_cache_hits = sum(r['perimeters'].get('cache_hits', 0) for r in results_list)
        perimeter_api_calls = sum(r['perimeters'].get('api_calls', 0) for r in results_list)
        perimeter_skipped = any(r['perimeters'].get('skipped', False) for r in results_list)
        
        neighbours_successful = sum(r['neighbours']['successful'] for r in results_list)
        neighbours_cache_hits = sum(r['neighbours'].get('cache_hits', 0) for r in results_list)
        neighbours_api_calls = sum(r['neighbours'].get('api_calls', 0) for r in results_list)
        neighbours_skipped = any(r['neighbours'].get('skipped', False) for r in results_list)
        
        geojson_successful = sum(r['geojson']['successful'] for r in results_list)
        geojson_cache_hits = sum(r['geojson'].get('cache_hits', 0) for r in results_list)
        geojson_api_calls = sum(r['geojson'].get('api_calls', 0) for r in results_list)
        geojson_skipped = any(r['geojson'].get('skipped', False) for r in results_list)
        
        # Prepare statistics data for both console output and file writing
        stats_lines = []
        stats_lines.append(f"{'='*60}")
        stats_lines.append(f"SUMMARY")
        if keyboard_interrupted:
            stats_lines.append(f"** Interrupted by user - showing stats for completed workers **")
        stats_lines.append(f"{'='*60}")
        stats_lines.append(f"Countries processed: {processed}/{len(all_countries)}")
        stats_lines.append(f"Total subdivisions processed: {total_subdivisions}")
        
        if total_subdivisions > 0:
            status_str = " (Skipped)" if latLngs_skipped else ""
            stats_lines.append(f"\nLatLngs: {latLngs_successful}/{total_subdivisions} ({latLngs_successful/total_subdivisions*100:.1f}%){status_str}")
            if not latLngs_skipped:
                stats_lines.append(f"  └─ Cache hits: {latLngs_cache_hits} | API calls: {latLngs_api_calls}")
            
            status_str = " (Skipped)" if bbox_skipped else ""
            stats_lines.append(f"Bounding Boxes: {bounding_boxes_successful}/{total_subdivisions} ({bounding_boxes_successful/total_subdivisions*100:.1f}%){status_str}")
            if not bbox_skipped:
                stats_lines.append(f"  └─ Cache hits: {bbox_cache_hits} | API calls: {bbox_api_calls}")
            
            status_str = " (Skipped)" if perimeter_skipped else ""
            stats_lines.append(f"Perimeters: {perimeters_successful}/{total_subdivisions} ({perimeters_successful/total_subdivisions*100:.1f}%){status_str}")
            if not perimeter_skipped:
                stats_lines.append(f"  └─ Cache hits: {perimeter_cache_hits} | API calls: {perimeter_api_calls}")
            
            status_str = " (Skipped)" if neighbours_skipped else ""
            stats_lines.append(f"Neighbours: {neighbours_successful}/{total_subdivisions} ({neighbours_successful/total_subdivisions*100:.1f}%){status_str}")
            if not neighbours_skipped:
                stats_lines.append(f"  └─ Cache hits: {neighbours_cache_hits} | API calls: {neighbours_api_calls}")
            
            status_str = " (Skipped)" if geojson_skipped else ""
            stats_lines.append(f"GeoJSON: {geojson_successful}/{total_subdivisions} ({geojson_successful/total_subdivisions*100:.1f}%){status_str}")
            if not geojson_skipped:
                stats_lines.append(f"  └─ Cache hits: {geojson_cache_hits} | API calls: {geojson_api_calls}")
        else:
            stats_lines.append(f"LatLngs: 0/0 (0.0%)")
            stats_lines.append(f"Bounding Boxes: 0/0 (0.0%)")
            stats_lines.append(f"Perimeters: 0/0 (0.0%)")
            stats_lines.append(f"Neighbours: 0/0 (0.0%)")
            stats_lines.append(f"GeoJSON: 0/0 (0.0%)")
        
        # Cache statistics
        cache_file_path = geo_cache_path if geo_cache_path else os.path.join(os.getcwd(), f"geo_cache_{timestamp}.csv")
        if os.path.exists(cache_file_path):
            cache_size = os.path.getsize(cache_file_path)
            try:
                cache_df = pd.read_csv(cache_file_path)
                cache_rows = len(cache_df)
                if cache_size < 1024:
                    cache_size_str = f"{cache_size} B"
                elif cache_size < 1024 * 1024:
                    cache_size_str = f"{round(cache_size / 1024, 2)} KB"
                else:
                    cache_size_str = f"{round(cache_size / (1024 * 1024), 2)} MB"
                stats_lines.append(f"\nCache Statistics:")
                stats_lines.append(f"  Cache file: {cache_file_path}")
                stats_lines.append(f"  Cache entries: {cache_rows}")
                stats_lines.append(f"  Cache size: {cache_size_str}")
            except Exception as e:
                stats_lines.append(f"\nCache Statistics: Error reading cache - {str(e)}")
        
        stats_lines.append(f"\nTime elapsed: {elapsed:.1f}s ({elapsed/60:.1f}m)")
        stats_lines.append(f"{'='*60}\n")
        
        # Print to console
        for line in stats_lines:
            print(line)
        
        # Write statistics to timestamped CSV file
        try:
            with open(cache_stats_file, 'w', newline='') as f:
                for line in stats_lines:
                    f.write(line + '\n')
            if verbose:
                print(f"Statistics exported to: {cache_stats_file}")
        except Exception as e:
            print(f"[ERROR] Failed to write statistics file: {str(e)}")


def get_geo_nulls(geo_cache_filepath: str, print_summary: bool = False, export_filename: Optional[str] = None) -> None:
    """
    Analyze a geo cache CSV file and identify all rows with null/None values for each geographical attribute.
    Generates a summary file containing lists of subdivision codes that are missing data for each attribute,
    as well as some other metadata about the current state of the cache.
    
    Parameters
    ==========
    geo_cache_filepath : str
        Path to the geo cache CSV file to analyze (e.g., 'geo_cache.csv').
    print_summary : bool, optional
        If True, prints the null summaries to console after exporting. Default is False.
    export_filename : str, optional
        Custom filename for the exported null analysis file. If None or empty string, uses default format
        'geo_cache_nulls_YYYYMMDD_HHMM.csv'. Default is None.
    
    Returns
    =======
    None
        Exports a summary file containing null analysis.
    
    Raises
    ======
    FileNotFoundError
        If the specified geo_cache_filepath does not exist.
    ValueError
        If the CSV file is missing required columns.
    """
    # Check if file exists, raise error if not
    if not os.path.exists(geo_cache_filepath):
        raise FileNotFoundError(f"Geo cache file not found: {geo_cache_filepath}")
    
    # Load the cache file
    try:
        cache_df = pd.read_csv(geo_cache_filepath)
    except Exception as e:
        raise ValueError(f"Failed to read geo cache file: {str(e)}")
    
    # Define required attributes to check
    required_attributes = ['latLng', 'boundingBox', 'geojson', 'perimeter', 'neighbours']
    
    # Verify all required columns exist
    missing_columns = [attr for attr in required_attributes if attr not in cache_df.columns]
    if missing_columns:
        raise ValueError(f"Cache file missing required columns: {missing_columns}")
    
    # Analyze nulls for each attribute
    null_summary = {}
    total_rows = len(cache_df)
    
    # Iterate over each required attribute and find nulls
    for attribute in required_attributes:
        # Check for null or NaN values (handles both None and np.nan)
        null_mask = cache_df[attribute].isna()
        null_codes = cache_df[null_mask]['subdivisionCode'].tolist() if 'subdivisionCode' in cache_df.columns else []
        null_count = len(null_codes)
        null_percentage = (null_count / total_rows * 100) if total_rows > 0 else 0

        # Store summary, including count, percentage, and affected codes
        null_summary[attribute] = {
            'count': null_count,
            'percentage': null_percentage,
            'codes': null_codes
        }
    
    # Generate output filename - use custom if provided and not empty, otherwise use default
    if export_filename and export_filename.strip():
        output_filename = export_filename.strip()
        output_filepath = output_filename if os.path.isabs(output_filename) else os.path.join(os.path.dirname(geo_cache_filepath), output_filename)
    else:
        timestamp = datetime.now().strftime("%Y%m%d")
        output_filename = f"geo_cache_nulls_{timestamp}.json"
        output_filepath = os.path.join(os.path.dirname(geo_cache_filepath), output_filename)
    
    # Write null summary to file as JSON
    try:
        # Calculate overall statistics
        total_null_count = sum(null_summary[attr]['count'] for attr in required_attributes)
        total_possible_values = total_rows * len(required_attributes)
        overall_completeness = round(((total_possible_values - total_null_count) / total_possible_values * 100), 2) if total_possible_values > 0 else 100.0
        
        # Get cache file size in KB
        cache_file_size_kb = round(os.path.getsize(geo_cache_filepath) / 1024, 2)
        
        # Build JSON structure with metadata and attribute analysis
        json_output = {
            "metadata": {
                "analysisDate": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "sourceFile": geo_cache_filepath,
                "totalRows": total_rows,
                "overallCompleteness": overall_completeness,
                "totalNullCount": total_null_count,
                "cacheFileSize": f"{cache_file_size_kb} KB"
            },
            "attributes": {}
        }
        
        # Add analysis for each attribute
        for attribute in required_attributes:
            summary = null_summary[attribute]
            # Extract unique country codes from subdivision codes (format: "CC-XX")
            country_codes = list(set(code.split('-')[0] for code in summary['codes']))
            country_codes.sort()  # Sort for consistent output
            
            json_output["attributes"][attribute] = {
                "totalCount": total_rows,
                "nullCount": summary['count'],
                "nullPercentage": round(summary['percentage'], 2),
                "countryCodes": ','.join(country_codes),  # Unique country codes with missing data
                "subdivisionCodes": ','.join(summary['codes'])  # Compact string format instead of array
            }
        
        # Write JSON to file
        with open(output_filepath, 'w') as f:
            json.dump(json_output, f, indent=2)
        
        print(f"✓ Null analysis exported to: {output_filepath}")
    except Exception as e:
        print(f"[ERROR] Failed to write null analysis file: {str(e)}")
        return
    
    # Print summary to console if requested
    if print_summary:
        print("\n" + "="*70)
        print("GEO CACHE NULL SUMMARY")
        print("="*70)
        print(f"Source: {geo_cache_filepath}")
        print(f"Total rows: {total_rows}")
        print("-"*70)
        print(f"{'Attribute':<15} {'Null Count':<12} {'Percentage':<12} {'Affected Codes':<30}")
        print("-"*70)
        
        # Print summary for each attribute, previewing up to 3 codes
        for attribute in required_attributes:
            summary = null_summary[attribute]
            codes_preview = ', '.join(summary['codes'][:3]) if summary['codes'] else 'None'
            if len(summary['codes']) > 3:
                codes_preview += f", +{len(summary['codes']) - 3} more"
            
            print(f"{attribute:<15} {summary['count']:<12} {summary['percentage']:>10.2f}%  {codes_preview:<30}")
        
        print("="*70)
        print(f"Details written to: {output_filepath}\n")