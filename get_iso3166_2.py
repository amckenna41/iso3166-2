import os
import time
import json
import argparse
import requests
import getpass
import pycountry
import iso3166
import iso3166_2 as iso
import googlemaps
from tqdm import tqdm
import natsort
from collections import OrderedDict

#initialise version 
__version__ = "1.2.2"

#initalise User-agent header for requests library 
USER_AGENT_HEADER = {'User-Agent': 'iso3166-2/{} ({}; {})'.format(__version__,
                                       'https://github.com/amckenna41/iso3166-2', getpass.getuser())}

#initialise google maps client 
gmaps = googlemaps.Client(key=os.environ["GOOGLE_MAPS_API_KEY"])

#list of data attributes supported by software
attribute_list = [
    "altSpellings", "area", "borders", "capital", "capitalInfo", "car", "cca2", "cca3", "ccn3", "cioc", "coatOfArms",
    "continents", "currencies", "demonyms", "fifa", "flag", "flags", "gini", "idd", "independent", "landlocked",
    "languages", "latlng", "maps", "name", "population", "postalCode", "region", "startOfWeek", "status", 
    "subdivisions", "subregion", "timezones", "tld", "translations", "unMember"
]

def export_iso3166_2(alpha2_codes="", output_folder="test-iso3166-2-output", json_filename="test-iso3166-2", verbose=1):
    """
    Export the two ISO 3166-2 jsons with fields including all subdivision related data using the pycountry
    library and all country data using the restcountries api (https://restcountries.com/). Also get the
    lat/longitude info for each country and subdivision using the Google Maps API. The iso3166-2.json stores 
    all country data + subdivisions data, the iso3166-2-min.json contains just country name, 2 letter alpha-2 
    code and subdivisions info. The full list of attributes exported can be viewed in the ATTRIBUTES.md file.

    Parameters
    ==========
    :alpha2_codes: str (default="")
        string of 1 or more 2 letter alpha-2 country codes to pull their latest ISO 3166-2 data.
    :output_folder : str (default="iso3166-2-output")
        output folder to store exported iso3166-2 jsons.
    :json_filename : str (default="iso3166-2")
        filename for both country data json exports. 
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

    #parse input alpha2_codes parameter, use all alpha-2 codes if parameter not set
    if (alpha2_codes == ['']):
        #use list of all 2 letter alpha-2 codes, according to ISO 3166-1 
        all_alpha2 = sorted(list(iso3166.countries_by_alpha2.keys()))
    else:
        #iterate over all codes, validating they're valid, convert alpha-3 to alpha-2 if applicable
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

    #append .json to filename if just filename input
    if (os.path.splitext(json_filename)[1] == ''):
        json_filename = json_filename + ".json"
    
    #path to json file will be in the main repo dir by default
    json_filepath = os.path.join(output_folder, json_filename)
    json_min_filepath = os.path.join(output_folder, os.path.splitext(json_filename)[0] + '-min.json')
    
    if (verbose):
        print("Exporting {} ISO 3166-2 country's data to folder {}.".format(len(all_alpha2), output_folder))
        print('#################################################################\n')

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

    #start counter
    start = time.time() 

    #if less than 5 input alpha-2 codes then don't display progress bar, or print elapsed time
    tqdm_disable = False
    if (len(all_alpha2) < 5):
        tqdm_disable = True

    #iterate over all country codes, getting country and subdivision info, append to json objects
    for alpha2 in tqdm(all_alpha2, ncols=50, disable=tqdm_disable):
        
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
        
        #print out progress if verbose set to true
        if (verbose):
            if (tqdm_disable):
                print("{} ({})".format(countryName, alpha2))
            else:
                print(" - {} ({})".format(countryName, alpha2))

        #add all country data from rest countries api response to json object
        all_country_data[alpha2] = rest_countries_response.json()[0]

        #round latitude/longitude coords to 3 decimal places
        all_country_data[alpha2]["latlng"] = [round(all_country_data[alpha2]["latlng"][0], 3), round(all_country_data[alpha2]["latlng"][1], 3)]

        #round area (km^2) to nearest whole number
        all_country_data[alpha2]["area"] = int(all_country_data[alpha2]["area"])

        #for min json object, create empty object with alpha-2 as key
        all_country_data_min[alpha2] = {}

        #create subdivisions and country name keys in json objects
        all_country_data[alpha2]["subdivisions"] = {}
        
        #iterate over all countrys' subdivisions, assigning subdiv code, name, type and parent code and flag URL, 
        # where applicable for both json objects
        for subd in allSubdivisions:
            
            #get subdivision coordinates using googlemaps api python client
            gmaps_latlng = gmaps.geocode(subd.name + ", " + countryName, region=alpha2, language="en")
            
            #set coordinates to None if not found using maps api, round to 3 decimal places
            if (gmaps_latlng != []):
                subdivision_coords = [round(gmaps_latlng[0]['geometry']['location']['lat'], 3), round(gmaps_latlng[0]['geometry']['location']['lng'], 3)]
            else:
                subdivision_coords = None

            all_country_data[alpha2]["subdivisions"][subd.code] = {}
            all_country_data[alpha2]["subdivisions"][subd.code]["name"] = subd.name
            all_country_data[alpha2]["subdivisions"][subd.code]["type"] = subd.type
            all_country_data[alpha2]["subdivisions"][subd.code]["parent_code"] = subd.parent_code
            all_country_data[alpha2]["subdivisions"][subd.code]["latlng"] = subdivision_coords

            all_country_data_min[alpha2][subd.code] = {}
            all_country_data_min[alpha2][subd.code]["name"] = subd.name
            all_country_data_min[alpha2][subd.code]["type"] = subd.type
            all_country_data_min[alpha2][subd.code]["parent_code"] = subd.parent_code
            all_country_data_min[alpha2][subd.code]["latlng"] = subdivision_coords

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
                            all_country_data[alpha2]["subdivisions"][subd.code]["flag_url"] = alpha2_flag_url + flag_file_extensions[extension]
                            all_country_data_min[alpha2][subd.code]["flag_url"] = alpha2_flag_url + flag_file_extensions[extension]
                            break
                        elif (extension == 4):
                            all_country_data[alpha2]["subdivisions"][subd.code]["flag_url"] = None
                            all_country_data_min[alpha2][subd.code]["flag_url"] = None
            else:
                    all_country_data[alpha2]["subdivisions"][subd.code]["flag_url"] = None
                    all_country_data_min[alpha2][subd.code]["flag_url"] = None

        #if attribute value found for country, set it's value to NA
        for attribute in attribute_list:
            if not (attribute in list(all_country_data[alpha2].keys())):
                all_country_data[alpha2][attribute] = "NA"

        #sort subdivision codes in json objects in natural alphabetical/numerical order using natsort library
        all_country_data[alpha2]["subdivisions"] = dict(OrderedDict(natsort.natsorted(all_country_data[alpha2]["subdivisions"].items())))
        all_country_data_min[alpha2] = dict(OrderedDict(natsort.natsorted(all_country_data_min[alpha2].items())))

        #sort keys in main output dict into alphabetical order
        all_country_data[alpha2] = {key: value for key, value in sorted(all_country_data[alpha2].items())}

    #write json data with all country info to json output file
    with open(json_filepath, 'w', encoding='utf-8') as f:
        if (len(all_alpha2) == 1):
            json.dump(all_country_data[all_alpha2[0]], f, ensure_ascii=False, indent=4)
        else:
            json.dump(all_country_data, f, ensure_ascii=False, indent=4)

    #dont export min json if no subdivisions listed
    if (any(all_country_data_min.values())):
        #write min json data with subdivision info to output file
        with open(json_min_filepath, 'w', encoding='utf-8') as f:
            if (len(all_alpha2) == 1):
                json.dump(all_country_data_min[all_alpha2[0]], f, ensure_ascii=False, indent=4)
            else:
                json.dump(all_country_data_min, f, ensure_ascii=False, indent=4)

    #stop counter and calculate elapsed time
    end = time.time()           
    elapsed = end - start
    
    if (verbose and not tqdm_disable):
        print('\n##########################################################\n')
        print("ISO 3166 data successfully exported the following files to the {} folder:\n{} and {}.".format(output_folder, json_filepath, json_min_filepath))
        print('\nElapsed Time for exporting all ISO 3166-2 data: {0:.2f} minutes.'.format(elapsed / 60))

if __name__ == '__main__':

    #parse input arguments using ArgParse 
    parser = argparse.ArgumentParser(description='Script for exporting iso3166-2 country data using pycountry package and restcountries api.')

    parser.add_argument('-alpha2_codes', '--alpha2_codes', type=str, required=False, default="", 
        help='One or more 2 letter alpha-2 country codes, by default all ISO 3166-2 data for all countries will be exported.')
    parser.add_argument('-json_filename', '--json_filename', type=str, required=False, default="test_iso3166-2.json", 
        help='Output filename for both iso3166-2 jsons.')
    parser.add_argument('-output_folder', '--output_folder', type=str, required=False, default="test_iso3166-2", 
        help='Output folder to store output jsons.')
    parser.add_argument('-verbose', '--verbose', required=False, action=argparse.BooleanOptionalAction, default=1, 
        help='Set to 1 to print out progress of export json function, 0 will not print progress.')

    #parse input args
    args = parser.parse_args()
    alpha2_codes = args.alpha2_codes
    output_folder = args.output_folder
    json_filename = args.json_filename
    verbose = args.verbose

    export_iso3166_2(alpha2_codes=alpha2_codes, output_folder=output_folder, json_filename=json_filename, verbose=verbose)