import iso3166
import requests
import getpass
import os
from importlib.metadata import metadata
from bs4 import BeautifulSoup
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

# @unittest.skip("")
class ISO3166_2_API_Tests(unittest.TestCase):
    """
    Test suite for testing ISO 3166-2 api created to accompany the iso3166-2 Python software package. 

    Test Cases
    ==========
    test_homepage_endpoint:
        testing main endpoint that returns the homepage and API documentation. 
    test_alpha2_endpoint:
        testing correct objects are returned from /alpha2 API endpoint using a variety of inputs.
    test_name_endpoint:
        testing correct objects are returned from /name API endpoint using a variety of inputs.
    test_all_endpoint:
        testing correct objects are returned from /name API endpoint, which returns all the available 
        ISO 3166-2 data.   
    """
    def setUp(self):
        """ Initialise test variables, import json. """
        #initalise User-agent header for requests library 
        self.__version__ = metadata('iso3166-2')['version']
        self.user_agent_header = {'User-Agent': 'iso3166-2/{} ({}; {})'.format(self.__version__,
                                            'https://github.com/amckenna41/iso3166-2', getpass.getuser())}

        #url endpoints for API
        self.api_base_url = "https://iso3166-2-api.vercel.app/api/"
        # self.api_base_url = "https://iso3166-2-api-amckenna41.vercel.app/api/" 
        self.alpha2_base_url = self.api_base_url + "alpha2/"
        self.name_base_url = self.api_base_url + "name/"
        self.all_base_url = self.api_base_url + "all"

        #list of keys that should be in subdivisions key of output object
        self.correct_subdivision_keys = ["name", "localName", "type", "parentCode", "latLng", "flagUrl"]

        #base url for subdivision flag icons
        self.flag_base_url = "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/"
        
    def test_homepage_endpoint(self):
        """ Testing contents of main "/api" endpoint that returns the homepage and API documentation. """
        test_request_main = requests.get(self.api_base_url, headers=self.user_agent_header)
        soup = BeautifulSoup(test_request_main.content, 'html.parser')
#1.)
        version = soup.find(id='version').text.split(': ')[1]
        last_updated = soup.find(id='last-updated').text.split(': ')[1]
        author = soup.find(id='author').text.split(': ')[1]

        self.assertEqual(version, "1.3.0", "Expected API version to be 1.3.0, got {}.".format(version))
        self.assertEqual(last_updated, "December 2023", "Expected last updated data to be December 2023, got {}.".format(last_updated))
        self.assertEqual(author, "AJ", "Expected author to be AJ, got {}.".format(author))
#2.)
        section_list_menu = soup.find(id='section-list-menu').find_all('li')
        correct_section_menu = ["About", "Attributes", "Endpoints", "All", "Alpha-2 Code", "Name", "Credits", "Contributing"]
        for li in section_list_menu:
            self.assertIn(li.text.strip(), correct_section_menu, "Expected list element {} to be in list.".format(li))

    def test_alpha2_endpoint(self):
        """ Testing alpha-2 endpoint, return all ISO 3166 subdivision data from input alpha-2 code/codes. """
        test_alpha2_au = "AU" #Australia
        test_alpha2_cy = "CY" #Cyprus
        test_alpha2_lu = "LU" #Luxembourg
        test_alpha2_pa_rw = "PA, RW" #Panama, Rwanda
        test_alpha2_error_1 = "ABCDE"
        test_alpha2_error_2 = "12345"
#1.)
        test_request_au = requests.get(self.alpha2_base_url + test_alpha2_au, headers=self.user_agent_header).json() #Australia

        self.assertIsInstance(test_request_au, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_au)))
        self.assertEqual(len(test_request_au), 1, "Expected output object of API to be of length 1, got {}.".format(len(test_request_au)))
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
        test_request_cy = requests.get(self.alpha2_base_url + test_alpha2_cy, headers=self.user_agent_header).json() #Cyprus

        self.assertIsInstance(test_request_cy, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_cy)))
        self.assertEqual(len(test_request_cy), 1, "Expected output object of API to be of length 1, got {}.".format(len(test_request_cy)))
        self.assertEqual(list(test_request_cy.keys()), ["CY"], "Expected output object of API to contain only the CY key, got {}.".format(list(test_request_cy.keys())))
        self.assertEqual(list(test_request_cy["CY"].keys()), ["CY-01", "CY-02", "CY-03", "CY-04", "CY-05", "CY-06"], "Expected list of subdivision codes doesn't match output.")       
        for subd in test_request_cy["CY"]:
            self.assertIsNot(test_request_cy["CY"][subd]["name"], None, 
                "Expected subdivision name to not be None, got {}.".format(test_request_cy["CY"][subd]["name"]))
            if not (test_request_cy["CY"][subd]["parentCode"] is None):
                self.assertIn(test_request_cy["CY"][subd]["parentCode"], list(test_request_cy["CY"][subd].keys()), 
                    "Parent code {} not found in list of subdivision codes.".format(test_request_cy["CY"][subd]["parentCode"]))
            if not (test_request_cy["CY"][subd]["flagUrl"] is None):
                self.assertEqual(os.path.splitext(test_request_cy["CY"][subd]["flagUrl"])[0], self.flag_base_url + "CY/" + subd, 
                    "Expected flag url to be {}, got {}.".format(self.flag_base_url + "CY/" + subd, os.path.splitext(test_request_cy["CY"][subd]["flagUrl"])[0])) 
                self.assertEqual(requests.get(test_request_cy["CY"][subd]["flagUrl"], headers=self.user_agent_header).status_code, 200, 
                    "Flag URL invalid: {}.".format(test_request_cy["CY"][subd]["flagUrl"]))
            for key in list(test_request_cy["CY"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_subdivision_keys))

        #CY-01 - Lefkosia
        self.assertEqual(test_request_cy["CY"]["CY-01"]["name"], "Lefkosia", 
            "Expected subdivsion name to be Lefkosia, got {}.".format(test_request_cy["CY"]["CY-01"]["name"]))  
        self.assertEqual(test_request_cy["CY"]["CY-01"]["localName"], "Lefkosia", 
            "Expected subdivsion local name to be Lefkosia, got {}.".format(test_request_cy["CY"]["CY-01"]["localName"])) 
        self.assertEqual(test_request_cy["CY"]["CY-01"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_request_cy["CY"]["CY-01"]["parentCode"]))
        self.assertEqual(test_request_cy["CY"]["CY-01"]["type"], "District", 
            "Expected subdivision type to be District, got {}.".format(test_request_cy["CY"]["CY-01"]["type"]))
        self.assertEqual(test_request_cy["CY"]["CY-01"]["latLng"], [35.186, 33.382],
            "Expected subdivision latLng to be [35.186, 33.382], got {}.".format(test_request_cy["CY"]["CY-01"]["latLng"]))
        self.assertEqual(test_request_cy["CY"]["CY-01"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/CY/CY-01.svg",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/CY/CY-01.svg, got {}.".format(test_request_cy["CY"]["CY-01"]["flagUrl"]))
        #CY-02 - Lemesos
        self.assertEqual(test_request_cy["CY"]["CY-02"]["name"], "Lemesos", 
            "Expected subdivsion name to be Lemesos, got {}.".format(test_request_cy["CY"]["CY-02"]["name"]))  
        self.assertEqual(test_request_cy["CY"]["CY-02"]["localName"], "Lemesos", 
            "Expected subdivsion local name to be Lemesos, got {}.".format(test_request_cy["CY"]["CY-02"]["localName"])) 
        self.assertEqual(test_request_cy["CY"]["CY-02"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_request_cy["CY"]["CY-02"]["parentCode"]))
        self.assertEqual(test_request_cy["CY"]["CY-02"]["type"], "District", 
            "Expected subdivision type to be District, got {}.".format(test_request_cy["CY"]["CY-02"]["type"]))
        self.assertEqual(test_request_cy["CY"]["CY-02"]["latLng"], [34.679, 33.041],
            "Expected subdivision latLng to be [34.679, 33.041], got {}.".format(test_request_cy["CY"]["CY-02"]["latLng"]))
        self.assertEqual(test_request_cy["CY"]["CY-02"]["flagUrl"], None,
            "Expected subdivision flag url to be None, got {}.".format(test_request_cy["CY"]["CY-02"]["flagUrl"]))
#3.) 
        test_request_lu = requests.get(self.alpha2_base_url + test_alpha2_lu, headers=self.user_agent_header).json() #Luxembourg

        self.assertIsInstance(test_request_lu, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_lu)))
        self.assertEqual(len(test_request_lu), 1, "Expected output object of API to be of length 1, got {}.".format(len(test_request_lu)))
        self.assertEqual(list(test_request_lu.keys()), ["LU"], "Expected output object of API to contain only the LU key, got {}.".format(list(test_request_lu.keys())))
        self.assertEqual(list(test_request_lu["LU"].keys()), ["LU-CA", "LU-CL", "LU-DI", "LU-EC", "LU-ES", "LU-GR", "LU-LU", "LU-ME", "LU-RD", "LU-RM", "LU-VD", "LU-WI"], 
            "Expected list of subdivision codes doesn't match output.")        
        for subd in test_request_lu["LU"]:
            self.assertIsNot(test_request_lu["LU"][subd]["name"], None, 
                "Expected subdivision name to not be None, got {}.".format(test_request_lu["LU"][subd]["name"]))
            self.assertEqual(test_request_lu["LU"][subd]["name"], test_request_lu["LU"][subd]["localName"],
                "Expected subdivision's name and local name to be the same.")
            if not (test_request_lu["LU"][subd]["parentCode"] is None):
                self.assertIn(test_request_lu["LU"][subd]["parentCode"], list(test_request_lu["LU"][subd].keys()), 
                    "Parent code {} not found in list of subdivision codes.".format(test_request_lu["LU"][subd]["parentCode"]))
            if not (test_request_lu["LU"][subd]["flagUrl"] is None):
                self.assertEqual(os.path.splitext(test_request_lu["LU"][subd]["flagUrl"])[0], self.flag_base_url + "LU/" + subd, 
                    "Expected flag url to be {}, got {}.".format(self.flag_base_url + "LU/" + subd, os.path.splitext(test_request_lu["LU"][subd]["flagUrl"])[0])) 
                self.assertEqual(requests.get(test_request_lu["LU"][subd]["flagUrl"], headers=self.user_agent_header).status_code, 200, 
                    "Flag URL invalid: {}.".format(test_request_lu["LU"][subd]["flagUrl"]))
            for key in list(test_request_lu["LU"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_subdivision_keys)) 

        #LU-CA - Capellen
        self.assertEqual(test_request_lu["LU"]["LU-CA"]["name"], "Capellen", 
            "Expected subdivsion name to be Capellen, got {}.".format(test_request_lu["LU"]["LU-CA"]["name"]))  
        self.assertEqual(test_request_lu["LU"]["LU-CA"]["localName"], "Capellen", 
            "Expected subdivsion local name to be Capellen, got {}.".format(test_request_lu["LU"]["LU-CA"]["localName"])) 
        self.assertEqual(test_request_lu["LU"]["LU-CA"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_request_lu["LU"]["LU-CA"]["parentCode"]))
        self.assertEqual(test_request_lu["LU"]["LU-CA"]["type"], "Canton", 
            "Expected subdivision type to be Canton, got {}.".format(test_request_lu["LU"]["LU-CA"]["type"]))
        self.assertEqual(test_request_lu["LU"]["LU-CA"]["latLng"], [49.646, 5.991],
            "Expected subdivision latLng to be [49.646, 5.991], got {}.".format(test_request_lu["LU"]["LU-CA"]["latLng"]))
        self.assertEqual(test_request_lu["LU"]["LU-CA"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/LU/LU-CA.svg",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/LU/LU-CA.svg, got {}.".format(test_request_lu["LU"]["LU-CA"]["flagUrl"]))
        #LU-LU - Luxembourg
        self.assertEqual(test_request_lu["LU"]["LU-LU"]["name"], "Luxembourg", 
            "Expected subdivsion name to be Luxembourg, got {}.".format(test_request_lu["LU"]["LU-LU"]["name"]))  
        self.assertEqual(test_request_lu["LU"]["LU-LU"]["localName"], "Luxembourg", 
            "Expected subdivsion local name to be Luxembourg, got {}.".format(test_request_lu["LU"]["LU-LU"]["localName"])) 
        self.assertEqual(test_request_lu["LU"]["LU-LU"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_request_lu["LU"]["LU-LU"]["parentCode"]))
        self.assertEqual(test_request_lu["LU"]["LU-LU"]["type"], "Canton", 
            "Expected subdivision type to be Canton, got {}.".format(test_request_lu["LU"]["LU-LU"]["type"]))
        self.assertEqual(test_request_lu["LU"]["LU-LU"]["latLng"], [49.815, 6.13],
            "Expected subdivision latLng to be [49.815, 6.13], got {}.".format(test_request_lu["LU"]["LU-LU"]["latLng"]))
        self.assertEqual(test_request_lu["LU"]["LU-LU"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/LU/LU-LU.png",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/LU/LU-LU.png, got {}.".format(test_request_lu["LU"]["LU-LU"]["flagUrl"]))
#4.)
        test_request_pa_rw = requests.get(self.alpha2_base_url + test_alpha2_pa_rw, headers=self.user_agent_header).json() #Panama and Rwanda

        self.assertIsInstance(test_request_pa_rw, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_pa_rw)))
        self.assertEqual(len(test_request_pa_rw), 2, "Expected output object of API to be of length 2, got {}.".format(len(test_request_pa_rw)))
        self.assertEqual(list(test_request_pa_rw.keys()), ["PA", "RW"], "Expected output object of API to contain only the PA and RW keys, got {}.".format(list(test_request_pa_rw.keys())))
        self.assertEqual(list(test_request_pa_rw["PA"].keys()), ["PA-1", "PA-10", "PA-2", "PA-3", "PA-4", "PA-5", "PA-6", "PA-7", "PA-8", "PA-9", "PA-EM", "PA-KY", "PA-NB", "PA-NT"], 
            "Expected list of subdivision codes doesn't match output.")        
        self.assertEqual(list(test_request_pa_rw["RW"].keys()), ["RW-01", "RW-02", "RW-03", "RW-04", "RW-05"], "Expected list of subdivision codes doesn't match output.")      
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
#5.) 
        test_request_error1 = requests.get(self.alpha2_base_url + test_alpha2_error_1, headers=self.user_agent_header).json() #ABCDE

        self.assertIsInstance(test_request_error1, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_error1)))
        self.assertEqual(len(test_request_error1), 3, "Expected output object of API to be of length 3, got {}.".format(len(test_request_error1)))
        self.assertEqual(test_request_error1["message"], 'Invalid 2 letter alpha-2 code input: ' + test_alpha2_error_1 + ".", 
                "Error message does not match expected:\n{}".format(test_request_error1["message"]))
        self.assertEqual(test_request_error1["path"], self.alpha2_base_url + test_alpha2_error_1, 
                "Error path does not match expected:\n{}.".format(test_request_error1["path"]))
        self.assertEqual(test_request_error1["status"], 400, 
                "Error status does not match expected:\n{}.".format(test_request_error1["status"]))
#6.)
        test_request_error2 = requests.get(self.alpha2_base_url + test_alpha2_error_2, headers=self.user_agent_header).json() #12345

        self.assertIsInstance(test_request_error2, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_error2)))
        self.assertEqual(len(test_request_error2), 3, "Expected output object of API to be of length 3, got {}.".format(len(test_request_error2)))
        self.assertEqual(test_request_error2["message"], 'Invalid 2 letter alpha-2 code input: ' + test_alpha2_error_2 + ".", 
                "Error message does not match expected:\n{}".format(test_request_error2["message"]))
        self.assertEqual(test_request_error2["path"], self.alpha2_base_url + test_alpha2_error_2, 
                "Error path does not match expected:\n{}.".format(test_request_error2["path"]))
        self.assertEqual(test_request_error2["status"], 400, 
                "Error status does not match expected:\n{}.".format(test_request_error2["status"]))

    def test_name_endpoint(self):
        """ Testing name endpoint, return all ISO 3166 subdivision data from input alpha-2 name/names. """
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
        test_request_bj = requests.get(self.name_base_url + test_name_bj, headers=self.user_agent_header).json() #Benin

        self.assertIsInstance(test_request_bj, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_bj)))
        self.assertEqual(len(test_request_bj), 1, "Expected output object of API to be of length 1, got {}.".format(len(test_request_bj)))
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
        test_request_tj = requests.get(self.name_base_url + test_name_tj, headers=self.user_agent_header).json() #Tajikistan

        self.assertIsInstance(test_request_tj, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_tj)))
        self.assertEqual(len(test_request_tj), 1, "Expected output object of API to be of length 1, got {}.".format(len(test_request_tj)))
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
        test_request_sd = requests.get(self.name_base_url + test_name_sd, headers=self.user_agent_header).json() #Sudan

        self.assertIsInstance(test_request_sd, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_sd)))
        self.assertEqual(len(test_request_sd), 1, "Expected output object of API to be of length 1, got {}.".format(len(test_request_sd)))
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
        test_request_ml_ni = requests.get(self.name_base_url + test_name_ml_ni, headers=self.user_agent_header).json() #Mali and Nicaragua

        self.assertIsInstance(test_request_ml_ni, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_ml_ni)))
        self.assertEqual(len(test_request_ml_ni), 2, "Expected output object of API to be of length 2, got {}.".format(len(test_request_ml_ni)))
        self.assertEqual(list(test_request_ml_ni.keys()), ["ML", "NI"], "Expected output object of API to contain only the ML and NI keys, got {}.".format(list(test_request_ml_ni.keys())))
        self.assertEqual(list(test_request_ml_ni["ML"].keys()), ["ML-1", "ML-10", "ML-2", "ML-3", "ML-4", "ML-5", "ML-6", "ML-7", "ML-8", "ML-9", "ML-BKO"], "")     
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

        self.assertEqual(list(test_request_ml_ni["NI"].keys()), 
            ["NI-AN", "NI-AS", "NI-BO", "NI-CA", "NI-CI", "NI-CO", "NI-ES", "NI-GR", "NI-JI", "NI-LE", "NI-MD", "NI-MN", "NI-MS", "NI-MT", "NI-NS", "NI-RI", "NI-SJ"], "")     
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
        test_request_error = requests.get(self.name_base_url + test_name_error1, headers=self.user_agent_header).json() #ABCDEF

        self.assertIsInstance(test_request_error, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_error)))
        self.assertEqual(len(test_request_error), 3, "Expected output object of API to be of length 3, got {}.".format(len(test_request_error)))
        self.assertEqual(test_request_error["message"], 'Country name ' + test_name_error1.title() + " not found in the ISO 3166.", 
                "Error message does not match expected:\n{}".format(test_request_error["message"]))
        self.assertEqual(test_request_error["path"], self.name_base_url + test_name_error1, 
                "Error path does not match expected:\n{}".format(test_request_error["path"]))
        self.assertEqual(test_request_error["status"], 400, 
                "Error status does not match expected:\n{}".format(test_request_error["status"]))
#6.)
        test_request_error = requests.get(self.name_base_url + test_name_error2, headers=self.user_agent_header).json() #12345

        self.assertIsInstance(test_request_error, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_error)))
        self.assertEqual(len(test_request_error), 3, "Expected output object of API to be of length 3, got {}.".format(len(test_request_error)))
        self.assertEqual(test_request_error["message"], 'Country name ' + test_name_error2.title() + " not found in the ISO 3166.", 
                "Error message does not match expected:\n{}".format(test_request_error["message"]))
        self.assertEqual(test_request_error["path"], self.name_base_url + test_name_error2, 
                "Error path does not match expected:\n{}".format(test_request_error["path"]))
        self.assertEqual(test_request_error["status"], 400, 
                "Error status does not match expected:\n{}".format(test_request_error["status"]))

    @unittest.skip("Skipping /all endpoint tests to not overload server.")
    def test_all_endpoint(self):
        """ Test 'all' endpoint which returns all subdivision data for all ISO 3166 countries. """
#1.)
        test_request_all = requests.get(self.all_base_url, headers=self.user_agent_header).json()

        self.assertIsInstance(test_request_all, dict, "Expected output object of API to be type dict, got {}.".format(type(test_request_all)))
        self.assertEqual(len(test_request_all), 250, "Expected output object of API to be of length 250, got {}.".format(len(test_request_all)))
        for alpha2 in list(test_request_all.keys()):
            self.assertIn(alpha2, iso3166.countries_by_alpha2, "Alpha-2 code {} not found in list of available codes.".format(alpha2))

if __name__ == '__main__':
    #run all unit tests
    unittest.main(verbosity=2)  