import iso3166
import requests
import getpass
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

class ISO3166_2_API_Tests(unittest.TestCase):
    """
    Test suite for testing ISO 3166-2 api created to accompany the iso3166-2 Python software package. 

    Test Cases
    ==========
    test_alpha2:
        testing correct objects are returned from /alpha2 API endpoint using a variety of inputs.
    test_name:
        testing correct objects are returned from /name API endpoint using a variety of inputs.
    test_all:
        testing correct objects are returned from /name API endpoint, which returns all the available 
        ISO 3166-2 data.    
    """
    def setUp(self):
        """ Initialise test variables, import json. """
        #initalise User-agent header for requests library 
        self.__version__ = "1.1.0"
        self.user_agent_header = {'User-Agent': 'iso3166-2/{} ({}; {})'.format(self.__version__,
                                            'https://github.com/amckenna41/iso3166-2', getpass.getuser())}

        #url endpoints for API
        self.api_base_url = "https://iso3166-2-api.vercel.app/api/"
        self.api_base_url = "https://iso3166-2-api-amckenna41.vercel.app/api/"
        self.alpha2_base_url = self.api_base_url + "alpha2/"
        self.name_base_url = self.api_base_url + "name/"
        self.all_base_url = self.api_base_url + "all"

        #list of output columns for main iso3166-2 json
        self.correct_output_cols = [
            "altSpellings", "area", "borders", "capital", "capitalInfo", "car", "cca2", "cca3", "ccn3", "cioc", "coatOfArms",
            "continents", "currencies", "demonyms", "fifa", "flag", "flags", "gini", "idd", "independent", "landlocked",
            "languages", "latlng", "maps", "name", "population", "postalCode", "region", "startOfWeek", "status",
            "subdivisions", "subregion", "timezones", "tld", "translations", "unMember"
        ]

        #list of keys that should be in subdivisions key of output object
        self.correct_subdivision_keys = ["flag_url", "latlng", "name", "parent_code", "type"]

    # @unittest.skip("Skipping to not overload API endpoint on test suite run.")
    def test_alpha2(self):
        """ Testing alpha-2 endpoint, return all ISO 3166 data from input alpha-2 code/codes. """
        test_alpha2_au = "AU" #Australia
        test_alpha2_cy = "CY" #Cyprus
        test_alpha2_lu = "LU" #Luxembourg
        test_alpha2_pa_rw = "PA, RW" #Panama, Rwanda
        test_alpha2_mac_mys = "MAC, MYS" #Macau, Malaysia
        test_alpha2_error_1 = "ABCDE"
        test_alpha2_error_2 = "12345"
#1.)
        #for each alpha-2 code, test API returns correct object, test using cca2 attribute
        for alpha2 in sorted(list(iso3166.countries_by_alpha2.keys())):
            test_request_alpha2 = requests.get(self.alpha2_base_url + alpha2, headers=self.user_agent_header).json()
            self.assertEqual(test_request_alpha2[alpha2]["cca2"], alpha2, 
                    "Input alpha-2 code {} and one in output object do not match: {}.".format(alpha2, test_request_alpha2[alpha2]["cca2"]))
#2.)
        test_request_au = requests.get(self.alpha2_base_url + test_alpha2_au, headers=self.user_agent_header).json() #Australia

        self.assertIsInstance(test_request_au, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_au)))
        self.assertEqual(len(test_request_au), 1, "Expected output object of API to be of length 1, got {}.".format(len(test_request_au)))
        self.assertEqual(list(test_request_au.keys()), ["AU"], "Expected output object of API to contain only the AU key, got {}.".format(list(test_request_au.keys())))

        self.assertEqual(test_request_au["AU"]["area"], 7692024, "Expected area to be 7692024, got {}.".format(test_request_au["AU"]["area"]))        
        self.assertEqual(test_request_au["AU"]["name"]["common"], "Australia", "Expected country name to be Australis, got {}.".format(test_request_au["AU"]["name"]["common"]))        
        self.assertEqual(test_request_au["AU"]["capital"][0], "Canberra", "")
        self.assertEqual(test_request_au["AU"]["cca2"], "AU", "")
        self.assertEqual(test_request_au["AU"]["cca3"], "AUS", "")
        self.assertEqual(test_request_au["AU"]["currencies"]["AUD"]['name'], "Australian dollar", "")        
        self.assertEqual(list(test_request_au["AU"]["languages"].keys())[0], "eng", "")        
        self.assertEqual(test_request_au["AU"]["latlng"], [-27.0, 133.0], "")        
        self.assertEqual(test_request_au["AU"]["population"], 25687041, "")        
        self.assertEqual(test_request_au["AU"]["region"], "Oceania", "")
        self.assertEqual(list(test_request_au["AU"]["subdivisions"].keys()), 
            ["AU-ACT", "AU-NSW", "AU-NT", "AU-QLD", "AU-SA", "AU-TAS", "AU-VIC", "AU-WA"], "")     
        for subd in test_request_au["AU"]["subdivisions"]:
            for key in list(test_request_au["AU"]["subdivisions"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Key {} not found in list of correct keys:\n{}.".format(key, self.correct_subdivision_keys))
        for col in list(test_request_au["AU"].keys()):
            self.assertIn(col, self.correct_output_cols, "Column {} not found in list of correct columns:\n{}.".format(col, self.correct_output_cols))
#3.)
        test_request_cy = requests.get(self.alpha2_base_url + test_alpha2_cy, headers=self.user_agent_header).json() #Cyprus

        self.assertIsInstance(test_request_cy, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_cy)))
        self.assertEqual(len(test_request_cy), 1, "Expected output object of API to be of length 1, got {}.".format(len(test_request_cy)))
        self.assertEqual(list(test_request_cy.keys()), ["CY"], "Expected output object of API to contain only the CY key, got {}.".format(list(test_request_cy.keys())))

        self.assertEqual(test_request_cy["CY"]["area"], 9251, "Expected area to be 9251, got {}.".format(test_request_cy["CY"]["area"]))              
        self.assertEqual(test_request_cy["CY"]["name"]["common"], "Cyprus", "")       
        self.assertEqual(test_request_cy["CY"]["capital"][0], "Nicosia", "")
        self.assertEqual(test_request_cy["CY"]["cca2"], "CY", "")
        self.assertEqual(test_request_cy["CY"]["cca3"], "CYP", "")
        self.assertEqual(test_request_cy["CY"]["currencies"]["EUR"]['name'], "Euro", "")          
        self.assertEqual(list(test_request_cy["CY"]["languages"].keys()), ["ell", "tur"], "")          
        self.assertEqual(test_request_cy["CY"]["latlng"], [35, 33], "")        
        self.assertEqual(test_request_cy["CY"]["population"], 1207361, "")          
        self.assertEqual(test_request_cy["CY"]["region"], "Europe", "")
        self.assertEqual(list(test_request_cy["CY"]["subdivisions"].keys()), 
            ["CY-01", "CY-02", "CY-03", "CY-04", "CY-05", "CY-06"], "")     
        for subd in test_request_cy["CY"]["subdivisions"]:
            for key in list(test_request_cy["CY"]["subdivisions"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Key {} not found in list of correct keys:\n{}.".format(key, self.correct_subdivision_keys))
        for col in list(test_request_cy["CY"].keys()):
            self.assertIn(col, self.correct_output_cols, "Column {} not found in list of correct columns:\n{}.".format(col, self.correct_output_cols))
#4.)
        test_request_lu = requests.get(self.alpha2_base_url + test_alpha2_lu, headers=self.user_agent_header).json() #Luxembourg

        self.assertIsInstance(test_request_lu, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_lu)))
        self.assertEqual(len(test_request_lu), 1, "Expected output object of API to be of length 1, got {}.".format(len(test_request_lu)))
        self.assertEqual(list(test_request_lu.keys()), ["LU"], "Expected output object of API to contain only the LU key, got {}.".format(list(test_request_lu.keys())))

        self.assertEqual(test_request_lu["LU"]["area"], 2586, "Expected area to be 2586, got {}.".format(test_request_lu["LU"]["area"]))             
        self.assertEqual(test_request_lu["LU"]["name"]["common"], "Luxembourg", "")        
        self.assertEqual(test_request_lu["LU"]["capital"][0], "Luxembourg", "")
        self.assertEqual(test_request_lu["LU"]["cca2"], "LU", "")
        self.assertEqual(test_request_lu["LU"]["cca3"], "LUX", "")
        self.assertEqual(test_request_lu["LU"]["currencies"]["EUR"]['name'], "Euro", "")        
        self.assertEqual(list(test_request_lu["LU"]["languages"].keys()), ["deu", "fra", "ltz"], "")        
        self.assertEqual(test_request_lu["LU"]["latlng"], [49.75, 6.167], "")        
        self.assertEqual(test_request_lu["LU"]["population"], 632275, "")        
        self.assertEqual(test_request_lu["LU"]["region"], "Europe", "")
        self.assertEqual(list(test_request_lu["LU"]["subdivisions"].keys()), 
            ["LU-CA", "LU-CL", "LU-DI", "LU-EC", "LU-ES", "LU-GR", "LU-LU", "LU-ME", "LU-RD", "LU-RM", "LU-VD", "LU-WI"], "")     
        for subd in test_request_lu["LU"]["subdivisions"]:
            for key in list(test_request_lu["LU"]["subdivisions"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Key {} not found in list of correct keys:\n{}.".format(key, self.correct_subdivision_keys))    
        for col in list(test_request_lu["LU"].keys()):
            self.assertIn(col, self.correct_output_cols, "Column {} not found in list of correct columns:\n{}.".format(col, self.correct_output_cols))
#5.)
        test_request_pa_rw = requests.get(self.alpha2_base_url + test_alpha2_pa_rw, headers=self.user_agent_header).json() #Panama and Rwanda

        self.assertIsInstance(test_request_pa_rw, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_pa_rw)))
        self.assertEqual(len(test_request_pa_rw), 2, "Expected output object of API to be of length 2, got {}.".format(len(test_request_pa_rw)))
        self.assertEqual(list(test_request_pa_rw.keys()), ["PA", "RW"], "Expected output object of API to contain only the PA and RW keys, got {}.".format(list(test_request_pa_rw.keys())))

        self.assertEqual(test_request_pa_rw["PA"]["area"], 75417, "Expected area to be 75417, got {}.".format(test_request_pa_rw["PA"]["area"]))        
        self.assertEqual(test_request_pa_rw["PA"]["name"]["common"], "Panama", "")        
        self.assertEqual(test_request_pa_rw["PA"]["capital"][0], "Panama City", "")
        self.assertEqual(test_request_pa_rw["PA"]["cca2"], "PA", "")
        self.assertEqual(test_request_pa_rw["PA"]["cca3"], "PAN", "")
        self.assertEqual(test_request_pa_rw["PA"]["currencies"]["PAB"]['name'], "Panamanian balboa", "")        
        self.assertEqual(list(test_request_pa_rw["PA"]["languages"].keys()), ["spa"], "")        
        self.assertEqual(test_request_pa_rw["PA"]["latlng"], [9, -80], "")        
        self.assertEqual(test_request_pa_rw["PA"]["population"], 4314768, "")        
        self.assertEqual(test_request_pa_rw["PA"]["region"], "Americas", "")
        self.assertEqual(list(test_request_pa_rw["PA"]["subdivisions"].keys()), 
            ["PA-1", "PA-10", "PA-2", "PA-3", "PA-4", "PA-5", "PA-6", "PA-7", "PA-8", "PA-9", "PA-EM", "PA-KY", "PA-NB"], "")     
        for subd in test_request_pa_rw["PA"]["subdivisions"]:
            for key in list(test_request_pa_rw["PA"]["subdivisions"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Key {} not found in list of correct keys:\n{}.".format(key, self.correct_subdivision_keys))    
        for col in list(test_request_pa_rw["PA"].keys()):
            self.assertIn(col, self.correct_output_cols, "Column {} not found in list of correct columns:\n{}.".format(col, self.correct_output_cols))

        self.assertEqual(test_request_pa_rw["RW"]["area"], 26338, "Expected area to be 26338, got {}.".format(test_request_pa_rw["RW"]["area"]))        
        self.assertEqual(test_request_pa_rw["RW"]["name"]["common"], "Rwanda", "")        
        self.assertEqual(test_request_pa_rw["RW"]["capital"][0], "Kigali", "")
        self.assertEqual(test_request_pa_rw["RW"]["cca2"], "RW", "")
        self.assertEqual(test_request_pa_rw["RW"]["cca3"], "RWA", "")
        self.assertEqual(test_request_pa_rw["RW"]["currencies"]["RWF"]['name'], "Rwandan franc", "")        
        self.assertEqual(list(test_request_pa_rw["RW"]["languages"].keys()), ["eng", "fra", "kin"], "")        
        self.assertEqual(test_request_pa_rw["RW"]["latlng"], [-2, 30], "")        
        self.assertEqual(test_request_pa_rw["RW"]["population"], 12952209, "")        
        self.assertEqual(test_request_pa_rw["RW"]["region"], "Africa", "")
        self.assertEqual(list(test_request_pa_rw["RW"]["subdivisions"].keys()), 
            ["RW-01", "RW-02", "RW-03", "RW-04", "RW-05"], "")     
        for subd in test_request_pa_rw["RW"]["subdivisions"]:
            for key in list(test_request_pa_rw["RW"]["subdivisions"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Key {} not found in list of correct keys:\n{}.".format(key, self.correct_subdivision_keys))    
        for col in list(test_request_pa_rw["RW"].keys()):
            self.assertIn(col, self.correct_output_cols, "Column {} not found in list of correct columns:\n{}.".format(col, self.correct_output_cols))
#6.)
        test_request_mac_mys = requests.get(self.alpha2_base_url + test_alpha2_mac_mys, headers=self.user_agent_header).json() #Macau, Malaysia

        self.assertIsInstance(test_request_mac_mys, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_mac_mys)))
        self.assertEqual(len(test_request_mac_mys), 2, "Expected output object of API to be of length 2, got {}.".format(len(test_request_mac_mys)))
        self.assertEqual(list(test_request_mac_mys.keys()), ["MO", "MY"], "Expected output object of API to contain only the MO and MY keys, got {}.".format(list(test_request_mac_mys.keys())))

        self.assertEqual(test_request_mac_mys["MO"]["area"], 30, "Expected area to be 30, got {}.".format(test_request_mac_mys["MO"]["area"]))                
        self.assertEqual(test_request_mac_mys["MO"]["name"]["common"], "Macau", "")        
        self.assertEqual(test_request_mac_mys["MO"]["cca2"], "MO", "")
        self.assertEqual(test_request_mac_mys["MO"]["cca3"], "MAC", "")
        self.assertEqual(test_request_mac_mys["MO"]["currencies"]["MOP"]['name'], "Macanese pataca", "")        
        self.assertEqual(list(test_request_mac_mys["MO"]["languages"].keys()), ["por", "zho"], "")        
        self.assertEqual(test_request_mac_mys["MO"]["latlng"], [22.167, 113.55], "")        
        self.assertEqual(test_request_mac_mys["MO"]["population"], 649342, "")        
        self.assertEqual(test_request_mac_mys["MO"]["region"], "Asia", "")
        self.assertEqual(test_request_mac_mys["MO"]["subdivisions"], {}, "")
        for col in list(test_request_mac_mys["MO"].keys()):
            self.assertIn(col, self.correct_output_cols, "Column {} not found in list of correct columns:\n{}.".format(col, self.correct_output_cols))

        self.assertEqual(test_request_mac_mys["MY"]["area"], 330803, "Expected area to be 330803, got {}.".format(test_request_mac_mys["MY"]["area"]))                        
        self.assertEqual(test_request_mac_mys["MY"]["name"]["common"], "Malaysia", "")        
        self.assertEqual(test_request_mac_mys["MY"]["capital"][0], "Kuala Lumpur", "")
        self.assertEqual(test_request_mac_mys["MY"]["cca2"], "MY", "")
        self.assertEqual(test_request_mac_mys["MY"]["cca3"], "MYS", "")
        self.assertEqual(test_request_mac_mys["MY"]["currencies"]["MYR"]['name'], "Malaysian ringgit", "")        
        self.assertEqual(list(test_request_mac_mys["MY"]["languages"].keys()), ["eng", "msa"] , "")        
        self.assertEqual(test_request_mac_mys["MY"]["latlng"], [2.5, 112.5], "")        
        self.assertEqual(test_request_mac_mys["MY"]["population"], 32365998, "")        
        self.assertEqual(test_request_mac_mys["MY"]["region"], "Asia", "")
        self.assertEqual(list(test_request_mac_mys["MY"]["subdivisions"].keys()), 
                         ["MY-01", "MY-02", "MY-03", "MY-04", "MY-05", "MY-06", "MY-07", "MY-08", "MY-09", \
                          "MY-10", "MY-11", "MY-12", "MY-13", "MY-14", "MY-15", "MY-16"], "")
        for subd in test_request_mac_mys["MY"]["subdivisions"]:
            for key in list(test_request_mac_mys["MY"]["subdivisions"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Key {} not found in list of correct keys:\n{}.".format(key, self.correct_subdivision_keys))      
        for col in list(test_request_mac_mys["MY"].keys()):
            self.assertIn(col, self.correct_output_cols, "Column {} not found in list of correct columns:\n{}.".format(col, self.correct_output_cols))
#7.) 
        test_request_error1 = requests.get(self.alpha2_base_url + test_alpha2_error_1, headers=self.user_agent_header).json() #ABCDE

        self.assertIsInstance(test_request_error1, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_error1)))
        self.assertEqual(len(test_request_error1), 3, "Expected output object of API to be of length 3, got {}.".format(len(test_request_error1)))
        self.assertEqual(test_request_error1["message"], 'Invalid 2 letter alpha-2 code input: ' + test_alpha2_error_1 + ".", 
                "Error message does not match expected:\n{}".format(test_request_error1["message"]))
        self.assertEqual(test_request_error1["path"], self.alpha2_base_url + test_alpha2_error_1, 
                "Error path does not match expected:\n{}.".format(test_request_error1["path"]))
        self.assertEqual(test_request_error1["status"], 400, 
                "Error status does not match expected:\n{}.".format(test_request_error1["status"]))
#8.)
        test_request_error2 = requests.get(self.alpha2_base_url + test_alpha2_error_2, headers=self.user_agent_header).json() #12345

        self.assertIsInstance(test_request_error2, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_error2)))
        self.assertEqual(len(test_request_error2), 3, "Expected output object of API to be of length 3, got {}.".format(len(test_request_error2)))
        self.assertEqual(test_request_error2["message"], 'Invalid 2 letter alpha-2 code input: ' + test_alpha2_error_2 + ".", 
                "Error message does not match expected:\n{}".format(test_request_error2["message"]))
        self.assertEqual(test_request_error2["path"], self.alpha2_base_url + test_alpha2_error_2, 
                "Error path does not match expected:\n{}.".format(test_request_error2["path"]))
        self.assertEqual(test_request_error2["status"], 400, 
                "Error status does not match expected:\n{}.".format(test_request_error2["status"]))

    # @unittest.skip("Skipping to not overload API endpoint on test suite run.")
    def test_name(self):
        """ Testing name endpoint, return all ISO 3166 data from input alpha-2 name/names. """
        test_name_bj = "Benin"
        test_name_tj = "Tajikistan"
        test_name_sd = "Sudan"
        test_name_ml_ni = "Mali, Nicaragua"
        test_name_error1 = "ABCDEF"
        test_name_error2 = "12345"
        name_exceptions_converted = {"Brunei Darussalam": "Brunei", "Bolivia, Plurinational State of": "Bolivia", 
                                     "Bonaire, Sint Eustatius and Saba": "Caribbean Netherlands", "Congo, Democratic Republic of the": "DR Congo",
                                     "Congo": "Republic of the Congo", "Côte d'Ivoire": "Ivory Coast", "Cabo Verde": "Cape Verde", "Falkland Islands (Malvinas)": 
                                     "Falkland Islands", "Micronesia, Federated States of" : "Micronesia", "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                                     "South Georgia and the South Sandwich Islands": "South Georgia", "Iran, Islamic Republic of": "Iran",
                                     "Korea, Democratic People's Republic of": "North Korea", "Korea, Republic of": "South Korea",
                                     "Lao People's Democratic Republic": "Laos", "Moldova, Republic of": "Moldova", "Saint Martin (French part)": "Saint Martin",
                                     "Macao": "Macau", "Pitcairn": "Pitcairn Islands", "Palestine, State of": "Palestine", "Russian Federation": "Russia", "Sao Tome and Principe": "São Tomé and Príncipe",
                                     "Sint Maarten (Dutch part)": "Sint Maarten", "Syrian Arab Republic": "Syria", "French Southern Territories": "French Southern and Antarctic Lands",
                                     "Türkiye": "Turkey", "Taiwan, Province of China": "Taiwan", "Tanzania, United Republic of": "Tanzania", "United States of America": "United States",
                                     "Holy See": "Vatican City", "Venezuela, Bolivarian Republic of": "Venezuela", "Virgin Islands, British": "British Virgin Islands",
                                     "Virgin Islands, U.S.": "United States Virgin Islands", "Viet Nam": "Vietnam"}
#1.)    
        #for each country name, test API returns correct object, test using common.name attribute 
        for alpha2 in sorted(list(iso3166.countries_by_alpha2.keys())):
            country_name = iso3166.countries_by_alpha2[alpha2].name
            test_request_name = requests.get(self.name_base_url + country_name, headers=self.user_agent_header).json()
            #convert country name to its more common name
            if (country_name in list(name_exceptions_converted.keys())):
                country_name = name_exceptions_converted[country_name]
            self.assertEqual(test_request_name[alpha2]["name"]["common"], country_name, 
                    "Input country name {} and one in output object do not match: {}.".format(country_name, test_request_name[alpha2]["name"]["common"]))
#2.)
        test_request_bj = requests.get(self.name_base_url + test_name_bj, headers=self.user_agent_header).json() #Benin

        self.assertIsInstance(test_request_bj, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_bj)))
        self.assertEqual(len(test_request_bj), 1, "Expected output object of API to be of length 1, got {}.".format(len(test_request_bj)))
        self.assertEqual(list(test_request_bj.keys()), ["BJ"], "Expected output object of API to contain only the BJ key, got {}.".format(list(test_request_bj.keys())))

        self.assertEqual(test_request_bj["BJ"]["area"], 112622, "")        
        self.assertEqual(test_request_bj["BJ"]["name"]["common"], "Benin", "")        
        self.assertEqual(test_request_bj["BJ"]["capital"][0], "Porto-Novo", "")
        self.assertEqual(test_request_bj["BJ"]["cca2"], "BJ", "")
        self.assertEqual(test_request_bj["BJ"]["cca3"], "BEN", "")
        self.assertEqual(test_request_bj["BJ"]["currencies"]["XOF"]['name'], "West African CFA franc", "")        
        self.assertEqual(list(test_request_bj["BJ"]["languages"].keys())[0], "fra", "")        
        self.assertEqual(test_request_bj["BJ"]["latlng"], [9.5, 2.25], "")        
        self.assertEqual(test_request_bj["BJ"]["population"], 12123198, "")        
        self.assertEqual(test_request_bj["BJ"]["region"], "Africa", "")
        self.assertEqual(list(test_request_bj["BJ"]["subdivisions"].keys()), 
            ["BJ-AK", "BJ-AL", "BJ-AQ", "BJ-BO", "BJ-CO", "BJ-DO", "BJ-KO", "BJ-LI", "BJ-MO", "BJ-OU", "BJ-PL", "BJ-ZO"], "")     
        for subd in test_request_bj["BJ"]["subdivisions"]:
            for key in list(test_request_bj["BJ"]["subdivisions"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Key {} not found in list of correct keys:\n{}".format(key, self.correct_subdivision_keys)) 
        for col in list(test_request_bj["BJ"].keys()):
                self.assertIn(col, self.correct_output_cols, "")
#3.)
        test_request_tj = requests.get(self.name_base_url + test_name_tj, headers=self.user_agent_header).json() #Tajikistan

        self.assertIsInstance(test_request_tj, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_tj)))
        self.assertEqual(len(test_request_tj), 1, "Expected output object of API to be of length 1, got {}.".format(len(test_request_tj)))
        self.assertEqual(list(test_request_tj.keys()), ["TJ"], "Expected output object of API to contain only the TJ key, got {}.".format(list(test_request_tj.keys())))

        self.assertEqual(test_request_tj["TJ"]["area"], 143100, "")        
        self.assertEqual(test_request_tj["TJ"]["name"]["common"], "Tajikistan", "")        
        self.assertEqual(test_request_tj["TJ"]["capital"][0], "Dushanbe", "")
        self.assertEqual(test_request_tj["TJ"]["cca2"], "TJ", "")
        self.assertEqual(test_request_tj["TJ"]["cca3"], "TJK", "")
        self.assertEqual(test_request_tj["TJ"]["currencies"]["TJS"]['name'], "Tajikistani somoni", "")        
        self.assertEqual(list(test_request_tj["TJ"]["languages"].keys())[0], "rus", "")        
        self.assertEqual(test_request_tj["TJ"]["latlng"], [39, 71], "")        
        self.assertEqual(test_request_tj["TJ"]["population"], 9537642, "")        
        self.assertEqual(test_request_tj["TJ"]["region"], "Asia", "")
        self.assertEqual(list(test_request_tj["TJ"]["subdivisions"].keys()), 
            ["TJ-DU", "TJ-GB", "TJ-KT", "TJ-RA", "TJ-SU"], "")     
        for subd in test_request_tj["TJ"]["subdivisions"]:
            for key in list(test_request_tj["TJ"]["subdivisions"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Key {} not found in list of correct keys:\n{}".format(key, self.correct_subdivision_keys)) 
        for col in list(test_request_tj["TJ"].keys()):
                self.assertIn(col, self.correct_output_cols, "")
#4.)
        test_request_sd = requests.get(self.name_base_url + test_name_sd, headers=self.user_agent_header).json() #Sudan

        self.assertIsInstance(test_request_sd, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_sd)))
        self.assertEqual(len(test_request_sd), 1, "Expected output object of API to be of length 1, got {}.".format(len(test_request_sd)))
        self.assertEqual(list(test_request_sd.keys()), ["SD"], "Expected output object of API to contain only the SD key, got {}.".format(list(test_request_sd.keys())))

        self.assertEqual(test_request_sd["SD"]["area"], 1886068, "")        
        self.assertEqual(test_request_sd["SD"]["name"]["common"], "Sudan", "")        
        self.assertEqual(test_request_sd["SD"]["capital"][0], "Khartoum", "")
        self.assertEqual(test_request_sd["SD"]["cca2"], "SD", "")
        self.assertEqual(test_request_sd["SD"]["cca3"], "SDN", "")
        self.assertEqual(test_request_sd["SD"]["currencies"]["SDG"]['name'], "Sudanese pound", "")        
        self.assertEqual(list(test_request_sd["SD"]["languages"].keys())[0], "ara", "")        
        self.assertEqual(test_request_sd["SD"]["latlng"], [15, 30], "")        
        self.assertEqual(test_request_sd["SD"]["population"], 43849269, "")        
        self.assertEqual(test_request_sd["SD"]["region"], "Africa", "")
        self.assertEqual(list(test_request_sd["SD"]["subdivisions"].keys()), 
            ["SD-DC", "SD-DE", "SD-DN", "SD-DS", "SD-DW", "SD-GD", "SD-GK", "SD-GZ", "SD-KA", "SD-KH", \
             "SD-KN", "SD-KS", "SD-NB", "SD-NO", "SD-NR", "SD-NW", "SD-RS", "SD-SI"], "")     
        for subd in test_request_sd["SD"]["subdivisions"]:
            for key in list(test_request_sd["SD"]["subdivisions"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Key {} not found in list of correct keys:\n{}".format(key, self.correct_subdivision_keys)) 
        for col in list(test_request_tj["TJ"].keys()):
                self.assertIn(col, self.correct_output_cols, "")
#5.)
        test_request_ml_ni = requests.get(self.name_base_url + test_name_ml_ni, headers=self.user_agent_header).json() #Mali and Nicaragua

        self.assertIsInstance(test_request_ml_ni, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_ml_ni)))
        self.assertEqual(len(test_request_ml_ni), 2, "Expected output object of API to be of length 2, got {}.".format(len(test_request_ml_ni)))
        self.assertEqual(list(test_request_ml_ni.keys()), ["ML", "NI"], "Expected output object of API to contain only the ML and NI keys, got {}.".format(list(test_request_ml_ni.keys())))

        self.assertEqual(test_request_ml_ni["ML"]["area"], 1240192, "")        
        self.assertEqual(test_request_ml_ni["ML"]["name"]["common"], "Mali", "")        
        self.assertEqual(test_request_ml_ni["ML"]["capital"][0], "Bamako", "")
        self.assertEqual(test_request_ml_ni["ML"]["cca2"], "ML", "")
        self.assertEqual(test_request_ml_ni["ML"]["cca3"], "MLI", "")
        self.assertEqual(test_request_ml_ni["ML"]["currencies"]["XOF"]['name'], "West African CFA franc", "")        
        self.assertEqual(list(test_request_ml_ni["ML"]["languages"].keys())[0], "fra", "")        
        self.assertEqual(test_request_ml_ni["ML"]["latlng"], [17, -4], "")        
        self.assertEqual(test_request_ml_ni["ML"]["population"], 20250834, "")        
        self.assertEqual(test_request_ml_ni["ML"]["region"], "Africa", "")
        self.assertEqual(list(test_request_ml_ni["ML"]["subdivisions"].keys()), 
            ["ML-1", "ML-10", "ML-2", "ML-3", "ML-4", "ML-5", "ML-6", "ML-7", "ML-8", "ML-9", "ML-BKO"], "")     
        for subd in test_request_ml_ni["ML"]["subdivisions"]:
            for key in list(test_request_ml_ni["ML"]["subdivisions"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Key {} not found in list of correct keys:\n{}".format(key, self.correct_subdivision_keys)) 
        for col in list(test_request_ml_ni["ML"].keys()):
                self.assertIn(col, self.correct_output_cols, "")

        self.assertEqual(test_request_ml_ni["NI"]["area"], 130373, "")        
        self.assertEqual(test_request_ml_ni["NI"]["name"]["common"], "Nicaragua", "")        
        self.assertEqual(test_request_ml_ni["NI"]["capital"][0], "Managua", "")
        self.assertEqual(test_request_ml_ni["NI"]["cca2"], "NI", "")
        self.assertEqual(test_request_ml_ni["NI"]["cca3"], "NIC", "")
        self.assertEqual(test_request_ml_ni["NI"]["currencies"]["NIO"]['name'], "Nicaraguan córdoba", "")        
        self.assertEqual(list(test_request_ml_ni["NI"]["languages"].keys())[0], "spa", "")        
        self.assertEqual(test_request_ml_ni["NI"]["latlng"], [13, -85], "")        
        self.assertEqual(test_request_ml_ni["NI"]["population"], 6624554, "")        
        self.assertEqual(test_request_ml_ni["NI"]["region"], "Americas", "")
        self.assertEqual(list(test_request_ml_ni["NI"]["subdivisions"].keys()), 
            ["NI-AN", "NI-AS", "NI-BO", "NI-CA", "NI-CI", "NI-CO", "NI-ES", "NI-GR", "NI-JI", "NI-LE", "NI-MD", "NI-MN", "NI-MS", "NI-MT", "NI-NS", "NI-RI", "NI-SJ"], "")     
        for subd in test_request_ml_ni["NI"]["subdivisions"]:
            for key in list(test_request_ml_ni["NI"]["subdivisions"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Key {} not found in list of correct keys:\n{}".format(key, self.correct_subdivision_keys)) 
        for col in list(test_request_ml_ni["NI"].keys()):
                self.assertIn(col, self.correct_output_cols, "")
#6.)
        test_request_error = requests.get(self.name_base_url + test_name_error1, headers=self.user_agent_header).json() #ABCDEF

        self.assertIsInstance(test_request_error, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_error)))
        self.assertEqual(len(test_request_error), 3, "Expected output object of API to be of length 3, got {}.".format(len(test_request_error)))
        self.assertEqual(test_request_error["message"], 'Country name ' + test_name_error1.title() + " not found in the ISO 3166.", 
                "Error message does not match expected:\n{}".format(test_request_error["message"]))
        self.assertEqual(test_request_error["path"], self.name_base_url + test_name_error1, 
                "Error path does not match expected:\n{}".format(test_request_error["path"]))
        self.assertEqual(test_request_error["status"], 400, 
                "Error status does not match expected:\n{}".format(test_request_error["status"]))
#7.)
        test_request_error = requests.get(self.name_base_url + test_name_error2, headers=self.user_agent_header).json() #12345

        self.assertIsInstance(test_request_error, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_error)))
        self.assertEqual(len(test_request_error), 3, "Expected output object of API to be of length 3, got {}.".format(len(test_request_error)))
        self.assertEqual(test_request_error["message"], 'Country name ' + test_name_error2.title() + " not found in the ISO 3166.", 
                "Error message does not match expected:\n{}".format(test_request_error["message"]))
        self.assertEqual(test_request_error["path"], self.name_base_url + test_name_error2, 
                "Error path does not match expected:\n{}".format(test_request_error["path"]))
        self.assertEqual(test_request_error["status"], 400, 
                "Error status does not match expected:\n{}".format(test_request_error["status"]))

    @unittest.skip("Skipping to not overload server as this test returns all data.")
    def test_all(self):
        """ Test 'all' endpoint which returns all data for all ISO 3166 countries. """
#1.)
        test_request_all = requests.get(self.all_base_url, headers=self.user_agent_header).json()

        self.assertIsInstance(test_request_all, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_all)))
        self.assertEqual(len(test_request_all), 250, "Expected output object of API to be of length 250, got {}.".format(len(test_request_all)))
        for alpha2 in list(test_request_all.keys()):
            self.assertIn(alpha2, iso3166.countries_by_alpha2, "Alpha-2 code {} not found in list of available codes.".format(alpha2))

if __name__ == '__main__':
    #run all unit tests
    unittest.main(verbosity=2)  