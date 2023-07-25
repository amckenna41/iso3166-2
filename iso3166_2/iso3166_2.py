import os
import sys
import json
import iso3166

class ISO3166_2():
    """
    This class is used to access all the ISO 3166 and ISO 3166-2 country data and attributes.
    There are two JSON's available in the package, iso3166-2-min.json and iso3166-2.json. The 
    former is a minified JSON of all country's ISO3166-2 subdivision info including subdivision
    name, type, code, parent code, lat/longitude and URL to its flag (if applicable). The latter 
    contains a verbose collection of all country data pulled from the restcountries API as well 
    as the country's subdivision data mentioned appened to each. Both JSONs are generated using 
    the getISO3166_2.py script in the main directory. All of the keys and objects in the JSON 
    are accessible via dot notation via the Map class. The plethora of attributes available
    in this class are described in the ATTRIBUTES.md file on the main repo dir 
    (https://github.com/amckenna41/iso3166-2/blob/main/ATTRIBUTES.md).

    Currently, this package supports data from 250 countries/territories, according to the 
    ISO 3166-1.
    
    Parameters
    ----------
    :iso3166_json_filename : str (default=iso3166-2-min.json)
        filename of iso3166-2 JSON data to import from data folder. Can either be the
        iso3166-2-min or iso3166-2 JSON files. 

    Usage
    -----
    import iso3166_2 as iso

    #get ALL country data (including subdivision data) for Ireland, Colombia, Denmark and Finland
    iso.country['IE']
    iso.country['CO']
    iso.country['DK']
    iso.country['FI']

    #get capital city, languages, region and currencies for Morocco
    iso.country['MA'].capital
    iso.country['MA'].languages
    iso.country['MA'].region
    iso.country['MA'].currencies

    #get ALL subdivision data for Lithuania, Namibia, Paraguay and Turkmenistan
    iso.subdivisions['LT'].subdivisions
    iso.subdivisions['NA'].subdivisions
    iso.subdivisions['PY'].subdivisions
    iso.subdivisions['TM'].subdivisions

    #get subdivision names, types, parent codes, flag urls and lat/longitudes 
    #   for GB-ANS, GB-BPL, GB-NTH, GB-WGN and GB-ZET subdivision codes for the UK
    iso.subdivisions['GB'].subdivisions['GB-ANS'].name
    iso.subdivisions['GB'].subdivisions['GB-BPL'].type
    iso.subdivisions['GB'].subdivisions['GB-NTH'].parent_code
    iso.subdivisions['GB'].subdivisions['GB-WGN'].flag_url
    iso.subdivisions['GB'].subdivisions['GB-ZET'].latlng
    """
    def __init__(self, iso3166_json_filename="iso3166-2-min.json"):

        self.iso3166_json_filename= iso3166_json_filename
        self.data_folder = "iso3166-2-data"
        self.using_country_data = False

        #get module path
        self.iso3166_2_module_path = os.path.dirname(os.path.abspath(sys.modules[self.__module__].__file__))
        
        #raise error if iso3166-2 json doesn't exist in the data folder
        if not (os.path.isfile(os.path.join(self.iso3166_2_module_path, self.data_folder, self.iso3166_json_filename))):
            raise OSError("Issue finding iso3166-2.json in data dir {}.".format(self.data_folder))

        #open iso3166-2 json file and load it into class variable
        with open(os.path.join(self.iso3166_2_module_path, self.data_folder, self.iso3166_json_filename)) as iso3166_2_json:
            self.all_iso3166_2_data = json.load(iso3166_2_json)
        
        #set bool variables indicating which json is being used
        if (self.iso3166_json_filename == "iso3166-2.json"):
            self.using_country_data = True

        #get list of all countries by 2 letter alpha-2 code
        self.alpha2 = sorted(list(iso3166.countries_by_alpha2.keys()))
        
        #get list of all countries by 3 letter alpha-3 code
        self.alpha3 = sorted(list(iso3166.countries_by_alpha3.keys()))

    def subdivision_codes(self, alpha2_code=""):
        """
        Return a list or dict of all ISO 3166-2 subdivision codes for one or more
        countries specified by their 2 letter alpha-2 code. If a single country 
        input then return list of subdivison codes, if multiple passed in return a dict
        of all country's subdivision codes. The function can also accept the 3 letter
        alpha-3 code for a country which is converted into its 2 letter alpha-2 
        counterpart. If no value passed into parameter then return dict of all 
        subdivision codes for all countries. If invalid country code input then raise 
        error.

        Parameters
        ----------
        :alpha2_code: str (default="")
            2 letter ISO 3166-1 alpha-2 code for country. The 3 letter alpha-3 country
            code can also be accepted.
        
        Returns
        -------
        :list / dict
            list of a country's ISO 3166-2 subdivision codes. Or dict of all country's
            subdivision names if no value passed into parameter.
        """
        subdivision_codes_ = {}

        #if no value passed into parameter, return all subdivision codes for all countries
        if (alpha2_code == ""):
            #get current JSON being used in class (the 2 JSONs have different nested dicts)
            if (self.using_country_data):
                #iterate over all country ISO 3166-2 data, append to subdivision codes dict
                for key, _ in self.all_iso3166_2_data.items():
                    subdivision_codes_[key] = list(self.all_iso3166_2_data[key]["subdivisions"])
            else:
                #iterate over all country ISO 3166-2 data, append to subdivision codes dict
                for key, _ in self.all_iso3166_2_data.items():
                    subdivision_codes_[key] = list(self.all_iso3166_2_data[key])
            return subdivision_codes_
        else:
            #sepetate list of alpha-2 codes into iterable list
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

                #append list of subdivision codes to dict, get current JSON being used in class, the 2 JSONs have different nested dicts
                if (self.using_country_data):
                    subdivision_codes_[alpha2_code[code]] = list(self.all_iso3166_2_data[alpha2_code[code]]["subdivisions"])
                else:
                    subdivision_codes_[alpha2_code[code]] = list(self.all_iso3166_2_data[alpha2_code[code]])
            
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
        input country's subdivision names. The function can also accept the 3 letter alpha-3 
        code for a country which is converted into its 2 letter alpha-2 counterpart. If no value
        passed into parameter then return dict of all subdivision names for all countries. If 
        invalid country code input then raise error.

        Parameters
        ----------
        :alpha2_code: str (default="")
            one or more 2 letter ISO 3166-1 alpha-2 codes for input countries.
        
        Returns
        -------
        :list / dict
            list or dict of input country's subdivision names, if no value passed into 
            parameter then all country subdivision name data is returned.
        """
        subdivision_names_ = {}

        #if no value passed into parameter, return all subdivision names for all countries
        if (alpha2_code == ""):
            #get current JSON being used in class (the 2 JSONs have different nested dicts)
            if (self.using_country_data):
                #iterate over all country ISO 3166-2 data, append to subdivision names dict
                for key, _ in self.all_iso3166_2_data.items():
                    subdivision_names_[key] = [self.all_iso3166_2_data[key]["subdivisions"][country]["name"] for country in self.all_iso3166_2_data[key]["subdivisions"]]
            else:
                #iterate over all country ISO 3166-2 data, append to subdivision names dict
                for key, _ in self.all_iso3166_2_data.items():
                    subdivision_names_[key] = [self.all_iso3166_2_data[key][country]["name"] for country in self.all_iso3166_2_data[key]]
            return subdivision_names_
        else:
            #sepetate list of alpha-2 codes into iterable list
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

                #append list of subdivision names to dict, get current JSON being used in class (the 2 JSONs have different nested dicts)
                if (self.using_country_data):
                    subdivision_names_[alpha2_code[code]] = [self.all_iso3166_2_data[alpha2_code[code]]["subdivisions"][x]["name"] for x in self.all_iso3166_2_data[alpha2_code[code]]["subdivisions"]]
                else:
                    subdivision_names_[alpha2_code[code]] = [self.all_iso3166_2_data[alpha2_code[code]][x]["name"] for x in self.all_iso3166_2_data[alpha2_code[code]]]
            
            #if only one alpha-2 code input then return list of its subdivison names else return dict object for all inputs
            if len(alpha2_code) == 1:
                return subdivision_names_[alpha2_code[0]]
            else:
                return subdivision_names_
        
    def __getitem__(self, alpha2_code):
        """
        Return all of a country's data and subdivision by making the class
        subscriptable. A list of country data can be returned if a comma
        seperated list of alpha-2 codes are input. The 2 letter alpha-2 code 
        is expected as input, although, for redundancy, the 3 letter alpha-3 
        code can be input which will be converted into its alpha-2 counterpart.
        If no value input then an error is raised.

        Parameters
        ----------
        :alpha2_code : str
            2 letter alpha-2 code for sought country/territory e.g (AD, EG, DE).
            Multiple country coded can be input in a comma seperated list. Can 
            also accept 3 letter alpha-3 code e.g (AND, EGT, DEU), this will 
            be converted into its alpha-2 counterpart.

        Returns
        -------
        :country[alpha2_code]: dict
            dict object of country/subdivision info for inputted alpha2_code.

        Usage
        -----
        import iso3166_2 as iso

        #get country & subdivision info for Ethiopia
        iso.subdivisions["ET"] 
        iso.subdivisions["ETH"] 
        iso.subdivisions["et"] 
 
        #get country & subdivision info for Gabon
        iso.subdivisions["GA"] 
        iso.subdivisions["GAB"] 
        iso.subdivisions["ga"] 

        #get country & subdivision info for Rwanda
        iso.country["RW"]
        iso.country["RWA"]
        iso.country["rw"]

        #get country & subdivision info for Haiti, Monaco and Namibia
        iso.subdivisions["HT, MC, NA"] 
        iso.subdivisions["HTI, MCO, NAM"] 
        iso.subdivisions["ht, mc, na"] 
        """
        #raise type error if input isn't a string
        if not (isinstance(alpha2_code, str)):
            raise TypeError('Input parameter {} is not of correct datatype string, got {}.' \
                .format(alpha2_code, type(alpha2_code)))       

        #stripping input of whitespace, uppercasing and seperating using a comma
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
            country[alpha2_code[code]] = Map(self.all_iso3166_2_data[alpha2_code[code]]) 

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
    ----------
    :alpha3_code: str
        3 letter ISO 3166-1 country code.
    
    Returns
    -------
    :iso3166.countries_by_alpha3[alpha3_code].alpha2: str
        2 letter ISO 3166 country code. 
    """
    #return None if 3 letter alpha-3 code not found
    if not (alpha3_code in list(iso3166.countries_by_alpha3.keys())):
        return None
    else:
        #use iso3166 package to find corresponding alpha-2 code from its alpha-3
        return iso3166.countries_by_alpha3[alpha3_code].alpha2
    
class Map(dict):
    """
    Class that accepts a dict and allows you to use dot notation to access
    members of the dictionary. 

    Parameters
    ----------
    :dict
        input dictionary to convert into instance of map class so the keys/vals
        can be accessed via dot notation.

    Usage
    -----
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
    ----------
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

#create two instance of ISO3166_2 class for both JSONs
subdivisions = ISO3166_2(iso3166_json_filename="iso3166-2-min.json")
country = ISO3166_2(iso3166_json_filename="iso3166-2.json")