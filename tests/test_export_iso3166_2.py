from scripts.export_iso3166_2 import *
import requests
import json
import os
from fake_useragent import UserAgent
from importlib.metadata import metadata
import xml.etree.ElementTree as ET
import shutil
import unittest
from unittest.mock import patch
import io
import warnings
unittest.TestLoader.sortTestMethodsUsing = None

#ignore resource warnings
warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

# @unittest.skip("Skipping export_iso3166_2 tests.")
class Export_ISO3166_2_Tests(unittest.TestCase):
    """
    Test suite for testing export_iso3166_2.py script that has the full export pipeline that
    pulls all the ISO 3166-2 subdivision data for all countries from the data sources. 

    Test Cases
    ==========
    test_export_iso3166_2:
        testing correct ISO 3166-2 data is exported and pulled from data sources and
        output to the JSON, CSV and XML files.
    test_export_iso3166_restcountries:
        testing correct ISO 3166-2 data is exported and pulled from data sources,
        with additional attributes from RestCountries exported.
    test_export_filter_attributes:
        testing correct ISO 3166-2 data is exported and pulled from data sources,
        with some of the default attributes filtered from export.
    test_export_iso3166_2_alpha_code_range:
        testing correct ISO 3166-2 data is exported and pulled from data sources to 
        and from the inputted alpha codes via the alpha_codes_range parameter.
    test_export_history:
        testing correct ISO 3166-2 data is exported when the subdivision historical 
        data is included in the data export.
    test_export_city_data:
        testing correct ISO 3166-2 data is exported when the city-level subdivision 
        data is included in the data export.
    test_export_lat_lng:
        testing functionality for exporting the latLng attribute using Google Maps API.
    test_save_each_iteration:
        testing save_each_iteration parameter in extract function that saves the subdivision
        export per iteration rather than just at the end all in one go.
    """
    @classmethod
    def setUp(self):
        """ Initialise test variables. """
        #initalise User-agent header for requests library 
        self.__version__ = metadata('iso3166-2')['version']
        self.user_agent_header = UserAgent().random

        self.test_output_dir = os.path.join("tests", "test_output_dir")
        self.test_output_filename = "test_iso3166_2_output"
        
        #create output dir if not already present
        if not (os.path.isdir(self.test_output_dir)):
            os.makedirs(self.test_output_dir)

        #list of output columns for main iso3166-2 json
        self.correct_default_output_attributes = ["name", "localOtherName", "type", "parentCode", "flag", "latLng"]

        #list of output columns for iso3166-2 CSV
        self.correct_default_output_columns = ["alphaCode", "subdivisionCode", "name", "localOtherName", "type", "parentCode", "flag", "latLng"]

        #turn off tqdm progress bar functionality when running tests
        os.environ["TQDM_DISABLE"] = "1"

        #base url for flag icons on iso3166-flags repo
        # self.flag_icons_base_url = "https://github.com/amckenna41/iso3166-flags/blob/main/iso3166-2-flags/"
        self.flag_icons_base_url = "https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/"

        #patch sys.stdout such that any print statements/outputs from the individual test cases aren't run
        # self.patcher = patch('sys.stdout', new_callable=io.StringIO)
        # self.mock_stdout = self.patcher.start()
    
    # @unittest.skip("")  
    def test_export_iso3166_2(self):
        """ Testing export functionality for getting ISO 3166-2 subdivision data from data sources. """
        test_alpha_dk = "DK" #Denmark
        test_alpha_fi = "FI" #Finland
        test_alpha_nz = "NZL" #New Zealand
        test_alpha_kg_mg_nr = "KG,MDG,520" #Kyrgyzstan, Madagascar, Nauru
        test_alpha_error1 = "ZZ"
        test_alpha_error2 = "ABCDEF"
        test_alpha_error3 = 1234
#1.)
        export_iso3166_2(alpha_codes=test_alpha_dk, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, 
                         export_csv=1, export_xml=1, extract_lat_lng=False, history=False) #Denmark
        
        #open exported json, csv and xml
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "_" + test_alpha_dk + ".json"))  as output_json:
            test_iso3166_2_dk_json = json.load(output_json)
        test_iso3166_2_dk_csv = pd.read_csv(os.path.join(self.test_output_dir, f'{self.test_output_filename}_{test_alpha_dk}.csv'))
        test_iso3166_2_dk_xml = ET.parse(os.path.join(self.test_output_dir, f'{self.test_output_filename}_{test_alpha_dk}.xml'))
        
        self.assertEqual(len(test_iso3166_2_dk_json["DK"]), 5, f"Expected 5 subdivisions to be in output dict, got {len(test_iso3166_2_dk_json['DK'])}.")
        self.assertEqual(list(test_iso3166_2_dk_json["DK"].keys()), ['DK-81', 'DK-82', 'DK-83', 'DK-84', 'DK-85'], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_iso3166_2_dk_json['DK'].keys())}.")   
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "_DK.csv")), 
            f"Expected subdivision data to be exported to a CSV: {os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0])}-DK.csv.")
        self.assertEqual(list(test_iso3166_2_dk_csv.columns), self.correct_default_output_columns[1:], 
            f"Expected column names don't match CSV columns:\n{test_iso3166_2_dk_csv.columns}.")
        self.assertEqual(len(test_iso3166_2_dk_csv), 5, "Expected there to be 5 rows in the exported subdivision CSV.")
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "_DK.xml")), 
            f"Expected subdivision data to be exported to an XML: {os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0])}-DK.xml.")
        self.assertEqual([elem.tag for elem in test_iso3166_2_dk_xml.getroot()], [test_alpha_dk], f"Expected top-level element DK does not match output, got {list(test_iso3166_2_dk_xml.getroot())}.")
        self.assertEqual(len(test_iso3166_2_dk_xml.find("DK")), 5, f"Expected 5 sub-level elements (subdivisions) in the output xml, got {len(test_iso3166_2_dk_xml.find('DK'))}.")
        for top_level in test_iso3166_2_dk_xml.getroot():
            for second_level in top_level:
                self.assertEqual(set([child.tag for child in second_level]), set(self.correct_default_output_attributes), 
                                 f"Expected second-level names in XML do match attributes, got {[child.tag for child in second_level]}.")

        for subd in test_iso3166_2_dk_json["DK"]:
            self.assertIsNot(test_iso3166_2_dk_json["DK"][subd]["name"], None, 
                f"Expected subdivision name to not be None, got {test_iso3166_2_dk_json['DK'][subd]['name']}.")
            if not (test_iso3166_2_dk_json["DK"][subd]["parentCode"] is None):
                self.assertIn(test_iso3166_2_dk_json["DK"][subd]["parentCode"], list(test_iso3166_2_dk_json["DK"][subd].keys()), 
                    f"Parent code {test_iso3166_2_dk_json['DK'][subd]['parentCode']} not found in list of subdivision codes:\n{list(test_iso3166_2_dk_json['DK'][subd].keys())}.")
            if not (test_iso3166_2_dk_json["DK"][subd]["flag"] is None):
                self.assertEqual(os.path.splitext(test_iso3166_2_dk_json["DK"][subd]["flag"])[0], self.flag_icons_base_url + "DK/" + subd, 
                    f"Expected flag URL to be {self.flag_icons_base_url}DK{subd}, got {os.path.splitext(test_iso3166_2_dk_json['DK'][subd]['flag'])[0]}.") 
                # self.assertEqual(requests.get(test_iso3166_2_dk_json["DK"][subd]["flag"], headers={"User-Agent": self.user_agent_header}).status_code, 200, 
                #     f"Flag URL invalid: {test_iso3166_2_dk_json['DK'][subd]['flag']}.")
            for key in list(test_iso3166_2_dk_json["DK"][subd].keys()):
                self.assertIn(key, self.correct_default_output_attributes, f"Attribute {key} not found in list of correct attributes:\n{self.correct_default_output_attributes}.")
        
        #DK-81 - Nordjylland
        test_iso3166_2_dk_json_dk_81_expected = {"name": "Nordjylland", "localOtherName": "North Denmark (eng), North Jutland Region (eng)", "parentCode": None, 
            "type": "Region", "flag": "https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/DK/DK-81.svg", "latLng": None}
        self.assertEqual(test_iso3166_2_dk_json_dk_81_expected, test_iso3166_2_dk_json["DK"]["DK-81"], 
            f"Expected and observed subdivision output for DK-81 do not match:\n{test_iso3166_2_dk_json_dk_81_expected}\n{test_iso3166_2_dk_json['DK']['DK-81']}.")
        #DK-82 - Midtjylland
        test_iso3166_2_dk_json_dk_82_expected = {"name": "Midtjylland", "localOtherName": "Central Denmark (eng), Central Jutland Region (eng), Mid-Jutland (eng)", 
            "parentCode": None, "type": "Region", "flag": "https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/DK/DK-82.svg", "latLng": None}
        self.assertEqual(test_iso3166_2_dk_json_dk_82_expected, test_iso3166_2_dk_json["DK"]["DK-82"], 
            f"Expected and observed subdivision output for DK-81 do not match:\n{test_iso3166_2_dk_json_dk_82_expected}\n{test_iso3166_2_dk_json['DK']['DK-82']}.")
#2.)    
        export_iso3166_2(alpha_codes=test_alpha_fi, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, 
                         export_xml=True, extract_lat_lng=False, history=False) #Finland

        #open exported json, csv and xml
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "_" + test_alpha_fi + ".json"))  as output_json:
            test_iso3166_2_fi_json = json.load(output_json)
        test_iso3166_2_fi_csv = pd.read_csv(os.path.join(self.test_output_dir, f'{self.test_output_filename}_{test_alpha_fi}.csv'))
        test_iso3166_2_fi_xml = ET.parse(os.path.join(self.test_output_dir, f'{self.test_output_filename}_{test_alpha_fi}.xml'))

        self.assertEqual(len(test_iso3166_2_fi_json["FI"]), 19, f"Expected subdivisions in output, got {len(test_iso3166_2_fi_json)}.")
        self.assertEqual(list(test_iso3166_2_fi_json["FI"].keys()), ["FI-01", "FI-02", "FI-03", "FI-04", "FI-05", "FI-06", "FI-07", "FI-08", "FI-09", 
            "FI-10", "FI-11", "FI-12", "FI-13", "FI-14", "FI-15", "FI-16", "FI-17", "FI-18", "FI-19"], 
                f"Expected list of subdivision codes doesn't match output:\n{list(test_iso3166_2_fi_json['FI'].keys())}.")   
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "_FI.csv")), 
            f"Expected subdivision data to be exported to a CSV: {os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0])}-FI.csv.")
        self.assertEqual(list(test_iso3166_2_fi_csv.columns), self.correct_default_output_columns[1:], f"Expected column names don't match CSV columns:\n{test_iso3166_2_fi_csv.columns}.")
        self.assertEqual(len(test_iso3166_2_fi_csv), 19, "Expected there to be 19 rows in the exported subdivision CSV.")
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "_FI.xml")), 
            f"Expected subdivision data to be exported to an XML: {os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0])}-FI.xml.")
        self.assertEqual([elem.tag for elem in test_iso3166_2_fi_xml.getroot()], [test_alpha_fi], f"Expected top-level element FI does not match output, got {list(test_iso3166_2_fi_xml.getroot())}.")
        self.assertEqual(len(test_iso3166_2_fi_xml.find("FI")), 19, f"Expected 19 sub-level elements (subdivisions) in the output xml, got {len(test_iso3166_2_fi_xml.find('FI'))}.")
        for top_level in test_iso3166_2_fi_xml.getroot():
            for second_level in top_level:
                self.assertEqual(set([child.tag for child in second_level]), set(self.correct_default_output_attributes), 
                                 f"Expected second-level names in XML do match attributes, got {[child.tag for child in second_level]}.")
                
        for subd in test_iso3166_2_fi_json["FI"]:
            self.assertIsNot(test_iso3166_2_fi_json["FI"][subd]["name"], None, 
                f"Expected subdivision name to not be None, got {test_iso3166_2_fi_json['FI'][subd]['name']}.")
            if not (test_iso3166_2_fi_json["FI"][subd]["parentCode"] is None):
                self.assertIn(test_iso3166_2_fi_json["FI"][subd]["parentCode"], list(test_iso3166_2_fi_json["FI"][subd].keys()), 
                    f"Parent code {test_iso3166_2_fi_json['FI'][subd]['parentCode']} not found in list of subdivision codes.")
            if not (test_iso3166_2_fi_json["FI"][subd]["flag"] is None):
                self.assertEqual(os.path.splitext(test_iso3166_2_fi_json["FI"][subd]["flag"])[0], self.flag_icons_base_url + "FI/" + subd, 
                    f"Expected flag URL to be {self.flag_icons_base_url}FI/{subd}, got {os.path.splitext(test_iso3166_2_fi_json['FI'][subd]['flag'])[0]}.") 
                # self.assertEqual(requests.get(test_iso3166_2_fi_json["FI"][subd]["flag"], headers={"User-Agent": self.user_agent_header}).status_code, 200, 
                #     f"Flag URL invalid: {test_iso3166_2_fi_json['FI'][subd]['flag']}.")
            for key in list(test_iso3166_2_fi_json["FI"][subd].keys()):
                self.assertIn(key, self.correct_default_output_attributes, f"Attribute {key} not found in list of correct attributes:\n{self.correct_default_output_attributes}.")

        #FI-02 - Etelä-Karjala
        test_iso3166_2_fi_json_fi_02_expected = {"name": "Etelä-Karjala", "localOtherName": "Södra Karelen (swe), South Karelia (eng)", "parentCode": None, 
            "type": "Region", "flag": "https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/FI/FI-02.png", "latLng": None}
        self.assertEqual(test_iso3166_2_fi_json_fi_02_expected, test_iso3166_2_fi_json["FI"]["FI-02"], 
            f"Expected and observed subdivision output for FI-02 do not match:\n{test_iso3166_2_fi_json_fi_02_expected}\n{test_iso3166_2_fi_json['FI']['FI-02']}.")
        #FI-17 - Satakunda
        test_iso3166_2_fi_json_fi_17_expected = {"name": "Satakunta", "localOtherName": "Satakunta (swe), Satakunta (eng)", "parentCode": None, 
            "type": "Region", "flag": "https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/FI/FI-17.svg", "latLng": None}
        self.assertEqual(test_iso3166_2_fi_json_fi_17_expected, test_iso3166_2_fi_json["FI"]["FI-17"], 
            f"Expected and observed subdivision output for FI-17 do not match:\n{test_iso3166_2_fi_json_fi_02_expected}\n{test_iso3166_2_fi_json['FI']['FI-17']}.")
#3.)
        export_iso3166_2(test_alpha_nz, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, 
                         export_xml=True, extract_lat_lng=False, history=False) #New Zealand

        #open exported json, csv and xml
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "_NZ.json")) as output_json:
            test_iso3166_2_nz_json = json.load(output_json)
        test_iso3166_2_nz_csv = pd.read_csv(os.path.join(self.test_output_dir, self.test_output_filename + "_NZ.csv"))
        test_iso3166_2_nz_xml = ET.parse(os.path.join(self.test_output_dir, self.test_output_filename + "_NZ.xml"))

        self.assertEqual(len(test_iso3166_2_nz_json['NZ']), 17, f"Expected subdivisions in output, got {len(test_iso3166_2_nz_json)}.")
        self.assertEqual(list(test_iso3166_2_nz_json['NZ'].keys()), ['NZ-AUK', 'NZ-BOP', 'NZ-CAN', 'NZ-CIT', 'NZ-GIS', 'NZ-HKB', 'NZ-MBH', 'NZ-MWT', 'NZ-NSN', 'NZ-NTL', 'NZ-OTA', 'NZ-STL', 'NZ-TAS', 'NZ-TKI', 'NZ-WGN', 'NZ-WKO', 'NZ-WTC'], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_iso3166_2_nz_json['NZ'].keys())}.")  
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "_NZ.csv")), 
            f"Expected subdivision data to be exported to a CSV: {os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0])}-NZ.csv.") 
        self.assertEqual(list(test_iso3166_2_nz_csv.columns), self.correct_default_output_columns[1:], f"Expected column names don't match CSV columns:\n{test_iso3166_2_nz_csv.columns}.")
        self.assertEqual(len(test_iso3166_2_nz_csv), 17, "Expected there to be 17 rows in the exported subdivision CSV.")
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "_NZ.xml")), 
            f"Expected subdivision data to be exported to an XML: {os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0])}-NP.xml.")
        self.assertEqual([elem.tag for elem in test_iso3166_2_nz_xml.getroot()], ['NZ'], f"Expected top-level element NP does not match output, got {list(test_iso3166_2_nz_xml.getroot())}.")
        self.assertEqual(len(test_iso3166_2_nz_xml.find("NZ")), 17, f"Expected 17 sub-level elements (subdivisions) in the output xml, got {len(test_iso3166_2_nz_xml.find('NZ'))}.")
        for top_level in test_iso3166_2_nz_xml.getroot():
            for second_level in top_level:
                self.assertEqual(set([child.tag for child in second_level]), set(self.correct_default_output_attributes), 
                                 f"Expected second-level names in XML do match attributes, got {[child.tag for child in second_level]}.")
                
        for subd in test_iso3166_2_nz_json['NZ']:
            self.assertIsNot(test_iso3166_2_nz_json['NZ'][subd]["name"], None, 
                f"Expected subdivision name to not be None, got {test_iso3166_2_nz_json['NZ'][subd]['name']}.")
            if not (test_iso3166_2_nz_json['NZ'][subd]["parentCode"] is None):
                self.assertIn(test_iso3166_2_nz_json['NZ'][subd]["parentCode"], list(test_iso3166_2_nz_json['NZ'][subd].keys()), 
                    f"Parent code {test_iso3166_2_nz_json['NZ'][subd]['parentCode']} not found in list of subdivision codes.")
            if not (test_iso3166_2_nz_json['NZ'][subd]["flag"] is None):
                self.assertEqual(os.path.splitext(test_iso3166_2_nz_json['NZ'][subd]["flag"])[0], self.flag_icons_base_url + "NZ/" + subd, 
                    f"Expected flag URL to be {self.flag_icons_base_url}NZ/{subd}, got {os.path.splitext(test_iso3166_2_nz_json['NZ'][subd]['flag'])[0]}.") 
                # self.assertEqual(requests.get(test_iso3166_2_nz_json['NZ'][subd]["flag"], headers={"User-Agent": self.user_agent_header}).status_code, 200, 
                #     f"Flag URL invalid: {test_iso3166_2_nz_json['NZ'][subd]['flag']}.")
            for key in list(test_iso3166_2_nz_json['NZ'][subd].keys()):
                self.assertIn(key, self.correct_default_output_attributes, f"Attribute {key} not found in list of correct attributes:\n{self.correct_default_output_attributes}.")

        #NZ-OTA - Otago
        test_iso3166_2_nz_json_nz_ota_expected = {"name": "Otago", "localOtherName": "Ō Tākou (mri)", 
            "parentCode": None, "type": "Region", "flag": "https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/NZ/NZ-OTA.svg", "latLng": None}
        self.assertEqual(test_iso3166_2_nz_json_nz_ota_expected, test_iso3166_2_nz_json['NZ']["NZ-OTA"], 
            f"Expected and observed subdivision output for NZ-OTA do not match:\n{test_iso3166_2_nz_json_nz_ota_expected}\n{test_iso3166_2_nz_json['NZ']['NZ-OTA']}.")
        #NZ-TKI - Taranaki
        test_iso3166_2_nz_json_nz_tki_expected = {"name": "Taranaki", "localOtherName": "Taranaki (mri)", 
            "parentCode": None, "type": "Region", "flag": None, "latLng": None}
        self.assertEqual(test_iso3166_2_nz_json_nz_tki_expected, test_iso3166_2_nz_json['NZ']["NZ-TKI"], 
            f"Expected and observed subdivision output for NZ-TKI do not match:\n{test_iso3166_2_nz_json_nz_tki_expected}\n{test_iso3166_2_nz_json['NZ']['NZ-TKI']}.")
#4.)
        export_iso3166_2(alpha_codes=test_alpha_kg_mg_nr, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, 
                         export_xml=True, extract_lat_lng=False, history=False) #Kyrgyzstan, Madagascar, Nauru

        #open exported json, csv and xml
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "_KG,MG,NR.json")) as output_json:
            test_iso3166_2_kg_mg_nr_json = json.load(output_json)
        test_iso3166_2_kg_mg_nr_csv = pd.read_csv(os.path.join(self.test_output_dir, self.test_output_filename + "_KG,MG,NR.csv"))
        test_iso3166_2_kg_mg_nr_xml = ET.parse(os.path.join(self.test_output_dir, self.test_output_filename + "_KG,MG,NR.xml"))

        self.assertEqual(len(test_iso3166_2_kg_mg_nr_json["KG"]), 9, f"Expected 9 subdivisions in output dict, got {len(test_iso3166_2_kg_mg_nr_json['KG'])}.")
        self.assertEqual(len(test_iso3166_2_kg_mg_nr_json["MG"]), 6, f"Expected 6 subdivisions in output dict, got {len(test_iso3166_2_kg_mg_nr_json['MG'])}.")
        self.assertEqual(len(test_iso3166_2_kg_mg_nr_json["NR"]), 14, f"Expected 14 subdivisions in output dict, got {len(test_iso3166_2_kg_mg_nr_json['NR'])}.")
        self.assertEqual(list(test_iso3166_2_kg_mg_nr_json["KG"].keys()), ['KG-B', 'KG-C', 'KG-GB', 'KG-GO', 'KG-J', 'KG-N', 'KG-O', 'KG-T', 'KG-Y'], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_iso3166_2_kg_mg_nr_json['KG'].keys())}.")   
        self.assertEqual(list(test_iso3166_2_kg_mg_nr_json["MG"].keys()), ["MG-A", "MG-D", "MG-F", "MG-M", "MG-T", "MG-U"], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_iso3166_2_kg_mg_nr_json['MG'].keys())}.")  
        self.assertEqual(list(test_iso3166_2_kg_mg_nr_json["NR"].keys()), ['NR-01', 'NR-02', 'NR-03', 'NR-04', 'NR-05', 'NR-06', 'NR-07', 'NR-08', 'NR-09', 'NR-10', 
            'NR-11', 'NR-12', 'NR-13', 'NR-14'], f"Expected list of subdivision codes doesn't match output:\n{list(test_iso3166_2_kg_mg_nr_json['NR'].keys())}.")   
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "_KG,MG,NR.csv")), 
            f"Expected subdivision data to be exported to a CSV: {os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0])}-KG,MG,NR.csv.")
        self.assertEqual(list(test_iso3166_2_kg_mg_nr_csv.columns), self.correct_default_output_columns, f"Expected column names don't match CSV columns:\n{test_iso3166_2_kg_mg_nr_csv.columns}.")
        self.assertEqual(len(test_iso3166_2_kg_mg_nr_csv), 29, "Expected there to be 29 rows in the exported subdivision CSV.")
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "_KG,MG,NR.xml")), 
            f"Expected subdivision data to be exported to an XML: {os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0])}-KG,MG,NR.xml.")
        self.assertEqual([elem.tag for elem in test_iso3166_2_kg_mg_nr_xml.getroot()], ['KG', 'MG', 'NR'], f"Expected top-level elements KG, MG & NR does not match output, got {list(test_iso3166_2_kg_mg_nr_xml.getroot())}.")
        self.assertEqual(len(test_iso3166_2_kg_mg_nr_xml.find("KG")), 9, f"Expected 9 sub-level elements (subdivisions) in the output xml, got {len(test_iso3166_2_kg_mg_nr_xml.find('KG'))}.")
        self.assertEqual(len(test_iso3166_2_kg_mg_nr_xml.find("MG")), 6, f"Expected 6 sub-level elements (subdivisions) in the output xml, got {len(test_iso3166_2_kg_mg_nr_xml.find('MG'))}.")
        self.assertEqual(len(test_iso3166_2_kg_mg_nr_xml.find("NR")), 14, f"Expected 14 sub-level elements (subdivisions) in the output xml, got {len(test_iso3166_2_kg_mg_nr_xml.find('NR'))}.")
        for top_level in test_iso3166_2_kg_mg_nr_xml.getroot():
            for second_level in top_level:
                self.assertEqual(set([child.tag for child in second_level]), set(self.correct_default_output_attributes), 
                                 f"Expected second-level names in XML do match attributes, got {[child.tag for child in second_level]}.")

        for country in test_iso3166_2_kg_mg_nr_json:
            for subd in test_iso3166_2_kg_mg_nr_json[country]:
                self.assertIsNot(test_iso3166_2_kg_mg_nr_json[country][subd]["name"], None, 
                    f"Expected subdivision name to not be None, got {test_iso3166_2_kg_mg_nr_json[country][subd]['name']}.")
                if not (test_iso3166_2_kg_mg_nr_json[country][subd]["parentCode"] is None):
                    self.assertIn(test_iso3166_2_kg_mg_nr_json[country][subd]["parentCode"], list(test_iso3166_2_kg_mg_nr_json[country][subd].keys()), 
                        f"Parent code {test_iso3166_2_kg_mg_nr_json[country][subd]['parentCode']} not found in list of subdivision codes.")
                if not (test_iso3166_2_kg_mg_nr_json[country][subd]["flag"] is None):
                    self.assertEqual(os.path.splitext(test_iso3166_2_kg_mg_nr_json[country][subd]["flag"])[0], self.flag_icons_base_url + country + "/" + subd, 
                        f"Expected flag URL to be {self.flag_icons_base_url + country + '/' + subd}, got {os.path.splitext(test_iso3166_2_kg_mg_nr_json[country][subd]['flag'])[0]}.") 
                    # self.assertEqual(requests.get(test_iso3166_2_kg_mg_nr_json[country][subd]["flag"], headers={"User-Agent": self.user_agent_header}).status_code, 200, 
                    #     f"Flag URL invalid: {test_iso3166_2_kg_mg_nr_json[country][subd]['flag']}.")
                for key in list(test_iso3166_2_kg_mg_nr_json[country][subd].keys()):
                    self.assertIn(key, self.correct_default_output_attributes, f"Attribute {key} not found in list of correct attributes:\n{self.correct_default_output_attributes}.")
        
        #KG-GB - Bishkek Shaary
        test_iso3166_2_kg_json_kg_gb_expected = {"name": "Bishkek Shaary", "localOtherName": "Бишкек шаары (kir), Город Бишкек (rus), Gorod Bishkek (rus), Gorod Biškek (rus), Bishkek (eng)", 
            "parentCode": None, "type": "City", "flag": "https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/KG/KG-GB.svg", "latLng": None}
        self.assertEqual(test_iso3166_2_kg_json_kg_gb_expected, test_iso3166_2_kg_mg_nr_json["KG"]["KG-GB"], 
            f"Expected and observed subdivision output for KG-GB do not match:\n{test_iso3166_2_kg_json_kg_gb_expected}\n{test_iso3166_2_kg_mg_nr_json['KG']['KG-GB']}.")
        #MG-D - Antsiranana
        test_iso3166_2_mg_sa_json_mg_d_expected = {"name": "Antsiranana", "localOtherName": None, "parentCode": None, "type": "Province", "flag": None, "latLng": None}
        self.assertEqual(test_iso3166_2_mg_sa_json_mg_d_expected, test_iso3166_2_kg_mg_nr_json["MG"]["MG-D"], 
            f"Expected and observed subdivision output for MG-D do not match:\n{test_iso3166_2_mg_sa_json_mg_d_expected}\n{test_iso3166_2_kg_mg_nr_json['MG']['MG-D']}.")
        #NR-02 - Anabar
        test_iso3166_2_nr_json_nr_02_expected = {"name": "Anabar", "localOtherName": None, "parentCode": None, "type": "District", "flag": None, "latLng": None}
        self.assertEqual(test_iso3166_2_nr_json_nr_02_expected, test_iso3166_2_kg_mg_nr_json["NR"]["NR-02"], 
            f"Expected and observed subdivision output for NR-02 do not match:\n{test_iso3166_2_nr_json_nr_02_expected}\n{test_iso3166_2_kg_mg_nr_json['NR']['NR-02']}.")
#5.)
        with (self.assertRaises(ValueError)):
            export_iso3166_2(alpha_codes=test_alpha_error1, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0) #ZZ
            export_iso3166_2(alpha_codes=test_alpha_error2, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0) #ABCDEF
            export_iso3166_2(alpha_codes=test_alpha_error3, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0) #1234
#6.)
        with (self.assertRaises(TypeError)):
            export_iso3166_2(alpha_codes=123)
            export_iso3166_2(alpha_codes=True)
            export_iso3166_2(alpha_codes=10.9)

    # @unittest.skip("")  
    def test_export_iso3166_restcountries(self):
        """ Testing export functionality for getting ISO 3166-2 subdivision data from data sources, including additional RestCountries API attributes. """
        test_alpha_gt = "GT" #Guatemala - continents & subregion
        test_alpha_ir = "IRN" #Iran - language, startOfWeek & region
        test_alpha_mg_sa = "450,sau" #Madagascar, Saudi Arabia - idd, currencies & postalCode
        test_rest_countries_keys_error1 = "ZZ"
        test_rest_countries_keys_error2 = "ABCDEF"
        test_rest_countries_keys_error3 = 1234    
#1.)
        export_iso3166_2(alpha_codes=test_alpha_gt, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1,
                         rest_countries_keys="continents,subregion", history=False, extract_lat_lng=False) #Guatemala - including additional continent and region attributes
        expected_attribute_list = self.correct_default_output_attributes + ["continents", "subregion"]

        #open exported json & csv
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "_GT.json")) as output_json:
            test_iso3166_2_gt_json = json.load(output_json)
        test_iso3166_2_gt_csv = pd.read_csv(os.path.join(self.test_output_dir, f'{self.test_output_filename}_{test_alpha_gt}.csv'))

        self.assertEqual(len(test_iso3166_2_gt_json["GT"]), 22, f"Expected 22 subdivisions in output dict, got {len(test_iso3166_2_gt_json['GT'])}.")
        self.assertEqual(list(test_iso3166_2_gt_json["GT"].keys()), ['GT-01', 'GT-02', 'GT-03', 'GT-04', 'GT-05', 'GT-06', 'GT-07', 'GT-08', 'GT-09', 'GT-10', 'GT-11', 
                                                            'GT-12', 'GT-13', 'GT-14', 'GT-15', 'GT-16', 'GT-17', 'GT-18', 'GT-19', 'GT-20', 'GT-21', 'GT-22'], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_iso3166_2_gt_json['GT'].keys())}.")   
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "_GT.csv")), 
            f"Expected subdivision data to be exported to a CSV: {os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + '-GT.csv')}.")
        self.assertEqual(list(test_iso3166_2_gt_csv.columns), self.correct_default_output_columns[1:] + ["continents", "subregion"], f"Expected column names don't match CSV columns:\n{test_iso3166_2_gt_csv.columns}.")
        self.assertEqual(len(test_iso3166_2_gt_csv), 22, "Expected there to be 22 rows in the exported subdivision CSV.")

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
                         rest_countries_keys="languages,startOfWeek,region", history=False, extract_lat_lng=False) #Iran - including additional languages, startOfWeek and region attributes
        expected_attribute_list = self.correct_default_output_attributes + ["languages", "startOfWeek", "region"]

        #open exported json & csv
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "_IR.json")) as output_json:
            test_iso3166_2_ir_json = json.load(output_json)
        test_iso3166_2_ir_csv = pd.read_csv(os.path.join(self.test_output_dir, self.test_output_filename + "_IR.csv"))
    
        self.assertEqual(len(test_iso3166_2_ir_json["IR"]), 31, f"Expected 31 subdivisions in output dict, got {len(test_iso3166_2_ir_json['IR'])}.")
        self.assertEqual(list(test_iso3166_2_ir_json["IR"].keys()), ['IR-00', 'IR-01', 'IR-02', 'IR-03', 'IR-04', 'IR-05', 'IR-06', 'IR-07', 'IR-08', 'IR-09', 'IR-10', 
                                                            'IR-11', 'IR-12', 'IR-13', 'IR-14', 'IR-15', 'IR-16', 'IR-17', 'IR-18', 'IR-19', 'IR-20', 'IR-21', 
                                                            'IR-22', 'IR-23', 'IR-24', 'IR-25', 'IR-26', 'IR-27', 'IR-28', 'IR-29', 'IR-30'],
            f"Expected list of subdivision codes doesn't match output:\n{list(test_iso3166_2_ir_json['IR'].keys())}.")   
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + '_IR.csv')), 
            f"Expected subdivision data to be exported to a CSV: {os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + '-IR.csv')}.")
        self.assertEqual(list(test_iso3166_2_ir_csv.columns), self.correct_default_output_columns[1:] + ["languages", "region", "startOfWeek"], f"Expected column names don't match CSV columns:\n{test_iso3166_2_ir_csv.columns}.")
        self.assertEqual(len(test_iso3166_2_ir_csv), 31, "Expected there to be 31 rows in the exported subdivision CSV.")

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
        export_iso3166_2(alpha_codes=test_alpha_mg_sa, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1,
                         rest_countries_keys="idd,currencies,postalCode", history=False, extract_lat_lng=False) #Madagascar, Saudi Arabia - including additional idd, currencies and postalCode attributes
        expected_attribute_list = self.correct_default_output_attributes + ["idd", "currencies", "postalCode"]

        #open exported json & csv
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "_MG,SA.json")) as output_json:
            test_iso3166_2_mg_sa_json = json.load(output_json)
        test_iso3166_2_mg_sa_csv = pd.read_csv(os.path.join(self.test_output_dir, self.test_output_filename + "_MG,SA.csv"))

        self.assertEqual(len(test_iso3166_2_mg_sa_json["MG"]), 6, f"Expected 6 subdivisions in output dict for MG, got {len(test_iso3166_2_mg_sa_json['MG'])}.")
        self.assertEqual(len(test_iso3166_2_mg_sa_json["SA"]), 13, f"Expected 13 subdivisions in output dict for SA, got {len(test_iso3166_2_mg_sa_json['SA'])}.")
        self.assertEqual(list(test_iso3166_2_mg_sa_json["MG"].keys()), ['MG-A', 'MG-D', 'MG-F', 'MG-M', 'MG-T', 'MG-U'], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_iso3166_2_mg_sa_json['MG'].keys())}.")   
        self.assertEqual(list(test_iso3166_2_mg_sa_json["SA"].keys()), ['SA-01', 'SA-02', 'SA-03', 'SA-04', 'SA-05', 'SA-06', 'SA-07', 'SA-08', 'SA-09', 'SA-10', 'SA-11', 'SA-12', 'SA-14'], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_iso3166_2_mg_sa_json['SA'].keys())}.")   
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + '_MG,SA.csv')), 
            f"Expected subdivision data to be exported to a CSV: {os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + '-MG,SA.csv')}.")
        self.assertEqual(list(test_iso3166_2_mg_sa_csv.columns), self.correct_default_output_columns + ["currencies", "idd", "postalCode"], f"Expected column names don't match CSV columns:\n{test_iso3166_2_mg_sa_csv.columns}.")
        self.assertEqual(len(test_iso3166_2_mg_sa_csv), 19, "Expected there to be 19 rows in the exported subdivision CSV.")

        for subd in test_iso3166_2_mg_sa_json["MG"]:
            for key in list(test_iso3166_2_mg_sa_json["MG"][subd].keys()):
                self.assertIn(key, expected_attribute_list, f"Attribute {key} not found in list of correct attributes:\n{expected_attribute_list}.")        
            self.assertEqual(test_iso3166_2_mg_sa_json["MG"][subd]["idd"], {"root": "+2", "suffixes": ["61"]}, 
                    f"Expected attribute value to be root: +2, suffixes: 61, got {test_iso3166_2_mg_sa_json['MG'][subd]['idd']}.")
            self.assertEqual(test_iso3166_2_mg_sa_json["MG"][subd]["currencies"], {"MGA": {"name": "Malagasy ariary", "symbol": "Ar"}}, 
                    f"Expected attribute value to be MGA: name:Malagasy ariary, symbol:Ar, got {test_iso3166_2_mg_sa_json['MG'][subd]['currencies']}.")
            self.assertEqual(test_iso3166_2_mg_sa_json["MG"][subd]["postalCode"], "Format: ###, Regex: " + r'^(\d{3})$', 
                    f"Expected attribute value to be Format: ###, Regex: r'^(\d{3})$', got {test_iso3166_2_mg_sa_json['MG'][subd]['postalCode']}.")
            
        for subd in test_iso3166_2_mg_sa_json["SA"]:
            for key in list(test_iso3166_2_mg_sa_json["SA"][subd].keys()):
                self.assertIn(key, expected_attribute_list, f"Attribute {key} not found in list of correct attributes:\n{expected_attribute_list}.")        
            self.assertEqual(test_iso3166_2_mg_sa_json["SA"][subd]["idd"], {"root": "+9", "suffixes": ["66"]}, 
                    f"Expected attribute value to be root: +9, suffixes: 66, got {test_iso3166_2_mg_sa_json['SA'][subd]['idd']}.")
            self.assertEqual(test_iso3166_2_mg_sa_json["SA"][subd]["currencies"], {"SAR": {"name": "Saudi riyal", "symbol": "ر.س"}}, 
                    f"Expected attribute value to be MGA: name: Saudi Riyal, symbol:ر.س, got {test_iso3166_2_mg_sa_json['SA'][subd]['currencies']}.")
            self.assertEqual(test_iso3166_2_mg_sa_json["SA"][subd]["postalCode"], "Format: #####, Regex: " + r'^(\d{5})$', 
                    f"Expected attribute value to be Format: #####, Regex: r'^(\d{5})$', got {test_iso3166_2_mg_sa_json['SA'][subd]['postalCode']}.")
#4.)
        with (self.assertRaises(ValueError)):
            export_iso3166_2(export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, rest_countries_keys=test_rest_countries_keys_error1, extract_lat_lng=False) #ZZ
            export_iso3166_2(export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, rest_countries_keys=test_rest_countries_keys_error2, extract_lat_lng=False) #ABCDEF
            export_iso3166_2(export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, rest_countries_keys=test_rest_countries_keys_error3, extract_lat_lng=False) #1234
    
    # @unittest.skip("")
    def test_export_filter_attributes(self):
        """ Testing export functionality for getting ISO 3166-2 subdivision data from data sources, with some default attributes filtered out. """
        test_alpha_ge = "GE" #Georgia - filtering the name, latLng & type
        test_alpha_gw = "GNB" #Guinea-Bissau - filtering the name & localOtherName
        test_alpha_ki = "296" #Kiribati - filtering latLng, parentCode & flag
        test_exclude_keys_error1 = "ZZ"
        test_exclude_keys_error2 = "ABCDEF"
        test_exclude_keys_error3 = 1234    
#1.)
        export_iso3166_2(alpha_codes=test_alpha_ge, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, 
                      filter_attributes="name,latLng,type", history=False, extract_lat_lng=False) #Georgia - filtering only the name, latLng and type default attributes 
    
        #open exported json & csv
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "_GE.json")) as output_json:
            test_iso3166_2_ge_json = json.load(output_json)
        test_iso3166_2_ge_csv = pd.read_csv(os.path.join(self.test_output_dir, self.test_output_filename + "_" + test_alpha_ge + ".csv"))

        self.assertEqual(len(test_iso3166_2_ge_json["GE"]), 12, f"Expected 12 subdivisions in output dict, got {len(test_iso3166_2_ge_json['GE'])}.")
        self.assertEqual(list(test_iso3166_2_ge_json["GE"].keys()), ['GE-AB', 'GE-AJ', 'GE-GU', 'GE-IM', 'GE-KA', 'GE-KK', 'GE-MM', 'GE-RL', 'GE-SJ', 'GE-SK', 'GE-SZ', 'GE-TB'], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_iso3166_2_ge_json['GE'].keys())}.")   
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "_GE.csv")), 
            f"Expected subdivision data to be exported to a CSV: {os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + '-GE.csv')}.")
        self.assertEqual(list(test_iso3166_2_ge_csv.columns), ['subdivisionCode', 'name', 'latLng', 'type'], 
            f"Expected column names don't match CSV columns:\n{test_iso3166_2_ge_csv.columns}.")
        self.assertEqual(len(test_iso3166_2_ge_csv), 12, "Expected there to be 12 rows in the exported subdivision CSV.")
        for country in test_iso3166_2_ge_json:
            for subd in test_iso3166_2_ge_json[country]:
                self.assertNotIn(["localOtherName", "parentCode", "flag", "history"], list(test_iso3166_2_ge_json[country][subd].keys()),
                    f"Expected the localOtherName, parentCode, flag and history default attributes to not be in subdivision attributes:\n{list(test_iso3166_2_ge_json[country][subd].keys())}.")
#2.) 
        export_iso3166_2(alpha_codes=test_alpha_gw, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1,
                      filter_attributes=["name", "localOtherName"], history=False, extract_lat_lng=False) #Guinea-Bissau - filtering the localOtherName and name default attributes 
    
        #open exported json & csv
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "_GW.json")) as output_json:
            test_iso3166_2_gw_json = json.load(output_json)
        test_iso3166_2_gw_csv = pd.read_csv(os.path.join(self.test_output_dir, self.test_output_filename + "_GW.csv"))

        self.assertEqual(len(test_iso3166_2_gw_json["GW"]), 12, f"Expected 12 subdivisions in output dict, got {len(test_iso3166_2_gw_json['GW'])}.")
        self.assertEqual(list(test_iso3166_2_gw_json["GW"].keys()), ['GW-BA', 'GW-BL', 'GW-BM', 'GW-BS', 'GW-CA', 'GW-GA', 'GW-L', 'GW-N', 'GW-OI', 'GW-QU', 'GW-S', 'GW-TO'], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_iso3166_2_gw_json['GW'].keys())}.")   
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "_GW.csv")), 
            f"Expected subdivision data to be exported to a CSV: {os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + '-GW.csv')}.")
        self.assertEqual(list(test_iso3166_2_gw_csv.columns), ['subdivisionCode', 'name', 'localOtherName'], 
            f"Expected column names don't match CSV columns:\n{test_iso3166_2_gw_csv.columns}.")
        self.assertEqual(len(test_iso3166_2_gw_csv), 12, "Expected there to be 12 rows in the exported subdivision CSV.")
        for country in test_iso3166_2_gw_json:
            for subd in test_iso3166_2_gw_json[country]:
                self.assertNotIn(["type", "parentCode", "flag", "latLng", "history"], list(test_iso3166_2_gw_json[country][subd].keys()),
                    f"Expected the type, parentCode, flag, latLng and history default attributes to not be in subdivision attributes:\n{list(test_iso3166_2_gw_json[country][subd].keys())}.")
#3.)
        export_iso3166_2(alpha_codes=test_alpha_ki, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1,
                         filter_attributes="parentCode, flag", history=False, extract_lat_lng=False) #Kiribati - filtering the parentCode and flag default attributes 
    
        #open exported json & csv
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "_KI.json")) as output_json:
            test_iso3166_2_ki_json = json.load(output_json)
        test_iso3166_2_ki_csv = pd.read_csv(os.path.join(self.test_output_dir, self.test_output_filename + "_KI.csv"))

        self.assertEqual(len(test_iso3166_2_ki_json["KI"]), 3, 
            f"Expected 3 subdivisions in output dict, got {len(test_iso3166_2_ki_json['KI'])}.")
        self.assertEqual(list(test_iso3166_2_ki_json["KI"].keys()), ['KI-G', 'KI-L', 'KI-P'], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_iso3166_2_ki_json['KI'].keys())}.")   
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + "_KI.csv")), 
            f"Expected subdivision data to be exported to a CSV: {os.path.join(self.test_output_dir, os.path.splitext(self.test_output_filename)[0] + '_KI.csv')}.")
        self.assertEqual(list(test_iso3166_2_ki_csv.columns), ['subdivisionCode', 'parentCode', 'flag'], 
            f"Expected column names don't match CSV columns:\n{test_iso3166_2_ki_csv.columns}.")
        self.assertEqual(len(test_iso3166_2_ki_csv), 3, 
            f"Expected there to be 3 rows in the exported subdivision CSV, got {len(test_iso3166_2_ki_csv)}.")        
        for country in test_iso3166_2_ki_json:
            for subd in test_iso3166_2_ki_json[country]:
                self.assertNotIn(["name", "localOtherName", "type", "latLng", "history"], list(test_iso3166_2_ki_json[country][subd].keys()),
                    f"Expected the name, localOtherName, type, latLng and history default attributes to not be in subdivision attributes:\n{list(test_iso3166_2_ki_json[country][subd].keys())}.")
#4.)
        with (self.assertRaises(ValueError)):
            export_iso3166_2(export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, filter_attributes=test_exclude_keys_error1, extract_lat_lng=False) #ZZ
            export_iso3166_2(export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, filter_attributes=test_exclude_keys_error2, extract_lat_lng=False) #ABCDEF
            export_iso3166_2(export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, filter_attributes=test_exclude_keys_error3, extract_lat_lng=False) #1234

    # @unittest.skip("Skipping to not overload test instances.") 
    def test_export_iso3166_2_alpha_code_range(self): 
        """ Testing correct ISO 3166-2 data is exported and pulled from data sources using a range of alpha codes via the alpha_codes_range parameter. """
        test_alpha_at_be = "AT-BE" #Austria - Belgium
        test_alpha_gd_gm = "GRD-GMB" #Grenada - Gambia
        test_alpha_va_vu = "336-548" #Vatican city - Vanuatu
        test_alpha_ye = "YE" #if single alpha code input then get all data using code as starting point (end alpha will be ZW)
        test_alpha_aa_ad = "AA-AD" #invalid alpha code
        test_alpha_xm_xx = "XM-XX" #invalid alpha codes
#1.)
        export_iso3166_2(alpha_codes_range=test_alpha_at_be, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=1, export_csv=1, extract_lat_lng=False) #AT-BE

        #open exported json & csv
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "_" + test_alpha_at_be + ".json")) as output_json:
            test_alpha_at_be_json = json.load(output_json)
        test_alpha_at_be_csv = pd.read_csv(os.path.join(self.test_output_dir, f'{self.test_output_filename}_{test_alpha_at_be}.csv'))

        self.assertEqual(list(test_alpha_at_be_json.keys()), ['AT', 'AU', 'AW', 'AX', 'AZ', 'BA', 'BB', 'BD', 'BE'], 
            f"Expected and observed list of country codes do not match:\n{list(test_alpha_at_be_json.keys())}.")
        self.assertEqual(set(test_alpha_at_be_csv["alphaCode"]), set(['AT', 'AU', 'AZ', 'BA', 'BB', 'BD', 'BE']), 
            f"Expected and observed list of country codes do not match:\n{test_alpha_at_be_csv['alphaCode']}.")
#2.)
        export_iso3166_2(alpha_codes_range=test_alpha_gd_gm, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, extract_lat_lng=False) #GD-GM

        #open exported json & csv
        with open(os.path.join(self.test_output_dir, f'{self.test_output_filename}_GD-GM.json')) as output_json:
            test_alpha_gd_gm_json = json.load(output_json)
        test_alpha_gd_gm_csv = pd.read_csv(os.path.join(self.test_output_dir, f'{self.test_output_filename}_GD-GM.csv'))
        expected_country_codes_fi_gm = ['GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GL', 'GM']
    
        self.assertEqual(list(test_alpha_gd_gm_json.keys()), expected_country_codes_fi_gm, 
            f"Expected and observed list of country codes do not match:\n{list(test_alpha_gd_gm_json.keys())}.")
        self.assertEqual(set(test_alpha_gd_gm_csv["alphaCode"]), set(['GD', 'GE', 'GH', 'GL', 'GM']), 
            f"Expected and observed list of country codes do not match:\n{set(test_alpha_gd_gm_csv['alphaCode'])}.")
#3.)
        export_iso3166_2(alpha_codes_range=test_alpha_va_vu, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, extract_lat_lng=False) #VC-VU

        #open exported json & csv
        with open(os.path.join(self.test_output_dir, f'{self.test_output_filename}_VA-VU.json')) as output_json:
            test_alpha_va_vu_json = json.load(output_json)
        test_alpha_va_vu_csv = pd.read_csv(os.path.join(self.test_output_dir, f'{self.test_output_filename}_VA-VU.csv'))
    
        self.assertEqual(list(test_alpha_va_vu_json.keys()), ['VA', 'VC', 'VE', 'VG', 'VI', 'VN', 'VU'], 
            f"Expected and observed list of country codes do not match:\n{list(test_alpha_va_vu_json.keys())}.")
        self.assertEqual(set(test_alpha_va_vu_csv["alphaCode"]), set(['VC', 'VE', 'VN', 'VU']), 
            f"Expected and observed list of country codes do not match:\n{set(test_alpha_va_vu_csv['alphaCode'])}.")
#4.)
        export_iso3166_2(alpha_codes_range=test_alpha_ye, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, extract_lat_lng=False) #YE

        #open exported json & csv
        with open(os.path.join(self.test_output_dir, f'{self.test_output_filename}_{test_alpha_ye}-ZW.json')) as output_json:
            test_alpha_ye_json = json.load(output_json)
        test_alpha_ye_csv = pd.read_csv(os.path.join(self.test_output_dir, f'{self.test_output_filename}_{test_alpha_ye}-ZW.csv'))
    
        self.assertEqual(list(test_alpha_ye_json.keys()), ['YE', 'YT', 'ZA', 'ZM', 'ZW'], 
            f"Expected and observed list of country codes do not match:\n{list(test_alpha_ye_json.keys())}.")
        self.assertEqual(set(test_alpha_ye_csv["alphaCode"]), set(['YE', 'ZA', 'ZM', 'ZW']), 
            f"Expected and observed list of country codes do not match:\n{set(test_alpha_ye_csv['alphaCode'])}.")
#5.)
        with self.assertRaises(ValueError):
            export_iso3166_2(alpha_codes_range=test_alpha_aa_ad, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, extract_lat_lng=False) #AA-AD
            export_iso3166_2(alpha_codes_range=test_alpha_xm_xx, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, extract_lat_lng=False) #XM-XX
#6.)
        with self.assertRaises(TypeError):
            export_iso3166_2(alpha_codes_range=123, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, extract_lat_lng=False) #123
            export_iso3166_2(alpha_codes_range=10.05, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, extract_lat_lng=False) #10.4
            export_iso3166_2(alpha_codes_range=False, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, extract_lat_lng=False) #False

    @unittest.skip("")
    def test_export_history(self):
        """ Testing correct ISO 3166-2 data with history attribute included are exported correctly. """
        test_alpha_ae = "AE" #UAE   
        test_alpha_it = "ITA" #Italy
        test_alpha_si = "SVN" #Slovenia
        test_alpha_lu_mk_om = "LU, MKD, 512" #Luxembourg, North Macedonia, Oman
#1.)
        export_iso3166_2(alpha_codes=test_alpha_ae, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, extract_lat_lng=False, history=True) #UAE 

        #open exported json & csv
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "_AE.json")) as output_json:
            test_iso3166_2_ae_json = json.load(output_json)

        #AE-AJ - ‘Ajmān
        expected_ae_aj_history = ['2015-11-27: Change of spelling of AE-AJ, AE-RK; addition of local variation of AE-FU, AE-RK, AE-UQ; update List Source. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:AE.']
        self.assertEqual(test_iso3166_2_ae_json["AE"]["AE-AJ"]["history"], expected_ae_aj_history, 
            f"Expected subdivision history attribute for AE-AJ does not match output:\n{test_iso3166_2_ae_json['AE']['AE-AJ']['history']}")
        #AE-AZ - Abū Z̧aby
        expected_ae_az_history = ['2002-08-20: Error correction: Spelling correction in AE-AZ. Source: Newsletter I-3 - https://web.archive.org/web/20081218103236/http://www.iso.org/iso/iso_3166-2_newsletter_i-3_en.pdf.']
        self.assertEqual(test_iso3166_2_ae_json["AE"]["AE-AZ"]["history"], expected_ae_az_history, 
            f"Expected subdivision history attribute for AE-AZ does not match output:\n{test_iso3166_2_ae_json['AE']['AE-AZ']['history']}")
        #AE-RK - Ra’s al Khaymah
        expected_ae_rk_history = ['2015-11-27: Change of spelling of AE-AJ, AE-RK; addition of local variation of AE-FU, AE-RK, AE-UQ; update List Source. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:AE.', 
                                  '2002-05-21: Spelling correction in AE-RK. Source: Newsletter I-2 - https://web.archive.org/web/20081218103157/http://www.iso.org/iso/iso_3166-2_newsletter_i-2_en.pdf.']
        self.assertEqual(test_iso3166_2_ae_json["AE"]["AE-RK"]["history"], expected_ae_rk_history, 
            f"Expected subdivision history attribute for AE-RK does not match output:\n{test_iso3166_2_ae_json['AE']['AE-RK']['history']}")
#2.)
        export_iso3166_2(alpha_codes=test_alpha_it, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, extract_lat_lng=False, history=True) #Italy 

        #open exported json & csv
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "_IT.json")) as output_json:
            test_iso3166_2_it_json = json.load(output_json)

        #IT-BT - Barletta-Andria-Trani
        expected_it_bt_history = ["2010-02-03 (corrected 2010-02-19): Subdivisions added: IT-BT Barletta-Andria-Trani. IT-FM Fermo. IT-MB Monza e Brianza. Codes: IT-FO Forlì -> IT-FC Forlì-Cesena. Description of Change: " \
                                  "Addition of the country code prefix as the first code element, administrative update. Source: Newsletter II-1 - https://www.iso.org/files/live/sites/isoorg/files/archive/pdf/en/iso_3166-2_newsletter_ii-1_corrected_2010-02-19.pdf."]       
        self.assertEqual(test_iso3166_2_it_json["IT"]["IT-BT"]["history"], expected_it_bt_history, 
            f"Expected subdivision history attribute does not match output:\n{test_iso3166_2_it_json['IT']['IT-BT']['history']}")
        #IT-FM -Fermo
        expected_it_fm_history = ["2010-02-03 (corrected 2010-02-19): Subdivisions added: IT-BT Barletta-Andria-Trani. IT-FM Fermo. IT-MB Monza e Brianza. Codes: IT-FO Forlì -> IT-FC Forlì-Cesena. Description of Change: " \
                                  "Addition of the country code prefix as the first code element, administrative update. Source: Newsletter II-1 - https://www.iso.org/files/live/sites/isoorg/files/archive/pdf/en/iso_3166-2_newsletter_ii-1_corrected_2010-02-19.pdf."]
        self.assertEqual(test_iso3166_2_it_json["IT"]["IT-FM"]["history"], expected_it_fm_history, 
            f"Expected subdivision history attribute does not match output:\n{test_iso3166_2_it_json['IT']['IT-FM']['history']}")
        #IT-SU - Sud Sardegna
        expected_it_su_history = ['2020-11-24: Code changes: IT-SD -> IT-SU Sud Sardegna. Subdivisions added: IT-GO Gorizia. IT-PN Pordenone. IT-TS Trieste. IT-UD Udine. Description of Change: Correction of subdivision code from IT-SD to IT-SU; Addition of category decentralized regional entity; addition of decentralized regional entity IT-GO, IT-PN, IT-TS, IT-UD; Update List Source. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:IT.']       
        self.assertEqual(test_iso3166_2_it_json["IT"]["IT-SU"]["history"], expected_it_su_history, 
            f"Expected subdivision history attribute does not match output:\n{test_iso3166_2_it_json['IT']['IT-SU']['history']}")
#3.)
        export_iso3166_2(alpha_codes=test_alpha_si, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, extract_lat_lng=False, history=True) #Slovenia 

        #open exported json & csv
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "_SI.json")) as output_json:
            test_iso3166_2_si_json = json.load(output_json)

        #SI-044 - Kanal ob Soči	
        expected_si_044_history = ["2022-11-29: Change of spelling of SI-044, SI-197; Addition of category urban municipality; Change of category name from municipality to urban municipality " 
                                   "for SI-011, SI-050, SI-052, SI-054, SI-061, SI-070, SI-080, SI-084, SI-085, SI-096, SI-112, SI-133; Update List Source. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:SI."]
        self.assertEqual(test_iso3166_2_si_json["SI"]["SI-044"]["history"], expected_si_044_history, 
            f"Expected subdivision history attribute does not match output:\n{test_iso3166_2_si_json['SI']['SI-044']['history']}")
        #SI-065 - Loška dolina	
        expected_si_065_history = ["2020-11-24: Correction of spelling for SI-065, SI-116, SI-169, SI-182, SI-204, SI-210; Deletion of asterisk from SI-212; Update List Source. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:SI."]
        self.assertEqual(test_iso3166_2_si_json["SI"]["SI-065"]["history"], expected_si_065_history, 
            f"Expected subdivision history attribute does not match output:\n{test_iso3166_2_si_json['SI']['SI-065']['history']}")
        #SI-212 - Mirna
        expected_si_212_history = ["2020-11-24: Correction of spelling for SI-065, SI-116, SI-169, SI-182, SI-204, SI-210; Deletion of asterisk from SI-212; Update List Source. " \
                                  "Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:SI.", "2014-11-03: Add 1 commune SI-212; update List Source. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:SI."]
        self.assertEqual(test_iso3166_2_si_json["SI"]["SI-212"]["history"], expected_si_212_history, 
            f"Expected subdivision history attribute does not match output:\n{test_iso3166_2_si_json['SI']['SI-212']['history']}")
#4.)
        export_iso3166_2(alpha_codes=test_alpha_lu_mk_om, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, extract_lat_lng=False, history=True) #Luxembourg, North Macedonia, Oman

        #open exported json & csv
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "_LU,MK,OM.json")) as output_json:
            test_iso3166_2_lu_mk_om_json = json.load(output_json)

        #LU-CA - Capellen
        expected_lu_ca_history = ["2015-11-27: Addition of cantons LU-CA, LU-CL, LU-DI, LU-EC, LU-ES, LU-GR, LU-LU, LU-ME, LU-RD, LU-RM, LU-VD, LU-WI; update List Source. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:LU."]
        self.assertEqual(test_iso3166_2_lu_mk_om_json["LU"]["LU-CA"]["history"], expected_lu_ca_history, 
            f"Expected subdivision history attribute does not match output:\n{test_iso3166_2_lu_mk_om_json['LU']['LU-CA']['history']}")
        #MK-801 - Aerodrom
        expected_mk_801_history = ['2020-03-02: Deletion of municipality MK-85; Change of subdivision code from MK-02 to MK-802, MK-03 to MK-201, MK-04 to MK-501, MK-05 to MK-401, MK-06 to MK-601, ' \
                                  'MK-07 to MK-402, MK-08 to MK-602, MK-10 to MK-403, MK-11 to MK-404, MK-12 to MK-301, MK-13 to MK-101, MK-14 to MK-202, MK-16 to MK-603, MK-18 to MK-405, MK-19 to ' \
                                  'MK-604, MK-20 to MK-102, MK-21 to MK-303, MK-22 to MK-304, MK-23 to MK-203, MK-24 to MK-103, MK-25 to MK-502, MK-26 to MK-406, MK-27 to MK-503, MK-30 to MK-605, MK-32 ' \
                                  'to MK-806, MK-33 to MK-204, MK-34 to MK-807, MK-35 to MK-606, MK-36 to MK-104, MK-37 to MK-205, MK-40 to MK-307, MK-41 to MK-407, MK-42 to MK-206, MK-43 to MK-701, MK-44 to ' \
                                  'MK-702, MK-45 to MK-504, MK-46 to MK-505, MK-47 to MK-703, MK-48 to MK-704, MK-49 to MK-105, MK-50 to MK-607, MK-51 to MK-207, MK-52 to MK-308, MK-53 to MK-506, MK-54 to MK-106, ' \
                                  'MK-55 to MK-507, MK-56 to MK-408, MK-58 to MK-310, MK-59 to MK-810, MK-60 to MK-208, MK-61 to MK-311, MK-62 to MK-508, MK-63 to MK-209, MK-64 to MK-409, MK-65 to MK-705, MK-66 to MK-509, ' \
                                  'MK-67 to MK-107, MK-69 to MK-108, MK-70 to MK-812, MK-71 to MK-706, MK-72 to MK-312, MK-73 to MK-410, MK-74 to MK-813, MK-75 to MK-608, MK-76 to MK-609, MK-78 to MK-313, MK-80 to MK-109, MK-81 ' \
                                  'to MK-210, MK-82 to MK-816, MK-83 to MK-211; Typographical correction of subdivision name of MK-816, addition of municipality MK-801, MK-803, MK-804, MK-805, MK-808, MK-809, MK-811, MK-814, MK-815, ' \
                                  'MK-817; Change of subdivision name of MK-304, MK-607; Update List Source; Update Code Source. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:MK.']
        
        self.assertEqual(test_iso3166_2_lu_mk_om_json["MK"]["MK-801"]["history"], expected_mk_801_history, 
            f"Expected subdivision history attribute does not match output:\n{test_iso3166_2_lu_mk_om_json['MK']['MK-801']['history']}")
        #OM-ZU - Z̧ufār
        expected_om_zu_history = ['2015-11-27: Change of subdivision category from region to governate for OM-BA, OM-DA, OM-SH, OM-WU, OM-ZA; change of subdivision code from OM-BA to OM-BJ, from OM-SH ' \
                                  'to OM-SJ; change of spelling of OM-BJ, OM-SJ; addition of governorates OM-BS, OM-SS; addition of local variations of OM-MA, OM-ZU; update List Source. Source: Online Browsing Platform (OBP) - ' \
                                  'https://www.iso.org/obp/ui/#iso:code:3166:OM.', '2010-06-30: Subdivisions added: OM-BU Al Buraymī. Codes: OM-JA Al Janūbīyah -> OM-ZU Z̧ufār. Description of Change: Update of the administrative structure ' \
                                  'and of the list source. Source: Newsletter II-2 - https://www.iso.org/files/live/sites/isoorg/files/archive/pdf/en/iso_3166-2_newsletter_ii-2_2010-06-30.pdf.']
        self.assertEqual(test_iso3166_2_lu_mk_om_json["OM"]["OM-ZU"]["history"], expected_om_zu_history, 
            f"Expected subdivision history attribute does not match output:\n{test_iso3166_2_lu_mk_om_json['OM']['OM-ZU']['history']}")

    @unittest.skip("")
    def test_export_city_data(self):
        """ Testing correct ISO 3166-2 data with city-level attribute are exported correctly. Only testing subset of cities per subdivision. """
        test_alpha_at_city_data = "AT"      #Austria
        test_alpha_km_city_data = "COM"     #Comoros
        test_alpha_mz_city_data = "MOZ"     #Mozambique
        test_alpha_pg_ro_city_data = "PG,RO" #Papa New Guinea, Romania
#1.)
        export_iso3166_2(alpha_codes=test_alpha_at_city_data, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, extract_lat_lng=False, state_city_data=True) #Austria 

        #open exported json & csv
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "_AT.json")) as output_json:
            test_iso3166_2_at_json = json.load(output_json)

        expected_at_1_city_data = ['Andau', 'Antau', 'Apetlon', 'Bad Sauerbrunn', 'Bad Tatzmannsdorf', 'Badersdorf', 'Bernstein', 'Bocksdorf', 'Breitenbrunn', 'Bruckneudorf', 
            'Deutsch Jahrndorf', 'Deutsch Kaltenbrunn', 'Deutschkreutz', 'Donnerskirchen', 'Drassburg', 'Eberau', 'Edelstal', 'Eisenstadt', 'Eisenstadt Stadt', 'Eisenstadt-Umgebung', 
            'Eltendorf', 'Forchtenstein', 'Frauenkirchen', 'Gattendorf', 'Gols']    #Burgenland
        #iterate through subset of city names for subdivision 
        for city in expected_at_1_city_data:
            self.assertIn(city, test_iso3166_2_at_json["AT"]["AT-1"]["cities"], f"City {city} not found in list of cities for AT-1 subdivision.")
#2.)
        export_iso3166_2(alpha_codes=test_alpha_km_city_data, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, extract_lat_lng=False, state_city_data=True) #Comoros 

        #open exported json & csv
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "_KM.json")) as output_json:
            test_iso3166_2_km_json = json.load(output_json)

        expected_km_g_city_data = ['Bahani', 'Bambadjani', 'Bouni', 'Chezani', 'Chindini', 'Chouani', 'Dembéni', 'Douniani', 'Dzahadjou', 'Foumbouni', 'Hantsindzi', 
                                   'Héroumbili', 'Itsandra', 'Itsandzéni', 'Ivouani', 'Koua', 'Madjeouéni', 'Mandza', 'Mavingouni', 'Mbéni', 'Mitsamiouli', 'Mitsoudjé', 
                                   'Mnoungou', 'Mohoro', 'Moroni', 'Mtsamdou', 'Mvouni', 'Nioumamilima']    #Andjazîdja
        #iterate through subset of city names for subdivision 
        for city in expected_km_g_city_data:
            self.assertIn(city, test_iso3166_2_km_json["KM"]["KM-G"]["cities"], f"City {city} not found in list of cities for KM-G (Andjazîdja) subdivision.")
#3.)
        export_iso3166_2(alpha_codes=test_alpha_mz_city_data, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, extract_lat_lng=False, state_city_data=True) #Mozambique 

        #open exported json & csv
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "_MZ.json")) as output_json:
            test_iso3166_2_mz_json = json.load(output_json)

        expected_mz_mpm_city_data = ['KaTembe', 'Maputo']  #Maputo
        #iterate through subset of city names for subdivision 
        for city in expected_mz_mpm_city_data:
            self.assertIn(city, test_iso3166_2_mz_json["MZ"]["MZ-MPM"]["cities"], f"City {city} not found in list of cities for MZ-MPM subdivision.")
#4.)
        export_iso3166_2(alpha_codes=test_alpha_pg_ro_city_data, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, extract_lat_lng=False, state_city_data=True) #Papa New Guinea, Romania 

        #open exported json & csv
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "_PG,RO.json")) as output_json:
            test_iso3166_2_pg_ro_json = json.load(output_json)

        expected_pg_ro_city_data = {"PG-NIK": ['Kavieng', 'Namatanai'], "RO-DB": ['Adânca', 'Aninoasa', 'Bezdead', 'Bilciureşti', 'Braniştea', 'Brezoaele', 'Brezoaia', 'Broșteni', 
                                    'Brăneşti', 'Buciumeni', 'Bucşani', 'Bungetu', 'Butimanu', 'Bâldana', 'Bădeni', 'Băleni Sârbi', 'Bălteni', 'Bărbuleţu', 'Cazaci', 'Ciocănari', 
                                    'Ciocăneşti', 'Cojasca', 'Colacu', 'Comişani', 'Comuna Aninoasa', 'Comuna Bezdead', 'Comuna Bilciureşti', 'Comuna Braniştea', 'Comuna Brezoaele', 'Comuna Brăneşti']} #New Ireland & Dâmbovița
        #iterate through subset of city names per subdivision 
        for subdivision_code in expected_pg_ro_city_data:
            for city in expected_pg_ro_city_data[subdivision_code]:
                self.assertIn(city, test_iso3166_2_pg_ro_json[subdivision_code.split('-')[0]][subdivision_code]["cities"], f"City {city} not found in list of cities for {subdivision_code} subdivision.")

    @unittest.skip("")
    def test_export_lat_lng(self):
        """ Testing latLng attribute is correctly exported via GoogleMaps API. """
        test_alpha_cl = "CL" #Chile
        test_alpha_dm = "DM" #Dominica 
        test_alpha_gn = "GIN" #Guinea
        test_alpha_la = "418" #Laos
#1.)
        export_iso3166_2(alpha_codes=test_alpha_cl, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, extract_lat_lng=True) #Chile

        #open exported json, csv and xml
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "_CL.json")) as output_json:
            test_iso3166_2_cl_json = json.load(output_json)

        #CL-AT - Atacama
        test_iso3166_2_cl_json_cl_at_expected_latlng = [-27.566, -70.05]
        self.assertEqual(test_iso3166_2_cl_json_cl_at_expected_latlng, test_iso3166_2_cl_json["CL"]["CL-AT"]["latLng"], 
            f"Expected and observed latLng subdivision output for CL-AT do not match:\n{test_iso3166_2_cl_json_cl_at_expected_latlng}\n{test_iso3166_2_cl_json['CL']['CL-AT']['latLng']}.")
        #CL-LI - Libertador General Bernardo O'Higgins
        test_iso3166_2_cl_json_cl_li_expected_latlng = [-34.576, -71.002]
        self.assertEqual(test_iso3166_2_cl_json_cl_li_expected_latlng, test_iso3166_2_cl_json["CL"]["CL-LI"]["latLng"], 
            f"Expected and observed latLng subdivision output for CL-LI do not match:\n{test_iso3166_2_cl_json_cl_li_expected_latlng}\n{test_iso3166_2_cl_json['CL']['CL-LI']['latLng']}.")
#2.)
        export_iso3166_2(alpha_codes=test_alpha_dm, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, extract_lat_lng=True) #Dominica

        #open exported json, csv and xml
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "_DM.json")) as output_json:
            test_iso3166_2_dm_json = json.load(output_json)

        #DM-03 - Saint David
        test_iso3166_2_dm_json_dm_03_expected_latlng = [15.408, -61.292]
        self.assertEqual(test_iso3166_2_dm_json_dm_03_expected_latlng, test_iso3166_2_dm_json["DM"]["DM-03"]["latLng"], 
            f"Expected and observed latLng subdivision output for DM-03 do not match:\n{test_iso3166_2_dm_json_dm_03_expected_latlng}\n{test_iso3166_2_dm_json['DM']['DM-03']['latLng']}.")
        #DM-06 - Saint Joseph
        test_iso3166_2_dm_json_dm_06_expected_latlng = [15.406, -61.422]
        self.assertEqual(test_iso3166_2_dm_json_dm_06_expected_latlng, test_iso3166_2_dm_json["DM"]["DM-06"]["latLng"], 
            f"Expected and observed latLng subdivision output for DM-06 do not match:\n{test_iso3166_2_dm_json_dm_06_expected_latlng}\n{test_iso3166_2_dm_json['DM']['DM-06']['latLng']}.")
#3.)
        export_iso3166_2(alpha_codes=[test_alpha_gn, test_alpha_la], export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=1, extract_lat_lng=True) #Guinea, Laos

        #open exported json, csv and xml
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "_GN,LA.json")) as output_json:
            test_iso3166_2_gn_la_json = json.load(output_json)

        #GN-BE - Beyla
        test_iso3166_2_gn_json_gn_be_expected_latlng = [8.688, -8.644]
        self.assertEqual(test_iso3166_2_gn_json_gn_be_expected_latlng, test_iso3166_2_gn_la_json["GN"]["GN-BE"]["latLng"], 
            f"Expected and observed latLng subdivision output for GN-BE do not match:\n{test_iso3166_2_gn_json_gn_be_expected_latlng}\n{test_iso3166_2_gn_la_json['GN']['GN-BE']['latLng']}.")
        #GN-C - Conakry
        test_iso3166_2_gn_json_gn_c_expected_latlng = [9.509, -13.712]
        self.assertEqual(test_iso3166_2_gn_json_gn_c_expected_latlng, test_iso3166_2_gn_la_json["GN"]["GN-C"]["latLng"], 
            f"Expected and observed latLng subdivision output for GN-C do not match:\n{test_iso3166_2_gn_json_gn_c_expected_latlng}\n{test_iso3166_2_gn_la_json['GN']['GN-C']['latLng']}.")
        #LA-HO - Houaphan
        test_iso3166_2_la_json_la_ho_expected_latlng = [20.325, 104.1]
        self.assertEqual(test_iso3166_2_la_json_la_ho_expected_latlng, test_iso3166_2_gn_la_json["LA"]["LA-HO"]["latLng"], 
            f"Expected and observed latLng subdivision output for LA-HO do not match:\n{test_iso3166_2_la_json_la_ho_expected_latlng}\n{test_iso3166_2_gn_la_json['LA']['LA-HO']['latLng']}.")
        #LA-LM - Louang Namtha
        test_iso3166_2_la_json_la_lm_expected_latlng = [20.948, 101.402]
        self.assertEqual(test_iso3166_2_la_json_la_lm_expected_latlng, test_iso3166_2_gn_la_json["LA"]["LA-LM"]["latLng"], 
            f"Expected and observed latLng subdivision output for LA-LM do not match:\n{test_iso3166_2_la_json_la_lm_expected_latlng}\n{test_iso3166_2_gn_la_json['LA']['LA-LM']['latLng']}.")

    # @unittest.skip("")
    def test_save_each_iteration(self):
        """ Testing the saving of each subdivision export data per iteration rather than all in one go. """
        test_alpha_et_fj = "ET-FJ" #Ethiopia - Fiji
        test_alpha_lv_ma = "LV-MA" #Latvia - Morocco
#1.)
        export_iso3166_2(alpha_codes_range=test_alpha_et_fj, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=0, export_xml=0, 
            extract_lat_lng=False, save_each_iteration=True) #Ethiopia - Fiji

        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, self.test_output_filename + "_ET.json")), 
            f"Expected output JSON file to exist in folder: {os.path.join(self.test_output_dir, self.test_output_filename + '_ET.json')}.")
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, self.test_output_filename + "_FI.json")), 
            f"Expected output JSON file to exist in folder: {os.path.join(self.test_output_dir, self.test_output_filename + '_FI.json')}.")
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, self.test_output_filename + "_FJ.json")), 
            f"Expected output JSON file to exist in folder: {os.path.join(self.test_output_dir, self.test_output_filename + '_FJ.json')}.")
#2.)
        export_iso3166_2(alpha_codes_range=test_alpha_lv_ma, export_folder=self.test_output_dir, export_filename=self.test_output_filename, verbose=0, export_csv=0, export_xml=0, 
            extract_lat_lng=False, save_each_iteration=True) #Latvia - Morocco

        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, self.test_output_filename + "_LV.json")), 
            f"Expected output JSON file to exist in folder: {os.path.join(self.test_output_dir, self.test_output_filename + '_LV.json')}.")
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, self.test_output_filename + "_LY.json")), 
            f"Expected output JSON file to exist in folder: {os.path.join(self.test_output_dir, self.test_output_filename + '_LY.json')}.")
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, self.test_output_filename + "_MA.json")), 
            f"Expected output JSON file to exist in folder: {os.path.join(self.test_output_dir, self.test_output_filename + '_MA.json')}.")

    @classmethod
    def tearDown(self):
        """ Delete any temp export folder. """
        shutil.rmtree(self.test_output_dir)

if __name__ == '__main__':  
    #run all unit tests
    unittest.main(verbosity=2)    