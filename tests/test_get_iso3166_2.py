import get_iso3166_2 as iso3166_2
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
    data for all countries from the data sources. 

    Test Cases
    ==========
    test_export_iso3166_2:
        testing correct ISO 3166-2 data is exported and pulled from data sources.
    """
    def setUp(self):
        """ Initialise test variables. """
        #initalise User-agent header for requests library 
        self.__version__ = "1.1.0"
        self.user_agent_header = {'User-Agent': 'iso3166-2/{} ({}; {})'.format(self.__version__,
                                            'https://github.com/amckenna41/iso3166-2', getpass.getuser())}
        self.test_output_dir = "test_output_dir"
        self.test_output_filename = "test_json"
    
        #list of output columns for main iso3166-2 json
        self.correct_output_attributes = [
            "altSpellings", "area", "borders", "capital", "capitalInfo", "car", "cca2", "cca3", "ccn3", "cioc", "coatOfArms",
            "continents", "currencies", "demonyms", "fifa", "flag", "flags", "gini", "idd", "independent", "landlocked",
            "languages", "latlng", "maps", "name", "population", "postalCode", "region", "startOfWeek", "status",
            "subdivisions", "subregion", "timezones", "tld", "translations", "unMember"
        ]
        os.environ["TQDM_DISABLE"] = "1"

    def test_export_iso3166_2(self):
        """ Testing export functionality for getting ISO 3166-2 data from data sources. """
        test_alpha2_dk = "DK" #Denmark
        test_alpha2_fk = "FK" #Falkland Islands
        test_alpha2_gd = "GD" #Grenada
        test_alpha2_kg_ms_nr = "KG,MS,NR" #Kyrgyzstan, Montserrat, Nauru
        test_alpha2_py_sl_tl = "PY,SL,TL" #Paraguay, Sierra Leone, Timor-Lests
        test_alpha2_bv_fo_gs_hk = ["BV", "FO", "GS", "HK"] #Bouvet Island, Faroe Islands, South Georgia, Hong Kong
        test_alpha2_error1 = "ZZ"
        test_alpha2_error2 = "ABCDEF"
        test_alpha2_error3 = 1234
#1.)
        iso3166_2.export_iso3166_2(alpha2_codes=test_alpha2_dk, output_folder=self.test_output_dir, json_filename=self.test_output_filename, verbose=0) #Denmark

        #open exported jsons
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha2_dk + ".json")) as output_json:
            test_iso3166_2_dk = json.load(output_json)
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha2_dk + "-min.json")) as output_json:
            test_iso3166_2_dk_min = json.load(output_json)

        self.assertIsInstance(test_iso3166_2_dk, dict, "Expected output to be type dict, got {}.".format(type(test_iso3166_2_dk)))
        self.assertEqual(len(test_iso3166_2_dk), 36, "Expected 36 keys/attributes in output dict, got {}.".format(len(test_iso3166_2_dk)))
        self.assertEqual(test_iso3166_2_dk["name"]["common"], "Denmark", "Name expected to be Denmark, got {}.".format(test_iso3166_2_dk["name"]["common"]))
        self.assertEqual(test_iso3166_2_dk["cca2"], "DK", "Expected alpha-2 code to be DK, got {}.".format(test_iso3166_2_dk["cca2"]))  
        self.assertEqual(test_iso3166_2_dk["cca3"], "DNK", "Expected alpha-3 code to be DNK, got {}.".format(test_iso3166_2_dk["cca3"]))     
        self.assertEqual(test_iso3166_2_dk["currencies"]["DKK"]['name'], "Danish krone", "Expected currency to be Danish krone, got {}.".format(test_iso3166_2_dk["currencies"]["DKK"]['name']))        
        self.assertEqual(test_iso3166_2_dk["capital"][0], "Copenhagen", "Expected capital city to be Copenhagen, got {}.".format(test_iso3166_2_dk["capital"][0]))        
        self.assertEqual(test_iso3166_2_dk["region"], "Europe", "Expected region to be Europe, got {}.".format(test_iso3166_2_dk["region"]))        
        self.assertEqual(list(test_iso3166_2_dk["languages"].keys()), ["dan"], "Expected language to be Danish, got {}.".format(list(test_iso3166_2_dk["languages"].keys())))        
        self.assertEqual(test_iso3166_2_dk["area"], 43094, "Expected total area to be 43094, got {}.".format(test_iso3166_2_dk["area"]))       
        self.assertEqual(test_iso3166_2_dk["population"], 5831404, "Expected population to be 5831404, got {}.".format(test_iso3166_2_dk["population"]))        
        self.assertEqual(len(test_iso3166_2_dk["subdivisions"]), 5, "Expected 5 total subdivisions, got {}.".format(len(test_iso3166_2_dk["subdivisions"])))
        self.assertEqual(test_iso3166_2_dk["latlng"], [56, 10], "Expected lat/longitude to be [56, 10], got {}.".format(test_iso3166_2_dk["latlng"]))        
        for col in test_iso3166_2_dk.keys(): 
            self.assertIn(col, self.correct_output_attributes, "Column {} not found in list of correct columns.".format(col))

        dk_subdivision_codes = ['DK-81', 'DK-82', 'DK-83', 'DK-84', 'DK-85']
        dk_subdivision_names = ['Nordjylland', 'Midtjylland', 'Syddanmark', 'Hovedstaden', 'Sjælland']

        self.assertIsInstance(test_iso3166_2_dk_min, dict, "Expected output object to be of type dict, got {}.".format(type(test_iso3166_2_dk_min)))
        self.assertEqual(len(test_iso3166_2_dk_min), 5, "Expected 5 total subdivision outputs, got {}.".format(len(test_iso3166_2_dk_min)))
        self.assertEqual(list(test_iso3166_2_dk_min.keys()), dk_subdivision_codes, "Subdivison codes do not equal expected codes:\n{}.".format(list(test_iso3166_2_dk_min.keys())))
        self.assertEqual(list(test_iso3166_2_dk_min['DK-81'].keys()), ['name', 'type', 'parent_code', 'latlng', 'flag_url'], "Expected keys for output dict don't match\n{}".format(list(test_iso3166_2_dk_min['DK-81'].keys())))
        for key in test_iso3166_2_dk_min:
            self.assertIn(test_iso3166_2_dk_min[key]["name"], dk_subdivision_names, "Subdivision name {} not found in list of subdivision names:\n{}.".format(test_iso3166_2_dk_min[key]["name"], dk_subdivision_names))
            if ((test_iso3166_2_dk_min[key]["flag_url"] is not None) or (test_iso3166_2_dk_min[key]["flag_url"] == "")):
                self.assertEqual(requests.get(test_iso3166_2_dk_min[key]["flag_url"], headers=self.user_agent_header).status_code, 200, "Flag URL invalid: {}.".format(test_iso3166_2_dk_min[key]["flag_url"]))
            self.assertIsNone(test_iso3166_2_dk_min[key]['parent_code'], "Parent code key cannot be None.")
            self.assertEqual(len(test_iso3166_2_dk_min[key]["latlng"]), 2, "Expected key should have both latitude and longitude.") 
#2.)    
        iso3166_2.export_iso3166_2(alpha2_codes=test_alpha2_fk, output_folder=self.test_output_dir, json_filename=self.test_output_filename, verbose=0) #Falkland Islands

        #open exported jsons
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha2_fk + ".json"))  as output_json:
            test_iso3166_2_fk = json.load(output_json)

        self.assertIsInstance(test_iso3166_2_fk, dict, "Expected output to be type dict, got {}.".format(type(test_iso3166_2_fk)))
        self.assertEqual(len(test_iso3166_2_fk), 36, "Expected 36 keys/attributes in output dict, got {}.".format(len(test_iso3166_2_fk)))
        self.assertEqual(test_iso3166_2_fk["name"]["common"], "Falkland Islands", "Name expected to be Falkland Islands, got {}.".format(test_iso3166_2_fk["name"]["common"]))      
        self.assertEqual(test_iso3166_2_fk["cca2"], "FK", "Expected alpha-2 code to be FK, got {}.".format(test_iso3166_2_fk["cca2"]))  
        self.assertEqual(test_iso3166_2_fk["cca3"], "FLK", "Expected alpha-3 code to be FLK, got {}.".format(test_iso3166_2_fk["cca3"]))     
        self.assertEqual(test_iso3166_2_fk["currencies"]["FKP"]['name'], "Falkland Islands pound", "Expected currency to be Falkland Islands pound, got {}.".format(test_iso3166_2_fk["currencies"]["FKP"]['name']))             
        self.assertEqual(test_iso3166_2_fk["capital"][0], "Stanley", "Expected capital city to be Stanley, got {}.".format(test_iso3166_2_fk["capital"][0]))               
        self.assertEqual(test_iso3166_2_fk["region"], "Americas", "Expected region to be Americas, got {}.".format(test_iso3166_2_fk["region"]))                
        self.assertEqual(list(test_iso3166_2_fk["languages"].keys()), ["eng"], "Expected language to be English, got {}.".format(list(test_iso3166_2_fk["languages"].keys())))        
        self.assertEqual(test_iso3166_2_fk["area"], 12173, "Expected total area to be 12173, got {}.".format(test_iso3166_2_fk["area"]))       
        self.assertEqual(test_iso3166_2_fk["population"], 2563, "Expected population to be 2563, got {}.".format(test_iso3166_2_fk["population"]))            
        self.assertEqual(test_iso3166_2_fk["cioc"], "NA", "Expected cioc value to be NA, got {}.".format(test_iso3166_2_fk["cioc"]))            
        self.assertEqual(len(test_iso3166_2_fk["subdivisions"]), 0, "Expected 0 total subdivisions, got {}.".format(len(test_iso3166_2_fk["subdivisions"])))
        self.assertEqual(test_iso3166_2_fk["latlng"], [-51.75, -59], "Expected lat/longitude to be [-51.75, -59], got {}.".format(test_iso3166_2_fk["latlng"]))          
        for col in test_iso3166_2_fk.keys():
            self.assertIn(col, self.correct_output_attributes, "Column {} not found in list of correct columns.".format(col))
#3.)
        iso3166_2.export_iso3166_2(alpha2_codes=test_alpha2_gd, output_folder=self.test_output_dir, json_filename=self.test_output_filename, verbose=0) #Grenada

        #open exported jsons
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha2_gd + ".json")) as output_json:
            test_iso3166_2_gd = json.load(output_json)
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha2_gd + "-min.json")) as output_json:
            test_iso3166_2_gd_min = json.load(output_json)

        self.assertIsInstance(test_iso3166_2_gd, dict, "Expected output to be type dict, got {}.".format(type(test_iso3166_2_gd)))
        self.assertEqual(len(test_iso3166_2_gd), 36, "Expected 36 keys/attributes in output dict, got {}.".format(len(test_iso3166_2_gd)))
        self.assertEqual(test_iso3166_2_gd["name"]["common"], "Grenada", "Name expected to be Grenada, got {}.".format(test_iso3166_2_gd["name"]["common"]))      
        self.assertEqual(test_iso3166_2_gd["cca2"], "GD", "Expected alpha-2 code to be GD, got {}.".format(test_iso3166_2_gd["cca2"]))  
        self.assertEqual(test_iso3166_2_gd["cca3"], "GRD", "Expected alpha-3 code to be GRD, got {}.".format(test_iso3166_2_gd["cca3"]))     
        self.assertEqual(test_iso3166_2_gd["currencies"]["XCD"]['name'], "Eastern Caribbean dollar", "Expected currency to be Eastern Caribbean dollar, got {}.".format(test_iso3166_2_gd["currencies"]["XCD"]['name']))        
        self.assertEqual(test_iso3166_2_gd["capital"][0], "St. George's", "Expected capital city to be St. George's, got {}.".format(test_iso3166_2_gd["capital"][0]))        
        self.assertEqual(test_iso3166_2_gd["region"], "Americas", "Expected region to be Americas, got {}.".format(test_iso3166_2_gd["region"]))                       
        self.assertEqual(list(test_iso3166_2_gd["languages"].keys()), ["eng"], "Expected language to be English, got {}.".format(list(test_iso3166_2_gd["languages"].keys())))        
        self.assertEqual(test_iso3166_2_gd["area"], 344, "Expected total area to be 344, got {}.".format(test_iso3166_2_gd["area"]))       
        self.assertEqual(test_iso3166_2_gd["population"], 112519, "Expected population to be 112519, got {}.".format(test_iso3166_2_gd["population"]))            
        self.assertEqual(test_iso3166_2_gd["borders"], "NA", "Expected borders to be NA, got {}.".format(test_iso3166_2_gd["borders"]))            
        self.assertEqual(len(test_iso3166_2_gd["subdivisions"]), 7, "Expected 7 total subdivisions, got {}.".format(len(test_iso3166_2_gd["subdivisions"])))
        self.assertEqual(test_iso3166_2_gd["latlng"], [12.117, -61.667], "Expected lat/longitude to be [12.117, -61.667], got {}.".format(test_iso3166_2_gd["latlng"]))         
        for col in test_iso3166_2_gd.keys(): 
            self.assertIn(col, self.correct_output_attributes, "Column {} not found in list of correct columns.".format(col))

        gd_subdivision_codes = ['GD-01', 'GD-02', 'GD-03', 'GD-04', 'GD-05', 'GD-06', 'GD-10']
        gd_subdivision_names = ['Saint Andrew', 'Saint David', 'Saint George', 'Saint John', 'Saint Mark', 'Saint Patrick', 'Southern Grenadine Islands']

        self.assertIsInstance(test_iso3166_2_gd_min, dict, "Expected output object to be of type dict, got {}.".format(type(test_iso3166_2_gd_min)))
        self.assertEqual(len(test_iso3166_2_gd_min), 7, "Expected 7 total subdivision outputs, got {}.".format(len(test_iso3166_2_gd_min)))
        self.assertEqual(list(test_iso3166_2_gd_min.keys()), gd_subdivision_codes, "Subdivison codes do not equal expected codes:\n{}.".format(list(test_iso3166_2_gd_min.keys())))
        self.assertEqual(list(test_iso3166_2_gd_min['GD-01'].keys()), ['name', 'type', 'parent_code', 'latlng', 'flag_url'], "Expected keys for output dict don't match\n{}".format(list(test_iso3166_2_gd_min['GD-01'].keys())))
        for key in test_iso3166_2_gd_min:
            self.assertIn(test_iso3166_2_gd_min[key]["name"], gd_subdivision_names, "Subdivision name {} not found in list of subdivision names:\n{}.".format(test_iso3166_2_gd_min[key]["name"], gd_subdivision_names))
            if ((test_iso3166_2_gd_min[key]["flag_url"] is not None) or (test_iso3166_2_gd_min[key]["flag_url"] == "")):
                self.assertEqual(requests.get(test_iso3166_2_gd_min[key]["flag_url"], headers=self.user_agent_header).status_code, 200, "Flag URL invalid: {}.".format(test_iso3166_2_gd_min[key]["flag_url"]))
            self.assertIsNone(test_iso3166_2_gd_min[key]['parent_code'], "Parent code key cannot be None.")
            self.assertEqual(len(test_iso3166_2_gd_min[key]["latlng"]), 2, "Expected key should have both latitude and longitude.") 
#4.)
        iso3166_2.export_iso3166_2(alpha2_codes=test_alpha2_kg_ms_nr, output_folder=self.test_output_dir, json_filename=self.test_output_filename, verbose=0) #Kyrgyzstan, Montserrat, Nauru

        #open exported jsons
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha2_kg_ms_nr + ".json")) as output_json:
            test_iso3166_2_kg_ms_nr = json.load(output_json)
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha2_kg_ms_nr + "-min.json")) as output_json:
            test_iso3166_2_kg_ms_nr_min = json.load(output_json)

        self.assertIsInstance(test_iso3166_2_kg_ms_nr, dict, "Expected output to be type dict, got {}.".format(type(test_iso3166_2_kg_ms_nr)))
        self.assertEqual(len(test_iso3166_2_kg_ms_nr["KG"]), 36, "Expected 36 keys/attributes in output dict, got {}.".format(len(test_iso3166_2_kg_ms_nr["KG"])))
        self.assertEqual(len(test_iso3166_2_kg_ms_nr["MS"]), 36, "Expected 36 keys/attributes in output dict, got {}.".format(len(test_iso3166_2_kg_ms_nr["MS"])))
        self.assertEqual(len(test_iso3166_2_kg_ms_nr["NR"]), 36, "Expected 36 keys/attributes in output dict, got {}.".format(len(test_iso3166_2_kg_ms_nr["NR"])))
        self.assertEqual(test_iso3166_2_kg_ms_nr["KG"]["cca2"], "KG", "Expected alpha-2 code to be KG, got {}.".format(test_iso3166_2_kg_ms_nr["KG"]["cca2"]))  
        self.assertEqual(test_iso3166_2_kg_ms_nr["MS"]["cca2"], "MS", "Expected alpha-2 code to be MS, got {}.".format(test_iso3166_2_kg_ms_nr["MS"]["cca2"]))  
        self.assertEqual(test_iso3166_2_kg_ms_nr["NR"]["cca2"], "NR", "Expected alpha-2 code to be NR, got {}.".format(test_iso3166_2_kg_ms_nr["NR"]["cca2"]))  
        self.assertEqual(len(test_iso3166_2_kg_ms_nr["KG"]["subdivisions"]), 9, "")
        self.assertEqual(len(test_iso3166_2_kg_ms_nr["NR"]["subdivisions"]), 14, "")
        for alpha_2 in test_iso3166_2_kg_ms_nr:
            for col in test_iso3166_2_kg_ms_nr[alpha_2].keys(): 
                self.assertIn(col, self.correct_output_attributes, "Column {} not found in list of correct columns.".format(col))

        kg_subdivision_codes = ['KG-B', 'KG-C', 'KG-GB', 'KG-GO', 'KG-J', 'KG-N', 'KG-O', 'KG-T', 'KG-Y']
        nr_subdivision_codes = ['NR-01', 'NR-02', 'NR-03', 'NR-04', 'NR-05', 'NR-06', 'NR-07', 'NR-08', 'NR-09', 'NR-10', 'NR-11', 'NR-12', 'NR-13', 'NR-14']

        self.assertIsInstance(test_iso3166_2_kg_ms_nr_min, dict, "Expected output object to be of type dict, got {}.".format(type(test_iso3166_2_kg_ms_nr_min)))
        self.assertEqual(len(test_iso3166_2_kg_ms_nr_min["KG"]), 9, "Expected 9 total subdivision outputs, got {}.".format(len(test_iso3166_2_kg_ms_nr_min["KG"])))
        self.assertEqual(len(test_iso3166_2_kg_ms_nr_min["MS"]), 0, "Expected 0 total subdivision outputs, got {}.".format(len(test_iso3166_2_kg_ms_nr_min["MS"])))
        self.assertEqual(len(test_iso3166_2_kg_ms_nr_min["NR"]), 14, "Expected 14 total subdivision outputs, got {}.".format(len(test_iso3166_2_kg_ms_nr_min["NR"])))
        self.assertEqual(list(test_iso3166_2_kg_ms_nr_min["KG"].keys()), kg_subdivision_codes, "Subdivison codes do not equal expected codes:\n{}.".format(list(test_iso3166_2_kg_ms_nr_min["KG"].keys())))
        self.assertEqual(list(test_iso3166_2_kg_ms_nr_min["NR"].keys()), nr_subdivision_codes, "Subdivison codes do not equal expected codes:\n{}.".format(list(test_iso3166_2_kg_ms_nr_min["NR"].keys())))
        self.assertEqual(list(test_iso3166_2_kg_ms_nr_min["KG"]['KG-B'].keys()), ['name', 'type', 'parent_code', 'latlng', 'flag_url'], "Expected keys for output dict don't match\n{}".format(list(test_iso3166_2_kg_ms_nr_min["KG"]['KG-B'].keys())))
        self.assertEqual(list(test_iso3166_2_kg_ms_nr_min["NR"]['NR-01'].keys()), ['name', 'type', 'parent_code', 'latlng', 'flag_url'], "Expected keys for output dict don't match\n{}".format(list(test_iso3166_2_kg_ms_nr_min["NR"]['NR-01'].keys())))
        for key in test_iso3166_2_kg_ms_nr_min:
            for subd in test_iso3166_2_kg_ms_nr_min[key]:
                if ((test_iso3166_2_kg_ms_nr_min[key][subd]["flag_url"] is not None) or (test_iso3166_2_kg_ms_nr_min[key][subd]["flag_url"] == "")):
                    self.assertEqual(requests.get(test_iso3166_2_kg_ms_nr_min[key][subd]["flag_url"], headers=self.user_agent_header).status_code, 200, "Flag URL invalid: {}.".format(test_iso3166_2_kg_ms_nr_min[key][subd]["flag_url"]))
                self.assertIsNone(test_iso3166_2_kg_ms_nr_min[key][subd]['parent_code'], "Parent code key cannot be None.")
                self.assertEqual(len(test_iso3166_2_kg_ms_nr_min[key][subd]["latlng"]), 2, "Expected key should have both latitude and longitude.") 
#5.)
        iso3166_2.export_iso3166_2(alpha2_codes=test_alpha2_py_sl_tl, output_folder=self.test_output_dir, json_filename=self.test_output_filename, verbose=0) #Paraguay, Sierra Leone, Timor-Lests

        #open exported jsons
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha2_py_sl_tl + ".json")) as output_json:
            test_iso3166_2_py_sl_tl = json.load(output_json)
        with open(os.path.join(self.test_output_dir, self.test_output_filename + "-" + test_alpha2_py_sl_tl + "-min.json")) as output_json:
            test_iso3166_2_py_sl_tl_min = json.load(output_json)

        self.assertIsInstance(test_iso3166_2_py_sl_tl, dict, "Expected output to be type dict, got {}.".format(type(test_iso3166_2_py_sl_tl)))
        self.assertEqual(len(test_iso3166_2_py_sl_tl["PY"]), 36, "Expected 36 keys/attributes in output dict, got {}.".format(len(test_iso3166_2_py_sl_tl["PY"])))
        self.assertEqual(len(test_iso3166_2_py_sl_tl["SL"]), 36, "Expected 36 keys/attributes in output dict, got {}.".format(len(test_iso3166_2_py_sl_tl["SL"])))
        self.assertEqual(len(test_iso3166_2_py_sl_tl["TL"]), 36, "Expected 36 keys/attributes in output dict, got {}.".format(len(test_iso3166_2_py_sl_tl["TL"])))
        self.assertEqual(test_iso3166_2_py_sl_tl["PY"]["cca2"], "PY", "Expected alpha-2 code to be PY, got {}.".format(test_iso3166_2_py_sl_tl["PY"]["cca2"]))  
        self.assertEqual(test_iso3166_2_py_sl_tl["SL"]["cca2"], "SL", "Expected alpha-2 code to be SL, got {}.".format(test_iso3166_2_py_sl_tl["SL"]["cca2"]))  
        self.assertEqual(test_iso3166_2_py_sl_tl["TL"]["cca2"], "TL", "Expected alpha-2 code to be TL, got {}.".format(test_iso3166_2_py_sl_tl["TL"]["cca2"]))  
        self.assertEqual(len(test_iso3166_2_py_sl_tl["PY"]["subdivisions"]), 18, "")
        self.assertEqual(len(test_iso3166_2_py_sl_tl["SL"]["subdivisions"]), 5, "")
        self.assertEqual(len(test_iso3166_2_py_sl_tl["TL"]["subdivisions"]), 13, "")
        for alpha_2 in test_iso3166_2_py_sl_tl:
            for col in test_iso3166_2_py_sl_tl[alpha_2].keys(): 
                self.assertIn(col, self.correct_output_attributes, "Column {} not found in list of correct columns.".format(col))

        py_subdivision_codes = ['PY-1', 'PY-2', 'PY-3', 'PY-4', 'PY-5', 'PY-6', 'PY-7', 'PY-8', 'PY-9', 'PY-10', 'PY-11', 'PY-12', 'PY-13', 'PY-14', 'PY-15', 'PY-16', 'PY-19', 'PY-ASU']
        sl_subdivision_codes = ['SL-E', 'SL-N', 'SL-NW', 'SL-S', 'SL-W']
        tl_subdivision_codes = ['TL-AL', 'TL-AN', 'TL-BA', 'TL-BO', 'TL-CO', 'TL-DI', 'TL-ER', 'TL-LA', 'TL-LI', 'TL-MF', 'TL-MT', 'TL-OE', 'TL-VI']

        self.assertIsInstance(test_iso3166_2_py_sl_tl_min, dict, "Expected output object to be of type dict, got {}.".format(type(test_iso3166_2_py_sl_tl_min)))
        self.assertEqual(len(test_iso3166_2_py_sl_tl_min["PY"]), 18, "Expected 18 total subdivision outputs, got {}.".format(len(test_iso3166_2_py_sl_tl_min["PY"])))
        self.assertEqual(len(test_iso3166_2_py_sl_tl_min["SL"]), 5, "Expected 5 total subdivision outputs, got {}.".format(len(test_iso3166_2_py_sl_tl_min["SL"])))
        self.assertEqual(len(test_iso3166_2_py_sl_tl_min["TL"]), 13, "Expected 13 total subdivision outputs, got {}.".format(len(test_iso3166_2_py_sl_tl_min["TL"])))
        self.assertEqual(list(test_iso3166_2_py_sl_tl_min["PY"].keys()), py_subdivision_codes, "Subdivison codes do not equal expected codes:\n{}.".format(list(test_iso3166_2_py_sl_tl_min["PY"].keys())))
        self.assertEqual(list(test_iso3166_2_py_sl_tl_min["SL"].keys()), sl_subdivision_codes, "Subdivison codes do not equal expected codes:\n{}.".format(list(test_iso3166_2_py_sl_tl_min["SL"].keys())))
        self.assertEqual(list(test_iso3166_2_py_sl_tl_min["TL"].keys()), tl_subdivision_codes, "Subdivison codes do not equal expected codes:\n{}.".format(list(test_iso3166_2_py_sl_tl_min["TL"].keys())))
        self.assertEqual(list(test_iso3166_2_py_sl_tl_min["PY"]['PY-1'].keys()), ['name', 'type', 'parent_code', 'latlng', 'flag_url'], "Expected keys for output dict don't match\n{}".format(list(test_iso3166_2_py_sl_tl_min["PY"]['PY-1'].keys())))
        self.assertEqual(list(test_iso3166_2_py_sl_tl_min["SL"]['SL-E'].keys()), ['name', 'type', 'parent_code', 'latlng', 'flag_url'], "Expected keys for output dict don't match\n{}".format(list(test_iso3166_2_py_sl_tl_min["SL"]['SL-E'].keys())))
        self.assertEqual(list(test_iso3166_2_py_sl_tl_min["TL"]['TL-AL'].keys()), ['name', 'type', 'parent_code', 'latlng', 'flag_url'], "Expected keys for output dict don't match\n{}".format(list(test_iso3166_2_py_sl_tl_min["TL"]['TL-AL'].keys())))
        for key in test_iso3166_2_py_sl_tl_min:
            for subd in test_iso3166_2_py_sl_tl_min[key]:
                if ((test_iso3166_2_py_sl_tl_min[key][subd]["flag_url"] is not None) or (test_iso3166_2_py_sl_tl_min[key][subd]["flag_url"] == "")):
                    self.assertEqual(requests.get(test_iso3166_2_py_sl_tl_min[key][subd]["flag_url"], headers=self.user_agent_header).status_code, 200, "Flag URL invalid: {}.".format(test_iso3166_2_py_sl_tl_min[key][subd]["flag_url"]))
                self.assertIsNone(test_iso3166_2_py_sl_tl_min[key][subd]['parent_code'], "Parent code key cannot be None.")
                self.assertEqual(len(test_iso3166_2_py_sl_tl_min[key][subd]["latlng"]), 2, "Expected key should have both latitude and longitude.") 
#6.)
        for attribute in iso3166_2.attribute_list:
            self.assertIn(attribute, self.correct_output_attributes, "Attriubte {} not found in list of correct attributes.".format(attribute))
#7.)
        for alpha_2 in test_alpha2_bv_fo_gs_hk:
            iso3166_2.export_iso3166_2(alpha2_codes=alpha_2, output_folder=self.test_output_dir, json_filename=self.test_output_filename, verbose=0)
            with (self.assertRaises(FileNotFoundError)):
                with open(os.path.join(self.test_output_dir, self.test_output_filename + "-" + alpha_2 + "-min.json")) as output_json:
                    json.load(output_json)
#8.)
        with (self.assertRaises(ValueError)):
            iso3166_2.export_iso3166_2(alpha2_codes=test_alpha2_error1, output_folder=self.test_output_dir, json_filename=self.test_output_filename, verbose=0) #ZZ
            iso3166_2.export_iso3166_2(alpha2_codes=test_alpha2_error2, output_folder=self.test_output_dir, json_filename=self.test_output_filename, verbose=0) #ABCDEF
            iso3166_2.export_iso3166_2(alpha2_codes=test_alpha2_error3, output_folder=self.test_output_dir, json_filename=self.test_output_filename, verbose=0) #1234

    def tearDown(self):
        """ Delete any exported json folder. """
        shutil.rmtree(self.test_output_dir)

if __name__ == '__main__':
    #run all unit tests
    unittest.main(verbosity=2)    