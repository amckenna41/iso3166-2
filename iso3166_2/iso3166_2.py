import os
import sys
import json
import iso3166

class ISO3166_2():
    """
    This class is used to access all the ISO-3166 and ISO-3166-2 country data and attributes.
    There are two JSON's available in the package, iso3166-2-min.json and iso3166-2.json. The 
    former is a minified JSON of all country's ISO3166-2 subdivision info including subdivision
    name, code, parent code and type. The latter contains a verbose collection of all country 
    data pulled from the restcountries API as well as the country's subdivision data appened to 
    each. Both JSONs are generated using the getISO3166_2.py script in the main directory. All 
    of the keys and objects in the JSON are accessible via dot notation using the Map class.
    
    Parameters
    ----------
    :iso3166_json_filename : str (default=iso3166-2-min.json)
        filename of iso3166-2 JSON data to import from data folder. Can either be the
        iso3166-2-min or iso3166-2 JSON files. 

    Usage
    -----
    import iso3166_2 as iso

    #get all country data for Ireland, Colombia, Denmark and Finland
    iso.country['IE']
    iso.country['CO']
    iso.country['DK']
    iso.country['FI']

    #get capital city, languages, region and currency for Morocco
    iso.country['MA'].capital
    iso.country['MA'].languages
    iso.country['MA'].region
    iso.country['MA'].currencies

    #get all subdivision data for Lithuania
    iso.subdivisions['LT'].subdivisions

    #get subdivision names and subdivision types for GB-ANS, GB-BPL, GB-NTH and GB-WGN codes for the UK
    iso.subdivisions['GB'].subdivisions['GB-ANS].name
    """
    def __init__(self, iso3166_json_filename="iso3166-2-min.json"):

        self.iso3166_json_filename= iso3166_json_filename
        self.data_folder = "iso3166-2-data"

        #get module path
        self.iso3166_2_module_path = os.path.dirname(os.path.abspath(sys.modules[self.__module__].__file__))
        
        #raise error if iso3166-2 json doesnt exist in the data folder
        if not (os.path.isfile(os.path.join(self.iso3166_2_module_path, self.data_folder, self.iso3166_json_filename))):
            raise OSError("Issue finding iso3166-2.json in data dir {}.".format(self.data_folder))

        #open iso3166-2 json file and load it into class variable
        with open(os.path.join(self.iso3166_2_module_path, self.data_folder, self.iso3166_json_filename)) as iso3166_2_json:
            self.all_iso3166_2_data = json.load(iso3166_2_json)
        
        #get list of all countries by 2 letter alpha3 code
        self.alpha2 = sorted(list(iso3166.countries_by_alpha2.keys()))
        
        #get list of all countries by 3 letter alpha3 code
        self.alpha3 = sorted(list(iso3166.countries_by_alpha3.keys()))
    
    def __sizeof__(self):
        """ Return size of instance of ISO3166-2 class. """
        return self.__sizeof__()

    def __getitem__(self, alpha2_code):
        """
        Return all of a countrys data and subdivision by making the class
        subscriptable. The 2 letter alpha2 code is expected as input, 
        although the 3 letter alpha3 code can be input which will be 
        converted into its alpha2 counterpart.

        Parameters
        ----------
        : alpha2_code : str
            2 letter alpha2 code for sought country/territory e.g (AD, EG, DE).

        Returns
        -------
        : country[alpha2_code]: dict
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
        """
        #raise type error if input isn't a string
        if not (isinstance(alpha2_code, str)):
            raise TypeError('Input parameter {} is not of correct datatype string, got {}.' \
                .format(alpha2_code, type(alpha2_code)))       
        
        #stripping input of whitespace and uppercasing
        alpha2_code = alpha2_code.strip().upper()

        #object to store country data
        country = {}

        #validate 2 letter alpha2 code exists in ISO3166-1, raise error if not found            
        if (len(alpha2_code) == 2):
            if (alpha2_code in self.alpha2):      
                alpha2_code = iso3166.countries_by_alpha2[alpha2_code].alpha2
            else:
                raise ValueError("Alpha2 Code {} not found in list of ISO3166-1 codes.".format(alpha2_code))            
        
        #if 3 letter code input, check it exists in ISO3166-1, then convert into its 2 letter alpha2 code, raise error if not found            
        if (len(alpha2_code) == 3):
            if (alpha2_code in self.alpha3):      
                alpha2_code = iso3166.countries_by_alpha3[alpha2_code].alpha2
            else:
                raise ValueError("Alpha3 Code {} not found in list of ISO3166-1 codes.".format(alpha2_code))            

        #create instance of Map class so dict can be accessed via dot notation 
        country[alpha2_code] = Map(self.all_iso3166_2_data[alpha2_code]) 

        #iterate over nested dicts, convert into instances of Map class so they can be accessed via dot notation
        for key in country[alpha2_code].keys():
            if (isinstance(country[alpha2_code][key], dict)):
                country[alpha2_code][key] = Map(country[alpha2_code][key])

        #convert country data object into Map class so it can be accessed via dot notation
        country = Map(country)
                 
        return country[alpha2_code]

    def __str__(self):
        return "Instance of ISO3166-2 class."

class Map(dict):
    """
    Class that accepts a dict and allows you to use dot notation to access
    members of the dictionary. 

    Parameters
    ----------
    : dict
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

#create two instance of ISO3166_2 class using both JSONs
subdivisions = ISO3166_2(iso3166_json_filename="iso3166-2-min.json")
country = ISO3166_2(iso3166_json_filename="iso3166-2.json")