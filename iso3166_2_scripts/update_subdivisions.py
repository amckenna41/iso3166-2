import os
import json
import iso3166
import natsort
from collections import OrderedDict
import pandas as pd
import numpy as np
from datetime import datetime

def update_subdivision(alpha2_code="", subdivision_code="", name="", local_name="", type="", latLng=[], parent_code=None, flag_url=None, 
                       delete=0, iso3166_2_filename=os.path.join("iso3166_2", "iso3166-2-data", "iso3166-2.json"), subdivision_csv="", export=1):
    """
    Auxillary function created to streamline the addition/amendment/deletion of 
    subdivisions in/from the iso3166-2.json object. There are two main ways at 
    which to add or make changes to the subdivision data. Firstly, this function 
    can accept all of the attributes that are available per each subdivision 
    (subdivision code, local name, name, type, parent_code, latitude/longitude, 
    flag). Secondly, a CSV of individual rows of  subdivision changes to be made 
    with all of the aforementioned attributes as columns, this allows for hundreds 
    of potential changes to be made to the object in one file and command. 
    
    If deleting an existing subdivision, the subdivision details should be passed 
    into the function alongisde setting the delete input parameter to 1. Similarly,
    in the CSV file, there is a delete column which should be set to 1 if deleting
    the subdivision specifed in the row.

    For both of the above methods, the existing ISO 3166-2 object with all the 
    subdivision data is duplicated/archived in case of any errors made when making
    changes/updates to the subdivision data. After all the unit tests for the
    software have completed and passed successfully, the archived data object 
    is deleted.
    
    Parameters
    ==========
    :alpha2_code: str (default="")
        2 letter alpha-2 country code.
    :subdivision_code: str (default="")
        subdivision code as per the ISO 3166-2.
    :name: str (default="")
        subdivision name.
    :local_name: str (default="")
        subdivision name in local language.
    :type: str (default="")
        subdivision type e.g district, state, canton, parish etc (default="").
    :latLng: array (default=[])
        array of subdivision's latitude/longitude.
    :parent_code: str (default=None)
        parent subdivision code for subdivision.
    :flag_url: str (default=None)
        URL for subdivision flag on iso3166-flag-icons repo, if applicable.
    :delete: bool (default=0)
        the delete flag is set to 1 if the inputted subdivision is to be deleted
        from json object.
    :iso3166_2_filename: str (default="iso3166_2/iso3166-2-data/iso3166-2.json")
        filename for main iso3166-2 object with all subdivision data.
    :subdivision_csv: str (default="")
        filename for CSV with latest subdivision data to be added or amended to 
        the software. 
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
    update_subdivisions("DZ", "DZ-49", name="Timimoun", local_name="ولاية تيميمون", type="Province", latLng=[29.263, 0.241], parent_code=None, flag_url=None)

    #adding Waterford County of Ireland (IE-WD) to ISO 3166-2 object - subdivision already present so no changes made
    update_subdivisions("IE", "IE-WD", "Waterford", local_name="Port Láirge", type="County", latLng=[52.260, -7.110], parent_code="IE-M", flag_url="https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/IE/IE-WD.png")
    #iso.update_subdivisions("IE", "IE-WD") - this will also work as only the first 2 params requried

    #amending the subdivision name of subdivision FI-17 from Satakunda to Satakunta (from newsletter 2022-11-29)
    update_subdivisions("FI", "FI-17", name="Satakunta")

    #deleting FR-GP (Guadeloupe) and (FR-MQ Martinique) subdivisions 
    update_subdivisions("FR", "FR-GP", delete=1)
    update_subdivisions("FR", "FR-MQ", delete=1)

    #error raised as both country_code and subdivision_code parameters required
    update_subdivisions(type="region", latLng=[], parent_code=None)

    #passing in a csv with rows of subdivision additions/updates/deletions
    update_subdivisions(subdivision_csv="new_subdivisions.csv")
    """
    #read json data with all current subdivision data
    with open(iso3166_2_filename, 'r', encoding='utf-8') as input_json:
        all_subdivision_data = json.load(input_json)

    def convert_to_alpha2(alpha3_code):
        """ 
        Convert an ISO 3166 country's 3 letter alpha-3 code into its 
        2 letter alpha-2 counterpart. 

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
        
    #if no subdivision csv passed in and subdivision changes passed in directly to function parameters
    if (subdivision_csv == ""):

        #raise type error if input isn't a string
        if not (isinstance(alpha2_code, str)):
            raise TypeError('Input alpha2_code parameter {} is not of correct datatype string, got {}.'.format(alpha2_code, type(alpha2_code)))       

        #uppercase and remove whitespace
        alpha2_code = alpha2_code.upper().replace(' ', '')

        #raise type error if input isn't a string
        if not (isinstance(subdivision_code, str)):
            raise TypeError('Input subdivision code parameter {} is not of correct datatype string, got {}.'.format(subdivision_code, type(subdivision_code)))      

        #uppercase and remove whitespace
        subdivision_code = subdivision_code.upper().replace(' ', '')

        #raise type error if input isn't a string
        if not (isinstance(type, str)):
            raise TypeError('Input subdivision name parameter {} is not of correct datatype string, got {}.'.format(type, type(type)))      

        #if 3 letter alpha-3 codes input then convert to corresponding alpha-2, else raise error
        if (len(alpha2_code) == 3):
            temp_alpha2_code = convert_to_alpha2(alpha2_code)
            if not (temp_alpha2_code is None):
                alpha2_code = temp_alpha2_code
            else:
                raise ValueError("Invalid alpha-3 code input, cannot convert into corresponding alpha-2 code: {}.".format(alpha2_code))

        #raise error if invalid alpha-2 code input
        if not (alpha2_code in sorted(list(iso3166.countries_by_alpha2.keys()))):
            raise ValueError("Invalid alpha-2 code input: {}.".format(alpha2_code))       
        
        #create temporary archive folder that will store the previous iso3166-2 objects before any changes were made to it
        if not (os.path.isdir("iso3166-2-data-archive")):
            os.makedirs("iso3166-2-data-archive")

        #create duplicate of current iso3166-2 object before making any changes to it
        with open(os.path.join("iso3166-2-data-archive", "archive-iso3166-2_" + \
            str(datetime.date(datetime.now())) + ".json"), 'w', encoding='utf-8') as output_json:
            json.dump(all_subdivision_data, output_json, ensure_ascii=False, indent=4)

        #delete subdivision if delete parameter set, raise error if code not found
        if (delete):
            if (subdivision_code in list(all_subdivision_data[alpha2_code].keys())):
                del all_subdivision_data[alpha2_code][subdivision_code] 
        else:
            #if brackets are in subdivision_code parameter than the subdivision code is to be updated itself, keeping its existing data
            if ('(' and ')' in subdivision_code):
                #parse current and new subdivision code which should be put in brackets in the subdivision code parameter
                current_subdivision_code = subdivision_code.split('(', 1)[0]
                new_subdivision_code = subdivision_code[subdivision_code.find("(")+1:subdivision_code.find(")")].replace(' ', '')

                #raise error if current subdivision not found in list of codes
                if (current_subdivision_code not in list(all_subdivision_data[alpha2_code].keys())):
                    raise ValueError("Subdivision code {} not found in country's list of codes:\n{}.".format(subdivision_code, list(all_subdivision_data[alpha2_code].keys())))
            
                #temp object with existing subdivision code data
                temp_subdivision = {}
                temp_subdivision[new_subdivision_code] = all_subdivision_data[alpha2_code][current_subdivision_code]
                
                #delete existing subdivision code data in object
                del all_subdivision_data[alpha2_code][current_subdivision_code]

                #add subdivision data with updated subdivision code key to object
                all_subdivision_data[alpha2_code][new_subdivision_code] = temp_subdivision[new_subdivision_code]

                #reorder subdivision attributes
                all_subdivision_data[alpha2_code][new_subdivision_code] = {k: all_subdivision_data[alpha2_code][new_subdivision_code][k] for k in ["name", "localName", "type", "parentCode", "flagUrl", "latLng"]}
            else:
                #amend existing subdivision data with input parameters provided
                if (subdivision_code in all_subdivision_data[alpha2_code]):
                    if (name != ""):
                        all_subdivision_data[alpha2_code][subdivision_code]["name"] = name
                    if (local_name != ""):
                        all_subdivision_data[alpha2_code][subdivision_code]["localName"] = local_name
                    if (type != ""):
                        all_subdivision_data[alpha2_code][subdivision_code]["type"] = type
                    if (latLng != []):
                        all_subdivision_data[alpha2_code][subdivision_code]["latLng"] = latLng
                    if (parent_code != None):
                        if not ((parent_code != None) and (parent_code in list(all_subdivision_data[alpha2_code].keys()))):
                            raise ValueError("Parent code {} not found in list of subdivision codes:\n{}.".format(parent_code, list(all_subdivision_data[alpha2_code].keys())))
                        else:
                            all_subdivision_data[alpha2_code][subdivision_code]["parentCode"] = parent_code
                    if (flag_url != None):
                        all_subdivision_data[alpha2_code][subdivision_code]["flagUrl"] = flag_url
                else:
                    #adding new subdivision data to object from input parameters
                    new_subdivision_data = {"name": name, "localName": local_name, "type": type, "parentCode": parent_code, "latLng": latLng, "flagUrl": flag_url}        
                    
                    #reorder subdivision attributes
                    all_subdivision_data[alpha2_code][subdivision_code] = {k: new_subdivision_data[k] for k in ["name", "localName", "type", "parentCode", "flagUrl", "latLng"]}
                    
        #sort subdivision codes in json objects in natural alphabetical/numerical order using natsort library
        all_subdivision_data[alpha2_code] = dict(OrderedDict(natsort.natsorted(all_subdivision_data[alpha2_code].items())))

    #if subdivision csv file input then parse it and make changes to subdivisions
    else:
        #raise OSError if subdivision file not found
        if not (os.path.isfile(subdivision_csv)):
            raise OSError("Subdivision data updates CSV not found: {}.".format(subdivision_csv))

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
        # subdivision_df = subdivision_df.sort_values('country_code').reset_index(drop=True)
        
        #iterate through all dataframe rows, adding the subdivision attributes to respective subdivisions in object
        for index, row in subdivision_df.iterrows():
            
            #uppercase and remove whitespace for country code
            country_code = row['country_code'].replace(' ', '').upper()

            #if brackets are in subdivision_code parameter than the subdivision code is to be updated itself, keeping its existing data
            if ('(' and ')' in row['code']):

                #parse current and new subdivision code which should be put in brackets in the subdivision code parameter
                current_subdivision_code = row['code'].split('(', 1)[0].replace(' ', '').upper()
                new_subdivision_code = row['code'][row['code'].find("(")+1:row['code'].find(")")].replace(' ', '').upper()

                #skip amendment of subdivision code if change have already been made to subdivision
                if not (new_subdivision_code in list(all_subdivision_data[country_code].keys())):

                    #raise error if current subdivision not found in list of codes
                    if (current_subdivision_code not in list(all_subdivision_data[country_code].keys())):
                        raise ValueError("Subdivision code {} not found in country's list of codes:\n{}.".format(current_subdivision_code, list(all_subdivision_data[country_code].keys())))
                    
                    #temp object with existing subdivision code data
                    new_subdivision = {}
                    new_subdivision[new_subdivision_code] = all_subdivision_data[country_code][current_subdivision_code]
                    
                    #delete existing subdivision code data in object
                    del all_subdivision_data[country_code][current_subdivision_code]

                    #add subdivision data with updated subdivision code key to object
                    all_subdivision_data[country_code][new_subdivision_code] = new_subdivision[new_subdivision_code]

                    #reorder attributes of individual subdivision
                    all_subdivision_data[country_code][new_subdivision_code] = {k: all_subdivision_data[country_code][new_subdivision_code][k] for k in ["name", "localName", "type", "parentCode", "flagUrl", "latLng"]}
                #skip to next iteration if new subdivision already in subdivision object
                else:
                    continue
            else:   
                #raise error if alpha-2 country code not found in object
                if not (country_code in list(all_subdivision_data.keys())):
                    raise ValueError("Country code {} in row not found in list of object country codes:\n{}.".format(country_code, list(all_subdivision_data.keys())))

                #if delete column is set then delete respective subdivision from object according to its subdivision code, skip to next iteration
                if (row['delete']): 
                    if (row['code'] in list(all_subdivision_data[country_code].keys())):
                        del all_subdivision_data[country_code][row['code']] 
                    continue
                else:     
                    #if subdivision already in object, make changes to its attributes according to values in row of csv
                    if (row["code"] in list(all_subdivision_data[row["country_code"]].keys())):
                        if (row['name'] != None and row['name'] != ""):
                            all_subdivision_data[country_code][row['code']]['name'] = row['name']
                        if (row['type'] != None and row['type'] != ""):
                            all_subdivision_data[country_code][row['code']]['type'] = row['type']
                        if (row['parentCode'] != None and row['parentCode'] != ""):
                            all_subdivision_data[country_code][row['code']]['parentCode'] = row['parentCode']
                        if (row['flagUrl'] != None and row['flagUrl'] != ""):
                            all_subdivision_data[country_code][row['code']]['flagUrl'] = row['flagUrl']
                        if (row['latLng'] != None and row['latLng'] != ""):
                            all_subdivision_data[country_code][row['code']]['latLng'] = json.loads(row["latLng"]) #convert string of array into array                
                        #if subdivision english name and common local name are the same - set to local name to name
                        if (row['localName'] == None or row['localName'] == ""):
                            if (row['localNameSpelling']):
                                all_subdivision_data[country_code][row['code']]['localName'] = row['name']
                        else:
                            all_subdivision_data[country_code][row['code']]['localName'] = row['localName']
                    else:
                        #raise error if subdivision code not present in row when adding a new subdivision
                        if (row['code'] == None or row['code'] == ""):
                            raise ValueError("Subdivsion code cannot be missing or null. Country code: {}.".format(country_code))
                        all_subdivision_data[row["country_code"]][row["code"]] = {}

                        #raise error if subdivision name not present in row when adding a new subdivision
                        if (row['name'] == None or row['name'] == ""):
                            raise ValueError("Subdivsion name cannot be missing or null. Country code: {}, Subdivision code: {}.".format(country_code, row['code']))
                        all_subdivision_data[row["country_code"]][row["code"]]["name"] = row["name"]

                        #raise error if subdivision type not present in row when adding a new subdivision
                        if (row['type'] == None or row['type'] == ""):
                            raise ValueError("Subdivsion type cannot be missing or null. Country code: {}, Subdivision code: {}.".format(country_code, row['code']))
                        all_subdivision_data[row["country_code"]][row["code"]]["type"] = row["type"]

                        #raise error if subdivision latLng not present in row when adding a new subdivision
                        if (row['latLng'] == None or row['latLng'] == ""): 
                            raise ValueError("Subdivsion latLng cannot be missing or null. Country code: {}, Subdivision code: {}.".format(country_code, row['code']))
                        all_subdivision_data[row["country_code"]][row["code"]]["latLng"] = json.loads(row["latLng"]) #convert string of array into array

                        #determine if subdivision local name is the same as subdivision name
                        if (row["localNameSpelling"]): 
                            all_subdivision_data[row["country_code"]][row["code"]]["localName"] = row["name"]
                        else:
                            all_subdivision_data[row["country_code"]][row["code"]]["localName"] = row["localName"]
                        
                        all_subdivision_data[row["country_code"]][row["code"]]["parentCode"] = row["parentCode"]
                        all_subdivision_data[row["country_code"]][row["code"]]["flagUrl"] = row["flagUrl"]
                
                #reorder attributes of individual subdivision
                all_subdivision_data[country_code][row['code']] = {k: all_subdivision_data[country_code][row['code']][k] for k in ["name", "localName", "type", "parentCode", "flagUrl", "latLng"]}

            #sort subdivision codes in json objects in natural alphabetical/numerical order using natsort library
            all_subdivision_data[country_code] = dict(OrderedDict(natsort.natsorted(all_subdivision_data[country_code].items())))

    #export the updated subdivision object to the folder or return the whole object, according to the export parameter
    if (export):
        with open(iso3166_2_filename, 'w', encoding='utf-8') as output_json:
            json.dump(all_subdivision_data, output_json, ensure_ascii=False, indent=4)  
        return 1  
    else:
        return all_subdivision_data

def add_local_names(all_subdivision_data):
    """
    Adding subdivision's local name taken from iso3166-2-updates/local_names.csv. Most
    subdivision's local name is the same as it's current sudivision name attribute, but 
    many country's also have their own non-english local variation. 

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
    local_name_df = pd.read_csv(os.path.join("iso3166-2-updates", "local_names.csv"))
    
    #replace any Nan values with None
    local_name_df = local_name_df.replace(np.nan, None)

    #sort dataframe rows by their country code and reindex rows 
    local_name_df = local_name_df.sort_values('country_code').reset_index(drop=True)

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