import os
import json
import iso3166
import natsort
from collections import OrderedDict
import argparse
import random
import pandas as pd
import requests
import numpy as np
from datetime import datetime

#at each calling of script and requests.get, select random user agent from below list
user_agents = [ 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36", 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"
] 

#base url for RestCountries URL
rest_countries_base_url = "https://restcountries.com/v3.1/"

def update_subdivision(alpha_code: str="", subdivision_code: str="", name: str="", local_name: str="", type_: str="", lat_lng: list|str=None, parent_code: str="", 
                       flag: str="", delete: bool=0, iso3166_2_filename: str=os.path.join("iso3166_2", "iso3166-2.json"), 
                       subdivision_csv: str="", rest_countries_keys: str="", exclude_default_keys: str="", export: bool=1) -> dict:
    """
    Auxillary function created to streamline the addition, amendment and or deletion 
    of subdivisions in/from the iso3166-2.json object. There are two main ways at 
    which to add or make changes to the subdivision data. Firstly, this function 
    can accept all of the attributes that are available per each subdivision: 
    subdivision code, local name, name, type, parent_code, latitude/longitude, 
    flag. Secondly, a CSV of individual rows of subdivision changes to be made 
    with all of the aforementioned attributes as columns. This is the recommended 
    and fastest approach as it allows for hundreds of potential changes to be made 
    to the object in one file and command. 
    
    The CSV file (iso3166_2_updates/subdivision_updates.csv) has the following 
    columns for each subdivision change: alpha_code, code, name, localName, type, 
    parentCode, flag, latLng, localNameSame, delete, notes and dateIssued. 
    Although, some of the default aforementioned columns may be excluded via the 
    "exclude_default_keys" parameter, meaning they will not be present in the CSV 
    file columns. When creating a row in the CSV, the country code and subdivision
    code columns are required, otherwise an error will be thrown.
    
    If deleting an existing subdivision, the subdivision details should be passed 
    into the function alongside setting the delete input parameter to 1. Similarly,
    in the CSV file, there is a delete column which should be set to 1 if deleting
    the subdivision specified in the row.

    For both of the above methods, the existing ISO 3166-2 object with all the 
    subdivision data is duplicated/archived in case of any errors made when 
    making changes/updates to the subdivision data. After all the unit tests for 
    the software have completed and passed successfully, the archived data object 
    is deleted.
    
    Parameters
    ==========
    :alpha_code: str (default="")
        ISO 3166-1 alpha-2, alpha-3 or numeric country code.
    :subdivision_code: str (default="")
        subdivision code as per the ISO 3166-2.
    :name: str (default="")
        subdivision name.
    :local_name: str (default="")
        subdivision name in local language.
    :type_: str (default="")
        subdivision type e.g district, state, canton, parish etc.
    :lat_lng: list | str (default=None)
        list of subdivision's latitude/longitude.
    :parent_code: str (default="")
        parent subdivision code for subdivision.
    :flag: str (default="")
        URL for subdivision flag on iso3166-flag-icons repo, if applicable.
    :delete: bool (default=0)
        the delete flag is set to 1 if the inputted subdivision is to be deleted
        from json object.
    :iso3166_2_filename: str (default="iso3166_2/iso3166-2.json")
        filename for main iso3166-2 object with all subdivision data.
    :subdivision_csv: str (default="")
        filename for CSV with latest subdivision data to be added, amended or deleted 
        to the object. 
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
    :export: bool (default=1)
        whether to export updated subdivision data to file pointed to by 
        iso3166_2_filename parameter, else return the whole updated subdivision
        object.

    Returns
    =======
    :all_subdivision_data: dict
        object containing all subdivision data with any additions, changes or 
        deletions.

    Usage 
    =====
    from iso3166_2_scripts.update_subdivisions import *

    #adding Timimoun Province of Algeria (DZ-49) to ISO 3166-2 object (from newsletter 2022-11-29)
    update_subdivision("DZ", "DZ-49", name="Timimoun", local_name="ولاية تيميمون", type="Province", latLng=[29.263, 0.241], parent_code=None, flag=None)

    #adding Waterford County of Ireland (IE-WD) to ISO 3166-2 object - subdivision already present so no changes made
    update_subdivision("IE", "IE-WD", "Waterford", local_name="Port Láirge", type="County", latLng=[52.260, -7.110], parent_code="IE-M", flag="https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/IE/IE-WD.png")
    #iso.update_subdivision("IE", "IE-WD") - this will also work as only the first 2 params requried

    #amending the subdivision name of subdivision FI-17 from Satakunda to Satakunta (from newsletter 2022-11-29)
    update_subdivision("FI", "FI-17", name="Satakunta")

    #deleting FR-GP (Guadeloupe) and (FR-MQ Martinique) subdivisions (from newsletter 2021-11-25)
    update_subdivision("FR", "FR-GP", delete=1)
    update_subdivision("FR", "FR-MQ", delete=1)

    #error raised as both alpha_code and subdivision_code parameters required if no subdivisions csv input
    update_subdivision(type="region", latLng=[], parent_code=None)

    #passing in a csv with rows of subdivision additions/updates/deletions
    update_subdivision(subdivision_csv="new_subdivisions.csv")
    """
    #read json data with all current subdivision data
    with open(iso3166_2_filename, 'r', encoding='utf-8') as input_json:
        all_subdivision_data = json.load(input_json)
    
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

    #list of default output keys/attributes per subdivision 
    expected_default_attributes = ["name", "localName", "type", "parentCode", "latLng", "flag"]

    #parse input default attributes to exclude from export
    if (exclude_default_keys != ""):
        #parse input attribute string into list, remove whitespace and split into comma separated list if string input
        if (isinstance(exclude_default_keys, str)):
            exclude_default_keys_converted_list = exclude_default_keys.replace(' ', '').split(',')
        else:
            exclude_default_keys_converted_list = exclude_default_keys

        #iterate over all input keys, raise error if invalid key input
        for key in exclude_default_keys_converted_list:
            if not (key in expected_default_attributes):
                raise ValueError(f"Attribute/field ({key}) invalid, please refer to list of the acceptable default attributes below:\n{expected_default_attributes}.")

        exclude_default_keys = exclude_default_keys_converted_list

    #parse input RestCountries attributes/fields, if applicable
    if (rest_countries_keys != ""):
        #list of rest country attributes that can be appended to output object
        rest_countries_keys_expected = ["idd", "carSigns", "carSide", "continents", "currencies", "languages", 
                                    "postalCode", "region", "startOfWeek", "subregion", "timezones", "tld"]

        #parse input attribute string into list, remove whitespace, skip if list of keys passed in 
        if isinstance(rest_countries_keys, str):
            rest_countries_keys_converted_list = rest_countries_keys.replace(' ', '').split(',')

            #iterate over all input keys, raise error if invalid key input
            for key in rest_countries_keys_converted_list:
                if not (key in rest_countries_keys_expected):
                    raise ValueError(f"Attribute/field ({key}) not available in RestCountries API, please refer to list of acceptable attributes below:\n{rest_countries_keys_expected}.")

            rest_countries_keys = rest_countries_keys_converted_list

    #remove any of the default attributes from list if they are to be excluded 
    temp_expected_attributes = expected_default_attributes
    if (exclude_default_keys != ""):
        for attr in exclude_default_keys:
            temp_expected_attributes.remove(attr)

    #append default attributes list with rest countries list if applicable 
    if (rest_countries_keys != ""):
        temp_expected_attributes.extend(sorted(rest_countries_keys))
    
    #parse lat_lng attribute, should be array of 2 str, can accept just a comma separated str, raise error if invalid input
    if (lat_lng != None and lat_lng != [] and not 'latLng' in exclude_default_keys):
        if (isinstance(lat_lng, str)):
            try:
                temp_lat_lng = []
                temp_lat_lng = [lat_lng.split(',')[0], lat_lng.split(',')[1]]
                lat_lng = temp_lat_lng  
            except:
                raise TypeError(f"Error parsing lat_lng attribute, expected a comma separated string of 2 inputs, got {lat_lng}.")
        elif not (isinstance(lat_lng, list)):
            raise TypeError(f"lat_lng attribute expected to be a list of floats or strings or a comma separated list of 2 elements, got {lat_lng}.")
        
        #round coordinates to 3d.p if applicable 
        lat_lng[0], lat_lng[1] = round(float(lat_lng[0]), 3), round(float(lat_lng[1]), 3)
    
    #if no subdivision csv passed in and subdivision changes passed in directly to function parameters
    if (subdivision_csv == ""): 

        #raise type error if input isn't a string
        if not (isinstance(alpha_code, str)):
            raise TypeError(f"Input alpha_code parameter {alpha_code} is not of correct datatype string, got {type(alpha_code)}.")       

        #raise error if alpha_code parameter empty 
        if (alpha_code == ""):
            raise ValueError("Alpha code parameter is required.")
        
        #uppercase and remove whitespace
        alpha_code = alpha_code.upper().replace(' ', '')
        
        #raise error if more than one alpha code input to function
        if (len(alpha_code.split(',')) > 1):
            raise ValueError(f"Only one country alpha code should be input to function, got {alpha_code}.")

        #raise error if subdivision_code parameter empty 
        if (subdivision_code == ""):
            raise ValueError("Subdivision code parameter is required.")
        
        #raise type error if input isn't a string
        if not (isinstance(subdivision_code, str)):
            raise TypeError(f"Input subdivision code parameter {subdivision_code} is not of correct datatype string, got {type(subdivision_code)}.")      

        #uppercase and remove whitespace
        subdivision_code = subdivision_code.upper().replace(' ', '')
        
        #if only half of subdivision code input to its parameter, prepend the alpha code to it to make it valid
        if ('-' not in subdivision_code):
            subdivision_code = alpha_code + '-' + subdivision_code

        #raise type error if input isn't a string
        if not (isinstance(type_, str)):
            raise TypeError(f"Input subdivision name parameter {type_} is not of correct datatype string, got {type(type_)}.")      

        #if 3 letter alpha-3 or numeric codes input then convert to corresponding alpha-2, else raise error
        if (len(alpha_code) == 3):
            temp_alpha_code = convert_to_alpha2(alpha_code)
            if not (temp_alpha_code is None):
                alpha_code = temp_alpha_code
            else:
                raise ValueError(f"Invalid alpha-3 or numeric country code input, cannot convert into corresponding alpha-2 code: {alpha_code}.")

        #raise error if invalid alpha-2 code input
        if not (alpha_code in sorted(list(iso3166.countries_by_alpha2.keys()))):
            raise ValueError(f"Invalid alpha-2 code input: {alpha_code}.")       
        
        #create temporary archive folder that will store the previous iso3166-2 objects before any changes were made to it
        if not (os.path.isdir("iso3166-2-data-archive")):
            os.makedirs("iso3166-2-data-archive")

        #create duplicate of current iso3166-2 object before making any changes to it
        with open(os.path.join("iso3166-2-data-archive", "archive-iso3166-2_" + \
            str(datetime.date(datetime.now())) + ".json"), 'w', encoding='utf-8') as output_json:
            json.dump(all_subdivision_data, output_json, ensure_ascii=False, indent=4)
        
        #delete subdivision if delete parameter set, raise error if code not found
        if (delete):
            if (subdivision_code in list(all_subdivision_data[alpha_code].keys())):
                del all_subdivision_data[alpha_code][subdivision_code] 
            else:
                raise ValueError(f"Subdivision code {subdivision_code} not present in country subdivision updates.")
        else:
            #if brackets are in subdivision_code parameter than the subdivision code is to be updated itself, keeping its existing data
            if ('(' and ')' in subdivision_code):
                #parse current and new subdivision code which should be put in brackets in the subdivision code parameter
                current_subdivision_code = subdivision_code.split('(', 1)[0]
                new_subdivision_code = subdivision_code[subdivision_code.find("(")+1:subdivision_code.find(")")].replace(' ', '')
            
                #raise error if current subdivision not found in list of codes
                if (current_subdivision_code not in list(all_subdivision_data[alpha_code].keys())):
                    raise ValueError(f"Subdivision code {current_subdivision_code} not found in country's list of codes:\n{list(all_subdivision_data[alpha_code].keys())}.")
                
                #raise error if new amended subdivision code does not have the same subdivision code prefix
                if (new_subdivision_code.split('-')[0] != current_subdivision_code.split('-')[0]):
                    raise ValueError(f"Country code of new subdivision code {new_subdivision_code} does not match that of original subdivision code {current_subdivision_code}.")

                #temp object with existing subdivision code data
                temp_subdivision = {}
                temp_subdivision[new_subdivision_code] = all_subdivision_data[alpha_code][current_subdivision_code]
                
                #add subdivision data with updated subdivision code key to object
                all_subdivision_data[alpha_code][new_subdivision_code] = temp_subdivision[new_subdivision_code]
                
                #when changing a subdivision's code itself, need to search for the subdivision's flag using its new code, from the iso3166-flag-icons repo
                if not ("flag" in temp_expected_attributes):
                    if (all_subdivision_data[alpha_code][new_subdivision_code]["flag"] == None or all_subdivision_data[alpha_code][new_subdivision_code]["flag"] == ""):
                        all_subdivision_data[alpha_code][new_subdivision_code]["flag"] = get_flag_icons_url(alpha_code, new_subdivision_code)
            
                #add rest countries key to object if applicable  
                if (rest_countries_keys != ""):
                    all_subdivision_data[alpha_code][new_subdivision_code] = parse_rest_countries(alpha_code, rest_countries_keys, all_subdivision_data[alpha_code][new_subdivision_code])

                #order attributes of individual subdivision using natsort
                all_subdivision_data[alpha_code][new_subdivision_code] = dict(OrderedDict(natsort.natsorted(all_subdivision_data[alpha_code][new_subdivision_code].items())))

                #validate if amended subdivision code has a flag on iso3166-flag-icons repo, if not then keep flag URL to the original code
                new_subdivision_flag = get_flag_icons_url(alpha_code, new_subdivision_code)
                if (new_subdivision_flag != None):
                    all_subdivision_data[alpha_code][new_subdivision_code]["flag"] = new_subdivision_flag

                #delete existing subdivision code data in object
                del all_subdivision_data[alpha_code][current_subdivision_code]
            else:
                #amend existing subdivision data with input parameters provided
                if (subdivision_code in all_subdivision_data[alpha_code]):
                    if (name != "" and not 'name' in exclude_default_keys):
                        all_subdivision_data[alpha_code][subdivision_code]["name"] = name
                    if (local_name != "" and not 'localName' in exclude_default_keys):
                        all_subdivision_data[alpha_code][subdivision_code]["localName"] = local_name
                    if (type_ != "" and not 'type' in exclude_default_keys):
                        all_subdivision_data[alpha_code][subdivision_code]["type"] = type_
                    if (lat_lng != None and not 'latLng' in exclude_default_keys):
                        all_subdivision_data[alpha_code][subdivision_code]["latLng"] = lat_lng
                    if (parent_code != "" and not 'parentCode' in exclude_default_keys):
                        if not ((parent_code != "") and (parent_code in list(all_subdivision_data[alpha_code].keys())) and (parent_code != subdivision_code)): #***
                            raise ValueError(f"Parent code {parent_code} not found in list of subdivision codes:\n{list(all_subdivision_data[alpha_code].keys())}.")
                        else:
                            all_subdivision_data[alpha_code][subdivision_code]["parentCode"] = parent_code
                    if (flag != "" and not 'flag' in exclude_default_keys):
                        all_subdivision_data[alpha_code][subdivision_code]["flag"] = flag
                else:
                    #adding new subdivision data to object from input parameters, exclude attributes if applicable 
                    new_subdivision_data = {}
                    if not ('name' in exclude_default_keys):
                        new_subdivision_data["name"] = name
                    if not ('localName' in exclude_default_keys):
                        new_subdivision_data["localName"] = local_name
                    if not ('type' in exclude_default_keys):
                        new_subdivision_data["type"] = type_
                    if not ('parentCode' in exclude_default_keys):
                        if (parent_code != ""):
                            #raise error if parent code not an existing subdivision code
                            if not (parent_code in list(all_subdivision_data[alpha_code].keys())) and (parent_code != subdivision_code):
                                raise ValueError(f"Parent code {parent_code} not found in list of subdivision codes:\n{list(all_subdivision_data[alpha_code].keys())}.")
                        new_subdivision_data["parentCode"] = parent_code
                    if not ('latLng' in exclude_default_keys):
                        new_subdivision_data["latLng"] = lat_lng
                    if not ('flag' in exclude_default_keys):
                        new_subdivision_data["flag"] = flag
                    
                    #append restcountries attribute values to new subdivision
                    if (rest_countries_keys != ""):
                        new_subdivision_data = parse_rest_countries(alpha_code, rest_countries_keys, new_subdivision_data)

                    #add new subdivision object to main subdivision data object
                    all_subdivision_data[alpha_code][subdivision_code] = new_subdivision_data

                #order attributes of individual subdivision using natsort
                all_subdivision_data[alpha_code][subdivision_code] = dict(OrderedDict(natsort.natsorted(all_subdivision_data[alpha_code][subdivision_code].items())))

        #sort subdivision codes in json objects in natural alphabetical/numerical order using natsort library
        all_subdivision_data[alpha_code] = dict(OrderedDict(natsort.natsorted(all_subdivision_data[alpha_code].items())))

    #if subdivision csv file input then parse it and make changes to subdivisions
    else:
        #raise OSError if subdivision file not found
        if not (os.path.isfile(subdivision_csv)):
            raise OSError(f"Subdivision data updates CSV not found: {subdivision_csv}.")

        #create temporary archive folder that will store the previous iso3166-2 objects before any changes were made to it
        if not (os.path.isdir("iso3166-2-data-archive")):
            os.makedirs("iso3166-2-data-archive")

        #create duplicate of current iso3166-2 object before making any changes to it
        with open(os.path.join("iso3166-2-data-archive", "archive-iso3166-2_" + \
            str(datetime.date(datetime.now())) + ".json"), 'w', encoding='utf-8') as output_json:
            json.dump(all_subdivision_data, output_json, ensure_ascii=False, indent=4)

        #read in subdivision csv as dataframe
        subdivision_df = pd.read_csv(subdivision_csv)
        
        #replace any Nan values with None
        subdivision_df = subdivision_df.replace(np.nan, None)

        #sort dataframe rows by their country code and reindex rows 
        # subdivision_df = subdivision_df.sort_values('alpha_code').reset_index(drop=True)

        #iterate through all dataframe rows, adding the subdivision attributes to respective subdivisions in object
        for index, row in subdivision_df.iterrows():
            
            #uppercase and remove whitespace for country code
            alpha_code = row['alpha_code'].replace(' ', '').upper()
            subdivision_code = row['code'].split('(', 1)[0].replace(' ', '').upper()

            #skip to next row in subdivisions csv if country code not in data object
            if not (alpha_code in list(all_subdivision_data.keys())):
                continue
            
            #if only half of subdivision code input to its parameter, prepend the alpha code to it to make it valid
            if ('-' not in subdivision_code):
                subdivision_code = alpha_code + '-' + subdivision_code
            
            #if brackets are in subdivision_code parameter than the subdivision code is to be updated itself, keeping its existing data
            if ('(' and ')' in row['code']):
                
                #parse current and new subdivision code which should be put in brackets in the subdivision code parameter
                new_subdivision_code = row['code'][row['code'].find("(")+1:row['code'].find(")")].replace(' ', '').upper()

                #raise error if new amended subdivision code does not have the same subdivision code prefix     ** here
                if (new_subdivision_code.split('-')[0] != subdivision_code.split('-')[0]):
                    raise ValueError(f"Country code of new subdivision code {new_subdivision_code} does not match that of original subdivision code {subdivision_code}.")

                #skip amendment of subdivision code if change have already been made to subdivision
                if not (new_subdivision_code in list(all_subdivision_data[alpha_code].keys())):

                    #raise error if current subdivision not found in list of codes
                    if (subdivision_code not in list(all_subdivision_data[alpha_code].keys())):
                        raise ValueError(f"Subdivision code {subdivision_code} not found in country's list of codes:\n{list(all_subdivision_data[alpha_code].keys())}.")
                    
                    #temp object with existing subdivision code data
                    new_subdivision = {}
                    new_subdivision[new_subdivision_code] = all_subdivision_data[alpha_code][subdivision_code]
                    
                    #add subdivision data with updated subdivision code key to object
                    all_subdivision_data[alpha_code][new_subdivision_code] = new_subdivision[new_subdivision_code]

                    #add rest countries key to object if applicable  
                    if (rest_countries_keys != ""):
                        all_subdivision_data[alpha_code][new_subdivision_code] = parse_rest_countries(alpha_code, rest_countries_keys, all_subdivision_data[alpha_code][new_subdivision_code])
                        
                    #delete existing subdivision code data in object
                    del all_subdivision_data[alpha_code][subdivision_code]

                    #validate if amended subdivision code has a flag on iso3166-flag-icons repo, if not then keep flag URL to the original code
                    new_subdivision_flag = get_flag_icons_url(alpha_code, new_subdivision_code)
                    if (new_subdivision_flag != None):
                        all_subdivision_data[alpha_code][new_subdivision_code]["flag"] = new_subdivision_flag

                    #order attributes of individual subdivision using natsort
                    all_subdivision_data[alpha_code][new_subdivision_code] = dict(OrderedDict(natsort.natsorted(all_subdivision_data[alpha_code][new_subdivision_code].items())))

                #skip to next iteration if new subdivision already in subdivision object
                else:
                    continue
            else:   
                #if delete column is set then delete respective subdivision from object according to its subdivision code, skip to next iteration
                if (row['delete']): 
                    if (subdivision_code in list(all_subdivision_data[alpha_code].keys())):
                        del all_subdivision_data[alpha_code][subdivision_code] 
                    continue
                else:     
                    #if subdivision already in object, make changes to its attributes according to values in row of csv
                    if (row["code"] in list(all_subdivision_data[alpha_code].keys())):
                        if (row['name'] != None and row['name'] != "" and not ('name' in exclude_default_keys)):
                            all_subdivision_data[alpha_code][subdivision_code]['name'] = row['name'] 
                        if (row['type'] != None and row['type'] != "" and not ('type' in exclude_default_keys)):
                            all_subdivision_data[alpha_code][subdivision_code]['type'] = row['type']
                        if (row['parentCode'] != None and row['parentCode'] != "" and not ('parentCode' in exclude_default_keys)):
                            if not ((row['parent_code'] in list(all_subdivision_data[alpha_code].keys())) and (row['parent_code'] != subdivision_code)): #validate parent code
                                raise ValueError(f"Parent code {row['parent_code']} not found in list of subdivision codes:\n{list(all_subdivision_data[alpha_code].keys())}.")
                            else:
                                all_subdivision_data[alpha_code][subdivision_code]['parentCode'] = row['parentCode']
                        if (row['flag'] != None and row['flag'] != "" and not ('flag' in exclude_default_keys)):
                            all_subdivision_data[alpha_code][subdivision_code]['flag'] = row['flag']
                        if (row['latLng'] != None and row['latLng'] != "" and not ('latLng' in exclude_default_keys)):
                            all_subdivision_data[alpha_code][subdivision_code]['latLng'] = json.loads(row["latLng"]) #convert string of array into array                
                        #if subdivision english name and common local name are the same - set to local name to name
                        if (row['localName'] == None or row['localName'] == "" and not ('localName' in exclude_default_keys)):
                            if (row['localNameSame']):
                                all_subdivision_data[alpha_code][subdivision_code]['localName'] = row['name']
                        elif (not ('localName' in exclude_default_keys)):
                            all_subdivision_data[alpha_code][subdivision_code]['localName'] = row['localName']
                    else:
                        #adding new subdivision 
                        all_subdivision_data[alpha_code][row["code"]] = {}

                        #raise error if subdivision name not present in row when adding a new subdivision
                        if not ('name' in exclude_default_keys):
                            if (row['name'] == None or row['name'] == ""):
                                raise ValueError(f"Subdivision name cannot be missing or null. Country code: {alpha_code}, Subdivision code: {subdivision_code}.")
                            all_subdivision_data[alpha_code][row["code"]]["name"] = row["name"]

                        #raise error if subdivision type not present in row when adding a new subdivision
                        if not ('type' in exclude_default_keys):
                            if (row['type'] == None or row['type'] == ""):
                                raise ValueError(f"Subdivision type cannot be missing or null. Country code: {alpha_code}, Subdivision code: {subdivision_code}.")
                            all_subdivision_data[alpha_code][row["code"]]["type"] = row["type"]

                        #raise error if subdivision lat_lng not present in row when adding a new subdivision
                        if not ('latLng' in exclude_default_keys):
                            if (row['latLng'] == None or row['latLng'] == ""): 
                                raise ValueError(f"Subdivision latLng cannot be missing or null. Country code: {alpha_code}, Subdivision code: {subdivision_code}.")
                            all_subdivision_data[alpha_code][row["code"]]["latLng"] = json.loads(row["latLng"]) #convert string of array into array

                        #determine if subdivision local name is the same as subdivision name
                        if not ('localName' in exclude_default_keys):
                            if (row["localNameSame"]): 
                                all_subdivision_data[alpha_code][row["code"]]["localName"] = row["name"]
                            else:
                                all_subdivision_data[alpha_code][row["code"]]["localName"] = row["localName"]
                        
                        #add parentCode and flag attributes if they are not to be excluded 
                        if not ('parentCode' in exclude_default_keys):
                            all_subdivision_data[alpha_code][row["code"]]["parentCode"] = row["parentCode"]
                        if not ('flag' in exclude_default_keys):
                            all_subdivision_data[alpha_code][row["code"]]["flag"] = row["flag"]

                        #append restcountries attribute values to new subdivision
                        if (rest_countries_keys != ""):
                            all_subdivision_data[alpha_code][row["code"]] = parse_rest_countries(alpha_code, rest_countries_keys, all_subdivision_data[alpha_code][row["code"]])
                            
                        # #iterate over each RestCountries key, if applicable, add attribute value to new object
                        # for key in rest_countries_keys:
                        #     #using an iterable, check if existing subdivision exists for country code, pull its attribute values for new object
                        #     all_subdivision_data_iterable = iter(all_subdivision_data[alpha_code])
                        #     if (next(all_subdivision_data_iterable, None) != None):
                        #         all_subdivision_data_iterable = iter(all_subdivision_data[alpha_code]) #reset iterable back to start of object
                        #         all_subdivision_data[alpha_code][subdivision_code][key] = all_subdivision_data[alpha_code][next(all_subdivision_data_iterable)][key]
                        #     #if subdivision not available for country code, use the RestCountries API to get the attribute values for new object
                        #     else:
                        #         #make call to RestCountries api if additional rest countries attributes input, raise error if invalid request
                        #         country_restcountries_response = requests.get(rest_countries_base_url + "alpha/" + all_subdivision_data[alpha_code], headers=USER_AGENT_HEADER)
                        #         country_restcountries_response.raise_for_status()
                        #         country_restcountries_data = country_restcountries_response.json()
                        #         all_subdivision_data[alpha_code][row["code"]][key] = country_restcountries_data[key]

                #order attributes of individual subdivision using natsort
                all_subdivision_data[alpha_code][subdivision_code] = dict(OrderedDict(natsort.natsorted(all_subdivision_data[alpha_code][subdivision_code].items())))

            #sort subdivision codes in json objects in natural alphabetical/numerical order using natsort library
            all_subdivision_data[alpha_code] = dict(OrderedDict(natsort.natsorted(all_subdivision_data[alpha_code].items())))

    #export the updated subdivision object to the folder or return the whole object, according to the export parameter
    if (export):
        with open(iso3166_2_filename, 'w', encoding='utf-8') as output_json:
            json.dump(all_subdivision_data, output_json, ensure_ascii=False, indent=4)  
        return {}
    else:
        return all_subdivision_data

def add_local_names(all_subdivision_data: dict) -> dict:
    """
    Adding subdivision's local name taken from iso3166_2_updates/local_names.csv. Most
    subdivision's local name is the same as it's current subdivision name attribute, but 
    many country's also have their own non-english local variations. 

    Parameters
    ==========
    :all_subdivision_data: dict
        data object containing all subdivision data.

    Returns
    =======
    :all_subdivision_data: dict
        input subdivision data object with local names for the subdivisions added.
    """
    #reading in, as dataframe, the csv that stores the local names for each subdivision
    local_name_df = pd.read_csv(os.path.join("iso3166_2_updates", "local_names.csv"))
    
    #replace any Nan values with None
    local_name_df = local_name_df.replace(np.nan, None)

    #sort dataframe rows by their country code and reindex rows 
    local_name_df = local_name_df.sort_values('alpha_code').reset_index(drop=True)

    #iterate over each country and subdivision, adding its local name
    for alpha2 in all_subdivision_data:
        for subd in list(all_subdivision_data[alpha2].keys()):
            #the localNames.csv file stores each subdivisions corresponding subdivision name as it is locally known
            #for most subdivisions the name and local name are the same, but for some, especially those not in the latin script, their local name of the subdivision differs
            #in the csv, the sameName column is set to 1 if the name and local name are the same, else the value from the localName column is taken
            if not (local_name_df.loc[local_name_df['subdivision_code'] == subd]['localName'].empty):
                if ((local_name_df.loc[local_name_df['subdivision_code'] == subd]['localName'].values[0] == None) or (local_name_df.loc[local_name_df['subdivision_code'] == subd]['localName'].values[0] == "")):
                    if (local_name_df.loc[local_name_df['subdivision_code'] == subd]['sameName'].values[0]):
                        all_subdivision_data[alpha2][subd]["localName"] = all_subdivision_data[alpha2][subd]["name"]
                    else:
                        all_subdivision_data[alpha2][subd]["localName"] = None
                else:
                    all_subdivision_data[alpha2][subd]["localName"] = local_name_df.loc[local_name_df['subdivision_code'] == subd]['localName'].values[0]
            else:
                all_subdivision_data[alpha2][subd]["localName"] = None

    return all_subdivision_data

def get_flag_icons_url(alpha2_code: str, subdivision_code: str) -> str|None:
    """ 
    Get URL for inputted subdivision code from the iso3166-flag-icons repo.
    
    Parameters
    ==========
    :alpha2_code: str
        alpha-2 country code.
    :subdivision_code: str
        ISO 3166-2 subdivision code.

    Returns
    =======
    :alpha2_flag + flag_file_extensions[extension] | None: str|None
        URL for subdivision flag if its found in the repo. If not on 
        the repo then None is returned. 
    """
    #base url for flag icons repo
    flag_icons_base_url = "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/"

    #list of flag file extensions in order of preference 
    flag_file_extensions = ['.svg', '.png', '.jpeg', '.jpg', '.gif']

    #if only half of subdivision code input to its parameter, prepend the alpha-2 code to it to make it valid
    if ('-' not in subdivision_code):
        subdivision_code = alpha2_code + '-' + subdivision_code
        
    #url to flag in iso3166-flag-icons repo
    alpha2_flag = flag_icons_base_url + alpha2_code + "/" + subdivision_code

    #set user agent to a random agent in the list
    USER_AGENT_HEADER = {'User-Agent': random.choice(user_agents)}

    #verify that path on flag icons repo exists, if not set flag url value to None
    if (requests.get(flag_icons_base_url + alpha2_code, headers=USER_AGENT_HEADER, timeout=15).status_code != 404):
        
        #iterate over all image extensions checking existence of flag in repo, if no flag with extensions found then set to null
        for extension in range(0, len(flag_file_extensions)):
                
                #if subdivision has a valid flag in flag icons repo set to its GitHub url, else set to None
                if (requests.get(alpha2_flag + flag_file_extensions[extension], headers=USER_AGENT_HEADER, timeout=15).status_code != 404):
                    return alpha2_flag + flag_file_extensions[extension]
                elif (extension == 4):
                    return None
    else:
        return None

def parse_rest_countries(alpha_code: str, rest_countries_keys: list, new_subdivision_data: dict) -> dict:
    """ 
    Extract and parse required data attributes from RestCountries API. Append each attribute's value to 
    subdivision object. 

    Parameters
    ==========
    :alpha_code: str
        ISO 3166-1 alpha-2 country code.
    :rest_countries_keys: list
        str of one or more comma separated additional attributes from the RestCountries API that can be 
        appended to each of the subdivisions in the output object. Here is the full list of accepted 
        fields/attributes: "idd", "carSigns", "carSide", "continents", "currencies", "languages", 
                    "postalCode", "region", "startOfWeek", "subregion", "timezones", "tld".        
    :new_subdivision_data: dict
        individual subdivision data object to be added or amended.

    Returns
    =======
    :new_subdivision_data: dict: dict
        individual subdivision data object with the applicable restcountries attribute values 
        appended to it.
    """
    #set user agent to a random agent in the list
    USER_AGENT_HEADER = {'User-Agent': random.choice(user_agents)}

    #use the RestCountries API to get the attribute values for country/subdivision
    country_restcountries_response = requests.get(rest_countries_base_url + "alpha/" + alpha_code, headers=USER_AGENT_HEADER, timeout=15)
    country_restcountries_response.raise_for_status()
    country_restcountries_data = country_restcountries_response.json()

    #iterate over each RestCountries key, if applicable, add attribute values to new object
    for key in rest_countries_keys:
        if (key == "carSigns"):
            new_subdivision_data[key] = country_restcountries_data[0]["car"]["signs"]
        elif (key == "carSide"):
            new_subdivision_data[key] = country_restcountries_data[0]["car"]["side"]
        elif (key == "idd"):
            new_subdivision_data[key] = "Root: " + str(country_restcountries_data[0]["idd"]["root"]) + ", Suffixes: " + str(country_restcountries_data[0]["idd"]["suffixes"])
        elif (key == "postalCode"):
            new_subdivision_data[key] = "Format: " + str(country_restcountries_data[0]["postalCode"]["format"]) + ", Regex: " + str(country_restcountries_data[0]["postalCode"]["regex"])
        else:
            new_subdivision_data[key] = country_restcountries_data[0][key]
        
    return new_subdivision_data
    
if __name__ == '__main__':

    #parse input arguments using ArgParse 
    parser = argparse.ArgumentParser(description='Script for adding, amending or deleting subdivision data from the object.')

    parser.add_argument('-alpha_code', '--alpha_code', type=str, required=False, default="", 
        help='ISO 3166-1 alpha-2, alpha-3 or numeric country code to be added, amended or deleted from object.')
    parser.add_argument('-subdivision_code', '--subdivision_code', type=str, required=False, default="", 
        help='ISO 3166-2 subdivision code to be added, amended or deleted from object.')
    parser.add_argument('-name', '--name', type=str, required=False, default="", 
        help='ISO 3166-2 subdivision name.')
    parser.add_argument('-local_name', '--local_name', type=str, required=False, default="", 
        help='ISO 3166-2 subdivision local name.')
    parser.add_argument('-type', '--type', type=str, required=False, default="", 
        help='ISO 3166-2 subdivision type.')
    parser.add_argument('-lat_lng', '--lat_lng', type=str, required=False, default=None, 
        help='ISO 3166-2 subdivision latitude/longitude.')
    parser.add_argument('-parent_code', '--parent_code', type=str, required=False, default="", 
        help='ISO 3166-2 subdivision parent subdivision code.')
    parser.add_argument('-flag', '--flag', type=str, required=False, default="", 
        help='ISO 3166-2 subdivision flag URL from iso3166-flag-icons repo.')
    parser.add_argument('-delete', '--delete', required=False, action=argparse.BooleanOptionalAction, default=0, 
        help='The delete flag is set to 1 if the inputted subdivision is to be deleted.')
    parser.add_argument('-iso3166_2_filename', '--iso3166_2_filename', type=str, required=False, default=os.path.join("iso3166_2", "iso3166-2.json"), 
        help='Filename for main iso3166-2 object with all subdivision data.')
    parser.add_argument('-subdivision_csv', '--subdivision_csv', type=str, required=False, default="", 
        help='Filename for CSV with latest subdivision data to be added, amended or deleted to the object.')
    parser.add_argument('-rest_countries_keys', '--rest_countries_keys', type=str, required=False, default="", 
        help='List of additional fields/attributes from RestCountries API to be added to each subdivision object.')
    parser.add_argument('-exclude_default_keys', '--exclude_default_keys', type=str, required=False, default="", 
        help="List of default fields/attributes to be excluded from each country's subdivision object.")
    parser.add_argument('-export', '--export', required=False, action=argparse.BooleanOptionalAction, default=1, 
        help='Whether to export updated subdivision data to file pointed to by iso3166_2_filename parameter, else return the whole updated subdivision object.')
    
    #parse input args
    args = parser.parse_args()
    alpha_code = args.alpha_code
    subdivision_code = args.subdivision_code
    name = args.name
    local_name = args.local_name
    type_ = args.type
    lat_lng = args.lat_lng
    parent_code = args.parent_code
    flag = args.flag
    delete = args.delete
    iso3166_2_filename = args.iso3166_2_filename
    subdivision_csv = args.subdivision_csv
    rest_countries_keys = args.rest_countries_keys
    exclude_default_keys = args.exclude_default_keys
    export = args.export

    update_subdivision(alpha_code=alpha_code, subdivision_code=subdivision_code, name=name, local_name=local_name, type_=type_, lat_lng=lat_lng, parent_code=parent_code,
                       flag=flag, delete=delete, iso3166_2_filename=iso3166_2_filename, subdivision_csv=subdivision_csv, rest_countries_keys=rest_countries_keys, 
                       exclude_default_keys=exclude_default_keys, export=export)