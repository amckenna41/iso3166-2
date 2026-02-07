import pandas as pd
import re
import os 
import numpy as np
from pycountry import languages, language_families
from typing import Optional, Dict, Tuple

#import utils from same package
try:
    from . import utils
    from .utils import *
except ImportError:
    from utils import *

def add_local_other_names(all_subdivision_data: Dict[str, Dict[str, Dict[str, any]]], remove_duplicate_translations: bool = False, max_local_other_names: Optional[int] = None, 
    filepath: str = os.path.join("iso3166_2_resources", "local_other_names.csv")) -> Dict[str, Dict[str, Dict[str, any]]]:
    """
    Adding subdivision's local or other names taken from iso3166_2_resources/local_other_names.csv. 
    These values are mostly translations of the subdivision name into one or more local language 
    of the country/subdivision, but some subdivisions have multiple variations of their name,
    e.g DO-01 is officially Distrito Nacional (Santo Domingo) but is also simplified to Santo 
    Domingo City. 

    For any variations of the name in different languages, the ISO 639 2 letter or 3 letter 
    language code is appended in brackets. For any languages that do not have a corresponding
    ISO 639 code, a code from the Glottlog and other databases (e.g IETF, Linguist) will be used, 
    if applicable.

    Parameters
    ==========
    :all_subdivision_data: dict
        data object containing all subdivision data.
    :remove_duplicate_translations: bool (default=False)
        when parsing the local/other names files, some subdivision's translations into other 
        languages are the same as their official name. Set this flag to True to exclude these 
        duplicate translations otherwise they will be included by default. For example, 
        CG-7: official name in French is Likouala which is the same as it is translated 
        in English, DO-38: official name in Spanish is Enriquillo which is similar to its 
        English translation Enriquillo.
    :max_local_other_names: int (default=None)
        set the max number of local/other names to be added to each subdivision. Several 
        subdivisions may have 6 or 7 translations/other names so this var limits this for 
        all rows. By default no limit is imposed per row. Currently, the value has to be
        greater than 1. If the value input is greater than the length of the number of
        local/other names then all but 1 of the names will be removed.
    :filepath: str (default=os.path.join("iso3166_2_resources", "local_other_names.csv")))
        filepath to local/other name csv.

    Returns
    =======
    :all_subdivision_data: dict
        input subdivision data object with local or other names for the subdivisions added.
    
    Raises
    ======
    OsError:
        Local/other name csv file not found.
    ValueError:
        Max number of local/other names per subdivision row has to be an int between 1 and the 
        length of the total number of names.
        Language code not specified for local/other name.
    """
    #raise error if local/other names file not found
    if not (os.path.isfile(filepath)):
        raise OSError(f"Invalid filepath to local/other names csv: {filepath}.")

    #reading in, as dataframe, the csv that stores the local/other names for each subdivision
    local_other_names_df = pd.read_csv(os.path.join(filepath))
    
    #replace any Nan values with None
    local_other_names_df = local_other_names_df.replace(np.nan, None)
    
    """
    In terms of sorting the order of the local/other names, the vast majority retain the order that
    they are within the file itself. For any names that are non-latin translations, they will take 
    precedence over any other latin translations, for example the local arabic translation of DZ-02 
    will be sorted ahead of any other names in English. 
    """
    #set the max number of local/other names in rows, remove any additional names
    if not (max_local_other_names is None):
        def limit_local_other_names(row):
            """ Auxiliary function that limits the total number of local/other names per row, removing additional ones after reordering/sorting. """
            #skip rows with no local/other name in them
            if (row["localOtherName"]):    
                #split names into list
                local_other_name_language_split = row["localOtherName"].split(',')

                #raise error if invalid value input for var
                if not (isinstance(int(str(max_local_other_names)), int)):
                    raise ValueError("Max number of local/other names per subdivision row has to be an int between 1 and the length of the total number of names.")
                
                #parse the input value, validating its range 
                max_local_val = 0
                if (max_local_other_names > len(local_other_name_language_split)):
                    max_local_val = len(local_other_name_language_split) - 1
                elif (max_local_other_names < 1):
                    max_local_val = 1
                else:
                    max_local_val = max_local_other_names

                #get the desired limited number of local/other names in row
                local_other_name_language_split = local_other_name_language_split[-max_local_val:]

                return local_other_name_language_split

        #for each row in the local/other name column, limit the max number of local/other names
        local_other_names_df['localOtherName'] = local_other_names_df.apply(limit_local_other_names, axis=1)

    #for each row, remove any duplicate names and translations from localOtherName column
    if (remove_duplicate_translations):
        def remove_duplicate_local_other_name_translations(row):
            """ Auxiliary function that removes any duplicate translations within the localOtherName column. """
            #updated list of local/other names and languages, with any non-required names removed
            local_other_name_language_updated_list = []

            #skip rows with no local/other name in them or null
            if (row["localOtherName"]):  

                #split multiple translations/other names into comma separated list
                #preserve any items in the list of local/other names that are surrounded by quotes 
                local_other_name_language_split = split_preserving_quotes(row['localOtherName'])

                #dict to store name:language
                local_other_name_language = {}

                #iterate over local/other names, transform into dictionary of name and language using regex
                for name in local_other_name_language_split:
                    match = re.match(r'(.+?)\((.+?)\)', name.strip())
                    local_other_name_language[match.group(1).strip()] = match.group(2).strip()

                #iterate over dict of local/other names and language, if name not to be excluded (isn't the same as name column) then append to list
                for name, lang in local_other_name_language.items():
                    if (name != row['name']):
                        #validate that language code provided for local/other name
                        if (lang == "" or lang == None):
                            raise ValueError(f"Language code not specified for local/other name: {name}.")
                        local_other_name_language_updated_list.append(name + " " + "(" + lang + ")")
                
                #transform list into string of comma separated names
                local_other_name_language_updated_list = ", ".join(map(str, local_other_name_language_updated_list))
            
            #if localOtherName attribute empty for row then return row
            if (local_other_name_language_updated_list == []):
                return row["localOtherName"]
            else:
                return local_other_name_language_updated_list
        
        #for each row in the local/other name column, remove any duplicate names and local/other names, if applicable 
        local_other_names_df['localOtherName'] = local_other_names_df.apply(remove_duplicate_local_other_name_translations, axis=1)

    #sort dataframe rows by their country code and reindex rows 
    local_other_names_df = local_other_names_df.sort_values('alphaCode').reset_index(drop=True)

    #iterate over each country and subdivision, adding its local/other names if applicable
    for alpha2 in all_subdivision_data:
        for subd in list(all_subdivision_data[alpha2].keys()):
            #the local_other_names.csv file stores each subdivision's corresponding subdivision name as it is locally known or any other names for it
            #most subdivision's do not have this attribute populated as their local translation is the same as their official ISO name
            #but many subdivision's, especially those not in the latin script, have their name in the local translated language(s)
            if not (local_other_names_df.loc[local_other_names_df['subdivisionCode'] == subd]['localOtherName'].empty):
                if ((local_other_names_df.loc[local_other_names_df['subdivisionCode'] == subd]['localOtherName'].values[0] == None) or (local_other_names_df.loc[local_other_names_df['subdivisionCode'] == subd]['localOtherName'].values[0] == "")):
                    all_subdivision_data[alpha2][subd]["localOtherName"] = None
                else:
                    all_subdivision_data[alpha2][subd]["localOtherName"] = local_other_names_df.loc[local_other_names_df['subdivisionCode'] == subd]['localOtherName'].values[0]
            else:
                all_subdivision_data[alpha2][subd]["localOtherName"] = None

    return all_subdivision_data

def sort_local_other_names(filepath: str = os.path.join("iso3166_2_resources", "local_other_names.csv"), export_filepath: str = "sorted_local_other_names.csv") -> None:
    """
    Auxiliary function for sorting the order of local/other names within the csv file. For each 
    row, non-latin name translations (e.g arabic, russian) take precedence over latin variations
    of their names. This is done as if there is a non-latin translation of the subdivision name
    it is most likely to be an official language or affiliate language within the subdivision. 
    The remainder of the list of local/other names is kept in the original order in the file. 

    Parameters
    ==========
    :filepath: str (default=os.path.join("iso3166_2_resources", "local_other_names.csv"))
        filepath to the local/other names csv.
    :export_filepath: str (default="sorted_local_other_names.csv")
        filename/filepath to the sorted csv file.

    Returns
    =======
    None

    Raises
    ======
    OSError:
        Invalid filepath for local/other names csv.

    References
    ==========
    [1]: https://stackoverflow.com/questions/3094498/how-can-i-check-if-a-python-unicode-string-contains-non-western-letters
    """
    #raise error if local/other names file not found
    if not (os.path.isfile(filepath)):
        raise OSError(f"Invalid filepath to local/other names csv: {filepath}.")

    #reading in, as dataframe, the csv that stores the local/other names for each subdivision, replace any Nan values with None
    local_other_names_df = pd.read_csv(os.path.join(filepath)).replace({np.nan: None})
    
    #create deep copy of dataframe
    local_other_names_df_copy = local_other_names_df.copy(deep=True)

    #iterate over all rows in local/other name column 
    for index, row in local_other_names_df['localOtherName'].iteritems():

        #skip to next row if no local/other name value present 
        if (row is None):
            continue

        #get list of local/other name elements in the current row
        row_local_other_names = local_other_names_df.at[index, 'localOtherName'].split(',')

        latin_chars = []
        non_latin_chars = []
        all_names = []

        #iterate over each name in list, adding to latin/non-latin list, depending on output of above functions
        for name in row_local_other_names:
            #remove any leading or trailing whitespace from name
            name = name.strip()

            #append to latin or non-latin list depending on character
            if not (only_roman_chars(name)):
                non_latin_chars.append(name)
            else:
                latin_chars.append(name)
        
        #create list of reordered names, with non-latin characters prepended first
        if (non_latin_chars != []):
            all_names = sorted(non_latin_chars) + latin_chars
        else:
            all_names = sorted(row_local_other_names)

        #update current row with new order of names
        local_other_names_df_copy.loc[index, 'localOtherName'] = ", ".join(all_names)

        #export new dataframe to export filepath name
        local_other_names_df_copy.to_csv(export_filepath)

def validate_local_other_names(local_other_names_csv: str = os.path.join("iso3166_2_resources", "local_other_names.csv")) -> Tuple[int, Optional[str]]:
    """ 
    Auxiliary function that iterates through all of the rows in the local/other names
    csv which stores the data for the localOtherNames attribute for each subdivision.
    For each row and local/other names value, function validates the list of columns/
    attributes, data type, the language codes for each value and the row's format 
    (each local name capitalised and excess whitespace removed etc). If any of these 
    are not met then an error will be raised, along with a message of the description 
    of the error.

    Parameters
    ==========
    :local_other_names_csv: str
        filepath to local/other names csv.

    Returns
    =======
    :int
        if no errors are found in the local names csv then 0 will be returned, otherwise -1
        indicating an error.
    :message: str/None
        error message indicating the type of error and the line/column it was found in. If no
        error then None will be returned.
    """
    #raise error if local/other names csv dataset not found
    if not (os.path.isfile(local_other_names_csv)):
        raise OSError(f"Local/other names csv file not found:{local_other_names_csv}.")
    
    #read in local names csv as pandas df, replace any Nan values with None
    local_other_names_df = pd.read_csv(local_other_names_csv).replace(np.nan, None)

    #raise error if invalid columns found
    valid_columns = ["alphaCode", "subdivisionCode", "name", "localOtherName"]
    if (list(local_other_names_df.columns) != valid_columns):
        return -1, f"Invalid column names found in local other names csv, expected\n{valid_columns}, but got\n{local_other_names_df.columns}."

    #raise error if invalid data type found in any row for any of the columns
    for index, row in local_other_names_df.iterrows():
        for column in local_other_names_df.columns:
            value = row[column]
            if value is None or pd.isna(value):
                continue
            if not isinstance(value, str):
                return -1, f"Invalid data type found at row {index} for column {column}: {value}. Each row value should be a string or null."

    #list of non-ISO 639 language codes
    language_code_exceptions = [
            "algh1238", "berr1239", "bunj1247", "brab1243", "cang1245", "chao1238",
            "cico1238", "de-AT", "east2276", "fuzh1239", "gall1275", "high1290",
            "79-aaa-gap", "ita-tus", "juri1235", "mila1243", "mone1238", "pera1260",
            "pala1356", "poit1240-sant1407", "sant1407", "resi1246", "mori1267",
            "sama1302", "soth1248", "suba1253", "taib1240", "taib1242", "ulst1239",
            "west2343", "paha1256"
        ]

    #get list of alpha-2 and alpha-3 language codes from the ISO 639, append to the same list
    all_language_codes = []
    for lang in list(languages):
        if ('alpha_2' in dir(lang)):
            all_language_codes.append(lang.alpha_2)
        all_language_codes.append(lang.alpha_3)
    for lang in list(language_families):
        if ('alpha_3' in dir(lang)):
            all_language_codes.append(lang.alpha_3)

    #iterate over local/other name column, ensuring each translation is valid
    for index, row in local_other_names_df["localOtherName"].items():

        #skip current row if localOtherName attribute null
        if row is None or pd.isna(row):
            continue

        #split multiple local/other name translations into comma separated list, preserve single quoted elements
        local_other_names_split  = split_preserving_quotes(row)

        #parse just the local/other names from the list
        # local_names_list = [re.sub(r'\s*\(.*?\)', '', name) for name in local_other_names_split]

        #raise an error if any duplicate names with the same language code found in the file
        if len(local_other_names_split) != len(set(local_other_names_split)):
            return -1, f"Duplicate language name and language code found for {local_other_names_df.at[index, 'name']} ({local_other_names_df.at[index, 'subdivisionCode']}): {local_other_names_split}."

        #iterate over local/other names, get language code using regex, validate it
        for name in local_other_names_split:
            match = re.match(r'(.+?)\((.+?)\)', name.strip())
            language_name = match.group(1).strip()
            language_code = match.group(2).strip()

            #return error message, every local/other name should be capitalised
            if (not language_name[0].isupper()) and (only_roman_chars(language_name)) and (language_name[0] != "‘") and (isinstance(language_name,int)):
                return -1, f"Each local/other name value should be capitalised: {language_name}."

            #return error message, every local/other name should have a defined language code
            if (language_code is None):
                return -1, f"Each local/other name value in the column should have a specified language code in brackets. Row {index}, value {language_name}."

            #skip current language code if it is in the exception list 
            if (language_code in language_code_exceptions):
                continue
            
            #return error message, every local/other name translation should have a valid language code
            if not (language_code in all_language_codes):
                return -1, f"Invalid ISO 639 language code found for row value: {name}."

    return 0, None

def convert_iso_639_language_codes(filepath: str = os.path.join("iso3166_2_resources", "local_other_names.csv"), export_filepath: str = "local_other_names_sorted.csv") -> None:
    """
    Converts any ISO 639-1 (2 letter) language codes to their ISO 639-2/ISO 639-3 (3 letter) counterparts to 
    cover all languages/language families, if applicable. If there is no matching 3 letter language code then 
    the original language code will be maintained.
    
    This function was originally created as the original local/other names csv had many 2 letter ISO 639-1
    codes but it was decided to convert these to the more broader and informative 3 letter ISO 639-2/ISO 639-3 
    codes. Therefore, it's call within the above functions has been removed. 

    Parameters
    ==========
    :filepath: str (default=os.path.join("iso3166_2_resources", "local_other_names.csv"))
        filepath to local/other names csv.
    :export_filepath: str (default="local_other_names_sorted.csv")
        filename/filepath to the converted csv file

    Returns
    =======
    None

    Raises
    ======
    OsError:
        Invalid filepath for local/other names csv.
    """
    #raise error if invalid filepath input
    if not (os.path.isfile(filepath)):
        raise OSError(f"Invalid filepath for local/other names csv: {filepath}.")

    #reading in, as dataframe, the csv that stores the local/other names for each subdivision, replace any Nan values with None
    local_other_names_df = pd.read_csv(filepath).replace({np.nan: None})
    
    #creating deep copy of original dataframe
    local_other_names_df_copy = local_other_names_df.copy(deep=True)

    #iterate over each row in local/other name column
    for index, row in local_other_names_df["localOtherName"].items():
        
        #skip to next row if no local/other name value present 
        if (row is None):
            continue

        #list to maintain full list of local/other names, pre & post conversion
        local_other_name_row = []

        #split multiple local/other name translations into comma separated list, preserve any single quoted strings
        local_other_names_split = split_preserving_quotes(row)

        #iterate over local/other names, get language code and name using regex, validate it
        for name in local_other_names_split:
            match = re.match(r'(.+?)\((.+?)\)', name.strip())
            language_name = match.group(1).strip()
            language_code = match.group(2).strip()

            #lambda function to capitilse the first letter of each language name, although not if the full name is 
            #already capitalised e.g NSW should stay NSW & NT, not Nsw & Nt
            capitalize_first_letter = lambda s: s if s.isupper() else s[0].upper() + s[1:]
            language_name = capitalize_first_letter(language_name)

            #skip to next local/other name language code if length!=2, append name to list
            if (len(language_code) != 2):
                local_other_name_row.append(capitalize_first_letter(name))
                continue
            
            #get language object for inputted code from languages module of pycountry package, using alpha-2 or alpha-3
            language = languages.get(alpha_2=language_code)

            #if converted language not found, append its original name and code to the list
            if (language is None):
                local_other_name_row.append(capitalize_first_letter(name))
            #if converted language found, add its name and converted code to the list
            else:
                local_other_name_row.append(capitalize_first_letter(language_name) + " (" + language.alpha_3 + ")")

        #update the current row with the new list of names & their language codes, if no conversion made then original row is maintained
        local_other_names_df_copy.loc[index, 'localOtherName'] = ", ".join(local_other_name_row)

    #export converted dataframe to original filepath 
    local_other_names_df_copy.to_csv(export_filepath, index=False)