import os
import time
import json
import argparse
import requests
import pycountry
import iso3166
import googlemaps
from tqdm import tqdm
import natsort
import random
import warnings
from collections import OrderedDict
import pandas as pd
import numpy as np
#multiple import options for update_subdivisions depending on if script is called directly or via test script
try:
    from update_subdivisions import *
except:
    from iso3166_2_scripts.update_subdivisions import *

#at each calling of script and requests.get, select random user agent from below list
user_agents = [ 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36", 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"\
] 
USER_AGENT_HEADER = {'User-Agent': random.choice(user_agents)}

#base URL for RestCountries API
rest_countries_base_url = "https://restcountries.com/v3.1/"

#base URL for Country State City API
country_state_city_base_url = "https://api.countrystatecity.in/v1/countries/"

#ignore resource warnings
warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

def export_iso3166_2(alpha_codes: str="", export_folder: str="test-iso3166-2-output", export_filename: str="test-iso3166-2", verbose: bool=1, 
                     export_csv=0, alpha_codes_start_from: str="", rest_countries_keys: str="", exclude_default_keys: str="", state_city_data: bool=False) -> None:
    """
    Export all ISO 3166-2 subdivision related data to JSON and CSV files. The default attributes
    exported for each subdivision include: subdivison code, name, local name, type, parent code, 
    flag URL and latitude/longitude. The flag URL attribute is taken from the custom-built 
    iso3166-flag-icons (https://github.com/amckenna41/iso3166-flag-icons) repo and the 
    latitude/longitude is retrived via the GoogleMaps API. By default all of the subdivision data
    for each ISO 3166 country will be exported but a string of 1 or more country alpha codes can
    be input. 

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

    Finally, there are 7 default attributes exported per each subdivision as mentioned above. 1 or more 
    of these can be excluded for each subdivision if only a subset is required. Simply pass in a string
    of one or more of the attribute as they are exported in the output object: "name", "localName", 
    "type", "parentCode", "flag" and "latLng". Note the country and subdivision code cannot be 
    excluded. 

    Parameters
    ==========
    :alpha_codes: str (default="")
        string of 1 or more 2 letter alpha-2, 3 letter alpha-3 or numeric country codes to extract their 
        latest ISO 3166-2 data.
    :export_folder: str (default="iso3166-2-output")
        output folder to store exported iso3166-2 data.
    :export_filename: str (default="iso3166-2")
        output filename for JSON object with all ISO 3166-2 data.
    :verbose: bool (default=1)
        Set to 1 to print out progress of export functionality, 0 will not print progress.
    :export_csv: bool (default=0)
        Set to 1 to export the ISO 3166-2 dataset to CSV, JSON exported by default.
    :alpha_codes_start_from: str (default="")
        a single ISO 3166-1 alpha-2, alpha-3 or numeric country code to start the export process from.
        The input alpha code will be the first subdivision data to be exported and the remaining codes
        alphabetically following will be exported, those alphabetically before will not be. Any alpha-3
        or numeric codes will be converted into their alpha-2 counterparts.
    :rest_countries_keys: str (default="")
        str of one or more comma separated additional attributes from the RestCountries API that can be 
        appended to each of the subdivisions in the output object. Here is the full list of accepted 
        fields/attributes: "idd", "carSigns", "carSide", "continents", "currencies", "languages", 
                    "postalCode", "region", "startOfWeek", "subregion", "timezones", "tld".
    :exclude_default_keys: str (default="")
        str of one or more of the default keys that are exported for each country's subdivision by default,
        to be excluded from each country's subdivision object. These include: name, localName, type, parentCode, 
        latLng and flag. Note the country and subdivision code keys are required for each subdivision
        and can't be excluded. By default, all of the aforementioned keys will be exported for each subdivision.
                    
    Returns
    =======
    None

    Usage 
    =====
    Please refer to the directory's README.md for usage examples:
    https://github.com/amckenna41/iso3166-2/tree/main/iso3166_2_scripts
    """
    def convert_to_alpha2(alpha_code: str) -> str:
        """ 
        Auxillary function that converts an ISO 3166 country's 3 letter alpha-3 
        or numeric code into its 2 letter alpha-2 counterpart. 

        Parameters 
        ==========
        :alpha3_code: str
            3 letter ISO 3166-1 alpha-3 or numeric country code.
        
        Returns
        =======
        :iso3166.countries_by_alpha3[alpha3_code].alpha2: str
            2 letter ISO 3166 alpha-2 country code. 
        """
        if (alpha_code.isdigit()):
            #return error if numeric code not found
            if not (alpha_code in list(iso3166.countries_by_numeric.keys())):
                return None
            else:
                #use iso3166 package to find corresponding alpha-2 code from its numeric code
                return iso3166.countries_by_numeric[alpha_code].alpha2
    
        #return error if 3 letter alpha-3 code not found
        if not (alpha_code in list(iso3166.countries_by_alpha3.keys())):
            return None
        else:
            #use iso3166 package to find corresponding alpha-2 code from its alpha-3 code
            return iso3166.countries_by_alpha3[alpha_code].alpha2
    
    #raise error if input alpha code prameter is not of correct type
    if not (isinstance(alpha_codes, str)):
        raise TypeError(f"Alpha code input parameter not of correct type, got {type(alpha_codes)}.")

    #split multiple alpha codes into list, remove any whitespace, uppercase
    alpha_codes = alpha_codes.upper().replace(' ', '').split(',')

    #parse input alpha_codes parameter, use all alpha-2 codes if parameter not set
    if (alpha_codes == ['']):
        #use list of all 2 letter alpha-2 codes, according to ISO 3166-1 
        all_alpha2 = sorted(list(iso3166.countries_by_alpha2.keys()))
    else:
        #iterate over all codes, checking they're valid, convert alpha-3 to alpha-2 if applicable
        for code in range(0, len(alpha_codes)):

            #convert 3 letter alpha-3 or numeric code into its 2 letter alpha-2 counterpart
            if len(alpha_codes[code]) == 3:
                alpha_codes[code] = convert_to_alpha2(alpha_codes[code])
            
            #raise error if invalid alpha-2 code found
            if (alpha_codes[code] not in list(iso3166.countries_by_alpha2.keys())):
                raise ValueError(f"Invalid alpha country code input: {alpha_codes[code]}.")
        
        all_alpha2 = sorted(alpha_codes)

    #if 10 or less alpha-2 codes input then append to filename
    if (len(all_alpha2) <= 10):
        export_filename = os.path.splitext(export_filename)[0] + "-" + ",".join(all_alpha2)
    
    #path to json file will be in the main repo dir by default
    export_filepath = os.path.join(export_folder, export_filename)
    
    #append json extension to output filename
    if (os.path.splitext(export_filepath) != ".json"):
        export_filepath = export_filepath + ".json"
    
    #get path to CSV of output data
    csv_filepath = os.path.splitext(export_filepath)[0] + ".csv"
        
    if (verbose):
        print(f"Exporting {len(all_alpha2)} ISO 3166-2 country's data to folder {export_folder}")
        print('################################################################\n')

    #objects to store all country output data in json and csv format
    all_country_data = {}

    #create output dir if doesn't exist
    if not (os.path.isdir(export_folder)):
        os.mkdir(export_folder)

    #start counter
    start = time.time() 
    
    #if less than 5 alpha-2 codes input then don't display progress bar, or print elapsed time
    tqdm_disable = False
    if (len(all_alpha2) < 5):
        tqdm_disable = True

    #reading in, as dataframe, the csv that stores the local names for each subdivision
    local_name_df = pd.read_csv(os.path.join("iso3166_2_updates", "local_names.csv"))
    
    #replace any Nan values with None
    local_name_df = local_name_df.replace(np.nan, None)

    #sort dataframe rows by their country code and reindex rows 
    local_name_df = local_name_df.sort_values('alpha_code').reset_index(drop=True)

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

    #parse input default attributes to exclude from export
    if (exclude_default_keys != ""):
        #list of default output keys/attributes per subdivision 
        exclude_default_keys_expected = ["name", "localName", "type", "parentCode", "latLng", "flag"]

        #parse input attribute string into list, remove whitespace
        exclude_default_keys_converted_list = exclude_default_keys.replace(' ', '').split(',')

        #iterate over all input keys, raise error if invalid key input
        for key in exclude_default_keys_converted_list:
            if not (key in exclude_default_keys_expected):
                raise ValueError(f"Attribute/field ({key}) invalid, please refer to list of the acceptable default attributes below:\n{exclude_default_keys_expected}.")

        exclude_default_keys = exclude_default_keys_converted_list
    
    #get new list of alpha-2 codes that starts alphabetically from inputted starting alpha code, validate and convert to alpha-2 code, if applicable 
    if (alpha_codes_start_from != ""):
        #split multiple alpha codes into list, remove any whitespace, uppercase 
        start_from_alpha_code = alpha_codes_start_from.upper().replace(' ', '').split(',')
        if (len(start_from_alpha_code) != 1):
            pass
        else:
            #convert 3 letter alpha-3 or numeric code into its 2 letter alpha-2 counterpart
            if len(start_from_alpha_code[0]) == 3:
                start_from_alpha_code[0] = convert_to_alpha2(start_from_alpha_code[0])
            
            #raise error if invalid alpha-2 code found
            if (start_from_alpha_code[0] not in list(iso3166.countries_by_alpha2.keys())):
                raise ValueError(f"Invalid alpha country code input: {start_from_alpha_code[0]}.")

            #sort list of alpha-2 codes alphabetically
            sorted_alpha2_list = sorted(list(iso3166.countries_by_alpha2.keys()))

            #get list of alpha codes beginning from input alpha code
            all_alpha2 = sorted(sorted_alpha2_list[sorted_alpha2_list.index(start_from_alpha_code[0]):])

    #iterate over all country codes, getting country and subdivision info, append to json object
    for alpha2 in tqdm(all_alpha2, ncols=50, disable=tqdm_disable):

        #kosovo has no associated subdivisions, manually set params
        if (alpha2 == "XK"):
            country_name = "Kosovo"
            all_subdivisions = []
        else:
            #get country name and list of its subdivisions using pycountry library 
            country_name = pycountry.countries.get(alpha_2=alpha2).name
            all_subdivisions = list(pycountry.subdivisions.get(country_code=alpha2))
        
        #print out progress if verbose set to true
        if (verbose):
            if (tqdm_disable):
                print(f"{country_name} ({alpha2})")
            else:
                print(f" - {country_name} ({alpha2})")

        #create country key in json object
        all_country_data[alpha2] = {}
        
        #make call to RestCountries api if additional rest countries attributes input, raise error if invalid request
        if (rest_countries_keys != ""):
            country_restcountries_response = requests.get(rest_countries_base_url + "alpha/" + alpha2, headers=USER_AGENT_HEADER, timeout=12)
            country_restcountries_response.raise_for_status()
            country_restcountries_data = country_restcountries_response.json()

        #iterate over all countrys' subdivisions, assigning subdivision code, name, type, parent code and flag URL, where applicable for the json object
        for subd in all_subdivisions:
            
            if (verbose):
                print(f"Subdivision: {subd.name} ({subd.code})")        

            #get subdivision coordinates using googlemaps api python client, don't make API call if latLng attribute to be excluded from output
            if ("latLng" in exclude_default_keys):
                gmaps_latlng = []
            else:
                #initialise google maps client with API key, close session
                gmaps = googlemaps.Client(key=os.environ["GOOGLE_MAPS_API_KEY"])
                gmaps.session.close()
                try:
                    gmaps_latlng = gmaps.geocode(subd.name + ", " + country_name, region=alpha2, language="en")
                except Exception as e:
                    print(f"Error thrown when searching for lat/lang of {subd.code} ({subd.name}) for {alpha2} using the GoogleMaps API:\n{e.args[0]}.")

            #set coordinates to None if not found using maps api, round to 3 decimal places
            if (gmaps_latlng != []):
                subdivision_coords = [round(gmaps_latlng[0]['geometry']['location']['lat'], 3), round(gmaps_latlng[0]['geometry']['location']['lng'], 3)]
            else:
                subdivision_coords = None

            #raise error if subdivision code already in output object
            if (subd.code in list(all_country_data[alpha2].keys())):
                raise ValueError(f"Subdivision code already present in output object: {subd.code}.")

            #initialise subdivision code object and its attributes
            all_country_data[alpha2][subd.code] = {}
            all_country_data[alpha2][subd.code]["name"] = subd.name
            all_country_data[alpha2][subd.code]["localName"] = None
            all_country_data[alpha2][subd.code]["type"] = subd.type
            all_country_data[alpha2][subd.code]["parentCode"] = subd.parent_code
            all_country_data[alpha2][subd.code]["latLng"] = subdivision_coords
                        
            #don't request.get flag URL if attribute excluded in exclude_default_keys parameter
            if not ("flag" in exclude_default_keys):
                all_country_data[alpha2][subd.code]["flag"] = get_flag_icons_url(alpha2, subd.code)
            else:
                all_country_data[alpha2][subd.code]["flag"] = None #temporary key for flag URL attribute 

            #append rest country key data to country output object if inputted
            if (rest_countries_keys != ""):
                for key in rest_countries_keys:
                    #some rest country object data is in nested dict
                    if (key == "carSigns"):
                        all_country_data[alpha2][subd.code][key] = country_restcountries_data[0]["car"]["signs"]
                    elif (key == "carSides"):
                        all_country_data[alpha2][subd.code][key] = country_restcountries_data[0]["car"]["side"]
                    elif (key == "postalCode"):
                        all_country_data[alpha2][subd.code][key] = "Format: " + country_restcountries_data[0]["postalCode"]["format"] + ", Regex: "  + country_restcountries_data[0]["postalCode"]["regex"]
                    else:
                        all_country_data[alpha2][subd.code][key] = country_restcountries_data[0][key]
                                            
                    #if attribute is list convert into str
                    if (isinstance(all_country_data[alpha2][subd.code][key], list)):
                        all_country_data[alpha2][subd.code][key] = ','.join(all_country_data[alpha2][subd.code][key])

            #reorder keys of subdivision object into alphabetical order
            all_country_data[alpha2][subd.code] = dict(OrderedDict(natsort.natsorted(all_country_data[alpha2][subd.code].items())))

            #iterate over each default attribute to be excluded from subdivision object, delete key, if applicabale 
            if (exclude_default_keys != ""):
                for key in exclude_default_keys:
                    del all_country_data[alpha2][subd.code][key]

        #sort subdivision codes in json objects in natural alphabetical/numerical order using natsort library
        all_country_data[alpha2] = dict(OrderedDict(natsort.natsorted(all_country_data[alpha2].items())))
        
    #write json data with all country info to json output file
    with open(export_filepath, 'w', encoding='utf-8') as f:
        json.dump(all_country_data, f, ensure_ascii=False, indent=4)

    #read json data with all current subdivision data
    with open(export_filepath, 'r', encoding='utf-8') as input_json:
        all_country_data = json.load(input_json)

    #append latest subdivision updates/changes from /iso3166_2_updates folder to the iso3166-2 object
    all_country_data = update_subdivision(iso3166_2_filename=export_filepath, subdivision_csv=os.path.join("iso3166_2_updates", "subdivision_updates.csv"), export=0, 
                                          exclude_default_keys=exclude_default_keys, rest_countries_keys=rest_countries_keys)

    #get local Name data for each subdivision, unless localName or name attributes to be excluded from export
    if (exclude_default_keys == "" or not ("localName" in exclude_default_keys or "name" in exclude_default_keys)):
        all_country_data = add_local_names(all_country_data)

    #write json data with all updated country info, including local name, to json output file
    with open(export_filepath, 'w', encoding='utf-8') as f:
        json.dump(all_country_data, f, ensure_ascii=False, indent=4)

    #export dataset to CSV if bool set to True
    if (export_csv):
        #initialise array to store each individual subdivision object
        all_country_csv = []

        #iterate over country data object, for each subdivision object append its subdivision and country code, append subdivision object to array 
        for country in all_country_data:
            for subd in all_country_data[country]:
                temp_all_country_data = all_country_data[country][subd].copy()
                temp_all_country_data["subdivision_code"] = subd
                temp_all_country_data["alpha_code"] = country
                all_country_csv.append(temp_all_country_data)
        
        #convert array of objects into a dataframe with each subdivision being a row, reorder columns and sort by subdivision then country code
        all_country_csv_df = pd.DataFrame(all_country_csv)
        
        #standard default column list without RestCountries attributes
        all_country_csv_df_standard_cols = ['alpha_code', 'subdivision_code', 'name', 'localName', 'type', 'parentCode', 'flag', 'latLng']
        
        #set standard column list without RestCountries attributes, remove any default attributes if applicable
        if (exclude_default_keys != ""):
            for key in exclude_default_keys:
                all_country_csv_df_standard_cols.remove(key)

        #sort/reindex columns with or without the addtional RestCountries attributes
        if (rest_countries_keys == ""):
            all_country_csv_df = all_country_csv_df.reindex(columns=all_country_csv_df_standard_cols)
            # all_country_csv_df = all_country_csv_df.reindex(columns=['alpha_code', 'subdivision_code', 'name', 'localName', 'type', 'parentCode', 'flag', 'latLng'])
        else:
            rest_country_cols = sorted(rest_countries_keys) #sort RestCountries attributes alphabetically
            all_country_csv_df = all_country_csv_df.reindex(columns=all_country_csv_df_standard_cols+rest_country_cols)
        
        #reindex columns based on subdivision and country code columns, drop index col
        all_country_csv_df = all_country_csv_df.sort_values('subdivision_code').reset_index(drop=True)
        all_country_csv_df = all_country_csv_df.sort_values('alpha_code').reset_index(drop=True)

        #export dataframe of subdivision objects to CSV
        all_country_csv_df.to_csv(csv_filepath, index=False)

    #stop counter and calculate elapsed time
    end = time.time()           
    elapsed = end - start
    
    if (verbose):
        print('\n##########################################################\n')
        print(f"ISO 3166 data successfully exported to {export_filepath}.")
        print("\nElapsed Time for exporting all ISO 3166-2 data: {0:.2f} minutes.".format(elapsed / 60))

if __name__ == '__main__':

    #parse input arguments using ArgParse 
    parser = argparse.ArgumentParser(description='Script for exporting ISO 3166-1 country and subdivision data.')

    parser.add_argument('-alpha_codes', '--alpha_codes', type=str, required=False, default="", 
        help='One or more ISO 3166-1 alpha-2, alpha-3 or numeric country codes, by default all ISO 3166-2 subdivision data for all countries will be exported.')
    parser.add_argument('-export_filename', '--export_filename', type=str, required=False, default="test_iso3166-2", 
        help='Output filename for iso3166-2 object.')
    parser.add_argument('-export_folder', '--export_folder', type=str, required=False, default="test_iso3166-2", 
        help='Output folder to store output objects.')
    parser.add_argument('-export_csv', '--export_csv', required=False, action=argparse.BooleanOptionalAction, default=1, 
        help='Set to 1 to export ISO 3166-2 dataset to CSV, JSON is only exported by default.')
    parser.add_argument('-verbose', '--verbose', required=False, action=argparse.BooleanOptionalAction, default=1, 
        help='Set to 1 to print out progress of export function, 0 will not print progress.')
    parser.add_argument('-alpha_codes_start_from', '--alpha_codes_start_from', type=str, required=False, default="", 
        help='Beginning alpha code to start the export functionality from, alphabetically.')
    parser.add_argument('-rest_countries_keys', '--rest_countries_keys', type=str, required=False, default="", 
        help='List of additional fields/attributes from RestCountries API to be added to each subdivision object.')
    parser.add_argument('-exclude_default_keys', '--exclude_default_keys', type=str, required=False, default="", 
        help="List of default fields/attributes to be excluded from each country's subdivision object.")
    
    #parse input args
    args = parser.parse_args()
    alpha_codes = args.alpha_codes
    export_folder = args.export_folder
    export_filename = args.export_filename
    export_csv = args.export_csv
    verbose = args.verbose
    rest_countries_keys = args.rest_countries_keys
    exclude_default_keys = args.exclude_default_keys
    alpha_codes_start_from = args.alpha_codes_start_from

    export_iso3166_2(alpha_codes=alpha_codes, export_folder=export_folder, export_filename=export_filename, verbose=verbose, export_csv=export_csv,
                     alpha_codes_start_from=alpha_codes_start_from, rest_countries_keys=rest_countries_keys, exclude_default_keys=exclude_default_keys)