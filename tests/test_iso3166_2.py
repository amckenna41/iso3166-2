import iso3166_2 as iso
import iso3166
import requests
import json
import os
import getpass
from importlib.metadata import metadata
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

class ISO3166_2_Tests(unittest.TestCase):
    """
    Test suite for testing the iso3166-2 Python software package. 

    Test Cases
    ----------
    test_iso3166_2_metadata:
        testing correct software metdata for the iso3166-2 package. 
    test_iso3166_2:
        testing correct data returned from the "subdivisions" and "country" objects in the ISO3166_2 
        class of the iso3166-2 package.  
    test_iso3166_2_json:
        testing correct objects are returned from the ISO 3166-2 JSON, using a variety of inputs.
    test_iso3166_2_min_json:
        testing correct objects are returned from the minified ISO 3166-2 JSON, using a variety of inputs.
    test_subdivision_names:
        testing correct ISO 3166-2 subdivision names are returned from the subdivision_names() class function.
    test_subdivision_codes:
        testing correct ISO 3166-2 subdivision codes are returned from the subdivision_codes() class function.  
    """
    def setUp(self):
        """ Initialise test variables, import json. """
        #initalise User-agent header for requests library 
        # self.__version__ = metadata('iso3166-2')['version']
        self.__version__ = "1.1.0"
        self.user_agent_header = {'User-Agent': 'iso3166-2/{} ({}; {})'.format(self.__version__,
                                            'https://github.com/amckenna41/iso3166-2', getpass.getuser())}
    
        #base url for flag icons on iso3166-flag-icons repo
        self.flag_icons_base_url = "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/"

        #list of output columns for main iso3166-2 json
        self.correct_output_cols = [
            "altSpellings", "area", "borders", "capital", "capitalInfo", "car", "cca2", "cca3", "ccn3", "cioc", "coatOfArms",
            "continents", "currencies", "demonyms", "fifa", "flag", "flags", "gini", "idd", "independent", "landlocked",
            "languages", "latlng", "maps", "name", "population", "postalCode", "region", "startOfWeek", "status",
            "subdivisions", "subregion", "timezones", "tld", "translations", "unMember"
        ]

    @unittest.skip("")
    def test_iso3166_2_metadata(self): 
        """ Testing correct iso3166-2 software version and metadata. """
        self.assertEqual(metadata('iso3166-2')['version'], "1.1.0", 
            "iso3166-2 version is not correct, got: {}".format(metadata('iso3166-2')['version']))
        self.assertEqual(metadata('iso3166-2')['name'], "iso3166-2", 
            "iso3166-2 software name is not correct, got: {}".format(metadata('iso3166-2')['name']))
        self.assertEqual(metadata('iso3166-2')['author'], 
            "AJ McKenna, https://github.com/amckenna41", "iso3166-updates author is not correct, got: {}".format(metadata('iso3166_2')['author']))
        self.assertEqual(metadata('iso3166-2')['author-email'], 
            "amckenna41@qub.ac.uk", "iso3166-updates author email is not correct, got: {}".format(metadata('iso3166_2')['author-email']))
        self.assertEqual(metadata('iso3166-2')['keywords'], 
            ','.join(["iso", "iso3166", "beautifulsoup", "python", "pypi", "countries", "country codes", "iso3166-2", "iso3166-1", "alpha-2", "iso3166-updates", "rest countries"]).replace(" ", ""), 
                "iso3166-updates keywords are not correct, got: {}".format(metadata('iso3166-2')['keywords']))
        self.assertEqual(metadata('iso3166-2')['home-page'], 
            "https://github.com/amckenna41/iso3166-2", "iso3166-2 home page url is not correct, got: {}".format(metadata('iso3166_2')['home-page']))
        self.assertEqual(metadata('iso3166-2')['maintainer'], 
            "AJ McKenna", "iso3166-updates maintainer is not correct, got: {}".format(metadata('iso3166-2')['maintainer']))
        self.assertEqual(metadata('iso3166-2')['license'], "MIT", 
            "iso3166-updates license type is not correct, got: {}".format(metadata('iso3166-2')['license']))

    def test_iso3166_2(self):
        """ Test ISO 3166-2 class and its methods and attributes. """
        #testing class using iso3166-2.json file as input
        self.assertIsInstance(iso.country.alpha2, list, 
            "Expected alpha-2 attribute to be a list, got {}.".format(type(iso.country.alpha2)))
        self.assertEqual(len(iso.country.alpha2), 250, 
            "Expected 250 alpha-2 codes, got {}.".format(len(iso.country.alpha2)))
        self.assertIsInstance(iso.country.alpha3, list, 
            "Expected alpha-3 attribute to be a list, got {}.".format(type(iso.country.alpha3)))
        self.assertEqual(len(iso.country.alpha3), 250, 
            "Expected 250 alpha-3 codes, got {}.".format(len(iso.country.alpha3)))
        self.assertIsInstance(iso.country.all_iso3166_2_data, dict,
            "Expected ISO 3166-2 data object to be a dict, got {}.".format(type(iso.country.all_iso3166_2_data)))
        self.assertEqual(len(iso.country.all_iso3166_2_data), 250, 
            "Expected 250 countrys in ISO 3166-2 data object, got {}.".format(len(iso.country.all_iso3166_2_data)))       
        self.assertTrue(iso.country.using_country_data, "Expected boolean attribute to be True.")
        for code in iso.country.all_iso3166_2_data:
            self.assertIn(code, iso.country.alpha2,
                "Alpha-2 code {} not found in list of available 2 letter codes.".format(code))

        #testing class using iso3166-2-min.json file as input
        self.assertIsInstance(iso.subdivisions.alpha2, list, 
            "Expected alpha-2 attribute to be a list, got {}.".format(type(iso.subdivisions.alpha2)))
        self.assertEqual(len(iso.subdivisions.alpha2), 250, 
            "Expected 250 alpha-2 codes, got {}.".format(len(iso.subdivisions.alpha2)))
        self.assertIsInstance(iso.subdivisions.alpha3, list, 
            "Expected alpha-3 attribute to be a list, got {}.".format(type(iso.country.alpha3)))
        self.assertEqual(len(iso.subdivisions.alpha3), 250, 
            "Expected 250 alpha-3 codes, got {}.".format(len(iso.subdivisions.alpha3)))
        self.assertIsInstance(iso.subdivisions.all_iso3166_2_data, dict,
            "Expected ISO3166-2 data object to be a dict, got {}.".format(type(iso.subdivisions.all_iso3166_2_data)))
        self.assertEqual(len(iso.subdivisions.all_iso3166_2_data), 250, 
            "Expected 250 countrys in ISO3166-2 data object, got {}.".format(len(iso.subdivisions.all_iso3166_2_data)))       
        self.assertFalse(iso.subdivisions.using_country_data, "Expected boolean attribute to be False.")
        for code in iso.subdivisions.all_iso3166_2_data:
            self.assertIn(code, iso.subdivisions.alpha2,
                "Alpha-2 code {} not found in list of available 2 letter codes.".format(code))

    # @unittest.skip("")
    def test_iso3166_2_json(self):
        """ Testing iso3166-2.json contents and data. """
        test_alpha2_au = iso.country['AU'] #Australia
        test_alpha2_lu = iso.country['LU'] #Luxembourg
        test_alpha2_mg = iso.country["MG"] #Madagascar 
        test_alpha2_om = iso.country["OM"] #Oman
        test_alpha2_tt_sd_uy = iso.country["TT, SD, UY"] #Trinidad and Tobago, Sudan, Uraguay
        test_alpha2_irn_jam_kaz = iso.country["IRN, JAM, KAZ"] #Iran, Jamaica, Kazakhstan
#1.)    
        self.assertIsInstance(test_alpha2_au, dict, "Expected output to be type dict, got {}.".format(type(test_alpha2_au)))
        self.assertEqual(len(test_alpha2_au), 35, "Expected 35 keys/attributes in output dict, got {}.".format(len(test_alpha2_au)))
        self.assertEqual(test_alpha2_au.name.common, "Australia", "Name expected to be Australia, got {}.".format(test_alpha2_au.name.common))        
        self.assertEqual(test_alpha2_au.cca2, "AU", "Expected alpha-2 code to be AU, got {}.".format(test_alpha2_au.cca2))        
        self.assertEqual(test_alpha2_au.cca3, "AUS", "Expected alpha-3 code to be AUS, got {}.".format(test_alpha2_au.cca3))         
        self.assertEqual(test_alpha2_au.currencies.AUD['name'], "Australian dollar")        
        self.assertEqual(test_alpha2_au.capital[0], "Canberra")        
        self.assertEqual(test_alpha2_au.region, "Oceania")        
        self.assertEqual(list(test_alpha2_au.languages.keys())[0], "eng")        
        self.assertEqual(test_alpha2_au.area, 7692024)        
        self.assertEqual(test_alpha2_au.population, 25687041)        
        self.assertEqual(test_alpha2_au.latlng, [-27.0, 133.0], "")        
        self.assertEqual(len(test_alpha2_au.subdivisions), 8, "")
        self.assertEqual(test_alpha2_au, iso.country['AUS']) #test objects match if using either alpha-2/alpha-3 codes
        for col in iso.country["AU"].keys():
            self.assertIn(col, self.correct_output_cols, "Column {} not found in list of correct columns.".format(col))
#2.)
        self.assertIsInstance(test_alpha2_lu, dict, "Expected output to be type dict, got {}.".format(type(test_alpha2_lu)))
        self.assertEqual(len(test_alpha2_lu), 36, "Expected 36 keys/attributes in output dict, got {}.".format(len(test_alpha2_lu)))
        self.assertEqual(test_alpha2_lu.name.common, "Luxembourg", "Name expected to be Luxembourg, got {}.".format(test_alpha2_lu.name.common))      
        self.assertEqual(test_alpha2_lu.cca2, "LU", "Expected alpha-2 code to be LU, got {}.".format(test_alpha2_lu.cca2))  
        self.assertEqual(test_alpha2_lu.cca3, "LUX", "Expected alpha-3 code to be LUX, got {}.".format(test_alpha2_lu.cca3))     
        self.assertEqual(test_alpha2_lu.currencies.EUR['name'], "Euro")        
        self.assertEqual(test_alpha2_lu.capital[0], "Luxembourg")        
        self.assertEqual(test_alpha2_lu.region, "Europe")        
        self.assertEqual(list(test_alpha2_lu.languages.keys()), ["deu", "fra", "ltz"])        
        self.assertEqual(test_alpha2_lu.area, 2586)        
        self.assertEqual(test_alpha2_lu.population, 632275)        
        self.assertEqual(len(test_alpha2_lu.subdivisions), 12, "")
        self.assertEqual(test_alpha2_lu.latlng, [49.75, 6.16666666], "")        
        self.assertEqual(test_alpha2_lu, iso.country['LUX']) #test objects match if using either alpha-2/alpha-3 codes
        for col in iso.country["LU"].keys():
            self.assertIn(col, self.correct_output_cols, "Column {} not found in list of correct columns.".format(col))
#3.)
        self.assertIsInstance(test_alpha2_mg, dict, "Expected output to be type dict, got {}.".format(type(test_alpha2_mg)))
        self.assertEqual(len(test_alpha2_mg), 35, "Expected 35 keys/attributes in output dict, got {}.".format(len(test_alpha2_mg)))
        self.assertEqual(test_alpha2_mg.name.common, "Madagascar", "Name expected to be Madagascar, got {}.".format(test_alpha2_mg.name.common))           
        self.assertEqual(test_alpha2_mg.cca2, "MG", "Expected alpha-2 code to be MG, got {}.".format(test_alpha2_mg.cca2))    
        self.assertEqual(test_alpha2_mg.cca3, "MDG", "Expected alpha-3 code to be MDG, got {}.".format(test_alpha2_mg.cca3))          
        self.assertEqual(test_alpha2_mg.currencies.MGA['name'], "Malagasy ariary")        
        self.assertEqual(test_alpha2_mg.capital[0], "Antananarivo")        
        self.assertEqual(test_alpha2_mg.region, "Africa")        
        self.assertEqual(list(test_alpha2_mg.languages.keys()), ["fra", "mlg"])        
        self.assertEqual(test_alpha2_mg.area, 587041)        
        self.assertEqual(test_alpha2_mg.population, 27691019)        
        self.assertEqual(test_alpha2_mg.latlng, [-20.0, 47.0], "")        
        self.assertEqual(len(test_alpha2_mg.subdivisions), 6, "")
        self.assertEqual(test_alpha2_mg, iso.country['MDG']) #test objects match if using either alpha-2/alpha-3 codes
        for col in iso.country["MG"].keys():
            self.assertIn(col, self.correct_output_cols, "Column {} not found in list of correct columns.".format(col))
#4.)
        self.assertIsInstance(test_alpha2_om, dict, "Expected output to be type dict, got {}.".format(type(test_alpha2_om)))
        self.assertEqual(len(test_alpha2_om), 35, "Expected 35 keys/attributes in output dict, got {}.".format(len(test_alpha2_om)))
        self.assertEqual(test_alpha2_om.name.common, "Oman", "Name expected to be Oman, got {}.".format(test_alpha2_om.name.common))   
        self.assertEqual(test_alpha2_om.cca2, "OM", "Expected alpha-2 code to be OM, got {}.".format(test_alpha2_om.cca2))         
        self.assertEqual(test_alpha2_om.cca3, "OMN", "Expected alpha-2 code to be OMN, got {}.".format(test_alpha2_om.cca2))          
        self.assertEqual(test_alpha2_om.currencies.OMR['name'], "Omani rial")        
        self.assertEqual(test_alpha2_om.capital[0], "Muscat")        
        self.assertEqual(test_alpha2_om.region, "Asia")        
        self.assertEqual(list(test_alpha2_om.languages.keys()), ["ara"])        
        self.assertEqual(test_alpha2_om.area, 309500)        
        self.assertEqual(test_alpha2_om.population, 5106622)        
        self.assertEqual(test_alpha2_om.latlng, [21.0, 57.0], "")        
        self.assertEqual(len(test_alpha2_om.subdivisions), 11, "")
        self.assertEqual(test_alpha2_om, iso.country['OMN']) #test objects match if using either alpha-2/alpha-3 codes
        for col in iso.country["OM"].keys():
            self.assertIn(col, self.correct_output_cols, "Column {} not found in list of correct columns.".format(col))
#5.)    
        self.assertIsInstance(test_alpha2_tt_sd_uy, dict, "Expected output to be type dict, got {}.".format(type(test_alpha2_tt_sd_uy)))
        self.assertEqual(list(test_alpha2_tt_sd_uy.keys()), ["TT", "SD", "UY"], "Expected output to contain keys TT, SD and UY, got {}.".format(list(test_alpha2_tt_sd_uy.keys())))
        self.assertEqual(len(test_alpha2_tt_sd_uy["TT"]), 34, "Expected 34 keys/attributes in output dict, got {}.".format(len(test_alpha2_tt_sd_uy["TT"])))
        self.assertEqual(len(test_alpha2_tt_sd_uy["SD"]), 36, "Expected 36 keys/attributes in output dict, got {}.".format(len(test_alpha2_tt_sd_uy["SD"])))
        self.assertEqual(len(test_alpha2_tt_sd_uy["UY"]), 36, "Expected 36 keys/attributes in output dict, got {}.".format(len(test_alpha2_tt_sd_uy["UY"])))
        self.assertEqual(test_alpha2_tt_sd_uy["TT"].name.common, "Trinidad and Tobago", "Name expected to be Trinidad and Tabago, got {}.".format(test_alpha2_tt_sd_uy["TT"].name.common))   
        self.assertEqual(test_alpha2_tt_sd_uy["SD"].name.common, "Sudan", "Name expected to be Sudan, got {}.".format(test_alpha2_tt_sd_uy["SD"].name.common))   
        self.assertEqual(test_alpha2_tt_sd_uy["UY"].name.common, "Uruguay", "Name expected to be Uruguay, got {}.".format(test_alpha2_tt_sd_uy["UY"].name.common))   
        for col in test_alpha2_tt_sd_uy["TT"].keys():
            self.assertIn(col, self.correct_output_cols, "Column {} not found in list of correct columns.".format(col))
        for col in test_alpha2_tt_sd_uy["SD"].keys():
            self.assertIn(col, self.correct_output_cols, "Column {} not found in list of correct columns.".format(col))
        for col in test_alpha2_tt_sd_uy["UY"].keys():
            self.assertIn(col, self.correct_output_cols, "Column {} not found in list of correct columns.".format(col))
#6.)    
        self.assertIsInstance(test_alpha2_irn_jam_kaz, dict, "Expected output to be type dict, got {}.".format(type(test_alpha2_irn_jam_kaz)))
        self.assertEqual(list(test_alpha2_irn_jam_kaz.keys()), ["IR", "JM", "KZ"], "Expected output to contain keys IR, JM and KZ, got {}.".format(list(test_alpha2_irn_jam_kaz.keys())))
        self.assertEqual(len(test_alpha2_irn_jam_kaz["IR"]), 36, "Expected 36 keys/attributes in output dict, got {}.".format(len(test_alpha2_irn_jam_kaz["IR"])))
        self.assertEqual(len(test_alpha2_irn_jam_kaz["JM"]), 34, "Expected 34 keys/attributes in output dict, got {}.".format(len(test_alpha2_irn_jam_kaz["JM"])))
        self.assertEqual(len(test_alpha2_irn_jam_kaz["KZ"]), 36, "Expected 36 keys/attributes in output dict, got {}.".format(len(test_alpha2_irn_jam_kaz["KZ"])))
        self.assertEqual(test_alpha2_irn_jam_kaz["IR"].name.common, "Iran", "Name expected to be Iran, got {}.".format(test_alpha2_irn_jam_kaz["IR"].name.common))   
        self.assertEqual(test_alpha2_irn_jam_kaz["JM"].name.common, "Jamaica", "Name expected to be Jamaica, got {}.".format(test_alpha2_irn_jam_kaz["JM"].name.common))   
        self.assertEqual(test_alpha2_irn_jam_kaz["KZ"].name.common, "Kazakhstan", "Name expected to be Kazakhstan, got {}.".format(test_alpha2_irn_jam_kaz["KZ"].name.common))   
        for col in test_alpha2_irn_jam_kaz["IR"].keys():
            self.assertIn(col, self.correct_output_cols, "Column {} not found in list of correct columns.".format(col))
        for col in test_alpha2_irn_jam_kaz["JM"].keys():
            self.assertIn(col, self.correct_output_cols, "Column {} not found in list of correct columns.".format(col))
        for col in test_alpha2_irn_jam_kaz["KZ"].keys():
            self.assertIn(col, self.correct_output_cols, "Column {} not found in list of correct columns.".format(col))
#7.)
        with (self.assertRaises(ValueError)):
            invalid_country = iso.country["ZZ"]
            invalid_country = iso.country["XY"]
            invalid_country = iso.country["XYZ"]
            invalid_country = iso.country["A, B, C, D"]
#8.)
        with (self.assertRaises(TypeError)):
            invalid_country = iso.country[123]
            invalid_country = iso.country[0.5]
            invalid_country = iso.country[False]

    # @unittest.skip("")
    def test_iso3166_2_min_json(self):
        """ Testing minified ISO3166-2 JSON contents and data. """
        test_alpha2_ba = iso.subdivisions["BA"] #Bosnia and Herzegovina
        test_alpha2_cy = iso.subdivisions["CY"] #Cyprus
        test_alpha2_ga = iso.subdivisions["GA"] #Gabon
        test_alpha2_rw_vu = iso.subdivisions["RW, VU"] #Rwanda, Vanuatu
        test_alpha2_gg_kw_vc = iso.subdivisions["GG, KW, VC"] #Guernsey, Kuwait, St Vincent & the Grenadines
#1.)    
        ba_subdivision_codes = ['BA-BIH', 'BA-BRC', 'BA-SRP']
        ba_subdivision_names = ['Federacija Bosne i Hercegovine', 'Brčko distrikt', 'Republika Srpska']

        self.assertIsInstance(test_alpha2_ba, dict, "")
        self.assertEqual(len(test_alpha2_ba), 3, "")
        self.assertEqual(list(test_alpha2_ba.keys()), ba_subdivision_codes, "")
        self.assertEqual(list(test_alpha2_ba['BA-BIH'].keys()), ['name', 'type', 'parent_code', 'latlng', 'flag_url'], "")
        for key in test_alpha2_ba:
            self.assertIn(test_alpha2_ba[key].name, ba_subdivision_names, "")
            if ((test_alpha2_ba[key].flag_url is not None) or (test_alpha2_ba[key].flag_url == "")):
                self.assertEqual(requests.get(test_alpha2_ba[key].flag_url, headers=self.user_agent_header).status_code, 200, "")
            self.assertIsNone(test_alpha2_ba[key]['parent_code'], "")
            self.assertEqual(len(test_alpha2_ba[key].latlng), 2, "")        
#2.)
        cy_subdivision_codes = ['CY-01', 'CY-02', 'CY-03', 'CY-04', 'CY-05', 'CY-06']
        cy_subdivision_names = ['Lefkosia', 'Lemesos', 'Larnaka', 'Ammochostos', 'Baf', 'Girne']

        self.assertIsInstance(test_alpha2_cy, dict, "")
        self.assertEqual(len(test_alpha2_cy), 6, "")
        self.assertEqual(list(test_alpha2_cy.keys()), cy_subdivision_codes, "")
        self.assertEqual(list(test_alpha2_cy['CY-01'].keys()), ['name', 'type', 'parent_code', 'latlng', 'flag_url'], "")
        for key in test_alpha2_cy:
            self.assertIn(test_alpha2_cy[key].name, cy_subdivision_names, "")
            if ((test_alpha2_cy[key].flag_url is not None) or (test_alpha2_cy[key].flag_url == "")):
                self.assertEqual(requests.get(test_alpha2_cy[key].flag_url, headers=self.user_agent_header).status_code, 200, "")
            self.assertIsNone(test_alpha2_cy[key]['parent_code'], "")
            self.assertEqual(len(test_alpha2_cy[key].latlng), 2, "")        
#3.)
        ga_subdivision_codes = ['GA-1', 'GA-2', 'GA-3', 'GA-4', 'GA-5', 'GA-6', 'GA-7', 'GA-8', 'GA-9']
        ga_subdivision_names = ['Estuaire', 'Haut-Ogooué', 'Moyen-Ogooué', 'Ngounié', 'Nyanga', 'Ogooué-Ivindo', 
            'Ogooué-Lolo', 'Ogooué-Maritime', 'Woleu-Ntem']
        
        self.assertIsInstance(test_alpha2_ga, dict, "")
        self.assertEqual(len(test_alpha2_ga), 9, "")
        self.assertEqual(list(test_alpha2_ga.keys()), ga_subdivision_codes, "")
        self.assertEqual(list(test_alpha2_ga['GA-1'].keys()), ['name', 'type', 'parent_code', 'latlng', 'flag_url'], "")
        for key in test_alpha2_ga:
            self.assertIn(test_alpha2_ga[key].name, ga_subdivision_names, "")
            if ((test_alpha2_ga[key].flag_url is not None) or (test_alpha2_ga[key].flag_url == "")):
                self.assertEqual(requests.get(test_alpha2_ga[key].flag_url, headers=self.user_agent_header).status_code, 200, "")
            self.assertIsNone(test_alpha2_ga[key]['parent_code'], "")
            self.assertEqual(len(test_alpha2_ga[key].latlng), 2, "")        
#4.)
        rw_subdivision_codes = ['RW-01', 'RW-02', 'RW-03', 'RW-04', 'RW-05']
        vu_subdivision_codes = ['VU-MAP', 'VU-PAM', 'VU-SAM', 'VU-SEE', 'VU-TAE', 'VU-TOB']
        rw_subdivision_names = ['City of Kigali', 'Eastern', 'Northern', 'Western', 'Southern']
        vu_subdivision_names = ['Malampa', 'Pénama', 'Sanma', 'Shéfa', 'Taféa', 'Torba']

        self.assertIsInstance(test_alpha2_rw_vu, dict, "")
        self.assertEqual(list(test_alpha2_rw_vu.keys()), ['RW', 'VU'], "")
        self.assertEqual(len(test_alpha2_rw_vu["RW"]), 5, "")
        self.assertEqual(len(test_alpha2_rw_vu["VU"]), 6, "")
        self.assertEqual(list(test_alpha2_rw_vu["RW"].keys()), rw_subdivision_codes, "")
        self.assertEqual(list(test_alpha2_rw_vu["VU"].keys()), vu_subdivision_codes, "")
        self.assertEqual(list(test_alpha2_rw_vu["RW"]['RW-01'].keys()), ['name', 'type', 'parent_code', 'latlng', 'flag_url'], "")
        self.assertEqual(list(test_alpha2_rw_vu["VU"]['VU-MAP'].keys()), ['name', 'type', 'parent_code', 'latlng', 'flag_url'], "")
        for key in test_alpha2_rw_vu["RW"]:
            self.assertIn(test_alpha2_rw_vu["RW"][key].name, rw_subdivision_names, "")
            if ((test_alpha2_rw_vu["RW"][key].flag_url is not None) or (test_alpha2_rw_vu["RW"][key].flag_url == "")):
                self.assertEqual(requests.get(test_alpha2_rw_vu["RW"][key].flag_url, headers=self.user_agent_header).status_code, 200, "")
            self.assertIsNone(test_alpha2_rw_vu["RW"][key]['parent_code'], "")
            self.assertEqual(len(test_alpha2_rw_vu["RW"][key].latlng), 2, "") 
        for key in test_alpha2_rw_vu["VU"]:
            self.assertIn(test_alpha2_rw_vu["VU"][key].name, vu_subdivision_names, "")
            if ((test_alpha2_rw_vu["VU"][key].flag_url is not None) or (test_alpha2_rw_vu["VU"][key].flag_url == "")):
                self.assertEqual(requests.get(test_alpha2_rw_vu["VU"][key].flag_url, headers=self.user_agent_header).status_code, 200, "")
            self.assertIsNone(test_alpha2_rw_vu["VU"][key]['parent_code'], "")
            self.assertEqual(len(test_alpha2_rw_vu["VU"][key].latlng), 2, "")            
#5.)
        kw_subdivision_codes = ['KW-AH', 'KW-FA', 'KW-HA', 'KW-JA', 'KW-KU', 'KW-MU']
        kw_subdivision_names = ['Al Aḩmadī', 'Al Farwānīyah', 'Ḩawallī', "Al Jahrā’", "Al ‘Āşimah", 'Mubārak al Kabīr']
        vc_subdivision_codes = ['VC-01', 'VC-02', 'VC-03', 'VC-04', 'VC-05', 'VC-06']
        vc_subdivision_names = ['Charlotte', 'Saint Andrew', 'Saint David', 'Saint George', 'Saint Patrick', 'Grenadines']
        
        self.assertIsInstance(test_alpha2_gg_kw_vc, dict, "")
        self.assertEqual(list(test_alpha2_gg_kw_vc.keys()), ['GG', 'KW', 'VC'], "")
        self.assertEqual(len(test_alpha2_gg_kw_vc["GG"]), 0, "")
        self.assertEqual(len(test_alpha2_gg_kw_vc["KW"]), 6, "")
        self.assertEqual(len(test_alpha2_gg_kw_vc["VC"]), 6, "")
        self.assertEqual(list(test_alpha2_gg_kw_vc["GG"].keys()), [], "")
        self.assertEqual(list(test_alpha2_gg_kw_vc["KW"].keys()), kw_subdivision_codes, "")
        self.assertEqual(list(test_alpha2_gg_kw_vc["VC"].keys()), vc_subdivision_codes, "")
        self.assertEqual(list(test_alpha2_gg_kw_vc["KW"]['KW-AH'].keys()), ['name', 'type', 'parent_code', 'latlng', 'flag_url'], "")
        self.assertEqual(list(test_alpha2_gg_kw_vc["VC"]['VC-01'].keys()), ['name', 'type', 'parent_code', 'latlng', 'flag_url'], "")
        for key in test_alpha2_gg_kw_vc["KW"]:
            self.assertIn(test_alpha2_gg_kw_vc["KW"][key].name, kw_subdivision_names, "")
            if ((test_alpha2_gg_kw_vc["KW"][key].flag_url is not None) or (test_alpha2_gg_kw_vc["KW"][key].flag_url == "")):
                self.assertEqual(requests.get(test_alpha2_gg_kw_vc["KW"][key].flag_url, headers=self.user_agent_header).status_code, 200, "")
            self.assertIsNone(test_alpha2_gg_kw_vc["KW"][key]['parent_code'], "")
            self.assertEqual(len(test_alpha2_gg_kw_vc["KW"][key].latlng), 2, "") 
        for key in test_alpha2_gg_kw_vc["VC"]:
            self.assertIn(test_alpha2_gg_kw_vc["VC"][key].name, vc_subdivision_names, "")
            if ((test_alpha2_gg_kw_vc["VC"][key].flag_url is not None) or (test_alpha2_gg_kw_vc["VC"][key].flag_url == "")):
                self.assertEqual(requests.get(test_alpha2_gg_kw_vc["VC"][key].flag_url, headers=self.user_agent_header).status_code, 200, "")
            self.assertIsNone(test_alpha2_gg_kw_vc["VC"][key]['parent_code'], "")
            self.assertEqual(len(test_alpha2_gg_kw_vc["VC"][key].latlng), 2, "")  
#6.)
        with (self.assertRaises(ValueError)):
            invalid_country = iso.subdivisions["ZZ"]
            invalid_country = iso.subdivisions["XY"]
            invalid_country = iso.subdivisions["XYZ"]
            invalid_country = iso.subdivisions["AB, CD, EF"]
#7.)
        with (self.assertRaises(TypeError)):
            invalid_country = iso.subdivisions[123]
            invalid_country = iso.subdivisions[0.5]
            invalid_country = iso.subdivisions[False]

    def test_subdivision_names(self):
        """ Testing functionality for getting list of all ISO 3166-2 subdivision names. """
        expected_km_subdivision_names = ['Andjouân', 'Andjazîdja', 'Mohéli']
        expected_er_subdivision_names = ['Ansabā', 'Debubawi K’eyyĭḥ Baḥri', 'Al Janūbī', 'Gash-Barka', 'Al Awsaţ', 'Semienawi K’eyyĭḥ Baḥri']
        expected_gl_subdivision_names = ['Avannaata Kommunia', 'Kommune Kujalleq', 'Qeqqata Kommunia', 'Kommune Qeqertalik', 'Kommuneqarfik Sermersooq']
        expected_ls_subdivision_names = ['Maseru', 'Botha-Bothe', 'Leribe', 'Berea', 'Mafeteng', "Mohale's Hoek", 'Quthing', "Qacha's Nek", 'Mokhotlong', 'Thaba-Tseka']
        expected_zm_subdivision_names = ['Western', 'Central', 'Eastern', 'Luapula', 'Northern', 'North-Western', 'Southern', 'Copperbelt', 'Lusaka', 'Muchinga']
        expected_ag_bn_subdivision_names = {"AG": ["Saint George", "Saint John", "Saint Mary", "Saint Paul", "Saint Peter", "Saint Philip", "Barbuda", "Redonda"], 
                                            "BN": ["Belait", "Brunei-Muara", "Temburong", "Tutong"]}
        expected_dj_va_subdivision_names = {"DJ": ["Arta", "Ali Sabieh", "Dikhil", "Djibouti", "Awbūk", "Tadjourah"], 
                                            "VA": []}
#1.)        
        km_subdivision_names = iso.subdivisions.subdivision_names("KM") #Comoros
        self.assertEqual(km_subdivision_names, expected_km_subdivision_names, "")
#2.)
        er_subdivision_names = iso.subdivisions.subdivision_names("ER") #Eritrea
        self.assertEqual(er_subdivision_names, expected_er_subdivision_names, "")
#3.)
        gl_subdivision_names = iso.subdivisions.subdivision_names("GL") #Greenland
        self.assertEqual(gl_subdivision_names, expected_gl_subdivision_names, "")
#4.)
        ls_subdivision_names = iso.subdivisions.subdivision_names("LS") #Lesotho
        self.assertEqual(ls_subdivision_names, expected_ls_subdivision_names, "")
#5.)
        zm_subdivision_names = iso.subdivisions.subdivision_names("ZM") #Zambia
        self.assertEqual(zm_subdivision_names, expected_zm_subdivision_names, "")
#6.)
        ag_bn_subdivision_names = iso.subdivisions.subdivision_names("AG, BN") #Antigua and Barbuda, Brunei
        self.assertEqual(ag_bn_subdivision_names, expected_ag_bn_subdivision_names, "")
#7.)
        dj_va_subdivision_names = iso.subdivisions.subdivision_names("DJI, VAT") #Djibouti, Vatican City
        self.assertEqual(dj_va_subdivision_names, expected_dj_va_subdivision_names, "")
#8.)
        all_subdivision_names = iso.subdivisions.subdivision_names() 
        self.assertEqual(len(all_subdivision_names), 250, "")
        for key, val in all_subdivision_names.items():
            self.assertIn(key, list(iso3166.countries_by_alpha2.keys()))
            self.assertIsInstance(val, list, "")
#9.)
        with (self.assertRaises(ValueError)):
            invalid_country = iso.subdivisions.subdivision_names("ABCD")
            invalid_country = iso.subdivisions.subdivision_names("Z")
            invalid_country = iso.subdivisions.subdivision_names("1234")
            invalid_country = iso.subdivisions.subdivision_names("blah, blah, blah")
            invalid_country = iso.subdivisions.subdivision_names(False)

    def test_subdivision_codes(self):
        """ Testing functionality for getting list of all ISO3166-2 subdivision codes. """
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
        bq_subdivision_codes = iso.subdivisions.subdivision_codes("BQ") #Bonaire, Sint Eustatius and Saba
        self.assertEqual(bq_subdivision_codes, expected_bq_subdivision_codes, "")
#2.)
        sz_subdivision_codes = iso.subdivisions.subdivision_codes("SZ") #Eswatini
        self.assertEqual(sz_subdivision_codes, expected_sz_subdivision_codes, "")
#3.)
        sm_subdivision_codes = iso.subdivisions.subdivision_codes("SM") #San Marino
        self.assertEqual(sm_subdivision_codes, expected_sm_subdivision_codes, "")
#4.)
        pw_subdivision_codes = iso.subdivisions.subdivision_codes("PW") #Palau
        self.assertEqual(pw_subdivision_codes, expected_pw_subdivision_codes, "")
#5.)   
        wf_subdivision_codes = iso.subdivisions.subdivision_codes("WF") #Wallis and Futuna 
        self.assertEqual(wf_subdivision_codes, expected_wf_subdivision_codes, "")      
#6.)   
        mg_sb_subdivision_codes = iso.subdivisions.subdivision_codes("MG, SB") #Madagascar, Solomon Islands
        self.assertEqual(mg_sb_subdivision_codes, expected_mg_sb_subdivision_codes, "")   
#7.)   
        gnq_tca_subdivision_codes = iso.subdivisions.subdivision_codes("GNQ, TCA") #Equitorial Guinea, Turks and Caicos Islands
        self.assertEqual(gnq_tca_subdivision_codes, expected_gnq_tca_subdivision_codes, "")   
#8.)
        all_subdivision_codes = iso.subdivisions.subdivision_codes() 
        self.assertEqual(len(all_subdivision_codes), 250, "")
        for key, val in all_subdivision_codes.items():
            self.assertIn(key, list(iso3166.countries_by_alpha2.keys()))
            self.assertIsInstance(val, list, "")
#9.)
        with (self.assertRaises(ValueError)):
            invalid_country = iso.subdivisions.subdivision_codes("ABCD")
            invalid_country = iso.subdivisions.subdivision_codes("Z")
            invalid_country = iso.subdivisions.subdivision_codes("1234")
            invalid_country = iso.subdivisions.subdivision_codes(False)
    
if __name__ == '__main__':
    #run all unit tests
    unittest.main(verbosity=2)    