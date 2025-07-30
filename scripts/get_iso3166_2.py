import os
import time
import json
import argparse
import requests
import pycountry
import flag
import googlemaps
from tqdm import tqdm
from fp.fp import FreeProxy
import warnings
import pandas as pd
import numpy as np
#multiple import options for update_subdivisions, local_other_names and utils modules depending on if script is called directly or via test script
try:
    from update_subdivisions import *
except:
    from scripts.update_subdivisions import *
try:
    from local_other_names import *
except:
    from scripts.local_other_names import *
try:
    from utils import *
except:
    from scripts.utils import *

#base URL for RestCountries API
rest_countries_base_url = "https://restcountries.com/v3.1/"

#base URL for Country State City API
country_state_city_base_url = "https://api.countrystatecity.in/v1/countries/"

#ignore resource warnings
warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

def export_iso3166_2(alpha_codes: str="", export_folder: str="test-iso3166-2-output", export_filename: str="test-iso3166-2",
                     resources_folder: str="iso3166_2_resources", verbose: bool=1, export_csv: bool=True, export_xml: bool=True, 
                     alpha_codes_range: str="", rest_countries_keys: str="", exclude_default_attributes: str="", state_city_data: bool=False, 
                     history: bool=True, extract_lat_lng: bool=0, save_each_iteration: bool=False, use_proxy=False) -> None:
    """
    Export all ISO 3166-2 subdivision related data to JSON, CSV and or XML files. The default attributes
    exported for each subdivision include: subdivision code, name, local name, type, parent code, flag
    URL, history and latitude/longitude. The flag URL attribute is taken from the custom-built
    iso3166-flag-icons (https://github.com/amckenna41/iso3166-flag-icons) repo, the history attribute
    is taken from the custom-built iso3166-updates (https://github.com/amckenna41/iso3166-updates) repo
    and latitude/longitude is retrieved via the GoogleMaps API. By default all of the subdivision data
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
        appended to each of the subdivisions in the output object. Here is the full list of accepted
        fields/attributes: "idd", "carSigns", "carSide", "continents", "currencies", "languages",
                    "postalCode", "region", "startOfWeek", "subregion", "timezones", "tld".
    :exclude_default_attributes: str (default="")
        str of one or more of the default keys/attributes that are exported for each country's subdivision by default,
        to be excluded from each country's subdivision object. These include: name, localOtherName, type, parentCode,
        latLng, history and flag. Note the country and subdivision code keys are required for each subdivision
        and can't be excluded. By default, all of the aforementioned keys will be exported for each subdivision.
    :state_city_data: bool (default=False)
        include the city-level data per subdivision via the Country State City API. By default these aren't
        included due to the additional verbose data.
    :history: bool (default=True)
        include any historical updates/changes per subdivision, published by the ISO, via the custom-built
        iso3166-updates software.
    :extract_lat_lng: bool (default=False)
        download the coordinates (latitude/longitude) for each subdivision via the Google Maps API. By default, the
        lat/lng are not extracted due to the resource cost, the latLng attribute will be set to [].
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

    Returns
    =======
    None

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
    if (rest_countries_keys != ""):
        #list of rest country attributes that can be appended to output object
        rest_countries_keys_expected = ["idd", "carSigns", "carSide", "continents", "currencies", "languages",
                                    "postalCode", "region", "startOfWeek", "subregion", "timezones", "tld"]

        #parse input attribute string into list, remove whitespace
        rest_countries_keys_converted_list = rest_countries_keys.replace(' ', '').split(',')

        #iterate over all input RestCountries keys, raise error if invalid key input
        for key in rest_countries_keys_converted_list:
            if not (key in rest_countries_keys_expected):
                raise ValueError(f"Attribute/field ({key}) not available in RestCountries API, please refer to list of acceptable attributes below:\n{rest_countries_keys_expected}.")

        rest_countries_keys = rest_countries_keys_converted_list

        # #append rest countries to all attributes list
        # all_attributes.append(", ".join(rest_countries_keys))

    #parse input default attributes to exclude from export
    if (exclude_default_attributes != ""):
        #list of default output keys/attributes per subdivision
        exclude_default_attributes_expected = ["name", "localOtherName", "type", "parentCode", "flag", "latLng"]

        #parse input attribute string into list, remove whitespace
        exclude_default_attributes_converted_list = exclude_default_attributes.replace(' ', '').split(',')

        #iterate over all input keys, raise error if invalid key input
        for key in exclude_default_attributes_converted_list:
            if not (key in exclude_default_attributes_expected):
                raise ValueError(f"Attribute/field ({key}) invalid, please refer to list of the acceptable default attributes below:\n{exclude_default_attributes_expected}.")

            #remove default key from list
            all_attributes.remove(key)

        exclude_default_attributes = exclude_default_attributes_converted_list

    #appending the different extra attributes to preserve custom order, 1st original attributes then history then rest country keys then cities
    if (history):
        all_attributes.append("history")
    if (rest_countries_keys):
        all_attributes.extend(rest_countries_keys)
    if (state_city_data):
        all_attributes.append("cities")
    # if not (extract_lat_lng):     #removing latLng attribute from default if not extracting
    #     all_attributes.remove('latLng')

    print(f"Exporting {len(alpha_codes)} ISO 3166-2 country's data to folder {export_folder} with the following attributes:\n{', '.join(all_attributes)}.")
    print('##################################################################################################\n')

    #by default, using no proxy when calling requests.get
    proxy = None

    #set random proxy IP if using it, only for wiki data not other APIs used in process
    if (use_proxy):
        #create instance of Free Proxy class & get random proxy
        random_proxy = FreeProxy().get()

        #create proxy addresses for http & https, set to None if not using proxies
        proxy = {"http": random_proxy, "https": random_proxy} if use_proxy else None

    #iterate over all country codes, getting country and subdivision info, append to json object
    for alpha2 in tqdm(alpha_codes, ncols=70, disable=tqdm_disable):

        #kosovo has no associated subdivisions, manually set params
        if (alpha2 == "XK"):
            country_name = "Kosovo"
            all_subdivisions = []
        else:
            #get country name and list of its subdivisions using pycountry library
            country_name = pycountry.countries.get(alpha_2=alpha2).name
            all_subdivisions = list(pycountry.subdivisions.get(country_code=alpha2))

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
            country_restcountries_response = requests.get(f'{rest_countries_base_url}alpha/{alpha2}', headers=USER_AGENT_HEADER, proxies=proxy, timeout=12)
            country_restcountries_response.raise_for_status()
            country_restcountries_data = country_restcountries_response.json()
        
        #validating that flag folder for current country exists on iso3166-flag-icons repo
        flag_folder_exists = False
        if (requests.get("https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/" + alpha2, headers=USER_AGENT_HEADER, proxies=proxy, timeout=15).status_code != 404):
          flag_folder_exists = True

        #iterate over all country's' subdivisions, assigning subdivision code, name, type, parent code and flag URL, where applicable for the json object
        for subd in all_subdivisions:

            #removing whitespace at start/end of string, also removing "†" and "*" characters which appears in some official ISO subdivision names e.g MK & ES
            subdivision_name = subd.name
            subdivision_name = subdivision_name.replace('†', '').replace("*", '').strip()

            #skip latLng getting functionality if bool parameter set
            if (extract_lat_lng):
                #get subdivision coordinates using googlemaps api python client, don't make API call if latLng attribute to be excluded from output
                if ("latLng" in exclude_default_attributes):
                    gmaps_latlng = []
                else:
                    #initialise google maps client with API key, use proxy if input proxy not None
                    session = requests.Session()
                    if (proxy):
                        session.proxies = {
                        "http": proxy,
                        "https": proxy
                    }
                                
                    gmaps = googlemaps.Client(key=os.environ["GOOGLE_MAPS_API_KEY"], requests_session=session)
                    # gmaps.session.close()
                    try:
                        gmaps_latlng = gmaps.geocode(subd.name + ", " + country_name, region=alpha2, language="en")
                        # gmaps_latlng.close()
                        #close session
                        session.close()

                    except Exception as e:
                        print(f"Error when searching for lat/lang of {subd.code} ({subd.name}) for {alpha2} using the GoogleMaps API:\n{e.args[0]}.")

                #set coordinates to None if not found using maps api, round to 3 decimal places
                if (gmaps_latlng != []):
                    subdivision_coords = [round(gmaps_latlng[0]['geometry']['location']['lat'], 3), round(gmaps_latlng[0]['geometry']['location']['lng'], 3)]
                else:
                    subdivision_coords = None

                #raise error if subdivision code already in output object
                if (subd.code in list(all_country_data[alpha2].keys())):
                    raise ValueError(f"Subdivision code already present in output object: {subd.code}.")
            else:
                subdivision_coords = None

            #initialise subdivision code object and its attributes
            all_country_data[alpha2][subd.code] = {}
            all_country_data[alpha2][subd.code]["name"] = subd.name
            all_country_data[alpha2][subd.code]["localOtherName"] = None
            all_country_data[alpha2][subd.code]["type"] = subd.type
            all_country_data[alpha2][subd.code]["parentCode"] = subd.parent_code
            all_country_data[alpha2][subd.code]["latLng"] = subdivision_coords

            #don't request.get flag URL if attribute excluded in exclude_default_attributes parameter
            if not ("flag" in exclude_default_attributes):
                if (flag_folder_exists):
                  all_country_data[alpha2][subd.code]["flag"] = get_flag_repo_url(subdivision_code=subd.code, alpha2_code=alpha2)
                else:
                  all_country_data[alpha2][subd.code]["flag"] = None
            else:
                all_country_data[alpha2][subd.code]["flag"] = None #temporary key for flag URL attribute

            #append rest country key data to country output object if inputted
            if (rest_countries_keys != "" and rest_countries_keys is not None):
                for key in rest_countries_keys:
                    #some rest country object data is in nested dict
                    if (key == "carSigns"):
                        all_country_data[alpha2][subd.code][key] = country_restcountries_data[0]["car"]["signs"]
                    elif (key == "carSides"):
                        all_country_data[alpha2][subd.code][key] = country_restcountries_data[0]["car"]["side"]
                    elif (key == "postalCode"):
                        all_country_data[alpha2][subd.code][key] = f"Format: {country_restcountries_data[0]['postalCode']['format']}, Regex: {country_restcountries_data[0]['postalCode']['regex']}"
                    else:
                        all_country_data[alpha2][subd.code][key] = country_restcountries_data[0][key]

                    #if attribute is list convert into str
                    if (isinstance(all_country_data[alpha2][subd.code][key], list)):
                        all_country_data[alpha2][subd.code][key] = ','.join(all_country_data[alpha2][subd.code][key])

            #get list of cities per subdivision, via the Country State City API
            if (state_city_data):
                #initialise cities attribute in subdivision object
                all_country_data[alpha2][subd.code]["cities"] = []

                #API requires the subdivision code minus the country code
                subd_code = subd.code.split('-')[1]

                #pull city-level subdivision data using the API
                subdivision_city_data_headers = USER_AGENT_HEADER
                subdivision_city_data_headers["X-CSCAPI-KEY"] = os.environ["COUNTRY_STATE_CITY_API_KEY"]
                subdivision_city_data = requests.get(f'{country_state_city_base_url}{alpha2}/states/{subd_code}/cities', headers=subdivision_city_data_headers, proxies=proxy, timeout=15).json()

                #iterate over each city object in API output, append each city name to attribute
                for city in subdivision_city_data:
                    all_country_data[alpha2][subd.code]["cities"].append(city['name'])

                #get lat/lang for each city, default False
                state_city_data_lat_lng = False

                #iterate over each city object in API output, append each city name and latLng to attribute - by default this is not executed
                if (state_city_data_lat_lng):
                    for city in subdivision_city_data:
                        all_country_data[alpha2][subd.code]["cities"].append({"name": city['name'], "latLng": [city['latitude'], city['longitude']]})

                #sort cities into alphabetical order
                all_country_data[alpha2][subd.code]["cities"] = sorted(all_country_data[alpha2][subd.code]["cities"])

            #iterate over each default attribute to be excluded from subdivision object, delete key, if applicable
            if (exclude_default_attributes != ""):
                for key in exclude_default_attributes:
                    # if (key != "latLng" and not extract_lat_lng):
                    del all_country_data[alpha2][subd.code][key]
            
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
                                                exclude_default_attributes=exclude_default_attributes, rest_countries_keys=rest_countries_keys)

            #get local/other name data for each subdivision, unless localOtherName or name attributes to be excluded from export
            if (exclude_default_attributes == "" or not ("localOtherName" in exclude_default_attributes)):
                all_country_data = add_local_other_names(all_country_data, filepath=local_other_names_filepath)

            #add historical subdivision data updates from iso3166-updates software - needs to be done here after all attribute values such as local name added to all subdivision objects
            if (history):
                all_country_data = add_history(all_country_data)
            
            #sort individual subdivision attributes into order and sort subdivision codes into natural order
            all_country_data = {
                country_code: {
                    subdivision_code: {
                        key: subdivisions[subdivision_code].get(key)
                        for key in all_attributes
                    }
                    for subdivision_code in sorted(subdivisions)
                }
                for country_code, subdivisions in sorted(all_country_data.items())
            }

            #export the subdivision data object to the output files
            export_iso3166_2_data(all_country_data=all_country_data, export_filepath=export_filepath, export_csv=export_csv, export_xml=export_xml, history=history,
                    exclude_default_attributes=exclude_default_attributes, rest_countries_keys=rest_countries_keys if isinstance(rest_countries_keys, list) else [])
    
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
    all_country_data = update_subdivision(iso3166_2_filename=export_filepath, subdivision_csv=os.path.join(resources_folder, "subdivision_updates.csv"), export=0,
                                          exclude_default_attributes=exclude_default_attributes, rest_countries_keys=rest_countries_keys)

    #get local Name data for each subdivision, unless localOtherName or name attributes to be excluded from export
    if (exclude_default_attributes == "" or not ("localOtherName" in exclude_default_attributes or "name" in exclude_default_attributes)):
        all_country_data = add_local_other_names(all_country_data, filepath=local_other_names_filepath)

    #add historical subdivision data updates from iso3166-updates software - needs to be done here after all attribute values such as local name added to all subdivision objects
    if (history):
        all_country_data = add_history(all_country_data)

    #sort subdivision objects into natural order and convert to regular dicts
    all_country_data = {
        country_code: {
            subdivision_code: {
                key: subdivisions[subdivision_code].get(key)
                for key in all_attributes
            }
            for subdivision_code in sorted(subdivisions)
        }
        for country_code, subdivisions in sorted(all_country_data.items())
    }

    #export the subdivision data object to the output files
    export_iso3166_2_data(all_country_data=all_country_data, export_filepath=export_filepath, export_csv=export_csv, export_xml=export_xml, history=history,
        exclude_default_attributes=exclude_default_attributes, rest_countries_keys=rest_countries_keys if isinstance(rest_countries_keys, list) else [])

    #stop counter and calculate elapsed time
    end = time.time()
    elapsed = end - start

    if (verbose):
        print('\n######################################################################\n')
        print(f"ISO 3166-2 data successfully exported to {export_filepath}.")
        print("\nElapsed Time for exporting all ISO 3166-2 data: {0:.2f} minutes.".format(elapsed / 60))

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
    parser.add_argument('-export_csv', '--export_csv', required=False, action=argparse.BooleanOptionalAction, default=1, 
        help='Set to 1 to export ISO 3166-2 dataset to CSV, JSON is only exported by default.')
    parser.add_argument('-export_xml', '--export_xml', required=False, action=argparse.BooleanOptionalAction, default=1, 
        help='Set to 1 to export ISO 3166-2 dataset to XML, JSON is only exported by default.')
    parser.add_argument('-extract_lat_lng', '--extract_lat_lng', required=False, action=argparse.BooleanOptionalAction, default=0, 
        help='Set to 1 to extract the lat/lng data for each subdivision via the Google Maps API, by default data not extracted due to resource cost.')
    parser.add_argument('-verbose', '--verbose', required=False, action=argparse.BooleanOptionalAction, default=1, 
        help='Set to 1 to print out progress of export function, 0 will not print progress.')
    parser.add_argument('-alpha_codes_range', '--alpha_codes_range', type=str, required=False, default="", 
        help='Range of alpha codes to export from, inclusive. If only a single alpha code input then it will serve as the starting country.')
    parser.add_argument('-rest_countries_keys', '--rest_countries_keys', type=str, required=False, default="", 
        help='List of additional fields/attributes from RestCountries API to be added to each subdivision object.')
    parser.add_argument('-exclude_default_attributes', '--exclude_default_attributes', type=str, required=False, default="", 
        help="List of default fields/attributes to be excluded from each country's subdivision object.")
    parser.add_argument('-state_city_data', '--state_city_data', required=False, action=argparse.BooleanOptionalAction, default=0, 
        help='Set to 1 to include city level data for each subdivision, by default this is not gotten.')
    parser.add_argument('-history', '--history', required=False, action=argparse.BooleanOptionalAction, default=0, 
        help='Set to 1 to get the historical data updates to the subdivision.')
    parser.add_argument('-save_each_iteration', '--save_each_iteration', required=False, action=argparse.BooleanOptionalAction, default=0, 
        help='Set to 1 to save the exported subdivision data on each iteration rather than just at the end.')
    parser.add_argument('-use_proxy', '--use_proxy', required=False, action=argparse.BooleanOptionalAction, default=0, 
        help='Set to 1 to use a proxy IP when scraping the data from wiki.')
    
    #parse input args
    args = parser.parse_args()

    #export ISO 3166-2 data 
    export_iso3166_2(**vars(args))
