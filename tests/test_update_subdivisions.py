from iso3166_2_scripts.get_iso3166_2 import *
import json
import os
import shutil
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

@unittest.skip("")
class Update_Subdivisions_Tests(unittest.TestCase):
    """
    Test suite for testing update_subdivisions.py script that that is used for the 
    streamlining of subdivision additions, changes or deletions to the ISO 3166-2 data object.

    Test Cases
    ==========
    test_update_subdivisions_add:
        testing adding subdivisions to the main subdivisions object via update_subdivisions function.
    test_update_subdivisions_amend:
        testing amending subdivisions to the main subdivisions object via update_subdivisions function.
    test_update_subdivisions_delete:
        testing deleting subdivisions to the main subdivisions object via update_subdivisions function.
    """
    def setUp(self):
        """ Initialise test variables. """
        #create test output directory - remove if already present
        self.test_output_dir = "test_output"
        if (os.path.isdir(self.test_output_dir)):
            shutil.rmtree(self.test_output_dir)
        os.mkdir(self.test_output_dir)

        self.test_iso3166_2_copy = os.path.join(self.test_output_dir, "iso3166_2_copy.json")

        #create hard copy of iso3166-2.json object for testing on 
        with open(os.path.join("iso3166_2", "iso3166-2.json"), "r") as input_json:
            iso3166_2_json = json.load(input_json)
        with open(self.test_iso3166_2_copy, "w") as output_json:
            json.dump(iso3166_2_json, output_json)

    # @unittest.skip("")
    def test_update_subdivisions_add(self):
        """ Testing adding subdivisions to the main subdivisions object via update_subdivisions function. """
        test_subdivision_gh = "GH" #Ghana
        test_subdivision_lt = "LT" #Lithuania
        test_subdivision_hk = "HKG" #Hong Kong - adding additional RestCountries attributes of currencies, idd and carSigns
        test_subdivision_kz = "398" #Kazakhstan - excluding default keys of localName and flag
#1.)    
        test_subdivision_gh_update_subdivisions_output = update_subdivision(alpha_code=test_subdivision_gh, subdivision_code="GH-DD", name="New Ghanian subdivision",   #Ghana (GH)
                                                                      local_name="Local subdivision name", type_="District", lat_lng=None, parent_code="GH-AA", 
                                                                      flag="", iso3166_2_filename=self.test_iso3166_2_copy, export=True)
        expected_test_subdivision_gh_output = {"name": "New Ghanian subdivision", "localName": "Local subdivision name", "type": "District", 
                                         "latLng": None, "parentCode": "GH-AA", "flag": ""}
        
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
        test_subdivision_lt_update_subdivisions_output = update_subdivision(alpha_code=test_subdivision_lt, subdivision_code="LT-100", name="Vilnius 2.0 municipality",    #Lithuania (LT)
                                                                      local_name="Vilnius 2.0 municipality", type_="City municipality", parent_code="LT-UT", 
                                                                      flag="https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/LT/LT-100.svg", 
                                                                      iso3166_2_filename=self.test_iso3166_2_copy, rest_countries_keys="currencies,idd,carSigns", export=True)
        expected_test_subdivision_lt_output = {"name": "Vilnius 2.0 municipality", "localName": "Vilnius 2.0 municipality", "type": "City municipality", 
                                         "latLng": None, "parentCode": "LT-UT", "flag": "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/LT/LT-100.svg"}
        
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
        test_subdivision_hk_update_subdivisions_output = update_subdivision(alpha_code=test_subdivision_hk, subdivision_code="HK-HK", name="Hong Kong Island",  #Hong Kong (HK)
                                                                      local_name="香港", type_="District", lat_lng=[22.3193, 114.1694], parent_code="HK-HK", 
                                                                      flag="", iso3166_2_filename=self.test_iso3166_2_copy, export=True)
        expected_test_subdivision_hk_output = {"name": "Hong Kong Island", "localName": "香港", "type": "District", 
                                         "latLng": [22.319, 114.169], "parentCode": "HK-HK", "flag": ""}
        
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
        test_subdivision_kz_update_subdivisions_output = update_subdivision(alpha_code=test_subdivision_kz, subdivision_code="KZ-100", name="New oblysy",   #Kazakhstan (KZ)
                                                                      local_name="жаңа облысы", type_="Region", lat_lng=[], parent_code="KZ-71", 
                                                                      flag="", iso3166_2_filename=self.test_iso3166_2_copy, export=True)
        expected_test_subdivision_kz_output = {"name": "New oblysy", "localName": "жаңа облысы", "type": "Region", 
                                         "latLng": [], "parentCode": "KZ-71", "flag": ""}
        
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
            update_subdivision(alpha_code="XY", subdivision_code="XY-XY", iso3166_2_filename=self.test_iso3166_2_copy)
            update_subdivision(alpha_code="AD,DE,FR", subdivision_code="AD-ZZ", iso3166_2_filename=self.test_iso3166_2_copy)
            update_subdivision(alpha_code="PK", subdivision_code="PK-AA", parent_code="PK-ZZ", iso3166_2_filename=self.test_iso3166_2_copy, export=True)
            update_subdivision(alpha_code="SS", subdivision_code="SS-BW,SS-NU", parent_code="SS-WR", iso3166_2_filename=self.test_iso3166_2_copy, export=True)
#7.)
        with (self.assertRaises(TypeError)):
            update_subdivision(alpha_code=123, subdivision_code="XY-XY", iso3166_2_filename=self.test_iso3166_2_copy, export=True)
            update_subdivision(alpha_code="ID", subdivision_code=False, iso3166_2_filename=self.test_iso3166_2_copy, export=True)
            update_subdivision(alpha_code="ID", subdivision_code="ID-12", name=5.5, iso3166_2_filename=self.test_iso3166_2_copy)
            update_subdivision(alpha_code="ID", subdivision_code="ID-12", local_name=5.5, iso3166_2_filename=self.test_iso3166_2_copy)
            update_subdivision(alpha_code="ID", subdivision_code="ID-12", lat_lng=5.5, iso3166_2_filename=self.test_iso3166_2_copy)
            update_subdivision(alpha_code="ID", subdivision_code="ID-12", parent_code=123, iso3166_2_filename=self.test_iso3166_2_copy)
            update_subdivision(alpha_code="ID", subdivision_code="ID-12", flag=False, iso3166_2_filename=self.test_iso3166_2_copy)
            update_subdivision(alpha_code="ID", subdivision_code="ID-12", rest_countries_keys=9.05, iso3166_2_filename=self.test_iso3166_2_copy)
            update_subdivision(alpha_code="ID", subdivision_code="ID-12", exclude_default_keys=True, iso3166_2_filename=self.test_iso3166_2_copy)

    @unittest.skip("")
    def test_update_subdivisions_amend(self):
        """ Testing amending subdivisions to the main subdivisions object via update_subdivisions function. """
        test_subdivision_jo_ka = "JO-KA" #Al Karak - changing subdivision name and local name
        test_subdivision_rs_00 = "RS-00" #Beograd - changing subdivision type and parent code
        test_subdivision_tz_03 = "TZ-03" #Dodoma - changing subdivision local name, type and flag 
        test_subdivision_wf_sg = "WF-SG" #Sigave - changing subdivision code
#1.)
        test_subdivision_jo_ka_update_subdivisions_output = update_subdivision(alpha_code="JO", subdivision_code=test_subdivision_jo_ka, name="Al Karak 2", local_name="Al Karak 2", 
                                                                         iso3166_2_filename=self.test_iso3166_2_copy, export=True)  #Jordan (JO-KA)
        expected_test_subdivision_jo_ka_output = {"name": "Al Karak 2", "localName": "Al Karak 2", "type": "Governorate", 
                                         "latLng": [31.185, 35.705], "parentCode": None, "flag": None}
        
        #import json with newly added subdivision
        with open(self.test_iso3166_2_copy, "r") as subdivision_update_json:
            test_subdivision_jo_ka_subdivisions_json = json.load(subdivision_update_json)

        self.assertEqual(test_subdivision_jo_ka_update_subdivisions_output, {}, 
            f"Expected updates subdivision output to be an empty dict, got:\n{test_subdivision_jo_ka_update_subdivisions_output}.")
        self.assertEqual(test_subdivision_jo_ka_subdivisions_json['JO']['JO-KA'], expected_test_subdivision_jo_ka_output, 
            f"Expected and observed subdivision output do not match:\n{test_subdivision_jo_ka_subdivisions_json['JO']['JO-KA']}.")    
#2.)
        test_subdivision_rs_00_update_subdivisions_output = update_subdivision(alpha_code="RS", subdivision_code=test_subdivision_rs_00, type_="Region", parent_code="RS-10", 
                                                                         iso3166_2_filename=self.test_iso3166_2_copy, export=True)  #Serbia (RS)
        expected_test_subdivision_rs_00_output = {"name": "Beograd", "localName": "Beograd", "type": "Region", 
                                         "latLng": [44.813, 20.461], "parentCode": "RS-10", "flag": None}

        #import json with newly added subdivision
        with open(self.test_iso3166_2_copy, "r") as subdivision_update_json:
            test_subdivision_rs_00_subdivisions_json = json.load(subdivision_update_json)

        self.assertEqual(test_subdivision_rs_00_update_subdivisions_output, {}, 
            f"Expected updates subdivision output to be an empty dict, got:\n{test_subdivision_rs_00_update_subdivisions_output}.")
        self.assertEqual(test_subdivision_rs_00_subdivisions_json['RS']['RS-00'], expected_test_subdivision_rs_00_output, 
            f"Expected and observed subdivision output do not match:\n{test_subdivision_rs_00_subdivisions_json['RS']['RS-00']}.")  
#3.)
        test_subdivision_tz_03_update_subdivisions_output = update_subdivision(alpha_code="TZ", subdivision_code=test_subdivision_tz_03, local_name="Jiji Kuu la Dodoma", type_="Capital", flag="flag.jpeg", 
                                                                         iso3166_2_filename=self.test_iso3166_2_copy, export=True)  #Tanzania (TZ)
        expected_test_subdivision_tz_03_output = {"name": "Dodoma", "localName": "Jiji Kuu la Dodoma", "type": "Capital", 
                                         "latLng": [-6.181, 35.747], "parentCode": None, "flag": "flag.jpeg"}
        
        #import json with newly added subdivision
        with open(self.test_iso3166_2_copy, "r") as subdivision_update_json:
            test_subdivision_tz_03_subdivisions_json = json.load(subdivision_update_json)

        self.assertEqual(test_subdivision_tz_03_update_subdivisions_output, {}, 
            f"Expected updates subdivision output to be an empty dict, got:\n{test_subdivision_tz_03_update_subdivisions_output}.")
        self.assertEqual(test_subdivision_tz_03_subdivisions_json['TZ']['TZ-03'], expected_test_subdivision_tz_03_output, 
            f"Expected and observed subdivision output do not match:\n{test_subdivision_tz_03_subdivisions_json['TZ']['TZ-03']}.")  
#4.)
        test_subdivision_wf_sg_update_subdivisions_output = update_subdivision(alpha_code="WF", subdivision_code=test_subdivision_wf_sg + " (WF-SW)", 
                                                                         iso3166_2_filename=self.test_iso3166_2_copy, export=True)  #Wallis and Futuna (WF)
        expected_test_subdivision_wf_sg_output = {"name": "Sigave", "localName": "Sigave", "type": "Administrative precinct", 
                                         "latLng": [-14.297, -178.158], "parentCode": None, "flag": "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/WF/WF-SG.svg"}
        
        #import json with newly added subdivision
        with open(self.test_iso3166_2_copy, "r") as subdivision_update_json:
            test_subdivision_wf_sg_subdivisions_json = json.load(subdivision_update_json)
        
        self.assertEqual(test_subdivision_wf_sg_update_subdivisions_output, {}, 
            f"Expected updates subdivision output to be an empty dict, got:\n{test_subdivision_wf_sg_update_subdivisions_output}.")
        self.assertEqual(test_subdivision_wf_sg_subdivisions_json['WF']['WF-SW'], expected_test_subdivision_wf_sg_output, 
            f"Expected and observed subdivision output do not match:\n{test_subdivision_wf_sg_subdivisions_json['WF']['WF-SW']}.")  
        
    @unittest.skip("")
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
            f"Expected new subdivision KW-KU to not be in list of KW subdivisions:\n{list(test_subdivision_kw_subdivisions_json['KW'].keys())}.")
        self.assertEqual(test_subdivision_kw_update_subdivisions_output, {}, 
            f"Expected updates subdivision output to be an empty dict, got:\n{test_subdivision_kw_update_subdivisions_output}.") 
#2.)
        test_subdivision_me_update_subdivisions_output = update_subdivision(alpha_code=test_subdivision_me, subdivision_code="07", 
                                                                            iso3166_2_filename=self.test_iso3166_2_copy, delete=1)     #Montenegro (ME)
        
        #import json with newly deleted subdivision
        with open(self.test_iso3166_2_copy, "r") as subdivision_update_json:
            test_subdivision_me_subdivisions_json = json.load(subdivision_update_json)

        self.assertNotIn("ME-07", list(test_subdivision_me_subdivisions_json['ME'].keys()), 
            f"Expected new subdivision ME-07 to not be in list of ME subdivisions:\n{list(test_subdivision_me_subdivisions_json['ME'].keys())}.")
        self.assertEqual(test_subdivision_me_update_subdivisions_output, {}, 
            f"Expected updates subdivision output to be an empty dict, got:\n{test_subdivision_me_update_subdivisions_output}.") 
#3.)
        test_subdivision_ru_update_subdivisions_output = update_subdivision(alpha_code=test_subdivision_ru, subdivision_code="BRY", 
                                                                            iso3166_2_filename=self.test_iso3166_2_copy, delete=1)     #Russia (RU)
        
        #import json with newly deleted subdivision
        with open(self.test_iso3166_2_copy, "r") as subdivision_update_json:
            test_subdivision_ru_subdivisions_json = json.load(subdivision_update_json)

        self.assertNotIn("RU-BRY", list(test_subdivision_ru_subdivisions_json['RU'].keys()), 
            f"Expected new subdivision RU-BRY to not be in list of RU subdivisions:\n{list(test_subdivision_ru_subdivisions_json['RU'].keys())}.")
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
            update_subdivision(alpha_code="AD", subdivision_code="100", iso3166_2_filename=self.test_iso3166_2_copy, delete=1)
            update_subdivision(alpha_code="DE", subdivision_code="AD", iso3166_2_filename=self.test_iso3166_2_copy, delete=1)
            update_subdivision(alpha_code="ZA", subdivision_code="ABC", iso3166_2_filename=self.test_iso3166_2_copy, delete=1)

    def tearDown(self):
        """ Delete any temp export folder. """
        shutil.rmtree(self.test_output_dir)

if __name__ == '__main__':
    #run all unit tests
    unittest.main(verbosity=2)    