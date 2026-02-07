from datetime import datetime
from scripts.main import *
from scripts.utils import *
from iso3166_2 import *
import json
import os
import re
import shutil
from pycountry import countries
import unittest
from numbers import Real
unittest.TestLoader.sortTestMethodsUsing = None

# @unittest.skip("Skipping update_subdivisions unit tests.")
class UpdateSubdivisionsTests(unittest.TestCase):
    """
    Test suite for testing update_subdivisions.py script that that is used for the 
    streamlining of subdivision additions, changes or deletions to the ISO 3166-2 data object.

    Test Cases
    ==========
    test_update_subdivisions_add:
        testing adding subdivisions to the main subdivisions object via update_subdivisions function.
    test_update_subdivisions_amend:
        testing amending existing subdivisions to the main subdivisions object via update_subdivisions function.
    test_update_subdivisions_delete:
        testing deleting existing subdivisions to the main subdivisions object via update_subdivisions function.
    test_update_subdivisions_csv:
        testing current csv used for updating subdivisions when exporting the ISO 3166-2 data.
        (tests/test_subdivision_updates.csv).
    test_update_subdivision_csv:
        testing metadata, row count and columns of the subdivision updates csv.
    test_update_subdivision_csv_implementation:
        testing that rows in subdivision updates CSV get implemented into the ISO 3166-2 object correctly.
    test_update_subdivisions_csv_unique:
        testing each row in the updates csv is unique.
    test_valid_subdivision_updates_alpha_subdivision_codes_names:
        testing all country and subdivision codes in updates csv are valid.
    """
    @classmethod
    def setUp(self):
        """ Initialise test variables. """
        #create test output directory - remove if already present
        self.test_output_dir = os.path.join("tests", "test_output")
        if (os.path.isdir(self.test_output_dir)):
            shutil.rmtree(self.test_output_dir)
        os.mkdir(self.test_output_dir)

        self.test_iso3166_2_copy = os.path.join(self.test_output_dir, "iso3166_2_copy.json")

        #create hard copy of iso3166-2.json object for testing on 
        with open(os.path.join("tests", "test_files", "test_iso3166-2.json"), "r") as input_json:
            iso3166_2_json = json.load(input_json)
        with open(self.test_iso3166_2_copy, "w") as output_json:
            json.dump(iso3166_2_json, output_json, ensure_ascii=False, indent=4)

        #import subdivision_updates.csv into a dataframe
        self.subdivision_updates_csv_filepath = os.path.join("tests", "test_files", "test_subdivision_updates.csv")
        self.subdivision_updates_df = pd.read_csv(self.subdivision_updates_csv_filepath, keep_default_na=False)

    # @unittest.skip("")
    def test_update_subdivisions_add(self):
        """ Testing adding subdivisions to the main subdivisions object via update_subdivisions function. """
        test_subdivision_gh = {"alpha_code": "GH", "subdivision_code": "GH-DD", "name": "New Ghanian subdivision", 
                               "local_other_name": "Local subdivision name", "type": "District", "lat_lng": None, "parent_code": "GH-AA", "flag": ""} #Ghana
        test_subdivision_lt = {"alpha_code": "LT", "subdivision_code": "LT-100", "name": "Vilnius 2.0 municipality", 
                               "local_other_name": "Vilnius 2.0 municipality", "type": "City municipality", "parent_code": "LT-UT", 
                               "flag": "https://github.com/amckenna41/iso3166-flags/blob/main/iso3166-2-flags/LT/LT-100.svg", "rest_countries_keys": "currencies,idd,carSigns"} #Lithuania
        test_subdivision_hk = {"alpha_code": "HKG", "subdivision_code": "HK-HK", "name": "Hong Kong Island", "local_other_name": "香港", "type": "District", 
                               "lat_lng": [22.3193, 114.1694], "parent_code": "HK-HK", "flag": "", "custom_attributes": {"population": 1188500, "area": 78}} #Hong Kong - adding additional RestCountries attributes of currencies, idd and carSigns, as well as custom population & area attributes
        test_subdivision_kz = {"alpha_code": "398", "subdivision_code": "KZ-100", "name": "New oblysy", "local_other_name": "жаңа облысы", "type": "region",
                               "lat_lng": [], "parent_code": "KZ-71", "flag": "", "custom_attributes": {"hdi": 0.6, "gini": 0.5}}  #Kazakhstan - excluding default keys of localOtherName and flag, as well as custom hdi & gini attributes
#1.)    
        test_subdivision_gh_update_subdivisions_output = update_subdivision(alpha_code=test_subdivision_gh["alpha_code"], subdivision_code=test_subdivision_gh["subdivision_code"], name=test_subdivision_gh["name"],   #Ghana (GH)
                                                                      local_other_name=test_subdivision_gh["local_other_name"], type_=test_subdivision_gh["type"], lat_lng=test_subdivision_gh["lat_lng"], parent_code=test_subdivision_gh["parent_code"], 
                                                                      flag="", iso3166_2_filename=self.test_iso3166_2_copy, export=True)
        expected_test_subdivision_gh_output = {'flag': '', 'latLng': None, 'localOtherName': 'Local subdivision name', 'name': 'New Ghanian subdivision', 'parentCode': 'GH-AA', 'type': 'District'}

        #import json with newly added subdivision
        with open(self.test_iso3166_2_copy, "r") as subdivision_update_json:
            test_subdivision_gh_subdivisions_json = json.load(subdivision_update_json)

        self.assertIn("GH-DD", list(test_subdivision_gh_subdivisions_json['GH'].keys()), 
            f"Expected new subdivision GH-DD to be in list of GH subdivisions:\n{list(test_subdivision_gh_subdivisions_json['GH'].keys())}.")
        self.assertEqual(test_subdivision_gh_update_subdivisions_output, {}, 
            f"Expected updates subdivision output to be an empty dict, got:\n{test_subdivision_gh_update_subdivisions_output}.")
        self.assertEqual(test_subdivision_gh_subdivisions_json['GH']['GH-DD'], expected_test_subdivision_gh_output, 
            f"Expected and observed subdivision output do not match:\n{test_subdivision_gh_subdivisions_json['GH']['GH-DD']}.")        
#2.)
        test_subdivision_lt_update_subdivisions_output = update_subdivision(alpha_code=test_subdivision_lt["alpha_code"], subdivision_code=test_subdivision_lt["subdivision_code"], name=test_subdivision_lt["name"],    #Lithuania (LT)
                                                                      local_other_name=test_subdivision_lt["local_other_name"], type_=test_subdivision_lt["type"], parent_code=test_subdivision_lt["parent_code"], 
                                                                      flag=test_subdivision_lt["flag"], iso3166_2_filename=self.test_iso3166_2_copy, rest_countries_keys=test_subdivision_lt["rest_countries_keys"], export=True)
        expected_test_subdivision_lt_output = {"name": "Vilnius 2.0 municipality", "localOtherName": "Vilnius 2.0 municipality", "type": "City municipality", 
                                         "latLng": [], "parentCode": "LT-UT", "flag": "https://github.com/amckenna41/iso3166-flags/blob/main/iso3166-2-flags/LT/LT-100.svg",
                                         "currencies": {"EUR": {"name": "Euro", "symbol": "€"}}, "carSigns": ["LT"], "idd": "Root: +3, Suffixes: ['70']"}
        
        #import json with newly added subdivision
        with open(self.test_iso3166_2_copy, "r") as subdivision_update_json:
            test_subdivision_lt_subdivisions_json = json.load(subdivision_update_json)

        self.assertIn("LT-100", list(test_subdivision_lt_subdivisions_json["LT"].keys()), 
            f"Expected new subdivision LT-100 to be in list of LT subdivisions:\n{list(test_subdivision_lt_subdivisions_json.keys())}.")
        self.assertEqual(test_subdivision_lt_update_subdivisions_output, {}, 
            f"Expected updates subdivision output to be an empty dict, got:\n{test_subdivision_lt_update_subdivisions_output}.")
        self.assertEqual(test_subdivision_lt_subdivisions_json['LT']['LT-100'], expected_test_subdivision_lt_output, 
            f"Expected and observed subdivision output do not match:\n{test_subdivision_lt_subdivisions_json['LT']['LT-100']}")
#3.)
        test_subdivision_hk_update_subdivisions_output = update_subdivision(alpha_code=test_subdivision_hk["alpha_code"], subdivision_code=test_subdivision_hk["subdivision_code"], name=test_subdivision_hk["name"],  #Hong Kong (HK)
                                                                      local_other_name=test_subdivision_hk["local_other_name"], type_=test_subdivision_hk["type"], parent_code=test_subdivision_hk["parent_code"], 
                                                                      flag=test_subdivision_hk["flag"], custom_attributes=test_subdivision_hk["custom_attributes"], iso3166_2_filename=self.test_iso3166_2_copy, export=True)
        expected_test_subdivision_hk_output = {'area': 78, 'flag': '', 'latLng': [], 'localOtherName': '香港', 'name': 'Hong Kong Island', 'parentCode': 'HK-HK', 'population': 1188500, 'type': 'District'}

        #import json with newly added subdivision
        with open(self.test_iso3166_2_copy, "r") as subdivision_update_json:
            test_subdivision_hk_subdivisions_json = json.load(subdivision_update_json)

        self.assertIn("HK-HK", list(test_subdivision_hk_subdivisions_json["HK"].keys()), 
            f"Expected new subdivision HK-HK to be in list of HK subdivisions:\n{list(test_subdivision_hk_subdivisions_json['HK'].keys())}.")
        self.assertEqual(test_subdivision_hk_update_subdivisions_output, {}, 
            f"Expected updates subdivision output to be an empty dict, got:\n{test_subdivision_hk_update_subdivisions_output}.")
        self.assertEqual(test_subdivision_hk_subdivisions_json['HK']['HK-HK'], expected_test_subdivision_hk_output, 
            f"Expected and observed subdivision output do not match:\n{test_subdivision_hk_subdivisions_json['HK']['HK-HK']}")
#4.)
        test_subdivision_kz_update_subdivisions_output = update_subdivision(alpha_code=test_subdivision_kz["alpha_code"], subdivision_code=test_subdivision_kz["subdivision_code"], name=test_subdivision_kz["name"],   #Kazakhstan (KZ)
                                                                      local_other_name=test_subdivision_kz["local_other_name"], type_=test_subdivision_kz["type"], lat_lng=test_subdivision_kz["lat_lng"], parent_code=test_subdivision_kz["parent_code"], 
                                                                      flag=test_subdivision_kz["flag"], custom_attributes=test_subdivision_kz["custom_attributes"], iso3166_2_filename=self.test_iso3166_2_copy, export=True)
        expected_test_subdivision_kz_output = {'flag': '', 'gini': 0.5, 'hdi': 0.6, 'latLng': [], 'localOtherName': 'жаңа облысы', 'name': 'New oblysy', 'parentCode': 'KZ-71', 'type': 'region'}

        #import json with newly added subdivision
        with open(self.test_iso3166_2_copy, "r") as subdivision_update_json:
            test_subdivision_kz_subdivisions_json = json.load(subdivision_update_json)

        self.assertIn("KZ-100", list(test_subdivision_kz_subdivisions_json['KZ'].keys()), 
            f"Expected new subdivision KZ-100 to be in list of KZ subdivisions:\n{list(test_subdivision_kz_subdivisions_json['KZ'].keys())}.")
        self.assertEqual(test_subdivision_kz_update_subdivisions_output, {}, 
            f"Expected updates subdivision output to be an empty dict, got:\n{test_subdivision_kz_update_subdivisions_output}.")
        self.assertEqual(test_subdivision_kz_subdivisions_json['KZ']['KZ-100'], expected_test_subdivision_kz_output, 
            f"Expected and observed subdivision output do not match:\n{test_subdivision_kz_subdivisions_json['KZ']['KZ-100']}")
#5.)
        with (self.assertRaises(OSError)):
            update_subdivision(subdivision_csv="invalid_csv.csv", iso3166_2_filename=self.test_iso3166_2_copy)
            update_subdivision(subdivision_csv=123, iso3166_2_filename=self.test_iso3166_2_copy)
#6.)
        with (self.assertRaises(ValueError)):
            update_subdivision(alpha_code="XY", subdivision_code="XY-XY", iso3166_2_filename=self.test_iso3166_2_copy)  #invalid alpha code
            update_subdivision(alpha_code="AD,DE,FR", subdivision_code="AD-ZZ", iso3166_2_filename=self.test_iso3166_2_copy)  #more than 1 alpha code
            update_subdivision(alpha_code="PK", subdivision_code="PK-AA", parent_code="PK-ZZ", iso3166_2_filename=self.test_iso3166_2_copy, export=True)  #invalid parent code
            update_subdivision(alpha_code="SS", subdivision_code="SS-BW,SS-NU", parent_code="SS-WR", iso3166_2_filename=self.test_iso3166_2_copy, export=True)  #more than 1 subdivision code
            update_subdivision(alpha_code="ZA", subdivision_code="AD-10")  #1st half of subdivision code doesn't match country code
#7.)
        with (self.assertRaises(TypeError)):
            update_subdivision(alpha_code=123, subdivision_code="XY-XY", iso3166_2_filename=self.test_iso3166_2_copy, export=True)
            update_subdivision(alpha_code="ID", subdivision_code=False, iso3166_2_filename=self.test_iso3166_2_copy, export=True)
            update_subdivision(alpha_code="ID", subdivision_code="ID-12", name=5.5, iso3166_2_filename=self.test_iso3166_2_copy)
            update_subdivision(alpha_code="ID", subdivision_code="ID-12", local_other_name=5.5, iso3166_2_filename=self.test_iso3166_2_copy)
            update_subdivision(alpha_code="ID", subdivision_code="ID-12", lat_lng=5.5, iso3166_2_filename=self.test_iso3166_2_copy)
            update_subdivision(alpha_code="ID", subdivision_code="ID-12", parent_code=123, iso3166_2_filename=self.test_iso3166_2_copy)
            update_subdivision(alpha_code="ID", subdivision_code="ID-12", flag=False, iso3166_2_filename=self.test_iso3166_2_copy)
            update_subdivision(alpha_code="ID", subdivision_code="ID-12", rest_countries_keys=9.05, iso3166_2_filename=self.test_iso3166_2_copy)
            update_subdivision(alpha_code="ID", subdivision_code="ID-12", iso3166_2_filename=self.test_iso3166_2_copy)
            update_subdivision(alpha_code="ID", subdivision_code="ID-12", custom_attributes="blahblah", iso3166_2_filename=self.test_iso3166_2_copy)

    # @unittest.skip("")
    def test_update_subdivisions_amend(self):
        """ Testing amending subdivisions to the main subdivisions object via update_subdivisions function. """
        test_subdivision_jo_ka = {"alpha_code": "JO", "subdivision_code": "JO-KA", "name": "Al Karak 2", "local_other_name": "Al Karak 2.5"} #Al Karak - changing subdivision name and local name
        test_subdivision_rs_00 = {"alpha_code": "RS", "subdivision_code": "RS-00", "type": "Region", "parent_code": "RS-10"} #Beograd - changing subdivision type and parent code
        test_subdivision_tz_03 = {"alpha_code": "TZ", "subdivision_code": "TZ-03", "local_other_name": "Jiji Kuu la Dodoma", "type": "Capital", "flag": "flag.jpeg"} #Dodoma - changing subdivision local name, type and flag 
        test_subdivision_wf_sg = {"alpha_code": "WF", "subdivision_code": "WF-SG (WF-SW)"} #Sigave - changing subdivision code
        test_subdivision_my_02_error = {"alpha_code": "MY", "subdivision_code": "MY-02", "custom_attributes": {"population": 123, "area": 100}}
        test_subdivision_om_ma_error = {"alpha_code": "OM", "subdivision_code": "OM-MA", "custom_attributes": {"custom_attribute": "abc"}}
#1.)
        test_subdivision_jo_ka_update_subdivisions_output = update_subdivision(alpha_code=test_subdivision_jo_ka["alpha_code"], subdivision_code=test_subdivision_jo_ka["subdivision_code"], name=test_subdivision_jo_ka["name"], 
                                                                               local_other_name=test_subdivision_jo_ka["local_other_name"], iso3166_2_filename=self.test_iso3166_2_copy, export=True)  #Jordan (JO-KA)
        expected_test_subdivision_jo_ka_output = {"flag": None, "history": None, "latLng": [31.1257, 35.8247], "localOtherName": "Al Karak 2.5", "name": "Al Karak 2", "parentCode": None, "type": "Governorate"}

        #import json with newly amended subdivision
        with open(self.test_iso3166_2_copy, "r") as subdivision_update_json:
            test_subdivision_jo_ka_subdivisions_json = json.load(subdivision_update_json)

        self.assertEqual(test_subdivision_jo_ka_update_subdivisions_output, {}, 
            f"Expected updates subdivision output to be an empty dict, got:\n{test_subdivision_jo_ka_update_subdivisions_output}.")
        self.assertEqual(test_subdivision_jo_ka_subdivisions_json['JO']['JO-KA'], expected_test_subdivision_jo_ka_output, 
            f"Expected and observed subdivision output do not match:\n{test_subdivision_jo_ka_subdivisions_json['JO']['JO-KA']}.")    
#2.)
        test_subdivision_rs_00_update_subdivisions_output = update_subdivision(alpha_code=test_subdivision_rs_00["alpha_code"], subdivision_code=test_subdivision_rs_00["subdivision_code"], type_=test_subdivision_rs_00["type"], 
                                                                               parent_code=test_subdivision_rs_00["parent_code"], iso3166_2_filename=self.test_iso3166_2_copy, export=True)  #Serbia (RS)
        expected_test_subdivision_rs_00_output = {'flag': "https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/RS/RS-00.svg", 'history': None, 'latLng': [44.6802, 20.3818], 'localOtherName': 'Београд (srp), Belgrade (eng)', 'name': 'Beograd', 'parentCode': 'RS-10', 'type': 'Region'}
        
        #import json with newly amended subdivision
        with open(self.test_iso3166_2_copy, "r") as subdivision_update_json:
            test_subdivision_rs_00_subdivisions_json = json.load(subdivision_update_json)

        self.assertEqual(test_subdivision_rs_00_update_subdivisions_output, {}, 
            f"Expected updates subdivision output to be an empty dict, got:\n{test_subdivision_rs_00_update_subdivisions_output}.")
        self.assertEqual(test_subdivision_rs_00_subdivisions_json['RS']['RS-00'], expected_test_subdivision_rs_00_output, 
            f"Expected and observed subdivision output do not match:\n{test_subdivision_rs_00_subdivisions_json['RS']['RS-00']}.")  
#3.)
        test_subdivision_tz_03_update_subdivisions_output = update_subdivision(alpha_code=test_subdivision_tz_03["alpha_code"], subdivision_code=test_subdivision_tz_03["subdivision_code"], local_other_name=test_subdivision_tz_03["local_other_name"], 
                                                                               type_=test_subdivision_tz_03["type"], flag=test_subdivision_tz_03["flag"], iso3166_2_filename=self.test_iso3166_2_copy, export=True)  #Tanzania (TZ)
        expected_test_subdivision_tz_03_output = {'flag': 'flag.jpeg', 'history': None, 'latLng': [-6.0103, 35.8245], 'localOtherName': 'Jiji Kuu la Dodoma', 'name': 'Dodoma', 'parentCode': None, 'type': 'Capital'}
        
        #import json with newly added subdivision
        with open(self.test_iso3166_2_copy, "r") as subdivision_update_json:
            test_subdivision_tz_03_subdivisions_json = json.load(subdivision_update_json)

        self.assertEqual(test_subdivision_tz_03_update_subdivisions_output, {}, 
            f"Expected updates subdivision output to be an empty dict, got:\n{test_subdivision_tz_03_update_subdivisions_output}.")
        self.assertEqual(test_subdivision_tz_03_subdivisions_json['TZ']['TZ-03'], expected_test_subdivision_tz_03_output, 
            f"Expected and observed subdivision output do not match:\n{test_subdivision_tz_03_subdivisions_json['TZ']['TZ-03']}.")  
#4.)
        test_subdivision_wf_sg_update_subdivisions_output = update_subdivision(alpha_code=test_subdivision_wf_sg["alpha_code"], subdivision_code=test_subdivision_wf_sg["subdivision_code"], 
                                                                         iso3166_2_filename=self.test_iso3166_2_copy, export=True)  #Wallis and Futuna (WF)
        expected_test_subdivision_wf_sg_output = {'flag': 'https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/WF/WF-SG.svg', 
                                                  'history': [{'Change': 'Addition of administrative precinct WF-AL, WF-SG, WF-UV; update List Source code source and categories.', 
                                                               'Description of Change': None, 'Date Issued': '2015-11-27', 'Source': 'Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:WF.'}], 
                                                               'latLng': [-14.2667, -178.1667], 'localOtherName': 'Singave (eng), Sigavé (wls)', 'name': 'Sigave', 'parentCode': None, 'type': 'Administrative precinct'}
        #import json with newly added subdivision
        with open(self.test_iso3166_2_copy, "r") as subdivision_update_json:
            test_subdivision_wf_sg_subdivisions_json = json.load(subdivision_update_json)
        
        self.assertEqual(test_subdivision_wf_sg_update_subdivisions_output, {}, 
            f"Expected updates subdivision output to be an empty dict, got:\n{test_subdivision_wf_sg_update_subdivisions_output}.")
        self.assertEqual(test_subdivision_wf_sg_subdivisions_json['WF']['WF-SW'], expected_test_subdivision_wf_sg_output, 
            f"Expected and observed subdivision output do not match:\n{test_subdivision_wf_sg_subdivisions_json['WF']['WF-SW']}.")  
#5.)
        with self.assertRaises(ValueError):
            test_subdivision_my_02_update_subdivisions_output = update_subdivision(alpha_code=test_subdivision_my_02_error["alpha_code"], subdivision_code=test_subdivision_my_02_error["subdivision_code"], 
                                                                            custom_attributes=test_subdivision_my_02_error["custom_attributes"], iso3166_2_filename=self.test_iso3166_2_copy, export=True)  #Myanmar (MY)
            test_subdivision_om_ma_update_subdivisions_output = update_subdivision(alpha_code=test_subdivision_om_ma_error["alpha_code"], subdivision_code=test_subdivision_om_ma_error["subdivision_code"], 
                                                                            custom_attributes=test_subdivision_om_ma_error["custom_attributes"], iso3166_2_filename=self.test_iso3166_2_copy, export=True)  #Oman (OM)
    
    # @unittest.skip("")
    def test_update_subdivisions_delete(self):
        """ Testing deleting subdivisions to the main subdivisions object via update_subdivisions function. """
        test_subdivision_kw = "KW" #Kuwait
        test_subdivision_me = "ME" #Montenegro
        test_subdivision_ru = "RU" #Russia 
        test_subdivision_sm = "SM" #San Marino 
#1.)    
        test_subdivision_kw_update_subdivisions_output = update_subdivision(alpha_code=test_subdivision_kw, subdivision_code="KU", 
                                                                            iso3166_2_filename=self.test_iso3166_2_copy, delete=1)     #Kuwait (KW)
        
        #import json with newly deleted subdivision
        with open(self.test_iso3166_2_copy, "r") as subdivision_update_json:
            test_subdivision_kw_subdivisions_json = json.load(subdivision_update_json)

        self.assertNotIn("KW-KU", list(test_subdivision_kw_subdivisions_json['KW'].keys()), 
            f"Expected subdivision KW-KU to not be in list of KW subdivisions:\n{list(test_subdivision_kw_subdivisions_json['KW'].keys())}.")
        self.assertEqual(test_subdivision_kw_update_subdivisions_output, {}, 
            f"Expected updates subdivision output to be an empty dict, got:\n{test_subdivision_kw_update_subdivisions_output}.") 
#2.)
        test_subdivision_me_update_subdivisions_output = update_subdivision(alpha_code=test_subdivision_me, subdivision_code="07", 
                                                                            iso3166_2_filename=self.test_iso3166_2_copy, delete=1)     #Montenegro (ME)
        
        #import json with newly deleted subdivision
        with open(self.test_iso3166_2_copy, "r") as subdivision_update_json:
            test_subdivision_me_subdivisions_json = json.load(subdivision_update_json)

        self.assertNotIn("ME-07", list(test_subdivision_me_subdivisions_json['ME'].keys()), 
            f"Expected subdivision ME-07 to not be in list of ME subdivisions:\n{list(test_subdivision_me_subdivisions_json['ME'].keys())}.")
        self.assertEqual(test_subdivision_me_update_subdivisions_output, {}, 
            f"Expected updates subdivision output to be an empty dict, got:\n{test_subdivision_me_update_subdivisions_output}.") 
#3.)
        test_subdivision_ru_update_subdivisions_output = update_subdivision(alpha_code=test_subdivision_ru, subdivision_code="BRY", 
                                                                            iso3166_2_filename=self.test_iso3166_2_copy, delete=1)     #Russia (RU)
        
        #import json with newly deleted subdivision
        with open(self.test_iso3166_2_copy, "r") as subdivision_update_json:
            test_subdivision_ru_subdivisions_json = json.load(subdivision_update_json)

        self.assertNotIn("RU-BRY", list(test_subdivision_ru_subdivisions_json['RU'].keys()), 
            f"Expected subdivision RU-BRY to not be in list of RU subdivisions:\n{list(test_subdivision_ru_subdivisions_json['RU'].keys())}.")
        self.assertEqual(test_subdivision_ru_update_subdivisions_output, {}, 
            f"Expected updates subdivision output to be an empty dict, got:\n{test_subdivision_ru_update_subdivisions_output}.") 
#4.)
        test_subdivision_sm_update_subdivisions_output = update_subdivision(alpha_code=test_subdivision_sm, subdivision_code="02", 
                                                                            iso3166_2_filename=self.test_iso3166_2_copy, delete=1)     #San Marino (SM)

        #import json with newly deleted subdivision
        with open(self.test_iso3166_2_copy, "r") as subdivision_update_json:
            test_subdivision_sm_subdivisions_json = json.load(subdivision_update_json)

        self.assertNotIn("SM-02", list(test_subdivision_sm_subdivisions_json['SM'].keys()), 
            f"Expected new subdivision SM-02 to not be in list of SM subdivisions:\n{list(test_subdivision_sm_subdivisions_json['SM'].keys())}.")
        self.assertEqual(test_subdivision_sm_update_subdivisions_output, {}, 
            f"Expected updates subdivision output to be an empty dict, got:\n{test_subdivision_sm_update_subdivisions_output}.") 
#5.)
        with (self.assertRaises(ValueError)):
            update_subdivision(alpha_code="AD", subdivision_code="100", iso3166_2_filename=self.test_iso3166_2_copy, delete=1)  #subdivision doesn't exist
            update_subdivision(alpha_code="DE", subdivision_code="AD", iso3166_2_filename=self.test_iso3166_2_copy, delete=1)  #subdivision doesn't exist
            update_subdivision(alpha_code="ZA", subdivision_code="ABC", iso3166_2_filename=self.test_iso3166_2_copy, delete=1)  #subdivision doesn't exist

    # @unittest.skip("")
    def test_updates_subdivision_csv(self):
        """ Testing current csv used for updating subdivisions when exporting the ISO 3166-2 data (tests/test_files/test_subdivision_updates.csv). """
        #import csv, replace any Nan values with None
        update_subdivisions_csv = pd.read_csv(os.path.join("tests", "test_files", "test_subdivision_updates.csv"), header=0)
        update_subdivisions_csv = update_subdivisions_csv.replace(np.nan, None)
#1.)
        self.assertEqual(list(update_subdivisions_csv.columns), ["alphaCode", "subdivisionCode", "name", "localOtherName", "type", "parentCode", "flag", "latLng", "customAttributes", "delete", "notes", "dateIssued"],
            f"Expected column names don't match CSV columns:\n{update_subdivisions_csv.columns}.")
#2.)
        self.assertEqual(len(update_subdivisions_csv), 501, f"Expected 501 rows in the subdivision updates dataframe dataframe, got {len(update_subdivisions_csv)}.")
#3.)
        for index, row in update_subdivisions_csv.iterrows():
            self.assertIn(row["alphaCode"], [country.alpha_2 for country in countries], f"Expected row's 2 letter alpha code to be valid, got {row['alphaCode']}.")
#4.)
        for index, row in update_subdivisions_csv.iterrows():
            self.assertTrue(re.match(r'^[A-Z]{2}-[A-Za-z0-9]{1,3}( \([A-Z]{2}-[A-Za-z0-9]{1,3}\))?$', row["subdivisionCode"]), 
                f"Expected row subdivision code to follow the format XX-Y, XX-YY or XX-YYY format, got {row['subdivisionCode']}.")
#5.)
        for index, row in update_subdivisions_csv.iterrows():
            if ("deleting" in row["notes"].lower()):
                self.assertTrue(row["delete"])
#6.)
        is_valid_date = lambda date_string: bool(datetime.strptime(date_string, '%Y-%m-%d') if date_string else False)
        for index, row in update_subdivisions_csv.iterrows():
            self.assertTrue(is_valid_date(row["dateIssued"]))
#7.)
        for index, row in update_subdivisions_csv.iterrows():
            if (row["name"] != None):
                self.assertIsInstance(row["name"], str, f"Expected row value for name column to be a str, got {type(row['name'])}.")
            if (row["localOtherName"] is not None and not pd.isna(row["localOtherName"])):
                self.assertIsInstance(row["localOtherName"], str, f"Expected row value for localOtherName column to be a str, got {type(row['localOtherName'])}.")
            if (row["type"] != None):
                self.assertIsInstance(row["type"], str, f"Expected row value for type column to be a str, got {type(row['type'])}.")
            if (row["parentCode"] != None):
                self.assertIsInstance(row["parentCode"], str, f"Expected row value for parentCode column to be a str, got {type(row['parentCode'])}.")
            if (row["flag"] != None):
                self.assertIsInstance(row["flag"], str, f"Expected row value for flag column to be a str, got {type(row['flag'])}.")
            if (row["latLng"] != None):
                self.assertIsInstance(row["latLng"], str, f"Expected row value for latLng column to be a str, got {type(row['latLng'])}.")
            if (row["delete"] is not None and row["delete"] != ""):
                self.assertIsInstance(row["delete"], Real, f"Expected row value for delete column to be numeric, got {type(row['delete'])}.")
            if (row["notes"] != None):
                self.assertIsInstance(row["notes"], str, f"Expected row value for notes column to be a str, got {type(row['notes'])}.")
            if (row["dateIssued"] != None):
                self.assertIsInstance(row["dateIssued"], str, f"Expected row value for dateIssued column to be a str, got {type(row['dateIssued'])}.")

    # @unittest.skip("")
    def test_update_subdivisions_csv_unique(self):
        """ Testing each row in the subdivision updates csv is unique. """
        duplicates = self.subdivision_updates_df.duplicated()
        self.assertEqual(duplicates.sum(), 0, f"Found {duplicates.sum()} duplicate rows in the CSV.")

    @unittest.skip("")
    def test_updates_subdivision_csv_implementation(self):
        """ Testing that rows in subdivision updates CSV get implemented into the ISO 3166-2 object correctly. """
#1.)    
        test_updated_subdivision_data = update_subdivision(iso3166_2_filename=self.test_iso3166_2_copy, subdivision_csv=self.subdivision_updates_csv_filepath)

    # @unittest.skip("Need to rerun after exporting data.")
    def test_valid_subdivision_updates_alpha_subdivision_codes_names(self):
        """ Testing valid country and subdivision codes for each row. """
#1.)
        country_codes_to_check = self.subdivision_updates_df["alphaCode"]
        invalid_country_codes = country_codes_to_check[~country_codes_to_check.isin([country.alpha_2 for country in countries])]
        self.assertTrue(invalid_country_codes.empty, f"Expected all country codes to be valid ISO 3166-1 alpha-2 codes:\n{invalid_country_codes}.")
#2.)    
        #create instance of Subdivisions class from iso3166-2 software
        iso3166_2_obj = Subdivisions()

        #get list of valid subdivision codes in updates CSV, if any codes contain brackets, parse the code from the brackets, ignore rows where delete=1
        all_subdivision_codes = [code for codes in iso3166_2_obj.subdivision_codes().values() for code in codes]
        non_deletion_subdivisions_mask = pd.to_numeric(self.subdivision_updates_df.get("delete", 0), errors="coerce").fillna(0).astype(int) != 1
        non_deletion_subdivisions_df = self.subdivision_updates_df[non_deletion_subdivisions_mask]
        subdivisions_codes_to_check = non_deletion_subdivisions_df["subdivisionCode"]
        brackets_mask = subdivisions_codes_to_check.str.contains(r'\(', na=False)
        subdivisions_codes_clean = subdivisions_codes_to_check.where(~brackets_mask, subdivisions_codes_to_check.str.extract(r'\(([^()]+)\)', expand=False).str.strip())
        invalid_subdivision_codes = subdivisions_codes_clean[~subdivisions_codes_clean.isin(all_subdivision_codes)]
       
        self.assertTrue(invalid_subdivision_codes.empty, f"Expected all subdivision codes to be valid ISO 3166-2 subdivision codes:\n{invalid_subdivision_codes}.")

    @classmethod
    def tearDown(self):
        """ Delete any temp export folder. """
        shutil.rmtree(self.test_output_dir)

# Run the unit tests
if __name__ == '__main__':
    #run all unit tests
    unittest.main(verbosity=2)    