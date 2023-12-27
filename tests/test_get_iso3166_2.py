from iso3166_2_scripts.get_iso3166_2 import *
import requests
import json
import os
import getpass
import shutil
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

class Get_ISO3166_2_Tests(unittest.TestCase):
    """
    Test suite for testing get_iso3166_2.py script that pulls all the ISO 3166-2
    subdivision data for all countries from the data sources. 

    Test Cases
    ==========
    test_export_iso3166_2:
        testing correct ISO 3166-2 data is exported and pulled from data sources.
    """
    def setUp(self):
        """ Initialise test variables. """
        #initalise User-agent header for requests library 
        self.__version__ = metadata('iso3166-2')['version']
        self.user_agent_header = {'User-Agent': 'iso3166-2/{} ({}; {})'.format(self.__version__,
                                            'https://github.com/amckenna41/iso3166-2', getpass.getuser())}
        self.test_output_dir = "test_output_dir"
        self.test_output_filename = "test_json"
    
        #list of output columns for main iso3166-2 json
        self.correct_output_attributes = ["name", "localName", "type", "parentCode", "flagUrl", "latLng"]

        #turn off tqdm progress bar functionality when running tests
        os.environ["TQDM_DISABLE"] = "1"

        #base url for flag icons on iso3166-flag-icons repo
        self.flag_icons_base_url = "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/"
        
    def test_export_iso3166_2(self):
        """ Testing export functionality for getting ISO 3166-2 subdivision data from data sources. """
        test_alpha2_dk = "DK" #Denmark
        test_alpha2_fi = "FI" #Finland
        test_alpha2_gd = "GD" #Grenada
        test_alpha2_kg_mg_nr = "KG,MG,NR" #Kyrgyzstan, Madagascar, Nauru
        test_alpha2_bv_fo_gs_hk = ["BV", "FO", "GS", "HK"] #Bouvet Island, Faroe Islands, South Georgia, Hong Kong
        test_alpha2_error1 = "ZZ"
        test_alpha2_error2 = "ABCDEF"
        test_alpha2_error3 = 1234
#1.)
        export_iso3166_2(alpha2_codes=test_alpha2_dk, output_folder=self.test_output_dir, json_filename=self.test_output_filename, verbose=0) #Denmark

        #open exported jsons
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha2_dk + ".json")) as output_json:
            test_iso3166_2_dk = json.load(output_json)

        self.assertIsInstance(test_iso3166_2_dk, dict, "Expected output to be type dict, got {}.".format(type(test_iso3166_2_dk)))
        self.assertEqual(len(test_iso3166_2_dk["DK"]), 5, "Expected 5 subdivisions to be in output dict, got {}.".format(len(test_iso3166_2_dk["DK"])))
        self.assertEqual(list(test_iso3166_2_dk["DK"].keys()), ['DK-81', 'DK-82', 'DK-83', 'DK-84', 'DK-85'], 
                "Expected list of subdivision codes doesn't match output:\n{}.".format(list(test_iso3166_2_dk["DK"].keys())))   
        for subd in test_iso3166_2_dk["DK"]:
            self.assertIsNot(test_iso3166_2_dk["DK"][subd]["name"], None, 
                "Expected subdivision name to not be None, got {}.".format(test_iso3166_2_dk["DK"][subd]["name"]))
            self.assertEqual(test_iso3166_2_dk["DK"][subd]["name"], test_iso3166_2_dk["DK"][subd]["localName"],
                "Expected subdivision's name and local name to be the same.")
            if not (test_iso3166_2_dk["DK"][subd]["parentCode"] is None):
                self.assertIn(test_iso3166_2_dk["DK"][subd]["parentCode"], list(test_iso3166_2_dk["DK"][subd].keys()), 
                    "Parent code {} not found in list of subdivision codes:\n{}.".format(test_iso3166_2_dk["DK"][subd]["parentCode"]), list(test_iso3166_2_dk["DK"][subd].keys()))
            if not (test_iso3166_2_dk["DK"][subd]["flagUrl"] is None):
                self.assertEqual(os.path.splitext(test_iso3166_2_dk["DK"][subd]["flagUrl"])[0], self.flag_icons_base_url + "DK/" + subd, 
                    "Expected flag url to be {}, got {}.".format(self.flag_icons_base_url + "DK/" + subd, os.path.splitext(test_iso3166_2_dk["DK"][subd]["flagUrl"])[0])) 
                self.assertEqual(requests.get(test_iso3166_2_dk["DK"][subd]["flagUrl"], headers=self.user_agent_header).status_code, 200, 
                    "Flag URL invalid: {}.".format(test_iso3166_2_dk["DK"][subd]["flagUrl"]))
            for key in list(test_iso3166_2_dk["DK"][subd].keys()):
                self.assertIn(key, self.correct_output_attributes, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_output_attributes))

        #DK-81 - Nordjylland
        self.assertEqual(test_iso3166_2_dk["DK"]["DK-81"]["name"], "Nordjylland", 
            "Expected subdivsion name to be Nordjylland, got {}.".format(test_iso3166_2_dk["DK"]["DK-81"]["name"]))  
        self.assertEqual(test_iso3166_2_dk["DK"]["DK-81"]["localName"], "Nordjylland", 
            "Expected subdivsion local name to be Nordjylland, got {}.".format(test_iso3166_2_dk["DK"]["DK-81"]["localName"]))  
        self.assertEqual(test_iso3166_2_dk["DK"]["DK-81"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_iso3166_2_dk["DK"]["DK-81"]["parentCode"]))
        self.assertEqual(test_iso3166_2_dk["DK"]["DK-81"]["type"], "Region", 
            "Expected subdivision type to be Region, got {}.".format(test_iso3166_2_dk["DK"]["DK-81"]["type"]))
        # self.assertEqual(test_iso3166_2_dk["DK"]["DK-81"]["latLng"], [56.831, 9.493],
        #     "Expected subdivision latLng to be [56.831, 9.493], got {}.".format(test_iso3166_2_dk["DK"]["DK-81"]["latLng"]))
        self.assertEqual(test_iso3166_2_dk["DK"]["DK-81"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/DK/DK-81.svg",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/DK/DK-81.svg, got {}.".format(test_iso3166_2_dk["DK"]["DK-81"]["flagUrl"]))
        #DK-82 - Midtjylland
        self.assertEqual(test_iso3166_2_dk["DK"]["DK-82"]["name"], "Midtjylland", 
            "Expected subdivsion name to be Midtjylland, got {}.".format(test_iso3166_2_dk["DK"]["DK-82"]["name"]))  
        self.assertEqual(test_iso3166_2_dk["DK"]["DK-82"]["localName"], "Midtjylland", 
            "Expected subdivsion local name to be Midtjylland, got {}.".format(test_iso3166_2_dk["DK"]["DK-82"]["localName"]))  
        self.assertEqual(test_iso3166_2_dk["DK"]["DK-82"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_iso3166_2_dk["DK"]["DK-82"]["parentCode"]))
        self.assertEqual(test_iso3166_2_dk["DK"]["DK-82"]["type"], "Region", 
            "Expected subdivision type to be Region, got {}.".format(test_iso3166_2_dk["DK"]["DK-82"]["type"]))
        # self.assertEqual(test_iso3166_2_dk["DK"]["DK-82"]["latLng"], [56.302, 9.303],
        #     "Expected subdivision latLng to be [56.302, 9.303], got {}.".format(test_iso3166_2_dk["DK"]["DK-82"]["latLng"]))
        self.assertEqual(test_iso3166_2_dk["DK"]["DK-82"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/DK/DK-82.svg",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/DK/DK-82.svg, got {}.".format(test_iso3166_2_dk["DK"]["DK-82"]["flagUrl"]))
#2.)    
        export_iso3166_2(alpha2_codes=test_alpha2_fi, output_folder=self.test_output_dir, json_filename=self.test_output_filename, verbose=0) #Finland

        #open exported jsons
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha2_fi + ".json"))  as output_json:
            test_iso3166_2_fi = json.load(output_json)

        self.assertIsInstance(test_iso3166_2_fi, dict, "Expected output to be type dict, got {}.".format(type(test_iso3166_2_fi)))
        self.assertEqual(len(test_iso3166_2_fi["FI"]), 19, "Expected 19 keys/attributes in output dict, got {}.".format(len(test_iso3166_2_fi)))
        self.assertEqual(list(test_iso3166_2_fi["FI"].keys()), ["FI-01", "FI-02", "FI-03", "FI-04", "FI-05", "FI-06", "FI-07", "FI-08", "FI-09", 
            "FI-10", "FI-11", "FI-12", "FI-13", "FI-14", "FI-15", "FI-16", "FI-17", "FI-18", "FI-19"], 
                "Expected list of subdivision codes doesn't match output:\n{}.".format(list(test_iso3166_2_fi["FI"].keys())))   
        for subd in test_iso3166_2_fi["FI"]:
            self.assertIsNot(test_iso3166_2_fi["FI"][subd]["name"], None, 
                "Expected subdivision name to not be None, got {}.".format(test_iso3166_2_fi["FI"][subd]["name"]))
            self.assertEqual(test_iso3166_2_fi["FI"][subd]["name"], test_iso3166_2_fi["FI"][subd]["localName"],
                "Expected subdivision's name and local name to be the same.")
            if not (test_iso3166_2_fi["FI"][subd]["parentCode"] is None):
                self.assertIn(test_iso3166_2_fi["FI"][subd]["parentCode"], list(test_iso3166_2_fi["FI"][subd].keys()), 
                    "Parent code {} not found in list of subdivision codes.".format(test_iso3166_2_fi["FI"][subd]["parentCode"]))
            if not (test_iso3166_2_fi["FI"][subd]["flagUrl"] is None):
                self.assertEqual(os.path.splitext(test_iso3166_2_fi["FI"][subd]["flagUrl"])[0], self.flag_icons_base_url + "FI/" + subd, 
                    "Expected flag url to be {}, got {}.".format(self.flag_icons_base_url + "FI/" + subd, os.path.splitext(test_iso3166_2_fi["FI"][subd]["flagUrl"])[0])) 
                self.assertEqual(requests.get(test_iso3166_2_fi["FI"][subd]["flagUrl"], headers=self.user_agent_header).status_code, 200, 
                    "Flag URL invalid: {}.".format(test_iso3166_2_fi["FI"][subd]["flagUrl"]))
            for key in list(test_iso3166_2_fi["FI"][subd].keys()):
                self.assertIn(key, self.correct_output_attributes, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_output_attributes))

        #FI-01 - Ahvenanmaan maakunta
        self.assertEqual(test_iso3166_2_fi["FI"]["FI-01"]["name"], "Åland", 
            "Expected subdivsion name to be Åland, got {}.".format(test_iso3166_2_fi["FI"]["FI-01"]["name"]))  
        self.assertEqual(test_iso3166_2_fi["FI"]["FI-01"]["localName"], "Åland", 
            "Expected subdivsion local name to be Åland, got {}.".format(test_iso3166_2_fi["FI"]["FI-01"]["localName"]))  
        self.assertEqual(test_iso3166_2_fi["FI"]["FI-01"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_iso3166_2_fi["FI"]["FI-01"]["parentCode"]))
        self.assertEqual(test_iso3166_2_fi["FI"]["FI-01"]["type"], "Region", 
            "Expected subdivision type to be Region, got {}.".format(test_iso3166_2_fi["FI"]["FI-01"]["type"]))
        # self.assertEqual(test_iso3166_2_fi["FI"]["FI-01"]["latLng"], [61.924, 25.748],
        #     "Expected subdivision latLng to be [61.924, 25.748], got {}.".format(test_iso3166_2_fi["FI"]["FI-01"]["latLng"]))
        self.assertEqual(test_iso3166_2_fi["FI"]["FI-01"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/FI/FI-01.svg",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/FI/FI-01.svg, got {}.".format(test_iso3166_2_fi["FI"]["FI-01"]["flagUrl"]))
        #FI-17 - Satakunda
        self.assertEqual(test_iso3166_2_fi["FI"]["FI-17"]["name"], "Satakunta", 
            "Expected subdivsion name to be Satakunda, got {}.".format(test_iso3166_2_fi["FI"]["FI-17"]["name"]))  
        self.assertEqual(test_iso3166_2_fi["FI"]["FI-17"]["localName"], "Satakunta", 
            "Expected subdivsion local name to be Satakunda, got {}.".format(test_iso3166_2_fi["FI"]["FI-17"]["localName"]))  
        self.assertEqual(test_iso3166_2_fi["FI"]["FI-17"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_iso3166_2_fi["FI"]["FI-17"]["parentCode"]))
        self.assertEqual(test_iso3166_2_fi["FI"]["FI-17"]["type"], "Region", 
            "Expected subdivision type to be Region, got {}.".format(test_iso3166_2_fi["FI"]["FI-17"]["type"]))
        # self.assertEqual(test_iso3166_2_fi["FI"]["FI-17"]["latLng"], [61.593, 22.148],
        #     "Expected subdivision latLng to be [61.593, 22.148], got {}.".format(test_iso3166_2_fi["FI"]["FI-17"]["latLng"]))
        self.assertEqual(test_iso3166_2_fi["FI"]["FI-17"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/FI/FI-17.svg",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/FI/FI-17.svg, got {}.".format(test_iso3166_2_fi["FI"]["FI-17"]["flagUrl"]))
#3.)
        export_iso3166_2(alpha2_codes=test_alpha2_gd, output_folder=self.test_output_dir, json_filename=self.test_output_filename, verbose=0) #Grenada

        #open exported jsons
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha2_gd + ".json")) as output_json:
            test_iso3166_2_gd = json.load(output_json)

        self.assertIsInstance(test_iso3166_2_gd, dict, "Expected output to be type dict, got {}.".format(type(test_iso3166_2_gd)))
        self.assertEqual(len(test_iso3166_2_gd["GD"]), 7, "Expected 7 keys/attributes in output dict, got {}.".format(len(test_iso3166_2_gd)))
        self.assertEqual(list(test_iso3166_2_gd["GD"].keys()), ["GD-01", "GD-02", "GD-03", "GD-04", "GD-05", "GD-06", "GD-10"], 
                "Expected list of subdivision codes doesn't match output:\n{}.".format(list(test_iso3166_2_gd["GD"].keys())))   
        for subd in test_iso3166_2_gd["GD"]:
            self.assertIsNot(test_iso3166_2_gd["GD"][subd]["name"], None, 
                "Expected subdivision name to not be None, got {}.".format(test_iso3166_2_gd["GD"][subd]["name"]))
            self.assertEqual(test_iso3166_2_gd["GD"][subd]["name"], test_iso3166_2_gd["GD"][subd]["localName"],
                "Expected subdivision's name and local name to be the same.")
            if not (test_iso3166_2_gd["GD"][subd]["parentCode"] is None):
                self.assertIn(test_iso3166_2_gd["GD"][subd]["parentCode"], list(test_iso3166_2_gd["GD"][subd].keys()), 
                    "Parent code {} not found in list of subdivision codes.".format(test_iso3166_2_gd["GD"][subd]["parentCode"]))
            if not (test_iso3166_2_gd["GD"][subd]["flagUrl"] is None):
                self.assertEqual(os.path.splitext(test_iso3166_2_gd["GD"][subd]["flagUrl"])[0], self.flag_icons_base_url + "GD/" + subd, 
                    "Expected flag url to be {}, got {}.".format(self.flag_icons_base_url + "GD/" + subd, os.path.splitext(test_iso3166_2_gd["GD"][subd]["flagUrl"])[0])) 
                self.assertEqual(requests.get(test_iso3166_2_gd["GD"][subd]["flagUrl"], headers=self.user_agent_header).status_code, 200, 
                    "Flag URL invalid: {}.".format(test_iso3166_2_gd["GD"][subd]["flagUrl"]))
            for key in list(test_iso3166_2_gd["GD"][subd].keys()):
                self.assertIn(key, self.correct_output_attributes, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_output_attributes))

        #GD-03 - Saint George
        self.assertEqual(test_iso3166_2_gd["GD"]["GD-03"]["name"], "Saint George", 
            "Expected subdivsion name to be Saint George, got {}.".format(test_iso3166_2_gd["GD"]["GD-03"]["name"]))  
        self.assertEqual(test_iso3166_2_gd["GD"]["GD-03"]["localName"], "Saint George", 
            "Expected subdivsion local name to be Saint George, got {}.".format(test_iso3166_2_gd["GD"]["GD-03"]["localName"]))  
        self.assertEqual(test_iso3166_2_gd["GD"]["GD-03"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_iso3166_2_gd["GD"]["GD-03"]["parentCode"]))
        self.assertEqual(test_iso3166_2_gd["GD"]["GD-03"]["type"], "Parish", 
            "Expected subdivision type to be Parish, got {}.".format(test_iso3166_2_gd["GD"]["GD-03"]["type"]))
        self.assertEqual(test_iso3166_2_gd["GD"]["GD-03"]["latLng"], [12.056, -61.749],
            "Expected subdivision latLng to be [12.056, -61.749], got {}.".format(test_iso3166_2_gd["GD"]["GD-03"]["latLng"]))
        self.assertEqual(test_iso3166_2_gd["GD"]["GD-03"]["flagUrl"], None,
            "Expected subdivision flag url to be None, got {}.".format(test_iso3166_2_gd["GD"]["GD-03"]["flagUrl"]))
        #GD-10 - Southern Grenadine Islands
        self.assertEqual(test_iso3166_2_gd["GD"]["GD-10"]["name"], "Southern Grenadine Islands", 
            "Expected subdivsion name to be Southern Grenadine Islands, got {}.".format(test_iso3166_2_gd["GD"]["GD-10"]["name"]))  
        self.assertEqual(test_iso3166_2_gd["GD"]["GD-10"]["localName"], "Southern Grenadine Islands", 
            "Expected subdivsion local name to be Southern Grenadine Islands, got {}.".format(test_iso3166_2_gd["GD"]["GD-10"]["localName"]))  
        self.assertEqual(test_iso3166_2_gd["GD"]["GD-10"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_iso3166_2_gd["GD"]["GD-10"]["parentCode"]))
        self.assertEqual(test_iso3166_2_gd["GD"]["GD-10"]["type"], "Dependency", 
            "Expected subdivision type to be Dependency, got {}.".format(test_iso3166_2_gd["GD"]["GD-10"]["type"]))
        # self.assertEqual(test_iso3166_2_gd["GD"]["GD-10"]["latLng"], [12.479, -61.449],
        #     "Expected subdivision latLng to be [12.479, -61.449], got {}.".format(test_iso3166_2_gd["GD"]["GD-10"]["latLng"]))
        self.assertEqual(test_iso3166_2_gd["GD"]["GD-10"]["flagUrl"], None,
            "Expected subdivision flag url to be None, got {}.".format(test_iso3166_2_gd["GD"]["GD-10"]["flagUrl"]))
#4.)
        export_iso3166_2(alpha2_codes=test_alpha2_kg_mg_nr, output_folder=self.test_output_dir, json_filename=self.test_output_filename, verbose=0) #Kyrgyzstan, Madagascar, Nauru

        #open exported jsons
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha2_kg_mg_nr + ".json")) as output_json:
            test_iso3166_2_kg_mg_nr = json.load(output_json)

        self.assertIsInstance(test_iso3166_2_kg_mg_nr, dict, "Expected output to be type dict, got {}.".format(type(test_iso3166_2_kg_mg_nr)))
        
        self.assertEqual(len(test_iso3166_2_kg_mg_nr["KG"]), 9, "Expected 9 subdivisions in output dict, got {}.".format(len(test_iso3166_2_kg_mg_nr["KG"])))
        self.assertEqual(len(test_iso3166_2_kg_mg_nr["MG"]), 6, "Expected 6 subdivisions in output dict, got {}.".format(len(test_iso3166_2_kg_mg_nr["MG"])))
        self.assertEqual(len(test_iso3166_2_kg_mg_nr["NR"]), 14, "Expected 14 subdivisions in output dict, got {}.".format(len(test_iso3166_2_kg_mg_nr["NR"])))
        self.assertEqual(list(test_iso3166_2_kg_mg_nr["KG"].keys()), ['KG-B', 'KG-C', 'KG-GB', 'KG-GO', 'KG-J', 'KG-N', 'KG-O', 'KG-T', 'KG-Y'], 
            "Expected list of subdivision codes doesn't match output.")   
        self.assertEqual(list(test_iso3166_2_kg_mg_nr["MG"].keys()), ["MG-A", "MG-D", "MG-F", "MG-M", "MG-T", "MG-U"], 
            "Expected list of subdivision codes doesn't match output.")   
        self.assertEqual(list(test_iso3166_2_kg_mg_nr["NR"].keys()), ['NR-01', 'NR-02', 'NR-03', 'NR-04', 'NR-05', 'NR-06', 'NR-07', 'NR-08', 'NR-09', 'NR-10', 
            'NR-11', 'NR-12', 'NR-13', 'NR-14'], "Expected list of subdivision codes doesn't match output.")   
        for country in test_iso3166_2_kg_mg_nr:
            for subd in test_iso3166_2_kg_mg_nr[country]:
                self.assertIsNot(test_iso3166_2_kg_mg_nr[country][subd]["name"], None, 
                    "Expected subdivision name to not be None, got {}.".format(test_iso3166_2_kg_mg_nr[country][subd]["name"]))
                if not (test_iso3166_2_kg_mg_nr[country][subd]["parentCode"] is None):
                    self.assertIn(test_iso3166_2_kg_mg_nr[country][subd]["parentCode"], list(test_iso3166_2_kg_mg_nr[country][subd].keys()), 
                        "Parent code {} not found in list of subdivision codes.".format(test_iso3166_2_kg_mg_nr[country][subd]["parentCode"]))
                if not (test_iso3166_2_kg_mg_nr[country][subd]["flagUrl"] is None):
                    self.assertEqual(os.path.splitext(test_iso3166_2_kg_mg_nr[country][subd]["flagUrl"])[0], self.flag_icons_base_url + country + "/" + subd, 
                        "Expected flag url to be {}, got {}.".format(self.flag_icons_base_url + country + "/" + subd, os.path.splitext(test_iso3166_2_kg_mg_nr[country][subd]["flagUrl"])[0])) 
                    self.assertEqual(requests.get(test_iso3166_2_kg_mg_nr[country][subd]["flagUrl"], headers=self.user_agent_header).status_code, 200, 
                        "Flag URL invalid: {}.".format(test_iso3166_2_kg_mg_nr[country][subd]["flagUrl"]))
                for key in list(test_iso3166_2_kg_mg_nr[country][subd].keys()):
                    self.assertIn(key, self.correct_output_attributes, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_output_attributes))
        
        #KG-GB - Bishkek Shaary
        self.assertEqual(test_iso3166_2_kg_mg_nr["KG"]["KG-GB"]["name"], "Bishkek Shaary", 
            "Expected subdivsion name to be Bishkek Shaary, got {}.".format(test_iso3166_2_kg_mg_nr["KG"]["KG-GB"]["name"]))  
        self.assertEqual(test_iso3166_2_kg_mg_nr["KG"]["KG-GB"]["localName"], "Bishkek Shaary", 
            "Expected subdivsion local name to be Bishkek Shaary, got {}.".format(test_iso3166_2_kg_mg_nr["KG"]["KG-GB"]["localName"]))  
        self.assertEqual(test_iso3166_2_kg_mg_nr["KG"]["KG-GB"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_iso3166_2_kg_mg_nr["KG"]["KG-GB"]["parentCode"]))
        self.assertEqual(test_iso3166_2_kg_mg_nr["KG"]["KG-GB"]["type"], "City", 
            "Expected subdivision type to be City, got {}.".format(test_iso3166_2_kg_mg_nr["KG"]["KG-GB"]["type"]))
        self.assertEqual(test_iso3166_2_kg_mg_nr["KG"]["KG-GB"]["latLng"], [42.875, 74.57],
            "Expected subdivision latLng to be [42.875, 74.57], got {}.".format(test_iso3166_2_kg_mg_nr["KG"]["KG-GB"]["latLng"]))
        self.assertEqual(test_iso3166_2_kg_mg_nr["KG"]["KG-GB"]["flagUrl"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/KG/KG-GB.svg",
            "Expected subdivision flag url to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/KG/KG-GB.svg, got {}.".format(test_iso3166_2_kg_mg_nr["KG"]["KG-GB"]["flagUrl"]))
        #MG-D - Antsiranana
        self.assertEqual(test_iso3166_2_kg_mg_nr["MG"]["MG-D"]["name"], "Antsiranana", 
            "Expected subdivsion name to be Antsiranana, got {}.".format(test_iso3166_2_kg_mg_nr["MG"]["MG-D"]["name"]))  
        self.assertEqual(test_iso3166_2_kg_mg_nr["MG"]["MG-D"]["localName"], "Antsiranana", 
            "Expected subdivsion local name to be Antsiranana, got {}.".format(test_iso3166_2_kg_mg_nr["MG"]["MG-D"]["localName"]))  
        self.assertEqual(test_iso3166_2_kg_mg_nr["MG"]["MG-D"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_iso3166_2_kg_mg_nr["MG"]["MG-D"]["parentCode"]))
        self.assertEqual(test_iso3166_2_kg_mg_nr["MG"]["MG-D"]["type"], "Province", 
            "Expected subdivision type to be Province, got {}.".format(test_iso3166_2_kg_mg_nr["MG"]["MG-D"]["type"]))
        self.assertEqual(test_iso3166_2_kg_mg_nr["MG"]["MG-D"]["latLng"], [-12.323, 49.294],
            "Expected subdivision latLng to be [-12.323, 49.294], got {}.".format(test_iso3166_2_kg_mg_nr["MG"]["MG-D"]["latLng"]))
        self.assertEqual(test_iso3166_2_kg_mg_nr["MG"]["MG-D"]["flagUrl"], None,
            "Expected subdivision flag url to be None, got {}.".format(test_iso3166_2_kg_mg_nr["MG"]["MG-D"]["flagUrl"]))
        #NR-02 - Anabar
        self.assertEqual(test_iso3166_2_kg_mg_nr["NR"]["NR-02"]["name"], "Anabar", 
            "Expected subdivsion name to be Anabar, got {}.".format(test_iso3166_2_kg_mg_nr["NR"]["NR-02"]["name"]))  
        self.assertEqual(test_iso3166_2_kg_mg_nr["NR"]["NR-02"]["localName"], "Anabar", 
            "Expected subdivsion local name to be Anabar, got {}.".format(test_iso3166_2_kg_mg_nr["NR"]["NR-02"]["localName"]))  
        self.assertEqual(test_iso3166_2_kg_mg_nr["NR"]["NR-02"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_iso3166_2_kg_mg_nr["NR"]["NR-02"]["parentCode"]))
        self.assertEqual(test_iso3166_2_kg_mg_nr["NR"]["NR-02"]["type"], "District", 
            "Expected subdivision type to be District, got {}.".format(test_iso3166_2_kg_mg_nr["NR"]["NR-02"]["type"]))
        self.assertEqual(test_iso3166_2_kg_mg_nr["NR"]["NR-02"]["latLng"], [-0.513, 166.948],
            "Expected subdivision latLng to be [-0.513, 166.948], got {}.".format(test_iso3166_2_kg_mg_nr["NR"]["NR-02"]["latLng"]))
        self.assertEqual(test_iso3166_2_kg_mg_nr["NR"]["NR-02"]["flagUrl"], None,
            "Expected subdivision flag url to be None, got {}.".format(test_iso3166_2_kg_mg_nr["NR"]["NR-02"]["flagUrl"]))
#5.)
        with (self.assertRaises(ValueError)):
            export_iso3166_2(alpha2_codes=test_alpha2_error1, output_folder=self.test_output_dir, json_filename=self.test_output_filename, verbose=0) #ZZ
            export_iso3166_2(alpha2_codes=test_alpha2_error2, output_folder=self.test_output_dir, json_filename=self.test_output_filename, verbose=0) #ABCDEF
            export_iso3166_2(alpha2_codes=test_alpha2_error3, output_folder=self.test_output_dir, json_filename=self.test_output_filename, verbose=0) #1234
#6.)
        # for alpha_2 in test_alpha2_bv_fo_gs_hk:
        #     export_iso3166_2(alpha2_codes=alpha_2, output_folder=self.test_output_dir, json_filename=self.test_output_filename, verbose=0)
        #     with (self.assertRaises(FileNotFoundError)):
        #         with open(os.path.join(self.test_output_dir, self.test_output_filename + "-" + alpha_2 + ".json")) as output_json:
        #             json.load(output_json)

    def tearDown(self):
        """ Delete any exported json folder. """
        shutil.rmtree(self.test_output_dir)

if __name__ == '__main__':
    #run all unit tests
    unittest.main(verbosity=2)    