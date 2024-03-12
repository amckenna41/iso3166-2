import iso3166
from iso3166_2 import *
import requests
import getpass
import os
from importlib.metadata import metadata
from bs4 import BeautifulSoup
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

class ISO3166_2_API_Tests(unittest.TestCase):
    """
    Test suite for testing ISO 3166-2 api created to accompany the iso3166-2 Python software package. 

    Test Cases
    ==========
    test_homepage_endpoint:
        testing main endpoint that returns the homepage and API documentation. 
    test_alpha_endpoint:
        testing correct data and attributes are returned from the /alpha API endpoint using a variety of alpha-2, 
        alpha-3 or numeric code inputs.
    test_subdivision_endpoint:
        testing correct data and attributes are returned from the /subdivision API endpoint using a variety of 
        subdivision code inputs.
    test_subdivision_name_endpoint:
        testing correct data and attributes are returned from the /name API endpoint using a variety of subdivision
        name inputs.
    test_country_name_endpoint:
        testing correct data and attributes are returned from the /country_name API endpoint using a variety of 
        country name inputs.
    test_all_endpoint:
        testing correct data and attributes are returned from the /all API endpoint, which returns all the available 
        ISO 3166-2 data.   
    """
    def setUp(self):
        """ Initialise test variables, import json. """
        #initalise User-agent header for requests library 
        self.__version__ = metadata('iso3166-2')['version']
        self.user_agent_header = {'User-Agent': 'iso3166-2/{} ({}; {})'.format(self.__version__,
                                            'https://github.com/amckenna41/iso3166-2', getpass.getuser())}

        #url endpoints for API
        # self.api_base_url = "https://iso3166-2-api.vercel.app/api/"
        self.api_base_url = "https://iso3166-2-api-amckenna41.vercel.app/api/" 
        self.alpha_base_url = self.api_base_url + "alpha/"
        self.subdivision_base_url = self.api_base_url + "subdivision/"
        self.subdivision_name_base_url = self.api_base_url + "name/"
        self.country_name_base_url = self.api_base_url + "country_name/"
        self.all_base_url = self.api_base_url + "all"

        #list of keys that should be in subdivisions key of output object
        self.correct_subdivision_keys = ["name", "localName", "type", "parentCode", "latLng", "flagUrl"]

        #base url for subdivision flag icons
        self.flag_base_url = "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/"

        #create instance of ISO 3166-2 class
        self.iso3166_2_data = ISO3166_2()
        
    def test_homepage_endpoint(self):
        """ Testing contents of main /api endpoint that returns the homepage and API documentation. """
        test_request_main = requests.get(self.api_base_url, headers=self.user_agent_header, timeout=(3.05, 27))
        soup = BeautifulSoup(test_request_main.content, 'html.parser')
#1.)    
        # version = soup.find(id='version').text.split(': ')[1] #need to get this using selenium as version is dynamically retrieved in frontend
        last_updated = soup.find(id='last-updated').text.split(': ')[1]
        author = soup.find(id='author').text.split(': ')[1]

        # self.assertEqual(version, "1.5.3", "Expected API version to be 1.5.3, got {}.".format(version)) 
        self.assertEqual(last_updated, "March 2024", "Expected last updated data to be March 2024, got {}.".format(last_updated))
        self.assertEqual(author, "AJ", "Expected author to be AJ, got {}.".format(author))
#2.)
        section_list_menu = soup.find(id='section-list-menu').find_all('li')
        correct_section_menu = ["About", "Attributes", "Endpoints", "All", "Country alpha code", "Country name", "Subdivision code", "Subdivision name", "Credits", "Contributing"]
        for li in section_list_menu:
            self.assertIn(li.text.strip(), correct_section_menu, "Expected list element {} to be in list.".format(li))

    def test_alpha_endpoint(self):
        """ Testing /alpha endpoint, return all ISO 3166 subdivision data from input alpha-2, alpha-3 or numeric code/codes. """
        test_alpha2_au = "AU" #Australia
        test_alpha3_lux = "LUX" #Luxembourg
        test_alpha3_pa_rw = "PAN, RWA" #Panama, Rwanda
        test_numeric_740_752 = "740, 752" #Suriname, Sweden
        test_alpha2_alpha3_numeric_ir_kgz_446 = "IR, KGZ, 446" #Iran, Kyrgyzstan, Macao
        test_alpha_error_1 = "ABCDE"
        test_alpha_error_2 = "12345"
        test_alpha_error_3 = ""
#1.)
        test_request_au = requests.get(self.alpha_base_url + test_alpha2_au, headers=self.user_agent_header).json() #Australia

        self.assertIsInstance(test_request_au, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_au)))
        self.assertEqual(list(test_request_au.keys()), ["AU"], "Expected output object of API to contain only the AU key, got {}.".format(list(test_request_au.keys())))
        self.assertEqual(list(test_request_au["AU"].keys()), ["AU-ACT", "AU-NSW", "AU-NT", "AU-QLD", "AU-SA", "AU-TAS", "AU-VIC", "AU-WA"], "Expected list of subdivision codes doesn't match output.")   
        for subd in test_request_au["AU"]:
            self.assertIsNot(test_request_au["AU"][subd]["name"], None, 
                "Expected subdivision name to not be None, got {}.".format(test_request_au["AU"][subd]["name"]))
            self.assertEqual(test_request_au["AU"][subd]["name"], test_request_au["AU"][subd]["localName"],
                "Expected subdivision's name and local name to be the same.")
            if not (test_request_au["AU"][subd]["parentCode"] is None):
                self.assertIn(test_request_au["AU"][subd]["parentCode"], list(test_request_au["AU"][subd].keys()), 
                    "Parent code {} not found in list of subdivision codes.".format(test_request_au["AU"][subd]["parentCode"]))
            if not (test_request_au["AU"][subd]["flagUrl"] is None):
                self.assertEqual(os.path.splitext(test_request_au["AU"][subd]["flagUrl"])[0], self.flag_base_url + "AU/" + subd, 
                    "Expected flag url to be {}, got {}.".format(self.flag_base_url + "AU/" + subd, os.path.splitext(test_request_au["AU"][subd]["flagUrl"])[0])) 
                self.assertEqual(requests.get(test_request_au["AU"][subd]["flagUrl"], headers=self.user_agent_header).status_code, 200, 
                    "Flag URL invalid: {}.".format(test_request_au["AU"][subd]["flagUrl"]))
            for key in list(test_request_au["AU"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_subdivision_keys))

        #AU-NSW - New South Wales 
        self.assertEqual(test_request_au["AU"]["AU-NSW"]["name"], "New South Wales", 
            "Expected subdivsion name to be New South Wales, got {}.".format(test_request_au["AU"]["AU-NSW"]["name"]))  
        self.assertEqual(test_request_au["AU"]["AU-NSW"]["localName"], "New South Wales", 
            "Expected subdivsion local name to be New South Wales, got {}.".format(test_request_au["AU"]["AU-NSW"]["localName"]))  
        self.assertEqual(test_request_au["AU"]["AU-NSW"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_request_au["AU"]["AU-NSW"]["parentCode"]))
        self.assertEqual(test_request_au["AU"]["AU-NSW"]["type"], "State", 
            "Expected subdivision type to be State, got {}.".format(test_request_au["AU"]["AU-NSW"]["type"]))
        self.assertEqual(test_request_au["AU"]["AU-NSW"]["latLng"], [-31.253, 146.921],
            "Expected subdivision latLng to be [-31.253, 146.921], got {}.".format(test_request_au["AU"]["AU-NSW"]["latLng"]))
        self.assertEqual(test_request_au["AU"]["AU-NSW"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/AU/AU-NSW.svg",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/AU/AU-NSW.svg, got {}.".format(test_request_au["AU"]["AU-NSW"]["flagUrl"]))
        #AU-QLD - Queensland
        self.assertEqual(test_request_au["AU"]["AU-QLD"]["name"], "Queensland", 
            "Expected subdivsion name to be Queensland, got {}.".format(test_request_au["AU"]["AU-QLD"]["name"]))  
        self.assertEqual(test_request_au["AU"]["AU-QLD"]["localName"], "Queensland", 
            "Expected subdivsion local name to be Queensland, got {}.".format(test_request_au["AU"]["AU-QLD"]["localName"]))  
        self.assertEqual(test_request_au["AU"]["AU-QLD"]["parentCode"], None,
            "Expected subdivision parent code to be None got {}.".format(test_request_au["AU"]["AU-QLD"]["parentCode"]))
        self.assertEqual(test_request_au["AU"]["AU-QLD"]["type"], "State",
            "Expected subdivision type to be State, got {}.".format(test_request_au["AU"]["AU-QLD"]["type"]))
        self.assertEqual(test_request_au["AU"]["AU-QLD"]["latLng"], [-22.575, 144.085],
            "Expected subdivision latLng to be [-22.575, 144.085], got {}.".format(test_request_au["AU"]["AU-NSW"]["latLng"]))
        self.assertEqual(test_request_au["AU"]["AU-QLD"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/AU/AU-QLD.svg",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/AU/AU-QLD.svg, got {}.".format(test_request_au["AU"]["AU-QLD"]["flagUrl"]))
#2.) 
        test_request_lux = requests.get(self.alpha_base_url + test_alpha3_lux, headers=self.user_agent_header).json() #Luxembourg

        self.assertIsInstance(test_request_lux, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_lux)))
        self.assertEqual(list(test_request_lux.keys()), ["LU"], "Expected output object of API to contain only the LU key, got {}.".format(list(test_request_lux.keys())))
        self.assertEqual(list(test_request_lux["LU"].keys()), ["LU-CA", "LU-CL", "LU-DI", "LU-EC", "LU-ES", "LU-GR", "LU-LU", "LU-ME", "LU-RD", "LU-RM", "LU-VD", "LU-WI"], 
            "Expected list of subdivision codes doesn't match output.")        
        for subd in test_request_lux["LU"]:
            self.assertIsNot(test_request_lux["LU"][subd]["name"], None, 
                "Expected subdivision name to not be None, got {}.".format(test_request_lux["LU"][subd]["name"]))
            self.assertEqual(test_request_lux["LU"][subd]["name"], test_request_lux["LU"][subd]["localName"],
                "Expected subdivision's name and local name to be the same.")
            if not (test_request_lux["LU"][subd]["parentCode"] is None):
                self.assertIn(test_request_lux["LU"][subd]["parentCode"], list(test_request_lux["LU"][subd].keys()), 
                    "Parent code {} not found in list of subdivision codes.".format(test_request_lux["LU"][subd]["parentCode"]))
            if not (test_request_lux["LU"][subd]["flagUrl"] is None):
                self.assertEqual(os.path.splitext(test_request_lux["LU"][subd]["flagUrl"])[0], self.flag_base_url + "LU/" + subd, 
                    "Expected flag url to be {}, got {}.".format(self.flag_base_url + "LUX/" + subd, os.path.splitext(test_request_lux["LU"][subd]["flagUrl"])[0])) 
                self.assertEqual(requests.get(test_request_lux["LU"][subd]["flagUrl"], headers=self.user_agent_header).status_code, 200, 
                    "Flag URL invalid: {}.".format(test_request_lux["LU"][subd]["flagUrl"]))
            for key in list(test_request_lux["LU"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_subdivision_keys)) 

        #LU-CA - Capellen
        self.assertEqual(test_request_lux["LU"]["LU-CA"]["name"], "Capellen", 
            "Expected subdivsion name to be Capellen, got {}.".format(test_request_lux["LU"]["LU-CA"]["name"]))  
        self.assertEqual(test_request_lux["LU"]["LU-CA"]["localName"], "Capellen", 
            "Expected subdivsion local name to be Capellen, got {}.".format(test_request_lux["LU"]["LU-CA"]["localName"])) 
        self.assertEqual(test_request_lux["LU"]["LU-CA"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_request_lux["LU"]["LU-CA"]["parentCode"]))
        self.assertEqual(test_request_lux["LU"]["LU-CA"]["type"], "Canton", 
            "Expected subdivision type to be Canton, got {}.".format(test_request_lux["LU"]["LU-CA"]["type"]))
        self.assertEqual(test_request_lux["LU"]["LU-CA"]["latLng"], [49.646, 5.991],
            "Expected subdivision latLng to be [49.646, 5.991], got {}.".format(test_request_lux["LU"]["LU-CA"]["latLng"]))
        self.assertEqual(test_request_lux["LU"]["LU-CA"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/LU/LU-CA.svg",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/LU/LU-CA.svg, got {}.".format(test_request_lux["LU"]["LU-CA"]["flagUrl"]))
        #LU-LU - Luxembourg
        self.assertEqual(test_request_lux["LU"]["LU-LU"]["name"], "Luxembourg", 
            "Expected subdivsion name to be Luxembourg, got {}.".format(test_request_lux["LU"]["LU-LU"]["name"]))  
        self.assertEqual(test_request_lux["LU"]["LU-LU"]["localName"], "Luxembourg", 
            "Expected subdivsion local name to be Luxembourg, got {}.".format(test_request_lux["LU"]["LU-LU"]["localName"])) 
        self.assertEqual(test_request_lux["LU"]["LU-LU"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_request_lux["LU"]["LU-LU"]["parentCode"]))
        self.assertEqual(test_request_lux["LU"]["LU-LU"]["type"], "Canton", 
            "Expected subdivision type to be Canton, got {}.".format(test_request_lux["LU"]["LU-LU"]["type"]))
        self.assertEqual(test_request_lux["LU"]["LU-LU"]["latLng"], [49.815, 6.13],
            "Expected subdivision latLng to be [49.815, 6.13], got {}.".format(test_request_lux["LU"]["LU-LU"]["latLng"]))
        self.assertEqual(test_request_lux["LU"]["LU-LU"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/LU/LU-LU.png",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/LU/LU-LU.png, got {}.".format(test_request_lux["LU"]["LU-LU"]["flagUrl"]))
#3.)
        test_request_pa_rw = requests.get(self.alpha_base_url + test_alpha3_pa_rw, headers=self.user_agent_header).json() #Panama and Rwanda

        self.assertIsInstance(test_request_pa_rw, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_pa_rw)))
        self.assertEqual(list(test_request_pa_rw.keys()), ["PA", "RW"], "Expected output object of API to contain only the PA and RW keys, got {}.".format(list(test_request_pa_rw.keys())))
        self.assertEqual(list(test_request_pa_rw["PA"].keys()), ["PA-1", "PA-10", "PA-2", "PA-3", "PA-4", "PA-5", "PA-6", "PA-7", "PA-8", "PA-9", "PA-EM", "PA-KY", "PA-NB", "PA-NT"], 
            "Expected list of subdivision codes doesn't match output.")        
        self.assertEqual(list(test_request_pa_rw["RW"].keys()), ["RW-01", "RW-02", "RW-03", "RW-04", "RW-05"], 
            "Expected list of subdivision codes doesn't match output.")      
        for subd in test_request_pa_rw["PA"]:
            self.assertIsNot(test_request_pa_rw["PA"][subd]["name"], None, 
                "Expected subdivision name to not be None, got {}.".format(test_request_pa_rw["PA"][subd]["name"]))
            self.assertEqual(test_request_pa_rw["PA"][subd]["name"], test_request_pa_rw["PA"][subd]["localName"],
                "Expected subdivision's name and local name to be the same.")
            if not (test_request_pa_rw["PA"][subd]["parentCode"] is None):
                self.assertIn(test_request_pa_rw["PA"][subd]["parentCode"], list(test_request_pa_rw["PA"][subd].keys()), 
                    "Parent code {} not found in list of subdivision codes.".format(test_request_pa_rw["PA"][subd]["parentCode"]))
            if not (test_request_pa_rw["PA"][subd]["flagUrl"] is None):
                self.assertEqual(os.path.splitext(test_request_pa_rw["PA"][subd]["flagUrl"])[0], self.flag_base_url + "PA/" + subd, 
                    "Expected flag url to be {}, got {}.".format(self.flag_base_url + "PA/" + subd, os.path.splitext(test_request_pa_rw["PA"][subd]["flagUrl"])[0])) 
                self.assertEqual(requests.get(test_request_pa_rw["PA"][subd]["flagUrl"], headers=self.user_agent_header).status_code, 200, 
                    "Flag URL invalid: {}.".format(test_request_pa_rw["PA"][subd]["flagUrl"]))
            for key in list(test_request_pa_rw["PA"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_subdivision_keys)) 
        for subd in test_request_pa_rw["RW"]:
            self.assertIsNot(test_request_pa_rw["RW"][subd]["name"], None, 
                "Expected subdivision name to not be None, got {}.".format(test_request_pa_rw["RW"][subd]["name"]))
            self.assertEqual(test_request_pa_rw["RW"][subd]["name"], test_request_pa_rw["RW"][subd]["localName"],
                "Expected subdivision's name and local name to be the same.")
            if not (test_request_pa_rw["RW"][subd]["parentCode"] is None):
                self.assertIn(test_request_pa_rw["RW"][subd]["parentCode"], list(test_request_pa_rw["RW"][subd].keys()), 
                    "Parent code {} not found in list of subdivision codes.".format(test_request_pa_rw["RW"][subd]["parentCode"]))
            if not (test_request_pa_rw["RW"][subd]["flagUrl"] is None):
                self.assertEqual(os.path.splitext(test_request_pa_rw["RW"][subd]["flagUrl"])[0], self.flag_base_url + "RW/" + subd, 
                    "Expected flag url to be {}, got {}.".format(self.flag_base_url + "RW/" + subd, os.path.splitext(test_request_pa_rw["RW"][subd]["flagUrl"])[0])) 
                self.assertEqual(requests.get(test_request_pa_rw["RW"][subd]["flagUrl"], headers=self.user_agent_header).status_code, 200, 
                    "Flag URL invalid: {}.".format(test_request_pa_rw["RW"][subd]["flagUrl"]))
            for key in list(test_request_pa_rw["RW"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_subdivision_keys)) 

        #PA-4 - Chiriquí
        self.assertEqual(test_request_pa_rw["PA"]["PA-4"]["name"], "Chiriquí", 
            "Expected subdivsion name to be Chiriquí, got {}.".format(test_request_pa_rw["PA"]["PA-4"]["name"])) 
        self.assertEqual(test_request_pa_rw["PA"]["PA-4"]["localName"], "Chiriquí", 
            "Expected subdivsion local name to be Chiriquí, got {}.".format(test_request_pa_rw["PA"]["PA-4"]["localName"]))  
        self.assertEqual(test_request_pa_rw["PA"]["PA-4"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_request_pa_rw["PA"]["PA-4"]["parentCode"]))
        self.assertEqual(test_request_pa_rw["PA"]["PA-4"]["type"], "Province", 
            "Expected subdivision type to be Province, got {}.".format(test_request_pa_rw["PA"]["PA-4"]["type"]))
        self.assertEqual(test_request_pa_rw["PA"]["PA-4"]["latLng"], [8.387, -82.28],
            "Expected subdivision latLng to be [8.387, -82.28], got {}.".format(test_request_pa_rw["PA"]["PA-4"]["latLng"]))
        self.assertEqual(test_request_pa_rw["PA"]["PA-4"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/PA/PA-4.svg",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/PA/PA-4.svg, got {}.".format(test_request_pa_rw["PA"]["PA-4"]["flagUrl"]))
        #RW-03 - Northern 
        self.assertEqual(test_request_pa_rw["RW"]["RW-03"]["name"], "Northern", 
            "Expected subdivsion name to be Northern, got {}.".format(test_request_pa_rw["RW"]["RW-03"]["name"]))  
        self.assertEqual(test_request_pa_rw["RW"]["RW-03"]["localName"], "Northern", 
            "Expected subdivsion local name to be Northern, got {}.".format(test_request_pa_rw["RW"]["RW-03"]["localName"]))  
        self.assertEqual(test_request_pa_rw["RW"]["RW-03"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_request_pa_rw["RW"]["RW-03"]["parentCode"]))
        self.assertEqual(test_request_pa_rw["RW"]["RW-03"]["type"], "Province", 
            "Expected subdivision type to be Province, got {}.".format(test_request_pa_rw["RW"]["RW-03"]["type"]))
        self.assertEqual(test_request_pa_rw["RW"]["RW-03"]["latLng"], [-1.656, 29.882],
            "Expected subdivision latLng to be [-1.656, 29.882], got {}.".format(test_request_pa_rw["RW"]["RW-03"]["latLng"]))
        self.assertEqual(test_request_pa_rw["RW"]["RW-03"]["flagUrl"], None,
            "Expected subdivision flag url to be None, got {}.".format(test_request_pa_rw["RW"]["RW-03"]["flagUrl"]))
#4.)
        test_request_740_752  = requests.get(self.alpha_base_url + test_numeric_740_752, headers=self.user_agent_header).json() #740 - Suriname, 752 - Sweden

        self.assertIsInstance(test_request_740_752, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_740_752)))
        self.assertEqual(list(test_request_740_752.keys()), ["SE", "SR"], "Expected output object of API to contain SR and SE keys, got {}.".format(list(test_request_740_752.keys())))
        self.assertEqual(list(test_request_740_752["SE"].keys()), ['SE-AB', 'SE-AC', 'SE-BD', 'SE-C', 'SE-D', 'SE-E', 'SE-F', 'SE-G', 'SE-H', 'SE-I', 'SE-K', \
                                                                   'SE-M', 'SE-N', 'SE-O', 'SE-S', 'SE-T', 'SE-U', 'SE-W', 'SE-X', 'SE-Y', 'SE-Z'], 
            "Expected list of subdivision codes doesn't match output.")   
        self.assertEqual(list(test_request_740_752["SR"].keys()), ["SR-BR", "SR-CM", "SR-CR", "SR-MA", "SR-NI", "SR-PM", "SR-PR", "SR-SA", "SR-SI", "SR-WA"], 
            "Expected list of subdivision codes doesn't match output.")    
        for subd in test_request_740_752["SR"]:
            self.assertIsNot(test_request_740_752["SR"][subd]["name"], None, 
                "Expected subdivision name to not be None, got {}.".format(test_request_740_752["SR"][subd]["name"]))
            self.assertEqual(test_request_740_752["SR"][subd]["name"], test_request_740_752["SR"][subd]["localName"],
                "Expected subdivision's name and local name to be the same.")
            if not (test_request_740_752["SR"][subd]["parentCode"] is None):
                self.assertIn(test_request_740_752["SR"][subd]["parentCode"], list(test_request_740_752["SR"][subd].keys()), 
                    "Parent code {} not found in list of subdivision codes.".format(test_request_740_752["SR"][subd]["parentCode"]))
            if not (test_request_740_752["SR"][subd]["flagUrl"] is None):
                self.assertEqual(os.path.splitext(test_request_740_752["SR"][subd]["flagUrl"])[0], self.flag_base_url + "SR/" + subd, 
                    "Expected flag url to be {}, got {}.".format(self.flag_base_url + "SR/" + subd, os.path.splitext(test_request_740_752["SR"][subd]["flagUrl"])[0])) 
                self.assertEqual(requests.get(test_request_740_752["SR"][subd]["flagUrl"], headers=self.user_agent_header).status_code, 200, 
                    "Flag URL invalid: {}.".format(test_request_740_752["SR"][subd]["flagUrl"]))
            for key in list(test_request_740_752["SR"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_subdivision_keys)) 
        for subd in test_request_740_752["SE"]:
            self.assertIsNot(test_request_740_752["SE"][subd]["name"], None, 
                "Expected subdivision name to not be None, got {}.".format(test_request_740_752["SE"][subd]["name"]))
            self.assertEqual(test_request_740_752["SE"][subd]["name"], test_request_740_752["SE"][subd]["localName"],
                "Expected subdivision's name and local name to be the same.")
            if not (test_request_740_752["SE"][subd]["parentCode"] is None):
                self.assertIn(test_request_740_752["SE"][subd]["parentCode"], list(test_request_740_752["SE"][subd].keys()), 
                    "Parent code {} not found in list of subdivision codes.".format(test_request_740_752["SE"][subd]["parentCode"]))
            if not (test_request_740_752["SE"][subd]["flagUrl"] is None):
                self.assertEqual(os.path.splitext(test_request_740_752["SE"][subd]["flagUrl"])[0], self.flag_base_url + "SE/" + subd, 
                    "Expected flag url to be {}, got {}.".format(self.flag_base_url + "SE/" + subd, os.path.splitext(test_request_740_752["SE"][subd]["flagUrl"])[0])) 
                self.assertEqual(requests.get(test_request_740_752["SE"][subd]["flagUrl"], headers=self.user_agent_header).status_code, 200, 
                    "Flag URL invalid: {}.".format(test_request_740_752["SE"][subd]["flagUrl"]))
            for key in list(test_request_740_752["SE"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_subdivision_keys)) 

        #SR-SI - Sipaliwini
        self.assertEqual(test_request_740_752["SR"]["SR-SI"]["name"], "Sipaliwini", 
            "Expected subdivsion name to be Sipaliwini, got {}.".format(test_request_740_752["SR"]["SR-SI"]["name"])) 
        self.assertEqual(test_request_740_752["SR"]["SR-SI"]["localName"], "Sipaliwini", 
            "Expected subdivsion local name to be Sipaliwini, got {}.".format(test_request_740_752["SR"]["SR-SI"]["localName"]))  
        self.assertEqual(test_request_740_752["SR"]["SR-SI"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_request_740_752["SR"]["SR-SI"]["parentCode"]))
        self.assertEqual(test_request_740_752["SR"]["SR-SI"]["type"], "District", 
            "Expected subdivision type to be District, got {}.".format(test_request_740_752["SR"]["SR-SI"]["type"]))
        self.assertEqual(test_request_740_752["SR"]["SR-SI"]["latLng"], [2.033, -56.134],
            "Expected subdivision latLng to be [2.033, -56.134], got {}.".format(test_request_740_752["SR"]["SR-SI"]["latLng"]))
        self.assertEqual(test_request_740_752["SR"]["SR-SI"]["flagUrl"], None,
            "Expected subdivision flag url to be None, got {}.".format(test_request_740_752["SR"]["SR-SI"]["flagUrl"]))
        #SE-I - Gotlands
        self.assertEqual(test_request_740_752["SE"]["SE-I"]["name"], "Gotlands län [SE-09]", 
            "Expected subdivsion name to be Gotlands län [SE-09], got {}.".format(test_request_740_752["SE"]["SE-I"]["name"])) 
        self.assertEqual(test_request_740_752["SE"]["SE-I"]["localName"], "Gotlands län [SE-09]", 
            "Expected subdivsion local name to be Gotlands län [SE-09], got {}.".format(test_request_740_752["SE"]["SE-I"]["localName"]))  
        self.assertEqual(test_request_740_752["SE"]["SE-I"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_request_740_752["SE"]["SE-I"]["parentCode"]))
        self.assertEqual(test_request_740_752["SE"]["SE-I"]["type"], "County", 
            "Expected subdivision type to be County, got {}.".format(test_request_740_752["SE"]["SE-I"]["type"]))
        self.assertEqual(test_request_740_752["SE"]["SE-I"]["latLng"], [57.531, 18.69],
            "Expected subdivision latLng to be [57.531, 18.69], got {}.".format(test_request_740_752["SE"]["SE-I"]["latLng"]))
        self.assertEqual(test_request_740_752["SE"]["SE-I"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/SE/SE-I.svg",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/SE/SE-I.svg, got {}.".format(test_request_740_752["SE"]["SE-I"]["flagUrl"]))
#5.)
        test_request_ir_kgz_446  = requests.get(self.alpha_base_url + test_alpha2_alpha3_numeric_ir_kgz_446, headers=self.user_agent_header).json() #Iran, Kyrgyzstan, Macao

        self.assertIsInstance(test_request_ir_kgz_446, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_ir_kgz_446)))
        self.assertEqual(list(test_request_ir_kgz_446.keys()), ["IR", "KG", "MO"], "Expected output object of API to contain IT, KG and MO keys, got {}.".format(list(test_request_ir_kgz_446.keys())))
        self.assertEqual(list(test_request_ir_kgz_446["IR"].keys()), ['IR-00', 'IR-01', 'IR-02', 'IR-03', 'IR-04', 'IR-05', 'IR-06', 'IR-07', 'IR-08', 'IR-09', 'IR-10', 'IR-11', 'IR-12', 'IR-13', 'IR-14', \
                                                                      'IR-15', 'IR-16', 'IR-17', 'IR-18', 'IR-19', 'IR-20', 'IR-21', 'IR-22', 'IR-23', 'IR-24', 'IR-25', 'IR-26', 'IR-27', 'IR-28', 'IR-29', 'IR-30'], 
            "Expected list of subdivision codes doesn't match output.")    
        self.assertEqual(list(test_request_ir_kgz_446["KG"].keys()), ['KG-B', 'KG-C', 'KG-GB', 'KG-GO', 'KG-J', 'KG-N', 'KG-O', 'KG-T', 'KG-Y'], 
            "Expected list of subdivision codes doesn't match output.") 
        self.assertEqual(list(test_request_ir_kgz_446["MO"].keys()), [], "Expected no suddivision codes in output object.") 
        
        for subd in test_request_ir_kgz_446["IR"]:
            self.assertIsNot(test_request_ir_kgz_446["IR"][subd]["name"], None, 
                "Expected subdivision name to not be None, got {}.".format(test_request_ir_kgz_446["IR"][subd]["name"]))
            self.assertEqual(test_request_ir_kgz_446["IR"][subd]["name"], test_request_ir_kgz_446["IR"][subd]["localName"],
                "Expected subdivision's name and local name to be the same.")
            if not (test_request_ir_kgz_446["IR"][subd]["parentCode"] is None):
                self.assertIn(test_request_ir_kgz_446["IR"][subd]["parentCode"], list(test_request_ir_kgz_446["IR"][subd].keys()), 
                    "Parent code {} not found in list of subdivision codes.".format(test_request_ir_kgz_446["IR"][subd]["parentCode"]))
            if not (test_request_ir_kgz_446["IR"][subd]["flagUrl"] is None):
                self.assertEqual(os.path.splitext(test_request_ir_kgz_446["IR"][subd]["flagUrl"])[0], self.flag_base_url + "IR/" + subd, 
                    "Expected flag url to be {}, got {}.".format(self.flag_base_url + "IR/" + subd, os.path.splitext(test_request_ir_kgz_446["IR"][subd]["flagUrl"])[0])) 
                self.assertEqual(requests.get(test_request_ir_kgz_446["IR"][subd]["flagUrl"], headers=self.user_agent_header).status_code, 200, 
                    "Flag URL invalid: {}.".format(test_request_ir_kgz_446["IR"][subd]["flagUrl"]))
            for key in list(test_request_ir_kgz_446["IR"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_subdivision_keys)) 
        for subd in test_request_ir_kgz_446["KG"]:
            self.assertIsNot(test_request_ir_kgz_446["KG"][subd]["name"], None, 
                "Expected subdivision name to not be None, got {}.".format(test_request_ir_kgz_446["KG"][subd]["name"]))
            self.assertEqual(test_request_ir_kgz_446["KG"][subd]["name"], test_request_ir_kgz_446["KG"][subd]["localName"],
                "Expected subdivision's name and local name to be the same.")
            if not (test_request_ir_kgz_446["KG"][subd]["parentCode"] is None):
                self.assertIn(test_request_ir_kgz_446["KG"][subd]["parentCode"], list(test_request_ir_kgz_446["KG"][subd].keys()), 
                    "Parent code {} not found in list of subdivision codes.".format(test_request_ir_kgz_446["KG"][subd]["parentCode"]))
            if not (test_request_ir_kgz_446["KG"][subd]["flagUrl"] is None):
                self.assertEqual(os.path.splitext(test_request_ir_kgz_446["KG"][subd]["flagUrl"])[0], self.flag_base_url + "KG/" + subd, 
                    "Expected flag url to be {}, got {}.".format(self.flag_base_url + "KG/" + subd, os.path.splitext(test_request_ir_kgz_446["KG"][subd]["flagUrl"])[0])) 
                self.assertEqual(requests.get(test_request_ir_kgz_446["KG"][subd]["flagUrl"], headers=self.user_agent_header).status_code, 200, 
                    "Flag URL invalid: {}.".format(test_request_ir_kgz_446["KG"][subd]["flagUrl"]))
            for key in list(test_request_ir_kgz_446["KG"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_subdivision_keys)) 
#6.) 
        test_request_error1 = requests.get(self.alpha_base_url + test_alpha_error_1, headers=self.user_agent_header).json() #ABCDE

        self.assertIsInstance(test_request_error1, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_error1)))
        self.assertEqual(len(test_request_error1), 3, "Expected output object of API to be of length 3, got {}.".format(len(test_request_error1)))
        self.assertEqual(test_request_error1["message"], "Invalid ISO 3166-1 alpha country code input, cannot convert into corresponding alpha-2 code: {}.".format(test_alpha_error_1), 
                "Error message does not match expected:\n{}".format(test_request_error1["message"]))
        self.assertEqual(test_request_error1["path"], self.alpha_base_url + test_alpha_error_1, 
                "Error path does not match expected:\n{}.".format(test_request_error1["path"]))
        self.assertEqual(test_request_error1["status"], 400, 
                "Error status does not match expected:\n{}.".format(test_request_error1["status"]))
#7.)
        test_request_error2 = requests.get(self.alpha_base_url + test_alpha_error_2, headers=self.user_agent_header).json() #12345

        self.assertIsInstance(test_request_error2, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_error2)))
        self.assertEqual(len(test_request_error2), 3, "Expected output object of API to be of length 3, got {}.".format(len(test_request_error2)))
        self.assertEqual(test_request_error2["message"], "Invalid ISO 3166-1 alpha country code input, cannot convert into corresponding alpha-2 code: {}.".format(test_alpha_error_2), 
                "Error message does not match expected:\n{}".format(test_request_error2["message"]))
        self.assertEqual(test_request_error2["path"], self.alpha_base_url + test_alpha_error_2, 
                "Error path does not match expected:\n{}.".format(test_request_error2["path"]))
        self.assertEqual(test_request_error2["status"], 400, 
                "Error status does not match expected:\n{}.".format(test_request_error2["status"]))
#8.)
        test_request_error3 = requests.get(self.alpha_base_url + test_alpha_error_3, headers=self.user_agent_header).json() #""

        self.assertIsInstance(test_request_error3, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_error3)))
        self.assertEqual(len(test_request_error3), 3, "Expected output object of API to be of length 3, got {}.".format(len(test_request_error3)))
        self.assertEqual(test_request_error3["message"], "The alpha input parameter cannot be empty.", 
                "Error message does not match expected:\n{}".format(test_request_error3["message"]))
        self.assertEqual(test_request_error3["path"], self.alpha_base_url + test_alpha_error_3, 
                "Error path does not match expected:\n{}.".format(test_request_error3["path"]))
        self.assertEqual(test_request_error3["status"], 400, 
                "Error status does not match expected:\n{}.".format(test_request_error3["status"]))
        
    def test_subdivision_endpoint(self):
        """ Testing /subdivision endpoint, return all ISO 3166 subdivision data from input subdivision code/codes. """
        test_subd_jm_05 = "JM-05"
        test_subd_pa_03 = "PA-3"
        test_subd_ss_ew = "SS-EW"
        test_subd_tv_nkf_tj_du = "TV-NKF, TJ-DU"
        test_subd_gb_xyz = "GB-XYZ"
        test_subd_xx_yy = "XX-YY"
#1.)
        test_request_jm_05 = requests.get(self.subdivision_base_url + test_subd_jm_05, headers=self.user_agent_header).json() #JM-05
        self.assertIsInstance(test_request_jm_05, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_jm_05)))
        self.assertEqual(list(test_request_jm_05.keys()), ["JM-05"], "Expected output object of API to contain only the JM-05 key, got {}.".format(list(test_request_jm_05.keys())))

        #JM-05 - Saint Mary
        self.assertEqual(test_request_jm_05["JM-05"]["name"], "Saint Mary", 
            "Expected subdivsion name to be Saint Mary, got {}.".format(test_request_jm_05["JM-05"]["name"]))  
        self.assertEqual(test_request_jm_05["JM-05"]["localName"], "Saint Mary", 
            "Expected subdivsion local name to be Saint Mary, got {}.".format(test_request_jm_05["JM-05"]["localName"]))  
        self.assertEqual(test_request_jm_05["JM-05"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_request_jm_05["JM-05"]["parentCode"]))
        self.assertEqual(test_request_jm_05["JM-05"]["type"], "Parish", 
            "Expected subdivision type to be Parish, got {}.".format(test_request_jm_05["JM-05"]["type"]))
        self.assertEqual(test_request_jm_05["JM-05"]["latLng"], [18.309, -76.964],
            "Expected subdivision latLng to be [18.309, -76.964], got {}.".format(test_request_jm_05["JM-05"]["latLng"]))
        self.assertEqual(test_request_jm_05["JM-05"]["flagUrl"], None,
            "Expected subdivision flag url to be None, got {}.".format(test_request_jm_05["JM-05"]["flagUrl"]))
#2)
        test_request_pa_03 = requests.get(self.subdivision_base_url + test_subd_pa_03, headers=self.user_agent_header).json() #PA-3
        self.assertIsInstance(test_request_pa_03, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_pa_03)))
        self.assertEqual(list(test_request_pa_03.keys()), ["PA-3"], "Expected output object of API to contain only the PA-3 key, got {}.".format(list(test_request_pa_03.keys())))

        #PA-3 - Colón
        self.assertEqual(test_request_pa_03["PA-3"]["name"], "Colón", 
            "Expected subdivsion name to be Colón, got {}.".format(test_request_pa_03["PA-3"]["name"]))  
        self.assertEqual(test_request_pa_03["PA-3"]["localName"], "Colón", 
            "Expected subdivsion local name to be Colón, got {}.".format(test_request_pa_03["PA-3"]["localName"]))  
        self.assertEqual(test_request_pa_03["PA-3"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_request_pa_03["PA-3"]["parentCode"]))
        self.assertEqual(test_request_pa_03["PA-3"]["type"], "Province", 
            "Expected subdivision type to be Province, got {}.".format(test_request_pa_03["PA-3"]["type"]))
        self.assertEqual(test_request_pa_03["PA-3"]["latLng"], [9.359, -79.9],
            "Expected subdivision latLng to be [9.359, -79.9], got {}.".format(test_request_pa_03["PA-3"]["latLng"]))
        self.assertEqual(test_request_pa_03["PA-3"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/PA/PA-3.svg",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/PA/PA-3.svg, got {}.".format(test_request_pa_03["PA-3"]["flagUrl"]))
#3.)
        test_request_ss_ew = requests.get(self.subdivision_base_url + test_subd_ss_ew, headers=self.user_agent_header).json() #SS-EW
        self.assertIsInstance(test_request_ss_ew, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_ss_ew)))
        self.assertEqual(list(test_request_ss_ew.keys()), ["SS-EW"], "Expected output object of API to contain only the SS-EW key, got {}.".format(list(test_request_ss_ew.keys())))

        #SS-EW - Western Equatoria
        self.assertEqual(test_request_ss_ew["SS-EW"]["name"], "Western Equatoria", 
            "Expected subdivsion name to be Western Equatoria, got {}.".format(test_request_ss_ew["SS-EW"]["name"]))  
        self.assertEqual(test_request_ss_ew["SS-EW"]["localName"], "Western Equatoria", 
            "Expected subdivsion local name to be Western Equatoria, got {}.".format(test_request_ss_ew["SS-EW"]["localName"]))  
        self.assertEqual(test_request_ss_ew["SS-EW"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_request_ss_ew["SS-EW"]["parentCode"]))
        self.assertEqual(test_request_ss_ew["SS-EW"]["type"], "State", 
            "Expected subdivision type to be State, got {}.".format(test_request_ss_ew["SS-EW"]["type"]))
        self.assertEqual(test_request_ss_ew["SS-EW"]["latLng"], [5.347, 28.299],
            "Expected subdivision latLng to be [5.347, 28.299], got {}.".format(test_request_ss_ew["SS-EW"]["latLng"]))
        self.assertEqual(test_request_ss_ew["SS-EW"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/SS/SS-EW.png",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/SS/SS-EW.png, got {}.".format(test_request_ss_ew["SS-EW"]["flagUrl"]))
#4.)
        test_request_tv_nkf_tj_du = requests.get(self.subdivision_base_url + test_subd_tv_nkf_tj_du, headers=self.user_agent_header).json() #TV-NKF, TJ-DU
        self.assertIsInstance(test_request_tv_nkf_tj_du, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_tv_nkf_tj_du)))
        self.assertEqual(list(test_request_tv_nkf_tj_du.keys()), ["TJ-DU", "TV-NKF"], "Expected output object of API to contain only the TJ-DU and TV-NKF keys, got {}.".format(list(test_request_tv_nkf_tj_du.keys())))

        #TV-NKF - Western Equatoria
        self.assertEqual(test_request_tv_nkf_tj_du["TV-NKF"]["name"], "Nukufetau", 
            "Expected subdivsion name to be Nukufetau, got {}.".format(test_request_tv_nkf_tj_du["TV-NKF"]["name"]))  
        self.assertEqual(test_request_tv_nkf_tj_du["TV-NKF"]["localName"], "Nukufetau", 
            "Expected subdivsion local name to be Nukufetau, got {}.".format(test_request_tv_nkf_tj_du["TV-NKF"]["localName"]))  
        self.assertEqual(test_request_tv_nkf_tj_du["TV-NKF"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_request_tv_nkf_tj_du["TV-NKF"]["parentCode"]))
        self.assertEqual(test_request_tv_nkf_tj_du["TV-NKF"]["type"], "Island council", 
            "Expected subdivision type to be Island Council, got {}.".format(test_request_tv_nkf_tj_du["TV-NKF"]["type"]))
        self.assertEqual(test_request_tv_nkf_tj_du["TV-NKF"]["latLng"], [-8, 178.5],
            "Expected subdivision latLng to be [-8, 178.5], got {}.".format(test_request_tv_nkf_tj_du["TV-NKF"]["latLng"]))
        self.assertEqual(test_request_tv_nkf_tj_du["TV-NKF"]["flagUrl"], None,
            "Expected subdivision flag url to be None, got {}.".format(test_request_tv_nkf_tj_du["TV-NKF"]["flagUrl"]))
        #TJ-DU - Dushanbe
        self.assertEqual(test_request_tv_nkf_tj_du["TJ-DU"]["name"], "Dushanbe", 
            "Expected subdivsion name to be Dushanbe, got {}.".format(test_request_tv_nkf_tj_du["TJ-DU"]["name"]))  
        self.assertEqual(test_request_tv_nkf_tj_du["TJ-DU"]["localName"], "Dushanbe", 
            "Expected subdivsion local name to be Dushanbe, got {}.".format(test_request_tv_nkf_tj_du["TJ-DU"]["localName"]))  
        self.assertEqual(test_request_tv_nkf_tj_du["TJ-DU"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_request_tv_nkf_tj_du["TJ-DU"]["parentCode"]))
        self.assertEqual(test_request_tv_nkf_tj_du["TJ-DU"]["type"], "Capital territory", 
            "Expected subdivision type to be Capital territory, got {}.".format(test_request_tv_nkf_tj_du["TJ-DU"]["type"]))
        self.assertEqual(test_request_tv_nkf_tj_du["TJ-DU"]["latLng"], [38.56, 68.787],
            "Expected subdivision latLng to be [38.56, 68.787], got {}.".format(test_request_tv_nkf_tj_du["TJ-DU"]["latLng"]))
        self.assertEqual(test_request_tv_nkf_tj_du["TJ-DU"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/TJ/TJ-DU.png",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/TJ/TJ-DU.png, got {}.".format(test_request_tv_nkf_tj_du["TJ-DU"]["flagUrl"]))
#5.)       
        test_request_gb_xyz = requests.get(self.subdivision_base_url + test_subd_gb_xyz, headers=self.user_agent_header).json() #GB-XYZ

        self.assertIsInstance(test_request_gb_xyz, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_gb_xyz)))
        self.assertEqual(len(test_request_gb_xyz), 3, "Expected output object of API to be of length 3, got {}.".format(len(test_request_gb_xyz)))
        self.assertEqual(test_request_gb_xyz["message"], "Subdivision code {} not found in list of available subdivisions for GB.".format(test_subd_gb_xyz), 
                "Error message does not match expected:\n{}".format(test_request_gb_xyz["message"]))
        self.assertEqual(test_request_gb_xyz["path"], self.subdivision_base_url + test_subd_gb_xyz, 
                "Error path does not match expected:\n{}".format(test_request_gb_xyz["path"]))
        self.assertEqual(test_request_gb_xyz["status"], 400, 
                "Error status does not match expected:\n{}".format(test_request_gb_xyz["status"]))
#6.)
        test_request_xx_yy = requests.get(self.subdivision_base_url + test_subd_xx_yy, headers=self.user_agent_header).json() #XX-YY

        self.assertIsInstance(test_request_xx_yy, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_xx_yy)))
        self.assertEqual(len(test_request_xx_yy), 3, "Expected output object of API to be of length 3, got {}.".format(len(test_request_xx_yy)))
        self.assertEqual(test_request_xx_yy["message"], "Subdivision code {} not found in list of available subdivisions for XX.".format(test_subd_xx_yy), 
                "Error message does not match expected:\n{}".format(test_request_xx_yy["message"]))
        self.assertEqual(test_request_xx_yy["path"], self.subdivision_base_url + test_subd_xx_yy, 
                "Error path does not match expected:\n{}".format(test_request_xx_yy["path"]))
        self.assertEqual(test_request_xx_yy["status"], 400, 
                "Error status does not match expected:\n{}".format(test_request_xx_yy["status"]))

    def test_subdivision_name_endpoint(self):
        """ Testing /name endpoint, return all ISO 3166 subdivision data from input subdivision name/names. """
        test_subdivision_name_azua = "Azua" #DO-02
        test_subdivision_name_cakaudrove = "Cakaudrove" #FJ-03
        test_subdivision_name_gelderland_overijssel = "Gelderland, Overijssel" #NL-GE, NL-OV
        test_subdivision_name_ciudad = "Ciudad"
        test_subdivision_madrid_armaghcity = "Madrid, Comunidad de, Armagh City, Banbridge and Craigavon" #ES-MD, GB-ABC
        test_subdivision_name_error1 = "blahblahblah"
        test_subdivision_name_error2 = "1234"
        test_subdivision_name_error3 = ""
#1.)
        test_request_azua = requests.get(self.subdivision_name_base_url + test_subdivision_name_azua, headers=self.user_agent_header).json() #DO-02 - Azua

        self.assertIsInstance(test_request_azua, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_azua)))
        self.assertEqual(list(test_request_azua.keys()), ["DO-02"], "Expected output object of API to contain only the DO-02 key, got {}.".format(list(test_request_azua.keys())))

        #DO-02 - Azua
        self.assertEqual(test_request_azua["DO-02"]["name"], "Azua", 
            "Expected subdivsion name to be Azua, got {}.".format(test_request_azua["DO-02"]["name"]))  
        self.assertEqual(test_request_azua["DO-02"]["localName"], "Azua", 
            "Expected subdivsion local name to be Azua, got {}.".format(test_request_azua["DO-02"]["localName"]))  
        self.assertEqual(test_request_azua["DO-02"]["parentCode"], "DO-41", 
            "Expected subdivision parent code to be DO-41, got {}.".format(test_request_azua["DO-02"]["parentCode"]))
        self.assertEqual(test_request_azua["DO-02"]["type"], "Province", 
            "Expected subdivision type to be Province, got {}.".format(test_request_azua["DO-02"]["type"]))
        self.assertEqual(test_request_azua["DO-02"]["latLng"], [18.453, -70.735],
            "Expected subdivision latLng to be [18.453, -70.735], got {}.".format(test_request_azua["DO-02"]["latLng"]))
        self.assertEqual(test_request_azua["DO-02"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/DO/DO-02.png",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/DO/DO-02.png, got {}.".format(test_request_azua["DO-02"]["flagUrl"]))
#2.)
        test_request_cakaudrove = requests.get(self.subdivision_name_base_url + test_subdivision_name_cakaudrove, headers=self.user_agent_header).json() #FJ-03 - Cakaudrove

        self.assertIsInstance(test_request_cakaudrove, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_cakaudrove)))
        self.assertEqual(list(test_request_cakaudrove.keys()), ["FJ-03"], "Expected output object of API to contain only the FJ-03 key, got {}.".format(list(test_request_cakaudrove.keys())))

        #FJ-03 - Cakaudrove
        self.assertEqual(test_request_cakaudrove["FJ-03"]["name"], "Cakaudrove", 
            "Expected subdivsion name to be Cakaudrove, got {}.".format(test_request_cakaudrove["FJ-03"]["name"]))  
        self.assertEqual(test_request_cakaudrove["FJ-03"]["localName"], "Cakaudrove", 
            "Expected subdivsion local name to be Cakaudrove, got {}.".format(test_request_cakaudrove["FJ-03"]["localName"]))  
        self.assertEqual(test_request_cakaudrove["FJ-03"]["parentCode"], "FJ-N", 
            "Expected subdivision parent code to be FJ-N, got {}.".format(test_request_cakaudrove["FJ-03"]["parentCode"]))
        self.assertEqual(test_request_cakaudrove["FJ-03"]["type"], "Province", 
            "Expected subdivision type to be Province, got {}.".format(test_request_cakaudrove["FJ-03"]["type"]))
        self.assertEqual(test_request_cakaudrove["FJ-03"]["latLng"], [-16.581, 179.436],
            "Expected subdivision latLng to be [-16.581, 179.436], got {}.".format(test_request_cakaudrove["FJ-03"]["latLng"]))
        self.assertEqual(test_request_cakaudrove["FJ-03"]["flagUrl"], None,
            "Expected subdivision flag url to be None, got {}.".format(test_request_cakaudrove["FJ-03"]["flagUrl"]))
#3.)
        test_request_gelderland_overijssel = requests.get(self.subdivision_name_base_url + test_subdivision_name_gelderland_overijssel, headers=self.user_agent_header).json() #NL-GE - Gelderland, NL-OV - Overijssel

        self.assertIsInstance(test_request_gelderland_overijssel, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_gelderland_overijssel)))
        self.assertEqual(list(test_request_gelderland_overijssel.keys()), ["NL-GE", "NL-OV"], "Expected output object of API to contain only the NL-GE and NL-OV keys, got {}.".format(list(test_request_gelderland_overijssel.keys())))

        #NL-GE - Gelderland
        self.assertEqual(test_request_gelderland_overijssel["NL-GE"]["name"], "Gelderland", 
            "Expected subdivsion name to be Gelderland, got {}.".format(test_request_gelderland_overijssel["NL-GE"]["name"]))  
        self.assertEqual(test_request_gelderland_overijssel["NL-GE"]["localName"], "Gelderland", 
            "Expected subdivsion local name to be Gelderland, got {}.".format(test_request_gelderland_overijssel["NL-GE"]["localName"]))  
        self.assertEqual(test_request_gelderland_overijssel["NL-GE"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_request_gelderland_overijssel["NL-GE"]["parentCode"]))
        self.assertEqual(test_request_gelderland_overijssel["NL-GE"]["type"], "Province", 
            "Expected subdivision type to be Province, got {}.".format(test_request_gelderland_overijssel["NL-GE"]["type"]))
        self.assertEqual(test_request_gelderland_overijssel["NL-GE"]["latLng"], [52.045, 5.872],
            "Expected subdivision latLng to be [52.045, 5.872], got {}.".format(test_request_gelderland_overijssel["NL-GE"]["latLng"]))
        self.assertEqual(test_request_gelderland_overijssel["NL-GE"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/NL/NL-GE.svg",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/NL/NL-GE.svg, got {}.".format(test_request_gelderland_overijssel["NL-GE"]["flagUrl"]))
        #NL-OV - Overijssel
        self.assertEqual(test_request_gelderland_overijssel["NL-OV"]["name"], "Overijssel", 
            "Expected subdivsion name to be Overijssel, got {}.".format(test_request_gelderland_overijssel["NL-OV"]["name"]))  
        self.assertEqual(test_request_gelderland_overijssel["NL-OV"]["localName"], "Overijssel", 
            "Expected subdivsion local name to be Overijssel, got {}.".format(test_request_gelderland_overijssel["NL-OV"]["localName"]))  
        self.assertEqual(test_request_gelderland_overijssel["NL-OV"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_request_gelderland_overijssel["NL-OV"]["parentCode"]))
        self.assertEqual(test_request_gelderland_overijssel["NL-OV"]["type"], "Province", 
            "Expected subdivision type to be Province, got {}.".format(test_request_gelderland_overijssel["NL-OV"]["type"]))
        self.assertEqual(test_request_gelderland_overijssel["NL-OV"]["latLng"], [52.439, 6.502],
            "Expected subdivision latLng to be [52.439, 6.502], got {}.".format(test_request_gelderland_overijssel["NL-OV"]["latLng"]))
        self.assertEqual(test_request_gelderland_overijssel["NL-OV"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/NL/NL-OV.svg",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/NL/NL-OV.svg, got {}.".format(test_request_gelderland_overijssel["NL-OV"]["flagUrl"]))
#4.)
        test_request_ciudad = requests.get(self.subdivision_name_base_url + test_subdivision_name_ciudad, headers=self.user_agent_header, params={"likeness": "50"}).json() #Ciudad - likeness score of 50

        self.assertIsInstance(test_request_ciudad, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_ciudad)))
        self.assertEqual(list(test_request_ciudad.keys()), ["AO-CAB", "AZ-CUL", "ES-CR", "MX-CMX", "ZW-MI"], "Expected output object of API to contain only the AO-CAB, AZ-CUL, ES-CR, MX-CMX and ZW-MI keys, got {}.".format(list(test_request_ciudad.keys())))

        #ES-CR - Ciudad Real
        self.assertEqual(test_request_ciudad["ES-CR"]["name"], "Ciudad Real", 
            "Expected subdivsion name to be Ciudad Real, got {}.".format(test_request_ciudad["ES-CR"]["name"]))  
        self.assertEqual(test_request_ciudad["ES-CR"]["localName"], "Ciudad Real", 
            "Expected subdivsion local name to be Ciudad Real, got {}.".format(test_request_ciudad["ES-CR"]["localName"]))  
        self.assertEqual(test_request_ciudad["ES-CR"]["parentCode"], "ES-CM", 
            "Expected subdivision parent code to be ES-CM, got {}.".format(test_request_ciudad["ES-CR"]["parentCode"]))
        self.assertEqual(test_request_ciudad["ES-CR"]["type"], "Province", 
            "Expected subdivision type to be Province, got {}.".format(test_request_ciudad["ES-CR"]["type"]))
        self.assertEqual(test_request_ciudad["ES-CR"]["latLng"], [38.985, -3.927],
            "Expected subdivision latLng to be [38.985, -3.927], got {}.".format(test_request_ciudad["ES-CR"]["latLng"]))
        self.assertEqual(test_request_ciudad["ES-CR"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/ES/ES-CR.svg",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/ES/ES-CR.svg, got {}.".format(test_request_ciudad["ES-CR"]["flagUrl"]))
        #MX-CMX - Ciudad de Mexico
        self.assertEqual(test_request_ciudad["MX-CMX"]["name"], "Ciudad de México", 
            "Expected subdivsion name to be Ciudad de México, got {}.".format(test_request_ciudad["MX-CMX"]["name"]))  
        self.assertEqual(test_request_ciudad["MX-CMX"]["localName"], "Ciudad de México", 
            "Expected subdivsion local name to be Ciudad de México, got {}.".format(test_request_ciudad["MX-CMX"]["localName"]))  
        self.assertEqual(test_request_ciudad["MX-CMX"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_request_ciudad["MX-CMX"]["parentCode"]))
        self.assertEqual(test_request_ciudad["MX-CMX"]["type"], "Federal entity", 
            "Expected subdivision type to be Federal entity, got {}.".format(test_request_ciudad["MX-CMX"]["type"]))
        self.assertEqual(test_request_ciudad["MX-CMX"]["latLng"], [19.433, -99.133],
            "Expected subdivision latLng to be [19.433, -99.133], got {}.".format(test_request_ciudad["MX-CMX"]["latLng"]))
        self.assertEqual(test_request_ciudad["MX-CMX"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/MX/MX-CMX.svg",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/MX/MX-CMX.svg, got {}.".format(test_request_ciudad["MX-CMX"]["flagUrl"]))
#5.)
        test_request_madrid_armaghcity = requests.get(self.subdivision_name_base_url + test_subdivision_madrid_armaghcity, headers=self.user_agent_header).json() #ES-MD - Madrid, GB-ABC - Armagh City, Banbridge and Craigavon

        self.assertIsInstance(test_request_madrid_armaghcity, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_madrid_armaghcity)))
        self.assertEqual(list(test_request_madrid_armaghcity.keys()), ["ES-MD", "GB-ABC"], "Expected output object of API to contain only the ES-MD and GB-ABC keys, got {}.".format(list(test_request_madrid_armaghcity.keys())))

        #ES-MD - Madrid
        self.assertEqual(test_request_madrid_armaghcity["ES-MD"]["name"], "Madrid, Comunidad de", 
            "Expected subdivsion name to be Madrid, Comunidad de, got {}.".format(test_request_madrid_armaghcity["ES-MD"]["name"]))  
        self.assertEqual(test_request_madrid_armaghcity["ES-MD"]["localName"], "Madrid, Comunidad de", 
            "Expected subdivsion local name to be Madrid, Comunidad de, got {}.".format(test_request_madrid_armaghcity["ES-MD"]["localName"]))  
        self.assertEqual(test_request_madrid_armaghcity["ES-MD"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_request_madrid_armaghcity["ES-MD"]["parentCode"]))
        self.assertEqual(test_request_madrid_armaghcity["ES-MD"]["type"], "Autonomous community", 
            "Expected subdivision type to be Autonomous community, got {}.".format(test_request_madrid_armaghcity["ES-MD"]["type"]))
        self.assertEqual(test_request_madrid_armaghcity["ES-MD"]["latLng"], [40.417, -3.704],
            "Expected subdivision latLng to be [40.417, -3.704], got {}.".format(test_request_madrid_armaghcity["ES-MD"]["latLng"]))
        self.assertEqual(test_request_madrid_armaghcity["ES-MD"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/ES/ES-MD.svg",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/ES/ES-MD.svg, got {}.".format(test_request_madrid_armaghcity["ES-MD"]["flagUrl"]))
        #GB-ABC - Armagh City, Banbridge and Craigavon
        self.assertEqual(test_request_madrid_armaghcity["GB-ABC"]["name"], "Armagh City, Banbridge and Craigavon", 
            "Expected subdivsion name to be Armagh City, Banbridge and Craigavon, got {}.".format(test_request_madrid_armaghcity["GB-ABC"]["name"]))  
        self.assertEqual(test_request_madrid_armaghcity["GB-ABC"]["localName"], "Armagh City, Banbridge and Craigavon", 
            "Expected subdivsion local name to be Armagh City, Banbridge and Craigavon, got {}.".format(test_request_madrid_armaghcity["GB-ABC"]["localName"]))  
        self.assertEqual(test_request_madrid_armaghcity["GB-ABC"]["parentCode"], "GB-NIR", 
            "Expected subdivision parent code to be GB-NIR, got {}.".format(test_request_madrid_armaghcity["GB-ABC"]["parentCode"]))
        self.assertEqual(test_request_madrid_armaghcity["GB-ABC"]["type"], "District", 
            "Expected subdivision type to be District, got {}.".format(test_request_madrid_armaghcity["GB-ABC"]["type"]))
        self.assertEqual(test_request_madrid_armaghcity["GB-ABC"]["latLng"], [54.393, -6.456],
            "Expected subdivision latLng to be [54.393, -6.456], got {}.".format(test_request_madrid_armaghcity["GB-ABC"]["latLng"]))
        self.assertEqual(test_request_madrid_armaghcity["GB-ABC"]["flagUrl"], None,
            "Expected subdivision flag url to be None, got {}.".format(test_request_madrid_armaghcity["GB-ABC"]["flagUrl"]))
#6.)
        test_request_subdivision_error1 = requests.get(self.subdivision_name_base_url + test_subdivision_name_error1, headers=self.user_agent_header).json() #blahblahblah

        self.assertIsInstance(test_request_subdivision_error1, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_subdivision_error1)))
        self.assertEqual(len(test_request_subdivision_error1), 3, "Expected output object of API to be of length 3, got {}.".format(len(test_request_subdivision_error1)))
        self.assertEqual(test_request_subdivision_error1["message"], "No valid subdivision found for input name: {}. Try using the query string parameter '?likeness' and "
                         "reduce the likeness score to expand the search space, e.g '?likeness=0.3' will return subdivisions that have a 30% match to the input name.".format(test_subdivision_name_error1), 
                "Error message does not match expected:\n{}".format(test_request_subdivision_error1["message"]))
        self.assertEqual(test_request_subdivision_error1["path"], self.subdivision_name_base_url + test_subdivision_name_error1, 
                "Error path does not match expected:\n{}".format(test_request_subdivision_error1["path"]))
        self.assertEqual(test_request_subdivision_error1["status"], 400, 
                "Error status does not match expected:\n{}".format(test_request_subdivision_error1["status"]))
#6.)
        test_request_subdivision_error2 = requests.get(self.subdivision_name_base_url + test_subdivision_name_error2, headers=self.user_agent_header).json() #1234

        self.assertIsInstance(test_request_subdivision_error2, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_subdivision_error2)))
        self.assertEqual(len(test_request_subdivision_error2), 3, "Expected output object of API to be of length 3, got {}.".format(len(test_request_subdivision_error2)))
        self.assertEqual(test_request_subdivision_error2["message"],  "No valid subdivision found for input name: {}. Try using the query string parameter '?likeness' and "
                         "reduce the likeness score to expand the search space, e.g '?likeness=0.3' will return subdivisions that have a 30% match to the input name.".format(test_subdivision_name_error2), 
                "Error message does not match expected:\n{}".format(test_request_subdivision_error2["message"]))
        self.assertEqual(test_request_subdivision_error2["path"], self.subdivision_name_base_url + test_subdivision_name_error2, 
                "Error path does not match expected:\n{}".format(test_request_subdivision_error2["path"]))
        self.assertEqual(test_request_subdivision_error2["status"], 400, 
                "Error status does not match expected:\n{}".format(test_request_subdivision_error2["status"]))
#7.)
        test_request_subdivision_error3 = requests.get(self.subdivision_name_base_url + test_subdivision_name_error3, headers=self.user_agent_header).json() #""

        self.assertIsInstance(test_request_subdivision_error3, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_subdivision_error3)))
        self.assertEqual(len(test_request_subdivision_error3), 3, "Expected output object of API to be of length 3, got {}.".format(len(test_request_subdivision_error3)))
        self.assertEqual(test_request_subdivision_error3["message"], "The subdivision name input parameter cannot be empty.",
                "Error message does not match expected:\n{}".format(test_request_subdivision_error3["message"]))
        self.assertEqual(test_request_subdivision_error3["path"], self.subdivision_name_base_url + test_subdivision_name_error3, 
                "Error path does not match expected:\n{}".format(test_request_subdivision_error3["path"]))
        self.assertEqual(test_request_subdivision_error3["status"], 400, 
                "Error status does not match expected:\n{}".format(test_request_subdivision_error3["status"]))
        
    def test_name_endpoint(self):
        """ Testing /country_name endpoint, return all ISO 3166 subdivision data from input country name/names. """
        test_country_name_bj = "Benin"
        test_country_name_tj = "Tajikistan"
        test_country_name_sd = "Sudan"
        test_country_name_ml_ni = "Mali, Nicaragua"
        test_country_name_error1 = "ABCDEF"
        test_country_name_error2 = "12345"
#1.)
        test_request_bj = requests.get(self.country_name_base_url + test_country_name_bj, headers=self.user_agent_header).json() #Benin

        self.assertIsInstance(test_request_bj, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_bj)))
        self.assertEqual(list(test_request_bj.keys()), ["BJ"], "Expected output object of API to contain only the BJ key, got {}.".format(list(test_request_bj.keys())))
        self.assertEqual(list(test_request_bj["BJ"].keys()), ["BJ-AK", "BJ-AL", "BJ-AQ", "BJ-BO", "BJ-CO", "BJ-DO", "BJ-KO", "BJ-LI", "BJ-MO", "BJ-OU", "BJ-PL", "BJ-ZO"], "")   

        for subd in test_request_bj["BJ"]:
            self.assertIsNot(test_request_bj["BJ"][subd]["name"], None, 
                "Expected subdivision name to not be None, got {}.".format(test_request_bj["BJ"][subd]["name"]))
            self.assertEqual(test_request_bj["BJ"][subd]["name"], test_request_bj["BJ"][subd]["localName"],
                "Expected subdivision's name and local name to be the same.")
            if not (test_request_bj["BJ"][subd]["parentCode"] is None):
                self.assertIn(test_request_bj["BJ"][subd]["parentCode"], list(test_request_bj["BJ"][subd].keys()), 
                    "Parent code {} not found in list of subdivision codes.".format(test_request_bj["BJ"][subd]["parentCode"]))
            if not (test_request_bj["BJ"][subd]["flagUrl"] is None):
                self.assertEqual(os.path.splitext(test_request_bj["BJ"][subd]["flagUrl"])[0], self.flag_base_url + "BJ/" + subd, 
                    "Expected flag url to be {}, got {}.".format(self.flag_base_url + "BJ/" + subd, os.path.splitext(test_request_bj["BJ"][subd]["flagUrl"])[0])) 
                self.assertEqual(requests.get(test_request_bj["BJ"][subd]["flagUrl"], headers=self.user_agent_header).status_code, 200, 
                    "Flag URL invalid: {}.".format(test_request_bj["BJ"][subd]["flagUrl"]))
            for key in list(test_request_bj["BJ"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_subdivision_keys)) 
#2.)
        test_request_tj = requests.get(self.country_name_base_url + test_country_name_tj, headers=self.user_agent_header).json() #Tajikistan

        self.assertIsInstance(test_request_tj, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_tj)))
        self.assertEqual(list(test_request_tj.keys()), ["TJ"], "Expected output object of API to contain only the TJ key, got {}.".format(list(test_request_tj.keys())))
        self.assertEqual(list(test_request_tj["TJ"].keys()), ["TJ-DU", "TJ-GB", "TJ-KT", "TJ-RA", "TJ-SU"], "")     

        for subd in test_request_tj["TJ"]:
            self.assertIsNot(test_request_tj["TJ"][subd]["name"], None, 
                "Expected subdivision name to not be None, got {}.".format(test_request_tj["TJ"][subd]["name"]))
            self.assertEqual(test_request_tj["TJ"][subd]["name"], test_request_tj["TJ"][subd]["localName"],
                "Expected subdivision's name and local name to be the same.")
            if not (test_request_tj["TJ"][subd]["parentCode"] is None):
                self.assertIn(test_request_tj["TJ"][subd]["parentCode"], list(test_request_tj["TJ"][subd].keys()), 
                    "Parent code {} not found in list of subdivision codes.".format(test_request_tj["TJ"][subd]["parentCode"]))
            if not (test_request_tj["TJ"][subd]["flagUrl"] is None):
                self.assertEqual(os.path.splitext(test_request_tj["TJ"][subd]["flagUrl"])[0], self.flag_base_url + "TJ/" + subd, 
                    "Expected flag url to be {}, got {}.".format(self.flag_base_url + "TJ/" + subd, os.path.splitext(test_request_tj["TJ"][subd]["flagUrl"])[0])) 
                self.assertEqual(requests.get(test_request_tj["TJ"][subd]["flagUrl"], headers=self.user_agent_header).status_code, 200, 
                    "Flag URL invalid: {}.".format(test_request_tj["TJ"][subd]["flagUrl"]))
            for key in list(test_request_tj["TJ"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_subdivision_keys)) 
#3.) 
        test_request_sd = requests.get(self.country_name_base_url + test_country_name_sd, headers=self.user_agent_header).json() #Sudan

        self.assertIsInstance(test_request_sd, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_sd)))
        self.assertEqual(list(test_request_sd.keys()), ["SD"], "Expected output object of API to contain only the SD key, got {}.".format(list(test_request_sd.keys())))
        self.assertEqual(list(test_request_sd["SD"].keys()), 
            ["SD-DC", "SD-DE", "SD-DN", "SD-DS", "SD-DW", "SD-GD", "SD-GK", "SD-GZ", "SD-KA", "SD-KH", \
             "SD-KN", "SD-KS", "SD-NB", "SD-NO", "SD-NR", "SD-NW", "SD-RS", "SD-SI"], "")    
         
        for subd in test_request_sd["SD"]:
            self.assertIsNot(test_request_sd["SD"][subd]["name"], None, 
                "Expected subdivision name to not be None, got {}.".format(test_request_sd["SD"][subd]["name"]))
            self.assertEqual(test_request_sd["SD"][subd]["name"], test_request_sd["SD"][subd]["localName"],
                "Expected subdivision's name and local name to be the same.")
            if not (test_request_sd["SD"][subd]["parentCode"] is None):
                self.assertIn(test_request_sd["SD"][subd]["parentCode"], list(test_request_sd["SD"][subd].keys()), 
                    "Parent code {} not found in list of subdivision codes.".format(test_request_sd["SD"][subd]["parentCode"]))
            if not (test_request_sd["SD"][subd]["flagUrl"] is None):
                self.assertEqual(os.path.splitext(test_request_sd["SD"][subd]["flagUrl"])[0], self.flag_base_url + "SD/" + subd, 
                    "Expected flag url to be {}, got {}.".format(self.flag_base_url + "SD/" + subd, os.path.splitext(test_request_sd["SD"][subd]["flagUrl"])[0])) 
                self.assertEqual(requests.get(test_request_sd["SD"][subd]["flagUrl"], headers=self.user_agent_header).status_code, 200, 
                    "Flag URL invalid: {}.".format(test_request_sd["SD"][subd]["flagUrl"]))
            for key in list(test_request_sd["SD"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_subdivision_keys)) 
#4.)
        test_request_ml_ni = requests.get(self.country_name_base_url + test_country_name_ml_ni, headers=self.user_agent_header).json() #Mali and Nicaragua

        self.assertIsInstance(test_request_ml_ni, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_ml_ni)))
        self.assertEqual(list(test_request_ml_ni.keys()), ["ML", "NI"], "Expected output object of API to contain only the ML and NI keys, got {}.".format(list(test_request_ml_ni.keys())))
        self.assertEqual(list(test_request_ml_ni["ML"].keys()), ["ML-1", "ML-10", "ML-2", "ML-3", "ML-4", "ML-5", "ML-6", "ML-7", "ML-8", "ML-9", "ML-BKO"], "")
        self.assertEqual(list(test_request_ml_ni["NI"].keys()), 
            ["NI-AN", "NI-AS", "NI-BO", "NI-CA", "NI-CI", "NI-CO", "NI-ES", "NI-GR", "NI-JI", "NI-LE", "NI-MD", "NI-MN", "NI-MS", "NI-MT", "NI-NS", "NI-RI", "NI-SJ"], "")    
        
        for subd in test_request_ml_ni["ML"]:
            self.assertIsNot(test_request_ml_ni["ML"][subd]["name"], None, 
                "Expected subdivision name to not be None, got {}.".format(test_request_ml_ni["ML"][subd]["name"]))
            self.assertEqual(test_request_ml_ni["ML"][subd]["name"], test_request_ml_ni["ML"][subd]["localName"],
                "Expected subdivision's name and local name to be the same.")
            if not (test_request_ml_ni["ML"][subd]["parentCode"] is None):
                self.assertIn(test_request_ml_ni["ML"][subd]["parentCode"], list(test_request_ml_ni["ML"][subd].keys()), 
                    "Parent code {} not found in list of subdivision codes.".format(test_request_ml_ni["ML"][subd]["parentCode"]))            
            if not (test_request_ml_ni["ML"][subd]["flagUrl"] is None):
                self.assertEqual(os.path.splitext(test_request_ml_ni["ML"][subd]["flagUrl"])[0], self.flag_base_url + "ML/" + subd, 
                    "Expected flag url to be {}, got {}.".format(self.flag_base_url + "ML/" + subd, os.path.splitext(test_request_ml_ni["ML"][subd]["flagUrl"])[0])) 
                self.assertEqual(requests.get(test_request_ml_ni["ML"][subd]["flagUrl"], headers=self.user_agent_header).status_code, 200, 
                    "Flag URL invalid: {}.".format(test_request_ml_ni["ML"][subd]["flagUrl"]))
            for key in list(test_request_ml_ni["ML"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_subdivision_keys)) 

        for subd in test_request_ml_ni["NI"]:
            self.assertIsNot(test_request_ml_ni["NI"][subd]["name"], None, 
                "Expected subdivision name to not be None, got {}.".format(test_request_ml_ni["NI"][subd]["name"]))
            self.assertEqual(test_request_ml_ni["NI"][subd]["name"], test_request_ml_ni["NI"][subd]["localName"],
                "Expected subdivision's name and local name to be the same.")
            if not (test_request_ml_ni["NI"][subd]["parentCode"] is None):
                self.assertIn(test_request_ml_ni["NI"][subd]["parentCode"], list(test_request_ml_ni["NI"][subd].keys()), 
                    "Parent code {} not found in list of subdivision codes.".format(test_request_ml_ni["NI"][subd]["parentCode"]))    
            if not (test_request_ml_ni["NI"][subd]["flagUrl"] is None):
                self.assertEqual(os.path.splitext(test_request_ml_ni["NI"][subd]["flagUrl"])[0], self.flag_base_url + "NI/" + subd, 
                    "Expected flag url to be {}, got {}.".format(self.flag_base_url + "NI/" + subd, os.path.splitext(test_request_ml_ni["NI"][subd]["flagUrl"])[0])) 
                self.assertEqual(requests.get(test_request_ml_ni["NI"][subd]["flagUrl"], headers=self.user_agent_header).status_code, 200, 
                    "Flag URL invalid: {}.".format(test_request_ml_ni["NI"][subd]["flagUrl"]))
            for key in list(test_request_ml_ni["NI"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_subdivision_keys)) 
#5.)
        test_request_error = requests.get(self.country_name_base_url + test_country_name_error1, headers=self.user_agent_header).json() #ABCDEF

        self.assertIsInstance(test_request_error, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_error)))
        self.assertEqual(len(test_request_error), 3, "Expected output object of API to be of length 3, got {}.".format(len(test_request_error)))
        self.assertEqual(test_request_error["message"], "Invalid country name input: {}.".format(test_country_name_error1.title()), 
                "Error message does not match expected:\n{}".format(test_request_error["message"]))
        self.assertEqual(test_request_error["path"], self.country_name_base_url + test_country_name_error1, 
                "Error path does not match expected:\n{}".format(test_request_error["path"]))
        self.assertEqual(test_request_error["status"], 400, 
                "Error status does not match expected:\n{}".format(test_request_error["status"]))
#6.)
        test_request_error = requests.get(self.country_name_base_url + test_country_name_error2, headers=self.user_agent_header).json() #12345

        self.assertIsInstance(test_request_error, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_error)))
        self.assertEqual(len(test_request_error), 3, "Expected output object of API to be of length 3, got {}.".format(len(test_request_error)))
        self.assertEqual(test_request_error["message"], "Invalid country name input: {}.".format(test_country_name_error2.title()), 
                "Error message does not match expected:\n{}".format(test_request_error["message"]))
        self.assertEqual(test_request_error["path"], self.country_name_base_url + test_country_name_error2, 
                "Error path does not match expected:\n{}".format(test_request_error["path"]))
        self.assertEqual(test_request_error["status"], 400, 
                "Error status does not match expected:\n{}".format(test_request_error["status"]))

    @unittest.skip("Skipping /all endpoint tests to not overload server.")
    def test_all_endpoint(self):
        """ Test /all endpoint which returns all subdivision data for all ISO 3166 countries. """
#1.)
        test_request_all = requests.get(self.all_base_url, headers=self.user_agent_header).json()

        self.assertIsInstance(test_request_all, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_all)))
        self.assertEqual(len(test_request_all), 250, "Expected output object of API to be of length 250, got {}.".format(len(test_request_all)))
        for alpha2 in list(test_request_all.keys()):
            self.assertIn(alpha2, iso3166.countries_by_alpha2, "Alpha-2 code {} not found in list of available country codes.".format(alpha2))
            for subd in test_request_all[alpha2]:
                self.assertIn(subd, self.iso3166_2_data.subdivision_codes(), "Subdivision code {} not found in list of available subdivision codes.".format(subd))

if __name__ == '__main__':
    #run all unit tests
    unittest.main(verbosity=2)  