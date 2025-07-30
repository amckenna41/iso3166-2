from iso3166_2 import *
import iso3166
import requests
import re
import json
import os
import shutil
from jsonschema import validate, ValidationError
from fake_useragent import UserAgent
from importlib.metadata import metadata
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

# @unittest.skip("Skipping main iso3166-2 unit tests.")
class ISO3166_2_Tests(unittest.TestCase):
    """
    Test suite for testing the iso3166-2 Python software package. 

    Test Cases
    ==========
    test_iso3166_2_metadata:
        testing correct software metadata for the iso3166-2 package. 
    test_iso3166_2:
        testing correct data returned from the ISO3166_2 class of the iso3166-2 package.  
    test_iso3166_2_json:
        testing correct objects are returned from the ISO 3166-2 JSON, using a variety of inputs.
    test_iso3166_2_json_schema:
        testing the correct schema for the main ISO 3166-2 JSON object.
    test_iso3166_2_individual_subdivision_totals:
        testing individual subdivision total counts for ISO 3166-2 JSON object.
    test_subdivision_codes:
        testing correct ISO 3166-2 subdivision codes are returned from the subdivision_codes() class function.  
    test_subdivision_names:
        testing correct ISO 3166-2 subdivision names are returned from the subdivision_names() class function.
    test_filter_attributes:
        testing correct objects are returned with the relevant attributes included.
    test_search:
        testing searching by subdivision name or local/other name functionality.
    test_custom_subdivision:
        testing custom_subdivision function that adds or deletes custom subdivisions to the main iso3166-2.json object.  
    test_check_for_updates:
        testing check_for_updates functionality which checks for the latest ISO 3166-2 data in the repo.
    test_len:
        testing __len__ functionality which outputs the total number of subdivisions.
    test_str:
        testing __str__ functionality which returns a string representation of the class instance. 
    test_repr:
        testing __repr__ functionality which returns an object representation of the class instance. 
    test_sizeof:
        testing __sizeof__ functionality that gets the size of the object in memory. 
    """
    @classmethod
    def setUp(self):
        """ Initialise test variables, import json. """
        #set random user-agent string for requests library, using fake_useragent package
        user_agent = UserAgent()
        self.user_agent_header = {"headers": user_agent.random}
    
        #base url for flag icons on iso3166-flag-icons repo
        self.flag_icons_base_url = "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/"

        #list of data attributes for main iso3166-2 json
        self.correct_output_attributes = ['name', 'localOtherName', 'type', 'parentCode', 'latLng', 'flag', 'history']

        #class instance with all ISO 3166-2 data
        self.all_iso3166_2 = Subdivisions()

        #create test output directory
        self.test_output_dir = os.path.join("tests", "test_output")
        if not (os.path.isdir(self.test_output_dir)):
            os.mkdir(self.test_output_dir)

    # @unittest.skip("")
    def test_iso3166_2_metadata(self): 
        """ Testing correct iso3166-2 software version and metadata. """
        # self.assertEqual(metadata('iso3166-2')['version'], "1.7.1", 
        #     f"iso3166-2 version is not correct, expected 1.7.1, got {metadata('iso3166-2')['version']}.")
        self.assertEqual(metadata('iso3166-2')['name'], "iso3166-2", 
            f"iso3166-2 software name is not correct, expected iso3166-2, got {metadata('iso3166-2')['name']}.")
        self.assertEqual(metadata('iso3166-2')['author'], "AJ McKenna", 
            f"iso3166-2 author is not correct, expected AJ McKenna, got {metadata('iso3166-2')['author']}.")
        self.assertEqual(metadata('iso3166-2')['author-email'], "amckenna41@qub.ac.uk", 
            f"iso3166-2 author email is not correct, expected amckenna41@qub.ac.uk, got {metadata('iso3166-2')['author-email']}.")
        self.assertEqual(metadata('iso3166-2')['summary'], "A lightweight Python package, and accompanying API, used to access all of the world's most up-to-date and accurate ISO 3166-2 subdivision data, including: name, local/other name, code, parent code, type, latitude/longitude, flag and history.", 
            f"iso3166-2 package summary is not correct, got:\n{metadata('iso3166-2')['summary']}.")
        self.assertEqual(metadata('iso3166-2')['maintainer'], "AJ McKenna", 
            f"iso3166-2 maintainer is not correct, expected AJ McKenna, got {metadata('iso3166-2')['maintainer']}.")
        self.assertEqual(metadata('iso3166-2')['license'], "MIT", 
            f"iso3166-2 license type is not correct, expected MIT, got {metadata('iso3166-2')['license']}.")
        # self.assertEqual(metadata('iso3166-2')['keywords'], "iso,iso3166,beautifulsoup,python,pypi,countries,country codes,iso3166-2,iso3166-1,alpha-2,iso3166-updates,iso3166-flag-icons,subdivisions,regions,dataset",
        #     f"iso3166-2 keywords are not correct, got:\n{metadata('iso3166-2')['keywords']}.")
        # self.assertEqual(metadata('iso3166-2')['documentation'], "https://iso3166-2.readthedocs.io/en/latest/", 
        #     f"iso3166-2 documentation url is not correct, expected https://iso3166-2.readthedocs.io/en/latest/, got {metadata('iso3166-2')['documentation']}.")
        # self.assertEqual(metadata('iso3166-2')['Home-page'], "Homepage, https://github.com/amckenna41/iso3166-2", 
        #     f"iso3166-2 home page url is not correct, expected Homepage, https://github.com/amckenna41/iso3166-2, got {metadata('iso3166-2')['Home-page']}.")

    # @unittest.skip("")
    def test_iso3166_2(self):
        """ Test ISO 3166-2 class and its methods and attributes. """
        self.assertIsInstance(self.all_iso3166_2.all, dict,
            f"Expected ISO 3166-2 data object to be a dict, got {type(self.all_iso3166_2.all)}.")
        self.assertEqual(len(self.all_iso3166_2.all), 250, 
            f"Expected 250 country's in ISO 3166-2 data object, got {len(self.all_iso3166_2.all)}.")  
        subdivision_total = 0     
        for country in self.all_iso3166_2.all: 
            for subd in list(self.all_iso3166_2[country].keys()):       #testing format of each subdivision code
                self.assertTrue(bool(re.match(r"^[A-Z][A-Z]-[A-Z0-9]$|^[A-Z][A-Z]-[A-Z0-9][A-Z0-9]$|[A-Z][A-Z]-[A-Z0-9][A-Z0-9][A-Z0-9]$", subd)), 
                        f"Subdivision code does not match expected format: XX-YYY, XX-YY or XX-Y, where XX is the alpha-2 country code and Y is the ISO 3166-2 subdivision code {subd}.")
                subdivision_total+=1
        self.assertEqual(subdivision_total, 5049, f"Expected there to be 5,049 total subdivisions, but got {subdivision_total}.")

    # @unittest.skip("") 
    def test_iso3166_2_json(self):
        """ Testing ISO 3166-2 JSON contents and data. """ 
        test_iso3166_2_ba = self.all_iso3166_2["BA"] #Bosnia and Herzegovina
        test_iso3166_2_cy = self.all_iso3166_2["CY"] #Cyprus
        test_iso3166_2_ki = self.all_iso3166_2["KIR"] #Kiribati
        test_iso3166_2_rw_548 = self.all_iso3166_2["RW, 548"] #Rwanda, Vanuatu
        test_iso3166_2_gg_kwt_670 = self.all_iso3166_2["GG, KWT, 670"] #Guernsey, Kuwait, St Vincent & the Grenadines
#1.)    
        expected_ba_subdivisions = {
            "BA-BIH": {
                "name": "Federacija Bosne i Hercegovine",
                "localOtherName": None,
                "type": "Entity",
                "parentCode": None,
                "flag": None,
                "latLng": [43.887, 17.843],
                "history": None,
            },
            "BA-BRC": {
                "name": "Brčko distrikt",
                "localOtherName": "Брчко Дистрикт (srp), Brčko District of Bosnia and Herzegovina (eng)",
                "type": "District with special status",
                "parentCode": None,
                "flag": "https://raw.githubusercontent.com/amckenna41/iso3166-flag-icons/main/iso3166-2-icons/BA/BA-BRC.svg",
                "latLng": [44.873, 18.811],
                "history": [
                    "2010-06-30: Subdivisions added: BA-BRC Brčko Distrikt. Description of Change: Addition of the country code prefix as the first code element, addition of names in administrative languages, update of the administrative structure and of the list source. Source: Newsletter II-2 - https://www.iso.org/files/live/sites/isoorg/files/archive/pdf/en/iso_3166-2_newsletter_ii-2_2010-06-30.pdf."
                ],
            },
            "BA-SRP": {
                "name": "Republika Srpska",
                "localOtherName": "Република Српска (srp), Republic of Srpska (eng)",
                "type": "Entity",
                "parentCode": None,
                "flag": "https://raw.githubusercontent.com/amckenna41/iso3166-flag-icons/main/iso3166-2-icons/BA/BA-SRP.svg",
                "latLng": [44.728, 17.315],
                "history": None,
            },
        }
        
        self.assertEqual(test_iso3166_2_ba, expected_ba_subdivisions, f"Expected and observed BA subdivisions do not match:\n{test_iso3166_2_ba}.")
        for key in test_iso3166_2_ba:
            if (not (test_iso3166_2_ba[key].flag is None) and (test_iso3166_2_ba[key].flag != "")):
                self.assertEqual(requests.get(test_iso3166_2_ba[key].flag, headers=self.user_agent_header).status_code, 200, f"Flag URL invalid: {test_iso3166_2_ba[key].flag}.")
            if not (test_iso3166_2_ba[key]["parentCode"] is None):
                self.assertIn(test_iso3166_2_ba[key]["parentCode"], list(test_iso3166_2_ba[key].keys()), 
                    f"Parent code {test_iso3166_2_ba[key]['parentCode']} not found in list of subdivision codes:\n{list(test_iso3166_2_ba[key].keys())}.")    
#2.)
        expected_cy_subdivisions = {
            "CY-01": {
                "name": "Lefkosia",
                "localOtherName": "Λευκωσία (ell), Lefkoşa (tur), Nicosia (eng)",
                "type": "District",
                "parentCode": None,
                "flag": "https://raw.githubusercontent.com/amckenna41/iso3166-flag-icons/main/iso3166-2-icons/CY/CY-01.svg",
                "latLng": [35.186, 33.382],
                "history": None,
            },
            "CY-02": {
                "name": "Lemesos",
                "localOtherName": "Λεμεσός (ell), Leymasun (tur), Limassol (eng)",
                "type": "District",
                "parentCode": None,
                "flag": None,
                "latLng": [34.679, 33.041],
                "history": [
                    "2017-11-23: Update List Source; change of spelling of CY-02, CY-04 (tur). Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:CY."
                ],
            },
            "CY-03": {
                "name": "Larnaka",
                "localOtherName": "Λάρνακα (ell), Larnaka (tur), Larnaca (eng)",
                "type": "District",
                "parentCode": None,
                "flag": None,
                "latLng": [34.918, 33.62],
                "history": None,
            },
            "CY-04": {
                "name": "Ammochostos",
                "localOtherName": "Αμμόχωστος (ell), Mağusa (tur), Famagusta (eng)",
                "type": "District",
                "parentCode": None,
                "flag": None,
                "latLng": [35.121, 33.938],
                "history": [
                    "2017-11-23: Update List Source; change of spelling of CY-02, CY-04 (tur). Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:CY."
                ],
            },
            "CY-05": {
                "name": "Pafos",
                "localOtherName": "Πάφος (ell), Baf (tur), Paphos (eng)",
                "type": "District",
                "parentCode": None,
                "flag": None,
                "latLng": [34.775, 32.422],
                "history": None,
            },
            "CY-06": {
                "name": "Keryneia",
                "localOtherName": "Κερύνεια (ell), Girne (tur), Kyrenia (eng)",
                "type": "District",
                "parentCode": None,
                "flag": None,
                "latLng": [35.332, 33.32],
                "history": None,
            },
        }

        self.assertEqual(test_iso3166_2_cy, expected_cy_subdivisions, f"Expected and observed CY subdivisions do not match:\n{test_iso3166_2_cy}.")
        for key in test_iso3166_2_cy:
            if (not (test_iso3166_2_cy[key].flag is None) and (test_iso3166_2_cy[key].flag != "")):
                self.assertEqual(requests.get(test_iso3166_2_cy[key].flag, headers=self.user_agent_header).status_code, 200, f"Flag URL invalid: {test_iso3166_2_cy[key].flag}.")
            if not (test_iso3166_2_cy[key]["parentCode"] is None):
                self.assertIn(test_iso3166_2_cy[key]["parentCode"], list(test_iso3166_2_cy[key].keys()), 
                    f"Parent code {test_iso3166_2_cy[key]['parentCode']} not found in list of subdivision codes:\n{list(test_iso3166_2_cy[key].keys())}.")    
#3.)
        expected_ki_subdivisions = {
                "KI-G": {
                    "name": "Gilbert Islands",
                    "localOtherName": "Tungaru (gil), Kingsmill (eng), Kings-Mill Islands (eng)",
                    "type": "Group of islands (20 inhabited islands)",
                    "parentCode": None,
                    "flag": None,
                    "latLng": [0.361, 173.185],
                    "history": None,
                },
                "KI-L": {
                    "name": "Line Islands",
                    "localOtherName": "Teraina Islands (eng), Equatorial Islands (eng), Aono Raina (gil)",
                    "type": "Group of islands (20 inhabited islands)",
                    "parentCode": None,
                    "flag": None,
                    "latLng": [-3.373, -155.301],
                    "history": None,
                },
                "KI-P": {
                    "name": "Phoenix Islands",
                    "localOtherName": "Rawaki (eng)",
                    "type": "Group of islands (20 inhabited islands)",
                    "parentCode": None,
                    "flag": None,
                    "latLng": [-3.73, -172.625],
                    "history": None,
                },
            }

        self.assertEqual(test_iso3166_2_ki, expected_ki_subdivisions, f"Expected and observed KI subdivisions do not match:\n{test_iso3166_2_ki}.")
        for key in test_iso3166_2_ki:
            if (not (test_iso3166_2_ki[key].flag is None) and (test_iso3166_2_ki[key].flag != "")):
                self.assertEqual(requests.get(test_iso3166_2_cy[key].flag, headers=self.user_agent_header).status_code, 200, f"Flag URL invalid: {test_iso3166_2_ki[key].flag}.")
            if not (test_iso3166_2_ki[key]["parentCode"] is None):
                self.assertIn(test_iso3166_2_ki[key]["parentCode"], list(test_iso3166_2_ki[key].keys()), 
                    f"Parent code {test_iso3166_2_ki[key]['parentCode']} not found in list of subdivision codes:\n{list(test_iso3166_2_ki[key].keys())}.")    
#4.)
        rw_subdivision_codes = ['RW-01', 'RW-02', 'RW-03', 'RW-04', 'RW-05']
        vu_subdivision_codes = ['VU-MAP', 'VU-PAM', 'VU-SAM', 'VU-SEE', 'VU-TAE', 'VU-TOB']
        rw_subdivision_names = ['City of Kigali', 'Eastern', 'Northern', 'Western', 'Southern']
        vu_subdivision_names = ['Malampa', 'Pénama', 'Sanma', 'Shéfa', 'Taféa', 'Torba']

        self.assertIsInstance(test_iso3166_2_rw_548, dict,  f"Expected output object to be of type dict, got {type(test_iso3166_2_rw_548)}.")
        self.assertEqual(list(test_iso3166_2_rw_548.keys()), ['RW', 'VU'], f"Expected output keys to be RW and VU, got {list(test_iso3166_2_rw_548.keys())}.")
        self.assertEqual(len(test_iso3166_2_rw_548["RW"]), 5, f"Expected 5 total subdivision outputs, got {len(test_iso3166_2_rw_548['RW'])}.")
        self.assertEqual(len(test_iso3166_2_rw_548["VU"]), 6, f"Expected 6 total subdivision outputs, got {len(test_iso3166_2_rw_548['VU'])}.")
        self.assertEqual(list(test_iso3166_2_rw_548["RW"].keys()), rw_subdivision_codes, f"Subdivision codes do not equal expected codes:\n{list(test_iso3166_2_rw_548['RW'].keys())}.")
        self.assertEqual(list(test_iso3166_2_rw_548["VU"].keys()), vu_subdivision_codes, f"Subdivision codes do not equal expected codes:\n{list(test_iso3166_2_rw_548['VU'].keys())}.")
        self.assertEqual(list(test_iso3166_2_rw_548["RW"]['RW-01'].keys()), ['name', 'localOtherName', 'type', 'parentCode', 'flag', 'latLng', 'history'], f"Expected keys for output dict don't match\n{list(test_iso3166_2_rw_548['RW']['RW-01'].keys())}.")
        self.assertEqual(list(test_iso3166_2_rw_548["VU"]['VU-MAP'].keys()), ['name', 'localOtherName', 'type', 'parentCode', 'flag', 'latLng', 'history'], f"Expected keys for output dict don't match\n{list(test_iso3166_2_rw_548['VU']['VU-MAP'].keys())}.")
        for key in list(test_iso3166_2_rw_548["RW"].keys()):
            self.assertIn(test_iso3166_2_rw_548["RW"][key].name, rw_subdivision_names, f"Subdivision name {test_iso3166_2_rw_548['RW'][key].name} not found in list of subdivision names:\n{rw_subdivision_names}.")
            if (not (test_iso3166_2_rw_548["RW"][key].flag is None) and (test_iso3166_2_rw_548["RW"][key].flag != "")):
                self.assertEqual(requests.get(test_iso3166_2_rw_548["RW"][key].flag, headers=self.user_agent_header).status_code, 200, f"Flag URL invalid: {test_iso3166_2_rw_548['RW'][key].flag}.")
            self.assertEqual(len(test_iso3166_2_rw_548["RW"][key].latLng), 2, "Expected key should have both lat/longitude.")        
        for key in list(test_iso3166_2_rw_548["VU"].keys()):
            self.assertIn(test_iso3166_2_rw_548["VU"][key].name, vu_subdivision_names, f"Subdivision name {test_iso3166_2_rw_548['VU'][key].name} not found in list of subdivision names:\n{vu_subdivision_names}.")
            if (not (test_iso3166_2_rw_548["VU"][key].flag is None) and (test_iso3166_2_rw_548["VU"][key].flag != "")):
                self.assertEqual(requests.get(test_iso3166_2_rw_548["VU"][key].flag, headers=self.user_agent_header).status_code, 200, f"Flag URL invalid: {test_iso3166_2_rw_548['VU'][key].flag}.")
            self.assertEqual(len(test_iso3166_2_rw_548["VU"][key].latLng), 2, "Expected key should have both lat/longitude.")              
#5.)
        kw_subdivision_codes = ['KW-AH', 'KW-FA', 'KW-HA', 'KW-JA', 'KW-KU', 'KW-MU']
        kw_subdivision_names = ['Al Aḩmadī', 'Al Farwānīyah', 'Ḩawallī', "Al Jahrā’", "Al ‘Āşimah", 'Mubārak al Kabīr']
        vc_subdivision_codes = ['VC-01', 'VC-02', 'VC-03', 'VC-04', 'VC-05', 'VC-06']
        vc_subdivision_names = ['Charlotte', 'Saint Andrew', 'Saint David', 'Saint George', 'Saint Patrick', 'Grenadines']
        
        self.assertIsInstance(test_iso3166_2_gg_kwt_670, dict, f"Expected output object to be of type dict, got {type(test_iso3166_2_gg_kwt_670)}.")
        self.assertEqual(list(test_iso3166_2_gg_kwt_670.keys()), ['GG', 'KW', 'VC'], f"Expected output keys to be GG, KW and VC, got {list(test_iso3166_2_gg_kwt_670.keys())}.")
        self.assertEqual(len(test_iso3166_2_gg_kwt_670["GG"]), 0, f"Expected 0 total subdivision outputs, got {len(test_iso3166_2_gg_kwt_670['GG'])}.")
        self.assertEqual(len(test_iso3166_2_gg_kwt_670["KW"]), 6, f"Expected 6 total subdivision outputs, got {len(test_iso3166_2_gg_kwt_670['KW'])}.")
        self.assertEqual(len(test_iso3166_2_gg_kwt_670["VC"]), 6, f"Expected 6 total subdivision outputs, got {len(test_iso3166_2_gg_kwt_670['VC'])}.")
        self.assertEqual(list(test_iso3166_2_gg_kwt_670["GG"].keys()), [], f"Expected no subdivision codes, got {list(test_iso3166_2_gg_kwt_670['GG'].keys())}.")
        self.assertEqual(list(test_iso3166_2_gg_kwt_670["KW"].keys()), kw_subdivision_codes, f"Subdivision codes do not equal expected codes:\n{list(test_iso3166_2_gg_kwt_670['KW'].keys())}.")
        self.assertEqual(list(test_iso3166_2_gg_kwt_670["VC"].keys()), vc_subdivision_codes, f"Subdivision codes do not equal expected codes:\n{list(test_iso3166_2_gg_kwt_670['VC'].keys())}.")
        self.assertEqual(list(test_iso3166_2_gg_kwt_670["KW"]['KW-AH'].keys()), ['name', 'localOtherName', 'type', 'parentCode', 'flag', 'latLng', 'history'], 
            f"Expected keys do not match output:\n{list(test_iso3166_2_gg_kwt_670['KW']['KW-AH'].keys())}.")
        self.assertEqual(list(test_iso3166_2_gg_kwt_670["VC"]['VC-01'].keys()), ['name', 'localOtherName', 'type', 'parentCode', 'flag', 'latLng', 'history'],
            f"Expected keys do not match output:\n{list(test_iso3166_2_gg_kwt_670['VC']['VC-01'].keys())}.")
        for key in list(test_iso3166_2_gg_kwt_670["KW"].keys()):
            self.assertIn(test_iso3166_2_gg_kwt_670["KW"][key].name, kw_subdivision_names, f"Subdivision name {test_iso3166_2_gg_kwt_670['KW'][key].name} not found in list of subdivision names:\n{kw_subdivision_names}.")
            if (not (test_iso3166_2_gg_kwt_670["KW"][key].flag is None) and (test_iso3166_2_gg_kwt_670["KW"][key].flag != "")):
                self.assertEqual(requests.get(test_iso3166_2_gg_kwt_670["KW"][key].flag, headers=self.user_agent_header).status_code, 200, f"Flag URL invalid: {test_iso3166_2_gg_kwt_670['KW'][key].flag}.")
            self.assertEqual(len(test_iso3166_2_gg_kwt_670["KW"][key].latLng), 2, "Expected key should have both lat/longitude.")        
        for key in list(test_iso3166_2_gg_kwt_670["VC"].keys()):
            self.assertIn(test_iso3166_2_gg_kwt_670["VC"][key].name, vc_subdivision_names, f"Subdivision name {test_iso3166_2_gg_kwt_670['VC'][key].name} not found in list of subdivision names:\n{vc_subdivision_names}.")
            if (not (test_iso3166_2_gg_kwt_670["VC"][key].flag is None) and (test_iso3166_2_gg_kwt_670["VC"][key].flag != "")):
                self.assertEqual(requests.get(test_iso3166_2_gg_kwt_670["VC"][key].flag, headers=self.user_agent_header).status_code, 200, f"Flag URL invalid: {test_iso3166_2_gg_kwt_670['VC'][key].flag}.")
            self.assertEqual(len(test_iso3166_2_gg_kwt_670["VC"][key].latLng), 2, "Expected key should have both lat/longitude.")        
#6.)
        for country in self.all_iso3166_2.all:              #testing that all subdivisions have a subdivision name, local name, type and lat/lng value
            for subd in self.all_iso3166_2.all[country]:
                self.assertTrue((self.all_iso3166_2.all[country][subd]["name"] != "" and self.all_iso3166_2.all[country][subd]["name"] != []), 
                    f"Expected name attribute to not be empty ({subd}):\n{self.all_iso3166_2.all[country][subd]['name']}.")
                self.assertTrue((self.all_iso3166_2.all[country][subd]["localOtherName"] != "" and self.all_iso3166_2.all[country][subd]["localOtherName"] != []),
                    f"Expected localOtherName attribute to not be empty ({subd}):\n{self.all_iso3166_2.all[country][subd]['localOtherName']}.")
                self.assertTrue((self.all_iso3166_2.all[country][subd]["type"] != "" and self.all_iso3166_2.all[country][subd]["type"] != []),
                    f"Expected type attribute to not be empty ({subd}):\n{self.all_iso3166_2.all[country][subd]['type']}.")
                self.assertTrue((self.all_iso3166_2.all[country][subd]["latLng"] != "" and self.all_iso3166_2.all[country][subd]["latLng"] != []),
                    f"Expected latLng attribute to not be empty ({subd}):\n{self.all_iso3166_2.all[country][subd]['latLng']}.")
#7.)
        with (self.assertRaises(ValueError)):
            Subdivisions("ZZ")
            Subdivisions("XY")
            Subdivisions("XYZ")
            Subdivisions("AB, CD, EF")
            Subdivisions("56789")
            self.all_iso3166_2["ZZ"]
            self.all_iso3166_2["XY"]
            self.all_iso3166_2["XYZ"]
            self.all_iso3166_2["AB, CD, EF"]
#8.)
        with (self.assertRaises(TypeError)):
            self.all_iso3166_2[123]
            self.all_iso3166_2[0.5]
            self.all_iso3166_2[False]

    # @unittest.skip("")
    def test_iso3166_2_json_schema(self):
        """ Testing the schema format of the ISO 3166-2 JSON object. """
        with open(os.path.join("tests", "test_files", "test_iso3166-2.json"), encoding="utf-8") as iso3166_2_json:
            iso3166_2_all = json.loads(iso3166_2_json.read())
        schema = {
            "type": "object",
            "patternProperties": {
                "^[A-Z]{2}$": {  # Country code like VE, US, GB
                    "type": "object",
                    "patternProperties": {
                        "^[A-Z]{2,3}-[A-Z0-9]{1,}$": {  # Subdivision code like VE-A, GB-ENG
                            "type": "object",
                            "properties": {
                                "flag": {"type": ["string", "null"]},
                                "latLng": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "minItems": 2,
                                    "maxItems": 2,
                                },
                                "localOtherName": {"type": ["string", "null"]},
                                "name": {"type": "string"},
                                "parentCode": {"type": ["string", "null"]},
                                "type": {"type": "string"},
                                "history": {"type": ["array", "null"]},
                            },
                            "required": ["name", "type", "latLng"],
                            "additionalProperties": False,
                        }
                    },
                    "additionalProperties": False,
                }
            },
            "additionalProperties": False,
        }

        try:
                validate(instance=iso3166_2_all, schema=schema)
        except ValidationError as e:
                self.fail(f"JSON schema for /all endpoint output validation failed: {e.message}.")

    # @unittest.skip("")
    def test_iso3166_2_individual_subdivision_totals(self):
        """ Testing individual subdivision total counts. """
        #expected subdivision counts per country
        expected_counts = {
            'AD': 7, 'AE': 7, 'AF': 34, 'AG': 8, 'AI': 0, 'AL': 12, 'AM': 11, 'AO': 18, 'AQ': 0, 'AR': 24,
            'AS': 0, 'AT': 9, 'AU': 8, 'AW': 0, 'AX': 0, 'AZ': 78, 'BA': 3, 'BB': 11, 'BD': 72, 'BE': 13,
            'BF': 58, 'BG': 28, 'BH': 4, 'BI': 18, 'BJ': 12, 'BL': 0, 'BM': 0, 'BN': 4, 'BO': 9, 'BQ': 3,
            'BR': 27, 'BS': 32, 'BT': 20, 'BV': 0, 'BW': 16, 'BY': 7, 'BZ': 6, 'CA': 13, 'CC': 0, 'CD': 26,
            'CF': 17, 'CG': 12, 'CH': 26, 'CI': 14, 'CK': 0, 'CL': 16, 'CM': 10, 'CN': 34, 'CO': 33,
            'CR': 7, 'CU': 16, 'CV': 24, 'CW': 0, 'CX': 0, 'CY': 6, 'CZ': 90, 'DE': 16, 'DJ': 6, 'DK': 5,
            'DM': 10, 'DO': 42, 'DZ': 58, 'EC': 24, 'EE': 94, 'EG': 27, 'EH': 0, 'ER': 6, 'ES': 69, 'ET': 13,
            'FI': 19, 'FJ': 19, 'FK': 0, 'FM': 4, 'FO': 0, 'FR': 124, 'GA': 9, 'GB': 224, 'GD': 7, 'GE': 12,
            'GF': 0, 'GG': 0, 'GH': 16, 'GI': 0, 'GL': 5, 'GM': 6, 'GN': 41, 'GP': 0, 'GQ': 10, 'GR': 14,
            'GS': 0, 'GT': 22, 'GU': 0, 'GW': 12, 'GY': 10, 'HK': 0, 'HM': 0, 'HN': 18, 'HR': 21, 'HT': 10,
            'HU': 43, 'ID': 45, 'IE': 30, 'IL': 6, 'IM': 0, 'IN': 36, 'IO': 0, 'IQ': 19, 'IR': 31, 'IS': 72,
            'IT': 126, 'JE': 0, 'JM': 14, 'JO': 12, 'JP': 47, 'KE': 47, 'KG': 9, 'KH': 25, 'KI': 3, 'KM': 3,
            'KN': 16, 'KP': 13, 'KR': 17, 'KW': 6, 'KY': 0, 'KZ': 20, 'LA': 18, 'LB': 8, 'LC': 10, 'LI': 11,
            'LK': 34, 'LR': 15, 'LS': 10, 'LT': 70, 'LU': 12, 'LV': 43, 'LY': 22, 'MA': 87, 'MC': 17,
            'MD': 37, 'ME': 25, 'MF': 0, 'MG': 6, 'MH': 26, 'MK': 80, 'ML': 11, 'MM': 15, 'MN': 22, 'MO': 0,
            'MP': 0, 'MQ': 0, 'MR': 15, 'MS': 0, 'MT': 68, 'MU': 12, 'MV': 21, 'MW': 31, 'MX': 32, 'MY': 16,
            'MZ': 11, 'NA': 14, 'NC': 0, 'NE': 8, 'NF': 0, 'NG': 37, 'NI': 17, 'NL': 18, 'NO': 13, 'NP': 7,
            'NR': 14, 'NU': 0, 'NZ': 17, 'OM': 11, 'PA': 14, 'PE': 26, 'PF': 0, 'PG': 22, 'PH': 99, 'PK': 7,
            'PL': 16, 'PM': 0, 'PN': 0, 'PR': 0, 'PS': 16, 'PT': 20, 'PW': 16, 'PY': 18, 'QA': 8, 'RE': 0,
            'RO': 42, 'RS': 32, 'RU': 83, 'RW': 5, 'SA': 13, 'SB': 10, 'SC': 27, 'SD': 18, 'SE': 21, 'SG': 5,
            'SH': 3, 'SI': 212, 'SJ': 0, 'SK': 8, 'SL': 5, 'SM': 9, 'SN': 14, 'SO': 18, 'SR': 10, 'SS': 10,
            'ST': 7, 'SV': 14, 'SX': 0, 'SY': 14, 'SZ': 4, 'TC': 0, 'TD': 23, 'TF': 0, 'TG': 5, 'TH': 78,
            'TJ': 5, 'TK': 0, 'TL': 13, 'TM': 6, 'TN': 24, 'TO': 5, 'TR': 81, 'TT': 15, 'TV': 8, 'TW': 22,
            'TZ': 31, 'UA': 27, 'UG': 139, 'UM': 9, 'US': 57, 'UY': 19, 'UZ': 14, 'VA': 0, 'VC': 6, 'VE': 25,
            'VG': 0, 'VI': 0, 'VN': 63, 'VU': 6, 'WF': 3, 'WS': 11, 'XK': 0, 'YE': 22, 'YT': 0, 'ZA': 9,
            'ZM': 10, 'ZW': 10
        }
#1.)
        for code, expected_count in expected_counts.items():
            actual_count = len(self.all_iso3166_2.all.get(code, []))
            self.assertEqual(actual_count, expected_count, 
                f"Incorrect subdivision total for code {code}. Expected {expected_count}, got {actual_count}.")

    # @unittest.skip("")
    def test_subdivision_codes(self):
        """ Testing functionality for getting list of all ISO 3166-2 subdivision codes. """
        expected_bq_subdivision_codes = ['BQ-BO', 'BQ-SA', 'BQ-SE']
        expected_sz_subdivision_codes = ['SZ-HH', 'SZ-LU', 'SZ-MA', 'SZ-SH']
        expected_sm_subdivision_codes = ['SM-01', 'SM-02', 'SM-03', 'SM-04', 'SM-05', 'SM-06', 'SM-07', 'SM-08', 'SM-09']
        expected_pw_subdivision_codes = ['PW-002', 'PW-004', 'PW-010', 'PW-050', 'PW-100', 'PW-150', 'PW-212', 'PW-214', \
                                         'PW-218', 'PW-222', 'PW-224', 'PW-226', 'PW-227', 'PW-228', 'PW-350', 'PW-370']
        expected_wf_subdivision_codes = ['WF-AL', 'WF-SG', 'WF-UV']
        expected_mg_sb_subdivision_codes = {"MG": ["MG-A", "MG-D", "MG-F", "MG-M", "MG-T", "MG-U"], 
                                            "SB": ["SB-CE", "SB-CH", "SB-CT", "SB-GU", "SB-IS", "SB-MK", "SB-ML", "SB-RB", "SB-TE", "SB-WE"]}
        expected_gnq_tca_subdivision_codes = {"GQ": ["GQ-AN", "GQ-BN", "GQ-BS", "GQ-C", "GQ-CS", "GQ-DJ", "GQ-I", "GQ-KN", "GQ-LI", "GQ-WN"], 
                                            "TC": []}
#1.)       
        test_iso3166_2_bg_instance = Subdivisions("BQ") #Bonaire, Sint Eustatius and Saba
        bq_subdivision_codes = test_iso3166_2_bg_instance.subdivision_codes() 
        self.assertEqual(bq_subdivision_codes, expected_bq_subdivision_codes, 
            f"Expected subdivision codes don't match output:\n{bq_subdivision_codes}.")
#2.)
        test_iso3166_2_sz_instance = Subdivisions("SZ") #Eswatini
        sz_subdivision_codes = test_iso3166_2_sz_instance.subdivision_codes() 
        self.assertEqual(sz_subdivision_codes, expected_sz_subdivision_codes, 
            f"Expected subdivision codes don't match output:\n{sz_subdivision_codes}.")
#3.)
        test_iso3166_2_sm_instance = Subdivisions("SMR") #San Marino
        sm_subdivision_codes = test_iso3166_2_sm_instance.subdivision_codes() 
        self.assertEqual(sm_subdivision_codes, expected_sm_subdivision_codes, 
            f"Expected subdivision codes don't match output:\n{sm_subdivision_codes}.")
#4.)
        test_iso3166_2_pw_instance = Subdivisions("PLW") #Palau
        pw_subdivision_codes = test_iso3166_2_pw_instance.subdivision_codes() 
        self.assertEqual(pw_subdivision_codes, expected_pw_subdivision_codes, 
            f"Expected subdivision codes don't match output:\n{pw_subdivision_codes}.")
#5.)   
        test_iso3166_2_wf_instance = Subdivisions("876") #Wallis and Futuna 
        wf_subdivision_codes = test_iso3166_2_wf_instance.subdivision_codes() 
        self.assertEqual(wf_subdivision_codes, expected_wf_subdivision_codes, 
            f"Expected subdivision codes don't match output:\n{wf_subdivision_codes}.")
#6.)   
        test_iso3166_2_mg_sb_instance = Subdivisions("MG, 090") #Madagascar, Solomon Islands
        mg_sb_subdivision_codes = test_iso3166_2_mg_sb_instance.subdivision_codes() 
        self.assertEqual(mg_sb_subdivision_codes, expected_mg_sb_subdivision_codes, 
            f"Expected subdivision codes don't match output:\n{mg_sb_subdivision_codes}.")   
#7.)   
        test_iso3166_2_gnq_tca_instance = Subdivisions("GNQ, TCA") #Equatorial Guinea, Turks and Caicos Islands
        gnq_tca_subdivision_codes = test_iso3166_2_gnq_tca_instance.subdivision_codes() 
        self.assertEqual(gnq_tca_subdivision_codes, expected_gnq_tca_subdivision_codes, 
            f"Expected subdivision codes don't match output:\n{gnq_tca_subdivision_codes}.")  
#8.)
        all_subdivision_codes = self.all_iso3166_2.subdivision_codes() 
        self.assertEqual(len(all_subdivision_codes), 250, f"Expected 250 total country objects in output, got {len(all_subdivision_codes)}.") 
        for key, val in all_subdivision_codes.items():
            self.assertIn(key, list(iso3166.countries_by_alpha2.keys()), f"Country code {key} not found in list of ISO 3166 alpha-2 codes.")
            self.assertIsInstance(val, list, f"Expected output of subdivision codes to be of type list, got {type(val)}.")
#9.)
        with (self.assertRaises(ValueError)):
            self.all_iso3166_2.subdivision_codes("ABCD")
            self.all_iso3166_2.subdivision_codes("Z")
            self.all_iso3166_2.subdivision_codes("1234")
            test_iso3166_2_bg_instance.subdivision_codes("AD")
            test_iso3166_2_sz_instance.subdivision_codes("KM")
            test_iso3166_2_wf_instance.subdivision_codes("090")

    # @unittest.skip("")
    def test_subdivision_names(self):
        """ Testing functionality for getting list of all ISO 3166-2 subdivision names. """
        expected_km_subdivision_names = ['Anjouan', 'Grande Comore', 'Mohéli']
        expected_er_subdivision_names = ['Al Awsaţ', 'Al Janūbī', 'Ansabā', 'Debubawi K’eyyĭḥ Baḥri', 'Gash-Barka', 'Semienawi K’eyyĭḥ Baḥri']
        expected_gl_subdivision_names = ['Avannaata Kommunia', 'Kommune Kujalleq', 'Kommune Qeqertalik', 'Kommuneqarfik Sermersooq', 'Qeqqata Kommunia']
        expected_ls_subdivision_names = ['Berea', 'Botha-Bothe', 'Leribe', 'Mafeteng', 'Maseru', "Mohale's Hoek", 'Mokhotlong', "Qacha's Nek", 'Quthing', 'Thaba-Tseka']
        expected_zm_subdivision_names = ['Central', 'Copperbelt', 'Eastern', 'Luapula', 'Lusaka', 'Muchinga', 'North-Western', 'Northern', 'Southern', 'Western']
        expected_ag_bn_subdivision_names = {"AG": ['Barbuda', 'Redonda', 'Saint George', 'Saint John', 'Saint Mary', 'Saint Paul', 'Saint Peter', 'Saint Philip'], 
                                            "BN": ['Belait', 'Brunei-Muara', 'Temburong', 'Tutong']}
        expected_dj_va_subdivision_names = {"DJ": ['Ali Sabieh', 'Arta', 'Dikhil', 'Djibouti', 'Obock', 'Tadjourah'], 
                                            "VA": []}
#1.)        
        test_iso3166_2_km_instance = Subdivisions("KM") #Comoros  
        km_subdivision_names = test_iso3166_2_km_instance.subdivision_names() 
        self.assertEqual(km_subdivision_names, expected_km_subdivision_names, 
            f"Expected subdivision names don't match output:\n{km_subdivision_names}.")
#2.)
        test_iso3166_2_er_instance = Subdivisions("ER") #Eritrea
        er_subdivision_names = test_iso3166_2_er_instance.subdivision_names() 
        self.assertEqual(er_subdivision_names, expected_er_subdivision_names, 
            f"Expected subdivision names don't match output:\n{er_subdivision_names}.")
#3.)
        test_iso3166_2_gl_instance = Subdivisions("GRL") #Greenland
        gl_subdivision_names = test_iso3166_2_gl_instance.subdivision_names() 
        self.assertEqual(gl_subdivision_names, expected_gl_subdivision_names, 
            f"Expected subdivision names don't match output:\n{gl_subdivision_names}.")
#4.)
        test_iso3166_2_ls_instance = Subdivisions("LSO") #Lesotho
        ls_subdivision_names = test_iso3166_2_ls_instance.subdivision_names() 
        self.assertEqual(ls_subdivision_names, expected_ls_subdivision_names, 
            f"Expected subdivision names don't match output:\n{ls_subdivision_names}.")
#5.)
        test_iso3166_2_zm_instance = Subdivisions("894") #Zambia
        zm_subdivision_names = test_iso3166_2_zm_instance.subdivision_names() 
        self.assertEqual(zm_subdivision_names, expected_zm_subdivision_names, 
            f"Expected subdivision names don't match output:\n{zm_subdivision_names}.")
#6.)
        test_iso3166_2_ag_bn_instance = Subdivisions("028, BN") #Antigua and Barbuda, Brunei
        ag_bn_subdivision_names = test_iso3166_2_ag_bn_instance.subdivision_names() 
        self.assertEqual(ag_bn_subdivision_names, expected_ag_bn_subdivision_names, 
            f"Expected subdivision names don't match output:\n{ag_bn_subdivision_names}.")
#7.)
        test_iso3166_2_dj_va_instance = Subdivisions("DJI, VAT") #Djibouti, Vatican City
        dj_va_subdivision_names = test_iso3166_2_dj_va_instance.subdivision_names() 
        self.assertEqual(dj_va_subdivision_names, expected_dj_va_subdivision_names, 
            f"Expected subdivision names don't match output:\n{dj_va_subdivision_names}.")
#8.)
        all_subdivision_names = self.all_iso3166_2.subdivision_names() 
        self.assertEqual(len(all_subdivision_names), 250, f"Expected 250 total country output objects, got {len(all_subdivision_names)}.")
        for key, val in all_subdivision_names.items():
            self.assertIn(key, list(iso3166.countries_by_alpha2.keys()), f"Country code {key} not found in list of ISO 3166 alpha-2 codes.")
            self.assertIsInstance(val, list, f"Expected output of subdivision names to be of type list, got {type(val)}.")
#9.)
        with (self.assertRaises(ValueError)):
            self.all_iso3166_2.subdivision_names("ABCD")
            self.all_iso3166_2.subdivision_names("Z")
            self.all_iso3166_2.subdivision_names("1234")
            self.all_iso3166_2.subdivision_names("blah, blah, blah")
            self.all_iso3166_2.subdivision_names(False)
            test_iso3166_2_km_instance.subdivision_names('ES')
            test_iso3166_2_er_instance.subdivision_names("DO")
            test_iso3166_2_zm_instance.subdivision_names("CPV")
            test_iso3166_2_dj_va_instance.subdivision_names("218")

    # @unittest.skip("") 
    def test_filter_attributes(self):
        """ Testing filter_attributes parameter that removes non-required attributes from subdivision object output."""
#1.)
        filter_subdivision_attributes_1 = Subdivisions(filter_attributes="flag, parentCode") #subdivision output should only include the flag and parentCode attributes 
        expected_attribute_list_1 = ["parentCode", "flag"]
        
        for alpha_code in filter_subdivision_attributes_1.all:
            for subd in filter_subdivision_attributes_1.all[alpha_code]:
                self.assertEqual(list(filter_subdivision_attributes_1.all[alpha_code][subd]), expected_attribute_list_1, 
                    f"Expected and observed list of subdivision attributes do not match:\n{list(filter_subdivision_attributes_1.all[alpha_code][subd])}.")
#2.)
        filter_subdivision_attributes_2 = Subdivisions(filter_attributes="type, name") #subdivision output should only include type and name attributes 
        expected_attribute_list_2 = ["name", "type"]

        for alpha_code in filter_subdivision_attributes_2.all:
            for subd in filter_subdivision_attributes_2.all[alpha_code]:
                self.assertEqual(list(filter_subdivision_attributes_2.all[alpha_code][subd]), expected_attribute_list_2, 
                    f"Expected and observed list of subdivision attributes do not match:\n{list(filter_subdivision_attributes_2.all[alpha_code][subd])}.")
#3.)
        filter_subdivision_attributes_3 = Subdivisions(filter_attributes="*") #subdivision output should include all attributes 
        expected_attribute_list_3 = ['name', 'localOtherName', 'type', 'parentCode', 'flag', 'latLng', 'history']
        
        for alpha_code in filter_subdivision_attributes_3.all:
            for subd in filter_subdivision_attributes_3.all[alpha_code]:
                self.assertEqual(list(filter_subdivision_attributes_3.all[alpha_code][subd]), expected_attribute_list_3, 
                    f"Expected and observed list of subdivision attributes do not match:\n{list(filter_subdivision_attributes_3.all[alpha_code][subd])}.")
#4.)
        with (self.assertRaises(ValueError)):
            filter_subdivision_attributes_5 = Subdivisions(filter_attributes="") 
            filter_subdivision_attributes_6 = Subdivisions(filter_attributes="flag, name, invalid_attribute1") 
            filter_subdivision_attributes_7 = Subdivisions(filter_attributes="invalid_attribute1, invalid_attribute2") 
            filter_subdivision_attributes_8 = Subdivisions(filter_attributes=123) 
            filter_subdivision_attributes_9 = Subdivisions(filter_attributes=False)

    # @unittest.skip("")
    def test_search(self):
        """ Testing searching by subdivision name functionality. """
        test_search_1 = "Monaghan" #IE-MN
        test_search_2 = "Olaines Novads" #LV-068
        test_search_3 = "Armagh City, Banbridge and Craigavon, Berlin" #GB-ABC, DE-BE
        test_search_4 = "North" 
        test_search_5 = "Saint George" #multiple subdivisons with this name
        test_search_6 = "область"  #Oblast in RU
        test_search_7 = ""
        test_search_8 = "zzzzzzzz"
        test_search_9 = "West Carolina"
        test_search_10 = True
        test_search_11 = 4.6
#1.)
        search_results_1 = self.all_iso3166_2.search(test_search_1, exclude_match_score=1) 
        expected_search_result_1 =  {
            'IE': {'IE-MN': {
                'name': 'Monaghan', 
                'localOtherName': 'Contae Mhuineacháin (gle), The Drumlin County (eng), The Farney County (eng)', 
                'type': 'County', 
                'parentCode': 'IE-U', 
                'flag': 'https://raw.githubusercontent.com/amckenna41/iso3166-flag-icons/main/iso3166-2-icons/IE/IE-MN.png', 
                'latLng': [54.249, -6.968], 
                'history': None
                }
            }
        }

        self.assertEqual(search_results_1, expected_search_result_1, f"Observed and expected output objects do not match:\n{search_results_1}.")
#2.)
        search_results_2 = self.all_iso3166_2.search(test_search_2, likeness_score=100)
        expected_search_result_2 = {
            'LV': {'LV-068': {
                'name': 'Olaines novads', 
                'localOtherName': 'Olaine Municipality (eng)', 
                'type': 'Municipality', 
                'parentCode': None, 
                'flag': 'https://raw.githubusercontent.com/amckenna41/iso3166-flag-icons/main/iso3166-2-icons/LV/LV-068.png', 
                'latLng': [56.787, 23.942], 
                'history': None
                }
            }
        }

        self.assertEqual(search_results_2, expected_search_result_2, f"Observed and expected output objects do not match:\n{search_results_2}.")
#3.)
        search_results_3 = self.all_iso3166_2.search(test_search_3, likeness_score=90, exclude_match_score=0)  #add Match Score to each search result output
        expected_search_result_3 = [
            {
                "Country Code": "GB",
                "Subdivision Code": "GB-ABC",
                "name": "Armagh City, Banbridge and Craigavon",
                "localOtherName": "'Ard Mhacha, Droichead na Banna agus Creag Abhann (gle)', 'Airmagh, Bannbrig an Craigavon (ulst1239)'",
                "type": "District",
                "parentCode": "GB-NIR",
                "flag": None,
                "latLng": [54.393, -6.456],
                "history": [
                    '2019-11-22: Change of subdivision name of GB-ABC, GB-DRS; modification of remark part 2; update list source. (Remark part 2: BS 6879 gives alternative name forms in Welsh (cy) for some of the Welsh unitary authorities (together with alternative code elements). Since this part of ISO 3166 does not allow for duplicate coding of identical subdivisions, such alternative names in Welsh and code elements are shown for information purposes only in square brackets after the English name of the subdivision. BS 6879 has been superseded but remains the original source of the codes. Included for completeness: EAW England and Wales; GBN Great Britain; UKM United Kingdom). Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:GB.', 
                    '2015-11-27: Deletion of district council areas GB-ANT, GB-ARD, GB-ARM, GB-BLA, GB-BLY, GB-BNB, GB-CKF, GB-CSR, GB-CLR, GB-CKT, GB-CGV, GB-DRY, GB-DOW, GB-DGN, GB-FER, GB-LRN, GB-LMV, GB-LSB, GB-MFT, GB-MYL, GB-NYM, GB-NTA, GB-NDN, GB-OMH, GB-STB; change of subdivision category from district council area to district GB-BFS; addition of districts GB-ANN, GB-AND, GB-ABC, GB-CCG, GB-DRS, GB-FMO, GB-LBC, GB-MEA, GB-MUL, GB-NMD; update List Source. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:GB.'
                    ],
                "Match Score": 100
            },
            {
                "Country Code": "DE",
                "Subdivision Code": "DE-BE",
                "name": "Berlin",
                "localOtherName": "Berlin (eng), Grey City (eng)",
                "type": "Land",
                "parentCode": None,
                "flag": "https://raw.githubusercontent.com/amckenna41/iso3166-flag-icons/main/iso3166-2-icons/DE/DE-BE.svg",
                "latLng": [52.52, 13.405],
                "history": None,
                "Match Score": 100
            }
        ]
    
        self.assertEqual(search_results_3, expected_search_result_3, f"Observed and expected output objects do not match:\n{search_results_3}.")
#4.)
        search_results_4 = self.all_iso3166_2.search(test_search_4, likeness_score=80) #North - likeness score of 80%
        expected_search_result_4 = {'CM': {'CM-NO': {'name': 'North', 'localOtherName': 'Nord (fra)', 'type': 'Region', 'parentCode': None, 'flag': None, 'latLng': [8.581, 13.914], 'history': None}}, 
                                    'GW': {'GW-N': {'name': 'Norte', 'localOtherName': 'North (eng)', 'type': 'Province', 'parentCode': None, 'flag': None, 'latLng': [11.804, -15.18], 'history': None}}}

        self.assertEqual(search_results_4, expected_search_result_4, f"Observed and expected output objects do not match:\n{search_results_4}.")
#5.)
        search_results_5 = self.all_iso3166_2.search(test_search_5, likeness_score=75, filter_attribute="localOtherName, name", local_other_name_search=True) #Saint George - filtering out all attributes except localOtherName and name & searching the localOtherName attribute to expand the search space
        expected_search_result_5 = {'AG': {'AG-03': {'name': 'Saint George', 'localOtherName': None}}, 
                                    'BB': {'BB-03': {'name': 'Saint George', 'localOtherName': None}}, 
                                    'DM': {'DM-04': {'name': 'Saint George', 'localOtherName': None}}, 
                                    'GD': {'GD-03': {'name': 'Saint George', 'localOtherName': 'The Cathedral Parish (eng)'}}, 
                                    'VC': {'VC-04': {'name': 'Saint George', 'localOtherName': None}}}          

        self.assertEqual(search_results_5, expected_search_result_5, f"Observed and expected output objects do not match:\n{search_results_5}.")
#6.)
        search_results_6 = self.all_iso3166_2.search(test_search_6, likeness_score=50, local_other_name_search=True) #область - searching the localOtherName attribute to expand the search space
        expected_search_result_6 = {}          
        self.assertEqual(search_results_6, expected_search_result_6, f"Observed and expected output objects do not match:\n{search_results_6}.")
#7.)
        search_results_7 = self.all_iso3166_2.search(test_search_7)
        self.assertEqual(search_results_7, {}, f"Expected output to be an empty dict, got {search_results_7}.")
#8.)
        search_results_8 = self.all_iso3166_2.search(test_search_8)
        self.assertEqual(search_results_8, {}, f"Expected output to be an empty dict, got {search_results_8}.")
#9.)
        search_results_9 = self.all_iso3166_2.search(test_search_9)
        self.assertEqual(search_results_9, {}, f"Expected output to be an empty dict, got {search_results_9}.")
#10.)
        with (self.assertRaises(TypeError)):
            self.all_iso3166_2.search(test_search_10)
            self.all_iso3166_2.search(test_search_11)

    # @unittest.skip("")
    def test_custom_subdivision(self):
        """ Testing custom_subdivision function that adds or deletes custom subdivisions to the main iso3166-2.json object,
            using a custom duplicated copy of the iso3166-2 object to not explicitly add/delete from it. """  
        #create hard copy of iso3166-2.json object for testing custom subdivision functionality on
        self.test_iso3166_2_copy = os.path.join(self.test_output_dir, "iso3166_2_copy.json")
        with open(self.test_iso3166_2_copy, "w") as output_json:
            json.dump(self.all_iso3166_2.all, output_json, ensure_ascii=False, indent=4)

        #class instance using duplicated ISO 3166-2 object
        all_iso3166_2_custom_subdivision = Subdivisions(iso3166_2_filepath=self.test_iso3166_2_copy)

        #add below test subdivisions to respective country objects
        all_iso3166_2_custom_subdivision.custom_subdivision("AD", "AD-ZZ", name="Bogus Subdivision", local_other_name="Bogus Subdivision", type_="District", lat_lng=[42.520, 1.657], parent_code=None, flag=None, save_new=1, save_new_filename=os.path.join(self.test_output_dir, "iso3166_2_custom_ad_zz.json"))
        all_iso3166_2_custom_subdivision.custom_subdivision("DE", "DE-100", name="Made up subdivision", local_other_name="Made up subdivision", type_="Land", lat_lng=[48.84, 11.479], parent_code=None, flag=None, save_new=1, save_new_filename=os.path.join(self.test_output_dir, "iso3166_2_custom_de_100.json"))
        all_iso3166_2_custom_subdivision.custom_subdivision("GY", "GY-ABC", name="New Guyana subdivision", local_other_name="New Guyana subdivision", type_="Region", lat_lng=[6.413, -60.123], parent_code=None, flag=None, history="blahblahblah", save_new=1, save_new_filename=os.path.join(self.test_output_dir, "iso3166_2_custom_gy_abc.json"))
        all_iso3166_2_custom_subdivision.custom_subdivision("ZA", "ZA-123", name="Zambian province", local_other_name="Zambian province", type_="Province", lat_lng=[-28.140, 26.777], parent_code=None, flag=None, history="historical subdivision updates", save_new=1, save_new_filename=os.path.join(self.test_output_dir, "iso3166_2_custom_za_123.json"))
        all_iso3166_2_custom_subdivision.custom_subdivision("IE", "IE-BF", name="Belfast", local_other_name="Béal Feirste", type_="Province", lat_lng=[54.596, -5.931], parent_code=None, flag=None, custom_attributes={"population": "345,318", "area": "115Km2"}, save_new=1, save_new_filename=os.path.join(self.test_output_dir, "iso3166_2_custom_ie_bf.json"))
        all_iso3166_2_custom_subdivision.custom_subdivision("RU", "RU-ASK", name="Alaska Oblast", local_other_name="Аляска", type_="Republic", lat_lng=[63.588, 154.493], parent_code=None, flag=None, custom_attributes={"population": "733,583", "gini": "0.43", "gdpPerCapita": "71,996"}, save_new=1, save_new_filename=os.path.join(self.test_output_dir, "iso3166_2_custom_ru_ask.json"))
#1.)    
        self.assertEqual(all_iso3166_2_custom_subdivision.all["AD"]["AD-ZZ"], {'flag': None, 'latLng': [42.52, 1.657], 'name': 'Bogus Subdivision', 'localOtherName': 'Bogus Subdivision', 'parentCode': None, 'type': 'District', 'history': None},
            f"Expected dict for custom AD-ZZ subdivision does not match output:\n{all_iso3166_2_custom_subdivision.all['AD']['AD-ZZ']}.")
#2.)
        self.assertEqual(all_iso3166_2_custom_subdivision.all["DE"]["DE-100"], {'flag': None, 'latLng': [48.84, 11.479], 'name': 'Made up subdivision', 'localOtherName': 'Made up subdivision', 'parentCode': None, 'type': 'Land', 'history': None},
            f"Expected dict for custom DE-100 subdivision does not match output:\n{all_iso3166_2_custom_subdivision.all['DE']['DE-100']}.")
#3.)
        self.assertEqual(all_iso3166_2_custom_subdivision.all["GY"]["GY-ABC"], {'flag': None, 'latLng': [6.413, -60.123], 'name': 'New Guyana subdivision', 'localOtherName': 'New Guyana subdivision', 'parentCode': None, 'type': 'Region', "history": "blahblahblah"},
            f"Expected dict for custom GY-ABC subdivision does not match output:\n{all_iso3166_2_custom_subdivision.all['GY']['GY-ABC']}.")
#4.)
        self.assertEqual(all_iso3166_2_custom_subdivision.all["ZA"]["ZA-123"], {'flag': None, 'latLng': [-28.14, 26.777], 'name': 'Zambian province', 'localOtherName': 'Zambian province', 'parentCode': None, 'type': 'Province', "history": "historical subdivision updates"},
            f"Expected dict for custom ZA-123 subdivision does not match output:\n{all_iso3166_2_custom_subdivision.all['ZA']['ZA-123']}.")
#5.)
        self.assertEqual(all_iso3166_2_custom_subdivision.all["IE"]["IE-BF"], {'flag': None, 'latLng': [54.596, -5.931], 'name': 'Belfast', 'localOtherName': 'Béal Feirste', 'parentCode': None, 'type': 'Province', "population": "345,318", "area": "115Km2", "history": None},
            f"Expected dict for custom IE-BF subdivision does not match output:\n{all_iso3166_2_custom_subdivision.all['IE']['IE-BF']}.")
#6.)
        self.assertEqual(all_iso3166_2_custom_subdivision.all["RU"]["RU-ASK"], {'flag': None, 'gdpPerCapita': '71,996', 'gini': '0.43', 'latLng': [63.588, 154.493], 'localOtherName': 'Аляска', 'name': 'Alaska Oblast', 'parentCode': None, 'population': '733,583', 'type': 'Republic', "history": None},
            f"Expected dict for custom RU-ASK subdivision does not match output:\n{all_iso3166_2_custom_subdivision.all['RU']['RU-ASK']}.")

        #delete above custom subdivisions
        all_iso3166_2_custom_subdivision.custom_subdivision("AD", subdivision_code="AD-ZZ", delete=1)
        all_iso3166_2_custom_subdivision.custom_subdivision("DE", subdivision_code="DE-100", delete=1)
        all_iso3166_2_custom_subdivision.custom_subdivision("GY", subdivision_code="GY-ABC", delete=1)
        all_iso3166_2_custom_subdivision.custom_subdivision("ZA", subdivision_code="ZA-123", delete=1)
        all_iso3166_2_custom_subdivision.custom_subdivision("IE", subdivision_code="IE-BF", delete=1)
        all_iso3166_2_custom_subdivision.custom_subdivision("RU", subdivision_code="RU-ASK", delete=1)

        #reinstantiating instance of class with above custom subdivisions deleted
        all_iso3166_2_custom_subdivision = Subdivisions(iso3166_2_filepath=self.test_iso3166_2_copy)
#7.)
        self.assertNotIn("AD-ZZ", list(all_iso3166_2_custom_subdivision.all["AD"].keys()), "Custom AD-ZZ subdivision should not be in object for AD.")
#8.)
        self.assertNotIn("DE-100", list(all_iso3166_2_custom_subdivision.all["DE"].keys()), "Custom DE-100 subdivision should not be in object for DE.")
#9.)
        self.assertNotIn("GY-ABC", list(all_iso3166_2_custom_subdivision.all["GY"].keys()), "Custom GY-ABC subdivision should not be in object for GY.")
#9.)
        self.assertNotIn("ZA-123", list(all_iso3166_2_custom_subdivision.all["ZA"].keys()), "Custom ZA-123 subdivision should not be in object for ZA.")
#10.)
        self.assertNotIn("IE-BF", list(all_iso3166_2_custom_subdivision.all["IE"].keys()), "Custom IE-BF subdivision should not be in object for IE.")
#11.)
        self.assertNotIn("RU-ASK", list(all_iso3166_2_custom_subdivision.all["RU"].keys()), "Custom RU-ASK subdivision should not be in object for RU.")
#12.)
        with self.assertRaises(ValueError):
            all_iso3166_2_custom_subdivision.custom_subdivision("IE", "IE-CN")
            all_iso3166_2_custom_subdivision.custom_subdivision("JM", "JM-01")
            all_iso3166_2_custom_subdivision.custom_subdivision("TV", "TV-NIT")
            all_iso3166_2_custom_subdivision.custom_subdivision("UZ", "UZ-AN")
            all_iso3166_2_custom_subdivision.custom_subdivision("ABC", "blah")
            all_iso3166_2_custom_subdivision.custom_subdivision("ZZ", "blahblahblah")
            all_iso3166_2_custom_subdivision.custom_subdivision("123", "idfuiwf")
#13.)
        with self.assertRaises(TypeError):
            all_iso3166_2_custom_subdivision.custom_subdivision(123, 10.5)
            all_iso3166_2_custom_subdivision.custom_subdivision(name=False)
            all_iso3166_2_custom_subdivision.custom_subdivision("AD", "AD-01", type=123)

    @unittest.skip("")
    def test_check_for_updates(self):
        """ Testing functionality that compares current iso3166-2 object with latest object on repo. """
        self.all_iso3166_2.check_for_updates()

    # @unittest.skip("")
    def test_len(self):
        """ Testing length functionality that outputs the total number of subdivision objects. """
        self.assertEqual(len(self.all_iso3166_2.all), 250, f"Expected the length of subdivisions object to be 250, got {len(self.all_iso3166_2.all)}.")

    # @unittest.skip("")
    def test_str(self):
        """ Testing __str__ function returns correct string representation for class object. """
        self.assertEqual(str(self.all_iso3166_2), f"Instance of Subdivisions class. Path: {self.all_iso3166_2.iso3166_2_module_path}, Version {self.all_iso3166_2.__version__}.", 
                f"Expected and observed string output for class instance do not match:\n{str(self.all_iso3166_2)}.")
        
    # @unittest.skip("")
    def test_repr(self):
        """ Testing __repr__ function returns correct object representation for class object. """
        self.assertEqual(repr(self.all_iso3166_2), "<iso3166-2(version=1.7.1, total_subdivisions=5049, source_file=iso3166-2.json)>",
                f"Expected and observed object representation for class instance do not match:\n{repr(self.all_iso3166_2)}.")

    # @unittest.skip("")
    def test_sizeof(self):
        """ Testing __sizeof__ function returns correct output for class object. """
        self.assertEqual(self.all_iso3166_2.__sizeof__(), 2.815, f"Expected and observed output for sizeof function do not match:\n{self.all_iso3166_2.__sizeof__()}.")

    @classmethod
    def tearDown(self):
        """ Delete any test json folders and objects . """
        #remove the temp dir created to store duplicate of iso3166-2 object before any changes were made using the add_subdivision() function,
        #a successful pass of all the above test cases mean there are no errors on the current object and the archive folder can be deleted
        shutil.rmtree(self.test_output_dir)
        if (os.path.isdir("archive-iso3166-2")):
            shutil.rmtree(self.test_output_dir)
        
        #delete object holding all ISO 3166-2 data
        del self.all_iso3166_2
            
if __name__ == '__main__':
    #run all unit tests
    unittest.main(verbosity=2)    