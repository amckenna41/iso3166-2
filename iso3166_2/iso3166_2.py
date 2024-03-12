import os
import sys
import json
import iso3166
from unidecode import unidecode
from thefuzz import process, fuzz
from urllib.parse import unquote_plus
import platform
import natsort
from collections import OrderedDict

class ISO3166_2():
    """
    This class is used to access all the ISO 3166-2 country subdivision data and attributes.
    All of the country data is stored in the iso3166-2.json, including the country's subdivision
    name, local name, type, code, parent code, latitude/longitude and URL to its flag (if applicable). 
    The desired subdivision data can be retrieved using its ISO 3166-1 alpha-2, alpha-3 or numeric 
    country codes; a comma seperate list of subdivision codes can also be input. Also you can 
    retrieve subdivisions via a built-in search functionality via its subdivision name, searching 
    for exact matches or matches based on a 'likeness' score. 

    There is also functionality to add custom subdivisions to the data object, allowing for the
    utilisation of the iso3166-2 software with custom subdivisions required for in-house/bespoke 
    applications.

    Currently, this package supports 5,039 individual subdivisions from 250 countries/territories, 
    according to the ISO 3166-1 standard, as of November 2023.
    
    Parameters
    ==========
    :country_code: str (default="")
        ISO 3166-1 alpha-2, alpha-3 or numeric country code to get subdivision data for. A list
        of country codes can also be input. If the alpha-3 or numeric codes are input, they are
        converted into their alpha-2 counterparts.
    
    Methods
    =======
    subdivision_codes(alpha_code=""):
        return a list or dict of all ISO 3166-2 subdivision codes for one or more countries 
        specified by their 2 letter alpha-2 code, 3 letter alpha-3 or numeric code.
    subdivision_names(alpha_code=""):
        return a list or dict of all ISO 3166-2 subdivision names for one or more
        countries specified by their 2 letter alpha-2 code, 3 letter alpha-3 or numeric code.
    custom_subdivision(alpha_code="", subdivision_code="", name="", local_name="", type="", 
            lat_lng=[], parent_code=None, flag_url=None, delete=0):
        add or delete a custom subdivision to an existing country on the main iso3166-2.json 
        object. Custom subdivisions and subdivision codes can be used for in-house/bespoke 
        applications that are using the iso3166-2 software but require additional custom 
        subdivisions to be represented.
    search(name="", likeness=1):
        searching for a particular subdivision and its data using its name.
    convert_to_alpha2(alpha_code):
        converts an ISO 3166 country's 3 letter alpha-3 code or numeric code into its 2 
        letter alpha-2 counterpart. 
    __getitem__(alpha_code):
        return all of a ISO 3166 country's subdivision data by making the class 
        subscriptable, according to its 2 letter alpha-2 code, 3 letter alpha-3 or 
        numeric code.

    Usage
    =====
    from iso3166_2 import * 

    #get ALL subdivision data for ALL countries
    all_subdivisions = ISO3166_2()

    #get ALL subdivision data for Lithuania, Namibia, Paraguay and Turkmenistan
    lt_subdivisions = ISO3166_2("LT")
    na_subdivisions = ISO3166_2("NA")
    pry_subdivisions = ISO3166_2("PRY")
    tm_subdivisions = ISO3166_2("795")

    #get subdivision names, local names, types, parent codes, flag urls and lat/longitudes 
    #   for GB-ANS, GB-BPL, GB-NTH, GB-WGN and GB-ZET subdivision codes for the UK
    gb_subdivisions = ISO3166_2("GB")
    
    gb_subdivisions['GB-ANS'].name
    gb_subdivisions['GB-BAS'].localName
    gb_subdivisions['GB-BPL'].type
    gb_subdivisions['GB-NTH'].parentCode
    gb_subdivisions['GB-WGN'].flagUrl
    gb_subdivisions['GB-ZET'].latLng

    #get list of all subdivision codes for Botswana
    bw_subdivisions = ISO3166_2("BW")
    bw_subdivisions.subdivision_codes()

    #get list of all subdivision names for Japan
    jpn_subdivisions = ISO3166_2("JPN")
    jpn_subdivisions.subdivision_names()

    #adding custom Belfast province to Ireland
    all_subdivisions = ISO3166_2()
    all_subdivisions.custom_subdivision("IE", "IE-BF", name="Belfast", local_name="Béal Feirste", type="province", lat_lng=[54.596, -5.931], parent_code=None, flag_url=None)
    
    #searching for the Monaghan county in Ireland (IE-MN) - returning exact matching subdivision
    all_subdivisions = ISO3166_2()
    all_subdivisions.search("Monaghan")

    #searching for any subdivisions that have "Southern" in their name, with a likeness score of 0.8
    all_subdivisions = ISO3166_2()
    all_subdivisions.search("Southern", any=True, likeness=0.8)
    """
    def __init__(self, country_code=""):

        self.country_code = country_code
        self.iso3166_json_filename= "iso3166-2.json"

        #get module path
        self.iso3166_2_module_path = os.path.dirname(os.path.abspath(sys.modules[self.__module__].__file__))
        
        #raise error if iso3166-2 json doesn't exist in the data folder
        if not (os.path.isfile(os.path.join(self.iso3166_2_module_path, self.iso3166_json_filename))):
            raise OSError("Issue finding data file {} in module directory: {}.".format(self.iso3166_json_filename, self.iso3166_2_module_path))

        #importing all subdivision data from JSON, open iso3166-2 json file and load it into class variable, loading in a JSON is different in Windows & Unix/Linux systems
        if (platform.system() != "Windows"):
            with open(os.path.join(self.iso3166_2_module_path, self.iso3166_json_filename)) as iso3166_2_json:
                self.all = json.load(iso3166_2_json)
        else:
            with open(os.path.join(self.iso3166_2_module_path, self.iso3166_json_filename), encoding="utf-8") as fp:
                self.all = json.loads(fp.read())

        #if input country code param set, iterate over data object and get subdivision data for specified input/inputs
        if (self.country_code != ""):
            temp_subdivision_data = {}
            self.country_code = self.country_code.upper().replace(" ", "").split(',')
            for code in range(0, len(self.country_code)):
                #if 3 letter alpha-3 or numeric codes input then convert to corresponding alpha-2, if invalid code then raise error
                if (len(self.country_code[code]) == 3):
                    temp_alpha2_code = self.convert_to_alpha2(self.country_code[code])
                    if (temp_alpha2_code is None and self.country_code[code].isdigit()):
                        raise ValueError("Invalid ISO 3166-1 numeric country code input, cannot convert into corresponding alpha-2 code: {}.".format(self.country_code[code]))
                    if (temp_alpha2_code is None):
                        raise ValueError("Invalid ISO 3166-1 alpha-3 country code input, cannot convert into corresponding alpha-2 code: {}.".format(self.country_code[code]))
                    self.country_code[code] = temp_alpha2_code

                #raise error if invalid alpha-2 code input
                if not (self.country_code[code] in sorted(list(iso3166.countries_by_alpha2.keys()))) or not (self.country_code[code] in list(self.all.keys())):
                    raise ValueError("Invalid alpha-2 country code input: {}.".format(self.country_code[code]))
                
                #create temporary subdivision data object
                temp_subdivision_data[self.country_code[code]] = {}
                temp_subdivision_data[self.country_code[code]] = self.all[self.country_code[code]]
            
            #delete existing 'all' class attribute that currently has all subdivision data for all countries, which aren't needed if input country is specified
            del self.all

            #set 'all' class attribute to the subdivision data from input country/countries
            self.all = temp_subdivision_data

        #get list of all countries by their 2 letter alpha-2 code
        #self.alpha_2 = sorted(list(iso3166.countries_by_alpha2.keys()))
            
        #get list of all countries by their 3 letter alpha-3 code
        #self.alpha_3 = sorted(list(iso3166.countries_by_alpha3.keys()))
            
        #get list of all countries by their numeric code
        #self.numeric = sorted(list(iso3166.countries_by_numeric.keys()))

        #list of data attributes available per subdivision
        self.attributes = ["name", "localName", "type", "parentCode", "latLng", "flagUrl"]

    def subdivision_codes(self, alpha_code=""):
        """
        Return a list or dict of all ISO 3166-2 subdivision codes for one or more
        countries specified by their 2 letter alpha-2, 3 letter alpha-3 or numeric 
        code. If the alpha-3 or numeric codes are input, these are converted into 
        their corresponding alpha-2 country codes. If a single country input then 
        return list of subdivison codes, if multiple passed in then return a dict 
        of all countries subdivision codes. If no value passed into parameter then 
        return dict of all subdivision codes for all countries. If invalid country 
        code input then raise error.

        Parameters
        ==========
        :alpha_code: str (default="")
            one or more 2 letter ISO 3166-1 alpha-2, 3 letter alpha-3 or numeric
            country codes. If no value input then all alpha-2 country codes will 
            be used.
        
        Returns
        =======
        :subdivision_codes_: list/dict
            list of a country's ISO 3166-2 subdivision codes. Or dict of all country's
            subdivision codes if no value passed into parameter.
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
            #seperate list of alpha codes into iterable comma seperated list
            alpha_code = alpha_code.upper().replace(' ', '').split(',')

            #iterate over all input alpha codes, append their subdivision codes to dict 
            for code in range(0, len(alpha_code)):
                #if 3 letter alpha-3 or numeric codes input then convert to corresponding alpha-2, else raise error
                if (len(alpha_code[code]) == 3):
                    temp_alpha_code = self.convert_to_alpha2(alpha_code[code])
                    if (temp_alpha_code is None and alpha_code[code].isdigit()):
                        raise ValueError("Invalid ISO 3166-1 numeric country code input, cannot convert into corresponding alpha-2 code: {}.".format(alpha_code[code]))
                    if (temp_alpha_code is None):
                        raise ValueError("Invalid ISO 3166-1 alpha-3 country code input, cannot convert into corresponding alpha-2 code: {}.".format(alpha_code[code]))
                    alpha_code[code] = temp_alpha_code
                #raise error if invalid alpha-2 code input
                if not (alpha_code[code] in sorted(list(iso3166.countries_by_alpha2.keys()))) or not (alpha_code[code] in list(self.all.keys())):
                    raise ValueError("Invalid alpha-2 country code input: {}.".format(alpha_code[code]))
                
                #append list of subdivision codes to dict
                subdivision_codes_[alpha_code[code]] = list(self.all[alpha_code[code]])
            
                #sort subdivision codes in json objects in alphabetical order
                subdivision_codes_[alpha_code[code]] = sorted(subdivision_codes_[alpha_code[code]])

            #if only one alpha-2 code input then return list of its subdivison codes else return dict object for all inputs
            if len(alpha_code) == 1:
                return subdivision_codes_[alpha_code[0]]
            else:
                return subdivision_codes_

    def subdivision_names(self, alpha_code=""):
        """
        Return a list or dict of all ISO 3166-2 subdivision names for one or more countries 
        specified by their 2 letter alpha-2, 3 letter alpha-3 or numeric country code. If the 
        alpha-3 or numeric codes are input, these are converted into their corresponding 
        alpha-2 country codes. If a single country input then return list of input country's 
        subdivision names, if multiple passed in return a dict of all input countries 
        subdivision names. If no value passed into parameter then return dict of all subdivision 
        names for all countries. If invalid country code input then raise error.

        Parameters
        ==========
        :alpha_code: str (default="")
            one or more 2 letter ISO 3166-1 alpha-2, 3 letter alpha-3 or numeric
            country codes. If no value input then all alpha-2 country codes will 
            be used.

        Returns
        =======
        :subdivision_names_: list/dict
            list or dict of input country's subdivision names, if no value passed into 
            parameter then all country subdivision name data is returned.
        """
        subdivision_names_ = {}

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
            #seperate list of alpha codes into iterable comma seperated list
            alpha_code = alpha_code.upper().replace(' ', '').split(',')

            #iterate over all input alpha codes, append their subdivision names to dict 
            for code in range(0, len(alpha_code)):
                #if 3 letter alpha-3 or numeric codes input then convert to corresponding alpha-2, else raise error
                if (len(alpha_code[code]) == 3):
                    temp_alpha_code = self.convert_to_alpha2(alpha_code[code])
                    if (temp_alpha_code is None and alpha_code[code].isdigit()):
                        raise ValueError("Invalid ISO 3166-1 numeric country code input, cannot convert into corresponding alpha-2 code: {}.".format(alpha_code[code]))
                    if (temp_alpha_code is None):
                        raise ValueError("Invalid ISO 3166-1 alpha-3 country code input, cannot convert into corresponding alpha-2 code: {}.".format(alpha_code[code]))
                    alpha_code[code] = temp_alpha_code

                #raise error if invalid alpha-2 code input
                if not (alpha_code[code] in sorted(list(iso3166.countries_by_alpha2.keys()))) or not (alpha_code[code] in list(self.all.keys())):
                    raise ValueError("Invalid alpha-2 country code input: {}.".format(alpha_code[code]))
                
                #append list of subdivision names to dict
                subdivision_names_[alpha_code[code]] = [self.all[alpha_code[code]][x]["name"] for x in self.all[alpha_code[code]]]
            
                #sort subdivision names in json objects in alphabetical order
                subdivision_names_[alpha_code[code]] = sorted(subdivision_names_[alpha_code[code]])

            #if only one alpha-2 code input then return list of its subdivison names else return dict object for all inputs
            if len(alpha_code) == 1:
                return subdivision_names_[alpha_code[0]]
            else:
                return subdivision_names_

    def custom_subdivision(self, alpha_code="", subdivision_code="", name="", local_name="", type="", 
            lat_lng=[], parent_code=None, flag_url=None, delete=0):
        """ 
        Add or delete a custom subdivision to an existing country on the main iso3166-2.json 
        object. The purpose of this functionality is similar to that of the user-assigned 
        code elements of the ISO 3166-1 standard. Custom subdivisions and subdivision codes 
        can be used for in-house/bespoke applications that are using the iso3166-2 software 
        but require additional custom subdivisions to be represented. If the input custom 
        subdivision code already exists then an error will be raised, otherwise it will be 
        appended to the object.

        Note that this is a destructive yet temporary functionality. Adding a new custom 
        subdivision will make the dataset out of sync with the official ISO 3166-2 data, 
        therefore it is the user's responsibility to keep track of any custom subdivisions
        and delete them when neccessary.

        If the added subdivision is required to be deleted from the object, then you can 
        call the same function with the alpha-2 and subdivision codes' parameters but also
        setting the 'delete' parameter to 1/True. 

        Parameters
        ==========
        :alpha_code: str (default="")
            ISO 3166-1 2 letter alpha-2, 3 letter alpha-3 or numeric country code.
        :subdivision_code: str (default="")
            custom subdivision code.
        :name: str (default="")
            subdivision name.
        :local_name: str (default="")
            subdivision name in local language.
        :type: str (default="")
            subdivision type e.g district, state, canton, parish etc (default="").
        :lat_lng: array (default=[])
            array of subdivision's latitude/longitude.
        :parent_code: str (default=None)
            parent subdivision code for subdivision.
        :flag_url: str (default=None)
            URL for subdivision flag, if applicable.
        :delete: bool (default=0)
            the delete flag is set to 1 if the inputted subdivision is to be deleted
            from json object.        

        Returns
        =======
        None

        Usage 
        =====
        from iso3166_2 import *

        #create instance of ISO3166_2() class
        iso = ISO3166_2()

        #adding custom Republic of Molossia state to United States 
        iso.custom_subdivision("US", "US-ML", name="Republic of Molossia", local_name="", type="State", lat_lng=[39.236, -119.588], parent_code=None, flag_url="https://upload.wikimedia.org/wikipedia/commons/c/c3/Flag_of_the_Republic_of_Molossia.svg")
        
        #adding custom Belfast province to Ireland
        iso.custom_subdivision("IE", "IE-BF", name="Belfast", local_name="Béal Feirste", type="province", lat_lng=[54.596, -5.931], parent_code=None, flag_url=None)

        #deleting above custom subdivisions
        iso.custom_subdivision("US", "US-ML", delete=1)
        iso.custom_subdivision("IE", "IE-BF", delete=1)
        """
        #open iso3166-2 json file and load it into class variable, loading in a JSON is different in Windows & Unix/Linux systems
        if (platform.system() != "Windows"):
            with open(os.path.join(self.iso3166_2_module_path, self.iso3166_json_filename)) as iso3166_2_json:
                all_subdivision_data = json.load(iso3166_2_json)
        else:
            with open(os.path.join(self.iso3166_2_module_path, self.iso3166_json_filename), encoding="utf-8") as fp:
                all_subdivision_data = json.loads(fp.read())

        #raise type error if input isn't a string
        if not (isinstance(alpha_code, str)):
            raise TypeError('Input alpha_code parameter {} is not of correct datatype string, got {}.'.format(alpha_code, type(alpha_code)))       

        #uppercase and remove whitespace
        alpha_code = alpha_code.upper().replace(' ', '')

        #raise type error if input isn't a string
        if not (isinstance(subdivision_code, str)):
            raise TypeError('Input subdivision code parameter {} is not of correct datatype string, got {}.'.format(subdivision_code, type(subdivision_code)))      

        #uppercase and remove whitespace
        subdivision_code = subdivision_code.upper().replace(' ', '')

        #raise type error if input isn't a string
        if not (isinstance(type, str)):
            raise TypeError('Input subdivision name parameter {} is not of correct datatype string, got {}.'.format(type, type(type)))      

        #if 3 letter alpha-3 or numeric codes input then convert to corresponding alpha-2, else raise error
        if (len(alpha_code) == 3):
            temp_alpha_code = self.convert_to_alpha2(alpha_code)
            if (temp_alpha_code is None and alpha_code.isdigit()):
                raise ValueError("Invalid ISO 3166-1 numeric country code input, cannot convert into corresponding alpha-2 code: {}.".format(alpha_code))
            if (temp_alpha_code is None):
                raise ValueError("Invalid ISO 3166-1 alpha-3 country code input, cannot convert into corresponding alpha-2 code: {}.".format(alpha_code))
            alpha_code = temp_alpha_code

        #raise error if invalid alpha-2 code input
        if not (alpha_code in sorted(list(iso3166.countries_by_alpha2.keys()))) or not (alpha_code in list(self.all.keys())):
            raise ValueError("Invalid ISO 3166-1 alpha-2 country code input: {}.".format(alpha_code))
    
        #delete subdivision if delete parameter set
        if (delete):
            if (subdivision_code in list(all_subdivision_data[alpha_code].keys())):
                del all_subdivision_data[alpha_code][subdivision_code] 
        else:
            #adding new subdivision data to object from input parameters
            custom_subdivision_data = {"name": name, "localName": local_name, "type": type, "parentCode": parent_code, "latLng": lat_lng, "flagUrl": flag_url}       

            #reorder subdivision attributes
            all_subdivision_data[alpha_code][subdivision_code] = {k: custom_subdivision_data[k] for k in ["name", "localName", "type", "parentCode", "flagUrl", "latLng"]}
                    
        #sort subdivision codes in json objects in natural alphabetical/numerical order using natsort library
        all_subdivision_data[alpha_code] = dict(OrderedDict(natsort.natsorted(all_subdivision_data[alpha_code].items())))

        #export the updated custom subdivision object
        with open(os.path.join(self.iso3166_2_module_path, self.iso3166_json_filename), 'w', encoding='utf-8') as output_json:
            json.dump(all_subdivision_data, output_json, ensure_ascii=False, indent=4)  

    def search(self, name="", likeness=1.0):
        """ 
        Search for a subdivision and its corresponding data using it's subdivision name. 
        The 'likeness' input parameter determines if the function searches for an exact 
        subdivision name or searches for 1 or more matching subdivisions, by default it 
        will search for an exact match (likeness=1). Setting the likeness score between
        0 and 1 will be a percentage score that names in the subdivision dataset have 
        to meet with that of the input subdivision name. A fuzzy search algorithm is 
        used to acquire the matching subdivisions via "thefuzz" package.
        
        If the default likeness score is input and no exact matching subdivision is found, 
        the likeness score will be reduced to 0.9 and then if no match is found after this 
        then an error will be raised. If multiple matching subdivisions are found then a 
        list of dicts will be returned.

        Parameters
        ==========
        :name: str (default="")
            subdivision name to search for.
        :likeness: float (default=1.0)
            likeness score between 0 and 1 that sets the percentage of likeness the input 
            subdivision name is to the list of subdivision names in the dataset. The default
            value of 1.0 will look for exact matches to the input name.
        
        Returns
        =======
        :dict/list
            if one subdivision found then a dict of its data will be returned. If one or more
            subdivisions found then a list of dicts will be returned.
        """
        #raise error if name parameter isn't a string
        if not (isinstance(name, str)):
            raise TypeError("Input subdivision name should be of type str, got {}.".format(type(name)))

        #function can also accept likeness value between 1 and 100, this will be divided to get it between 0 and 1
        if (1 < likeness < 100):
            likeness = likeness/100

        #set likeness value to 1 if invalid or out of range value input
        if not (0 < likeness < 1):
            likeness = 1

        #object to store the subdivision name and its corresponding alpha-2 code (name: alpha_2)
        all_subdivision_names = {}

        #list to store all subdivision names for all countries
        all_subdivision_names_list = []

        #list of subdivision names with comma in their official name from dataset, required if multiple subdivison names are input e.g - Murcia, Regiónde, Newry, Mourne and Down
        subdivision_name_expections = []

        #seperate list to keep track if any of input subdivsion names are exceptions (have comma in their official them)
        subdivision_name_expections_input = []
        
        #iterate over all ISO 3166-2 subdivision data, appending each subdivision's name, country code and 
        #subdivision code to object that will be used to search through, lowercase, remove whitespace and any accents,
        #if a comma is in the official subdivision name then append to the exception list only if comma is in input parameter
        for alpha_2 in self.all:
            for subd in self.all[alpha_2]:

                #append object of the subdivison's alpha-2 code and subdivision code with its name as the key
                if not (unidecode(self.all[alpha_2][subd]["name"].lower().replace(' ', '')) in list(all_subdivision_names.keys())):
                    all_subdivision_names[unidecode(unquote_plus(self.all[alpha_2][subd]["name"]).lower().replace(' ', ''))]  = []
                    all_subdivision_names[unidecode(unquote_plus(self.all[alpha_2][subd]["name"]).lower().replace(' ', ''))].append({"alpha2": alpha_2, "code": subd})
                else:
                    all_subdivision_names[unidecode(unquote_plus(self.all[alpha_2][subd]["name"]).lower().replace(' ', ''))].append({"alpha2": alpha_2, "code": subd})

                #append subdivision name to list of subdivision names for searching
                all_subdivision_names_list.append(unidecode(unquote_plus(self.all[alpha_2][subd]["name"]).lower().replace(' ', '')))

                #if comma in official subdivision name, append to the exception list, which is needed if a comma seperated list of names are input
                if (',' in name):
                    if (',' in unidecode(unquote_plus(self.all[alpha_2][subd]["name"]).lower().replace(' ', ''))):
                        subdivision_name_expections.append(unidecode(unquote_plus(self.all[alpha_2][subd]["name"]).lower().replace(' ', '')))

        #sort exceptions list alphabetically 
        subdivision_name_expections.sort()

        #decode any unicode or accent characters using utf-8 encoding, lowercase and remove additional whitespace
        name = unidecode(unquote_plus(name)).replace(' ', '').lower()
        
        #only execute subdivision name exception code if comma is in input param
        if (',' in name):
            #temp var to track input subdivision name 
            temp_subdivision_name = name

            #iterate over all subdivision names exceptions (those with a comma in their official name), append to seperate list if input param is one
            for sub_name in subdivision_name_expections:
                if (sub_name in temp_subdivision_name):
                    subdivision_name_expections_input.append(sub_name)
                    #remove current subdivision name from temp var, strip of commas
                    name = temp_subdivision_name.replace(sub_name, '').strip(',')

        #sort all subdivision names codes
        subdivision_names = sorted([name])
        
        #split multiple subdivision names into list
        subdivision_names = subdivision_names[0].split(',')

        #extend subdivsion names list if any subdivision name exceptions are present in input param
        if (subdivision_name_expections_input != []):
            subdivision_names.extend(subdivision_name_expections_input)

        #object to keep track of matching subdivisions and their data
        output_subdivisions =  {}

        #iterate over all input subdivision names, and find matching subdivision in data object
        for subdiv in subdivision_names: 

            #using thefuzz library, get all subdivisions that match the input subdivision names
            all_subdivision_name_matches = process.extract(subdiv, all_subdivision_names_list, scorer=fuzz.ratio) #partial_ratio
            name_matches = []
            
            #iterate over all found subdivision name matches, look for exact matches, if none found then look for ones that have likeness score>=90
            for match in all_subdivision_name_matches:
                #use default likeness score of 100 (exact) followed by 90 if no exact matches found
                if (likeness == 1):
                    if (match[1] == 100):
                        name_matches.append(match[0])
                    elif (match[1] >= 90):
                        name_matches.append(match[0])
                else:
                    if (match[1] >= likeness * 100):
                        name_matches.append(match[0])
                        
            #iterate over all subdivision name mathces and get corresponding subdivision object from dataset
            for subd in range(0, len(name_matches)): 
                for obj in range(0, len(all_subdivision_names[name_matches[subd]])):
                    #create temp object for subdivision and its data attributes, with its subdivision code as key
                    subdivision = self.all[all_subdivision_names[name_matches[subd]][obj]["alpha2"]][all_subdivision_names[name_matches[subd]][obj]["code"]]
                    #append subdivision data and its attributes to the output object
                    output_subdivisions[all_subdivision_names[name_matches[subd]][obj]["code"]] = subdivision

        #return object of matching subdivisions and their data
        return output_subdivisions

    def convert_to_alpha2(self, alpha_code):
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

    def __getitem__(self, alpha_code):
        """
        Return all of a country's subdivision data by making the class subscriptable via
        its alpha-2, alpha-3 or numeric country codes. A list of country data can be returned 
        if a comma seperated list of alpha codes are input. If the alpha-3 or numeric codes
        are input these will be converted into their alpha-2 counterpart. If no value input 
        then an error is raised.

        Parameters
        ==========
        :alpha_code: str
            2 letter alpha-2, alpha-3 or numeric country codes for sought country/territory 
            e.g (AD, EGY, 276). Multiple country codes of different types can be input via 
            a comma seperated list. The alpha-3 or numeric codes will be converted into their 
            alpha-2 counterpart. If no value input then an error will be raised

        Returns
        =======
        :country[alpha_code]: dict
            dict object of country/subdivision info for inputted alpha_code.

        Usage
        =====
        from iso3166_2 import *
        iso = ISO3166_2()

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
        iso["ht, mc, 516"] 
        """
        #raise type error if input isn't a string
        if not (isinstance(alpha_code, str)):
            raise TypeError('Input parameter {} is not of correct datatype string, got {}.'.format(alpha_code, type(alpha_code)))       

        #stripping input of whitespace, uppercasing and seperating into comma seperated list
        alpha_code = alpha_code.replace(' ', '').upper().split(',')

        #object to store country data
        country = {}
        
        #iterate over all input alpha codes, append their country and subdivision data to output object
        for code in range(0, len(alpha_code)):

            #if 3 letter alpha-3 or numeric codes input then convert to corresponding alpha-2, else raise error
            if (len(alpha_code[code]) == 3):
                temp_alpha_code = self.convert_to_alpha2(alpha_code[code])
                if not (temp_alpha_code is None):
                    alpha_code[code] = temp_alpha_code
                else:
                    raise ValueError("Invalid alpha-3 code input, cannot convert into corresponding alpha-2 code: {}.".format(alpha_code[code]))

            #raise error if invalid alpha-2 code input
            if not (alpha_code[code] in sorted(list(iso3166.countries_by_alpha2.keys()))) or not (alpha_code[code] in list(self.all.keys())):
                raise ValueError("Invalid alpha-2 code input: {}.".format(alpha_code[code]))
                
            #add subdivision specific data to output object 
            country[alpha_code[code]] = self.all[alpha_code[code]]

            #iterate over nested dicts, convert into instances of Map class so they can be accessed via dot notation
            for key in country[alpha_code[code]].keys():
                if (isinstance(country[alpha_code[code]][key], dict)):
                    country[alpha_code[code]][key] = Map(country[alpha_code[code]][key])

        #if only one alpha-2 code input then return list of its country data and attributes else return dict object for all inputs
        if len(alpha_code) == 1:
            return country[alpha_code[0]]
        else:
            return country
           
    def __str__(self):
        return "Instance of ISO3166_2 class."

    def __sizeof__(self):
        """ Return size of instance of ISO3166_2 class. """
        return self.__sizeof__()
    
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