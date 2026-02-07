import unicodedata as ud
import pandas as pd
import requests
import os
import json
import time
from pycountry import countries 
from fake_useragent import UserAgent
from dicttoxml import dicttoxml
try:
    import openai
except ImportError:
    pass  # openai is optional
from dotenv import load_dotenv 
import xml.etree.ElementTree as ET

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
    :countries.get(alpha_3=alpha_code).alpha_2 | countries.get(numeric=alpha_code).alpha_2: str
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
        if (alpha_code in [country.numeric for country in countries]):
            return countries.get(numeric=alpha_code).alpha_2

    #return input alpha code if its valid
    if len(alpha_code) == 2:
        if (alpha_code in [country.alpha_2 for country in countries]):
            return alpha_code

    #use iso3166 package to find corresponding alpha-2 code from its alpha-3 code
    if len(alpha_code) == 3:
        if (alpha_code in [country.alpha_3 for country in countries]):
            return countries.get(alpha_3=alpha_code).alpha_2
    
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
    ValueError:
        Invalid alpha code input.
    """
    #get sorted set of all valid ISO 3166 alpha-2 codes
    all_codes_set = set(country.alpha_2 for country in countries)
    sorted_alpha_codes = sorted(all_codes_set)
    
    if alpha_codes:
        #handle list input
        if isinstance(alpha_codes, list):
            alpha_codes = ", ".join(alpha_codes)
        #raise error if input isn't a string or list
        elif not isinstance(alpha_codes, str):
            raise TypeError(f"Input parameter alpha_codes should be a list or string, got {type(alpha_codes)}.")
        
        #parse, validate and convert all codes to alpha-2 in one pass
        codes_set = set()
        for code in alpha_codes.split(','):
            converted_code = convert_to_alpha2(code.strip())
            codes_set.add(converted_code)
        
        #validate all codes are valid
        invalid_codes = codes_set - all_codes_set
        if invalid_codes:
            raise ValueError(f"Invalid ISO 3166-1 country code(s): {', '.join(sorted(invalid_codes))}.")
        
        return sorted(codes_set), ""
    
    elif alpha_codes_range:
        #raise error if alpha codes range parameter is not a string
        if not isinstance(alpha_codes_range, str):
            raise TypeError(f"Input parameter alpha_codes_range should be a string, got {type(alpha_codes_range)}.")
        
        #if no '-' separator, single alpha code serves as starting point
        if '-' not in alpha_codes_range:
            #convert and validate the starting alpha code
            start_alpha_code = convert_to_alpha2(alpha_codes_range.strip())
            
            #ensure code is valid
            if start_alpha_code not in all_codes_set:
                raise ValueError(f"Invalid ISO 3166-1 country code: {start_alpha_code}.")
            
            #get all codes from start to end alphabetically
            start_idx = sorted_alpha_codes.index(start_alpha_code)
            alpha_codes_list = sorted_alpha_codes[start_idx:]
            
            #set range parameter to start code through ZW
            alpha_codes_range = f"{start_alpha_code}-ZW"
        else:
            #split range and convert both codes
            range_parts = alpha_codes_range.split('-')
            start_alpha_code = convert_to_alpha2(range_parts[0].strip())
            end_alpha_code = convert_to_alpha2(range_parts[1].strip())
            
            #validate both codes are valid
            if start_alpha_code not in all_codes_set:
                raise ValueError(f"Invalid ISO 3166-1 country code: {start_alpha_code}.")
            if end_alpha_code not in all_codes_set:
                raise ValueError(f"Invalid ISO 3166-1 country code: {end_alpha_code}.")
            
            #ensure codes are in alphabetical order
            if start_alpha_code > end_alpha_code:
                start_alpha_code, end_alpha_code = end_alpha_code, start_alpha_code
            
            #set corrected range parameter
            alpha_codes_range = f"{start_alpha_code}-{end_alpha_code}"
            
            #get range of codes using list slicing for efficiency
            start_idx = sorted_alpha_codes.index(start_alpha_code)
            end_idx = sorted_alpha_codes.index(end_alpha_code)
            alpha_codes_list = sorted_alpha_codes[start_idx:end_idx + 1]
        
        return alpha_codes_list, alpha_codes_range
    else:
        #return all ISO 3166 alpha-2 codes
        return sorted_alpha_codes, ""

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
    with open(export_file_name, 'w', encoding='utf-8') as f:
        json.dump(combined_json, f, ensure_ascii=False, indent=4)

def get_nulls(iso3166_2_json_filepath: str, attributes: list|str, export: bool = False, 
              export_filename: str = "iso3166_2_null_attributes.csv") -> dict:
    """
    Scans the ISO 3166-2 JSON file and identifies subdivision codes where specified
    attributes have null/None values. Returns a dictionary mapping each attribute
    to a list of subdivision codes where that attribute is null.

    Parameters
    ==========
    :iso3166_2_json_filepath: str
        filepath to the ISO 3166-2 JSON file to analyze.
    :attributes: list|str
        list of attribute names or comma-separated string of attributes to check for null values. 
        This parameter is required. Use '*' to check all available attributes.
        Valid attributes: 'flag', 'latLng', 'localName', 'name', 'parentCode', 'type', 'history', 'area', 'population'
    :export: bool (default=False)
        if True, exports the null mapping results to a CSV file.
    :export_filename: str (default="iso3166_2_null_attributes.csv")
        filename for the exported CSV file. Only used when export=True.

    Returns
    =======
    :null_mapping: dict
        dictionary where keys are attribute names and values are lists of subdivision
        codes that have null values for that attribute. Format:
        {'attribute_name': ['subdivision_code1', 'subdivision_code2', ...]}

    Raises
    ======
    OSError:
        ISO 3166-2 JSON file not found at given path.
    TypeError:
        attributes parameter is not a list or string.
    ValueError:
        attributes parameter is empty/null or contains invalid attribute names.
    """
    #raise error if JSON file not found
    if not os.path.isfile(iso3166_2_json_filepath):
        raise OSError(f"ISO 3166-2 JSON file not found: {iso3166_2_json_filepath}.")

    #define valid attribute names 
    valid_attributes = ['flag', 'latLng', 'localName', 'name', 'parentCode', 'type', 'history']

    #convert string to list if comma-separated string provided
    if isinstance(attributes, str):
        #if wildcard '*' is provided, use all valid attributes
        if attributes.strip() == '*':
            attributes = valid_attributes.copy()
        else:
            attributes = [attr.strip() for attr in attributes.split(',')]
    elif not isinstance(attributes, list):
        raise TypeError(f"attributes parameter must be a list or string, got {type(attributes)}.")

    #raise error if attributes parameter is empty or None
    if not attributes:
        raise ValueError("attributes parameter is required and cannot be empty.")

    #validate all attributes are valid
    invalid_attributes = [attr for attr in attributes if attr not in valid_attributes]
    if invalid_attributes:
        raise ValueError(f"Invalid attribute name(s): {', '.join(invalid_attributes)}. "
                        f"Valid attributes are: {', '.join(valid_attributes)}.")

    #load the JSON file with better error handling
    try:
        with open(iso3166_2_json_filepath, 'r', encoding='utf-8') as file:
            iso3166_2_json = json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in {iso3166_2_json_filepath}. "
                        f"Error at line {e.lineno}, column {e.colno}: {e.msg}. "
                        f"Character position: {e.pos}") from e

    #initialize dictionary to store null mappings
    null_mapping = {attr: [] for attr in attributes}

    #iterate over each country and subdivision
    for country_code, country_data in iso3166_2_json.items():
        for subdivision_code, subdivision_data in country_data.items():
            if isinstance(subdivision_data, dict):
                #check each requested attribute
                for attribute in attributes:
                    #check if attribute exists and is None/null
                    if attribute in subdivision_data and subdivision_data[attribute] is None:
                        null_mapping[attribute].append(subdivision_code)

    #export results to CSV if export parameter is True
    if export:
        #prepare data for CSV export
        export_data = []
        
        #iterate over each attribute and its null subdivision codes
        for attribute, subdivision_codes in null_mapping.items():
            for subdivision_code in subdivision_codes:
                export_data.append({
                    'attribute': attribute,
                    'subdivision_code': subdivision_code
                })
        
        #if no null values found, create empty dataframe with headers
        if not export_data:
            null_df = pd.DataFrame(columns=['attribute', 'subdivision_code'])
        else:
            #create dataframe from export data
            null_df = pd.DataFrame(export_data)
            
            #sort by attribute name and subdivision code
            null_df = null_df.sort_values(['attribute', 'subdivision_code']).reset_index(drop=True)
        
        #export to CSV
        null_df.to_csv(export_filename, index=False)
        
        print(f"✓ Null attributes analysis exported to {export_filename}\n")
        
        #print attribute null counts
        print("Attribute Null Count Summary:")
        print("-" * 40)
        for attribute in attributes:
            count = len(null_mapping[attribute])
            print(f"{attribute}: {count}")
        print("-" * 40)

    return null_mapping



# def anomaly_detection(iso3166_2_json_filepath: str, export_filename: str = "iso3166_2_anomalies.csv",
#                       api_key: str = "", verbose: bool = True, batch_size: int = 50, max_subdivisions: int = 0) -> dict:
#     """
#     Detects anomalies and data quality issues in the ISO 3166-2 JSON file using OpenAI API.
#     Processes subdivisions in batches to avoid token limits.
#     Generates a comprehensive report of all detected anomalies and exports to CSV.

#     Parameters
#     ==========
#     :iso3166_2_json_filepath: str
#         filepath to the ISO 3166-2 JSON file to analyze.
#     :export_filename: str (default="iso3166_2_anomolies.csv")
#         filename for the exported CSV file containing detected anomalies.
#     :api_key: str (default="")
#         OpenAI API key (optional). If not provided, will attempt to load from OPENAI_API_KEY
#         environment variable. Environment variable takes precedence.
#     :verbose: bool (default=True)
#         if True, prints progress messages during analysis.
#     :batch_size: int (default=50)
#         number of subdivisions to process per API call to avoid token limits.
#     :max_subdivisions: int (default=0)
#         maximum total number of subdivisions to process (for testing). If 0, processes all subdivisions.
#         Use this to limit processing to e.g. first 100 subdivisions for testing purposes.

#     Returns
#     =======
#     :anomalies_report: dict
#         dictionary containing all detected anomalies and summary statistics.

#     Raises
#     ======
#     OSError:
#         ISO 3166-2 JSON file not found at given path.
#     ValueError:
#         API key not found or invalid JSON format.
#     """
#     # Check if file exists
#     if not os.path.isfile(iso3166_2_json_filepath):
#         raise OSError(f"ISO 3166-2 JSON file not found: {iso3166_2_json_filepath}.")
    
#     # Load environment variables from .env file
#     load_dotenv()
    
#     # Get API key from environment variable first, then fallback to parameter
#     env_api_key = os.getenv("OPENAI_API_KEY")
    
#     if env_api_key:
#         final_api_key = env_api_key
#     elif api_key:
#         final_api_key = api_key
#     else:
#         raise ValueError("API key not found. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
    
#     # Initialize OpenAI client
#     client = openai.OpenAI(api_key=final_api_key)
    
#     if verbose:
#         print(f"Starting anomaly detection analysis for {iso3166_2_json_filepath}")
#         print("=" * 70)
    
#     # Load JSON file
#     try:
#         with open(iso3166_2_json_filepath, 'r', encoding='utf-8') as f:
#             iso3166_2_json = json.load(f)
#     except json.JSONDecodeError as e:
#         raise ValueError(f"Invalid JSON format in {iso3166_2_json_filepath}. "
#                         f"Error at line {e.lineno}, column {e.colno}: {e.msg}")
    
#     if verbose:
#         total_countries = len(iso3166_2_json)
#         total_subdivisions = sum(len(subs) for subs in iso3166_2_json.values())
#         print(f"✓ JSON loaded successfully")
#         print(f"  Countries: {total_countries}")
#         print(f"  Total subdivisions available: {total_subdivisions}")
#         if max_subdivisions > 0:
#             print(f"  Processing only first {max_subdivisions} subdivisions (testing mode)")
#         print(f"  Batch size: {batch_size} subdivisions per API call")
    
#     # Prepare the base analysis prompt
#     audit_prompt_template = """You are a meticulous data quality auditor for a JSON dataset of ISO 3166-2 country subdivisions.

# Your job: Check every attribute on every subdivision in this batch for possible anomalies.

#     Validation rules:
#     - name: required string, non-empty
#     - type: required, non-empty string
#     - parentCode: string or null
#     - flag: URL string or null (must be HTTPS if present)
#     - latLng: array of exactly 2 numeric values [latitude, longitude], or null
#     - history: null or array of objects

#     Detect and report ALL anomalies including:
#     - Missing required attributes (name, type)
#     - Wrong data types
#     - latLng outside valid ranges or not exactly 2 numbers
#     - Malformed URLs or non-HTTPS flags
#     - Inconsistent data

# Output ONLY valid JSON (no extra text):
# {
#   "anomalies": [
#     {
#       "country_code": string,
#       "subdivision_code": string,
#       "attribute": string,
#       "value": any,
#       "issue_type": string,
#       "severity": "low" | "medium" | "high",
#       "details": string
#     }
#   ]
# }

# Return { "anomalies": [] } if no anomalies found."""
    
#     # Create batches of subdivisions
#     all_anomalies = []
#     batch_count = 0
#     total_batches = 0
#     subdivisions_processed = 0
    
#     # Flatten all subdivisions with their country codes
#     all_subdivisions = []
#     for country_code, subdivisions in iso3166_2_json.items():
#         for subdivision_code, subdivision_data in subdivisions.items():
#             all_subdivisions.append((country_code, subdivision_code, subdivision_data))
    
#     # Limit to max_subdivisions if specified (for testing)
#     if max_subdivisions > 0:
#         all_subdivisions = all_subdivisions[:max_subdivisions]
    
#     # Calculate total batches
#     total_batches = (len(all_subdivisions) + batch_size - 1) // batch_size
    
#     if verbose:
#         print(f"  Total batches to process: {total_batches}\n")
    
#     # Process subdivisions in batches
#     for i in range(0, len(all_subdivisions), batch_size):
#         batch_count += 1
#         batch_items = all_subdivisions[i:i + batch_size]
        
#         # Group batch items by country code for JSON structure
#         batch_json = {}
#         for country_code, subdivision_code, subdivision_data in batch_items:
#             if country_code not in batch_json:
#                 batch_json[country_code] = {}
#             batch_json[country_code][subdivision_code] = subdivision_data
        
#         if verbose:
#             print(f"  Processing batch {batch_count}/{total_batches} ({len(batch_items)} subdivisions)...")
        
#         try:
#             response = client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {
#                         "role": "system",
#                         "content": "You are a data quality analyst. Return only valid JSON with no additional text."
#                     },
#                     {
#                         "role": "user",
#                         "content": f"{audit_prompt_template}\n\n{json.dumps(batch_json)}"
#                     }
#                 ],
#                 temperature=0,
#                 timeout=60
#             )
            
#             # Parse the response
#             response_text = response.choices[0].message.content.strip()
            
#             # Extract JSON from response
#             json_start = response_text.find('{')
#             json_end = response_text.rfind('}') + 1
            
#             if json_start != -1 and json_end > json_start:
#                 json_str = response_text[json_start:json_end]
#                 anomalies_data = json.loads(json_str)
#                 all_anomalies.extend(anomalies_data.get('anomalies', []))
            
#             # Rate limiting: small delay between requests
#             time.sleep(0.5)
            
#         except Exception as e:
#             print(f"  ⚠ Error processing batch {batch_count}: {str(e)}")
#             continue
    
#     if verbose:
#         print(f"\n✓ All batches processed")
    
#     # Perform comprehensive client-side validation to filter actual anomalies
#     # and generate accurate descriptions
#     export_data = []
    
#     # Rebuild ISO3166-2 JSON into flat structure for easy access
#     subdivision_map = {}
#     for country_code, subdivisions in iso3166_2_json.items():
#         for subdivision_code, subdivision_data in subdivisions.items():
#             full_code = f"{country_code}-{subdivision_code}"
#             subdivision_map[full_code] = (country_code, subdivision_code, subdivision_data)
    
#     # Validate each subdivision's attributes
#     for country_code, subdivisions in iso3166_2_json.items():
#         for subdivision_code, subdivision_data in subdivisions.items():
#             if not isinstance(subdivision_data, dict):
#                 continue
            
#             # Check each attribute for actual data quality issues
#             # name: required, must be non-empty string
#             if 'name' not in subdivision_data or subdivision_data['name'] is None:
#                 export_data.append({
#                     'subdivision_code': f"{country_code}-{subdivision_code}",
#                     'attribute': 'name',
#                     'issue_type': 'Missing Required Attribute',
#                     'severity': 'high',
#                     'value': 'null',
#                     'anomoly_description': 'Subdivision name is required but missing (null)'
#                 })
#             elif not isinstance(subdivision_data['name'], str) or subdivision_data['name'].strip() == '':
#                 export_data.append({
#                     'subdivision_code': f"{country_code}-{subdivision_code}",
#                     'attribute': 'name',
#                     'issue_type': 'Invalid Data Type',
#                     'severity': 'high',
#                     'value': str(subdivision_data['name']),
#                     'anomoly_description': f"Name must be a non-empty string, got: {subdivision_data['name']}"
#                 })
            
#             # type: required, must be non-empty string
#             if 'type' not in subdivision_data or subdivision_data['type'] is None:
#                 export_data.append({
#                     'subdivision_code': f"{country_code}-{subdivision_code}",
#                     'attribute': 'type',
#                     'issue_type': 'Missing Required Attribute',
#                     'severity': 'high',
#                     'value': 'null',
#                     'anomoly_description': 'Subdivision type is required but missing (null)'
#                 })
#             elif not isinstance(subdivision_data['type'], str) or subdivision_data['type'].strip() == '':
#                 export_data.append({
#                     'subdivision_code': f"{country_code}-{subdivision_code}",
#                     'attribute': 'type',
#                     'issue_type': 'Invalid Data Type',
#                     'severity': 'high',
#                     'value': str(subdivision_data['type']),
#                     'anomoly_description': f"Type must be a non-empty string, got: {subdivision_data['type']}"
#                 })
            
#             # flag: optional, but if present must be HTTPS URL with valid format
#             if 'flag' in subdivision_data and subdivision_data['flag'] is not None:
#                 flag_val = subdivision_data['flag']
#                 if not isinstance(flag_val, str):
#                     export_data.append({
#                         'subdivision_code': f"{country_code}-{subdivision_code}",
#                         'attribute': 'flag',
#                         'issue_type': 'Invalid Data Type',
#                         'severity': 'medium',
#                         'value': str(flag_val),
#                         'anomoly_description': f"Flag must be a string URL, got type {type(flag_val).__name__}"
#                     })
#                 elif not flag_val.startswith('https://'):
#                     export_data.append({
#                         'subdivision_code': f"{country_code}-{subdivision_code}",
#                         'attribute': 'flag',
#                         'issue_type': 'Non-HTTPS URL',
#                         'severity': 'medium',
#                         'value': flag_val[:100],
#                         'anomoly_description': f"Flag URL must use HTTPS protocol: {flag_val[:80]}"
#                     })
#                 elif not any(flag_val.endswith(ext) for ext in ['.svg', '.png', '.jpeg', '.jpg']):
#                     export_data.append({
#                         'subdivision_code': f"{country_code}-{subdivision_code}",
#                         'attribute': 'flag',
#                         'issue_type': 'Unsupported Format',
#                         'severity': 'low',
#                         'value': flag_val[:100],
#                         'anomoly_description': f"Flag URL has unsupported format (must be .svg, .png, .jpeg, or .jpg): {flag_val[:80]}"
#                     })
            
#             # latLng: optional, but if present must be [lat, lng] with valid ranges
#             if 'latLng' in subdivision_data and subdivision_data['latLng'] is not None:
#                 lat_lng = subdivision_data['latLng']
#                 if not isinstance(lat_lng, list) or len(lat_lng) != 2:
#                     export_data.append({
#                         'subdivision_code': f"{country_code}-{subdivision_code}",
#                         'attribute': 'latLng',
#                         'issue_type': 'Invalid Data Type',
#                         'severity': 'high',
#                         'value': str(lat_lng),
#                         'anomoly_description': f"Coordinates must be [latitude, longitude] array with 2 elements, got: {lat_lng}"
#                     })
#                 else:
#                     try:
#                         lat, lng = float(lat_lng[0]), float(lat_lng[1])
#                         if lat < -90 or lat > 90:
#                             export_data.append({
#                                 'subdivision_code': f"{country_code}-{subdivision_code}",
#                                 'attribute': 'latLng',
#                                 'issue_type': 'Out of Range',
#                                 'severity': 'high',
#                                 'value': str(lat_lng),
#                                 'anomoly_description': f"Latitude out of valid range [-90, 90]: {lat}"
#                             })
#                         elif lng < -180 or lng > 180:
#                             export_data.append({
#                                 'subdivision_code': f"{country_code}-{subdivision_code}",
#                                 'attribute': 'latLng',
#                                 'issue_type': 'Out of Range',
#                                 'severity': 'high',
#                                 'value': str(lat_lng),
#                                 'anomoly_description': f"Longitude out of valid range [-180, 180]: {lng}"
#                             })
#                     except (ValueError, TypeError):
#                         export_data.append({
#                             'subdivision_code': f"{country_code}-{subdivision_code}",
#                             'attribute': 'latLng',
#                             'issue_type': 'Invalid Data Type',
#                             'severity': 'high',
#                             'value': str(lat_lng),
#                             'anomoly_description': f"Coordinates must contain numeric values, got: {lat_lng}"
#                         })
    
#     # Build summary statistics from validated anomalies only
#     anomalies_by_severity = {'high': 0, 'medium': 0, 'low': 0}
#     anomalies_by_country = {}
#     anomalies_by_type = {}
    
#     for anomaly_record in export_data:
#         severity = anomaly_record.get('severity', 'low')
#         anomalies_by_severity[severity] = anomalies_by_severity.get(severity, 0) + 1
        
#         # Extract country code from subdivision_code (format: "CC-XX")
#         subd_code = anomaly_record.get('subdivision_code', '')
#         if subd_code and '-' in subd_code:
#             country_code = subd_code.split('-')[0]
#             anomalies_by_country[country_code] = anomalies_by_country.get(country_code, 0) + 1
        
#         issue_type = anomaly_record.get('issue_type', 'unknown')
#         anomalies_by_type[issue_type] = anomalies_by_type.get(issue_type, 0) + 1
    
#     if export_data:
#         export_df = pd.DataFrame(export_data)
#         export_df = export_df.sort_values(['subdivision_code', 'severity']).reset_index(drop=True)
#         export_df.to_csv(export_filename, index=False)
#     else:
#         export_df = pd.DataFrame(columns=['subdivision_code', 'attribute', 'issue_type', 'severity', 'value', 'anomoly_description'])
#         export_df.to_csv(export_filename, index=False)
    
#     if verbose:
#         print(f"\n{'='*70}")
#         print("Anomaly Detection Summary:")
#         print(f"{'='*70}")
#         print(f"  Total anomalies detected: {len(all_anomalies)}")
#         print(f"  High severity: {anomalies_by_severity['high']}")
#         print(f"  Medium severity: {anomalies_by_severity['medium']}")
#         print(f"  Low severity: {anomalies_by_severity['low']}")
#         if anomalies_by_type:
#             print(f"\n  Anomalies by type (top 10):")
#             sorted_types = sorted(anomalies_by_type.items(), key=lambda x: x[1], reverse=True)[:10]
#             for issue_type, count in sorted_types:
#                 print(f"    {issue_type}: {count}")
#         if anomalies_by_country:
#             print(f"\n  Countries with most anomalies (top 10):")
#             sorted_countries = sorted(anomalies_by_country.items(), key=lambda x: x[1], reverse=True)[:10]
#             for country, count in sorted_countries:
#                 print(f"    {country}: {count}")
#         print(f"\n✓ Anomaly report exported to: {export_filename}")
#         print(f"{'='*70}\n")
    
#     return {
#         'anomalies': all_anomalies,
#         'total_anomalies': len(all_anomalies),
#         'anomalies_by_severity': anomalies_by_severity,
#         'anomalies_by_country': anomalies_by_country,
#         'anomalies_by_type': anomalies_by_type,
#         'export_path': export_filename
#     }

# def correct_demographics(iso3166_2_json_filepath: str, verbose: bool = True, export: bool = True,
#                         export_filename: str = "") -> None:
#     """
#     Corrects None/null area and population values in the ISO 3166-2 JSON file by fetching
#     demographics data from the demographics module using Wikidata SPARQL endpoint.
#     Only modifies subdivisions where area or population is None/null, leaving all other data unchanged.

#     Parameters
#     ==========
#     :iso3166_2_json_filepath: str
#         filepath to the exported ISO 3166-2 JSON file to correct.
#     :verbose: bool (default=True)
#         if True, prints progress messages during correction process.
#     :export: bool (default=True)
#         if True (default), exports the corrected data to a new JSON file. If False, overwrites the original.
#     :export_filename: str (default="")
#         filename for the exported corrected JSON file. Required when export=True.
#         Must be a valid non-empty filename string. Raises ValueError if empty or invalid when export=True.

#     Returns
#     =======
#     None

#     Raises
#     ======
#     OSError:
#         ISO 3166-2 JSON file not found at given path.
#     ValueError:
#         If export=True but export_filename is empty or invalid.
#         If unable to fetch or process demographics data.
#     """
#     #validate export_filename if export is True
#     if export:
#         if not export_filename or not isinstance(export_filename, str) or export_filename.strip() == "":
#             raise ValueError("export_filename parameter is required and must be a non-empty string when export=True.")
    
#     #import demographics module
#     try:
#         from .demographics import export_demographics
#     except ImportError:
#         from demographics import export_demographics
    
#     #raise error if JSON file not found
#     if not os.path.isfile(iso3166_2_json_filepath):
#         raise OSError(f"ISO 3166-2 JSON file not found: {iso3166_2_json_filepath}.")

#     #load the JSON file
#     with open(iso3166_2_json_filepath, 'r', encoding='utf-8') as file:
#         iso3166_2_json = json.load(file)

#     #track statistics
#     total_subdivisions = 0
#     null_demo_count = 0
#     corrected_count = 0
#     failed_corrections = {}  # Changed to dict to store {full_code: (name, error_details)}
#     successful_corrections = []

#     if verbose:
#         print(f"Starting demographics correction process for {iso3166_2_json_filepath}")
#         print("=" * 70)

#     #iterate over each country
#     for country_code, country_data in iso3166_2_json.items():
#         if verbose:
#             print(f"\nProcessing country: {country_code}")
        
#         #track if any subdivisions in this country need correction
#         country_has_nulls = False
        
#         for subdivision_code, subdivision_data in country_data.items():
#             total_subdivisions += 1
            
#             #check if this subdivision has null area or population
#             has_null_area = subdivision_data.get('area') is None
#             has_null_pop = subdivision_data.get('population') is None
            
#             if has_null_area or has_null_pop:
#                 null_demo_count += 1
#                 if not country_has_nulls:
#                     country_has_nulls = True
        
#         #if country has any subdivisions needing correction, fetch demographics data
#         if country_has_nulls:
#             try:
#                 if verbose:
#                     print(f"  Fetching demographics data from Wikidata for {country_code}...")
                
#                 #fetch demographics data for entire country
#                 demographics_data = export_demographics(
#                     country_code,
#                     all_years=False,
#                     include_pop_year=False,
#                     include_population_rank=False,
#                     include_metadata=False,
#                     include_subdiv_name=False
#                 )
                
#                 #iterate through subdivisions again to apply corrections
#                 for subdivision_code, subdivision_data in country_data.items():
#                     has_null_area = subdivision_data.get('area') is None
#                     has_null_pop = subdivision_data.get('population') is None
                    
#                     if has_null_area or has_null_pop:
#                         #try to find matching subdivision in demographics data
#                         #ISO 3166-2 codes in JSON are full codes (e.g., "GB-ABC")
#                         #but demographics returns data keyed by subdivision code without country
#                         iso_code_suffix = subdivision_code.split('-', 1)[1] if '-' in subdivision_code else subdivision_code
                        
#                         #search for matching entry in demographics data
#                         matching_demo = None
#                         for demo_iso_code, demo_data in demographics_data.items():
#                             if demo_iso_code.upper() == subdivision_code.upper() or demo_iso_code.upper().endswith(iso_code_suffix.upper()):
#                                 matching_demo = demo_data
#                                 break
                        
#                         if matching_demo:
#                             #update area if it was null and we have data
#                             if has_null_area and matching_demo.get('area') is not None:
#                                 subdivision_data['area'] = matching_demo['area']
#                                 if verbose:
#                                     print(f"  ✓ Updated area for {subdivision_code}: {matching_demo['area']} km²")
                            
#                             #update population if it was null and we have data
#                             if has_null_pop and matching_demo.get('population') is not None:
#                                 subdivision_data['population'] = matching_demo['population']
#                                 if verbose:
#                                     print(f"  ✓ Updated population for {subdivision_code}: {matching_demo['population']}")
                            
#                             corrected_count += 1
                            
#                             #track successful correction
#                             success_msg = f"{subdivision_code} ({subdivision_data.get('name', 'Unknown')})"
#                             successful_corrections.append(success_msg)
#                         else:
#                             subdivision_name = subdivision_data.get('name', 'Unknown')
#                             full_code = subdivision_code
#                             error_details = f"No matching demographics data found for {full_code} ({subdivision_name}) in {country_code}"
#                             failed_corrections[full_code] = (subdivision_name, error_details)
                            
#                             if verbose:
#                                 print(f"  ✗ {error_details}")
                
#             except Exception as e:
#                 error_msg = f"Error fetching demographics for {country_code}: {str(e)}"
#                 failed_corrections[f"{country_code}-ERROR"] = (country_code, error_msg)
                
#                 if verbose:
#                     print(f"  ⚠ {error_msg}")
            
#             #add delay to respect Wikidata API rate limits
#             time.sleep(1)

#     #print summary statistics
#     if verbose:
#         print("\n" + "=" * 70)
#         print("Demographics Correction Summary:")
#         print(f"  Total subdivisions processed: {total_subdivisions}")
#         print(f"  Subdivisions with null area/population: {null_demo_count}")
#         print(f"  Successfully corrected: {corrected_count}")
#         print(f"  Failed corrections: {len(failed_corrections)}")
#         print("=" * 70)

#     #determine output filename
#     output_file = export_filename if export else iso3166_2_json_filepath

#     #save the corrected data to the JSON file
#     with open(output_file, 'w', encoding='utf-8') as f:
#         json.dump(iso3166_2_json, f, ensure_ascii=False, indent=4)

#     if verbose:
#         print(f"\n✓ Successfully saved corrected data to {output_file}")

#     #output successful corrections if any
#     if successful_corrections and verbose:
#         print("\n" + "=" * 70)
#         print("✓ Subdivisions with Successfully Corrected Demographics:")
#         print("=" * 70)
#         for success_msg in successful_corrections:
#             print(f"  • {success_msg}")
#         print("=" * 70)

#     #output failed corrections if any
#     if failed_corrections and verbose:
#         print("\n" + "=" * 70)
#         print("⚠ Subdivisions with Failed Demographics Corrections:")
#         print("=" * 70)
        
#         for subdivision_code, (subdivision_name, error_details) in failed_corrections.items():
#             print(f"\n{subdivision_code}: {subdivision_name}\n")
            
#             # Parse and format error details line by line
#             error_lines = error_details.split('\n')
#             for line in error_lines:
#                 stripped_line = line.strip()
#                 if stripped_line:
#                     # Check if line already starts with a bullet point
#                     if stripped_line.startswith('•'):
#                         # Line already has bullet point, just print with indentation
#                         print(f"  {stripped_line}")
#                     else:
#                         # Line doesn't have bullet point, add one
#                         print(f"  • {stripped_line}")
        
#         print("\n" + "=" * 70)
# def correct_lat_lng(iso3166_2_json_filepath: str, verbose: bool = True, export: bool = True,
#                    export_filename: str = "iso3166_2_lat_lng_corrected.json") -> None:
#     """
#     Corrects None/null latLng values in the ISO 3166-2 JSON file by recalculating
#     the lat_lng data using the Geo class. Only modifies subdivisions
#     where latLng is None/null, leaving all other data unchanged.

#     Parameters
#     ==========
#     :iso3166_2_json_filepath: str
#         filepath to the exported ISO 3166-2 JSON file to correct.
#     :verbose: bool (default=True)
#         if True, prints progress messages during correction process.
#     :export: bool (default=True)
#         if True (default), exports the corrected data to a new JSON file. If False, overwrites the original.
#     :export_filename: str (default="iso3166_2_lat_lng_corrected.json")
#         filename for the exported corrected JSON file. Required when export=True.
#         Must be a valid non-empty filename string. Raises ValueError if empty or invalid when export=True.

#     Returns
#     =======
#     None

#     Raises
#     ======
#     OSError:
#         ISO 3166-2 JSON file not found at given path.
#     ValueError:
#         If export=True but export_filename is empty or invalid.
#         If a valid relation ID and lat_lng cannot be found for a subdivision.
#     """
#     #validate export_filename if export is True
#     if export:
#         if not export_filename or not isinstance(export_filename, str) or export_filename.strip() == "":
#             raise ValueError("export_filename parameter is required and must be a non-empty string when export=True.")
    
#     #raise error if JSON file not found
#     if not os.path.isfile(iso3166_2_json_filepath):
#         raise OSError(f"ISO 3166-2 JSON file not found: {iso3166_2_json_filepath}.")

#     #load the JSON file
#     with open(iso3166_2_json_filepath, 'r', encoding='utf-8') as file:
#         iso3166_2_json = json.load(file)

#     #track statistics
#     total_subdivisions = 0
#     null_lat_lng_count = 0
#     corrected_count = 0
#     failed_corrections = {}  # Changed to dict to store {full_code: (name, error_details)}
#     successful_corrections = []

#     if verbose:
#         print(f"Starting latLng correction process for {iso3166_2_json_filepath}")
#         print("=" * 70)

#     #iterate over each country and subdivision
#     for country_code, country_data in iso3166_2_json.items():
#         if verbose:
#             print(f"\nProcessing country: {country_code}")
        
#         for subdivision_code, subdivision_data in country_data.items():
#             total_subdivisions += 1
            
#             #check if this subdivision has a None/null latLng value
#             if subdivision_data.get('latLng') is None:
#                 null_lat_lng_count += 1
                
#                 if verbose:
#                     print(f"  Found null latLng for {subdivision_code} ({subdivision_data.get('name', 'Unknown')})")
                
#                 try:
#                     #import Geo locally to avoid circular imports
#                     from geo import Geo
                    
#                     #create Geo instance for this subdivision
#                     osm_subdiv = Geo(subdivision_code, proxy=None)
                    
#                     #get the lat_lng using the enhanced get_lat_lng method
#                     lat_lng = geo.get_lat_lng(verbose=verbose)
                    
#                     if lat_lng is not None:
#                         #convert tuple to list format [lat, lng]
#                         subdivision_data['latLng'] = list(lat_lng)
#                         corrected_count += 1
                        
#                         #track successful correction
#                         success_msg = f"{subdivision_code} ({subdivision_data.get('name', 'Unknown')}): {lat_lng}"
#                         successful_corrections.append(success_msg)
                        
#                         if verbose:
#                             print(f"  ✓ Successfully corrected {subdivision_code}: {lat_lng}")
#                     else:
#                         #lat_lng could not be found even after retries - use diagnostic info if available
#                         subdivision_name = subdivision_data.get('name', 'Unknown')
#                         full_code = subdivision_code
                        
#                         if hasattr(osm_subdiv, 'lat_lng_failure_reason') and osm_subdiv.lat_lng_failure_reason:
#                             error_details = osm_subdiv.lat_lng_failure_reason
#                         else:
#                             error_details = f"Failed to get valid lat_lng for {full_code} ({subdivision_name}) in {country_code}"
                        
#                         failed_corrections[full_code] = (subdivision_name, error_details)
                        
#                         if verbose:
#                             print(f"  ✗ Failed to correct {full_code}: {subdivision_name}")
                
#                 except Exception as e:
#                     subdivision_name = subdivision_data.get('name', 'Unknown')
#                     full_code = subdivision_code
#                     error_details = f"Error processing {full_code} ({subdivision_name}) in {country_code}:\n{str(e)}"
#                     failed_corrections[full_code] = (subdivision_name, error_details)
                    
#                     if verbose:
#                         print(f"  ✗ {error_details}")
                
#                 #add delay to respect API rate limits
#                 time.sleep(1)

#     #print summary statistics
#     if verbose:
#         print("\n" + "=" * 70)
#         print("Correction Summary:")
#         print(f"  Total subdivisions processed: {total_subdivisions}")
#         print(f"  Subdivisions with null latLng: {null_lat_lng_count}")
#         print(f"  Successfully corrected: {corrected_count}")
#         print(f"  Failed corrections: {len(failed_corrections)}")
#         print("=" * 70)

#     #determine output filename
#     output_file = export_filename if export else iso3166_2_json_filepath

#     #save the corrected data to the JSON file
#     with open(output_file, 'w', encoding='utf-8') as f:
#         json.dump(iso3166_2_json, f, ensure_ascii=False, indent=4)

#     if verbose:
#         print(f"\n✓ Successfully saved corrected data to {output_file}")

#     #output successful corrections if any
#     if successful_corrections and verbose:
#         print("\n" + "=" * 70)
#         print("✓ Subdivisions with Successfully Corrected latLng:")
#         print("=" * 70)
#         for success_msg in successful_corrections:
#             print(f"  • {success_msg}")
#         print("=" * 70)

#     #output failed corrections if any
#     if failed_corrections and verbose:
#         print("\n" + "=" * 70)
#         print("⚠ Subdivisions with Failed latLng Corrections:")
#         print("=" * 70)
        
#         for subdivision_code, (subdivision_name, error_details) in failed_corrections.items():
#             print(f"\n{subdivision_code}: {subdivision_name}\n")
            
#             # Parse and format error details line by line
#             error_lines = error_details.split('\n')
#             for line in error_lines:
#                 stripped_line = line.strip()
#                 if stripped_line:
#                     # Check if line already starts with a bullet point
#                     if stripped_line.startswith('•'):
#                         # Line already has bullet point, just print with indentation
#                         print(f"  {stripped_line}")
#                     else:
#                         # Line doesn't have bullet point, add one
#                         print(f"  • {stripped_line}")
        
#         print("\n" + "=" * 70)