import os
import time
import json
import argparse
import requests
from pycountry import countries, subdivisions
import flag
from tqdm import tqdm
from fp.fp import FreeProxy
import warnings
import pandas as pd
import numpy as np
try:
    from update_subdivisions import update_subdivision
    from local_other_names import add_local_other_names, validate_local_other_names
    from utils import export_iso3166_2_data, get_alpha_codes_list, get_flag_repo_url
    from geo import Geo
    from restcountries_api import get_rest_countries_country_data, get_supported_fields
    from city_data import get_cities_for_subdivision
    from history import add_history
    from iso3166_2 import Subdivisions
except ImportError:
    from scripts.update_subdivisions import update_subdivision
    from scripts.local_other_names import add_local_other_names, validate_local_other_names
    from scripts.utils import export_iso3166_2_data, get_alpha_codes_list, get_flag_repo_url
    from scripts.geo import Geo
    from scripts.restcountries_api import get_rest_countries_country_data, get_supported_fields
    from scripts.city_data import get_cities_for_subdivision
    from scripts.history import add_history
    from iso3166_2 import Subdivisions

#ignore resource warnings
warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

#user agent header for requests
USER_AGENT_HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

def export_iso3166_2(alpha_codes: str="", export_folder: str="test-iso3166-2-output", export_filename: str="test-iso3166-2",
                     resources_folder: str="iso3166_2_resources", verbose: bool=1, export: bool=False, export_csv: bool=True, 
                     export_xml: bool=True, alpha_codes_range: str="", rest_countries_keys: str="", filter_attributes: str="", 
                     state_city_data: bool=False, history: bool=True, save_each_iteration: bool=False, use_proxy=False, 
                     geo_cache_path: str=os.path.join("iso3166_2_resources", "geo_cache_min.csv")) -> None:
    """
    Export all ISO 3166-2 subdivision related data to JSON, CSV and or XML files. The default attributes
    exported for each subdivision include: subdivision code, name, local name, type, parent code, flag
    URL, history and latitude/longitude. The flag URL attribute is taken from the custom-built
    iso3166-flags (https://github.com/amckenna41/iso3166-flags) repo, the history attribute
    is taken from the custom-built iso3166-updates (https://github.com/amckenna41/iso3166-updates) repo
    and latitude/longitude is retrieved via the OpenStreetMap API. By default all of the subdivision data
    for each ISO 3166 country will be exported but a string of 1 or more country alpha codes can
    be input, as well as a range of alpha codes e.g "AD-EG" etc.

    The generated JSON is used as a baseline for the ISO 3166-2 data object, but additional and more
    up-to-date and accurate data is added with the help of the iso3166-updates software/API
    (https://github.com/amckenna41/iso3166-updates). The update_subdivisions module is imported that
    adds, amends and or deletes any subdivisions from this baseline object to make it up-to-date,
    reliable and accurate to any recent updates to the ISO 3166-2 database, according to the ISO.

    When exporting this JSON you can also add additional fields/attributes to each country's subdivision
    object via the RestCountries API. The subset of supported fields include: idd, carSigns, carSide,
    continents, currencies, languages, postalCode, region, startOfWeek, subregion, timezones, tld. Note
    that these attribute values are at the country level and not the subdivision level. A description
    for each of these fields can be seen on the RestCountries repo:
    https://gitlab.com/restcountries/restcountries/-/blob/master/FIELDS.md?plain=1.

    An additional optional attribute is history. Any historical changes/updates to the subdivision,
    published by the ISO, are exported from the iso3166-updates custom-built Python package. If no
    explicit change found to the subdivision's code, name or local name then it will be set to null.
    To include this historical data in the export, set the history parameter to True.

    We can also export the city-level data per subdivision by setting the state_city_data parameter to True.
    This will pull a list of cities per subdivision and their coordinates via the Country State City API
    (https://countrystatecity.in/).An API key to use this API is required.

    Finally, there are 7 default attributes exported per each subdivision as mentioned above. 1 or more
    of these can be excluded for each subdivision if only a subset is required. Simply pass in a string
    of one or more of the attribute as they are exported in the output object: name, localOtherName,
    type, parentCode, flag, history or latLng. Note the country and subdivision code cannot be excluded.

    Parameters
    ==========
    :alpha_codes: str (default="")
        string of 1 or more 2 letter alpha-2, 3 letter alpha-3 or numeric country codes to extract their
        latest ISO 3166-2 data.
    :export_folder: str (default="iso3166-2-output")
        output folder to store exported iso3166-2 data.
    :export_filename: str (default="iso3166-2")
        output filename for JSON object with all ISO 3166-2 data.
    :resources_folder: str (default=resources_folder)
        directory to external resources folder that stores the local/other names dataset & subdivision
        updates csv.
    :verbose: bool (default=1)
        set to 1 to print out progress of export functionality, 0 will not print progress.
    :export: bool (default=False)
        set to 1 to export the ISO 3166-2 data object from the function.
    :export_csv: bool (default=True)
        set to 1 to export the ISO 3166-2 dataset to CSV.
    :export_xml: bool (default=True)
        set to 1 to export the ISO 3166-2 dataset to XML.
    :alpha_codes_range: str (default="")
        a range of 2 ISO 3166-1 alpha-2, alpha-3 or numeric country codes to export the data from,
        separated by a '-'. The code on the left hand side will be the starting alpha code and the
        code on the right hand side will be the final alpha code to which the data is exported from,
        e.g AD-LV, will export all data from Andorra to Latvia, alphabetically. Useful if a subset
        of codes are required. If only a single alpha code input then it will serve as the starting country.
    :rest_countries_keys: str (default="")
        str of one or more comma separated additional attributes from the RestCountries API that can be
        appended to each of the subdivisions in the output object. If the wildcard '*' is input then 
        all available keys will be exported. Here is the full list of accepted fields/attributes: 
        "idd", "carSigns", "carSide", "continents", "currencies", "languages", "postalCode", "region", 
        "startOfWeek", "subregion", "timezones", "tld".
    :filter_attributes: str (default="")
        str of one or more of the default keys/attributes that are exported for each country's subdivision by default,
        to be included in each country's subdivision object. These include: name, localOtherName, type, parentCode,
        latLng, history and flag. Note the country and subdivision code keys are required for each subdivision
        and will be included by default. Any keys not included that are in the aforementioned list will be
        included.
    :state_city_data: bool (default=False)
        include the city-level data per subdivision via the Country State City API. By default these aren't
        included due to the additional verbose data.
    :history: bool (default=True)
        include any historical updates/changes per subdivision, published by the ISO, via the custom-built
        iso3166-updates software.
    :save_each_iteration: bool (default=False)
        if this parameter is set then during each country code iteration, the exported data will be 
        saved to the export dir, rather than at the end all in one go. This was implemented as
        during the extraction process if one country/iteration fails, you will loose all the progress 
        of all the previous iterations. This is only for the JSON exports. The exported JSON on each 
        iteration will contain all the exported data up to and including the current iteration and not 
        just the current iteration's data. 
    :use_proxy: bool (default=False)
        if set to True then use a proxy IP when scraping the wiki data via the requests.get, not used for 
        any of the other APIs in extraction process.
    :geo_cache_path: str (default="iso3166_2_resources/geo_cache_min.csv")
        custom path to geo cache CSV file. If not provided or empty string, uses the default cache path
        (iso3166_2_resources/geo_cache.csv). This parameter is passed to the Geo class instance for
        fetching geographical data like latitude/longitude coordinates.

    Returns
    =======
    :iso3166_2_data: dict|None
        the ISO 3166-2 data object that contains all the country and subdivision data if the export
        parameter is set to True otherwise return None.

    Raises
    ======
    TypeError:
        Invalid data type for alpha code parameter.
    ValueError:
        Error parsing the local/other names csv.
        Attribute/field not listed in default attributes list.
        Attribute/field not available in RestCountries API.
        Subdivision code already present in the object.

    Usage
    =====
    Please refer to the directory's README.md for usage examples:
    https://github.com/amckenna41/iso3166-2/tree/main/scripts
    """
    #if list of alpha codes input, cast into a comma separated string
    if (isinstance(alpha_codes, list)):
        alpha_codes = ", ".join(alpha_codes)

    #raise error if input alpha code parameter is not of correct type
    if not (isinstance(alpha_codes, str)):
        raise TypeError(f"Alpha code input parameter not of correct type, got {type(alpha_codes)}.")

    #validate and convert inputted alpha codes and alpha codes range, if applicable
    alpha_codes, alpha_codes_range = get_alpha_codes_list(alpha_codes, alpha_codes_range)

    #objects to store all country output data in json and csv format
    all_country_data = {}

    #list with all attributes being exported in this script call, default attributes added first
    all_attributes = ["name", "localOtherName", "type", "parentCode", "flag", "latLng"]

    #create output dir if doesn't exist
    if not (os.path.isdir(export_folder)):
        os.mkdir(export_folder)

    #start timer
    start = time.time()

    #if less than 5 alpha-2 codes input then don't display progress bar, or print elapsed time
    tqdm_disable = False
    if (len(alpha_codes) < 5):
        tqdm_disable = True
    
    #get full path to local/other names csv
    local_other_names_filepath = os.path.join(resources_folder, "local_other_names.csv")

    #raise error and return error message if local other names csv is found to be invalid
    local_other_names_csv_valid, error_message = validate_local_other_names(local_other_names_csv=local_other_names_filepath)
    if (local_other_names_csv_valid == -1):
        raise ValueError(f"An error was found in the localOtherNames csv:\n{error_message}")

    #reading in, as dataframe, the csv that stores the local names for each subdivision, replace any Nan values with None
    local_other_name_df = pd.read_csv(local_other_names_filepath).replace(np.nan, None)

    #sort dataframe rows by their country code and reindex rows
    local_other_name_df = local_other_name_df.sort_values('alphaCode').reset_index(drop=True)

    #parse input RestCountries attributes/fields, if applicable
    if rest_countries_keys:
        rest_countries_keys_expected = get_supported_fields()
        if rest_countries_keys == "*":
            rest_countries_keys_converted_list = rest_countries_keys_expected
        else:
            rest_countries_keys_converted_list = rest_countries_keys.replace(' ', '').split(',')
            for key in rest_countries_keys_converted_list:
                if key not in rest_countries_keys_expected:
                    raise ValueError(f"Attribute/field ({key}) not available in RestCountries API, please refer to list of acceptable attributes below:\n{rest_countries_keys_expected}.")
        rest_countries_keys = sorted(rest_countries_keys_converted_list)
    
    #parse input default attributes to include/exclude from export
    if (filter_attributes != "" and filter_attributes != []):
        #list of default output keys/attributes per subdivision
        filter_attributes_expected = ["name", "localOtherName", "type", "parentCode", "flag", "latLng"]
        
        #if parameter is a list, convert to str
        if (isinstance(filter_attributes, list)):
            filter_attributes = " ,".join(filter_attributes)

        #parse input attribute string into list, remove whitespace
        filter_attributes_converted_list = filter_attributes.replace(' ', '').split(',')
        
        #iterate over all input keys, raise error if invalid key input
        for key in filter_attributes_converted_list:
            if not (key in filter_attributes_expected):
                raise ValueError(f"Attribute/field ({key}) invalid, please refer to list of the acceptable default attributes below:\n{filter_attributes_expected}.")

        #extend history attribute if applicable, set history parameter to True if it is in filter_attributes input param
        if (history):
            filter_attributes_expected.extend(["history"])
        else:
            if ("history" in filter_attributes_converted_list):
                history = True

        # #extend area and population attributes if applicable, set demographics parameter to True if it is in filter_attributes input param
        # if (demographics):
        #     filter_attributes_expected.extend(["area", "population"])
        # else:
        #     if ("area" in filter_attributes_converted_list or "population" in filter_attributes_converted_list):
        #         demographics = True

        #     # #remove default key from list
        #     # all_attributes.remove(key)

        # #set filter_attributes var to filtered list
        filter_attributes = filter_attributes_converted_list
        # # all_attributes = [item for item in filter_attributes if item in all_attributes]
    else:
        filter_attributes = all_attributes

    #appending the different extra attributes to preserve custom order, 1st original attributes then history then rest country keys then cities
    # if (demographics):
    #     filter_attributes.extend(["area", "population"])
    if (history and "history" not in filter_attributes):
        filter_attributes.append("history")
    if (rest_countries_keys):
        filter_attributes.extend(rest_countries_keys)
    if (state_city_data and "cities" not in filter_attributes):
        filter_attributes.append("cities")

    #by default, using no proxy when calling requests.get
    proxy = None

    #set random proxy IP if using it, only for wiki data not other APIs used in process
    if (use_proxy):
        #create instance of Free Proxy class & get random proxy
        random_proxy = FreeProxy().get()

        #create proxy addresses for http & https, set to None if not using proxies
        proxy = {"http": random_proxy, "https": random_proxy} if use_proxy else None

    #create instance of Geo class, all of the required data should already be exported to the geo cache file
    geo = Geo(proxy=proxy, verbose=False, use_cache=True, export_to_cache=True, geo_cache_path=geo_cache_path if geo_cache_path else None)

    def _get_cached_latlng(subdivision_code: str):
        if geo.geo_cache is None or geo.geo_cache.empty or 'latLng' not in geo.geo_cache.columns:
            return None
        cached_latlng = geo.geo_cache.loc[geo.geo_cache['subdivisionCode'] == subdivision_code, 'latLng']
        if cached_latlng.empty:
            return None
        cached_val = cached_latlng.values[0]
        if cached_val is None or pd.isna(cached_val):
            return None
        if isinstance(cached_val, str) and cached_val.strip():
            return [float(x.strip()) for x in cached_val.split(',')]
        return None

    #iterate over all country codes, getting country and subdivision info, append to json object
    for alpha2 in tqdm(alpha_codes, ncols=70, disable=tqdm_disable):
        country_iter_start = time.time()

        #kosovo has no associated subdivisions, manually set params
        if (alpha2 == "XK"):
            country_name = "Kosovo"
            all_subdivisions = []
        else:
            #get country name and list of its subdivisions using pycountry library
            country_name = countries.get(alpha_2=alpha2).name
            all_subdivisions = list(subdivisions.get(country_code=alpha2))

        #print out progress if verbose
        if verbose:
            flag_icon = flag.flag(alpha2) if alpha2 != "XK" else ""
            print(f"\n- {country_name} ({alpha2}) {flag_icon}")

            if all_subdivisions:
                #print subdivisions & indent
                for sub in sorted(all_subdivisions, key=lambda s: s.code):
                    print(f"  Subdivision: {sub.name} ({sub.code})")
            else:
                print("  Subdivision: None")

        #create country key in json object
        all_country_data[alpha2] = {}

        #make call to RestCountries api if additional rest countries attributes input, raise error if invalid request
        if (rest_countries_keys != ""):
            rc_start = time.time()
            print(f"  [{alpha2}] Fetching RestCountries data...")
            country_restcountries_data = get_rest_countries_country_data(alpha2, proxy=proxy)
            print(f"  [{alpha2}] RestCountries complete - {time.time() - rc_start:.2f}s")
        
        #validating that flag folder for current country exists on iso3166-flags repo, only check if flag in desired attributes
        flag_folder_exists = False
        if ("flag" in filter_attributes):
            flag_start = time.time()
            if (requests.get("https://github.com/amckenna41/iso3166-flags/blob/main/iso3166-2-flags/" + alpha2, headers=USER_AGENT_HEADER, proxies=proxy, timeout=15).status_code != 404):
                flag_folder_exists = True
            print(f"  [{alpha2}] Flag check complete - {time.time() - flag_start:.2f}s")

        #iterate over all country's' subdivisions, assigning subdivision code, name, type, parent code and flag URL, where applicable for the json object
        print(f"  [{alpha2}] Processing {len(all_subdivisions)} subdivisions...")
                
        for subd in all_subdivisions:

            #removing whitespace at start/end of string, also removing "†" and "*" characters which appears in some official ISO subdivision names e.g MK & ES
            subdivision_name = subd.name
            subdivision_name = subdivision_name.replace('†', '').replace("*", '').strip()

            #raise error if subdivision code already in output object
            if (subd.code in list(all_country_data[alpha2].keys())):
                raise ValueError(f"Subdivision code already present in output object: {subd.code}.")

            #raise error if subdivision code already in output object
            if (subd.code in list(all_country_data[alpha2].keys())):
                raise ValueError(f"Subdivision code already present in output object: {subd.code}.")

            #initialise subdivision code object and its attributes
            all_country_data[alpha2][subd.code] = {}
            all_country_data[alpha2][subd.code]["name"] = subdivision_name
            all_country_data[alpha2][subd.code]["localOtherName"] = None
            all_country_data[alpha2][subd.code]["type"] = subd.type
            all_country_data[alpha2][subd.code]["parentCode"] = subd.parent_code

            #get subdivision coordinates (centroid) using OSM API and Geo class
            if ("latLng" in filter_attributes):
                # Use pre-fetched centroids instead of fetching per-subdivision
                cached_latlng = _get_cached_latlng(subd.code)
                all_country_data[alpha2][subd.code]["latLng"] = cached_latlng
            else:
                all_country_data[alpha2][subd.code]["latLng"] = None

            #don't request.get flag URL if not included in filter_attributes parameter
            if ("flag" in filter_attributes):
                if (flag_folder_exists):
                  all_country_data[alpha2][subd.code]["flag"] = get_flag_repo_url(subdivision_code=subd.code, alpha2_code=alpha2)
                else:
                  all_country_data[alpha2][subd.code]["flag"] = None
            else:
                all_country_data[alpha2][subd.code]["flag"] = None #temporary key for flag URL attribute

            #append rest country key data to country output object if inputted
            if rest_countries_keys != "" and rest_countries_keys is not None:
                for key in rest_countries_keys:
                    value = country_restcountries_data.get(key) if country_restcountries_data else None
                    all_country_data[alpha2][subd.code][key] = value

            #get list of cities per subdivision using city_data.py module
            if state_city_data:
                cities = get_cities_for_subdivision(alpha2, subd.code, proxy=proxy)
                all_country_data[alpha2][subd.code]["cities"] = cities

        # # print("demographics", demographics)
        # if (demographics):
        #     demo_start = time.time()
        #     print(f"  [{alpha2}] Fetching demographics data (area/population)...")
        #     #get area and population data for each subdivision via wikipedia
        #     demographics_data = export_demographics(alpha2)
        #     print(f"  [{alpha2}] Demographics complete - {time.time() - demo_start:.2f}s")
            
        #     # print("demographics_data", demographics_data)
        #     #iterate over each subdivision in country object, append area and population data where applicable
        #     for subdivision_code in all_country_data[alpha2]:
        #         if (subdivision_code in demographics_data):
        #             all_country_data[alpha2][subdivision_code]["area"] = demographics_data[subdivision_code]["area"]
        #             all_country_data[alpha2][subdivision_code]["population"] = demographics_data[subdivision_code]["population"]
        #             # all_country_data[alpha2][subdivision_code]["population_rank"] = demographics_data[subdivision_code].get("population_rank")
        #             # all_country_data[alpha2][subdivision_code]["population_density"] = demographics_data[subdivision_code].get("population_density")
        #         else:
        #             all_country_data[alpha2][subdivision_code]["area"] = None
        #             all_country_data[alpha2][subdivision_code]["population"] = None
        #             # all_country_data[alpha2][subdivision_code]["population_rank"] = None
        #             # all_country_data[alpha2][subdivision_code]["population_density"] = None

        #add any subdivisions missing from pycountry using iso3166_2 dataset
        if (alpha2 != "XK"):
            try:
                iso_subdivisions = Subdivisions(alpha2)
                iso_subdivision_data = iso_subdivisions.all.get(alpha2, {})
            except Exception:
                iso_subdivision_data = {}

            if iso_subdivision_data:
                for subdivision_code, subdivision_data in iso_subdivision_data.items():
                    if subdivision_code in all_country_data[alpha2]:
                        continue

                    all_country_data[alpha2][subdivision_code] = {}
                    all_country_data[alpha2][subdivision_code]["name"] = subdivision_data.get("name")
                    all_country_data[alpha2][subdivision_code]["localOtherName"] = None
                    all_country_data[alpha2][subdivision_code]["type"] = subdivision_data.get("type")
                    all_country_data[alpha2][subdivision_code]["parentCode"] = subdivision_data.get("parentCode")

                    if ("latLng" in filter_attributes):
                        cached_latlng = _get_cached_latlng(subdivision_code)
                        all_country_data[alpha2][subdivision_code]["latLng"] = cached_latlng if cached_latlng is not None else subdivision_data.get("latLng")
                    else:
                        all_country_data[alpha2][subdivision_code]["latLng"] = None

                    if ("flag" in filter_attributes):
                        if (flag_folder_exists):
                            all_country_data[alpha2][subdivision_code]["flag"] = get_flag_repo_url(subdivision_code=subdivision_code, alpha2_code=alpha2)
                        else:
                            all_country_data[alpha2][subdivision_code]["flag"] = None
                    else:
                        all_country_data[alpha2][subdivision_code]["flag"] = None

        #save current exported country subdivision data at the current iteration - useful for saving exported process if one iteration fails 
        if (save_each_iteration):

            #path to json file will be in the main repo dir by default
            export_filepath = os.path.join(export_folder, export_filename)  

            #add current country code to filename
            export_filepath = os.path.splitext(export_filepath)[0] + f"_{alpha2}"

            #append json extension to output filename
            if (os.path.splitext(export_filepath) != ".json"):
                export_filepath = export_filepath + ".json"

            #write json data with all country info to json output file
            with open(export_filepath, 'w', encoding='utf-8') as f:
                json.dump(all_country_data, f, ensure_ascii=False, indent=4)

            #read json data with all current subdivision data
            with open(export_filepath, 'r', encoding='utf-8') as input_json:
                all_country_data = json.load(input_json)
            
            #append latest subdivision updates/changes from /iso3166_2_resources folder to the iso3166-2 object
            all_country_data = update_subdivision(iso3166_2_filename=export_filepath, subdivision_csv=os.path.join(resources_folder, "subdivision_updates.csv"), export=0,
                                                    rest_countries_keys=rest_countries_keys)

            #get local/other name data for each subdivision, unless localOtherName or name attributes to be excluded from export
            if (filter_attributes == "" or ("localOtherName" in filter_attributes)):
                all_country_data = add_local_other_names(all_country_data, filepath=local_other_names_filepath)

            #add historical subdivision data updates from iso3166-updates software - needs to be done here after all attribute values such as local name added to all subdivision objects
            if (history or "history" in filter_attributes):
                all_country_data = add_history(all_country_data)
            
            #sort individual subdivision attributes into order and sort subdivision codes into natural order
            all_country_data = {
                country_code: {
                    subdivision_code: {
                        key: subdivisions[subdivision_code].get(key)
                        for key in filter_attributes
                    }
                    for subdivision_code in sorted(subdivisions)
                }
                for country_code, subdivisions in sorted(all_country_data.items())
            }

            #export the subdivision data object to the output files - only JSON when save_each_iteration is True
            export_iso3166_2_data(all_country_data=all_country_data, export_filepath=export_filepath, export_csv=False, export_xml=False)
    
        print(f"  [{alpha2}] Iteration complete - {time.time() - country_iter_start:.2f}s total\n")
        #sort subdivision codes in json objects in natural alphabetical/numerical order using natsort library
        # all_country_data[alpha2] = dict(OrderedDict(natsort.natsorted(all_country_data[alpha2].items())))

    #if 10 or less alpha-2 codes input then append to filename, else add range of alpha codes specified by alpha_codes_range parameter
    if (len(alpha_codes) <= 10 and (alpha_codes_range == "")):
        export_filename = os.path.splitext(export_filename)[0] + "_" + ",".join(alpha_codes)
    elif (alpha_codes_range != ""):
        #add range of alpha codes being extracted to the filename, if only 1 alpha code input to alpha_codes_range then set end alpha code as ZW
        if not ("-" in alpha_codes_range):
            start_alpha_code = alpha_codes_range
            end_alpha_code = alpha_codes[-1]
        else:
            start_alpha_code, end_alpha_code = alpha_codes_range.split('-')[0].upper().replace(' ', ''), alpha_codes_range.split('-')[1].upper().replace(' ', '')

            #swap 2 alpha codes to ensure they're in alphabetical order
            if (start_alpha_code > end_alpha_code):
                temp_code = start_alpha_code
                start_alpha_code = end_alpha_code
                end_alpha_code = temp_code

        #create export filename with alpha code range
        export_filename = os.path.splitext(export_filename)[0] + "_" + start_alpha_code + "-" + end_alpha_code

    #path to json file will be in the main repo dir by default
    export_filepath = os.path.join(export_folder, export_filename)

    #append json extension to output filename
    if (os.path.splitext(export_filepath) != ".json"):
        export_filepath = export_filepath + ".json"

    #write json data with all country info to json output file
    with open(export_filepath, 'w', encoding='utf-8') as f:
        json.dump(all_country_data, f, ensure_ascii=False, indent=4)

    #read json data with all current subdivision data
    with open(export_filepath, 'r', encoding='utf-8') as input_json:
        all_country_data = json.load(input_json)
    
    #append latest subdivision updates/changes from /iso3166_2_resources folder to the iso3166-2 object
    update_start = time.time()
    all_country_data = update_subdivision(iso3166_2_filename=export_filepath, subdivision_csv=os.path.join(resources_folder, "subdivision_updates.csv"), export=0,
                                          rest_countries_keys=rest_countries_keys)

    #get local Name data for each subdivision, unless localOtherName or name attributes to be excluded from export
    if (filter_attributes == "" or ("localOtherName" in filter_attributes or "name" in filter_attributes)):
        local_start = time.time()
        all_country_data = add_local_other_names(all_country_data, filepath=local_other_names_filepath)

    #add historical subdivision data updates from iso3166-updates software - needs to be done here after all attribute values such as local name added to all subdivision objects
    if (history or "history" in filter_attributes):
        history_start = time.time()
        all_country_data = add_history(all_country_data)

    #sort subdivision objects into natural order and convert to regular dicts
    all_country_data = {
        country_code: {
            subdivision_code: {
                key: subdivisions[subdivision_code].get(key)
                for key in filter_attributes
            }
            for subdivision_code in sorted(subdivisions)
        }
        for country_code, subdivisions in sorted(all_country_data.items())
    }
    #start export timer
    export_start = time.time()

    #export the subdivision data object to the output files
    export_iso3166_2_data(all_country_data=all_country_data, export_filepath=export_filepath, export_csv=export_csv, export_xml=export_xml)

    #stop counter and calculate elapsed time
    end = time.time()
    elapsed = end - start

    if (verbose):
        print('\n######################################################################\n')
        print(f"ISO 3166-2 data successfully exported to {export_filepath}.")
        print(f"\n[FINAL] Elapsed Time: {(elapsed / 60):.2f} minutes ({elapsed:.1f}s)")
        print(f"[FINAL] Completed at {time.strftime('%H:%M:%S')}")
        print('######################################################################')

    #return the ISO 3166-2 data object if applicable
    if (export):
        return all_country_data
    
if __name__ == '__main__':

    #parse input arguments using ArgParse 
    parser = argparse.ArgumentParser(description='Script for exporting ISO 3166-1 country and subdivision data.')

    parser.add_argument('-alpha_codes', '--alpha_codes', type=str, required=False, default="", 
        help='One or more ISO 3166-1 alpha-2, alpha-3 or numeric country codes, by default all ISO 3166-2 subdivision data for all countries will be exported.')
    parser.add_argument('-export_filename', '--export_filename', type=str, required=False, default="test_iso3166-2", 
        help='Output filename for iso3166-2 object.')
    parser.add_argument('-resources_folder', '--resources_folder', type=str, required=False, default="iso3166_2_resources", 
        help='Filepath to the resources folder required for export, including the local/other names csv and updates subdivisions csv.')
    parser.add_argument('-export_folder', '--export_folder', type=str, required=False, default="test_iso3166-2", 
        help='Output folder to store output objects.')
    parser.add_argument('-export', '--export', required=False, action=argparse.BooleanOptionalAction, default=0, 
        help='Set to 1 to export ISO 3166-2 data object from the function.')
    parser.add_argument('-export_csv', '--export_csv', required=False, action=argparse.BooleanOptionalAction, default=1, 
        help='Set to 1 to export ISO 3166-2 dataset to CSV, JSON is only exported by default.')
    parser.add_argument('-export_xml', '--export_xml', required=False, action=argparse.BooleanOptionalAction, default=1, 
        help='Set to 1 to export ISO 3166-2 dataset to XML, JSON is only exported by default.')
    parser.add_argument('-verbose', '--verbose', required=False, action=argparse.BooleanOptionalAction, default=1, 
        help='Set to 1 to print out progress of export function, 0 will not print progress.')
    parser.add_argument('-alpha_codes_range', '--alpha_codes_range', type=str, required=False, default="", 
        help='Range of alpha codes to export from, inclusive. If only a single alpha code input then it will serve as the starting country.')
    parser.add_argument('-rest_countries_keys', '--rest_countries_keys', type=str, required=False, default="", 
        help='List of additional fields/attributes from RestCountries API to be added to each subdivision object.')
    parser.add_argument('-filter_attributes', '--filter_attributes', type=str, required=False, default="", 
        help="Subset of default fields/attributes to include in each country's subdivision object.")
    parser.add_argument('-state_city_data', '--state_city_data', required=False, action=argparse.BooleanOptionalAction, default=0, 
        help='Set to 1 to include city level data for each subdivision, by default this is not gotten.')
    parser.add_argument('-history', '--history', required=False, action=argparse.BooleanOptionalAction, default=0, 
        help='Set to 1 to get the historical data updates to the subdivision.')
    parser.add_argument('-save_each_iteration', '--save_each_iteration', required=False, action=argparse.BooleanOptionalAction, default=0, 
        help='Set to 1 to save the exported subdivision data on each iteration rather than just at the end.')
    parser.add_argument('-use_proxy', '--use_proxy', required=False, action=argparse.BooleanOptionalAction, default=0, 
        help='Set to 1 to use a proxy IP when scraping the data from wiki.')
    parser.add_argument('-geo_cache_path', '--geo_cache_path', type=str, required=False, default=os.path.join("iso3166_2_resources", "geo_cache_min.csv"), 
        help='Custom path to geo cache CSV file. If not provided, uses the default cache path.')
    
    #parse input args
    args = parser.parse_args()

    #export ISO 3166-2 data 
    export_iso3166_2(**vars(args))