import os
import sys
import json
import iso3166
import platform
from difflib import get_close_matches
import natsort
from collections import OrderedDict

class ISO3166_2():
    """
    This class is used to access all the ISO 3166-2 country subdivision data and attributes.
    All of the country data is stored in the iso3166-2.json, including the country's subdivision
    name, local name, type, code, parent code, lat/longitude and URL to its flag (if applicable). 
    The JSON is generated using the get_iso3166_2.py script in the iso3166_2_scripts directory. 
    All of the keys and objects in the JSON are accessible via dot notation via the Map class. 

    There is also functionality to add custom subdivisions to the data object, allowing for the
    utilisation of the iso3166-2 software with custom subdivisions required for in-house/bespoke 
    applications. Also you can search for a specific subdivision via its name, either searching
    for an exact subdivision match or return a list of approximately matching subdivisions.

    Currently, this package supports 5,039 individual subdivisions from 250 countries/territories, 
    according to the ISO 3166-1 standard, as of November 2023.
    
    Parameters
    ==========
    None
    
    Methods
    =======
    subdivision_codes(alpha2_code=""):
        return a list or dict of all ISO 3166-2 subdivision codes for one or more
        countries specified by their 2 letter alpha-2 code.
    subdivision_names(alpha2_code=""):
        return a list or dict of all ISO 3166-2 subdivision names for one or more
        countries specified by their 2 letter alpha-2 code.
    subdivision_parent_codes(alpha2_code=""):
        return a list or dict of all ISO 3166-2 subdivision parent codes for one 
        or more countries specified by their 2 letter alpha-2 code.
    custom_subdivision(alpha2_code="", subdivision_code="", name="", local_name="", type="", 
            lat_lng=[], parent_code=None, flag_url=None, delete=0):
        add or delete a custom subdivision to an existing country on the main iso3166-2.json 
        object. Custom subdivisions and subdivision codes can be used for in-house/bespoke 
        applications that are using the iso3166-2 software but require additional custom 
        subdivisions to be represented.
    search(name="", any=False):
        searching for a particular subdivision and its data using its name.
    __getitem__(alpha2_code):
        return all of a ISO 3166 country's subdivision data by making the class 
        subscriptable, according to its 2 letter alpha-2 code.

    Usage
    =====
    import iso3166_2 as iso

    #get ALL subdivision data for Lithuania, Namibia, Paraguay and Turkmenistan
    iso.country['LT'].subdivisions
    iso.country['NA'].subdivisions
    iso.country['PY'].subdivisions
    iso.country['TM'].subdivisions

    #get subdivision names, local names, types, parent codes, flag urls and lat/longitudes 
    #   for GB-ANS, GB-BPL, GB-NTH, GB-WGN and GB-ZET subdivision codes for the UK
    iso.country['GB'].subdivisions['GB-ANS'].name
    iso.country['GB'].subdivisions['GB-BAS'].localName
    iso.country['GB'].subdivisions['GB-BPL'].type
    iso.country['GB'].subdivisions['GB-NTH'].parentCode
    iso.country['GB'].subdivisions['GB-WGN'].flagUrl
    iso.country['GB'].subdivisions['GB-ZET'].latLng

    #get list of all subdivision codes for Botswana
    iso.subdivision_codes("BW")

    #get list of all subdivision names for Japan
    iso.subdivision_names("JP")

    #adding custom Belfast province to Ireland
    iso.country.custom_subdivision("IE", "IE-BF", name="Belfast", local_name="Béal Feirste", type="province", lat_lng=[54.596, -5.931], parent_code=None, flag_url=None)
    
    #searching for the Monaghan county in Ireland (IE-MN) - returning exact matching subdivision
    iso.country.search("Monaghan", any=False)

    #searching for any subdivisions that have "Southern" in their name
    iso.country.search("Southern", any=True)
    """
    def __init__(self):

        self.iso3166_json_filename= "iso3166-2.json"
        self.data_folder = "iso3166-2-data"

        #get module path
        self.iso3166_2_module_path = os.path.dirname(os.path.abspath(sys.modules[self.__module__].__file__))
        
        #raise error if iso3166-2 json doesn't exist in the data folder
        if not (os.path.isfile(os.path.join(self.iso3166_2_module_path, self.data_folder, self.iso3166_json_filename))):
            raise OSError("Issue finding {} in data dir {}.".format(self.iso3166_json_filename, self.data_folder))

        #open iso3166-2 json file and load it into class variable, loading in a JSON is different in Windows & Unix/Linux systems
        if (platform.system() != "Windows"):
            with open(os.path.join(self.iso3166_2_module_path, self.data_folder, self.iso3166_json_filename)) as iso3166_2_json:
                self.all = json.load(iso3166_2_json)
        else:
            with open(os.path.join(self.iso3166_2_module_path, self.data_folder, self.iso3166_json_filename), encoding="utf-8") as fp:
                self.all = json.loads(fp.read())

        #get list of all countries by their 2 letter alpha-2 code
        self.alpha_2 = sorted(list(iso3166.countries_by_alpha2.keys()))

        #list of data attributes available per subdivision
        self.attributes = ["name", "localName", "type", "parentCode", "latLng", "flagUrl"]

    def subdivision_codes(self, alpha2_code=""):
        """
        Return a list or dict of all ISO 3166-2 subdivision codes for one or more
        countries specified by their 2 letter alpha-2 code. If a single country 
        input then return list of subdivison codes, if multiple passed in then return 
        a dict of all countries subdivision codes. The function can also accept the 3 
        letter alpha-3 code for a country which is converted into its 2 letter alpha-2 
        counterpart. If no value passed into parameter then return dict of all 
        subdivision codes for all countries. If invalid country code input then raise 
        error.

        Parameters
        ==========
        :alpha2_code: str (default="")
            one or more 2 letter ISO 3166-1 alpha-2 codes; the 3 letter alpha-3 country
            code can also be accepted. If no value input then all alpha-2 country codes
            will be used.
        
        Returns
        =======
        :subdivision_codes_: list/dict
            list of a country's ISO 3166-2 subdivision codes. Or dict of all country's
            subdivision names if no value passed into parameter.
        """
        subdivision_codes_ = {}

        #if no value passed into parameter, return all subdivision codes for all countries
        if (alpha2_code == ""):
            #iterate over all subdivision ISO 3166-2 data, append to subdivision codes dict
            for key, _ in self.all.items():
                subdivision_codes_[key] = list(self.all[key])
            return subdivision_codes_
        else:
            #seperate list of alpha-2 codes into iterable comma seperated list
            alpha2_code = alpha2_code.replace(' ', '').split(',')

            #iterate over all input alpha-2 codes, append their subdivision codes to dict 
            for code in range(0, len(alpha2_code)):

                #if 3 letter alpha-3 codes input then convert to corresponding alpha-2, else raise error
                if (len(alpha2_code[code]) == 3):
                    temp_alpha2_code = convert_to_alpha2(alpha2_code[code])
                    if not (temp_alpha2_code is None):
                        alpha2_code[code] = temp_alpha2_code
                    else:
                        raise ValueError("Invalid alpha-3 code input, cannot convert into corresponding alpha-2 code: {}.".format(alpha2_code[code]))
                    
                #raise error if invalid alpha-2 code input
                if not (alpha2_code[code] in sorted(list(iso3166.countries_by_alpha2.keys()))):
                    raise ValueError("Invalid alpha-2 code input: {}.".format(alpha2_code[code]))

                #append list of subdivision codes to dict
                subdivision_codes_[alpha2_code[code]] = list(self.all[alpha2_code[code]])
            
                #sort subdivision codes in json objects in alphabetical order
                subdivision_codes_[alpha2_code[code]] = sorted(subdivision_codes_[alpha2_code[code]])

            #if only one alpha-2 code input then return list of its subdivison codes else return dict object for all inputs
            if len(alpha2_code) == 1:
                return subdivision_codes_[alpha2_code[0]]
            else:
                return subdivision_codes_

    def subdivision_names(self, alpha2_code=""):
        """
        Return a list or dict of all ISO 3166-2 subdivision names for one or more countries 
        specified by their 2 letter alpha-2 code. If a single country input then return 
        list of input country's subdivision names, if multiple passed in return a dict of all
        input countries subdivision names. The function can also accept the 3 letter alpha-3 
        code for a country which is converted into its 2 letter alpha-2 counterpart. If no value
        passed into parameter then return dict of all subdivision names for all countries. If 
        invalid country code input then raise error.

        Parameters
        ==========
        :alpha2_code: str (default="")
            one or more 2 letter ISO 3166-1 alpha-2 codes; the 3 letter alpha-3 country
            code can also be accepted. If no value input then all alpha-2 country codes
            will be used.

        Returns
        =======
        :subdivision_names_: list/dict
            list or dict of input country's subdivision names, if no value passed into 
            parameter then all country subdivision name data is returned.
        """
        subdivision_names_ = {}

        #if no value passed into parameter, return all subdivision names for all countries
        if (alpha2_code == ""):
            #iterate over all subdivision ISO 3166-2 data, append to subdivision names dict
            for key, _ in self.all.items():
                subdivision_names_[key] = [self.all[key][country]["name"] for country in self.all[key]]
            return subdivision_names_
        else:
            #seperate list of alpha-2 codes into iterable comma seperated list
            alpha2_code = alpha2_code.replace(' ', '').split(',')

            #iterate over all input alpha-2 codes, append their subdivision names to dict 
            for code in range(0, len(alpha2_code)):

                #if 3 letter alpha-3 codes input then convert to corresponding alpha-2, else raise error
                if (len(alpha2_code[code]) == 3):
                    temp_alpha2_code = convert_to_alpha2(alpha2_code[code])
                    if not (temp_alpha2_code is None):
                        alpha2_code[code] = temp_alpha2_code
                    else:
                        raise ValueError("Invalid alpha-3 code input, cannot convert into corresponding alpha-2 code: {}.".format(alpha2_code[code]))

                #raise error if invalid alpha-2 code input
                if not (alpha2_code[code] in sorted(list(iso3166.countries_by_alpha2.keys()))):
                    raise ValueError("Invalid alpha-2 code input: {}.".format(alpha2_code[code]))

                #append list of subdivision names to dict
                subdivision_names_[alpha2_code[code]] = [self.all[alpha2_code[code]][x]["name"] for x in self.all[alpha2_code[code]]]
            
                #sort subdivision names in json objects in alphabetical order
                subdivision_names_[alpha2_code[code]] = sorted(subdivision_names_[alpha2_code[code]])

            #if only one alpha-2 code input then return list of its subdivison names else return dict object for all inputs
            if len(alpha2_code) == 1:
                return subdivision_names_[alpha2_code[0]]
            else:
                return subdivision_names_

    def subdivision_local_names(self, alpha2_code=""):
        """
        Return a list or dict of all ISO 3166-2 subdivision local names for one or more countries 
        specified by their 2 letter alpha-2 code. If a single country input then return 
        list of input country's subdivision local names, if multiple passed in return a dict of all
        input countries subdivision local names. The function can also accept the 3 letter alpha-3 
        code for a country which is converted into its 2 letter alpha-2 counterpart. If no value
        passed into parameter then return dict of all subdivision local names for all countries. 
        If invalid country code input then raise error.

        Parameters
        ==========
        :alpha2_code: str (default="")
            one or more 2 letter ISO 3166-1 alpha-2 codes; the 3 letter alpha-3 country
            code can also be accepted. If no value input then all alpha-2 country codes
            will be used.

        Returns
        =======
        :subdivision_local_names_: list/dict
            list or dict of input country's subdivision local names, if no value passed into 
            parameter then all country subdivision local name data is returned.
        """
        subdivision_local_names_ = {}

        #if no value passed into parameter, return all subdivision local names for all countries
        if (alpha2_code == ""):
            #iterate over all subdivision ISO 3166-2 data, append to subdivision local names dict
            for key, _ in self.all.items():
                subdivision_local_names_[key] = [self.all[key][country]["localName"] for country in self.all[key]]
            return subdivision_local_names_
        else:
            #seperate list of alpha-2 codes into iterable comma seperated list
            alpha2_code = alpha2_code.replace(' ', '').split(',')

            #iterate over all input alpha-2 codes, append their subdivision local names to dict 
            for code in range(0, len(alpha2_code)):

                #if 3 letter alpha-3 codes input then convert to corresponding alpha-2, else raise error
                if (len(alpha2_code[code]) == 3):
                    temp_alpha2_code = convert_to_alpha2(alpha2_code[code])
                    if not (temp_alpha2_code is None):
                        alpha2_code[code] = temp_alpha2_code
                    else:
                        raise ValueError("Invalid alpha-3 code input, cannot convert into corresponding alpha-2 code: {}.".format(alpha2_code[code]))

                #raise error if invalid alpha-2 code input
                if not (alpha2_code[code] in sorted(list(iso3166.countries_by_alpha2.keys()))):
                    raise ValueError("Invalid alpha-2 code input: {}.".format(alpha2_code[code]))

                #append list of subdivision local names to dict
                subdivision_local_names_[alpha2_code[code]] = [self.all[alpha2_code[code]][x]["localName"] for x in self.all[alpha2_code[code]]]
            
                #sort subdivision local names in json objects in alphabetical order
                subdivision_local_names_[alpha2_code[code]] = sorted(subdivision_local_names_[alpha2_code[code]])

            #if only one alpha-2 code input then return list of its subdivison local names else return dict object for all inputs
            if len(alpha2_code) == 1:
                return subdivision_local_names_[alpha2_code[0]]
            else:
                return subdivision_local_names_
            
    def subdivision_parent_codes(self, alpha2_code=""):
        """
        Return a list or dict of all ISO 3166-2 subdivision parent codes for one or more countries 
        specified by their 2 letter alpha-2 code. If a single country is input then return list of 
        input country's subdivision parent codes, if multiple passed in return a dict of all input 
        country's subdivision parent codes. The function can also accept the 3 letter alpha-3 
        code for a country which is converted into its 2 letter alpha-2 counterpart. If no value
        passed into parameter then return dict of all subdivision parent codes for all countries. 
        If invalid country code/codes input then raise error.

        Parameters
        ==========
        :alpha2_code: str (default="")
            one or more 2 letter ISO 3166-1 alpha-2 codes; the 3 letter alpha-3 country
            code can also be accepted. If no value input then all alpha-2 country codes
            will be used.

        Returns
        =======
        :subdivision_parent_codes_: list/dict
            list or dict of input country's subdivision parent codes, if no value passed into 
            parameter then all country subdivision name data is returned.
        """
        subdivision_parent_codes_ = {}

        #if no value passed into parameter, return all subdivision parent codes for all countries
        if (alpha2_code == ""):
            #iterate over all subdivision ISO 3166-2 data, append to subdivision parent codes dict
            for key, _ in self.all.items():
                subdivision_parent_codes_[key] = [self.all[key][country]["parentCode"] for country in self.all[key]]
            return subdivision_parent_codes_
        else:
            #seperate list of alpha-2 codes into iterable comma seperated list
            alpha2_code = alpha2_code.replace(' ', '').upper().split(',')

            #iterate over all input alpha-2 codes, append their subdivision parent codes to dict 
            for code in range(0, len(alpha2_code)):

                #if 3 letter alpha-3 codes input then convert to corresponding alpha-2, else raise error
                if (len(alpha2_code[code]) == 3):
                    temp_alpha2_code = convert_to_alpha2(alpha2_code[code])
                    if not (temp_alpha2_code is None):
                        alpha2_code[code] = temp_alpha2_code
                    else:
                        raise ValueError("Invalid alpha-3 code input, cannot convert into corresponding alpha-2 code: {}.".format(alpha2_code[code]))

                #raise error if invalid alpha-2 code input
                if not (alpha2_code[code] in sorted(list(iso3166.countries_by_alpha2.keys()))):
                    raise ValueError("Invalid alpha-2 code input: {}.".format(alpha2_code[code]))

                #append list of subdivision parent codes to dict
                subdivision_parent_codes_[alpha2_code[code]] = set([self.all[alpha2_code[code]][x]["parentCode"] for x in self.all[alpha2_code[code]]])

                #remove any null values from list
                subdivision_parent_codes_[alpha2_code[code]] = [parent_code for parent_code in subdivision_parent_codes_[alpha2_code[code]] if parent_code is not None]

                #sort subdivision parent codes in json objects into  alphabetical order 
                subdivision_parent_codes_[alpha2_code[code]] = sorted(subdivision_parent_codes_[alpha2_code[code]])

            #if only one alpha-2 code input then return list of its subdivison parent codes else return dict object for all inputs
            if len(alpha2_code) == 1:
                return subdivision_parent_codes_[alpha2_code[0]]
            else:
                return subdivision_parent_codes_

    def __getitem__(self, alpha2_code):
        """
        Return all of a country's and subdivision data by making the class
        subscriptable. A list of country data can be returned if a comma
        seperated list of alpha-2 codes are input. The 2 letter alpha-2 code 
        is expected as input, although for redundancy, the 3 letter alpha-3 
        code can also be input which will be converted into its alpha-2 
        counterpart. If no value input then an error is raised.

        Parameters
        ==========
        :alpha2_code: str
            2 letter alpha-2 code for sought country/territory e.g (AD, EG, DE).
            Multiple country codes can be input in a comma seperated list. Can 
            also accept the 3 letter alpha-3 code e.g (AND, EGT, DEU), this will 
            be converted into its alpha-2 counterpart. If no value input then an
            error will be raised

        Returns
        =======
        :country[alpha2_code]: dict
            dict object of country/subdivision info for inputted alpha2_code.

        Usage
        =====
        import iso3166_2 as iso

        #get subdivision info for Ethiopia
        iso.country["ET"] 
        iso.country["ETH"] 
        iso.country["et"] 
 
        #get subdivision info for Gabon
        iso.country["GA"] 
        iso.country["GAB"] 
        iso.country["ga"] 

        #get subdivision info for Rwanda
        iso.country["RW"]
        iso.country["RWA"]
        iso.country["rw"]

        #get subdivision info for Haiti, Monaco and Namibia
        iso.country["HT, MC, NA"] 
        iso.country["HTI, MCO, NAM"] 
        iso.country["ht, mc, na"] 
        """
        #raise type error if input isn't a string
        if not (isinstance(alpha2_code, str)):
            raise TypeError('Input parameter {} is not of correct datatype string, got {}.'\
                .format(alpha2_code, type(alpha2_code)))       

        #stripping input of whitespace, uppercasing and seperating into comma seperated list
        alpha2_code = alpha2_code.replace(' ', '').upper().split(',')

        #object to store country data
        country = {}
        
        #iterate over all input alpha-2 codes, append their country and subdivision data to output object
        for code in range(0, len(alpha2_code)):

            #if 3 letter alpha-3 codes input then convert to corresponding alpha-2, else raise error
            if (len(alpha2_code[code]) == 3):
                temp_alpha2_code = convert_to_alpha2(alpha2_code[code])
                if not (temp_alpha2_code is None):
                    alpha2_code[code] = temp_alpha2_code
                else:
                    raise ValueError("Invalid alpha-3 code input, cannot convert into corresponding alpha-2 code: {}.".format(alpha2_code[code]))

            #raise error if invalid alpha-2 code input
            if not (alpha2_code[code] in sorted(list(iso3166.countries_by_alpha2.keys()))):
                raise ValueError("Invalid alpha-2 code input: {}.".format(code))        
            
            #create instance of Map class so dict can be accessed via dot notation 
            country[alpha2_code[code]] = Map(self.all[alpha2_code[code]]) 

            #iterate over nested dicts, convert into instances of Map class so they can be accessed via dot notation
            for key in country[alpha2_code[code]].keys():
                if (isinstance(country[alpha2_code[code]][key], dict)):
                    country[alpha2_code[code]][key] = Map(country[alpha2_code[code]][key])

        #convert country data object into Map class so it can be accessed via dot notation
        country = Map(country)

        #if only one alpha-2 code input then return list of its country data and attributes else return dict object for all inputs
        if len(alpha2_code) == 1:
            return country[alpha2_code[0]]
        else:
            return country

    def custom_subdivision(self, alpha2_code="", subdivision_code="", name="", local_name="", type="", 
            lat_lng=[], parent_code=None, flag_url=None, delete=0):
        """ 
        Add or delete a custom subdivision to an existing country on the main iso3166-2.json 
        object. The purpose of this functionality is similar to that of the user-assigned 
        code elements of the ISO 3166-1 standard. Custom subdivisions and subdivision codes 
        can be used for in-house/bespoke applications that are using the iso3166-2 software 
        but require additional custom subdivisions to be represented. If the input custom 
        subdivision code already exists then an error will be raised, otherwise it will be 
        appended to the object.

        If the added subdivision is required to be deleted from the object, then you can 
        call the same function with the alpha-2 and subdivision codes' parameters but also
        setting the 'delete' parameter to 1/True. 

        Parameters
        ==========
        :alpha2_code: str (default="")
            2 letter alpha-2 country code.
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
        import iso3166_2 as iso

        #adding custom Republic of Molossia state to United States 
        iso.country.custom_subdivision("US", "US-ML", name="Republic of Molossia", local_name="", type="State", lat_lng=[39.236, -119.588], parent_code=None, flag_url="https://upload.wikimedia.org/wikipedia/commons/c/c3/Flag_of_the_Republic_of_Molossia.svg")
        
        #adding custom Belfast province to Ireland
        iso.country.custom_subdivision("IE", "IE-BF", name="Belfast", local_name="Béal Feirste", type="province", lat_lng=[54.596, -5.931], parent_code=None, flag_url=None)

        #deleting above custom subdivisions
        iso.country.custom_subdivision("US", "US-ML", delete=1)
        iso.country.custom_subdivision("IE", "IE-BF", delete=1)
        """
        #open iso3166-2 json file and load it into class variable, loading in a JSON is different in Windows & Unix/Linux systems
        if (platform.system() != "Windows"):
            with open(os.path.join(self.iso3166_2_module_path, self.data_folder, self.iso3166_json_filename)) as iso3166_2_json:
                all_subdivision_data = json.load(iso3166_2_json)
        else:
            with open(os.path.join(self.iso3166_2_module_path, self.data_folder, self.iso3166_json_filename), encoding="utf-8") as fp:
                all_subdivision_data = json.loads(fp.read())

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
        
        #delete subdivision if delete parameter set, raise error if code not found
        if (delete):
            if (subdivision_code in list(all_subdivision_data[alpha2_code].keys())):
                del all_subdivision_data[alpha2_code][subdivision_code] 
        else:
            #adding new subdivision data to object from input parameters
            custom_subdivision_data = {"name": name, "localName": local_name, "type": type, "parentCode": parent_code, "latLng": lat_lng, "flagUrl": flag_url}       

            #reorder subdivision attributes
            all_subdivision_data[alpha2_code][subdivision_code] = {k: custom_subdivision_data[k] for k in ["name", "localName", "type", "parentCode", "flagUrl", "latLng"]}
                    
        #sort subdivision codes in json objects in natural alphabetical/numerical order using natsort library
        all_subdivision_data[alpha2_code] = dict(OrderedDict(natsort.natsorted(all_subdivision_data[alpha2_code].items())))

        #export the updated custom subdivision object
        with open(os.path.join(self.iso3166_2_module_path, self.data_folder, self.iso3166_json_filename), 'w', encoding='utf-8') as output_json:
            json.dump(all_subdivision_data, output_json, ensure_ascii=False, indent=4)  

    def search(self, name="", any=False):
        """ 
        Search for a subdivision and its corresponding data using it's subdivision name. The 'any' 
        input parameter determines if the function searches for an exact subdivision name or searches
        for 1 or more matching subdivisions, by default it will search for an exact match, set 'any' 
        to True if searching for approximate matching subdivisions. If a single subdivision is found 
        the dict of the subdivision data will be returned, if one or more similarly named subdivisions 
        are found then a list of dicts will be returned.

        Parameters
        ==========
        :name: str (default="")
            subdivision name to search for.
        :any: bool (default=False)
            if False then only return subdivision data if an exact match found otherwise return
            1 or more subdivisions that appoximately match input value.
        
        Returns
        =======
        :dict/list
            if one subdivision found then a dict of its data will be returned. If one more more
            subdivisions found then a list of dicts will be returned.
        """
        #raise error if name parameter isn't a string
        if not (isinstance(name, str)):
            raise TypeError("Input subdivision name should be of type str, got {}.".format(type(name)))

        #object to store the subdivision name and its corresponding alpha-2 code (name: alpha_2)
        all_subdivision_names = {}

        #list to store all subdivision names for all countries
        all_subdivision_names_list = []

        #iterate over all ISO 3166-2 subdivision data, appending each subdivision's name, country code and 
        #subdivision code to object that will be used to search through 
        for alpha_2 in self.all:
            for subd in self.all[alpha_2]:
                all_subdivision_names[self.all[alpha_2][subd]["name"].lower()] = {"alpha2": alpha_2, "code": subd}
                all_subdivision_names_list.append(self.all[alpha_2][subd]["name"].lower())

        #the 'any' default parameter value (False) will only return data if exact match found, otherwise
        #it will return 1 or more approximate subdivisions that match the input name, if 'any' = True
        if (any):
            #get closest subdivision name matches with a cutoff of 0.8
            subdivision_name_matches = get_close_matches(name.lower(), all_subdivision_names_list, cutoff=0.8)
        else:
            #get closest subdivision name matches with a cutoff of 1 - exact match
            subdivision_name_matches = get_close_matches(name.lower(), all_subdivision_names_list, cutoff=1)

        #return empty object if no matches found
        if (subdivision_name_matches == []):
            return {}
        #return subdivision data if one match found
        elif (len(subdivision_name_matches) == 1):
            #add country code and subdivision code to subdivision data object
            temp_subdivision = self.all[all_subdivision_names[subdivision_name_matches[0]]["alpha2"]][all_subdivision_names[subdivision_name_matches[0]]["code"]]
            temp_subdivision["alpha_2"] = all_subdivision_names[subdivision_name_matches[0]]["alpha2"]
            temp_subdivision["subdivision_code"] = all_subdivision_names[subdivision_name_matches[0]]["code"]
            return temp_subdivision
        #return list of subdivision data objects for all matches found
        else:
            subdivision_list = []
            for subd in range(0, len(subdivision_name_matches)):
                #add country code and subdivision code to subdivision data object
                temp_subdivision = self.all[all_subdivision_names[subdivision_name_matches[subd]]["alpha2"]][all_subdivision_names[subdivision_name_matches[subd]]["code"]]
                temp_subdivision["alpha_2"] = all_subdivision_names[subdivision_name_matches[subd]]["alpha2"]
                temp_subdivision["subdivision_code"] = all_subdivision_names[subdivision_name_matches[subd]]["code"]

                #append data object to list
                subdivision_list.append(temp_subdivision)

            return subdivision_list
        
    def __str__(self):
        return "Instance of ISO 3166-2 class."

    def __sizeof__(self):
        """ Return size of instance of ISO3166_2 class. """
        return self.__sizeof__()

def convert_to_alpha2(alpha3_code):
    """ 
    Auxillary function that converts an ISO 3166 country's 3 letter alpha-3 
    code into its 2 letter alpha-2 counterpart. 

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

#create instance of ISO3166_2 class
country = ISO3166_2()