import os
import sys
import json
import iso3166
from thefuzz import fuzz
from urllib.parse import unquote_plus
import pprint
import natsort
import requests
from collections import OrderedDict

class Subdivisions():
    """
    This class is used to access all the ISO 3166-2 country subdivision data and attributes, with
    all of the subdivision data stored in the iso3166-2.json object. The desired subdivision data 
    can be retrieved using its ISO 3166-1 alpha-2, alpha-3 or numeric country codes; a comma 
    separated list of codes can also be input. 

    For each country's subdivision the software supports the following attributes: 
    - code - subdivision code
    - name - subdivision name
    - localOtherName - local or alternative names that the subdivision is commonly known as in English
        and in any relevant languages to the subdivision. 
    - type - subdivision type (e.g region, municipality, canton, commune etc)
    - parentCode - parent subdivision code for the current subdivision
    - latitude/longitude - coordinates of the subdivision via the GoogleMaps location API
    - flag - URL to the subdivision's flag on the custom-built iso3166-updates repo, if applicable
    - history - historical updates/changes to the subdivision code and its data, as per the custom-built 
        iso3166-updates repo.

    You can query, filter or customize the dataset and class. The subdivision data can be searched
    via the 'search' function, searching for exact matches or approximate matches via the 'likeness'
    score input parameter. By default the search function will just search the 'name' attribute of 
    each subdivision but the 'localOtherName' attribute can be added to the search space by setting 
    the parameter local_other_name_search to True. There is also functionality to add custom 
    subdivisions to the data object, allowing for the utilization of the iso3166-2 software with
    custom subdivisions that may be required for in-house/bespoke applications. 

    Currently, this package supports 5,039 individual subdivisions from 250 countries/territories, 
    according to the ISO 3166-1 standard, as of *.
    
    Parameters
    ==========
    :country_code: str (default="")
        ISO 3166-1 alpha-2, alpha-3 or numeric countryCode to get subdivision data for. A list
        of country codes can also be input. If the alpha-3 or numeric codes are input, they are
        converted into their alpha-2 counterparts.
    :iso3166_2_filepath: str (default="")
        custom filepath to different iso3166-2 object to import that the class will use instead
        of the default iso3166-2.json object path.
    :filter_attributes: str (default="")
        str of one or more of the default attributes available for each subdivision by default,
        to be filtered into each country's subdivision object, excluding all other attributes. 
        These include: name, localOtherName, type, parentCode, latLng, flag and or history. 
        By default, all of the aforementioned keys will be exported for each subdivision.

    Methods
    =======
    subdivision_codes(alpha_code=""):
        return a list or dict of all ISO 3166-2 subdivision codes for one or more countries 
        specified by their ISO 3166-1 alpha-2, alpha-3 or numeric country codes.
    subdivision_names(alpha_code=""):
        return a list or dict of all ISO 3166-2 subdivision names for one or more
        countries specified by their ISO 3166-1 alpha-2, alpha-3 or numeric country codes.
    search(name="", likeness_score=100, filter_attribute="", local_other_name_search=False,
        exclude_match_score=True):
        searching for a particular subdivision and its data using its name. Setting the 
        'local_other_name_search' parameter to True will include the 'localOtherName'
        attribute in the search space. Setting exclude_match_score to False will include
        the % matching score the subdivision names are to the input. 
    custom_subdivision(alpha_code="", subdivision_code="", name="", local_other_name="", type_="", 
            lat_lng=[], parent_code=None, flag=None, history=None, delete=0, custom_attributes={},
            save_new=0, save_new_filename: str="iso3166_2_copy.json"):
        add or delete a custom subdivision to an existing country on the main iso3166-2.json 
        object. Custom subdivisions and subdivision codes can be used for in-house/bespoke 
        applications that are using the iso3166-2 software but require additional custom 
        subdivisions to be represented. You can also add custom attributes to the custom
        subdivision e.g area, population, gdp etc.
    check_for_updates():
        compare the current object in the software with the same object in the repo (which will
        be the latest version of the dataset). Output any differences in the objects, suggesting
        to update/reinstall the software if there's a mismatch in the data.
    convert_to_alpha2(alpha_code):
        converts an ISO 3166 country's 3 letter alpha-3 code or numeric code into its 2 
        letter alpha-2 counterpart. 
    __getitem__(alpha_code):
        return all of a ISO 3166 country's subdivision data by making the class 
        subscriptable, according to its ISO 3166-1 alpha-2, alpha-3 or numeric code.
    __len__:
        get total length of ISO 3166-2 subdivisions object - number of individual subdivisions.
    __str__:
        string representation of the instance.
    __repr__:
        object representation of the instance. 
    __sizeof__:
        total size of ISO 3166-2 subdivision object in MB.

    Usage
    =====
    from iso3166_2 import * 

    #get ALL subdivision data for ALL countries
    all_subdivisions = Subdivisions()

    #get ALL subdivision data for Lithuania, Namibia, Paraguay and Turkmenistan
    all_subdivisions["LT"]
    all_subdivisions["NA"]
    all_subdivisions["PRY"]
    all_subdivisions["795"]

    #get subdivision names, local names, types, parent codes, flag urls and lat/longitudes 
    #   for GB-ANS, GB-BPL, GB-NTH, GB-WGN and GB-ZET subdivision codes for the UK
    gb_subdivisions = Subdivisions("GB")
    
    gb_subdivisions['GB-ANS'].name
    gb_subdivisions['GB-BAS'].localOtherName
    gb_subdivisions['GB-BPL'].type
    gb_subdivisions['GB-NTH'].parentCode
    gb_subdivisions['GB-WGN'].flag
    gb_subdivisions['GB-ZET'].latLng

    #get list of all subdivision codes for Botswana
    bw_subdivisions = Subdivisions("BW")
    bw_subdivisions.subdivision_codes()

    #get list of all subdivision names for Japan
    jpn_subdivisions = Subdivisions("JPN")
    jpn_subdivisions.subdivision_names()

    #adding custom Belfast province to Ireland
    all_subdivisions = Subdivisions()
    all_subdivisions.custom_subdivision("IE", "IE-BF", name="Belfast", local_other_name="Béal Feirste", type_="province", lat_lng=[54.596, -5.931], parent_code=None, flag=None, history=None)

    #adding custom Alaska province to Russia with additional population and area attribute values
    all_subdivisions.custom_subdivision("RU", "RU-ASK", name="Alaska Oblast", local_other_name="Аляска", type_="Republic", lat_lng=[63.588, 154.493], parent_code=None, flag=None, custom_attributes={"population": "733,583", "gini": "0.43", "gdpPerCapita": "71,996"})

    #delete the above custom subdivisions
    all_subdivisions.custom_subdivision("IE", "IE-BF", delete=1)
    all_subdivisions.custom_subdivision("RU", "RU-ASK", delete=1)

    #searching for the Monaghan county in Ireland (IE-MN) - returning exact matching subdivision
    all_subdivisions = Subdivisions()
    all_subdivisions.search("Monaghan")

    #searching for the Roche Caiman district in Seychelles (SC-25) - returning exact matching subdivision (likeness=100), include Match Score attribute
    all_subdivisions.search("Roche Caiman", exclude_match_score=0)

    #searching for any subdivisions that have "Southern" in their name, with a likeness score of 80 (%)
    all_subdivisions = Subdivisions()
    all_subdivisions.search("Southern", likeness_score=80)

    #searching for state of Texas and French Department Meuse - both subdivision objects will be returned
    all_subdivisions = Subdivisions()
    all_subdivisions.search("Texas, Meuse") 

    #searching for any subdivision that has "Blue" in its name, we are also searching the local/other name attributes for name as well
    all_subdivisions = Subdivisions()
    all_subdivisions.search("Blue", local_other_name_search=True) 

    #check for the latest updates - compare current installed object with the latest on the repo
    all_subdivisions.check_for_updates()

    #get total number of subdivisions in object
    len(all_subdivisions)
    """
    def __init__(self, country_code: str="", iso3166_2_filepath: str="", filter_attributes: str=""):

        self.country_code = country_code
        self.iso3166_2_filepath = iso3166_2_filepath
        self.iso3166_json_filename= "iso3166-2.json"
        self.filter_attributes = filter_attributes
        self.__version__ = "1.8.0"

        #get full path to default object
        self.iso3166_2_module_path = os.path.join(os.path.dirname(os.path.abspath(sys.modules[self.__module__].__file__)), self.iso3166_json_filename)

        #raise error if iso3166-2 json doesn't exist in the data folder
        if not (os.path.isfile(self.iso3166_2_module_path)):
            raise OSError(f"Issue finding data file {self.iso3166_json_filename} in module directory: {self.iso3166_2_module_path}.")

        #using custom object at filepath
        if (self.iso3166_2_filepath != ""):
            self.iso3166_2_module_path = self.iso3166_2_filepath
            if not (os.path.isfile(self.iso3166_2_module_path)):
                raise OSError(f"Issue finding custom data file directory: {self.iso3166_2_module_path}.")

        #importing all subdivision data from JSON, open iso3166-2 json file and load it into class variable, raise error if issue reading in JSON
        try:
            with open(self.iso3166_2_module_path, encoding="utf-8") as fp:
                self.all = json.load(fp)
        except FileNotFoundError: 
            raise OSError("Error ❗: The ISO 3166-2 file was not found.") #**
        except json.JSONDecodeError:
            raise ValueError("Error ❗: The ISO 3166 -2dates file contains invalid JSON.")
        
        #if input country code param set, iterate over data object and get subdivision data for specified input/inputs
        if (self.country_code != ""):
            temp_subdivision_data = {}
            self.country_code = self.country_code.upper().replace(" ", "").split(',')
            for code in range(0, len(self.country_code)):
                #if 3 letter alpha-3 or numeric codes input then convert to corresponding alpha-2, if invalid code then raise error
                temp_alpha_code = self.convert_to_alpha2(self.country_code[code])
                self.country_code[code] = temp_alpha_code

                #raise error if invalid alpha-2 code input
                if not (self.country_code[code] in sorted(list(iso3166.countries_by_alpha2.keys()))) or not (self.country_code[code] in list(self.all.keys())):
                    raise ValueError(f"Invalid alpha-2 country code input: {self.country_code[code]}.")
                
                #create temporary subdivision data object
                temp_subdivision_data[self.country_code[code]] = {}
                temp_subdivision_data[self.country_code[code]] = self.all[self.country_code[code]]
            
            #delete existing 'all' class attribute that currently has all subdivision data for all countries, which aren't needed if input country is specified
            del self.all

            #set 'all' class attribute to the subdivision data from input country/countries
            self.all = temp_subdivision_data

        #parse input default attributes to include in export
        if (self.filter_attributes != ""):
            #list of default output keys/attributes per subdivision 
            filter_attributes_expected = ["name", "localOtherName", "type", "parentCode", "latLng", "flag", "history"]

            #include all attributes if * wildcard is in input param
            if (self.filter_attributes == "*"):
                self.filter_attributes = filter_attributes_expected
            else:
                    
                #parse input attribute string into list, remove whitespace
                filter_attributes_converted_list = self.filter_attributes.replace(' ', '').split(',')

                #iterate over all input keys, raise error if invalid key input
                for key in filter_attributes_converted_list:
                    if not (key in filter_attributes_expected):
                        raise ValueError(f"Attribute/field ({key}) invalid, please refer to list of the acceptable default attributes below:\n{filter_attributes_expected}.")
                
                self.filter_attributes = filter_attributes_converted_list

            #iterate over each attribute and subdivision object in self.all, remove any attributes if applicable 
            for attr in filter_attributes_expected:
                if (attr not in self.filter_attributes):
                    for alpha_code in self.all:
                        for subdivision in self.all[alpha_code]:
                            del self.all[alpha_code][subdivision][attr]
        else:
            #include all attributes in output
            self.filter_attributes = ["name", "localOtherName", "type", "parentCode", "latLng", "flag", "history"]

        #get list of all countries by their 2 letter alpha-2 code
        #self.alpha_2 = sorted(list(iso3166.countries_by_alpha2.keys()))
            
        #get list of all countries by their 3 letter alpha-3 code
        #self.alpha_3 = sorted(list(iso3166.countries_by_alpha3.keys()))
            
        #get list of all countries by their numeric code
        #self.numeric = sorted(list(iso3166.countries_by_numeric.keys()))

    def subdivision_codes(self, alpha_code: str="") -> dict|list:
        """
        Return a list or dict of all ISO 3166-2 subdivision codes for one or more
        countries specified by their ISO 3166-1 alpha-2, alpha-3 or numeric country
        codes. If the alpha-3 or numeric codes are input, these are converted into 
        their corresponding alpha-2 country codes. If a single country input then 
        return list of subdivision codes, if multiple passed in then return a dict 
        of all countries subdivision codes. If no value passed into parameter then 
        return dict of all subdivision codes for all countries. If invalid country 
        code input then raise error.

        Parameters
        ==========
        :alpha_code: str (default="")
            one or more ISO 3166-1 alpha-2, alpha-3 or numeric country codes. If 
            no value input then all alpha-2 country codes will be used.
        
        Returns
        =======
        :subdivision_codes_: list/dict
            list of a country's ISO 3166-2 subdivision codes. Or dict of all country's
            subdivision codes if no value passed into parameter.
        
        Raises
        ======
        ValueError:
            When a valid alpha-2 code input but the data is not available as not all
            country data imported on class instantiation.
        """
        subdivision_codes_ = {}

        #if no value passed into parameter, return all subdivision codes for all countries
        if (alpha_code == ""):
            #iterate over all subdivision ISO 3166-2 data, append to subdivision codes dict
            for key, _ in self.all.items():
                subdivision_codes_[key] = list(self.all[key])
            #return list of subdivision codes for country if one country in 'self.all' attribute, else return dict
            if (len(list(self.all.keys())) == 1):
                return subdivision_codes_[list(self.all.keys())[0]]
            else:
                return subdivision_codes_
        else:
            #separate list of alpha codes into iterable comma separated list
            alpha_code = alpha_code.split(',')

            #iterate over all input alpha codes, append their subdivision codes to dict 
            for code in range(0, len(alpha_code)):
                #if 3 letter alpha-3 or numeric codes input then convert to corresponding alpha-2, else raise error
                temp_alpha_code = self.convert_to_alpha2(alpha_code[code])
                alpha_code[code] = temp_alpha_code

                #raise error if country data not imported on object instantiation 
                if not (alpha_code[code] in list(self.all.keys())):
                    raise ValueError(f"Valid alpha-2 code input {alpha_code[code]}, but country data not available as country code parameter was input on class instantiation,"
                                    " try creating another instance of the class with no initial input parameter value, e.g iso = Subdivisions().")
                
                #append list of subdivision codes to dict
                subdivision_codes_[alpha_code[code]] = list(self.all[alpha_code[code]])
            
                #sort subdivision codes in json objects in alphabetical order
                subdivision_codes_[alpha_code[code]] = sorted(subdivision_codes_[alpha_code[code]])

            #if only one alpha-2 code input then return list of its subdivision codes else return dict object for all inputs
            if len(alpha_code) == 1:
                return subdivision_codes_[alpha_code[0]]
            else:
                return subdivision_codes_

    def subdivision_names(self, alpha_code: str="") -> dict|list:
        """
        Return a list or dict of all ISO 3166-2 subdivision names for one or more countries 
        specified by their ISO 3166-1 alpha-2, alpha-3 or numeric country codes. If the 
        alpha-3 or numeric codes are input, these are converted into their corresponding 
        alpha-2 country codes. If a single country input then return list of input country's 
        subdivision names, if multiple passed in return a dict of all input countries 
        subdivision names. If no value passed into parameter then return dict of all subdivision 
        names for all countries. If invalid country code input then raise error.

        Parameters
        ==========
        :alpha_code: str (default="")
            one or more ISO 3166-1 alpha-2, alpha-3 or numeric country codes. If no value input 
            then all alpha-2 country codes will be used.

        Returns
        =======
        :subdivision_names_: list/dict
            list or dict of input country's subdivision names, if no value passed into 
            parameter then all country subdivision name data is returned.
        
        Raises
        ======
        ValueError:
            If name attribute is listed as an excluded attribute.
            When a valid alpha-2 code input but the data is not available as not all
            country data imported on class instantiation.
        """
        subdivision_names_ = {}

        #raise error if name attribute was excluded on class instantiation 
        if ("name" not in self.filter_attributes):
            raise ValueError("Name attribute was excluded from subdivision outputs on class instantiation,\
                             create a new object of the class without excluding the name attribute.")

        #if no value passed into parameter, return all subdivision names for all countries
        if (alpha_code == ""):
            #iterate over all subdivision ISO 3166-2 data, append to subdivision names dict
            for key, _ in self.all.items():
                subdivision_names_[key] = [self.all[key][country]["name"] for country in self.all[key]]
                subdivision_names_[key] = sorted(subdivision_names_[key])
            #return list of subdivision names for country if one country in 'self.all' attribute, else return dict
            if (len(list(self.all.keys())) == 1):
                return subdivision_names_[list(self.all.keys())[0]] 
            else:
                return subdivision_names_
        else:
            #separate list of alpha codes into iterable comma separated list
            alpha_code = alpha_code.split(',')

            #iterate over all input alpha codes, append their subdivision names to dict 
            for code in range(0, len(alpha_code)):
                #if 3 letter alpha-3 or numeric codes input then convert to corresponding alpha-2, else raise error
                temp_alpha_code = self.convert_to_alpha2(alpha_code[code])
                alpha_code[code] = temp_alpha_code

                #raise error if country data not imported on object instantiation 
                if not (alpha_code[code] in list(self.all.keys())):
                    raise ValueError(f"Valid alpha-2 code input {alpha_code[code]}, but country data not available as country code parameter was input on class instantiation,"
                                    " try creating another instance of the class with no initial input parameter value, e.g iso = Subdivisions().")
                
                #append list of subdivision names to dict
                subdivision_names_[alpha_code[code]] = [self.all[alpha_code[code]][x]["name"] for x in self.all[alpha_code[code]]]
            
                #sort subdivision names in json objects in alphabetical order
                subdivision_names_[alpha_code[code]] = sorted(subdivision_names_[alpha_code[code]])

            #if only one alpha-2 code input then return list of its subdivision names else return dict object for all inputs
            if len(alpha_code) == 1:
                return subdivision_names_[alpha_code[0]]
            else:
                return subdivision_names_
    
    def custom_subdivision(self, alpha_code: str, subdivision_code: str, name: str=None, local_other_name: str=None, type_: str=None, 
                           lat_lng: list|str=None, parent_code: str=None, flag: str=None, history: str=None, delete: bool=0, copy: bool=0, 
                           custom_attributes: dict={}, custom_subdivision_object: dict={}, save_new: bool=0, 
                           save_new_filename: str="iso3166_2_copy.json") -> None:
        """ 
        Add or delete a custom subdivision to an existing country in the main iso3166-2.json 
        object. The purpose of this functionality is similar to that of the user-assigned 
        code elements of the ISO 3166-1 standard. Custom subdivisions and subdivision codes 
        can be used for in-house/bespoke applications that are using the iso3166-2 software 
        but require additional custom subdivisions to be represented. If the input custom 
        subdivision code already exists then an error will be raised, otherwise it will be 
        appended to the object. You can also add custom attributes to a new subdivision via
        the custom_attributes input parameter e.g population, area, gdp etc.

        Note that this is a destructive yet temporary functionality. Adding a new custom 
        subdivision will make the dataset out of sync with the official ISO 3166-2 data, 
        therefore it is the user's responsibility to keep track of any custom subdivisions
        and delete them when necessary.

        If the added subdivision is required to be deleted from the object, then you can 
        call the same function with the alpha-2 and subdivision codes' parameters but also
        setting the 'delete' parameter to 1/True. You can also uninstall and reinstall the
        software package.

        Parameters
        ==========
        :alpha_code: str 
            ISO 3166-1 alpha-2, alpha-3 or numeric country code.
        :subdivision_code: str 
            custom subdivision code.
        :name: str (default=None)
            subdivision name.
        :local_other_name: str (default=None)
            local or alternative name for the subdivision, if applicable.
        :type_: str (default=None)
            subdivision type e.g district, state, canton, parish etc.
        :lat_lng: list|str (default=None)
            array or str of subdivision's latitude/longitude.
        :parent_code: str (default=None)
            parent subdivision code for subdivision.
        :history: str (default=None)
            historical updates of subdivision, according to ISO, if applicable.
        :flag: str (default=None)
            URL for subdivision flag from iso3166-flags repo, if applicable.
        :delete: bool (default=0)
            the delete flag is set to 1 if the inputted subdivision is to be deleted
            from json object.      
        :copy: bool (default=0)
            create a duplicate copy of the iso3166-2.json object such that there remains
            a copy of the original json prior to custom subdivision change.  
        :custom_attributes: dict (default={})
            for each custom subdivision, you can also add custom attributes e.g population,
            area, gdp etc. Both the attribute and its value need to be input in a dict.
        :custom_subdivision_object: dict (default={})
            object of the new custom subdivision object with the required attributes and values. 
            If this object is populated, the values in this object will be prioritised over the 
            individual parameter values. 
        :save_new: bool (default=0)
            save a new copy of the iso3166-2.json object with the new changes applied,
            such that the original object is not overwritten. 
        :save_new_filename: str (default="iso3166_2_copy.json")
            filename for copied iso3166-2.json object with the new changes applied.

        Returns
        =======
        None

        Usage 
        =====
        from iso3166_2 import *

        #create instance of Subdivisions() class
        iso = Subdivisions()

        #adding custom Republic of Molossia state to United States 
        iso.custom_subdivision("US", "US-ML", name="Republic of Molossia", local_other_name="", type_="State", lat_lng=[39.236, -119.588], parent_code=None, flag="https://upload.wikimedia.org/wikipedia/commons/c/c3/Flag_of_the_Republic_of_Molossia.svg")
        
        #adding custom Belfast province to Ireland
        iso.custom_subdivision("IE", "IE-BF", name="Belfast", local_other_name="Béal Feirste", type_="province", lat_lng=[54.596, -5.931], parent_code=None, flag=None, history=None)

        #adding custom Belfast province to Ireland with additional population and area attribute values
        iso.custom_subdivision("IE", "IE-BF", name="Belfast", local_other_name="Béal Feirste", type_="province", lat_lng=[54.596, -5.931], parent_code=None, flag=None, custom_attributes={"population": "345,318", "area": "115Km2"})

        #deleting above custom subdivisions
        iso.custom_subdivision("US", "US-ML", delete=1)
        iso.custom_subdivision("IE", "IE-BF", delete=1)

        Raises
        ======
        TypeError:
            Invalid input parameter data types.
            Incorrect data type for latLng attribute.
        ValueError:
            Incorrect format for latLng attribute.
            Invalid alpha-2 code input.
            New custom subdivision code should be unique and not already present in the object.
            No matching subdivision object found when delete=1.
        """
        #raise type error if input isn't a string
        if not (isinstance(alpha_code, str)):
            raise TypeError(f"Input alpha_code parameter is not of correct datatype string, got {type(alpha_code)}.")       

        #raise type error if input isn't a string
        if not (isinstance(subdivision_code, str)):
            raise TypeError(f"Input subdivision code parameter is not of correct datatype string, got {type(subdivision_code)}.")   
 
        #raise type error if type isn't a string or None
        if not (isinstance(type_, str)) and not type_ is None:
            raise TypeError(f"Input subdivision type parameter is not of correct datatype string, got {type(type_)}.")  

        #parse lat_lng attribute, should be array of 2 str, can accept just a comma separated str, raise error if invalid input
        if (lat_lng != None and lat_lng != []):
            if (isinstance(lat_lng, str)):
                try:
                    temp_lat_lng = []
                    temp_lat_lng = [lat_lng.split(',')[0], lat_lng.split(',')[1]]
                    lat_lng = temp_lat_lng  
                except:
                    raise ValueError(f"Error parsing lat_lng attribute, expected a comma separated string of 2 inputs, got {lat_lng}.")
            elif not (isinstance(lat_lng, list)):
                raise TypeError(f"lat_lng attribute expected to be a list of floats or strings or a comma separated list of 2 elements, got {lat_lng}.")
        
            #round coordinates to 3d.p if applicable 
            lat_lng[0], lat_lng[1] = round(float(lat_lng[0]), 3), round(float(lat_lng[1]), 3)

        #uppercase and remove whitespace
        subdivision_code = subdivision_code.upper().replace(' ', '')
    
        #if 3 letter alpha-3 or numeric codes input then convert to corresponding alpha-2, else raise error
        alpha_code = self.convert_to_alpha2(alpha_code)

        #if only half of subdivision code input to its parameter, prepend the alpha code to it to make it valid
        if ('-' not in subdivision_code):
            subdivision_code = alpha_code + '-' + subdivision_code

        #create a copy of the original iso3166-2.json object prior to making any changes to it
        if (copy):
            test_iso3166_2_copy = os.path.join(os.path.dirname(os.path.abspath(sys.modules[self.__module__])), "iso3166_2_copy.json")
            with open(test_iso3166_2_copy, "w") as output_json:
                json.dump(self.all, output_json)

        #get subdivision data for country code
        all_subdivision_data = self.all[alpha_code]

        #bool to track if custom subdivisions are valid and should be added to the existing object
        new_update_object = False

        #delete subdivision if delete parameter set, raise error if no matching subdivision found
        if (delete):
            if (custom_subdivision_object):
                #raise error if no subdivision code found to delete
                if not (custom_subdivision_object[subdivision_code] in list(all_subdivision_data.keys())):
                    raise ValueError(f"No matching subdivision code found to delete: {custom_subdivision_object}")

                #delete subdivision object from all attribute
                del self.all[alpha_code][custom_subdivision_object[subdivision_code]]
            else:
                #raise error if no subdivision code found to delete
                if not (subdivision_code in list(all_subdivision_data.keys())):
                    raise ValueError(f"No matching subdivision code found to delete: {subdivision_code}")

                #delete subdivision object from all attribute
                del self.all[alpha_code][subdivision_code]
        else:
            if (custom_subdivision_object):
                #raise error if subdivision already present in object, cannot add custom subdivision that overwrites existing subdivision
                # if (custom_subdivision_object[subdivision_code] in list(all_subdivision_data.keys())):
                #     raise ValueError(f"Custom subdivision codes should be unique and not already present as an existing code: {custom_subdivision_object[subdivision_code]}.")
                
                #create object of new data to be added, reorder attributes
                custom_subdivision_data = {key: custom_subdivision_object[key] for key in ['name', 'localOtherName', 'type', 'parentCode', 'flag', 'latLng', 'history']}

                #add custom attributes to subdivision, if applicable
                if (custom_attributes != {}):
                    for attribute, value in custom_attributes.items():
                        custom_subdivision_data[attribute] = value

                #new object valid and can be added to updates object
                new_update_object = True 
            else:
                #create object of new data to be added from input parameters, reorder attributes
                custom_subdivision_data = {"name": name, "localOtherName": local_other_name, "type": type_, "parentCode": parent_code, "flag": flag, "latLng": lat_lng, "history": history}

                #add custom attributes to subdivision, if applicable
                if (custom_attributes != {}):
                    for attribute, value in custom_attributes.items():
                        custom_subdivision_data[attribute] = value

                #new object valid and can be added to updates object
                new_update_object = True

        #add new subdivision object to main all attribute
        if (new_update_object):
            self.all[alpha_code][subdivision_code] = custom_subdivision_data

        #export new subdivision object to custom output file if parameter set
        if (save_new):
            with open(save_new_filename, 'w', encoding='utf-8') as output_json:
                json.dump(self.all, output_json, ensure_ascii=False, indent=4)  
        #export new subdivision object to existing object
        else:
            with open(os.path.join(self.iso3166_2_module_path), 'w', encoding='utf-8') as output_json:
                json.dump(self.all, output_json, ensure_ascii=False, indent=4)  

    def search(self, input_search_term: str, likeness_score: int=100, filter_attribute: str="", local_other_name_search: bool=True, 
               exclude_match_score: bool=1) -> dict:
        """
        Search for a subdivision and its corresponding data using it's subdivision name. 
        The 'likeness_score' input parameter determines if the function searches for an exact 
        subdivision name or searches for 1 or more matching subdivisions, by default it 
        will search for an exact match (likeness_score=100). Setting the likeness score between
        0 and 100 will be a percentage likeness that subdivision names in the dataset have to 
        meet with that of the input subdivision name. A fuzzy search algorithm is used to acquire 
        the matching subdivisions via "thefuzz" package.
        
        If the default likeness score is input and no exact matching subdivision is found, 
        the likeness score will be reduced to 85, and then if no match is found after this 
        then an error will be raised. If multiple matching subdivisions are found then a 
        list of dicts will be returned. By default, the Match Score attribute will be added
        to each subdivision object, this is % score that the input search terms are to the
        found subdivision object, the output is sorted by this score.

        The filter_attribute query string parameter allows you to include only a subset of 
        required data attributes for the sought subdivisions e.g "name,localOtherName", 
        will only return the name and localOtherName attributes for any found subdivisions.

        You can also increase the search space by searching over the localOtherName attribute
        in addition to the default name attribute by setting the local_other_name_search 
        parameter to True.

        The exclude_match_score parameter allows you to exclude the Match Score attribute
        from the found subdivision objects. If this parameter is set then the output will
        be sorted alphabetically.
         
        Parameters
        ==========
        :name: str
            subdivision name to search for.
        :likeness_score: int (default=100)
            likeness score between 0 and 100 that sets the percentage of likeness the input 
            subdivision name is to the list of subdivision names in the dataset. The default
            value of 100 will look for exact matches to the input name.
        :filter_attribute: str (default="")
            include only a subset of data attributes from the list of supported attributes
            in the software. If an attribute is not found then an error will be raised. 
        :local_other_name_search: bool (default=False)
            search via the localOtherName attribute as well as the default name attribute
            for any potential matches, increasing the function search space. 
        :exclude_match_score: bool (default=True)
            set to True to exclude the % match the returned subdivision objects are to the input
            search keywords. If this attribute is excluded from the output, a dict of outputs
            will be returned, sorted alphabetically by country code, otherwise a list will be 
            returned, sorted by match score.

        Returns
        =======
        :final_results: dict/list
            resultant subdivision object found from input search terms. If one subdivision found then 
            a dict of its data will be returned, otherwise a list multiple subdivisions will be returned.
        
        Raises
        ======
        TypeError:
            Incorrect data type for name parameter.
        ValueError:
            Invalid likeness score range, should be between 1 and 100.
            Invalid attributes input to filter attributes parameter.
        """
        #raise error if search_term parameter isn't a string
        if not isinstance(input_search_term, str):
            raise TypeError(f"Input subdivision name should be of type str, got {type(input_search_term)}.")

        #raise error if invalid likeness score input (has to between 1 and 100)
        if not (0 <= likeness_score <= 100):
            raise ValueError(f"Likeness score must be between 0 and 100, got {likeness_score}.")

        #create list of subdivision attributes to search across, add localOtherName to list if applicable
        attributes_list = ["name"]
        if local_other_name_search:
            attributes_list.append("localOtherName")

        #create object of normalized subdivision entries: (normalized_name, alpha2, code)
        entries = []
        comma_names_set = set()
        for alpha2 in self.all:
            for code, data in self.all[alpha2].items():
                for attr in attributes_list:
                    val = data.get(attr)
                    if val:
                        normalized = unquote_plus(val).lower()
                        entries.append((normalized.replace(" ", ""), alpha2, code))
                        #add normalized name to separate list for names that have a comma in them
                        if ("," in val):
                            comma_names_set.add(normalized)

        #normalize, remove quotes & lowercase input search terms
        input_normalized = unquote_plus(input_search_term).lower()

        #iterate over subdivision names with commas in them and add to terms list and normalize
        terms = []
        for full_name in comma_names_set:
            if full_name in input_normalized:
                terms.append(full_name.replace(" ", ""))
                input_normalized = input_normalized.replace(full_name, "")
        leftover_terms = [t.strip().replace(" ", "") for t in input_normalized.split(",") if t.strip()]
        terms.extend(leftover_terms)

        #iterate over input search terms, use a fuzzy search algorithm to get any matching names/localOther names,
        # using the likeness parameter as a % likeness the input terms have to be to the subdivision names
        found = {}
        for term in terms:
            matches = []
            for norm_name, alpha2, code in entries:
                likeness = fuzz.ratio(term, norm_name)
                if likeness_score == 100 and likeness == 100:
                    matches.append((alpha2, code, likeness))
                elif likeness_score < 100 and likeness >= likeness_score:
                    matches.append((alpha2, code, likeness))

            #fallback: if no matches found, reduce the likeness slightly
            if likeness_score == 100 and not matches:
                for norm_name, alpha2, code in entries:
                    likeness = fuzz.ratio(term, norm_name)
                    if likeness >= 85:
                        matches.append((alpha2, code, likeness))

            #add found matching objects to found object, including % Match Score, Country & Subdivision Code
            for alpha2, code, score in matches:
                if code not in found:
                    found[code] = {
                        **self.all[alpha2][code],
                        "matchScore": score,
                        "countryCode": alpha2,
                        "subdivisionCode": code
                    }

        #filter out attributes from subdivision object, if applicable
        if filter_attribute:
            filter_list = filter_attribute.replace(" ", "").split(",")
            valid_attrs = {"name", "localOtherName", "type", "parentCode", "flag", "latLng", "history"}
            #if wildcard in filter list, add all attributes to output
            if "*" in filter_list:
                filter_list = list(valid_attrs)
            #raise error if invalid attribute input
            elif not all(attr in valid_attrs for attr in filter_list):
                raise ValueError(f"Invalid attribute(s) in filter_attribute: {filter_list}")
            #iterate over search results, filtering out the non-required attributes & keeping the main default attributes
            for code in list(found.keys()):
                match_score = found[code].get("matchScore")
                country_code = found[code].get("countryCode")
                filtered = {k: v for k, v in found[code].items() if k in filter_list}
                filtered["subdivisionCode"] = code
                filtered["countryCode"] = country_code
                if not exclude_match_score and match_score is not None:
                    filtered["matchScore"] = match_score
                found[code] = filtered

        #exclude the % match score attribute from subdivision objects
        if exclude_match_score:
            grouped = {}
            #iterate over nested subdivision objects, removing Match Score, Country Code & Subdivision Code attributes
            for code, data in found.items():
                data.pop("matchScore", None)
                country_code = data.pop("countryCode", "")
                sub_code = data.pop("subdivisionCode", code)
                #set the parent key of the subdivision object to its alpha country code
                grouped.setdefault(country_code, {})[sub_code] = data
            return dict(sorted(grouped.items()))
        else:
            final_results = []
            #iterate over all subdivision objects, reordering attributes with inclusion of Match Score
            for code, data in found.items():
                entry = {
                    "countryCode": data.pop("countryCode", ""),
                    "subdivisionCode": data.pop("subdivisionCode", code),
                    **data,
                    "matchScore": data.pop("matchScore", 0)
                }
                #append to results array
                final_results.append(entry)

            #reorder results via Match Score attribute, descending
            final_results.sort(key=lambda x: x.get("matchScore", 0), reverse=True)

            return final_results

    @staticmethod
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

    def __getitem__(self, alpha_code: str) -> dict:
        """
        Return all of a country's subdivision data by making the class subscriptable via
        its ISO 3166-1 alpha-2, alpha-3 or numeric country codes. A list of country data 
        can be returned if a comma separated list of alpha codes are input. If the alpha-3 
        or numeric codes are input these will be converted into their alpha-2 counterpart. 
        If no value input then an error is raised.

        Parameters
        ==========
        :alpha_code: str
            ISO 3166-1 2 letter alpha-2, alpha-3 or numeric country codes for sought
            country/territory e.g (AD, EGY, 276). Multiple country codes of different types 
            can be input via a comma separated list. The alpha-3 or numeric codes will be 
            converted into their alpha-2 counterpart. If no value input then an error will 
            be raised.

        Returns
        =======
        :country[alpha_code]: dict
            dict object of country/subdivision info for inputted alpha_code.

        Usage
        =====
        from iso3166_2 import *
        iso = Subdivisions()

        #get subdivision info for Ethiopia
        iso["ET"] 
        iso["ETH"] 
        iso["231"] 
 
        #get subdivision info for Gabon
        iso["GA"] 
        iso["GAB"] 
        iso["266"] 

        #get subdivision info for Rwanda
        iso["RW"]
        iso["RWA"]
        iso["646"]

        #get subdivision info for Haiti, Monaco and Namibia
        iso["HT, MC, NA"] 
        iso["HTI, MCO, NAM"] 
        iso["332, 492, 516"] 

        Raises
        ======
        TypeError:
            Invalid data type for alpha code parameter.
        ValueError:
            When a valid alpha-2 code input but the data is not available as not all
            country data imported on class instantiation.
        """
        #raise type error if input isn't a string
        if not (isinstance(alpha_code, str)):
            raise TypeError(f"Input parameter {alpha_code} is not of correct datatype string, got {type(alpha_code)}.")       

        #separate alpha codes into into comma separated list
        alpha_code = alpha_code.split(',')

        #object to store country data
        country = {}
        
        #iterate over all input alpha codes, append their country and subdivision data to output object
        for code in range(0, len(alpha_code)):

            #if 3 letter alpha-3 or numeric codes input then convert to corresponding alpha-2, else raise error
            alpha_code[code] = self.convert_to_alpha2(alpha_code[code])

            #raise error if country data not imported on object instantiation 
            if not (alpha_code[code] in list(self.all.keys())):
                raise ValueError(f"Valid alpha-2 code input {alpha_code[code]}, but country data not available as country code parameter was input on class instantiation,"
                                 " try creating another instance of the class with no initial input parameter value, e.g iso = Subdivisions().")
                
            #add subdivision specific data to output object 
            country[alpha_code[code]] = self.all[alpha_code[code]]

            #iterate over nested dicts, convert into instances of Map class so they can be accessed via dot notation
            for key in country[alpha_code[code]].keys():
                if (isinstance(country[alpha_code[code]][key], dict)):
                    country[alpha_code[code]][key] = Map(country[alpha_code[code]][key])

        #if only one alpha-2 code input then return its country view; else return dict of views
        if len(alpha_code) == 1:
            a2 = alpha_code[0]
            return CountrySubdivisions(self, a2, country[a2])
        else:
            #wrap each country entry so you can also do subd["AD"].subdivision_names() & subd["AD"].subdivision_codes()
            for a2 in list(country.keys()):
                country[a2] = CountrySubdivisions(self, a2, country[a2])
            return country

        # #if only one alpha-2 code input then return list of its country data and attributes else return dict object for all inputs
        # if len(alpha_code) == 1:
        #     return country[alpha_code[0]]
        # else:
        #     return country
    
    def check_for_updates(self):
        """ 
        Pull the latest version of the object from the repo, comparing it with the current 
        version of the object installed in the software. If new updates/changes are found
        output them and a message encouraging the user to download latest version.

        Parameters
        ==========
        None

        Returns
        =======
        None

        Raises
        ======
        requests.exceptions.RequestException:
            Error pulling data object from URL.
        """
        #pull latest data object from repo using requests library
        try:
            response = requests.get("https://raw.githubusercontent.com/amckenna41/iso3166-2/main/iso3166_2/iso3166-2.json")
            response.raise_for_status()
            latest_iso3166_2_json = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch the latest updates data from: {e}.")
            return
            
        #separate object that holds individual data objects that were found on the object in the repo that weren't in the software object
        new_iso3166_2 = {}

        #bool to track if any new updates found
        updates_found = False

        #iterate over all ISO 3166-2 data in latest object on repo, if update/row not found in current json in software version, append to new updated_json object 
        for alpha_code, entries in latest_iso3166_2_json.items():
            current_entries = self.all.get(alpha_code, {})
            new_iso3166_2[alpha_code] = {}

            #update objects and vars to track if new data found
            for key, value in entries.items():
                if key not in current_entries or current_entries[key] != value:
                    updates_found = True
                    new_iso3166_2[alpha_code][key] = value

            #sort the updates
            new_iso3166_2[alpha_code] = OrderedDict(natsort.natsorted(new_iso3166_2[alpha_code].items()))

            #remove any entries with no updates
            if not new_iso3166_2[alpha_code]:
                new_iso3166_2.pop(alpha_code, None)
                
        #print out any found updates 
        if (updates_found):

            print("New ISO 3166-2 data found, please update the iso3166-2 software to incorporate these latest changes, you can do this by running:")
            print("pip install iso3166-2 --upgrade\n\n\n")

            #get total sum of new data updates for all countries and subdivisions in json
            total_updates = sum(len(code) for code in new_iso3166_2.values())
            total_countries = len(new_iso3166_2)
            
            print(f"{str(total_updates)} update(s) found for {str(total_countries)} country/countries, these are outlined below")
            print("==================================================================\n\n")
            
            #iterate over all found updates, print them out
            for code, updates in new_iso3166_2.items():
                #get country name from code
                country_name = iso3166.countries_by_alpha2[code].name
                print(f"{country_name} ({code}):")
                pprint.pprint(updates, compact=True)
        #no updates found
        else:
            print("No new updates found for iso3166-2.")
             
    def __str__(self) -> str:
        """ Return string representation of the class instance. """
        return f"Instance of Subdivisions class. Path: {self.iso3166_2_module_path}, Version {self.__version__}."
    
    def __repr__(self) -> str:
        """ Return object representation of class instance. """
        return f"<iso3166-2(version={self.__version__}, total_subdivisions={len(self)}, source_file={os.path.basename(self.iso3166_2_module_path)})>"

    def __len__(self) -> int:
        """ Return total number of ISO 3166-2 subdivisions. """
        return sum(len(subdivisions) for subdivisions in self.all.values())
    
    def __sizeof__(self):
        """ Return size of instance of Subdivisions class/iso3166-2 object. """
        size_in_bytes = os.path.getsize(self.iso3166_2_module_path)  
        size_in_mb = size_in_bytes / (1024 * 1024) 
        return round(size_in_mb, 3)
    
class Map(dict):
    """
    Class that accepts a dict and allows you to use dot notation to access
    members of the dictionary. 

    Parameters
    ==========
    :dict
        input dictionary to convert into instance of map class so the keys/vals
        can be accessed via dot notation.

    Usage
    =====
    # create instance of map class
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    # Add new key
    m.new_key = 'Hello world!'
    # Or
    m['new_key'] = 'Hello world!'
    # Update values
    m.new_key = 'Yay!'
    # Or
    m['new_key'] = 'Yay!'
    # Delete key
    del m.new_key
    # Or
    del m['new_key']

    References
    ==========
    [1]: https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary
    """
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v
        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]
        
class CountrySubdivisions(Map):
    """
    Auxiliary class for the subscriptable subdivision data via the Map class,
    allowing the subdivision_codes() and subdivision_names() functions to be called.
   ."""
    def __init__(self, parent: "Subdivisions", alpha2: str, data: dict):
        super().__init__(data)
        object.__setattr__(self, "_parent", parent)
        object.__setattr__(self, "_alpha2", alpha2)

    def subdivision_codes(self) -> list[str]:
        #call the function of the parent via the country's alpha-2
        return self._parent.subdivision_codes(self._alpha2)

    def subdivision_names(self) -> list[str]:
        #call the function of the parent via the country's alpha-2
        return self._parent.subdivision_names(self._alpha2)