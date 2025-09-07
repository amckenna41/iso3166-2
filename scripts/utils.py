import unicodedata as ud
import pandas as pd
import requests
import os
import json
import time
import iso3166
import re
from fake_useragent import UserAgent
from dicttoxml import dicttoxml
import xml.etree.ElementTree as ET
from urllib.parse import unquote_plus
from iso3166_updates import *

#set random user-agent string for requests library to avoid detection, using fake-useragent package
user_agent = UserAgent()
USER_AGENT_HEADER = {"User-Agent": user_agent.random}

def convert_to_alpha2(alpha_code: str) -> str:
    """ 
    Auxiliary function that converts an ISO 3166 country's 3 letter alpha-3 
    or numeric code into its 2 letter alpha-2 counterpart. The function also
    validates the input alpha-2 or converted alpha-2 code, raising an error 
    if it is invalid. 

    Parameters 
    ==========
    :alpha_code: str
        2 letter letter ISO 3166-1 alpha-2 or 3 letter alpha-3/ numeric country code.
    
    Returns
    =======
    :iso3166.countries_by_alpha3[alpha_code].alpha2|iso3166.countries_by_numeric[alpha_code].alpha: str
        converted 2 letter ISO 3166 alpha-2 country code. 
    
    Raises
    ======
    TypeError:
        Invalid data type for alpha code parameter input.
    ValueError:
        Issue converting the inputted alpha code into alpha-2 code.
        More than 1 country code input, only 1 should be.
    """
    #raise error if invalid type input
    if not (isinstance(alpha_code, str)):
        raise TypeError(f"Expected input alpha code to be a string, got {type(alpha_code)}.")

    #raise error if more than 1 country code input
    if ("," in alpha_code):
        raise ValueError(f"Only one country code should be input into the function: {alpha_code}.")
    
    #uppercase alpha code, remove leading/trailing whitespace
    alpha_code = alpha_code.upper().strip()

    #use iso3166 package to find corresponding alpha-2 code from its numeric code
    if (alpha_code.isdigit()):
        if (alpha_code in list(iso3166.countries_by_numeric.keys())):
            return iso3166.countries_by_numeric[alpha_code].alpha2

    #return input alpha code if its valid
    if len(alpha_code) == 2:
        if (alpha_code in list(iso3166.countries_by_alpha2.keys())):
            return alpha_code

    #use iso3166 package to find corresponding alpha-2 code from its alpha-3 code
    if len(alpha_code) == 3:
        if (alpha_code in list(iso3166.countries_by_alpha3.keys())):
            return iso3166.countries_by_alpha3[alpha_code].alpha2
    
    #return error by default if input country code invalid and can't be converted into alpha-2
    raise ValueError(f"Invalid ISO 3166-1 country code input {alpha_code}.")

def get_alpha_codes_list(alpha_codes: str="", alpha_codes_range: str="") -> tuple[list, str]:
    """
    Get the full list of ISO 3166 alpha-2 country codes to export the ISO 3166-2 data
    for. The function validates and converts the list/str of alpha codes input, if 
    applicable. If a range of alpha codes input via the alpha_codes_range parameter,
    the full range of alpha codes will be gotten, alphabetically. If both parameters
    are populated, the alpha codes list will take precedence. 

    Parameters
    ==========
    :alpha_codes: str|list (default="")
        comma separated list of one or more ISO 3166 alpha-2, alpha-3 or numeric country codes.
    :alpha_codes_range: str
        a range of 2 ISO 3166-1 alpha-2, alpha-3 or numeric country codes to export the 
        updates data from, separated by a '-'. The code on the left hand side will be the 
        starting alpha code and the code on the right hand side will be the final alpha code 
        to which the data is exported from, e.g AD-LV, will export all updates data from 
        Andorra to Latvia, alphabetically. If only a single alpha code input then it will 
        serve as the starting country.

    Returns
    =======
    :alpha_codes_list: list
        list of validated and converted alpha-2 country codes.
    :alpha_codes_range: str (default="")
        corrected and validated range of alpha codes.
    
    Raises
    ======
    TypeError:
        Input parameters are not of correct str type.
    """
    if alpha_codes:
        if isinstance(alpha_codes, list):
            alpha_codes = ", ".join(alpha_codes)
        #raise error if input isn't a string or list
        elif not isinstance(alpha_codes, str):
            raise TypeError(f"Input parameter alpha_codes should be a list or string, got {type(alpha_codes)}.")
        #get list of alpha-2 codes, convert to alpha-2 if applicable
        alpha_codes_list = [convert_to_alpha2(code) for code in alpha_codes.split(',')]
        alpha_codes_range = ""
    elif alpha_codes_range:
    
        #sorted list of ISO 3166 alpha codes
        sorted_alpha_codes = sorted(iso3166.countries_by_alpha2.keys())

        #raise error if alpha codes range parameter is not a string
        if not isinstance(alpha_codes_range, str):
            raise TypeError(f"Input parameter alpha_codes_range should be a string, got {type(alpha_codes_range)}.")
    
        #if 2 alpha-2 codes separated by '-' not in parameter then the single alpha code will serve as the starting point
        if not ('-' in alpha_codes_range):
            #convert 3 letter alpha-3 or numeric code into its 2 letter alpha-2 counterpart OR validate existing 2 letter alpha-2 code
            start_alpha_code = convert_to_alpha2(alpha_codes_range.upper().replace(' ', ''))

            #get list of alpha codes from start alpha code, alphabetically, using its index
            alpha_codes_list = sorted_alpha_codes[sorted_alpha_codes.index(start_alpha_code):]

            #alpha codes range parameter set to input alpha code to the last country code alphabetically (ZW)
            alpha_codes_range = start_alpha_code + "-ZW"
        else:
            #convert 3 letter alpha-3 or numeric code into its 2 letter alpha-2 counterpart OR validate existing 2 letter alpha-2 code
            start_alpha_code = convert_to_alpha2(alpha_codes_range.split('-')[0])
            end_alpha_code = convert_to_alpha2(alpha_codes_range.split('-')[1])

            #swap 2 alpha codes to ensure they're in alphabetical order
            if (start_alpha_code > end_alpha_code):
                temp_code = start_alpha_code
                start_alpha_code = end_alpha_code
                end_alpha_code = temp_code

            #alpha codes range parameter set to validated and converted start and end alpha code
            alpha_codes_range = start_alpha_code + "-" + end_alpha_code

            #get full range of alpha codes from range parameter 
            alpha_codes_list = [code for code in sorted_alpha_codes if start_alpha_code <= code <= end_alpha_code]
    else:
        #using all ISO 3166 alpha codes
        alpha_codes_list = sorted(iso3166.countries_by_alpha2.keys())

    #sort list of alpha codes alphabetically
    alpha_codes_list.sort()

    return alpha_codes_list, alpha_codes_range

#var for maintaining the list of roman/latin characters
latin_letters= {}

def is_latin(uchr: str) -> str:
    """ Auxiliary function that checks if an individual character is a latin/non-latin character. """
    try: 
        return latin_letters[uchr]
    except KeyError:
        return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))

def only_roman_chars(unistr: str) -> str:
    """ Auxiliary function that checks if a string of character is made up of latin/non-latin characters. """
    return all(is_latin(uchr)
        for uchr in unistr
                if uchr.isalpha()) 

def split_preserving_quotes(text: str) -> list:
    """ 
    Static class method that splits multiple comma-separated strings into list elements but ensures elements 
    wrapped in single quotes are preserved. 
    
    Parameters
    ==========
    :text: str
        string of text to split into list of comma separated items.

    Returns
    =======
    :elements: list
        list of comma separated string elements, ensuring any strings wrapped in single quotes
        are preserved as individual elements.
    
    Raises
    ======
    TypeError:
        Invalid data type for input text parameter.
    """
    #raise error if input isn't a string
    if not (isinstance(text, str)):
        raise TypeError(f"Input should be a string, got {type(text)}.")

    elements = []
    current_element = []
    inside_quotes = False
    
    #iterate over each element in text, creating comma separated list of elements
    for char in text:
        if char == "'":
            inside_quotes = not inside_quotes
        elif char == "," and not inside_quotes:
            elements.append("".join(current_element).strip())
            current_element = []
        else:
            current_element.append(char)

    #append current element to list, remove any leading/trailing whitespace
    if current_element:
        elements.append("".join(current_element).strip())

    return elements

def get_flag_repo_url(alpha2_code: str, subdivision_code: str="") -> str|None:
    """ 
    Get URL for inputted subdivision code from the iso3166-flags repo.
    The alpha-2 code for the subdivision is optional as it should be able to 
    be parsed from the subdivision code, e.g "GB-ABC", although if just "ABC"
    is input into subdivision_code parameter then an error may be raised. 
    
    Parameters
    ==========
    :alpha2_code: str (default="")
        alpha-2 country code.
    :subdivision_code: str
        ISO 3166-2 subdivision code.

    Returns
    =======
    :alpha2_flag + flag_file_extensions[extension]| None: str|None
        URL for subdivision flag if its found in the repo. If not on 
        the repo then None is returned. 
    
    Raises
    ======
    TypeError:
        Invalid data type for alpha and subdivision code input parameters.
    ValueError:
        If the second half of the subdivision code just input without the 
        country code before the "-" & the alpha code parameter is "" then 
        the country code for the subdivision can't be parsed.
    """
    #base url for flag icons repo
    # flag_icons_folder_base_url = "https://github.com/amckenna41/iso3166-flags/blob/main/iso3166-2-flags/"
    flag_icons_file_base_url = "https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/"

    #list of flag file extensions, in order of preference 
    flag_file_extensions = ['.svg', '.png', '.jpeg', '.jpg']

    #raise an error if invalid data type input for parameters
    if (not isinstance(subdivision_code, str) or not isinstance(alpha2_code, str)):
        raise TypeError(f"Subdivision and alpha code parameters should be a string, got {type(subdivision_code)} and {type(alpha2_code)}, respectively.")

    #raise an error if no alpha code and non-full subdivision code input, parse alpha & subdivision codes from parameters
    if ('-' not in subdivision_code and alpha2_code == ""):
        raise ValueError("No alpha code and full subdivision code parameter was input so the alpha code cannot be parsed from the subdivision code.\n"
                        "E.g, for GB-ABC, the inputs should be ABC and GB, respectively, but GB-ABC can also just be input, leaving alpha code parameter blank.")
    elif (alpha2_code == ""):
        alpha2_code = subdivision_code.split("-")[0]
    elif ('-' not in subdivision_code):
        subdivision_code = alpha2_code + '-' + subdivision_code

    #uppercase alpha and subdivision code
    alpha2_code, subdivision_code = alpha2_code.upper(), subdivision_code.upper()
        
    #url to flag in iso3166-flags repo
    alpha2_flag = flag_icons_file_base_url + alpha2_code + "/" + subdivision_code

    #verify that path on flag icons repo exists, if not set flag url value to None
    # if (requests.get(flag_icons_folder_base_url + alpha2_code, headers=USER_AGENT_HEADER, timeout=15).status_code != 404):
        
    #iterate over all image extensions checking existence of flag in repo, if no flag with extensions found then set to null
    for extension in range(0, len(flag_file_extensions)):
            #if subdivision has a valid flag in flag icons repo set to its GitHub url, else set to None
            if (requests.get(alpha2_flag + flag_file_extensions[extension], headers=USER_AGENT_HEADER, timeout=15).status_code == 200):
                time.sleep(1)
                return alpha2_flag + flag_file_extensions[extension]
            elif (extension == 4):
                return None

def attributes_memory_usage(iso3166_2_json_filepath: str="iso3166-2.json", country_level_usage: bool=False, 
                            export: bool=True, export_folder="iso3166_2_resources") -> None:
    """ 
    Calculate the memory usage for each attribute within the ISO 3166-2 object.
    The output is useful in understanding the proportion of the object that is 
    taken up per attribute. We can also get the memory usage per country code 
    object, helping to see what country/subdivision codes take up the most 
    memory within the dataset, this will be ordered by memory usage.

    Parameters
    ========== 
    :iso3166_2_json_filepath (default="iso3166-2.json"):
        input filepath to ISO 3166-2 JSON file.
    :country_level_usage (default=False):
        export the attribute memory usage data per country.
    :export (default=True):
        export dataframe of memory usage to csv.
    :export_folder (default="iso3166_2_resources")
        folder to save the exported table to, by default
        it'll be saved in the iso3166_2_resources directory.

    Returns
    =======
    None

    Raises
    ======
    OsError:
        ISO 3166-2 JSON not found.
    """
    #raise error if object not found
    if not(os.path.isfile(iso3166_2_json_filepath)):
        raise OSError(f"ISO 3166-2 JSON not found: {iso3166_2_json_filepath}.")

    #load json
    with open(iso3166_2_json_filepath, 'r', encoding='utf-8') as file:
        iso3166_2_json = json.load(file)

    #calculate the size of individual country objects
    total_json_size = os.path.getsize(iso3166_2_json_filepath) / 1024  #convert total size to KB

    #aggregate attribute sizes across the whole file
    attribute_totals_global = {attribute: 0 for attribute in ['flag', 'latLng', 'localName', 'name', 'parentCode', 'type', 'history']}
    total_data_size = 0

    #iterate over each country and subdivision code objects, calculate size of attribute and add to output object
    for country_code, country_content in iso3166_2_json.items():
        for region_code, region_data in country_content.items():
            if isinstance(region_data, dict):
                total_data_size += json.dumps(region_data).encode('utf-8').__sizeof__() / 2024  #convert to KB
                for attribute, value in region_data.items():
                    if attribute in attribute_totals_global:
                        attribute_totals_global[attribute] += json.dumps({attribute: value}).encode('utf-8').__sizeof__()
    
    #object of memory usage data per attribute
    global_attribute_data = [
        {
            'Attribute': attribute,
            'Size (KB)': round(size / 1024, 3),  #convert size from bytes to KB
            # 'Percentage (%)': round((size / total_json_size) * 100 if total_json_size > 0 else 0, 3)
            'Percentage (%)': round((size / (total_json_size * 1024)) * 100 if total_json_size > 0 else 0, 3)
        }
        for attribute, size in attribute_totals_global.items()
    ]

    #create dataframe for global attribute analysis
    global_attribute_df = pd.DataFrame(global_attribute_data)

    #output filename
    attribute_memory_usage_filename = os.path.join(export_folder, "iso3166_2_attribute_memory_usage.csv")

    #export or print out the results of the attribute memory usage analysis
    if (export):
        global_attribute_df.to_csv(attribute_memory_usage_filename, index=False)
    else:
        print("Attribute memory usage for ISO 3166 object")
        print("########################################\n")
        print(global_attribute_df)

    #get memory usage per country object if parameter set
    if (country_level_usage):
        country_sizes = []

        #iterate over each country object, and its nested attribute memory usages
        for country_code, country_content in iso3166_2_json.items():
            country_size = json.dumps(country_content).encode('utf-8').__sizeof__() / 1024  #convert to KB
            country_percentage = (country_size / total_json_size) * 100
            country_sizes.append({
                'Country Code': country_code,
                'Size (KB)': round(country_size, 3),
                'Percentage (%)': round(country_percentage, 3)
            })
        
        #create dataframe for country sizes
        country_sizes_df = pd.DataFrame(country_sizes)

        #sorting by memory usage descending
        country_sizes_df = country_sizes_df.sort_values(by="Size (KB)", ascending=False).reset_index(drop=True)

        #output filename
        country_object_memory_usage_filename = os.path.join(export_folder, "iso3166_2_country_object_memory_usage.csv")
        
        #export or print out the results of the country object memory usage analysis
        if (export):
            country_sizes_df.to_csv(country_object_memory_usage_filename, index=False)
        else:
            print("Attribute memory usage for ISO 3166 object")
            print("########################################\n")
            print(country_sizes_df)

def add_history(all_country_data: dict) -> dict:
    """
    Extract the historical updates data for all of the inputted subdivisions and 
    append to subdivision object. The historical updates data is pulled from the
    custom-built iso3166-updates package (https://github.com/amckenna41/iso3166-updates)
    and outlines all of the published changes to the subdivision codes/name by the ISO. 
    The package supports changes data from 1996 and up to the current year.

    For each subdivision, its name, code and local/other name data is searched across
    the data entries for that subdivision's country data in the iso3166-updates object.
    If any of these are found the change information as well as the publication date and 
    source is appended to the subdivision object.


    Parameters
    ==========
    :all_country_data: dict
        object of all the extracted subdivision data, ordered per country code.

    Returns
    =======
    :all_country_data: dict
        object of all the extracted subdivision data, ordered per country code with any 
        applicable historical updates data appended to each subdivision object.
    """
    #create instance of Updates class
    iso_updates = Updates()
    #iterate over all alpha codes and their subdivisions
    for alpha2 in list(all_country_data.keys()):
        if (alpha2 == "XK"):
            continue

        #get updated data for current country using alpha-2 code
        current_alpha2_updates = iso_updates[alpha2]
        for subd in list(all_country_data[alpha2].keys()):

            #create set for the matching attributes, add subdivision code, name and local/other name
            matching_attributes = set()
            matching_attributes.add(unquote_plus(subd.lower()))
            matching_attributes.add(unquote_plus(all_country_data[alpha2][subd]["name"].lower().replace(' ', '')))

            #if local/other name attribute not empty, append each of its names to the search list
            if not (all_country_data[alpha2][subd]["localOtherName"] is None):

                #normalize local/other name & remove language codes from localOtherName attribute
                local_other_cleaned = re.sub(r'\s*\(.*?\)', '', all_country_data[alpha2][subd]["localOtherName"])
                local_names = re.split(r',\s*', local_other_cleaned)
                for name in local_names:
                    matching_attributes.add(unquote_plus(name.lower().strip()))

            #create history attribute in output object
            all_country_data[alpha2][subd]["history"] = []

            #iterate over each ISO 3166 update for current country, if subdivision code, name or local name found in updates description then append description, publication date and Source to history attribute
            for update in current_alpha2_updates[alpha2]:
                    
                #get normalized version of change and desc of change attributes
                norm_change = unquote_plus(update.get("Change", "")).lower()
                norm_desc = unquote_plus(update.get("Description of Change", "")).lower()

                #if match found between matching_attributes and country updates data, add to history attribute
                if any(attr in norm_change for attr in matching_attributes) or any(attr in norm_desc for attr in matching_attributes):
                    historical_change = update["Date Issued"] + ": " + update["Change"]
                    if update["Description of Change"]:
                        historical_change += " Description of Change: " + update["Description of Change"]
                    historical_change += " Source: " + update["Source"]
                    all_country_data[alpha2][subd]["history"].append(historical_change)

            #if no history attribute value found for current subdivision, set to None
            if not all_country_data[alpha2][subd]["history"]:
                all_country_data[alpha2][subd]["history"] = None
                
    return all_country_data

def export_iso3166_2_data(all_country_data: dict={}, input_filename: str="", export_filepath: str="iso366-2-export", export_csv: bool=True, export_xml: bool=True):
    """
    Export the extracted ISO 3166-2 subdivision data to the output files. By default, the subdivision data
    is exported to JSON but it can also be exported to CSV and XML via the export_csv and export_xml
    parameters, respectively. You can input the data directly via the all_country_data variable but a
    JSON file can also be imported via the input_filename, allowing you to export to the other file 
    formats. If both of these aforementioned vars are populated, the all_country_data will take
    precedence. 
    
    Parameters
    ==========
    :all_country_data: dict (default={})
        object of all the extracted subdivision data, ordered per country code.
    :input_filename: str (default="")
        input filename for already exported JSON filepath.
    :export_filepath: str (default="iso3166-2-export")
        export filename for subdivision output.
    :export_csv: bool (default=False)
        export the subdivision data to CSV.
    :export_xml: bool (default=False)
        export the subdivision data to XML.

    Returns
    =======
    None
    """
    #raise error if no filename for JSON data input to function, no data to work with
    if (not all_country_data and input_filename == ""):
        raise ValueError("No ISO 3166-2 data available, needs to be input via the all_country_data var or importing it via input_filename.")
    elif (not all_country_data and os.path.isfile(input_filename)):
        with open(input_filename, 'r', encoding='utf-8') as file:
            all_country_data = json.load(file)

    #convert any empty attribute values in the object to null
    def empty_to_none(x):
        return (
            {k: empty_to_none(v) for k, v in x.items()} if isinstance(x, dict) else
            [empty_to_none(v) for v in x] if isinstance(x, list) else
            (None if x in ("", None) else x)
        )
    all_country_data = empty_to_none(all_country_data)

    #remove the extension from the export filename
    if (os.path.splitext(export_filepath)[1] != ""):
        export_filepath = os.path.splitext(export_filepath)[0]

    #export list of subdivision attributes using the first non-empty subdivision object using an iterable
    first_country = next((cc for cc, subs in all_country_data.items() if subs), None)
    if first_country is None:
        raise ValueError("No subdivisions found: object might be empty.")
    first_subdivision = next(iter(all_country_data[first_country]))
    base_cols = list(all_country_data[first_country][first_subdivision].keys())

    #export subdivision data to JSON
    with open(export_filepath + ".json", 'w', encoding='utf-8') as f:
        json.dump(all_country_data, f, ensure_ascii=False, indent=4)

    #export subdivision data to CSV
    if export_csv:
        all_country_csv = []

        #iterate over each subdivision object, append each to list
        for country in all_country_data:
            for subd in all_country_data[country]:
                temp = all_country_data[country][subd].copy()
                temp["subdivisionCode"] = subd
                temp["alphaCode"] = country
                all_country_csv.append(temp)

        #prepend the alpha and subdivision code attributes to CSV column output
        csv_base_cols = base_cols
        csv_base_cols = ["alphaCode", "subdivisionCode"] + csv_base_cols 

        #transform list of subdivision data into dataframe
        all_country_data_df = pd.DataFrame(all_country_csv, columns=csv_base_cols)

        #sort output by country code and subdivision code, reindex
        all_country_data_df = all_country_data_df.sort_values(['alphaCode', 'subdivisionCode']).reset_index(drop=True)

        #drop country code column if only one country's data in output
        if len(all_country_data) == 1:
            all_country_data_df.drop("alphaCode", axis=1, inplace=True)

        #convert dataframe to csv
        all_country_data_df.to_csv(export_filepath + ".csv", index=False)

    #export subdivision data to XML
    if export_xml:
        #convert dict to XML & convert XML to string 
        xml_data = dicttoxml(all_country_data)
        root = ET.fromstring(xml_data)

        #add indentation to output for readability
        def indent(elem, level=0):
            """ Auxiliary function for adding indentation to XML output. """
            i = "\n" + level * "  "
            if len(elem):
                if not elem.text or not elem.text.strip():
                    elem.text = i + "  "
                for subelem in elem:
                    indent(subelem, level + 1)
                    if not subelem.tail or not subelem.tail.strip():
                        subelem.tail = i
            else:
                if level and (not elem.tail or not elem.tail.strip()):
                    elem.tail = i

        #indent XML string
        indent(root)

        #export XML to output folder
        ET.ElementTree(root).write(export_filepath + ".xml", encoding="utf-8", xml_declaration=True)

def combine_multiple_exports(file_list: list, export_file_name: str) -> None:
    """
    Concatenate multiple exported JSON ISO 3166-2 data into one master file. The use case for this
    function is when multiple batched exports of the data was exported and they need to be combined
    into one master file, e.g when using the alpha_codes_range parameter.
    
    Parameters
    ==========
    :file_list: list
        list of 1 or more previously exported ISO 3166-2 data files to be concatenated.
    :export_file_name: str
        filename for concatenated master data file.

    Returns
    =======
    None

    Raises
    ======
    OSError:
        One or more of the exported JSON files not found from given path.
    """
    #raise error if any of the input JSONs are not found
    for file in file_list:
        if not (os.path.isfile(file)):
            raise OSError(f"File not found in path {file}.")

    #object of combined JSONs
    combined_json = {}

    for file in file_list:
        #load json
        with open(file, 'r', encoding='utf-8') as file:
            iso3166_2_json = json.load(file)
            for country, subdiv in iso3166_2_json.items():
                if (country not in combined_json):
                    combined_json[country] = subdiv
                else:
                    combined_json[country].update(subdiv)

    #add extension to output file
    if (os.path.splitext(export_file_name)[1] != ".json"):
        export_file_name = export_file_name + ".json"

    #export combined data into JSON
    with open(export_file_name + ".json", 'w', encoding='utf-8') as f:
        json.dump(combined_json, f, ensure_ascii=False, indent=4)