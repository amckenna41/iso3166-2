import iso3166_2 as iso
import iso3166
import requests
import getpass
import json
import os
import shutil
from importlib.metadata import metadata
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

# @unittest.skip("")
class ISO3166_2_Tests(unittest.TestCase):
    """
    Test suite for testing the iso3166-2 Python software package. 

    Test Cases
    ==========
    test_iso3166_2_metadata:
        testing correct software metdata for the iso3166-2 package. 
    test_iso3166_2:
        testing correct data returned from the "subdivisions" object in the ISO3166_2 class of the 
        iso3166-2 package.  
    test_iso3166_2_json:
        testing correct objects are returned from the ISO 3166-2 JSON, using a variety of inputs.
    test_subdivision_names:
        testing correct ISO 3166-2 subdivision names are returned from the subdivision_names() class function.
    test_subdivision_local_names:
        testing correct ISO 3166-2 subdivision local names are returned from the subdivision_local_names() class function.
    test_subdivision_codes:
        testing correct ISO 3166-2 subdivision codes are returned from the subdivision_codes() class function.  
    test_subdivision_parent_codes:
        testing correct ISO 3166-2 subdivision parent codes are returned from the subdivision_parent_codes() class function.  
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

        #create test output directory - remove if already present
        self.test_output_dir = "test_output"
        if (os.path.isdir(self.test_output_dir)):
            shutil.rmtree(self.test_output_dir)
        os.mkdir(self.test_output_dir)

    def test_iso3166_2_metadata(self): 
        """ Testing correct iso3166-2 software version and metadata. """
        # self.assertEqual(metadata('iso3166-2')['version'], "1.4.0", 
        #     "iso3166-2 version is not correct, expected 1.4.0, got {}.".format(metadata('iso3166-2')['version']))
        self.assertEqual(metadata('iso3166-2')['name'], "iso3166-2", 
            "iso3166-2 software name is not correct, expected iso3166-2, got {}.".format(metadata('iso3166-2')['name']))
        self.assertEqual(metadata('iso3166-2')['author'], "AJ McKenna, https://github.com/amckenna41", 
            "iso3166-2 author is not correct, expected AJ McKenna, got {}.".format(metadata('iso3166-2')['author']))
        self.assertEqual(metadata('iso3166-2')['author-email'], "amckenna41@qub.ac.uk", 
            "iso3166-2 author email is not correct, expected amckenna41@qub.ac.uk, got {}.".format(metadata('iso3166-2')['author-email']))
        # self.assertEqual(metadata('iso3166-2')['summary'], "A lightweight Python package, and accompanying API, that can be used to access all of the world's most up-to-date and accurate ISO 3166-2 subdivision data, including: name, local name, code, parent code, type, latitude/longitude and flag.", 
        #     "iso3166-2 package summary is not correct, got: {}.".format(metadata('iso3166-2')['summary']))
        self.assertEqual(metadata('iso3166-2')['keywords'], "iso,iso3166,beautifulsoup,python,pypi,countries,country codes,iso3166-2,iso3166-1,alpha-2,iso3166-updates,subdivisions",
            "iso3166-2 keywords are not correct, got:\n{}.".format(metadata('iso3166-2')['keywords']))
        self.assertEqual(metadata('iso3166-2')['home-page'], "https://github.com/amckenna41/iso3166-2", 
            "iso3166-2 home page url is not correct, expected https://github.com/amckenna41/iso3166-2, got {}.".format(metadata('iso3166-2')['home-page']))
        self.assertEqual(metadata('iso3166-2')['maintainer'], "AJ McKenna", 
            "iso3166-2 maintainer is not correct, expected AJ McKenna, got {}.".format(metadata('iso3166-2')['maintainer']))
        self.assertEqual(metadata('iso3166-2')['license'], "MIT", 
            "iso3166-2 license type is not correct, expected MIT, got {}.".format(metadata('iso3166-2')['license']))

    def test_iso3166_2(self):
        """ Test ISO 3166-2 class and its methods and attributes. """
        #testing class using iso3166-2.json file as input
        self.assertIsInstance(iso.country.alpha_2, list, 
            "Expected alpha-2 attribute to be a list, got {}.".format(type(iso.country.alpha_2)))
        self.assertEqual(len(iso.country.alpha_2), 250, 
            "Expected 250 alpha-2 codes, got {}.".format(len(iso.country.alpha_2)))
        self.assertIsInstance(iso.country.all, dict,
            "Expected ISO 3166-2 data object to be a dict, got {}.".format(type(iso.country.all)))
        self.assertEqual(len(iso.country.all), 250, 
            "Expected 250 countrys in ISO 3166-2 data object, got {}.".format(len(iso.country.all)))       
        self.assertIsInstance(iso.country.attributes, list, 
            "Expected attributes class variable to be a list, got {}.".format(type(iso.country.attributes)))
        self.assertEqual(set(iso.country.attributes), set(self.correct_output_attributes), 
            "List of attributes in class do not match expected, got:\n{}.".format(iso.country.attributes))
        for code in iso.country.all:
            self.assertIn(code, iso.country.alpha_2,
                "Alpha-2 code {} not found in list of available 2 letter codes.".format(code))

    def test_iso3166_2_json(self):
        """ Testing ISO 3166-2 JSON contents and data. """ 
        test_alpha2_ba = iso.country["BA"] #Bosnia and Herzegovina
        test_alpha2_cy = iso.country["CY"] #Cyprus
        test_alpha2_ga = iso.country["GA"] #Gabon
        test_alpha2_rw_vu = iso.country["RW, VU"] #Rwanda, Vanuatu
        test_alpha2_gg_kw_vc = iso.country["GG, KW, VC"] #Guernsey, Kuwait, St Vincent & the Grenadines
#1.)    
        ba_subdivision_codes = ['BA-BIH', 'BA-BRC', 'BA-SRP']
        ba_subdivision_names = ['Federacija Bosne i Hercegovine', 'Brčko distrikt', 'Republika Srpska']

        self.assertIsInstance(test_alpha2_ba, dict, "Expected output object to be of type dict, got {}.".format(type(test_alpha2_ba)))
        self.assertEqual(len(test_alpha2_ba), 3, "Expected 3 total subdivision outputs, got {}.".format(len(test_alpha2_ba)))
        self.assertEqual(list(test_alpha2_ba.keys()), ba_subdivision_codes, "Subdivison codes do not equal expected codes:\n{}.".format(list(test_alpha2_ba.keys())))
        self.assertEqual(list(test_alpha2_ba['BA-BIH'].keys()), ['name', 'localName', 'type', 'parentCode', 'flagUrl', 'latLng'], "Expected keys for output dict don't match\n{}.".format(list(test_alpha2_ba['BA-BIH'].keys())))
        for key in test_alpha2_ba:
            self.assertIn(test_alpha2_ba[key].name, ba_subdivision_names, "Subdivision name {} not found in list of subdivision names:\n{}.".format(test_alpha2_ba[key].name, ba_subdivision_names))
            if (not (test_alpha2_ba[key].flagUrl is None) and (test_alpha2_ba[key].flagUrl != "")):
                self.assertEqual(requests.get(test_alpha2_ba[key].flagUrl, headers=self.user_agent_header).status_code, 200, "Flag URL invalid: {}.".format(test_alpha2_ba[key].flagUrl))
            if not (test_alpha2_ba[key]["parentCode"] is None):
                self.assertIn(test_alpha2_ba[key]["parentCode"], list(test_alpha2_ba[key].keys()), 
                    "Parent code {} not found in list of subdivision codes:\n.".format(test_alpha2_ba[key]["parentCode"], list(test_alpha2_ba[key].keys())))    
            self.assertEqual(len(test_alpha2_ba[key].latLng), 2, "Expected key should have both lat/longitude.")        
#2.)
        cy_subdivision_codes = ['CY-01', 'CY-02', 'CY-03', 'CY-04', 'CY-05', 'CY-06']
        cy_subdivision_names = ['Lefkosia', 'Lemesos', 'Larnaka', 'Ammochostos', 'Baf', 'Girne']
        
        self.assertIsInstance(test_alpha2_cy, dict,  "Expected output object to be of type dict, got {}.".format(type(test_alpha2_cy)))
        self.assertEqual(len(test_alpha2_cy), 6, "Expected 6 total subdivision outputs, got {}.".format(len(test_alpha2_cy)))
        self.assertEqual(list(test_alpha2_cy.keys()), cy_subdivision_codes, "Subdivison codes do not equal expected codes:\n{}.".format(list(test_alpha2_cy.keys())))
        self.assertEqual(list(test_alpha2_cy['CY-01'].keys()), ['name', 'localName', 'type', 'parentCode', 'flagUrl', 'latLng'], "Expected keys for output dict don't match\n{}.".format(list(test_alpha2_cy['CY-01'].keys())))
        for key in test_alpha2_cy:
            self.assertIn(test_alpha2_cy[key].name, cy_subdivision_names, "Subdivision name {} not found in list of subdivision names:\n{}.".format(test_alpha2_cy[key].name, cy_subdivision_names))
            if (not (test_alpha2_cy[key].flagUrl is None) and (test_alpha2_cy[key].flagUrl != "")):
                self.assertEqual(requests.get(test_alpha2_cy[key].flagUrl, headers=self.user_agent_header).status_code, 200, "Flag URL invalid: {}.".format(test_alpha2_cy[key].flagUrl))
            if not (test_alpha2_cy[key]["parentCode"] is None):
                self.assertIn(test_alpha2_cy[key]["parentCode"], list(test_alpha2_cy[key].keys()), 
                    "Parent code {} not found in list of subdivision codes:\n.".format(test_alpha2_cy[key]["parentCode"], list(test_alpha2_cy[key].keys())))    
            self.assertEqual(len(test_alpha2_cy[key].latLng), 2, "Expected key should have both lat/longitude.")              
#3.)
        ga_subdivision_codes = ['GA-1', 'GA-2', 'GA-3', 'GA-4', 'GA-5', 'GA-6', 'GA-7', 'GA-8', 'GA-9'] 
        ga_subdivision_names = ['Estuaire', 'Haut-Ogooué', 'Moyen-Ogooué', 'Ngounié', 'Nyanga', 'Ogooué-Ivindo', 
            'Ogooué-Lolo', 'Ogooué-Maritime', 'Woleu-Ntem']
        
        self.assertIsInstance(test_alpha2_ga, dict,  "Expected output object to be of type dict, got {}.".format(type(test_alpha2_ga)))
        self.assertEqual(len(test_alpha2_ga), 9, "Expected 9 total subdivision outputs, got {}.".format(len(test_alpha2_ga)))
        self.assertEqual(list(test_alpha2_ga.keys()), ga_subdivision_codes, "Subdivison codes do not equal expected codes:\n{}.".format(list(test_alpha2_ga.keys())))
        self.assertEqual(list(test_alpha2_ga['GA-1'].keys()), ['name', 'localName', 'type', 'parentCode', 'flagUrl', 'latLng'], "Expected keys for output dict don't match\n{}.".format(list(test_alpha2_ga['GA-1'].keys())))
        for key in test_alpha2_ga:
            self.assertIn(test_alpha2_ga[key].name, ga_subdivision_names, "Subdivision name {} not found in list of subdivision names:\n{}.".format(test_alpha2_ga[key].name, ga_subdivision_names))
            if (not (test_alpha2_ga[key].flagUrl is None) and (test_alpha2_ga[key].flagUrl != "")):
                self.assertEqual(requests.get(test_alpha2_ga[key].flagUrl, headers=self.user_agent_header).status_code, 200, "Flag URL invalid: {}.".format(test_alpha2_ga[key].flagUrl))
            if not (test_alpha2_ga[key]["parentCode"] is None):
                self.assertIn(test_alpha2_ga[key]["parentCode"], list(test_alpha2_ga[key].keys()), 
                    "Parent code {} not found in list of subdivision codes:\n.".format(test_alpha2_ga[key]["parentCode"], list(test_alpha2_ga[key].keys())))    
            self.assertEqual(len(test_alpha2_ga[key].latLng), 2, "Expected key should have both lat/longitude.")        
#4.)
        rw_subdivision_codes = ['RW-01', 'RW-02', 'RW-03', 'RW-04', 'RW-05']
        vu_subdivision_codes = ['VU-MAP', 'VU-PAM', 'VU-SAM', 'VU-SEE', 'VU-TAE', 'VU-TOB']
        rw_subdivision_names = ['City of Kigali', 'Eastern', 'Northern', 'Western', 'Southern']
        vu_subdivision_names = ['Malampa', 'Pénama', 'Sanma', 'Shéfa', 'Taféa', 'Torba']

        self.assertIsInstance(test_alpha2_rw_vu, dict,  "Expected output object to be of type dict, got {}.".format(type(test_alpha2_rw_vu)))
        self.assertEqual(list(test_alpha2_rw_vu.keys()), ['RW', 'VU'], "Expected output keys to be RW and VU, got {}.".format(list(test_alpha2_rw_vu.keys())))
        self.assertEqual(len(test_alpha2_rw_vu["RW"]), 5, "Expected 5 total subdivision outputs, got {}.".format(len(test_alpha2_rw_vu["RW"])))
        self.assertEqual(len(test_alpha2_rw_vu["VU"]), 6, "Expected 6 total subdivision outputs, got {}.".format(len(test_alpha2_rw_vu["VU"])))
        self.assertEqual(list(test_alpha2_rw_vu["RW"].keys()), rw_subdivision_codes, "Subdivison codes do not equal expected codes:\n{}.".format(list(test_alpha2_rw_vu["RW"].keys())))
        self.assertEqual(list(test_alpha2_rw_vu["VU"].keys()), vu_subdivision_codes, "Subdivison codes do not equal expected codes:\n{}.".format(list(test_alpha2_rw_vu["VU"].keys())))
        self.assertEqual(list(test_alpha2_rw_vu["RW"]['RW-01'].keys()), ['name', 'localName', 'type', 'parentCode', 'flagUrl', 'latLng'], "Expected keys for output dict don't match\n{}.".format(list(test_alpha2_rw_vu["RW"]['RW-01'].keys())))
        self.assertEqual(list(test_alpha2_rw_vu["VU"]['VU-MAP'].keys()), ['name', 'localName', 'type', 'parentCode', 'flagUrl', 'latLng'], "Expected keys for output dict don't match\n{}.".format(list(test_alpha2_rw_vu["VU"]['VU-MAP'].keys())))
        for key in test_alpha2_rw_vu["RW"]:
            self.assertIn(test_alpha2_rw_vu["RW"][key].name, rw_subdivision_names, "Subdivision name {} not found in list of subdivision names:\n{}.".format(test_alpha2_rw_vu["RW"][key].name, rw_subdivision_names))
            if (not (test_alpha2_rw_vu["RW"].flagUrl is None) and (test_alpha2_rw_vu["RW"].flagUrl != "")):
                self.assertEqual(requests.get(test_alpha2_rw_vu["RW"][key].flagUrl, headers=self.user_agent_header).status_code, 200, "Flag URL invalid: {}.".format(test_alpha2_rw_vu["RW"][key].flagUrl))
            self.assertEqual(len(test_alpha2_rw_vu["RW"][key].latLng), 2, "Expected key should have both lat/longitude.")        
        for key in test_alpha2_rw_vu["VU"]:
            self.assertIn(test_alpha2_rw_vu["VU"][key].name, vu_subdivision_names, "Subdivision name {} not found in list of subdivision names:\n{}.".format(test_alpha2_rw_vu["VU"][key].name, vu_subdivision_names))
            if (not (test_alpha2_rw_vu["VU"].flagUrl is None) and (test_alpha2_rw_vu["VU"].flagUrl != "")):
                self.assertEqual(requests.get(test_alpha2_rw_vu["VU"][key].flagUrl, headers=self.user_agent_header).status_code, 200, "Flag URL invalid: {}.".format(test_alpha2_rw_vu["VU"][key].flagUrl))
            self.assertEqual(len(test_alpha2_rw_vu["VU"][key].latLng), 2, "Expected key should have both lat/longitude.")              
#5.)
        kw_subdivision_codes = ['KW-AH', 'KW-FA', 'KW-HA', 'KW-JA', 'KW-KU', 'KW-MU']
        kw_subdivision_names = ['Al Aḩmadī', 'Al Farwānīyah', 'Ḩawallī', "Al Jahrā’", "Al ‘Āşimah", 'Mubārak al Kabīr']
        vc_subdivision_codes = ['VC-01', 'VC-02', 'VC-03', 'VC-04', 'VC-05', 'VC-06']
        vc_subdivision_names = ['Charlotte', 'Saint Andrew', 'Saint David', 'Saint George', 'Saint Patrick', 'Grenadines']
        
        self.assertIsInstance(test_alpha2_gg_kw_vc, dict, "Expected output object to be of type dict, got {}.".format(type(test_alpha2_gg_kw_vc)))
        self.assertEqual(list(test_alpha2_gg_kw_vc.keys()), ['GG', 'KW', 'VC'], "Expected output keys to be GG, KW and VC, got {}.".format(list(test_alpha2_gg_kw_vc.keys())))
        self.assertEqual(len(test_alpha2_gg_kw_vc["GG"]), 0, "Expected 0 total subdivision outputs, got {}.".format(len(test_alpha2_gg_kw_vc["GG"])))
        self.assertEqual(len(test_alpha2_gg_kw_vc["KW"]), 6, "Expected 6 total subdivision outputs, got {}.".format(len(test_alpha2_gg_kw_vc["KW"])))
        self.assertEqual(len(test_alpha2_gg_kw_vc["VC"]), 6, "Expected 6 total subdivision outputs, got {}.".format(len(test_alpha2_gg_kw_vc["VC"])))
        self.assertEqual(list(test_alpha2_gg_kw_vc["GG"].keys()), [], "Expected no subdivision codes, got {}.".format(list(test_alpha2_gg_kw_vc["GG"].keys())))
        self.assertEqual(list(test_alpha2_gg_kw_vc["KW"].keys()), kw_subdivision_codes, "Subdivison codes do not equal expected codes:\n{}.".format(list(test_alpha2_gg_kw_vc["KW"].keys())))
        self.assertEqual(list(test_alpha2_gg_kw_vc["VC"].keys()), vc_subdivision_codes, "Subdivison codes do not equal expected codes:\n{}.".format(list(test_alpha2_gg_kw_vc["VC"].keys())))
        self.assertEqual(list(test_alpha2_gg_kw_vc["KW"]['KW-AH'].keys()), ['name', 'localName', 'type', 'parentCode', 'flagUrl', 'latLng'], 
            "Expected keys do not match output:\n{}.".format(list(test_alpha2_gg_kw_vc["KW"]['KW-AH'].keys())))
        self.assertEqual(list(test_alpha2_gg_kw_vc["VC"]['VC-01'].keys()), ['name', 'localName', 'type', 'parentCode', 'flagUrl', 'latLng'],
            "Expected keys do not match output:\n{}.".format(list(test_alpha2_gg_kw_vc["VC"]['VC-01'].keys())))
        for key in test_alpha2_gg_kw_vc["KW"]:
            self.assertIn(test_alpha2_gg_kw_vc["KW"][key].name, kw_subdivision_names, "Subdivision name {} not found in list of subdivision names:\n{}.".format(test_alpha2_gg_kw_vc["KW"][key].name, kw_subdivision_names))
            if (not (test_alpha2_gg_kw_vc["KW"].flagUrl is None) and (test_alpha2_gg_kw_vc["KW"].flagUrl != "")):
                self.assertEqual(requests.get(test_alpha2_gg_kw_vc["KW"][key].flagUrl, headers=self.user_agent_header).status_code, 200, "Flag URL invalid: {}.".format(test_alpha2_gg_kw_vc["KW"][key].flagUrl))
            self.assertEqual(len(test_alpha2_gg_kw_vc["KW"][key].latLng), 2, "Expected key should have both lat/longitude.")        
        for key in test_alpha2_gg_kw_vc["VC"]:
            self.assertIn(test_alpha2_gg_kw_vc["VC"][key].name, vc_subdivision_names, "Subdivision name {} not found in list of subdivision names:\n{}.".format(test_alpha2_gg_kw_vc["VC"][key].name, vc_subdivision_names))
            if (not (test_alpha2_gg_kw_vc["VC"].flagUrl is None) and (test_alpha2_gg_kw_vc["VC"].flagUrl != "")):
                self.assertEqual(requests.get(test_alpha2_gg_kw_vc["VC"][key].flagUrl, headers=self.user_agent_header).status_code, 200, "Flag URL invalid: {}.".format(test_alpha2_gg_kw_vc["VC"][key].flagUrl))
            self.assertEqual(len(test_alpha2_gg_kw_vc["VC"][key].latLng), 2, "Expected key should have both lat/longitude.")        
#6.)
        for country in iso.country.all:              #testing that all subdivisions have a subdivision name
            for subd in iso.country.all[country]:
                self.assertTrue((iso.country.all[country][subd]["name"] != "" and iso.country.all[country][subd]["name"] != []), "")
#7.)
        for country in iso.country.all:              #testing that all subdivisions have a subdivision local name
            for subd in iso.country.all[country]:
                self.assertTrue((iso.country.all[country][subd]["localName"] != "" and iso.country.all[country][subd]["localName"] != []), "")
#8.)
        for country in iso.country.all:              #testing that all subdivisions have a subdivision type
            for subd in iso.country.all[country]:
                self.assertTrue((iso.country.all[country][subd]["type"] != "" and iso.country.all[country][subd]["type"] != []), "")
#9.)
        for country in iso.country.all:              #testing that all subdivisions have a latitude/longitude
            for subd in iso.country.all[country]:
                self.assertTrue((iso.country.all[country][subd]["latLng"] != "" and iso.country.all[country][subd]["latLng"] != []), "")
#10.)
        with (self.assertRaises(ValueError)):
            iso.country["ZZ"]
            iso.country["XY"]
            iso.country["XYZ"]
            iso.country["AB, CD, EF"]
#11.)
        with (self.assertRaises(TypeError)):
            iso.country[123]
            iso.country[0.5]
            iso.country[False]

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
        km_subdivision_names = iso.country.subdivision_names("KM") #Comoros
        self.assertEqual(km_subdivision_names, expected_km_subdivision_names, "Expected subdivison names don't match output:\n{}.".format(expected_km_subdivision_names))
#2.)
        er_subdivision_names = iso.country.subdivision_names("ER") #Eritrea
        self.assertEqual(er_subdivision_names, expected_er_subdivision_names, "Expected subdivison names don't match output:\n{}.".format(expected_er_subdivision_names))
#3.)
        gl_subdivision_names = iso.country.subdivision_names("GL") #Greenland
        self.assertEqual(gl_subdivision_names, expected_gl_subdivision_names, "Expected subdivison names don't match output:\n{}.".format(expected_gl_subdivision_names))
#4.)
        ls_subdivision_names = iso.country.subdivision_names("LS") #Lesotho
        self.assertEqual(ls_subdivision_names, expected_ls_subdivision_names, "Expected subdivison names don't match output:\n{}.".format(expected_ls_subdivision_names))
#5.)
        zm_subdivision_names = iso.country.subdivision_names("ZM") #Zambia
        self.assertEqual(zm_subdivision_names, expected_zm_subdivision_names, "Expected subdivison names don't match output:\n{}.".format(expected_zm_subdivision_names))
#6.)
        ag_bn_subdivision_names = iso.country.subdivision_names("AG, BN") #Antigua and Barbuda, Brunei
        self.assertEqual(ag_bn_subdivision_names, expected_ag_bn_subdivision_names, "Expected subdivison names don't match output:\n{}.".format(expected_ag_bn_subdivision_names))
#7.)
        dj_va_subdivision_names = iso.country.subdivision_names("DJI, VAT") #Djibouti, Vatican City
        self.assertEqual(dj_va_subdivision_names, expected_dj_va_subdivision_names, "Expected subdivison names don't match output:\n{}.".format(expected_dj_va_subdivision_names))
#8.)
        all_subdivision_names = iso.country.subdivision_names() 
        self.assertEqual(len(all_subdivision_names), 250, "Expected 250 total subdivisions, got {}.".format(len(all_subdivision_names)))
        for key, val in all_subdivision_names.items():
            self.assertIn(key, list(iso3166.countries_by_alpha2.keys()), "Subdivision code {} not found in list of ISO 3166 alpha-2 codes.".format(key))
            self.assertIsInstance(val, list, "Expected output of subdivision names to be of type list, got {}.".format(type(val)))
#9.)
        with (self.assertRaises(ValueError)):
            iso.country.subdivision_names("ABCD")
            iso.country.subdivision_names("Z")
            iso.country.subdivision_names("1234")
            iso.country.subdivision_names("blah, blah, blah")
            iso.country.subdivision_names(False)

    def test_subdivision_local_names(self):
        """ Testing functionality for getting list of all ISO 3166-2 subdivision local names. """
        expected_bb_local_names = ['Christ Church', 'Saint Andrew', 'Saint George', 'Saint James', 'Saint John', 'Saint Joseph', 'Saint Lucy', \
                                   'Saint Michael', 'Saint Peter', 'Saint Philip', 'Saint Thomas']
        expected_lr_local_names = ['Bomi', 'Bong', 'Gbarpolu', 'Grand Bassa', 'Grand Cape Mount', 'Grand Gedeh', 'Grand Kru', 'Lofa', 'Margibi', \
                                   'Maryland', 'Montserrado', 'Nimba', 'River Cess', 'River Gee', 'Sinoe']
        expected_na_local_names = ['//Karas', 'Erongo', 'Hardap', 'Kavango East', 'Kavango West', 'Khomas', 'Kunene', 'Ohangwena', 'Omaheke', 'Omusati', 'Oshana', 'Oshikoto', 'Otjozondjupa', 'Zambezi']
        expected_nr_local_names = ['Aiwo', 'Anabar', 'Anetan', 'Anibare', 'Baitsi', 'Boe', 'Buada', 'Denigomodu', 'Ewa', 'Ijuw', 'Meneng', 'Nibok', 'Uaboe', 'Yaren']
        expected_pr_sc_local_names = {'PR': [], 'SC': ['Anse Boileau', 'Anse Etoile', 'Anse Royale', 'Anse aux Pins', 'Au Cap', 'Baie Lazare', 'Baie Sainte Anne', 'Beau Vallon', 'Bel Air', 'Bel Ombre',\
                                                       'Cascade', 'English River', 'Glacis', 'Grand Anse Mahe', 'Grand Anse Praslin', 'Ile Perseverance I', 'Ile Perseverance II', 'La Digue', 'Les Mamelles',\
                                                        'Mont Buxton', 'Mont Fleuri', 'Plaisance', 'Pointe Larue', 'Port Glaud', 'Roche Caiman', 'Saint Louis', 'Takamaka']}
#1.)
        bb_subdivision_local_names = iso.country.subdivision_local_names("BB") #Barbados
        self.assertEqual(bb_subdivision_local_names, expected_bb_local_names, "Expected subdivison local names don't match output:\n{}.".format(expected_bb_local_names))
#2.)
        lr_subdivision_local_names = iso.country.subdivision_local_names("LR") #Liberia
        self.assertEqual(lr_subdivision_local_names, expected_lr_local_names, "Expected subdivison local names don't match output:\n{}.".format(expected_lr_local_names))
#3.)
        na_subdivision_local_names = iso.country.subdivision_local_names("NA") #Namibia
        self.assertEqual(na_subdivision_local_names, expected_na_local_names, "Expected subdivison local names don't match output:\n{}.".format(expected_na_local_names))
#4.)
        nr_subdivision_local_names = iso.country.subdivision_local_names("NR") #Nauru
        self.assertEqual(nr_subdivision_local_names, expected_nr_local_names, "Expected subdivison local names don't match output:\n{}.".format(expected_nr_local_names))
#5.)
        pr_sc_subdivision_local_names = iso.country.subdivision_local_names("PR,SC") #Puerto Rico, Seychelles
        self.assertEqual(pr_sc_subdivision_local_names, expected_pr_sc_local_names, "Expected subdivison local names don't match output:\n{}.".format(expected_pr_sc_local_names))
#6.)
        all_subdivision_local_names = iso.country.subdivision_names() 
        self.assertEqual(len(all_subdivision_local_names), 250, "Expected 250 total subdivisions, got {}.".format(len(all_subdivision_local_names)))
        for key, val in all_subdivision_local_names.items():
            self.assertIn(key, list(iso3166.countries_by_alpha2.keys()), "Subdivision code {} not found in list of ISO 3166 alpha-2 codes.".format(key))
            self.assertIsInstance(val, list, "Expected output of subdivision local names to be of type list, got {}.".format(type(val)))
#7.)
        with (self.assertRaises(ValueError)):
            iso.country.subdivision_local_names("ABCD")
            iso.country.subdivision_local_names("Z")
            iso.country.subdivision_local_names("1234")
            iso.country.subdivision_local_names("blah, blah, blah")
            iso.country.subdivision_local_names(False)

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
        bq_subdivision_codes = iso.country.subdivision_codes("BQ") #Bonaire, Sint Eustatius and Saba
        self.assertEqual(bq_subdivision_codes, expected_bq_subdivision_codes, "Expected subdivison codes don't match output:\n{}.".format(expected_bq_subdivision_codes))
#2.)
        sz_subdivision_codes = iso.country.subdivision_codes("SZ") #Eswatini
        self.assertEqual(sz_subdivision_codes, expected_sz_subdivision_codes, "Expected subdivison codes don't match output:\n{}.".format(expected_sz_subdivision_codes))
#3.)
        sm_subdivision_codes = iso.country.subdivision_codes("SM") #San Marino
        self.assertEqual(sm_subdivision_codes, expected_sm_subdivision_codes, "Expected subdivison codes don't match output:\n{}.".format(expected_sm_subdivision_codes))
#4.)
        pw_subdivision_codes = iso.country.subdivision_codes("PW") #Palau
        self.assertEqual(pw_subdivision_codes, expected_pw_subdivision_codes, "Expected subdivison codes don't match output:\n{}.".format(expected_pw_subdivision_codes))
#5.)   
        wf_subdivision_codes = iso.country.subdivision_codes("WF") #Wallis and Futuna 
        self.assertEqual(wf_subdivision_codes, expected_wf_subdivision_codes, "Expected subdivison codes don't match output:\n{}.".format(expected_wf_subdivision_codes))
#6.)   
        mg_sb_subdivision_codes = iso.country.subdivision_codes("MG, SB") #Madagascar, Solomon Islands
        self.assertEqual(mg_sb_subdivision_codes, expected_mg_sb_subdivision_codes, "Expected subdivison codes don't match output:\n{}.".format(expected_mg_sb_subdivision_codes))   
#7.)   
        gnq_tca_subdivision_codes = iso.country.subdivision_codes("GNQ, TCA") #Equitorial Guinea, Turks and Caicos Islands
        self.assertEqual(gnq_tca_subdivision_codes, expected_gnq_tca_subdivision_codes, "Expected subdivison codes don't match output:\n{}.".format(expected_gnq_tca_subdivision_codes))  
#8.)
        all_subdivision_codes = iso.country.subdivision_codes() 
        self.assertEqual(len(all_subdivision_codes), 250, "Expected 250 total subdivisions, got {}.".format(len(all_subdivision_codes)))
        for key, val in all_subdivision_codes.items():
            self.assertIn(key, list(iso3166.countries_by_alpha2.keys()), "Subdivision code {} not found in list of ISO 3166 alpha-2 codes.".format(key))
            self.assertIsInstance(val, list, "Expected output of subdivision parent codes to be of type list, got {}.".format(type(val)))
#9.)
        with (self.assertRaises(ValueError)):
            iso.country.subdivision_codes("ABCD")
            iso.country.subdivision_codes("Z")
            iso.country.subdivision_codes("1234")
            iso.country.subdivision_codes(False)
    
    def test_subdivision_parent_codes(self):
        """ Testing functionality for getting list of all ISO 3166-2 subdivision parent codes. """
        expected_lt_parent_codes = ["LT-AL", "LT-KL", "LT-KU", "LT-MR", "LT-PN", "LT-SA", "LT-TA", "LT-TE", "LT-UT", "LT-VL"]
        expected_mw_parent_codes = ["MW-C", "MW-N", "MW-S"]
        expected_rs_parent_codes = ["RS-KM", "RS-VO"]
        expected_ug_parent_codes = ["UG-C", "UG-E", "UG-N", "UG-W"]
        expected_za_parent_codes = []
#1.)
        lt_parentCodes = iso.country.subdivision_parent_codes("LT")
        for code in lt_parentCodes:
            self.assertIn(code, list(iso.country["LT"].keys()), "Parent code not found in list of country's subdivision codes:\n{}.".format(list(iso.country["LT"].keys())))
        self.assertEqual(lt_parentCodes, expected_lt_parent_codes, "Expected subdivison parent codes don't match output:\n{}.".format(expected_lt_parent_codes))
#2.)
        mw_parentCodes = iso.country.subdivision_parent_codes("MW")
        for code in mw_parentCodes:
            self.assertIn(code, list(iso.country["MW"].keys()), "Parent code not found in list of country's subdivision codes:\n{}.".format(list(iso.country["MW"].keys())))
        self.assertEqual(mw_parentCodes, expected_mw_parent_codes, "Expected subdivison parent codes don't match output:\n{}.".format(expected_mw_parent_codes))
#3.)
        rs_parentCodes = iso.country.subdivision_parent_codes("RS")
        for code in rs_parentCodes:
            self.assertIn(code, list(iso.country["RS"].keys()), "Parent code not found in list of country's subdivision codes:\n{}.".format(list(iso.country["RS"].keys())))
        self.assertEqual(rs_parentCodes, expected_rs_parent_codes, "Expected subdivison parent codes don't match output:\n{}.".format(expected_rs_parent_codes))
#4.)
        ug_parentCodes = iso.country.subdivision_parent_codes("UG")
        for code in ug_parentCodes:
            self.assertIn(code, list(iso.country["UG"].keys()), "Parent code not found in list of country's subdivision codes:\n{}.".format(list(iso.country["UG"].keys())))
        self.assertEqual(ug_parentCodes, expected_ug_parent_codes, "Expected subdivison parent codes don't match output:\n{}.".format(expected_ug_parent_codes))
#5.)
        za_parentCodes = iso.country.subdivision_parent_codes("ZA")
        for code in za_parentCodes:
            self.assertIn(code, list(iso.country["ZA"].keys()), "Parent code not found in list of country's subdivision codes:\n{}.".format(list(iso.country["ZA"].keys())))
        self.assertEqual(za_parentCodes, expected_za_parent_codes, "Expected subdivison parent codes don't match output:\n{}.".format(expected_za_parent_codes))
#6.)
        all_subdivision_parent_codes = iso.country.subdivision_parent_codes() 
        self.assertEqual(len(all_subdivision_parent_codes), 250, "Expected 250 total subdivision parent codes, got {}.".format(len(all_subdivision_parent_codes)))
        for key, val in all_subdivision_parent_codes.items():
            self.assertIn(key, list(iso3166.countries_by_alpha2.keys()), "Subdivision code {} not found in list of ISO 3166 alpha-2 codes.".format(key))
            self.assertIsInstance(val, list, "Expected output to be of type list, got {}.".format(type(val)))
#7.)
        with (self.assertRaises(ValueError)):
            iso.country.subdivision_parent_codes("ABCD")
            iso.country.subdivision_parent_codes("Z")
            iso.country.subdivision_parent_codes("1234")
            iso.country.subdivision_parent_codes(False)
    
    @unittest.skip("Skipping to not change the main iso3166-2 object during other unit tests running.")
    def test_custom_subdivision(self):
        """ Testing custom_subdivision function that adds or deletes custom subdivisions to the main iso3166-2.json object. """        
        #add below test subdivisions to respective country objects
        iso.country.custom_subdivision("AD", "AD-ZZ", name="Bogus Subdivision", local_name="Bogus Subdivision", type="District", lat_lng=[42.520, 1.657], parent_code=None, flag_url=None)
        iso.country.custom_subdivision("DE", "DE-100", name="Made up subdivision", local_name="Made up subdivision", type="Land", lat_lng=[48.84, 11.479], parent_code=None, flag_url=None,)
        iso.country.custom_subdivision("GY", "GY-ABC", name="New Guyana subdivision", local_name="New Guyana subdivision", type="Region", lat_lng=[6.413, -60.123], parent_code=None, flag_url=None)
        iso.country.custom_subdivision("ZA", "ZA-123", name="Zambian province", local_name="Zambian province", type="Province", lat_lng=[-28.140, 26.777], parent_code=None, flag_url=None)

        #open test json with new subdivisions added
        with open(os.path.join("iso3166_2", "iso3166-2-data", "iso3166-2.json"), 'r', encoding='utf-8') as input_json: 
            test_all_subdivision_data = json.load(input_json)
#1.) 
        self.assertEqual(test_all_subdivision_data["AD"]["AD-ZZ"], {'flagUrl': None, 'latLng': [42.52, 1.657], 'name': 'Bogus Subdivision', 'localName': 'Bogus Subdivision', 'parentCode': None, 'type': 'District'},
            "Expected dict for AD-ZZ added subdivision does not match output:\n{}.".format(test_all_subdivision_data["AD"]["AD-ZZ"]))
#2.)
        self.assertEqual(test_all_subdivision_data["DE"]["DE-100"], {'flagUrl': None, 'latLng': [48.84, 11.479], 'name': 'Made up subdivision', 'localName': 'Made up subdivision', 'parentCode': None, 'type': 'Land'},
            "Expected dict for DE-100 added subdivision does not match output:\n{}.".format(test_all_subdivision_data["DE"]["DE-100"]))
#3.)
        self.assertEqual(test_all_subdivision_data["GY"]["GY-ABC"], {'flagUrl': None, 'latLng': [6.413, -60.123], 'name': 'New Guyana subdivision', 'localName': 'New Guyana subdivision', 'parentCode': None, 'type': 'Region'},
            "Expected dict for GY-ABC added subdivision does not match output:\n{}.".format(test_all_subdivision_data["GY"]["GY-ABC"]))
#4.)
        self.assertEqual(test_all_subdivision_data["ZA"]["ZA-123"], {'flagUrl': None, 'latLng': [-28.14, 26.777], 'name': 'Zambian province', 'localName': 'Zambian province', 'parentCode': None, 'type': 'Province'},
            "Expected dict for ZA-123 added subdivision does not match output:\n{}.".format(test_all_subdivision_data["ZA"]["ZA-123"]))

        #delete above custom subdivisions
        iso.country.custom_subdivision("AD", subdivision_code="AD-ZZ", delete=1)
        iso.country.custom_subdivision("DE", subdivision_code="DE-100", delete=1)
        iso.country.custom_subdivision("GY", subdivision_code="GY-ABC", delete=1)
        iso.country.custom_subdivision("ZA", subdivision_code="ZA-123", delete=1)

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
            iso.country.custom_subdivision("IE", "IE-CN")
            iso.country.custom_subdivision("JM", "JM-01")
            iso.country.custom_subdivision("TV", "TV-NIT")
            iso.country.custom_subdivision("UZ", "UZ-AN")
            iso.country.custom_subdivision("ABC", "blah")
            iso.country.custom_subdivision("ZZ", "blahblahblah")
            iso.country.custom_subdivision("123", "idfuiwf")
#10.)
        with self.assertRaises(TypeError):
            iso.country.custom_subdivision(123, 10.5)
            iso.country.custom_subdivision(name=False)
            iso.country.custom_subdivision("AD", "AD-01", type=123)

    def test_search(self):
        """ Testing searching by subdivision name functionality. """
        test_search_1 = "Monaghan" #IE
        test_search_2 = "Olaines Novads" #LV
        test_search_3 = "Ohangwena" #NA
        test_search_4 = "North" 
        test_search_5 = "Eastern" 
        test_search_6 = ""
        test_search_7 = "zzzzzzzz"
        test_search_8 = True
#1.)
        search_results_1 = iso.country.search(test_search_1, any=False)
        expected_search_result_1 = {'alpha_2': "IE", "subdivision_code": "IE-MN", 'name': 'Monaghan', 'localName': 'Monaghan', 'type': 'County', 
                                  'parentCode': 'IE-U', 
                                  'flagUrl': 'https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/IE/IE-MN.png', 
                                  'latLng': [54.249, -6.968]}
        self.assertIsInstance(search_results_1, dict, 
            "Expected output object to be a dict, got {}.".format(type(search_results_1)))
        self.assertEqual(search_results_1, expected_search_result_1, 
            "Observed and expected output objects do not match:\n{}.".format(search_results_1))
#2.)
        search_results_2 = iso.country.search(test_search_2, any=False)
        expected_search_result_2 = {'alpha_2': "LV", "subdivision_code": "LV-068", 'name': 'Olaines novads', 'localName': 'Olaines novads', 'type': 'Municipality', 
                                    'parentCode': None, 'flagUrl': 'https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/LV/LV-068.png', 
                                    'latLng': [56.795, 24.015]}
        self.assertIsInstance(search_results_2, dict,
            "Expected output object to be a dict, got {}.".format(type(search_results_2)))
        self.assertEqual(search_results_2, expected_search_result_2, 
            "Observed and expected output objects do not match:\n{}.".format(search_results_2))
#3.)
        search_results_3 = iso.country.search(test_search_3, any=False)
        expected_search_result_3 = {'alpha_2': "NA", "subdivision_code": "NA-OW", 'name': 'Ohangwena', 'localName': 'Ohangwena', 'type': 'Region', 
                                    'parentCode': None, 'flagUrl': None, 'latLng': [-17.598, 16.818]}
        self.assertIsInstance(search_results_3, dict,
            "Expected output object to be a dict, got {}.".format(type(search_results_3)))
        self.assertEqual(search_results_3, expected_search_result_3, 
            "Observed and expected output objects do not match:\n{}.".format(search_results_3))
#4.)
        search_results_4 = iso.country.search(test_search_4, any=True) #North
        expected_search_result_4 = [{'name': 'North', 'localName': 'North', 'type': 'Region', 'parentCode': None, 'flagUrl': None, 'latLng': [8.581, 13.914], 
                                     'alpha_2': 'CM', 'subdivision_code': 'CM-NO'}, {'name': 'Norte', 'localName': 'Norte', 'type': 'Province', 
                                     'parentCode': None, 'flagUrl': None, 'latLng': [11.804, -15.18], 'alpha_2': 'GW', 'subdivision_code': 'GW-N'}]

        self.assertIsInstance(search_results_4, list,
            "Expected output object to be a list, got {}.".format(type(search_results_4)))                 
        self.assertEqual(search_results_4, expected_search_result_4, 
            "Observed and expected output objects do not match:\n{}.".format(search_results_4))
#5.)
        search_results_5 = iso.country.search(test_search_5, any=True) #Eastern
        expected_search_result_5 = [{'name': 'Eastern', 'localName': 'Eastern', 'type': 'Province', 'parentCode': None, 
                                     'flagUrl': 'https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/ZM/ZM-03.png', 'latLng': [-13.806, 31.993], 
                                     'alpha_2': 'ZM', 'subdivision_code': 'ZM-03'}, {'name': 'Eastern', 'localName': 'Eastern', 'type': 'Province', 'parentCode': None, 
                                     'flagUrl': 'https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/ZM/ZM-03.png', 'latLng': [-13.806, 31.993], 
                                     'alpha_2': 'ZM', 'subdivision_code': 'ZM-03'}, {'name': 'Eastern', 'localName': 'Eastern', 'type': 'Province', 'parentCode': None, 
                                     'flagUrl': 'https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/ZM/ZM-03.png', 'latLng': [-13.806, 31.993], 
                                     'alpha_2': 'ZM', 'subdivision_code': 'ZM-03'}]

        self.assertIsInstance(search_results_5, list,
            "Expected output object to be a list, got {}.".format(type(search_results_5)))                 
        self.assertEqual(search_results_5, expected_search_result_5, 
            "Observed and expected output objects do not match:\n{}.".format(search_results_5))
#6.)
        search_results_6 = iso.country.search(test_search_6)
        self.assertEqual(search_results_6, {}, "Expected output to be an empty dict, got {}.".format(search_results_6))
#7.)
        search_results_7 = iso.country.search(test_search_7)
        self.assertEqual(search_results_7, {}, "Expected output to be an empty dict, got {}.".format(search_results_7))
#8.)
        with (self.assertRaises(TypeError)):
            search_results_7 = iso.country.search(test_search_8)
        
    def tearDown(self):
        """ Delete any test json folders. """
        shutil.rmtree(self.test_output_dir)

        #remove the temp dir created to store duplicate of iso3166-2 object before any changes were made using the add_subdivision() function,
        #a successful pass of all the above test cases mean there are no errors on the current object and the archive folder can be deleted
        if (os.path.isdir("archive-iso3166-2")):
            shutil.rmtree(self.test_output_dir)
            
if __name__ == '__main__':
    #run all unit tests
    unittest.main(verbosity=2)    