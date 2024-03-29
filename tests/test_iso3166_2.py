from iso3166_2 import *
import iso3166
import requests
import getpass
import json
import os
import shutil
from importlib.metadata import metadata
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

class ISO3166_2_Tests(unittest.TestCase):
    """
    Test suite for testing the iso3166-2 Python software package. 

    Test Cases
    ==========
    test_iso3166_2_metadata:
        testing correct software metdata for the iso3166-2 package. 
    test_iso3166_2:
        testing correct data returned from the ISO3166_2 class of the iso3166-2 package.  
    test_iso3166_2_json:
        testing correct objects are returned from the ISO 3166-2 JSON, using a variety of inputs.
    test_subdivision_names:
        testing correct ISO 3166-2 subdivision names are returned from the subdivision_names() class function.
    test_subdivision_codes:
        testing correct ISO 3166-2 subdivision codes are returned from the subdivision_codes() class function.  
    test_custom_subdivision:
        testing custom_subdivision function that adds or deletes custom subdivisions to the main iso3166-2.json object.  
    test_search:
        testing searching by subdivision name functionality.
    """
    def setUp(self):
        """ Initialise test variables, import json. """
        #initalise User-agent header for requests library 
        self.__version__ = metadata('iso3166-2')['version']
        self.user_agent_header = {'User-Agent': 'iso3166-2/{} ({}; {})'.format(self.__version__,
                                            'https://github.com/amckenna41/iso3166-2', getpass.getuser())}
    
        #base url for flag icons on iso3166-flag-icons repo
        self.flag_icons_base_url = "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/"

        #list of data attributes for main iso3166-2 json
        self.correct_output_attributes = ['name', 'localName', 'type', 'parentCode', 'latLng', 'flagUrl']

        #class instance with all ISO 3166-2 data
        self.all_iso3166_2 = ISO3166_2()

        #create test output directory - remove if already present
        self.test_output_dir = "test_output"
        if (os.path.isdir(self.test_output_dir)):
            shutil.rmtree(self.test_output_dir)
        os.mkdir(self.test_output_dir)

    def test_iso3166_2_metadata(self): 
        """ Testing correct iso3166-2 software version and metadata. """
        # self.assertEqual(metadata('iso3166-2')['version'], "1.5.4", 
        #     "iso3166-2 version is not correct, expected 1.5.4, got {}.".format(metadata('iso3166-2')['version']))
        self.assertEqual(metadata('iso3166-2')['name'], "iso3166-2", 
            "iso3166-2 software name is not correct, expected iso3166-2, got {}.".format(metadata('iso3166-2')['name']))
        self.assertEqual(metadata('iso3166-2')['author'], "AJ McKenna", 
            "iso3166-2 author is not correct, expected AJ McKenna, got {}.".format(metadata('iso3166-2')['author']))
        self.assertEqual(metadata('iso3166-2')['author-email'], "amckenna41@qub.ac.uk", 
            "iso3166-2 author email is not correct, expected amckenna41@qub.ac.uk, got {}.".format(metadata('iso3166-2')['author-email']))
        self.assertEqual(metadata('iso3166-2')['summary'], "A lightweight Python package, and accompanying API, that can be used to access all of the world's most up-to-date and accurate ISO 3166-2 subdivision data, including: name, local name, code, parent code, type, latitude/longitude and flag.", 
            "iso3166-2 package summary is not correct, got: {}.".format(metadata('iso3166-2')['summary']))
        self.assertEqual(metadata('iso3166-2')['keywords'], "iso,iso3166,beautifulsoup,python,pypi,countries,country codes,iso3166-2,iso3166-1,alpha-2,iso3166-updates,subdivisions,regions",
            "iso3166-2 keywords are not correct, got:\n{}.".format(metadata('iso3166-2')['keywords']))
        self.assertEqual(metadata('iso3166-2')['home-page'], "https://iso3166-2-api.vercel.app/api", 
            "iso3166-2 home page url is not correct, expected https://iso3166-2-api.vercel.app/api, got {}.".format(metadata('iso3166-2')['home-page']))
        self.assertEqual(metadata('iso3166-2')['maintainer'], "AJ McKenna", 
            "iso3166-2 maintainer is not correct, expected AJ McKenna, got {}.".format(metadata('iso3166-2')['maintainer']))
        self.assertEqual(metadata('iso3166-2')['license'], "MIT", 
            "iso3166-2 license type is not correct, expected MIT, got {}.".format(metadata('iso3166-2')['license']))

    def test_iso3166_2(self):
        """ Test ISO 3166-2 class and its methods and attributes. """
        self.assertIsInstance(self.all_iso3166_2.all, dict,
            "Expected ISO 3166-2 data object to be a dict, got {}.".format(type(self.all_iso3166_2.all)))
        self.assertEqual(len(self.all_iso3166_2.all), 250, 
            "Expected 250 countrys in ISO 3166-2 data object, got {}.".format(len(self.all_iso3166_2.all)))       
        self.assertIsInstance(self.all_iso3166_2.attributes, list, 
            "Expected attributes class variable to be a list, got {}.".format(type(self.all_iso3166_2.attributes)))
        self.assertEqual(set(self.all_iso3166_2.attributes), set(self.correct_output_attributes), 
            "List of attributes in class do not match expected, got:\n{}.".format(self.all_iso3166_2.attributes))
        # self.assertIsInstance(self.all_iso3166_2.alpha_2, list, 
        #     "Expected alpha-2 attribute to be a list, got {}.".format(type(self.all_iso3166_2.alpha_2)))
        # self.assertEqual(len(self.all_iso3166_2.alpha_2), 250, 
        #     "Expected 250 alpha-2 codes, got {}.".format(len(self.all_iso3166_2.alpha_2)))
        # for code in self.all_iso3166_2.all:
        #     self.assertIn(code, self.all_iso3166_2.alpha_2,
        #         "Alpha-2 code {} not found in list of available 2 letter codes.".format(code))
        # self.assertIsInstance(self.all_iso3166_2.alpha_3, list, 
        #     "Expected alpha-3 attribute to be a list, got {}.".format(type(self.all_iso3166_2.alpha_3)))
        # self.assertEqual(len(self.all_iso3166_2.alpha_3), 250, 
        #     "Expected 250 alpha-3 codes, got {}.".format(len(self.all_iso3166_2.alpha_3)))
        # self.assertIsInstance(self.all_iso3166_2.numeric, list, 
        #     "Expected numeric attribute to be a list, got {}.".format(type(self.all_iso3166_2.numeric)))
        # self.assertEqual(len(self.all_iso3166_2.numeric), 250, 
        #     "Expected 250 numeric codes, got {}.".format(len(self.all_iso3166_2.numeric)))
        
    def test_iso3166_2_json(self):
        """ Testing ISO 3166-2 JSON contents and data. """ 
        test_alpha_ba = self.all_iso3166_2["BA"] #Bosnia and Herzegovina
        test_alpha_cy = self.all_iso3166_2["CY"] #Cyprus
        test_alpha_gab = self.all_iso3166_2["GAB"] #Gabon
        test_alpha_rw_548 = self.all_iso3166_2["RW, 548"] #Rwanda, Vanuatu
        test_alpha_gg_kwt_670 = self.all_iso3166_2["GG, KWT, 670"] #Guernsey, Kuwait, St Vincent & the Grenadines
#1.)    
        ba_subdivision_codes = ['BA-BIH', 'BA-BRC', 'BA-SRP']
        ba_subdivision_names = ['Federacija Bosne i Hercegovine', 'Brčko distrikt', 'Republika Srpska']

        self.assertIsInstance(test_alpha_ba, dict, "Expected output object to be of type dict, got {}.".format(type(test_alpha_ba)))
        self.assertEqual(len(test_alpha_ba), 3, "Expected 3 total subdivision outputs, got {}.".format(len(test_alpha_ba)))
        self.assertEqual(list(test_alpha_ba.keys()), ba_subdivision_codes, "Subdivison codes do not equal expected codes:\n{}.".format(list(test_alpha_ba.keys())))
        self.assertEqual(list(test_alpha_ba['BA-BIH'].keys()), ['name', 'localName', 'type', 'parentCode', 'flagUrl', 'latLng'], "Expected keys for output dict don't match\n{}.".format(list(test_alpha_ba['BA-BIH'].keys())))
        for key in test_alpha_ba:
            self.assertIn(test_alpha_ba[key].name, ba_subdivision_names, "Subdivision name {} not found in list of subdivision names:\n{}.".format(test_alpha_ba[key].name, ba_subdivision_names))
            if (not (test_alpha_ba[key].flagUrl is None) and (test_alpha_ba[key].flagUrl != "")):
                self.assertEqual(requests.get(test_alpha_ba[key].flagUrl, headers=self.user_agent_header).status_code, 200, "Flag URL invalid: {}.".format(test_alpha_ba[key].flagUrl))
            if not (test_alpha_ba[key]["parentCode"] is None):
                self.assertIn(test_alpha_ba[key]["parentCode"], list(test_alpha_ba[key].keys()), 
                    "Parent code {} not found in list of subdivision codes:\n.".format(test_alpha_ba[key]["parentCode"], list(test_alpha_ba[key].keys())))    
            self.assertEqual(len(test_alpha_ba[key].latLng), 2, "Expected key should have both lat/longitude.")        
#2.)
        cy_subdivision_codes = ['CY-01', 'CY-02', 'CY-03', 'CY-04', 'CY-05', 'CY-06']
        cy_subdivision_names = ['Lefkosia', 'Lemesos', 'Larnaka', 'Ammochostos', 'Baf', 'Girne']
        
        self.assertIsInstance(test_alpha_cy, dict,  "Expected output object to be of type dict, got {}.".format(type(test_alpha_cy)))
        self.assertEqual(len(test_alpha_cy), 6, "Expected 6 total subdivision outputs, got {}.".format(len(test_alpha_cy)))
        self.assertEqual(list(test_alpha_cy.keys()), cy_subdivision_codes, "Subdivison codes do not equal expected codes:\n{}.".format(list(test_alpha_cy.keys())))
        self.assertEqual(list(test_alpha_cy['CY-01'].keys()), ['name', 'localName', 'type', 'parentCode', 'flagUrl', 'latLng'], "Expected keys for output dict don't match\n{}.".format(list(test_alpha_cy['CY-01'].keys())))
        for key in test_alpha_cy:
            self.assertIn(test_alpha_cy[key].name, cy_subdivision_names, "Subdivision name {} not found in list of subdivision names:\n{}.".format(test_alpha_cy[key].name, cy_subdivision_names))
            if (not (test_alpha_cy[key].flagUrl is None) and (test_alpha_cy[key].flagUrl != "")):
                self.assertEqual(requests.get(test_alpha_cy[key].flagUrl, headers=self.user_agent_header).status_code, 200, "Flag URL invalid: {}.".format(test_alpha_cy[key].flagUrl))
            if not (test_alpha_cy[key]["parentCode"] is None):
                self.assertIn(test_alpha_cy[key]["parentCode"], list(test_alpha_cy[key].keys()), 
                    "Parent code {} not found in list of subdivision codes:\n.".format(test_alpha_cy[key]["parentCode"], list(test_alpha_cy[key].keys())))    
            self.assertEqual(len(test_alpha_cy[key].latLng), 2, "Expected key should have both lat/longitude.")              
#3.)
        ga_subdivision_codes = ['GA-1', 'GA-2', 'GA-3', 'GA-4', 'GA-5', 'GA-6', 'GA-7', 'GA-8', 'GA-9'] 
        ga_subdivision_names = ['Estuaire', 'Haut-Ogooué', 'Moyen-Ogooué', 'Ngounié', 'Nyanga', 'Ogooué-Ivindo', 
            'Ogooué-Lolo', 'Ogooué-Maritime', 'Woleu-Ntem']

        self.assertIsInstance(test_alpha_gab, dict,  "Expected output object to be of type dict, got {}.".format(type(test_alpha_gab)))
        self.assertEqual(len(test_alpha_gab), 9, "Expected 9 total subdivision outputs, got {}.".format(len(test_alpha_gab)))
        self.assertEqual(list(test_alpha_gab.keys()), ga_subdivision_codes, "Subdivison codes do not equal expected codes:\n{}.".format(list(test_alpha_gab.keys())))
        self.assertEqual(list(test_alpha_gab['GA-1'].keys()), ['name', 'localName', 'type', 'parentCode', 'flagUrl', 'latLng'], "Expected keys for output dict don't match\n{}.".format(list(test_alpha_gab['GA-1'].keys())))
        for key in test_alpha_gab:
            self.assertIn(test_alpha_gab[key].name, ga_subdivision_names, "Subdivision name {} not found in list of subdivision names:\n{}.".format(test_alpha_gab[key].name, ga_subdivision_names))
            if (not (test_alpha_gab[key].flagUrl is None) and (test_alpha_gab[key].flagUrl != "")):
                self.assertEqual(requests.get(test_alpha_gab[key].flagUrl, headers=self.user_agent_header).status_code, 200, "Flag URL invalid: {}.".format(test_alpha_gab[key].flagUrl))
            if not (test_alpha_gab[key]["parentCode"] is None):
                self.assertIn(test_alpha_gab[key]["parentCode"], list(test_alpha_gab[key].keys()), 
                    "Parent code {} not found in list of subdivision codes:\n.".format(test_alpha_gab[key]["parentCode"], list(test_alpha_gab[key].keys())))    
            self.assertEqual(len(test_alpha_gab[key].latLng), 2, "Expected key should have both lat/longitude.")        
#4.)
        rw_subdivision_codes = ['RW-01', 'RW-02', 'RW-03', 'RW-04', 'RW-05']
        vu_subdivision_codes = ['VU-MAP', 'VU-PAM', 'VU-SAM', 'VU-SEE', 'VU-TAE', 'VU-TOB']
        rw_subdivision_names = ['City of Kigali', 'Eastern', 'Northern', 'Western', 'Southern']
        vu_subdivision_names = ['Malampa', 'Pénama', 'Sanma', 'Shéfa', 'Taféa', 'Torba']

        self.assertIsInstance(test_alpha_rw_548, dict,  "Expected output object to be of type dict, got {}.".format(type(test_alpha_rw_548)))
        self.assertEqual(list(test_alpha_rw_548.keys()), ['RW', 'VU'], "Expected output keys to be RW and VU, got {}.".format(list(test_alpha_rw_548.keys())))
        self.assertEqual(len(test_alpha_rw_548["RW"]), 5, "Expected 5 total subdivision outputs, got {}.".format(len(test_alpha_rw_548["RW"])))
        self.assertEqual(len(test_alpha_rw_548["VU"]), 6, "Expected 6 total subdivision outputs, got {}.".format(len(test_alpha_rw_548["VU"])))
        self.assertEqual(list(test_alpha_rw_548["RW"].keys()), rw_subdivision_codes, "Subdivison codes do not equal expected codes:\n{}.".format(list(test_alpha_rw_548["RW"].keys())))
        self.assertEqual(list(test_alpha_rw_548["VU"].keys()), vu_subdivision_codes, "Subdivison codes do not equal expected codes:\n{}.".format(list(test_alpha_rw_548["VU"].keys())))
        self.assertEqual(list(test_alpha_rw_548["RW"]['RW-01'].keys()), ['name', 'localName', 'type', 'parentCode', 'flagUrl', 'latLng'], "Expected keys for output dict don't match\n{}.".format(list(test_alpha_rw_548["RW"]['RW-01'].keys())))
        self.assertEqual(list(test_alpha_rw_548["VU"]['VU-MAP'].keys()), ['name', 'localName', 'type', 'parentCode', 'flagUrl', 'latLng'], "Expected keys for output dict don't match\n{}.".format(list(test_alpha_rw_548["VU"]['VU-MAP'].keys())))
        for key in list(test_alpha_rw_548["RW"].keys()):
            self.assertIn(test_alpha_rw_548["RW"][key].name, rw_subdivision_names, "Subdivision name {} not found in list of subdivision names:\n{}.".format(test_alpha_rw_548["RW"][key].name, rw_subdivision_names))
            if (not (test_alpha_rw_548["RW"][key].flagUrl is None) and (test_alpha_rw_548["RW"][key].flagUrl != "")):
                self.assertEqual(requests.get(test_alpha_rw_548["RW"][key].flagUrl, headers=self.user_agent_header).status_code, 200, "Flag URL invalid: {}.".format(test_alpha_rw_548["RW"][key].flagUrl))
            self.assertEqual(len(test_alpha_rw_548["RW"][key].latLng), 2, "Expected key should have both lat/longitude.")        
        for key in list(test_alpha_rw_548["VU"].keys()):
            self.assertIn(test_alpha_rw_548["VU"][key].name, vu_subdivision_names, "Subdivision name {} not found in list of subdivision names:\n{}.".format(test_alpha_rw_548["VU"][key].name, vu_subdivision_names))
            if (not (test_alpha_rw_548["VU"][key].flagUrl is None) and (test_alpha_rw_548["VU"][key].flagUrl != "")):
                self.assertEqual(requests.get(test_alpha_rw_548["VU"][key].flagUrl, headers=self.user_agent_header).status_code, 200, "Flag URL invalid: {}.".format(test_alpha_rw_548["VU"][key].flagUrl))
            self.assertEqual(len(test_alpha_rw_548["VU"][key].latLng), 2, "Expected key should have both lat/longitude.")              
#5.)
        kw_subdivision_codes = ['KW-AH', 'KW-FA', 'KW-HA', 'KW-JA', 'KW-KU', 'KW-MU']
        kw_subdivision_names = ['Al Aḩmadī', 'Al Farwānīyah', 'Ḩawallī', "Al Jahrā’", "Al ‘Āşimah", 'Mubārak al Kabīr']
        vc_subdivision_codes = ['VC-01', 'VC-02', 'VC-03', 'VC-04', 'VC-05', 'VC-06']
        vc_subdivision_names = ['Charlotte', 'Saint Andrew', 'Saint David', 'Saint George', 'Saint Patrick', 'Grenadines']
        
        self.assertIsInstance(test_alpha_gg_kwt_670, dict, "Expected output object to be of type dict, got {}.".format(type(test_alpha_gg_kwt_670)))
        self.assertEqual(list(test_alpha_gg_kwt_670.keys()), ['GG', 'KW', 'VC'], "Expected output keys to be GG, KW and VC, got {}.".format(list(test_alpha_gg_kwt_670.keys())))
        self.assertEqual(len(test_alpha_gg_kwt_670["GG"]), 0, "Expected 0 total subdivision outputs, got {}.".format(len(test_alpha_gg_kwt_670["GG"])))
        self.assertEqual(len(test_alpha_gg_kwt_670["KW"]), 6, "Expected 6 total subdivision outputs, got {}.".format(len(test_alpha_gg_kwt_670["KW"])))
        self.assertEqual(len(test_alpha_gg_kwt_670["VC"]), 6, "Expected 6 total subdivision outputs, got {}.".format(len(test_alpha_gg_kwt_670["VC"])))
        self.assertEqual(list(test_alpha_gg_kwt_670["GG"].keys()), [], "Expected no subdivision codes, got {}.".format(list(test_alpha_gg_kwt_670["GG"].keys())))
        self.assertEqual(list(test_alpha_gg_kwt_670["KW"].keys()), kw_subdivision_codes, "Subdivison codes do not equal expected codes:\n{}.".format(list(test_alpha_gg_kwt_670["KW"].keys())))
        self.assertEqual(list(test_alpha_gg_kwt_670["VC"].keys()), vc_subdivision_codes, "Subdivison codes do not equal expected codes:\n{}.".format(list(test_alpha_gg_kwt_670["VC"].keys())))
        self.assertEqual(list(test_alpha_gg_kwt_670["KW"]['KW-AH'].keys()), ['name', 'localName', 'type', 'parentCode', 'flagUrl', 'latLng'], 
            "Expected keys do not match output:\n{}.".format(list(test_alpha_gg_kwt_670["KW"]['KW-AH'].keys())))
        self.assertEqual(list(test_alpha_gg_kwt_670["VC"]['VC-01'].keys()), ['name', 'localName', 'type', 'parentCode', 'flagUrl', 'latLng'],
            "Expected keys do not match output:\n{}.".format(list(test_alpha_gg_kwt_670["VC"]['VC-01'].keys())))
        for key in list(test_alpha_gg_kwt_670["KW"].keys()):
            self.assertIn(test_alpha_gg_kwt_670["KW"][key].name, kw_subdivision_names, "Subdivision name {} not found in list of subdivision names:\n{}.".format(test_alpha_gg_kwt_670["KW"][key].name, kw_subdivision_names))
            if (not (test_alpha_gg_kwt_670["KW"][key].flagUrl is None) and (test_alpha_gg_kwt_670["KW"][key].flagUrl != "")):
                self.assertEqual(requests.get(test_alpha_gg_kwt_670["KW"][key].flagUrl, headers=self.user_agent_header).status_code, 200, "Flag URL invalid: {}.".format(test_alpha_gg_kwt_670["KW"][key].flagUrl))
            self.assertEqual(len(test_alpha_gg_kwt_670["KW"][key].latLng), 2, "Expected key should have both lat/longitude.")        
        for key in list(test_alpha_gg_kwt_670["VC"].keys()):
            self.assertIn(test_alpha_gg_kwt_670["VC"][key].name, vc_subdivision_names, "Subdivision name {} not found in list of subdivision names:\n{}.".format(test_alpha_gg_kwt_670["VC"][key].name, vc_subdivision_names))
            if (not (test_alpha_gg_kwt_670["VC"][key].flagUrl is None) and (test_alpha_gg_kwt_670["VC"][key].flagUrl != "")):
                self.assertEqual(requests.get(test_alpha_gg_kwt_670["VC"][key].flagUrl, headers=self.user_agent_header).status_code, 200, "Flag URL invalid: {}.".format(test_alpha_gg_kwt_670["VC"][key].flagUrl))
            self.assertEqual(len(test_alpha_gg_kwt_670["VC"][key].latLng), 2, "Expected key should have both lat/longitude.")        
#6.)
        for country in self.all_iso3166_2.all:              #testing that all subdivisions have a subdivision name, local name, type and lat/lng value
            for subd in self.all_iso3166_2.all[country]:
                self.assertTrue((self.all_iso3166_2.all[country][subd]["name"] != "" and self.all_iso3166_2.all[country][subd]["name"] != []), "")
                self.assertTrue((self.all_iso3166_2.all[country][subd]["localName"] != "" and self.all_iso3166_2.all[country][subd]["localName"] != []), "")
                self.assertTrue((self.all_iso3166_2.all[country][subd]["type"] != "" and self.all_iso3166_2.all[country][subd]["type"] != []), "")
                self.assertTrue((self.all_iso3166_2.all[country][subd]["latLng"] != "" and self.all_iso3166_2.all[country][subd]["latLng"] != []), "")
#7.)
        with (self.assertRaises(ValueError)):
            ISO3166_2("ZZ")
            ISO3166_2("XY")
            ISO3166_2("XYZ")
            ISO3166_2("AB, CD, EF")
            ISO3166_2("56789")
            self.all_iso3166_2["ZZ"]
            self.all_iso3166_2["XY"]
            self.all_iso3166_2["XYZ"]
            self.all_iso3166_2["AB, CD, EF"]
#11.)
        with (self.assertRaises(TypeError)):
            self.all_iso3166_2[123]
            self.all_iso3166_2[0.5]
            self.all_iso3166_2[False]

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
        bg_instance = ISO3166_2("BQ") #Bonaire, Sint Eustatius and Saba
        bq_subdivision_codes = bg_instance.subdivision_codes() 
        self.assertEqual(bq_subdivision_codes, expected_bq_subdivision_codes, "Expected subdivison codes don't match output:\n{}.".format(expected_bq_subdivision_codes))
#2.)
        sz_instance = ISO3166_2("SZ") #Eswatini
        sz_subdivision_codes = sz_instance.subdivision_codes() 
        self.assertEqual(sz_subdivision_codes, expected_sz_subdivision_codes, "Expected subdivison codes don't match output:\n{}.".format(expected_sz_subdivision_codes))
#3.)
        sm_instance = ISO3166_2("SMR") #San Marino
        sm_subdivision_codes = sm_instance.subdivision_codes() 
        self.assertEqual(sm_subdivision_codes, expected_sm_subdivision_codes, "Expected subdivison codes don't match output:\n{}.".format(expected_sm_subdivision_codes))
#4.)
        pw_instance = ISO3166_2("PLW") #Palau
        pw_subdivision_codes = pw_instance.subdivision_codes() 
        self.assertEqual(pw_subdivision_codes, expected_pw_subdivision_codes, "Expected subdivison codes don't match output:\n{}.".format(expected_pw_subdivision_codes))
#5.)   
        wf_instance = ISO3166_2("876") #Wallis and Futuna 
        wf_subdivision_codes = wf_instance.subdivision_codes() 
        self.assertEqual(wf_subdivision_codes, expected_wf_subdivision_codes, "Expected subdivison codes don't match output:\n{}.".format(expected_wf_subdivision_codes))
#6.)   
        mg_sb_instance = ISO3166_2("MG, 090") #Madagascar, Solomon Islands
        mg_sb_subdivision_codes = mg_sb_instance.subdivision_codes() 
        self.assertEqual(mg_sb_subdivision_codes, expected_mg_sb_subdivision_codes, "Expected subdivison codes don't match output:\n{}.".format(expected_mg_sb_subdivision_codes))   
#7.)   
        gnq_tca_instance = ISO3166_2("GNQ, TCA") #Equitorial Guinea, Turks and Caicos Islands
        gnq_tca_subdivision_codes = gnq_tca_instance.subdivision_codes() 
        self.assertEqual(gnq_tca_subdivision_codes, expected_gnq_tca_subdivision_codes, "Expected subdivison codes don't match output:\n{}.".format(expected_gnq_tca_subdivision_codes))  
#8.)
        all_subdivision_codes = self.all_iso3166_2.subdivision_codes() 
        self.assertEqual(len(all_subdivision_codes), 250, "Expected 250 total country objects in output, got {}.".format(len(all_subdivision_codes))) 
        for key, val in all_subdivision_codes.items():
            self.assertIn(key, list(iso3166.countries_by_alpha2.keys()), "Country code {} not found in list of ISO 3166 alpha-2 codes.".format(key))
            self.assertIsInstance(val, list, "Expected output of subdivision names to be of type list, got {}.".format(type(val)))
#9.)
        with (self.assertRaises(ValueError)):
            self.all_iso3166_2.subdivision_codes("ABCD")
            self.all_iso3166_2.subdivision_codes("Z")
            self.all_iso3166_2.subdivision_codes("1234")
            bg_instance.subdivision_codes("AD")
            sz_instance.subdivision_codes("KM")
            wf_instance.subdivision_codes("090")

    def test_subdivision_names(self):
        """ Testing functionality for getting list of all ISO 3166-2 subdivision names. """
        expected_km_subdivision_names = ['Andjazîdja', 'Andjouân', 'Mohéli']
        expected_er_subdivision_names = ['Al Awsaţ', 'Al Janūbī', 'Ansabā', 'Debubawi K’eyyĭḥ Baḥri', 'Gash-Barka', 'Semienawi K’eyyĭḥ Baḥri']
        expected_gl_subdivision_names = ['Avannaata Kommunia', 'Kommune Kujalleq', 'Kommune Qeqertalik', 'Kommuneqarfik Sermersooq', 'Qeqqata Kommunia']
        expected_ls_subdivision_names = ['Berea', 'Botha-Bothe', 'Leribe', 'Mafeteng', 'Maseru', "Mohale's Hoek", 'Mokhotlong', "Qacha's Nek", 'Quthing', 'Thaba-Tseka']
        expected_zm_subdivision_names = ['Central', 'Copperbelt', 'Eastern', 'Luapula', 'Lusaka', 'Muchinga', 'North-Western', 'Northern', 'Southern', 'Western']
        expected_ag_bn_subdivision_names = {"AG": ['Barbuda', 'Redonda', 'Saint George', 'Saint John', 'Saint Mary', 'Saint Paul', 'Saint Peter', 'Saint Philip'], 
                                            "BN": ['Belait', 'Brunei-Muara', 'Temburong', 'Tutong']}
        expected_dj_va_subdivision_names = {"DJ": ['Ali Sabieh', 'Arta', 'Awbūk', 'Dikhil', 'Djibouti', 'Tadjourah'], 
                                            "VA": []}
#1.)        
        km_instance = ISO3166_2("KM") #Comoros
        km_subdivision_names = km_instance.subdivision_names() 
        self.assertEqual(km_subdivision_names, expected_km_subdivision_names, "Expected subdivison names don't match output:\n{}.".format(expected_km_subdivision_names))
#2.)
        er_instance = ISO3166_2("ER") #Eritrea
        er_subdivision_names = er_instance.subdivision_names() 
        self.assertEqual(er_subdivision_names, expected_er_subdivision_names, "Expected subdivison names don't match output:\n{}.".format(expected_er_subdivision_names))
#3.)
        gl_instance = ISO3166_2("GRL") #Greenland
        gl_subdivision_names = gl_instance.subdivision_names() 
        self.assertEqual(gl_subdivision_names, expected_gl_subdivision_names, "Expected subdivison names don't match output:\n{}.".format(expected_gl_subdivision_names))
#4.)
        ls_instance = ISO3166_2("LSO") #Lesotho
        ls_subdivision_names = ls_instance.subdivision_names() 
        self.assertEqual(ls_subdivision_names, expected_ls_subdivision_names, "Expected subdivison names don't match output:\n{}.".format(expected_ls_subdivision_names))
#5.)
        zm_instance = ISO3166_2("894") #Zambia
        zm_subdivision_names = zm_instance.subdivision_names() 
        self.assertEqual(zm_subdivision_names, expected_zm_subdivision_names, "Expected subdivison names don't match output:\n{}.".format(expected_zm_subdivision_names))
#6.)
        ag_bn_instance = ISO3166_2("028, BN") #Antigua and Barbuda, Brunei
        ag_bn_subdivision_names = ag_bn_instance.subdivision_names() 
        self.assertEqual(ag_bn_subdivision_names, expected_ag_bn_subdivision_names, "Expected subdivison names don't match output:\n{}.".format(expected_ag_bn_subdivision_names))
#7.)
        dj_va_instance = ISO3166_2("DJI, VAT") #Djibouti, Vatican City
        dj_va_subdivision_names = dj_va_instance.subdivision_names() 
        self.assertEqual(dj_va_subdivision_names, expected_dj_va_subdivision_names, "Expected subdivison names don't match output:\n{}.".format(expected_dj_va_subdivision_names))
#8.)
        all_subdivision_names = self.all_iso3166_2.subdivision_names() 
        self.assertEqual(len(all_subdivision_names), 250, "Expected 250 total country output objects, got {}.".format(len(all_subdivision_names)))
        for key, val in all_subdivision_names.items():
            self.assertIn(key, list(iso3166.countries_by_alpha2.keys()), "Country code {} not found in list of ISO 3166 alpha-2 codes.".format(key))
            self.assertIsInstance(val, list, "Expected output of subdivision names to be of type list, got {}.".format(type(val)))
#9.)
        with (self.assertRaises(ValueError)):
            self.all_iso3166_2.subdivision_names("ABCD")
            self.all_iso3166_2.subdivision_names("Z")
            self.all_iso3166_2.subdivision_names("1234")
            self.all_iso3166_2.subdivision_names("blah, blah, blah")
            self.all_iso3166_2.subdivision_names(False)
            km_instance.subdivision_names('ES')
            er_instance.subdivision_names("DO")
            zm_instance.subdivision_names("CPV")
            dj_va_instance.subdivision_names("218")
    
    @unittest.skip("Skipping to not change the main iso3166-2 object during other unit tests running.")
    def test_custom_subdivision(self):
        """ Testing custom_subdivision function that adds or deletes custom subdivisions to the main iso3166-2.json object. """        
        #add below test subdivisions to respective country objects
        self.all_iso3166_2.custom_subdivision("AD", "AD-ZZ", name="Bogus Subdivision", local_name="Bogus Subdivision", type="District", lat_lng=[42.520, 1.657], parent_code=None, flag_url=None)
        self.all_iso3166_2.custom_subdivision("DE", "DE-100", name="Made up subdivision", local_name="Made up subdivision", type="Land", lat_lng=[48.84, 11.479], parent_code=None, flag_url=None,)
        self.all_iso3166_2.custom_subdivision("GY", "GY-ABC", name="New Guyana subdivision", local_name="New Guyana subdivision", type="Region", lat_lng=[6.413, -60.123], parent_code=None, flag_url=None)
        self.all_iso3166_2.custom_subdivision("ZA", "ZA-123", name="Zambian province", local_name="Zambian province", type="Province", lat_lng=[-28.140, 26.777], parent_code=None, flag_url=None)

        #open test json with new subdivisions added
        with open(os.path.join("iso3166_2", "iso3166-2-data", "iso3166-2.json"), 'r', encoding='utf-8') as input_json: 
            test_all_subdivision_data = json.load(input_json)
#1.) 
        self.assertEqual(test_all_subdivision_data["AD"]["AD-ZZ"], {'flagUrl': None, 'latLng': [42.52, 1.657], 'name': 'Bogus Subdivision', 'localName': 'Bogus Subdivision', 'parentCode': None, 'type': 'District'},
            "Expected dict for custom AD-ZZ subdivision does not match output:\n{}.".format(test_all_subdivision_data["AD"]["AD-ZZ"]))
#2.)
        self.assertEqual(test_all_subdivision_data["DE"]["DE-100"], {'flagUrl': None, 'latLng': [48.84, 11.479], 'name': 'Made up subdivision', 'localName': 'Made up subdivision', 'parentCode': None, 'type': 'Land'},
            "Expected dict for custom DE-100 subdivision does not match output:\n{}.".format(test_all_subdivision_data["DE"]["DE-100"]))
#3.)
        self.assertEqual(test_all_subdivision_data["GY"]["GY-ABC"], {'flagUrl': None, 'latLng': [6.413, -60.123], 'name': 'New Guyana subdivision', 'localName': 'New Guyana subdivision', 'parentCode': None, 'type': 'Region'},
            "Expected dict for custom GY-ABC subdivision does not match output:\n{}.".format(test_all_subdivision_data["GY"]["GY-ABC"]))
#4.)
        self.assertEqual(test_all_subdivision_data["ZA"]["ZA-123"], {'flagUrl': None, 'latLng': [-28.14, 26.777], 'name': 'Zambian province', 'localName': 'Zambian province', 'parentCode': None, 'type': 'Province'},
            "Expected dict for custom ZA-123 subdivision does not match output:\n{}.".format(test_all_subdivision_data["ZA"]["ZA-123"]))

        #delete above custom subdivisions
        self.all_iso3166_2.custom_subdivision("AD", subdivision_code="AD-ZZ", delete=1)
        self.all_iso3166_2.custom_subdivision("DE", subdivision_code="DE-100", delete=1)
        self.all_iso3166_2.custom_subdivision("GY", subdivision_code="GY-ABC", delete=1)
        self.all_iso3166_2.custom_subdivision("ZA", subdivision_code="ZA-123", delete=1)

        #open test json with new subdivisions added
        with open(os.path.join("iso3166_2", "iso3166-2-data", "iso3166-2.json"), 'r', encoding='utf-8') as input_json:
            test_all_subdivision_data = json.load(input_json)
#5.)
        self.assertNotIn("AD-ZZ", list(test_all_subdivision_data["AD"].keys()), "Custom AD-ZZ subdivision should not be in object for AD.")
#6.)
        self.assertNotIn("DE-100", list(test_all_subdivision_data["DE"].keys()), "Custom DE-100 subdivision should not be in object for DE.")
#7.)
        self.assertNotIn("GY-ABC", list(test_all_subdivision_data["GY"].keys()), "Custom GY-ABC subdivision should not be in object for GY.")
#8.)
        self.assertNotIn("ZA-123", list(test_all_subdivision_data["ZA"].keys()), "Custom ZA-123 subdivision should not be in object for ZA.")
#9.)
        with self.assertRaises(ValueError):
            self.all_iso3166_2.custom_subdivision("IE", "IE-CN")
            self.all_iso3166_2.custom_subdivision("JM", "JM-01")
            self.all_iso3166_2.custom_subdivision("TV", "TV-NIT")
            self.all_iso3166_2.custom_subdivision("UZ", "UZ-AN")
            self.all_iso3166_2.custom_subdivision("ABC", "blah")
            self.all_iso3166_2.custom_subdivision("ZZ", "blahblahblah")
            self.all_iso3166_2.custom_subdivision("123", "idfuiwf")
#10.)
        with self.assertRaises(TypeError):
            self.all_iso3166_2.custom_subdivision(123, 10.5)
            self.all_iso3166_2.custom_subdivision(name=False)
            self.all_iso3166_2.custom_subdivision("AD", "AD-01", type=123)

    def test_search(self):
        """ Testing searching by subdivision name functionality. """
        test_search_1 = "Monaghan" #IE
        test_search_2 = "Olaines Novads" #LV
        test_search_3 = "Armagh City, Banbridge and Craigavon, Berlin" #GB, DE
        test_search_4 = "North" 
        test_search_5 = "Eastern" 
        test_search_6 = ""
        test_search_7 = "zzzzzzzz"
        test_search_8 = "West Carolina"
        test_search_9 = True
        test_search_10 = 4.6
#1.)
        search_results_1 = self.all_iso3166_2.search(test_search_1, likeness=1) #IE
        expected_search_result_1 = {"IE-MN": {'name': 'Monaghan', 'localName': 'Monaghan', 'type': 'County', 
                                  'parentCode': 'IE-U', 
                                  'flagUrl': 'https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/IE/IE-MN.png', 
                                  'latLng': [54.249, -6.968]}}
        self.assertEqual(search_results_1, expected_search_result_1, 
            "Observed and expected output objects do not match:\n{}.".format(search_results_1))
#2.)
        search_results_2 = self.all_iso3166_2.search(test_search_2, likeness=100)
        expected_search_result_2 = {"LV-068": {'name': 'Olaines novads', 'localName': 'Olaines novads', 'type': 'Municipality', 
                                    'parentCode': None, 'flagUrl': 'https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/LV/LV-068.png', 
                                    'latLng': [56.795, 24.015]}}
        self.assertEqual(search_results_2, expected_search_result_2, 
            "Observed and expected output objects do not match:\n{}.".format(search_results_2))
#3.)
        search_results_3 = self.all_iso3166_2.search(test_search_3, likeness=0.9)
        expected_search_result_3 = {"DE-BE": {'name': "Berlin", "localName": "Berlin", 'type': 'Land', 'parentCode': None, 
                                    "flagUrl": "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/DE/DE-BE.svg", 'latLng': [52.52, 13.405]},
                                    "GB-ABC": {'name': 'Armagh City, Banbridge and Craigavon', 'localName': 'Armagh City, Banbridge and Craigavon', 'type': 'District', 
                                    'parentCode': "GB-NIR", 'flagUrl': None, 'latLng': [54.393, -6.456]}}
        self.assertEqual(search_results_3, expected_search_result_3, 
            "Observed and expected output objects do not match:\n{}.".format(search_results_3))
#4.)
        search_results_4 = self.all_iso3166_2.search(test_search_4, likeness=70) #North
        expected_search_result_4 = {"CM-NO": {'name': 'North', 'localName': 'North', 'type': 'Region', 'parentCode': None, 'flagUrl': None, 'latLng': [8.581, 13.914]},
                                    "GW-N": {'name': 'Norte', 'localName': 'Norte', 'type': 'Province', 'parentCode': None, 'flagUrl': None, 'latLng': [11.804, -15.18]},
                                    'CM-EN': {'name': 'Far North', 'localName': 'Far North', 'type': 'Region', 'parentCode': None, 'flagUrl': None, 'latLng': [10.632, 14.659]},                                                                   
                                    'FJ-N': {'name': 'Northern', 'localName': 'Northern', 'type': 'Division', 'parentCode': None, 'flagUrl': None, 'latLng': [-16.627, 179.018]}, 
                                    'GH-NP': {'name': 'Northern', 'localName': 'Northern', 'type': 'Region', 'parentCode': None, 'flagUrl': None, 'latLng': [9.367, -0.149]}, 
                                    'PG-NPP': {'name': 'Northern', 'localName': 'Northern', 'type': 'Province', 'parentCode': None, 'flagUrl': 'https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/PG/PG-NPP.png', 'latLng': [-8.899, 148.189]}, 
                                    'RW-03': {'name': 'Northern', 'localName': 'Northern', 'type': 'Province', 'parentCode': None, 'flagUrl': None, 'latLng': [-1.656, 29.882]}, 
                                    'SD-NO': {'name': 'Northern', 'localName': 'Northern', 'type': 'State', 'parentCode': None, 'flagUrl': 'https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/SD/SD-NO.png', 'latLng': [18.445, 30.159]}, 
                                    'SL-N': {'name': 'Northern', 'localName': 'Northern', 'type': 'Province', 'parentCode': None, 'flagUrl': None, 'latLng': [9.182, -11.525]}, 
                                    'UG-N': {'name': 'Northern', 'localName': 'Northern', 'type': 'Geographical region', 'parentCode': None, 'flagUrl': None, 'latLng': [2.878, 32.718]}, 
                                    'ZM-05': {'name': 'Northern', 'localName': 'Northern', 'type': 'Province', 'parentCode': None, 'flagUrl': 'https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/ZM/ZM-05.png', 'latLng': [-9.767, 30.896]}}  
        self.assertEqual(search_results_4, expected_search_result_4, 
            "Observed and expected output objects do not match:\n{}.".format(search_results_4))
#5.)
        search_results_5 = self.all_iso3166_2.search(test_search_5, likeness=0.7) #Eastern
        expected_search_result_5 = {"FJ-E": {'name': 'Eastern', 'localName': 'Eastern', 'type': 'Division', 'parentCode': None, "flagUrl": None, "latLng": [-17.689, 178.807]}, 
                                     "GH-EP": {'name': 'Eastern', 'localName': 'Eastern', 'type': 'Region', 'parentCode': None, "flagUrl": "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/GH/GH-EP.svg", "latLng": [6.578, -0.45]}, 
                                     "RW-02": {'name': 'Eastern', 'localName': 'Eastern', 'type': 'Province', 'parentCode': None, "flagUrl": None, "latLng": [-1.782, 30.436]}, 
                                     "SL-E": {'name': 'Eastern', 'localName': 'Eastern', 'type': 'Province', 'parentCode': None, "flagUrl": None, "latLng": [7.811, -11.162]}, 
                                     "UG-E": {'name': 'Eastern', 'localName': 'Eastern', 'type': 'Geographical region', 'parentCode': None, "flagUrl": None, "latLng": [1.269, 33.438]}, 
                                     "ZM-03": {'name': 'Eastern', 'localName': 'Eastern', 'type': 'Province', 'parentCode': None, "flagUrl": "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/ZM/ZM-03.png", "latLng": [-13.806, 31.993]}}              
        self.assertEqual(search_results_5, expected_search_result_5, 
            "Observed and expected output objects do not match:\n{}.".format(search_results_5))
#6.)
        search_results_6 = self.all_iso3166_2.search(test_search_6)
        self.assertEqual(search_results_6, {}, "Expected output to be an empty dict, got {}.".format(search_results_6))
#7.)
        search_results_7 = self.all_iso3166_2.search(test_search_7)
        self.assertEqual(search_results_7, {}, "Expected output to be an empty dict, got {}.".format(search_results_7))
#8.)
        search_results_8 = self.all_iso3166_2.search(test_search_8)
        self.assertEqual(search_results_8, {}, "Expected output to be an empty dict, got {}.".format(search_results_8))
#9.)
        with (self.assertRaises(TypeError)):
            self.all_iso3166_2.search(test_search_9)
            self.all_iso3166_2.search(test_search_10)
        
    def tearDown(self):
        """ Delete any test json folders and objects . """
        shutil.rmtree(self.test_output_dir)

        #remove the temp dir created to store duplicate of iso3166-2 object before any changes were made using the add_subdivision() function,
        #a successful pass of all the above test cases mean there are no errors on the current object and the archive folder can be deleted
        if (os.path.isdir("archive-iso3166-2")):
            shutil.rmtree(self.test_output_dir)
        
        #delete object holding all ISO 3166-2 data
        del self.all_iso3166_2
            
if __name__ == '__main__':
    #run all unit tests
    unittest.main(verbosity=2)    