"""
Download all ISO3166-2 data using the restcountries api, export all data
to JSON files. 

This module is working and done.
"""
import os
import sys
import json
import argparse
import requests
import logging
import getpass
import pycountry
import iso3166
from tqdm import tqdm

#initialise logging library 
__version__ = "0.0.2"
log = logging.getLogger(__name__)

#initalise User-agent header for requests library 
USER_AGENT_HEADER = {'User-Agent': 'iso3166-2/{} ({}; {})'.format(__version__,
                                       'https://github.com/amckenna41/iso3166-2', getpass.getuser())}


def export_iso3166_2(output_folder="", json_filename=""):
    """
    Export the two ISO3166-2 jsons with fields including all subdivisions related data using the pycountry
    library and all country data using the restcountries api (https://restcountries.com/). The 
    iso3166-2.json stores all country data + subdivisions data, the iso3166-2-min.json contains just 
    country name, 2 letter alpha2 code and subdivisions.

    Parameters
    ----------
    :output_folder : str (default = "")
        output folder to store exported iso3166-2 jsons.
    :json_filename : str (default = "")
        filename for both country data json exports. 

    Returns
    -------
    None
    """
    #append .json to filename if just filename input
    if (os.path.splitext(json_filename)[1] == ''):
        json_filename = json_filename + ".json"

    #path to json file will be in the main repo dir by default
    json_filepath = os.path.join(output_folder, json_filename)
    json_min_filepath = os.path.join(output_folder, os.path.splitext(json_filename)[0] + '-min.json')

    #get list of all 2 letter alpha2 codes
    all_alpha2 = sorted(list(iso3166.countries_by_alpha2.keys()))

    print("Exporting {} ISO3166-2 country data JSON {} to folder {}.".format
        (len(all_alpha2), json_filepath, output_folder))

    #base url for rest countries api
    base_restcountries_url = "https://restcountries.com/v3.1/alpha/"

    #base url for flag icons repo
    flag_icons_base_url = "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/"

    #objects to store all country output data
    all_country_data = {}
    all_country_data_min = {}

    #create output dir if doesnt exist
    if not (os.path.isdir(output_folder)):
        os.mkdir(output_folder)

    #iterate over all country codes, getting country and subdivision info, append to json objects
    for alpha2 in tqdm(all_alpha2, unit=" ", position=0, 
        desc="Alpha2 Country Codes", mininterval=45):
        
        #get rest countries api url 
        country_url = base_restcountries_url + alpha2.upper()

        #get country info from restcountries api
        rest_countries_response = requests.get(country_url, stream=True, headers=USER_AGENT_HEADER)
        
        #if endpoint returns a non 200 status code skip to next iteration
        if (rest_countries_response.status_code != 200):
            continue

        #kosovo not in pycountry package as it has no associated subdivisions, manually set params
        if (alpha2 == "XK"):
            countryName = "Kosovo"
            allSubdivisions = []
        else:
            #get country name and list of its subdivisions using pycountry library 
            countryName = pycountry.countries.get(alpha_2=alpha2).name
            allSubdivisions = list(pycountry.subdivisions.get(country_code=alpha2))

        print("{} ({})".format(countryName, alpha2))

        #add all country data from rest countries api response to json object
        all_country_data[alpha2] = rest_countries_response.json()[0]
        
        #for min json object, create empty object with alpha2 as key
        all_country_data_min[alpha2] = {}

        #create subdivisions and country name keys in json objects
        all_country_data[alpha2]["subdivisions"] = {}
        # all_country_data_min[alpha2]["name"] = countryName
        # all_country_data_min[alpha2]["subdivisions"] = {}
        
        sortedDict = {}

        #iterate over all countrys' subdivisions, assigning subdiv code, name, type and parent code, where applicable
        #for both json objects
        for subd in allSubdivisions:
            all_country_data[alpha2]["subdivisions"][subd.code] = {}
            all_country_data[alpha2]["subdivisions"][subd.code]["name"] = subd.name
            all_country_data[alpha2]["subdivisions"][subd.code]["type"] = subd.type
            all_country_data[alpha2]["subdivisions"][subd.code]["parent_code"] = subd.parent_code

            # all_country_data_min[alpha2]["subdivisions"][subd.code] = {}
            # all_country_data_min[alpha2]["subdivisions"][subd.code]["name"] = subd.name
            # all_country_data_min[alpha2]["subdivisions"][subd.code]["type"] = subd.type
            # all_country_data_min[alpha2]["subdivisions"][subd.code]["parent_code"] = subd.parent_code
            all_country_data_min[alpha2][subd.code] = {}
            all_country_data_min[alpha2][subd.code]["name"] = subd.name
            all_country_data_min[alpha2][subd.code]["type"] = subd.type
            all_country_data_min[alpha2][subd.code]["parent_code"] = subd.parent_code

            #url to flag in iso3166-flag-icons repo
            alpha2_flag_url = flag_icons_base_url + alpha2 + "/" + subd.code + ".svg"
            
            #if subdivision has an valid flag in flag icons repo set to its Github url
            if (requests.get(alpha2_flag_url, headers=USER_AGENT_HEADER).status_code != 404):
                all_country_data[alpha2]["subdivisions"][subd.code]["flag_url"] = alpha2_flag_url
                all_country_data_min[alpha2][subd.code]["flag_url"] = alpha2_flag_url
            else:
                all_country_data[alpha2]["subdivisions"][subd.code]["flag_url"] = None
                all_country_data_min[alpha2][subd.code]["flag_url"] = None

        #sort subdivision codes in json objects in alphabetical/numerical order
        all_country_data[alpha2]["subdivisions"] = dict(sorted(all_country_data[alpha2]["subdivisions"].items()))
        # all_country_data_min[alpha2]["subdivisions"] = dict(sorted(all_country_data_min[alpha2]["subdivisions"].items()))
        all_country_data_min[alpha2] = dict(sorted(all_country_data_min[alpha2].items()))

    #write json data with all country info to json output file
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(all_country_data, f, ensure_ascii=False, indent=4)

    #write min json data with subdivision info to output file
    with open(json_min_filepath, 'w', encoding='utf-8') as f:
        json.dump(all_country_data_min, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':

    #parse input arguments using ArgParse 
    parser = argparse.ArgumentParser(description='Script for exporting iso3166-2 data using pycountry package and restcountries api.')

    parser.add_argument('-json_filename', '--json_filename', type=str, required=False, default="test-iso3166-2.json", 
        help='Output filename for both iso3166-2 jsons.')
    parser.add_argument('-output_folder', '--output_folder', type=str, required=False, default="test-iso3166_2", 
        help='Output folder to store output jsons.')

    #parse input args
    args = parser.parse_args()
    output_folder = args.output_folder
    json_filename = args.json_filename

    export_iso3166_2(output_folder=output_folder, json_filename=json_filename)