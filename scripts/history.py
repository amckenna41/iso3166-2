from urllib.parse import unquote_plus
import re
from iso3166_updates import *

def add_history(input_country_data: dict) -> dict:
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
    for alpha2 in list(input_country_data.keys()):
        if (alpha2 == "XK"):
            continue

        #get updated data for current country using alpha-2 code
        current_alpha2_updates = iso_updates[alpha2]
        for subd in list(input_country_data[alpha2].keys()):

            #create set for the matching attributes, add subdivision code, name and local/other name
            matching_attributes = set()
            matching_attributes.add(unquote_plus(subd.lower()))
            matching_attributes.add(unquote_plus(input_country_data[alpha2][subd]["name"].lower().replace(' ', '')))

            #if local/other name attribute not empty, append each of its names to the search list
            if not (input_country_data[alpha2][subd]["localOtherName"] is None):

                #normalize local/other name & remove language codes from localOtherName attribute
                local_other_cleaned = re.sub(r'\s*\(.*?\)', '', input_country_data[alpha2][subd]["localOtherName"])
                local_names = re.split(r',\s*', local_other_cleaned)
                for name in local_names:
                    matching_attributes.add(unquote_plus(name.lower().strip()))

            #create history attribute in output object
            input_country_data[alpha2][subd]["history"] = []

            #iterate over each ISO 3166 update for current country, if subdivision code, name or local name found in updates description then append description, publication date and Source to history attribute
            for update in current_alpha2_updates[alpha2]:
            
                #get normalized version of change and desc of change attributes
                norm_change = unquote_plus(update.get("Change", "")).lower()
                norm_desc = unquote_plus(update.get("Description of Change", "")).lower()

                #if match found between matching_attributes and country updates data, add to history attribute
                if any(attr in norm_change for attr in matching_attributes) or any(attr in norm_desc for attr in matching_attributes):
                    # historical_change = update["Date Issued"] + ": " + update["Change"]
                    # if update["Description of Change"]:
                    #     historical_change += " Description of Change: " + update["Description of Change"]
                    # historical_change += " Source: " + update["Source"]
                    input_country_data[alpha2][subd]["history"].append(update)

            #if no history attribute value found for current subdivision, set to None
            if not input_country_data[alpha2][subd]["history"]:
                input_country_data[alpha2][subd]["history"] = None
                
    return input_country_data