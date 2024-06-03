from iso3166_2_scripts.get_iso3166_2 import *
import requests
import json
import os
import getpass
import shutil
import unittest
import warnings
unittest.TestLoader.sortTestMethodsUsing = None

#ignore resource warnings
warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

# @unittest.skip("")
class Get_ISO3166_2_Tests(unittest.TestCase):
    """
    Test suite for testing get_iso3166_2.py script that pulls all the ISO 3166-2
    subdivision data for all countries from the data sources. 

    Test Cases
    ==========
    test_export_iso3166_2:
        testing correct ISO 3166-2 data is exported and pulled from data sources.
    test_export_iso3166_restcountries:
        testing correct ISO 3166-2 data is exported and pulled from data sources,
        with additional attributes from RestCountries exported.
    test_export_exclude_default_attributes:
        testing correct ISO 3166-2 data is exported and pulled from data sources,
        with some of the default attributes excluded from export.
    """
    def setUp(self):
        """ Initialise test variables. """
        #initalise User-agent header for requests library 
        self.__version__ = metadata('iso3166-2')['version']
        self.user_agent_header = {'User-Agent': f"iso3166-2/{self.__version__} (https://github.com/amckenna41/iso3166-2; {getpass.getuser()})"}

        self.test_output_dir = "test_output_dir"
        self.test_output_filename = "test_json"
    
        #list of output columns for main iso3166-2 json
        self.correct_output_attributes = ["name", "localName", "type", "parentCode", "flag", "latLng"]

        #list of output columns for iso3166-2 CSV
        self.correct_output_columns = ["alpha_code", "subdivision_code", "name", "localName", "type", "parentCode", "flag", "latLng"]

        #turn off tqdm progress bar functionality when running tests
        os.environ["TQDM_DISABLE"] = "1"

        #base url for flag icons on iso3166-flag-icons repo
        self.flag_icons_base_url = "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/"
        
    def test_export_iso3166_2(self):
        """ Testing export functionality for getting ISO 3166-2 subdivision data from data sources. """
        test_alpha_dk = "DK" #Denmark
        test_alpha_fi = "FI" #Finland
        test_alpha_np = "NPL" #Nepal
        test_alpha_kg_mg_nr = "KG,MDG,520" #Kyrgyzstan, Madagascar, Nauru
        test_alpha_error1 = "ZZ"
        test_alpha_error2 = "ABCDEF"
        test_alpha_error3 = 1234
#1.)
        export_iso3166_2(alpha_codes=test_alpha_dk, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1) #Denmark

        #open exported json
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha_dk + ".json")) as output_json:
            test_iso3166_2_dk_json = json.load(output_json)
        #open exported CSV
        test_iso3166_2_dk_csv = pd.read_csv(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha_dk + ".csv"))

        self.assertEqual(len(test_iso3166_2_dk_json["DK"]), 5, "Expected 5 subdivisions to be in output dict, got {}.".format(len(test_iso3166_2_dk_json["DK"])))
        self.assertEqual(list(test_iso3166_2_dk_json["DK"].keys()), ['DK-81', 'DK-82', 'DK-83', 'DK-84', 'DK-85'], 
            "Expected list of subdivision codes doesn't match output:\n{}.".format(list(test_iso3166_2_dk_json["DK"].keys())))   
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "-DK.csv")), 
            "Expected subdivision data to be exported to a CSV: {}.".format(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "-DK.csv")))
        self.assertEqual(list(test_iso3166_2_dk_csv.columns), self.correct_output_columns, "Expected column names don't match CSV columns:\n{test_iso3166_2_dk_csv.columns}.")
        self.assertEqual(len(test_iso3166_2_dk_csv), 5, "Expected there to be 5 rows in the exported subdivision CSV.")

        for subd in test_iso3166_2_dk_json["DK"]:
            self.assertIsNot(test_iso3166_2_dk_json["DK"][subd]["name"], None, 
                "Expected subdivision name to not be None, got {}.".format(test_iso3166_2_dk_json["DK"][subd]["name"]))
            self.assertEqual(test_iso3166_2_dk_json["DK"][subd]["name"], test_iso3166_2_dk_json["DK"][subd]["localName"],
                "Expected subdivision name and local name to be the same.")
            if not (test_iso3166_2_dk_json["DK"][subd]["parentCode"] is None):
                self.assertIn(test_iso3166_2_dk_json["DK"][subd]["parentCode"], list(test_iso3166_2_dk_json["DK"][subd].keys()), 
                    "Parent code {} not found in list of subdivision codes:\n{}.".format(test_iso3166_2_dk_json["DK"][subd]["parentCode"]), list(test_iso3166_2_dk_json["DK"][subd].keys()))
            if not (test_iso3166_2_dk_json["DK"][subd]["flag"] is None):
                self.assertEqual(os.path.splitext(test_iso3166_2_dk_json["DK"][subd]["flag"])[0], self.flag_icons_base_url + "DK/" + subd, 
                    "Expected flag URL to be {}, got {}.".format(self.flag_icons_base_url + "DK/" + subd, os.path.splitext(test_iso3166_2_dk_json["DK"][subd]["flag"])[0])) 
                self.assertEqual(requests.get(test_iso3166_2_dk_json["DK"][subd]["flag"], headers=self.user_agent_header).status_code, 200, 
                    "Flag URL invalid: {}.".format(test_iso3166_2_dk_json["DK"][subd]["flag"]))
            for key in list(test_iso3166_2_dk_json["DK"][subd].keys()):
                self.assertIn(key, self.correct_output_attributes, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_output_attributes))

        #DK-81 - Nordjylland
        self.assertEqual(test_iso3166_2_dk_json["DK"]["DK-81"]["name"], "Nordjylland", 
            "Expected subdivsion name to be Nordjylland, got {}.".format(test_iso3166_2_dk_json["DK"]["DK-81"]["name"]))  
        self.assertEqual(test_iso3166_2_dk_json["DK"]["DK-81"]["localName"], "Nordjylland", 
            "Expected subdivsion local name to be Nordjylland, got {}.".format(test_iso3166_2_dk_json["DK"]["DK-81"]["localName"]))  
        self.assertEqual(test_iso3166_2_dk_json["DK"]["DK-81"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_iso3166_2_dk_json["DK"]["DK-81"]["parentCode"]))
        self.assertEqual(test_iso3166_2_dk_json["DK"]["DK-81"]["type"], "Region", 
            "Expected subdivision type to be Region, got {}.".format(test_iso3166_2_dk_json["DK"]["DK-81"]["type"]))
        self.assertEqual(test_iso3166_2_dk_json["DK"]["DK-81"]["latLng"], [56.831, 9.493],
            "Expected subdivision latLng to be [56.831, 9.493], got {}.".format(test_iso3166_2_dk_json["DK"]["DK-81"]["latLng"]))
        self.assertEqual(test_iso3166_2_dk_json["DK"]["DK-81"]["flag"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/DK/DK-81.svg",
            "Expected subdivision flag URL to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/DK/DK-81.svg, got {}.".format(test_iso3166_2_dk_json["DK"]["DK-81"]["flag"]))
        #DK-82 - Midtjylland
        self.assertEqual(test_iso3166_2_dk_json["DK"]["DK-82"]["name"], "Midtjylland", 
            "Expected subdivsion name to be Midtjylland, got {}.".format(test_iso3166_2_dk_json["DK"]["DK-82"]["name"]))  
        self.assertEqual(test_iso3166_2_dk_json["DK"]["DK-82"]["localName"], "Midtjylland", 
            "Expected subdivsion local name to be Midtjylland, got {}.".format(test_iso3166_2_dk_json["DK"]["DK-82"]["localName"]))  
        self.assertEqual(test_iso3166_2_dk_json["DK"]["DK-82"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_iso3166_2_dk_json["DK"]["DK-82"]["parentCode"]))
        self.assertEqual(test_iso3166_2_dk_json["DK"]["DK-82"]["type"], "Region", 
            "Expected subdivision type to be Region, got {}.".format(test_iso3166_2_dk_json["DK"]["DK-82"]["type"]))
        self.assertEqual(test_iso3166_2_dk_json["DK"]["DK-82"]["latLng"], [56.302, 9.303],
            "Expected subdivision latLng to be [56.302, 9.303], got {}.".format(test_iso3166_2_dk_json["DK"]["DK-82"]["latLng"]))
        self.assertEqual(test_iso3166_2_dk_json["DK"]["DK-82"]["flag"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/DK/DK-82.svg",
            "Expected subdivision flag URL to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/DK/DK-82.svg, got {}.".format(test_iso3166_2_dk_json["DK"]["DK-82"]["flag"]))
#2.)    
        export_iso3166_2(alpha_codes=test_alpha_fi, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1) #Finland

        #open exported json
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha_fi + ".json"))  as output_json:
            test_iso3166_2_fi_json = json.load(output_json)
        #open exported CSV
        test_iso3166_2_fi_csv = pd.read_csv(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha_fi + ".csv"))

        self.assertEqual(len(test_iso3166_2_fi_json["FI"]), 19, "Expected 19 keys/attributes in output dict, got {}.".format(len(test_iso3166_2_fi_json)))
        self.assertEqual(list(test_iso3166_2_fi_json["FI"].keys()), ["FI-01", "FI-02", "FI-03", "FI-04", "FI-05", "FI-06", "FI-07", "FI-08", "FI-09", 
            "FI-10", "FI-11", "FI-12", "FI-13", "FI-14", "FI-15", "FI-16", "FI-17", "FI-18", "FI-19"], 
                "Expected list of subdivision codes doesn't match output:\n{}.".format(list(test_iso3166_2_fi_json["FI"].keys())))   
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "-FI.csv")), 
            "Expected subdivision data to be exported to a CSV: {}.".format(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "-FI.csv")))
        self.assertEqual(list(test_iso3166_2_fi_csv.columns), self.correct_output_columns, "Expected column names don't match CSV columns:\n{test_iso3166_2_fi_csv.columns}.")
        self.assertEqual(len(test_iso3166_2_fi_csv), 19, "Expected there to be 19 rows in the exported subdivision CSV.")

        for subd in test_iso3166_2_fi_json["FI"]:
            self.assertIsNot(test_iso3166_2_fi_json["FI"][subd]["name"], None, 
                "Expected subdivision name to not be None, got {}.".format(test_iso3166_2_fi_json["FI"][subd]["name"]))
            self.assertEqual(test_iso3166_2_fi_json["FI"][subd]["name"], test_iso3166_2_fi_json["FI"][subd]["localName"],
                "Expected subdivision name and local name to be the same.")
            if not (test_iso3166_2_fi_json["FI"][subd]["parentCode"] is None):
                self.assertIn(test_iso3166_2_fi_json["FI"][subd]["parentCode"], list(test_iso3166_2_fi_json["FI"][subd].keys()), 
                    "Parent code {} not found in list of subdivision codes.".format(test_iso3166_2_fi_json["FI"][subd]["parentCode"]))
            if not (test_iso3166_2_fi_json["FI"][subd]["flag"] is None):
                self.assertEqual(os.path.splitext(test_iso3166_2_fi_json["FI"][subd]["flag"])[0], self.flag_icons_base_url + "FI/" + subd, 
                    "Expected flag URL to be {}, got {}.".format(self.flag_icons_base_url + "FI/" + subd, os.path.splitext(test_iso3166_2_fi_json["FI"][subd]["flag"])[0])) 
                self.assertEqual(requests.get(test_iso3166_2_fi_json["FI"][subd]["flag"], headers=self.user_agent_header).status_code, 200, 
                    "Flag URL invalid: {}.".format(test_iso3166_2_fi_json["FI"][subd]["flag"]))
            for key in list(test_iso3166_2_fi_json["FI"][subd].keys()):
                self.assertIn(key, self.correct_output_attributes, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_output_attributes))

        #FI-02 - Etelä-Karjala
        self.assertEqual(test_iso3166_2_fi_json["FI"]["FI-02"]["name"], "Etelä-Karjala", 
            "Expected subdivsion name to be Etelä-Karjala, got {}.".format(test_iso3166_2_fi_json["FI"]["FI-02"]["name"]))  
        self.assertEqual(test_iso3166_2_fi_json["FI"]["FI-02"]["localName"], "Etelä-Karjala", 
            "Expected subdivsion local name to be Etelä-Karjala, got {}.".format(test_iso3166_2_fi_json["FI"]["FI-02"]["localName"]))  
        self.assertEqual(test_iso3166_2_fi_json["FI"]["FI-02"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_iso3166_2_fi_json["FI"]["FI-02"]["parentCode"]))
        self.assertEqual(test_iso3166_2_fi_json["FI"]["FI-02"]["type"], "Region", 
            "Expected subdivision type to be Region, got {}.".format(test_iso3166_2_fi_json["FI"]["FI-02"]["type"]))
        self.assertEqual(test_iso3166_2_fi_json["FI"]["FI-02"]["latLng"], [61.203, 28.623],
            "Expected subdivision latLng to be [61.203, 28.623], got {}.".format(test_iso3166_2_fi_json["FI"]["FI-02"]["latLng"]))
        self.assertEqual(test_iso3166_2_fi_json["FI"]["FI-02"]["flag"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/FI/FI-02.svg",
            "Expected subdivision flag URL to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/FI/FI-02.svg, got {}.".format(test_iso3166_2_fi_json["FI"]["FI-02"]["flag"]))
        #FI-17 - Satakunda
        self.assertEqual(test_iso3166_2_fi_json["FI"]["FI-17"]["name"], "Satakunta", 
            "Expected subdivsion name to be Satakunta, got {}.".format(test_iso3166_2_fi_json["FI"]["FI-17"]["name"]))  
        self.assertEqual(test_iso3166_2_fi_json["FI"]["FI-17"]["localName"], "Satakunta", 
            "Expected subdivsion local name to be Satakunta, got {}.".format(test_iso3166_2_fi_json["FI"]["FI-17"]["localName"]))  
        self.assertEqual(test_iso3166_2_fi_json["FI"]["FI-17"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_iso3166_2_fi_json["FI"]["FI-17"]["parentCode"]))
        self.assertEqual(test_iso3166_2_fi_json["FI"]["FI-17"]["type"], "Region", 
            "Expected subdivision type to be Region, got {}.".format(test_iso3166_2_fi_json["FI"]["FI-17"]["type"]))
        self.assertEqual(test_iso3166_2_fi_json["FI"]["FI-17"]["latLng"], [61.593, 22.148],
            "Expected subdivision latLng to be [61.593, 22.148], got {}.".format(test_iso3166_2_fi_json["FI"]["FI-17"]["latLng"]))
        self.assertEqual(test_iso3166_2_fi_json["FI"]["FI-17"]["flag"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/FI/FI-17.svg",
            "Expected subdivision flag URL to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/FI/FI-17.svg, got {}.".format(test_iso3166_2_fi_json["FI"]["FI-17"]["flag"]))
#3.)
        export_iso3166_2(test_alpha_np, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1) #Nepal

        #open exported json
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-" + "NP" + ".json")) as output_json:
            test_iso3166_2_np_json = json.load(output_json)
        #open exported CSV
        test_iso3166_2_np_csv = pd.read_csv(os.path.join(self.test_output_dir, self.test_output_filename + "-" + "NP" + ".csv"))

        self.assertEqual(len(test_iso3166_2_np_json["NP"]), 7, "Expected 7 keys/attributes in output dict, got {}.".format(len(test_iso3166_2_np_json)))
        self.assertEqual(list(test_iso3166_2_np_json["NP"].keys()), ["NP-P1", "NP-P2", "NP-P3", "NP-P4", "NP-P5", "NP-P6", "NP-P7"], 
            "Expected list of subdivision codes doesn't match output:\n{}.".format(list(test_iso3166_2_np_json["NP"].keys())))  
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "-NP.csv")), 
            "Expected subdivision data to be exported to a CSV: {}.".format(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "-NP.csv"))) 
        self.assertEqual(list(test_iso3166_2_np_csv.columns), self.correct_output_columns, "Expected column names don't match CSV columns:\n{test_iso3166_2_np_csv.columns}.")
        self.assertEqual(len(test_iso3166_2_np_csv), 7, "Expected there to be 7 rows in the exported subdivision CSV.")
        
        for subd in test_iso3166_2_np_json["NP"]:
            self.assertIsNot(test_iso3166_2_np_json["NP"][subd]["name"], None, 
                "Expected subdivision name to not be None, got {}.".format(test_iso3166_2_np_json["NP"][subd]["name"]))
            self.assertEqual(test_iso3166_2_np_json["NP"][subd]["name"], test_iso3166_2_np_json["NP"][subd]["localName"],
                "Expected subdivision name and local name to be the same.")
            if not (test_iso3166_2_np_json["NP"][subd]["parentCode"] is None):
                self.assertIn(test_iso3166_2_np_json["NP"][subd]["parentCode"], list(test_iso3166_2_np_json["NP"][subd].keys()), 
                    "Parent code {} not found in list of subdivision codes.".format(test_iso3166_2_np_json["NP"][subd]["parentCode"]))
            if not (test_iso3166_2_np_json["NP"][subd]["flag"] is None):
                self.assertEqual(os.path.splitext(test_iso3166_2_np_json["NP"][subd]["flag"])[0], self.flag_icons_base_url + "NP/" + subd, 
                    "Expected flag URL to be {}, got {}.".format(self.flag_icons_base_url + "NP/" + subd, os.path.splitext(test_iso3166_2_np_json["NP"][subd]["flag"])[0])) 
                self.assertEqual(requests.get(test_iso3166_2_np_json["NP"][subd]["flag"], headers=self.user_agent_header).status_code, 200, 
                    "Flag URL invalid: {}.".format(test_iso3166_2_np_json["NP"][subd]["flag"]))
            for key in list(test_iso3166_2_np_json["NP"][subd].keys()):
                self.assertIn(key, self.correct_output_attributes, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_output_attributes))
        self.assertFalse(any(x in list(test_iso3166_2_np_json["NP"].keys()) for x in ["NP-BA", "NP-BH", "NP-DH", "NP-GA", "NP-JA", "NP-KA", "NP-KO", "NP-LU", "NP-MA", "NP-ME", "NP-NA", "NP-RA", "NP-SA", "NP-SE"]),
            f"Deleted subdivisions should not be in output object:\n{list(test_iso3166_2_np_json['NP'].keys())}.")

        #NP-P1 - Koshi
        self.assertEqual(test_iso3166_2_np_json["NP"]["NP-P1"]["name"], "Koshi", 
            "Expected subdivsion name to be Koshi, got {}.".format(test_iso3166_2_np_json["NP"]["NP-P1"]["name"]))  
        self.assertEqual(test_iso3166_2_np_json["NP"]["NP-P1"]["localName"], "Koshi", 
            "Expected subdivsion local name to be Koshi, got {}.".format(test_iso3166_2_np_json["NP"]["NP-P1"]["localName"]))  
        self.assertEqual(test_iso3166_2_np_json["NP"]["NP-P1"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_iso3166_2_np_json["NP"]["NP-P1"]["parentCode"]))
        self.assertEqual(test_iso3166_2_np_json["NP"]["NP-P1"]["type"], "Province", 
            "Expected subdivision type to be Province, got {}.".format(test_iso3166_2_np_json["NP"]["NP-P1"]["type"]))
        self.assertEqual(test_iso3166_2_np_json["NP"]["NP-P1"]["latLng"], [27.337, 87.381],
            "Expected subdivision latLng to be [27.337, 87.381], got {}.".format(test_iso3166_2_np_json["NP"]["NP-P1"]["latLng"]))
        self.assertEqual(test_iso3166_2_np_json["NP"]["NP-P1"]["flag"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/NP/NP-P1.png",
            "Expected subdivision flag URL to be None, got {}.".format(test_iso3166_2_np_json["NP"]["NP-P1"]["flag"]))
        #NP
        self.assertEqual(test_iso3166_2_np_json["NP"]["NP-P3"]["name"], "Bagmati", 
            "Expected subdivsion name to be Bagmati, got {}.".format(test_iso3166_2_np_json["NP"]["NP-P3"]["name"]))  
        self.assertEqual(test_iso3166_2_np_json["NP"]["NP-P3"]["localName"], "Bagmati", 
            "Expected subdivsion local name to be Bagmati, got {}.".format(test_iso3166_2_np_json["NP"]["NP-P3"]["localName"]))  
        self.assertEqual(test_iso3166_2_np_json["NP"]["NP-P3"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_iso3166_2_np_json["NP"]["NP-P3"]["parentCode"]))
        self.assertEqual(test_iso3166_2_np_json["NP"]["NP-P3"]["type"], "Province", 
            "Expected subdivision type to be Province, got {}.".format(test_iso3166_2_np_json["NP"]["NP-P3"]["type"]))
        self.assertEqual(test_iso3166_2_np_json["NP"]["NP-P3"]["latLng"], [27.662, 85.438],
            "Expected subdivision latLng to be [27.662, 85.438], got {}.".format(test_iso3166_2_np_json["NP"]["NP-P3"]["latLng"]))
        self.assertEqual(test_iso3166_2_np_json["NP"]["NP-P3"]["flag"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/NP/NP-P3.jpeg",
            "Expected subdivision flag URL to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/NP/NP-P3.jpeg, got {}.".format(test_iso3166_2_np_json["NP"]["NP-P3"]["flag"]))
#4.)
        export_iso3166_2(alpha_codes=test_alpha_kg_mg_nr, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1) #Kyrgyzstan, Madagascar, Nauru

        #open exported json
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-" + "KG,MG,NR" + ".json")) as output_json:
            test_iso3166_2_kg_mg_nr_json = json.load(output_json)
        #open exported CSV
        test_iso3166_2_kg_mg_nr_csv = pd.read_csv(os.path.join(self.test_output_dir, self.test_output_filename + "-" + "KG,MG,NR" + ".csv"))

        self.assertEqual(len(test_iso3166_2_kg_mg_nr_json["KG"]), 9, "Expected 9 subdivisions in output dict, got {}.".format(len(test_iso3166_2_kg_mg_nr_json["KG"])))
        self.assertEqual(len(test_iso3166_2_kg_mg_nr_json["MG"]), 6, "Expected 6 subdivisions in output dict, got {}.".format(len(test_iso3166_2_kg_mg_nr_json["MG"])))
        self.assertEqual(len(test_iso3166_2_kg_mg_nr_json["NR"]), 14, "Expected 14 subdivisions in output dict, got {}.".format(len(test_iso3166_2_kg_mg_nr_json["NR"])))
        self.assertEqual(list(test_iso3166_2_kg_mg_nr_json["KG"].keys()), ['KG-B', 'KG-C', 'KG-GB', 'KG-GO', 'KG-J', 'KG-N', 'KG-O', 'KG-T', 'KG-Y'], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_iso3166_2_kg_mg_nr_json['KG'].keys())}.")   
        self.assertEqual(list(test_iso3166_2_kg_mg_nr_json["MG"].keys()), ["MG-A", "MG-D", "MG-F", "MG-M", "MG-T", "MG-U"], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_iso3166_2_kg_mg_nr_json['MG'].keys())}.")  
        self.assertEqual(list(test_iso3166_2_kg_mg_nr_json["NR"].keys()), ['NR-01', 'NR-02', 'NR-03', 'NR-04', 'NR-05', 'NR-06', 'NR-07', 'NR-08', 'NR-09', 'NR-10', 
            'NR-11', 'NR-12', 'NR-13', 'NR-14'], f"Expected list of subdivision codes doesn't match output:\n{list(test_iso3166_2_kg_mg_nr_json['NR'].keys())}.")   
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "-KG,MG,NR.csv")), 
            "Expected subdivision data to be exported to a CSV: {}.".format(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "-KG,MG,NR.csv")))
        self.assertEqual(list(test_iso3166_2_kg_mg_nr_csv.columns), self.correct_output_columns, "Expected column names don't match CSV columns:\n{test_iso3166_2_kg_mg_nr_csv.columns}.")
        self.assertEqual(len(test_iso3166_2_kg_mg_nr_csv), 29, "Expected there to be 29 rows in the exported subdivision CSV.")

        for country in test_iso3166_2_kg_mg_nr_json:
            for subd in test_iso3166_2_kg_mg_nr_json[country]:
                self.assertIsNot(test_iso3166_2_kg_mg_nr_json[country][subd]["name"], None, 
                    "Expected subdivision name to not be None, got {}.".format(test_iso3166_2_kg_mg_nr_json[country][subd]["name"]))
                if not (test_iso3166_2_kg_mg_nr_json[country][subd]["parentCode"] is None):
                    self.assertIn(test_iso3166_2_kg_mg_nr_json[country][subd]["parentCode"], list(test_iso3166_2_kg_mg_nr_json[country][subd].keys()), 
                        "Parent code {} not found in list of subdivision codes.".format(test_iso3166_2_kg_mg_nr_json[country][subd]["parentCode"]))
                if not (test_iso3166_2_kg_mg_nr_json[country][subd]["flag"] is None):
                    self.assertEqual(os.path.splitext(test_iso3166_2_kg_mg_nr_json[country][subd]["flag"])[0], self.flag_icons_base_url + country + "/" + subd, 
                        "Expected flag URL to be {}, got {}.".format(self.flag_icons_base_url + country + "/" + subd, os.path.splitext(test_iso3166_2_kg_mg_nr_json[country][subd]["flag"])[0])) 
                    self.assertEqual(requests.get(test_iso3166_2_kg_mg_nr_json[country][subd]["flag"], headers=self.user_agent_header).status_code, 200, 
                        "Flag URL invalid: {}.".format(test_iso3166_2_kg_mg_nr_json[country][subd]["flag"]))
                for key in list(test_iso3166_2_kg_mg_nr_json[country][subd].keys()):
                    self.assertIn(key, self.correct_output_attributes, "Attribute {} not found in list of correct attributes:\n{}.".format(key, self.correct_output_attributes))
        
        #KG-GB - Bishkek Shaary
        self.assertEqual(test_iso3166_2_kg_mg_nr_json["KG"]["KG-GB"]["name"], "Bishkek Shaary", 
            "Expected subdivsion name to be Bishkek Shaary, got {}.".format(test_iso3166_2_kg_mg_nr_json["KG"]["KG-GB"]["name"]))  
        self.assertEqual(test_iso3166_2_kg_mg_nr_json["KG"]["KG-GB"]["localName"], "Bishkek Shaary", 
            "Expected subdivsion local name to be Bishkek Shaary, got {}.".format(test_iso3166_2_kg_mg_nr_json["KG"]["KG-GB"]["localName"]))  
        self.assertEqual(test_iso3166_2_kg_mg_nr_json["KG"]["KG-GB"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_iso3166_2_kg_mg_nr_json["KG"]["KG-GB"]["parentCode"]))
        self.assertEqual(test_iso3166_2_kg_mg_nr_json["KG"]["KG-GB"]["type"], "City", 
            "Expected subdivision type to be City, got {}.".format(test_iso3166_2_kg_mg_nr_json["KG"]["KG-GB"]["type"]))
        self.assertEqual(test_iso3166_2_kg_mg_nr_json["KG"]["KG-GB"]["latLng"], [42.875, 74.57],
            "Expected subdivision latLng to be [42.875, 74.57], got {}.".format(test_iso3166_2_kg_mg_nr_json["KG"]["KG-GB"]["latLng"]))
        self.assertEqual(test_iso3166_2_kg_mg_nr_json["KG"]["KG-GB"]["flag"], "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/KG/KG-GB.svg",
            "Expected subdivision flag URL to be https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/KG/KG-GB.svg, got {}.".format(test_iso3166_2_kg_mg_nr_json["KG"]["KG-GB"]["flag"]))
        #MG-D - Antsiranana
        self.assertEqual(test_iso3166_2_kg_mg_nr_json["MG"]["MG-D"]["name"], "Antsiranana", 
            "Expected subdivsion name to be Antsiranana, got {}.".format(test_iso3166_2_kg_mg_nr_json["MG"]["MG-D"]["name"]))  
        self.assertEqual(test_iso3166_2_kg_mg_nr_json["MG"]["MG-D"]["localName"], "Antsiranana", 
            "Expected subdivsion local name to be Antsiranana, got {}.".format(test_iso3166_2_kg_mg_nr_json["MG"]["MG-D"]["localName"]))  
        self.assertEqual(test_iso3166_2_kg_mg_nr_json["MG"]["MG-D"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_iso3166_2_kg_mg_nr_json["MG"]["MG-D"]["parentCode"]))
        self.assertEqual(test_iso3166_2_kg_mg_nr_json["MG"]["MG-D"]["type"], "Province", 
            "Expected subdivision type to be Province, got {}.".format(test_iso3166_2_kg_mg_nr_json["MG"]["MG-D"]["type"]))
        self.assertEqual(test_iso3166_2_kg_mg_nr_json["MG"]["MG-D"]["latLng"], [-12.323, 49.294],
            "Expected subdivision latLng to be [-12.323, 49.294], got {}.".format(test_iso3166_2_kg_mg_nr_json["MG"]["MG-D"]["latLng"]))
        self.assertEqual(test_iso3166_2_kg_mg_nr_json["MG"]["MG-D"]["flag"], None,
            "Expected subdivision flag URL to be None, got {}.".format(test_iso3166_2_kg_mg_nr_json["MG"]["MG-D"]["flag"]))
        #NR-02 - Anabar
        self.assertEqual(test_iso3166_2_kg_mg_nr_json["NR"]["NR-02"]["name"], "Anabar", 
            "Expected subdivsion name to be Anabar, got {}.".format(test_iso3166_2_kg_mg_nr_json["NR"]["NR-02"]["name"]))  
        self.assertEqual(test_iso3166_2_kg_mg_nr_json["NR"]["NR-02"]["localName"], "Anabar", 
            "Expected subdivsion local name to be Anabar, got {}.".format(test_iso3166_2_kg_mg_nr_json["NR"]["NR-02"]["localName"]))  
        self.assertEqual(test_iso3166_2_kg_mg_nr_json["NR"]["NR-02"]["parentCode"], None, 
            "Expected subdivision parent code to be None, got {}.".format(test_iso3166_2_kg_mg_nr_json["NR"]["NR-02"]["parentCode"]))
        self.assertEqual(test_iso3166_2_kg_mg_nr_json["NR"]["NR-02"]["type"], "District", 
            "Expected subdivision type to be District, got {}.".format(test_iso3166_2_kg_mg_nr_json["NR"]["NR-02"]["type"]))
        self.assertEqual(test_iso3166_2_kg_mg_nr_json["NR"]["NR-02"]["latLng"], [-0.511, 166.954],
            "Expected subdivision latLng to be [-0.513, 166.948], got {}.".format(test_iso3166_2_kg_mg_nr_json["NR"]["NR-02"]["latLng"]))
        self.assertEqual(test_iso3166_2_kg_mg_nr_json["NR"]["NR-02"]["flag"], None,
            "Expected subdivision flag URL to be None, got {}.".format(test_iso3166_2_kg_mg_nr_json["NR"]["NR-02"]["flag"]))
#5.)
        with (self.assertRaises(ValueError)):
            export_iso3166_2(alpha_codes=test_alpha_error1, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0) #ZZ
            export_iso3166_2(alpha_codes=test_alpha_error2, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0) #ABCDEF
            export_iso3166_2(alpha_codes=test_alpha_error3, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0) #1234
#6.)
        with (self.assertRaises(TypeError)):
            export_iso3166_2(alpha_codes=123)
            export_iso3166_2(alpha_codes=True)
            
    def test_export_iso3166_restcountries(self):
        """ Testing export functionality for getting ISO 3166-2 subdivision data from data sources, including additional RestCountries API attributes. """
        test_alpha_gt = "GT" #Guatemala
        test_alpha_ir = "IRN" #Iran
        test_alpha_mg = "450" #Madagascar
        test_rest_countries_keys_error1 = "ZZ"
        test_rest_countries_keys_error2 = "ABCDEF"
        test_rest_countries_keys_error3 = 1234    
#1.)
        export_iso3166_2(alpha_codes=test_alpha_gt, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1,
                         rest_countries_keys="continents,subregion") #Guatemala - including additional continent and region attributes
        expected_attribute_list = self.correct_output_attributes + ["continents", "subregion"]

        #open exported json
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-" + "GT" + ".json")) as output_json:
            test_iso3166_2_gt_json = json.load(output_json)
        #open exported CSV
        test_iso3166_2_gt_csv = pd.read_csv(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha_gt + ".csv"))

        self.assertEqual(len(test_iso3166_2_gt_json["GT"]), 22, f"Expected 22 subdivisions in output dict, got {len(test_iso3166_2_gt_json['GT'])}.")
        self.assertEqual(list(test_iso3166_2_gt_json["GT"].keys()), ['GT-01', 'GT-02', 'GT-03', 'GT-04', 'GT-05', 'GT-06', 'GT-07', 'GT-08', 'GT-09', 'GT-10', 'GT-11', 
                                                            'GT-12', 'GT-13', 'GT-14', 'GT-15', 'GT-16', 'GT-17', 'GT-18', 'GT-19', 'GT-20', 'GT-21', 'GT-22'], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_iso3166_2_gt_json['GT'].keys())}.")   
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "-GT.csv")), 
            "Expected subdivision data to be exported to a CSV: {}.".format(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "-GT.csv")))
        self.assertEqual(list(test_iso3166_2_gt_csv.columns), self.correct_output_columns + ["continents", "subregion"], f"Expected column names don't match CSV columns:\n{test_iso3166_2_gt_csv.columns}.")
        self.assertEqual(len(test_iso3166_2_gt_csv), 6, "Expected there to be 6 rows in the exported subdivision CSV.")

        for country in test_iso3166_2_gt_json:
            for subd in test_iso3166_2_gt_json[country]:
                for key in list(test_iso3166_2_gt_json[country][subd].keys()):
                    self.assertIn(key, expected_attribute_list, f"Attribute {key} not found in list of correct attributes:\n{expected_attribute_list}.")
                self.assertEqual(test_iso3166_2_gt_json[country][subd]["continents"], "North America", 
                        f"Expected attribute value to be North America, got {test_iso3166_2_gt_json[country][subd]['continents']}.")
                self.assertEqual(test_iso3166_2_gt_json[country][subd]["subregion"], "Central America", 
                        f"Expected attribute value to be Central America, got {test_iso3166_2_gt_json[country][subd]['subregion']}.")
#2.)
        export_iso3166_2(alpha_codes=test_alpha_ir, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1,
                         rest_countries_keys="languages,startOfWeek,region") #Iran - including additional languages, startOfWeek and region attributes
        expected_attribute_list = self.correct_output_attributes + ["languages", "startOfWeek", "region"]

        #open exported json
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha_ir + ".json")) as output_json:
            test_iso3166_2_ir_json = json.load(output_json)
        #open exported CSV
        test_iso3166_2_ir_csv = pd.read_csv(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha_ir + ".csv"))
    
        self.assertEqual(len(test_iso3166_2_ir_json["IR"]), 31, f"Expected 31 subdivisions in output dict, got {len(test_iso3166_2_ir_json['IR'])}.")
        self.assertEqual(list(test_iso3166_2_ir_json["IR"].keys()), ['IR-00', 'IR-01', 'IR-02', 'IR-03', 'IR-04', 'IR-05', 'IR-06', 'IR-07', 'IR-08', 'IR-09', 'IR-10', 
                                                            'IR-11', 'IR-12', 'IR-13', 'IR-14', 'IR-15', 'IR-16', 'IR-17', 'IR-18', 'IR-19', 'IR-20', 'IR-21', 
                                                            'IR-22', 'IR-23', 'IR-24', 'IR-25', 'IR-26', 'IR-27', 'IR-28', 'IR-29', 'IR-30'],
            f"Expected list of subdivision codes doesn't match output:\n{list(test_iso3166_2_ir_json['IR'].keys())}.")   
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "-IR.csv")), 
            "Expected subdivision data to be exported to a CSV: {}.".format(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "-IR.csv")))
        self.assertEqual(list(test_iso3166_2_ir_csv.columns), self.correct_output_columns + ["languages", "region", "startOfWeek"], f"Expected column names don't match CSV columns:\n{test_iso3166_2_ir_csv.columns}.")
        self.assertEqual(len(test_iso3166_2_ir_csv), 6, "Expected there to be 6 rows in the exported subdivision CSV.")

        for country in test_iso3166_2_ir_json:
            for subd in test_iso3166_2_ir_json[country]:
                for key in list(test_iso3166_2_ir_json[country][subd].keys()):
                    self.assertIn(key, expected_attribute_list, f"Attribute {key} not found in list of correct attributes:\n{expected_attribute_list}.")
                self.assertEqual(test_iso3166_2_ir_json[country][subd]["languages"], {"fas": "Persian (Farsi)"}, 
                        f"Expected attribute value to be Persian (Farsi), got {test_iso3166_2_ir_json[country][subd]['languages']}.")
                self.assertEqual(test_iso3166_2_ir_json[country][subd]["startOfWeek"], "saturday", 
                        f"Expected attribute value to be saturday, got {test_iso3166_2_ir_json[country][subd]['startOfWeek']}.")
                self.assertEqual(test_iso3166_2_ir_json[country][subd]["region"], "Asia", 
                        f"Expected attribute value to be Asia, got {test_iso3166_2_ir_json[country][subd]['region']}.")
#3.)
        export_iso3166_2(alpha_codes=test_alpha_mg, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1,
                         rest_countries_keys="idd,currencies,postalCode") #Madagascar - including additional idd, currencies and postalCode attributes
        expected_attribute_list = self.correct_output_attributes + ["idd", "currencies", "postalCode"]

        #open exported json
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha_mg + ".json")) as output_json:
            test_iso3166_2_mg_json = json.load(output_json)
        #open exported CSV
        test_iso3166_2_mg_csv = pd.read_csv(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha_mg + ".csv"))

        self.assertEqual(len(test_iso3166_2_mg_json["MG"]), 6, f"Expected 6 subdivisions in output dict, got {len(test_iso3166_2_mg_json['MG'])}.")
        self.assertEqual(list(test_iso3166_2_mg_json["MG"].keys()), ['MG-A', 'MG-D', 'MG-F', 'MG-M', 'MG-T', 'MG-U'], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_iso3166_2_mg_json['MG'].keys())}.")   
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "-MG.csv")), 
            "Expected subdivision data to be exported to a CSV: {}.".format(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "-MG.csv")))
        self.assertEqual(list(test_iso3166_2_mg_csv.columns), self.correct_output_columns + ["currencies", "idd", "postalCode"], f"Expected column names don't match CSV columns:\n{test_iso3166_2_mg_csv.columns}.")
        self.assertEqual(len(test_iso3166_2_mg_csv), 6, "Expected there to be 6 rows in the exported subdivision CSV.")

        for country in test_iso3166_2_mg_json:
            for subd in test_iso3166_2_mg_json[country]:
                for key in list(test_iso3166_2_mg_json[country][subd].keys()):
                    self.assertIn(key, expected_attribute_list, f"Attribute {key} not found in list of correct attributes:\n{expected_attribute_list}.")
                self.assertEqual(test_iso3166_2_mg_json[country][subd]["idd"], {"root": "+2", "suffixes": ["61"]}, 
                        f"Expected attribute value to be root: +2, suffixes: 61, got {test_iso3166_2_mg_json[country][subd]['idd']}.")
                self.assertEqual(test_iso3166_2_mg_json[country][subd]["currencies"], {"MGA": {"name": "Malagasy ariary", "symbol": "Ar"}}, 
                        f"Expected attribute value to be MGA: name:Malagasy ariary, symbol:Ar, got {test_iso3166_2_mg_json[country][subd]['currencies']}.")
                self.assertEqual(test_iso3166_2_mg_json[country][subd]["postalCode"], "Format: ###, Regex: ^(\d{3})$", 
                        f"Expected attribute value to be Format: ###, Regex: ^(\d{3})$, got {test_iso3166_2_mg_json[country][subd]['postalCode']}.")
#4.)
        with (self.assertRaises(ValueError)):
            export_iso3166_2(export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, rest_countries_keys=test_rest_countries_keys_error1) #ZZ
            export_iso3166_2(export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, rest_countries_keys=test_rest_countries_keys_error2) #ABCDEF
            export_iso3166_2(export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, rest_countries_keys=test_rest_countries_keys_error3) #1234

    # @unittest.skip("")
    def test_export_exclude_default_attributes(self):
        """ Testing export functionality for getting ISO 3166-2 subdivision data from data sources, with some default attributes excluded. """
        test_alpha_ge = "GE" #Georgia
        test_alpha_gw = "GNB" #Guinea-Bissau
        test_alpha_ki = "296" #Kiribati
        test_exclude_keys_error1 = "ZZ"
        test_exclude_keys_error2 = "ABCDEF"
        test_exclude_keys_error3 = 1234    
#1.)
        export_iso3166_2(alpha_codes=test_alpha_ge, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1,
                         exclude_default_keys="latLng, type") #Georgia - excluding the latLng and type default attributes 
    
        #open exported json
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-GE.json")) as output_json:
            test_alpha_ge_json = json.load(output_json)
        #open exported CSV
        test_iso3166_2_ge_csv = pd.read_csv(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha_ge + ".csv"))

        self.assertEqual(len(test_alpha_ge_json["GE"]), 12, f"Expected 12 subdivisions in output dict, got {len(test_alpha_ge_json['GE'])}.")
        self.assertEqual(list(test_alpha_ge_json["GE"].keys()), ['GE-AB', 'GE-AJ', 'GE-GU', 'GE-IM', 'GE-KA', 'GE-KK', 'GE-MM', 'GE-RL', 'GE-SJ', 'GE-SK', 'GE-SZ', 'GE-TB'], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_alpha_ge_json['GE'].keys())}.")   
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "-GE.csv")), 
            "Expected subdivision data to be exported to a CSV: {}.".format(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "-GE.csv")))
        self.assertEqual(list(test_iso3166_2_ge_csv.columns), ["alpha_code", "subdivision_code", "name", "localName", "parentCode", "flag"], f"Expected column names don't match CSV columns:\n{test_iso3166_2_ge_csv.columns}.")
        self.assertEqual(len(test_iso3166_2_ge_csv), 12, "Expected there to be 12 rows in the exported subdivision CSV.")
        for country in test_alpha_ge_json:
            for subd in test_alpha_ge_json[country]:
                self.assertNotIn("latLng", list(test_alpha_ge_json[country][subd].keys()), 
                    f"Expected latLng default attribute to not be in subdivision attributes:\n{list(test_alpha_ge_json[country][subd].keys())}.")
                self.assertNotIn("type", list(test_alpha_ge_json[country][subd].keys()), 
                    f"Expected type default attribute to not be in subdivision attributes:\n{list(test_alpha_ge_json[country][subd].keys())}.")
#2.) 
        export_iso3166_2(alpha_codes=test_alpha_gw, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1,
                         exclude_default_keys="localName, name") #Guinea-Bissau - excluding the localName and name default attributes 
    
        #open exported json
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-GW.json")) as output_json:
            test_iso3166_2_gw_json = json.load(output_json)
        #open exported CSV
        test_iso3166_2_gw_csv = pd.read_csv(os.path.join(self.test_output_dir, self.test_output_filename + "-GW.csv"))

        self.assertEqual(len(test_iso3166_2_gw_json["GW"]), 12, f"Expected 12 subdivisions in output dict, got {len(test_iso3166_2_gw_json['GW'])}.")
        self.assertEqual(list(test_iso3166_2_gw_json["GW"].keys()), ['GW-BA', 'GW-BL', 'GW-BM', 'GW-BS', 'GW-CA', 'GW-GA', 'GW-L', 'GW-N', 'GW-OI', 'GW-QU', 'GW-S', 'GW-TO'], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_iso3166_2_gw_json['GW'].keys())}.")   
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "-GW.csv")), 
            "Expected subdivision data to be exported to a CSV: {}.".format(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "-GW.csv")))
        self.assertEqual(list(test_iso3166_2_gw_csv.columns), ["alpha_code", "subdivision_code", "type", "parentCode", "flag", "latLng"], f"Expected column names don't match CSV columns:\n{test_iso3166_2_gw_csv.columns}.")
        self.assertEqual(len(test_iso3166_2_gw_csv), 12, "Expected there to be 12 rows in the exported subdivision CSV.")
        for country in test_iso3166_2_gw_json:
            for subd in test_iso3166_2_gw_json[country]:
                self.assertNotIn("localName", list(test_iso3166_2_gw_json[country][subd].keys()), 
                    f"Expected localName default attribute to not be in subdivision attributes:\n{list(test_iso3166_2_gw_json[country][subd].keys())}.")
                self.assertNotIn("name", list(test_iso3166_2_gw_json[country][subd].keys()), 
                    f"Expected name default attribute to not be in subdivision attributes:\n{list(test_iso3166_2_gw_json[country][subd].keys())}.")
#3.)
        export_iso3166_2(alpha_codes=test_alpha_ki, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1,
                         exclude_default_keys="name, parentCode, flag") #Kiribati - excluding the name, parentCode and flag default attributes 
    
        #open exported json
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-KI.json")) as output_json:
            test_iso3166_2_ki_json = json.load(output_json)
        #open exported CSV
        test_iso3166_2_ki_csv = pd.read_csv(os.path.join(self.test_output_dir, self.test_output_filename + "-KI.csv"))

        self.assertEqual(len(test_iso3166_2_ki_json["KI"]), 3, f"Expected 3 subdivisions in output dict, got {len(test_iso3166_2_ki_json['KI'])}.")
        self.assertEqual(list(test_iso3166_2_ki_json["KI"].keys()), ['KI-G', 'KI-L', 'KI-P'], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_iso3166_2_ki_json['KI'].keys())}.")   
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "-KI.csv")), 
            "Expected subdivision data to be exported to a CSV: {}.".format(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "-KI.csv")))
        self.assertEqual(list(test_iso3166_2_ki_csv.columns), ["alpha_code", "subdivision_code", "localName", "type", "latLng"], f"Expected column names don't match CSV columns:\n{test_iso3166_2_ki_csv.columns}.")
        self.assertEqual(len(test_iso3166_2_ki_csv), 3, "Expected there to be 3 rows in the exported subdivision CSV.")        
        for country in test_iso3166_2_ki_json:
            for subd in test_iso3166_2_ki_json[country]:
                self.assertNotIn("parentCode", list(test_iso3166_2_ki_json[country][subd].keys()), 
                    f"Expected parentCode default attribute to not be in subdivision attributes:\n{list(test_iso3166_2_ki_json[country][subd].keys())}.")
                self.assertNotIn("name", list(test_iso3166_2_ki_json[country][subd].keys()), 
                    f"Expected name default attribute to not be in subdivision attributes:\n{list(test_iso3166_2_ki_json[country][subd].keys())}.")
                self.assertNotIn("flag", list(test_iso3166_2_ki_json[country][subd].keys()), 
                    f"Expected flag default attribute to not be in subdivision attributes:\n{list(test_iso3166_2_ki_json[country][subd].keys())}.")
#4.)
        with (self.assertRaises(ValueError)):
            export_iso3166_2(export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, exclude_default_keys=test_exclude_keys_error1) #ZZ
            export_iso3166_2(export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, exclude_default_keys=test_exclude_keys_error2) #ABCDEF
            export_iso3166_2(export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, exclude_default_keys=test_exclude_keys_error3) #1234

    def tearDown(self):
        """ Delete any temp export folder. """
        shutil.rmtree(self.test_output_dir)

if __name__ == '__main__':  
    #run all unit tests
    unittest.main(verbosity=2)    