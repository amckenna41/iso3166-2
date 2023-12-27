import os
import time
import json
import argparse
import requests
import getpass
from importlib.metadata import metadata
import pycountry
import iso3166
import googlemaps
from tqdm import tqdm
import natsort
from collections import OrderedDict
import pandas as pd
import numpy as np
from .update_subdivisions import *

#initialise version 
__version__ = metadata('iso3166-2')['version']

#initalise User-agent header for requests library 
USER_AGENT_HEADER = {'User-Agent': 'iso3166-2/{} ({}; {})'.format(__version__,
                                       'https://github.com/amckenna41/iso3166-2', getpass.getuser())}

#initialise google maps client with API key
gmaps = googlemaps.Client(key=os.environ["GOOGLE_MAPS_API_KEY"])

def export_iso3166_2(alpha2_codes="", output_folder="test-iso3166-2-output", json_filename="test-iso3166-2", verbose=1):
    """
    Export all ISO 3166-2 subdivision related data using the ISO 3166-2 library to a JSON. Also get the
    lat/longitude info for each subdivision using the Google Maps API. The iso3166-2.json stores all
    the subdivision data including: subdivison code, name, type, parent code, flag and latitude/longitude.

    The generated JSON is used as a baseline for the ISO 3166-2 data object, but additional and more 
    up-to-date and accurate data is added with the help of the iso3166-updates software/API 
    (https://github.com/amckenna41/iso3166-updates).

    Parameters
    ==========
    :alpha2_codes: str (default="")
        string of 1 or more 2 letter alpha-2 country codes to extract their latest ISO 3166-2 data.
    :output_folder: str (default="iso3166-2-output")
        output folder to store exported iso3166-2 data.
    :json_filename: str (default="iso3166-2")
        output filename for JSON object with all ISO 3166-2 data.
    :verbose: int (default=1)
        Set to 1 to print out progress of export functionality, 0 will not print progress.

    Returns
    =======
    None
    """
    def convert_to_alpha2(alpha3_code):
        """ 
        Convert an ISO 3166 country's 3 letter alpha-3 code into its 2 letter
        alpha-2 counterpart. 

        Parameters 
        ==========
        :alpha3_code: str
            3 letter ISO 3166-1 alpha-3 country code.
        
        Returns
        =======
        :iso3166.countries_by_alpha3[alpha3_code].alpha2: str
            2 letter ISO 3166 alpha-2 country code. 
        """
        #return None if 3 letter alpha-3 code not found
        if not (alpha3_code in list(iso3166.countries_by_alpha3.keys())):
            return None
        else:
            #use iso3166 package to find corresponding alpha-2 code from its alpha-3 code
            return iso3166.countries_by_alpha3[alpha3_code].alpha2
    
    #split multiple alpha-2 codes into list, remove any whitespace
    alpha2_codes = alpha2_codes.replace(' ', '').split(',')

    #bool to keep track if getting data for all countries
    using_all_data = False

    #parse input alpha2_codes parameter, use all alpha-2 codes if parameter not set
    if (alpha2_codes == ['']):
        #use list of all 2 letter alpha-2 codes, according to ISO 3166-1 
        all_alpha2 = sorted(list(iso3166.countries_by_alpha2.keys()))
        using_all_data = True
    else:
        #iterate over all codes, checking they're valid, convert alpha-3 to alpha-2 if applicable
        for code in range(0, len(alpha2_codes)):

            #convert 3 letter alpha-3 code into its 2 letter alpha-2 counterpart
            if len(alpha2_codes[code]) == 3:
                alpha2_codes[code] = convert_to_alpha2(alpha2_codes[code])
            
            #raise error if invalid alpha-2 code found
            if (alpha2_codes[code] not in list(iso3166.countries_by_alpha2.keys())):
                raise ValueError("Input alpha-2 country code {} not found.".format(alpha2_codes[code]))
        
        all_alpha2 = alpha2_codes

    #if 10 or less alpha-2 codes input then append to filename
    if (len(all_alpha2) <= 10):
        json_filename = os.path.splitext(json_filename)[0] + "-" + ",".join(all_alpha2)
    
    #path to json file will be in the main repo dir by default
    json_filepath = os.path.join(output_folder, json_filename)
    
    #append json extension to output filename
    if (os.path.splitext(json_filepath) != ".json"):
        json_filepath = json_filepath + ".json"
        
    if (verbose):
        print("Exporting {} ISO 3166-2 country's data to folder {}".format(len(all_alpha2), output_folder))
        print('################################################################\n')

    #objects to store all country output data
    all_country_data = {}

    #create output dir if doesn't exist
    if not (os.path.isdir(output_folder)):
        os.mkdir(output_folder)

    #start counter
    start = time.time() 
    
    #if less than 5 alpha-2 codes input then don't display progress bar, or print elapsed time
    tqdm_disable = False
    if (len(all_alpha2) < 5):
        tqdm_disable = True

    #base url for flag icons repo
    flag_icons_base_url = "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/"

    #reading in, as dataframe, the csv that stores the local names for each subdivision
    local_name_df = pd.read_csv(os.path.join("iso3166-2-updates", "local_names.csv"))
    
    #replace any Nan values with None
    local_name_df = local_name_df.replace(np.nan, None)

    #sort dataframe rows by their country code and reindex rows 
    local_name_df = local_name_df.sort_values('country_code').reset_index(drop=True)
    
    #iterate over all country codes, getting country and subdivision info, append to json objects
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
                print("{} ({})".format(country_name, alpha2))
            else:
                print(" - {} ({})".format(country_name, alpha2))

        #create country key in json object
        all_country_data[alpha2] = {}
        
        #iterate over all countrys' subdivisions, assigning subdiv code, name, type and parent code and flag URL, where applicable for the json object
        for subd in all_subdivisions:
            
            #get subdivision coordinates using googlemaps api python client
            gmaps_latlng = gmaps.geocode(subd.name + ", " + country_name, region=alpha2, language="en")
            # gmaps_latlng = []
            #set coordinates to None if not found using maps api, round to 3 decimal places
            if (gmaps_latlng != []):
                subdivision_coords = [round(gmaps_latlng[0]['geometry']['location']['lat'], 3), round(gmaps_latlng[0]['geometry']['location']['lng'], 3)]
            else:
                subdivision_coords = None

            #initialise subdivision code object
            all_country_data[alpha2][subd.code] = {}
            all_country_data[alpha2][subd.code]["name"] = subd.name
            all_country_data[alpha2][subd.code]["localName"] = None
            all_country_data[alpha2][subd.code]["type"] = subd.type
            all_country_data[alpha2][subd.code]["parentCode"] = subd.parent_code
            all_country_data[alpha2][subd.code]["latLng"] = subdivision_coords
            
            #list of flag file extensions in order of preference 
            flag_file_extensions = ['.svg', '.png', '.jpeg', '.jpg', '.gif']
            
            #url to flag in iso3166-flag-icons repo
            alpha2_flag_url = flag_icons_base_url + alpha2 + "/" + subd.code
            
            #verify that path on flag icons repo exists, if not set flag url value to None
            if (requests.get(flag_icons_base_url + alpha2, headers=USER_AGENT_HEADER).status_code != 404):
                
                #iterate over all image extensions checking existence of flag in repo
                for extension in range(0, len(flag_file_extensions)):
                    
                        #if subdivision has a valid flag in flag icons repo set to its GitHub url, else set to None
                        if (requests.get(alpha2_flag_url + flag_file_extensions[extension], headers=USER_AGENT_HEADER).status_code != 404):
                            all_country_data[alpha2][subd.code]["flagUrl"] = alpha2_flag_url + flag_file_extensions[extension]
                            break
                        elif (extension == 4):
                            all_country_data[alpha2][subd.code]["flagUrl"] = None
            else:
                all_country_data[alpha2][subd.code]["flagUrl"] = None

            #reorder keys of each subdivision object
            all_country_data[alpha2][subd.code] = {k: all_country_data[alpha2][subd.code][k] for k in ["name", "localName", "type", "parentCode", "flagUrl", "latLng"]}

        #sort subdivision codes in json objects in natural alphabetical/numerical order using natsort library
        all_country_data[alpha2] = dict(OrderedDict(natsort.natsorted(all_country_data[alpha2].items())))

        #sort keys in main output dict into alphabetical order
        # all_country_data[alpha2] = {key: value for key, value in sorted(all_country_data[alpha2].items())}

    #write json data with all country info to json output file
    with open(json_filepath, 'w', encoding='utf-8') as f:
        # if (len(all_alpha2) == 1): json.dump(all_country_data[all_alpha2[0]], f, ensure_ascii=False, indent=4) else: #all outputs will have country code as key
        json.dump(all_country_data, f, ensure_ascii=False, indent=4)

    #read json data with all current subdivision data
    with open(json_filepath, 'r', encoding='utf-8') as input_json:
        all_country_data = json.load(input_json)

    #call update_subdivision() function if using all alpha-2 codes
    if (using_all_data):
        #append latest subdivision updates/changes from /iso3166-2-updates folder to the iso3166-2 object
        all_country_data = update_subdivision(iso3166_2_filename=json_filepath, subdivision_csv=os.path.join("iso3166-2-updates", "subdivision_updates.csv"), export=0)

    #add local names for each subdivision from local_names.csv file    
    all_country_data = add_local_names(all_country_data)

    #write json data with all updated country info, including local name, to json output file
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(all_country_data, f, ensure_ascii=False, indent=4)

    #stop counter and calculate elapsed time
    end = time.time()           
    elapsed = end - start
    
    if (verbose):
        print('\n##########################################################\n')
        print("ISO 3166 data successfully exported to {}.".format(json_filepath))
        print('\nElapsed Time for exporting all ISO 3166-2 data: {0:.2f} minutes.'.format(elapsed / 60))

if __name__ == '__main__':

    #parse input arguments using ArgParse 
    parser = argparse.ArgumentParser(description='Script for exporting iso3166-2 country data using pycountry package.')

    parser.add_argument('-alpha2_codes', '--alpha2_codes', type=str, required=False, default="", 
        help='One or more 2 letter alpha-2 country codes, by default all ISO 3166-2 subdivision data for all countries will be exported.')
    parser.add_argument('-json_filename', '--json_filename', type=str, required=False, default="test_iso3166-2", 
        help='Output filename for both iso3166-2 JSON.')
    parser.add_argument('-output_folder', '--output_folder', type=str, required=False, default="test_iso3166-2", 
        help='Output folder to store output JSON.')
    parser.add_argument('-verbose', '--verbose', required=False, action=argparse.BooleanOptionalAction, default=1, 
        help='Set to 1 to print out progress of export json function, 0 will not print progress.')

    #parse input args
    args = parser.parse_args()
    alpha2_codes = args.alpha2_codes
    output_folder = args.output_folder
    json_filename = args.json_filename
    verbose = args.verbose

    export_iso3166_2(alpha2_codes=alpha2_codes, output_folder=output_folder, json_filename=json_filename, verbose=verbose)