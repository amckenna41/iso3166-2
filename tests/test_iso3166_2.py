import iso3166_2 as iso
import iso3166
import requests
import json
import os
import getpass
# import importlib.metadata as metadata  
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

__version__ = "1.0.1"

class ISO3166_2_Updates(unittest.TestCase):

    def setUp(self):
        """ Initialise test variables, import json. """
        #initalise User-agent header for requests library 
        self.user_agent_header = {'User-Agent': 'iso3166-2/{} ({}; {})'.format(__version__,
                                            'https://github.com/amckenna41/iso3166-2', getpass.getuser())}
    
        #import main iso3166-2 json 
        with open(os.path.join("iso3166_2", "iso3166-2-data", "iso3166-2.json")) as iso3166_2_json:
            self.all_iso3166_2_data = json.load(iso3166_2_json)

        #import min iso3166-2 json
        with open(os.path.join("iso3166_2", "iso3166-2-data", "iso3166-2-min.json")) as iso3166_2_json:
            self.all_iso3166_2_min_data = json.load(iso3166_2_json)

        #base url for flag icons on iso3166-flag-icons repo
        self.flag_icons_base_url = "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/"

    # @unittest.skip("")
    # def test_iso3166_2_metadata(self): 
    #     """ Testing correct iso3166-2 software version and metadata. """
    #     self.assertEqual(metadata.metadata('iso3166_2')['version'], "1.0.2", 
    #         "iso3166-2 version is not correct, got: {}".format(metadata.metadata('iso3166-2')['version']))
    #     self.assertEqual(metadata.metadata('iso3166-2')['name'], "iso3166-2", 
    #         "iso3166-2 software name is not correct, got: {}".format(metadata.metadata('iso3166-2')['name']))
    #     self.assertEqual(metadata.metadata('iso3166-2')['author'], 
    #         "AJ McKenna, https://github.com/amckenna41", "iso3166-updates author is not correct, got: {}".format(metadata.metadata('iso3166_2')['author']))
    #     self.assertEqual(metadata.metadata('iso3166-2')['author-email'], 
    #         "amckenna41@qub.ac.uk", "iso3166-updates author email is not correct, got: {}".format(metadata.metadata('iso3166_2')['author-email']))
    #     self.assertEqual(metadata.metadata('iso3166-2')['keywords'], 
    #         ','.join(["iso", "iso3166", "beautifulsoup", "python", "pypi", "countries", "country codes", "iso3166-2", "iso3166-1", "alpha-2", "iso3166-updates", "rest countries"]).replace(" ", ""), 
    #             "iso3166-updates keywords are not correct, got: {}".format(metadata.metadata('iso3166-2')['keywords']))
    #     self.assertEqual(metadata.metadata('iso3166-2')['home-page'], 
    #         "https://github.com/amckenna41/iso3166-2", "iso3166-2 home page url is not correct, got: {}".format(metadata.metadata('iso3166_2')['home-page']))
    #     self.assertEqual(metadata.metadata('iso3166-2')['maintainer'], 
    #         "AJ McKenna", "iso3166-updates maintainer is not correct, got: {}".format(metadata.metadata('iso3166-2')['maintainer']))
    #     self.assertEqual(metadata.metadata('iso3166-2')['license'], "MIT", 
    #         "iso3166-updates license type is not correct, got: {}".format(metadata.metadata('iso3166-2')['license']))

    def test_iso3166_2(self):
        """ Test ISO3166-2 class and its methods and attributes. """
        #testing class using iso3166-2.json file as input
        self.assertIsInstance(iso.country.alpha2, list, 
            "Expected alpha-2 attribute to be a list, got {}.".format(type(iso.country.alpha2)))
        self.assertEqual(len(iso.country.alpha2), 250, 
            "Expected 250 alpha-2 codes, got {}.".format(len(iso.country.alpha2)))
        self.assertIsInstance(iso.country.alpha3, list, 
            "Expected alpha3 attribute to be a list, got {}.".format(type(iso.country.alpha3)))
        self.assertEqual(len(iso.country.alpha3), 250, 
            "Expected 250 alpha3 codes, got {}.".format(len(iso.country.alpha3)))
        self.assertIsInstance(iso.country.all_iso3166_2_data, dict,
            "Expected ISO3166-2 data object to be a dict, got {}.".format(type(iso.country.all_iso3166_2_data)))
        self.assertEqual(len(iso.country.all_iso3166_2_data), 250, 
            "Expected 250 countrys in ISO3166-2 data object, got {}.".format(len(iso.country.all_iso3166_2_data)))       
        for code in iso.country.all_iso3166_2_data:
            self.assertIn(code, iso.country.alpha2,
                "Alpha-2 code {} not found in list of available 2 letter codes.".format(code))

        #testing class using iso3166-2-min.json file as input
        self.assertIsInstance(iso.subdivisions.alpha2, list, 
            "Expected alpha-2 attribute to be a list, got {}.".format(type(iso.subdivisions.alpha2)))
        self.assertEqual(len(iso.subdivisions.alpha2), 250, 
            "Expected 250 alpha-2 codes, got {}.".format(len(iso.subdivisions.alpha2)))
        self.assertIsInstance(iso.subdivisions.alpha3, list, 
            "Expected alpha3 attribute to be a list, got {}.".format(type(iso.country.alpha3)))
        self.assertEqual(len(iso.subdivisions.alpha3), 250, 
            "Expected 250 alpha3 codes, got {}.".format(len(iso.subdivisions.alpha3)))
        self.assertIsInstance(iso.subdivisions.all_iso3166_2_data, dict,
            "Expected ISO3166-2 data object to be a dict, got {}.".format(type(iso.subdivisions.all_iso3166_2_data)))
        self.assertEqual(len(iso.subdivisions.all_iso3166_2_data), 250, 
            "Expected 250 countrys in ISO3166-2 data object, got {}.".format(len(iso.subdivisions.all_iso3166_2_data)))       
        for code in iso.subdivisions.all_iso3166_2_data:
            self.assertIn(code, iso.subdivisions.alpha2,
                "Alpha-2 code {} not found in list of available 2 letter codes.".format(code))
        
    def test_iso3166_2_json(self):
        """ Testing iso3166-2.json contents and data. """
        test_alpha2_au = iso.country['AU'] #Australia
        test_alpha2_lu = iso.country['LU'] #Luxembourg
        test_alpha2_mg = iso.country["MG"] #Madagascar 
        test_alpha2_om = iso.country["OM"] #Oman
#1.)    
        self.assertIsInstance(test_alpha2_au, dict, "")
        self.assertEqual(len(test_alpha2_au), 35, "")
        self.assertEqual(test_alpha2_au.name.common, "Australia")        
        self.assertEqual(test_alpha2_au.cca2, "AU")        
        self.assertEqual(test_alpha2_au.cca3, "AUS")        
        self.assertEqual(test_alpha2_au.currencies.AUD['name'], "Australian dollar")        
        self.assertEqual(test_alpha2_au.capital[0], "Canberra")        
        self.assertEqual(test_alpha2_au.region, "Oceania")        
        self.assertEqual(list(test_alpha2_au.languages.keys())[0], "eng")        
        self.assertEqual(test_alpha2_au.area, 7692024)        
        self.assertEqual(test_alpha2_au.population, 25687041)        
        self.assertEqual(test_alpha2_au.latlng, [-27.0, 133.0], "")        
        self.assertEqual(len(test_alpha2_au.subdivisions), 8, "")
        self.assertEqual(test_alpha2_au, iso.country['AUS']) #test objects match if using either alpha-2/alpha-3 codes
#2.)
        self.assertIsInstance(test_alpha2_lu, dict, "")
        self.assertEqual(len(test_alpha2_lu), 36, "")
        self.assertEqual(test_alpha2_lu.name.common, "Luxembourg")        
        self.assertEqual(test_alpha2_lu.cca2, "LU")        
        self.assertEqual(test_alpha2_lu.cca3, "LUX")        
        self.assertEqual(test_alpha2_lu.currencies.EUR['name'], "Euro")        
        self.assertEqual(test_alpha2_lu.capital[0], "Luxembourg")        
        self.assertEqual(test_alpha2_lu.region, "Europe")        
        self.assertEqual(list(test_alpha2_lu.languages.keys()), ["deu", "fra", "ltz"])        
        self.assertEqual(test_alpha2_lu.area, 2586)        
        self.assertEqual(test_alpha2_lu.population, 632275)        
        self.assertEqual(len(test_alpha2_lu.subdivisions), 12, "")
        self.assertEqual(test_alpha2_lu.latlng, [49.75, 6.16666666], "")        
        self.assertEqual(test_alpha2_lu, iso.country['LUX']) #test objects match if using either alpha-2/alpha-3 codes
#3.)
        self.assertIsInstance(test_alpha2_mg, dict, "")
        self.assertEqual(len(test_alpha2_mg), 35, "")
        self.assertEqual(test_alpha2_mg.name.common, "Madagascar")        
        self.assertEqual(test_alpha2_mg.cca2, "MG")        
        self.assertEqual(test_alpha2_mg.cca3, "MDG")        
        self.assertEqual(test_alpha2_mg.currencies.MGA['name'], "Malagasy ariary")        
        self.assertEqual(test_alpha2_mg.capital[0], "Antananarivo")        
        self.assertEqual(test_alpha2_mg.region, "Africa")        
        self.assertEqual(list(test_alpha2_mg.languages.keys()), ["fra", "mlg"])        
        self.assertEqual(test_alpha2_mg.area, 587041)        
        self.assertEqual(test_alpha2_mg.population, 27691019)        
        self.assertEqual(test_alpha2_mg.latlng, [-20.0, 47.0], "")        
        self.assertEqual(len(test_alpha2_mg.subdivisions), 6, "")
        self.assertEqual(test_alpha2_mg, iso.country['MDG']) #test objects match if using either alpha-2/alpha-3 codes
#4.)
        self.assertIsInstance(test_alpha2_om, dict, "")
        self.assertEqual(len(test_alpha2_om), 35, "")
        self.assertEqual(test_alpha2_om.name.common, "Oman")        
        self.assertEqual(test_alpha2_om.cca2, "OM")        
        self.assertEqual(test_alpha2_om.cca3, "OMN")        
        self.assertEqual(test_alpha2_om.currencies.OMR['name'], "Omani rial")        
        self.assertEqual(test_alpha2_om.capital[0], "Muscat")        
        self.assertEqual(test_alpha2_om.region, "Asia")        
        self.assertEqual(list(test_alpha2_om.languages.keys()), ["ara"])        
        self.assertEqual(test_alpha2_om.area, 309500)        
        self.assertEqual(test_alpha2_om.population, 5106622)        
        self.assertEqual(test_alpha2_om.latlng, [21.0, 57.0], "")        
        self.assertEqual(len(test_alpha2_om.subdivisions), 11, "")
        self.assertEqual(test_alpha2_om, iso.country['OMN']) #test objects match if using either alpha-2/alpha-3 codes
#5.)
        with (self.assertRaises(ValueError)):
            invalid_country = iso.country["ZZ"]
            invalid_country = iso.country["XY"]
            invalid_country = iso.country["XYZ"]
#6.)
        with (self.assertRaises(TypeError)):
            invalid_country = iso.country[123]
            invalid_country = iso.country[0.5]
            invalid_country = iso.country[False]

    def test_iso3166_2_min_json(self):
        """ Testing minified ISO3166-2 JSON contents and data. """
        test_alpha2_ba = iso.subdivisions["BA"] #Bosnia and Herz
        test_alpha2_cy = iso.subdivisions["CY"] #Cyprus
        test_alpha2_ga = iso.subdivisions["GA"] #Gabon
        test_alpha2_rw = iso.subdivisions["RW"] #Rwanda
#1.)    
        ba_subdivision_codes = ['BA-BIH', 'BA-BRC', 'BA-SRP']
        ba_subdivision_names = ['Federacija Bosne i Hercegovine', 'Brčko distrikt', 'Republika Srpska']
        self.assertIsInstance(test_alpha2_ba, dict)
        self.assertEqual(len(test_alpha2_ba), 3)
        self.assertEqual(list(test_alpha2_ba.keys()), ba_subdivision_codes)
        self.assertEqual(list(test_alpha2_ba['BA-BIH'].keys()), ['name', 'type', 'parent_code', 'latlng', 'flag_url'])
        for key in test_alpha2_ba:
            self.assertIn(test_alpha2_ba[key].name, ba_subdivision_names)
            if ((test_alpha2_ba[key].flag_url is not None) or (test_alpha2_ba[key].flag_url == "")):
                self.assertEqual(requests.get(test_alpha2_ba[key].flag_url, headers=self.user_agent_header).status_code, 200)
            self.assertIsNone(test_alpha2_ba[key]['parent_code'], "")
            self.assertEqual(len(test_alpha2_ba[key].latlng), 2, "")        
#2.)
        cy_subdivision_codes = ['CY-01', 'CY-02', 'CY-03', 'CY-04', 'CY-05', 'CY-06']
        cy_subdivision_names = ['Lefkosia', 'Lemesos', 'Larnaka', 'Ammochostos', 'Baf', 'Girne']
        self.assertIsInstance(test_alpha2_cy, dict)
        self.assertEqual(len(test_alpha2_cy), 6)
        self.assertEqual(list(test_alpha2_cy.keys()), cy_subdivision_codes)
        self.assertEqual(list(test_alpha2_cy['CY-01'].keys()), ['name', 'type', 'parent_code', 'latlng', 'flag_url'])
        for key in test_alpha2_cy:
            self.assertIn(test_alpha2_cy[key].name, cy_subdivision_names)
            if ((test_alpha2_cy[key].flag_url is not None) or (test_alpha2_cy[key].flag_url == "")):
                self.assertEqual(requests.get(test_alpha2_cy[key].flag_url, headers=self.user_agent_header).status_code, 200)
            self.assertIsNone(test_alpha2_cy[key]['parent_code'], "")
            self.assertEqual(len(test_alpha2_cy[key].latlng), 2, "")        
#3.)
        ga_subdivision_codes = ['GA-1', 'GA-2', 'GA-3', 'GA-4', 'GA-5', 'GA-6', 'GA-7', 'GA-8', 'GA-9']
        ga_subdivision_names = ['Estuaire', 'Haut-Ogooué', 'Moyen-Ogooué', 'Ngounié', 'Nyanga', 'Ogooué-Ivindo', 
            'Ogooué-Lolo', 'Ogooué-Maritime', 'Woleu-Ntem']
        self.assertIsInstance(test_alpha2_ga, dict)
        self.assertEqual(len(test_alpha2_ga), 9)
        self.assertEqual(list(test_alpha2_ga.keys()), ga_subdivision_codes)
        self.assertEqual(list(test_alpha2_ga['GA-1'].keys()), ['name', 'type', 'parent_code', 'latlng', 'flag_url'])
        for key in test_alpha2_ga:
            self.assertIn(test_alpha2_ga[key].name, ga_subdivision_names)
            if ((test_alpha2_ga[key].flag_url is not None) or (test_alpha2_ga[key].flag_url == "")):
                self.assertEqual(requests.get(test_alpha2_ga[key].flag_url, headers=self.user_agent_header).status_code, 200)
            self.assertIsNone(test_alpha2_ga[key]['parent_code'], "")
            self.assertEqual(len(test_alpha2_ga[key].latlng), 2, "")        
#4.)
        rw_subdivision_codes = ['RW-01', 'RW-02', 'RW-03', 'RW-04', 'RW-05']
        rw_subdivision_names = ['City of Kigali', 'Eastern', 'Northern', 'Western', 'Southern']
        rw_latlng = [[], [], [], [], []]
        self.assertIsInstance(test_alpha2_rw, dict)
        self.assertEqual(len(test_alpha2_rw), 5)
        self.assertEqual(list(test_alpha2_rw.keys()), rw_subdivision_codes)
        self.assertEqual(list(test_alpha2_rw['RW-01'].keys()), ['name', 'type', 'parent_code', 'latlng', 'flag_url'])
        for key in test_alpha2_rw:
            self.assertIn(test_alpha2_rw[key].name, rw_subdivision_names)
            if ((test_alpha2_rw[key].flag_url is not None) or (test_alpha2_rw[key].flag_url == "")):
                self.assertEqual(requests.get(test_alpha2_rw[key].flag_url, headers=self.user_agent_header).status_code, 200)
        self.assertIsNone(test_alpha2_rw[key]['parent_code'], "")
        self.assertEqual(len(test_alpha2_rw[key].latlng), 2, "")        
#5.)
        with (self.assertRaises(ValueError)):
            invalid_country = iso.subdivisions["ZZ"]
            invalid_country = iso.subdivisions["XY"]
            invalid_country = iso.subdivisions["XYZ"]
#6.)
        with (self.assertRaises(TypeError)):
            invalid_country = iso.subdivisions[123]
            invalid_country = iso.subdivisions[0.5]
            invalid_country = iso.subdivisions[False]

    def test_subdivision_names(self):
        """ Testing functionality for getting list of all ISO3166-2 subdivision names. """
        expected_km_subdivision_names = ['Andjouân', 'Andjazîdja', 'Mohéli']
        expected_er_subdivision_names = ['Ansabā', 'Debubawi K’eyyĭḥ Baḥri', 'Al Janūbī', 'Gash-Barka', 'Al Awsaţ', 'Semienawi K’eyyĭḥ Baḥri']
        expected_gl_subdivision_names = ['Avannaata Kommunia', 'Kommune Kujalleq', 'Qeqqata Kommunia', 'Kommune Qeqertalik', 'Kommuneqarfik Sermersooq']
        expected_vc_subdivision_names = ['Charlotte', 'Saint Andrew', 'Saint David', 'Saint George', 'Saint Patrick', 'Grenadines']
#1.)        
        km_subdivision_names = iso.subdivisions.subdivision_names("KM") #Comoros
        er_subdivision_names = iso.subdivisions.subdivision_names("ER") #Eritrea
        gl_subdivision_names = iso.subdivisions.subdivision_names("GL") #Greenland
        vc_subdivision_names = iso.subdivisions.subdivision_names("VC") #St Vincent

        self.assertEqual(km_subdivision_names, expected_km_subdivision_names, "")
        self.assertEqual(er_subdivision_names, expected_er_subdivision_names, "")
        self.assertEqual(gl_subdivision_names, expected_gl_subdivision_names, "")
        self.assertEqual(vc_subdivision_names, expected_vc_subdivision_names, "")

        self.assertIsInstance(km_subdivision_names, list, "")
        self.assertIsInstance(er_subdivision_names, list, "")
        self.assertIsInstance(gl_subdivision_names, list, "")
        self.assertIsInstance(vc_subdivision_names, list, "")
#2.)   
        km_subdivision_names = iso.country.subdivision_names("KM") #Comoros
        er_subdivision_names = iso.country.subdivision_names("ER") #Eritrea
        gl_subdivision_names = iso.country.subdivision_names("GL") #Greenland
        vc_subdivision_names = iso.country.subdivision_names("VC") #St Vincent

        self.assertEqual(km_subdivision_names, expected_km_subdivision_names, "")
        self.assertEqual(er_subdivision_names, expected_er_subdivision_names, "")
        self.assertEqual(gl_subdivision_names, expected_gl_subdivision_names, "")
        self.assertEqual(vc_subdivision_names, expected_vc_subdivision_names, "")

        self.assertIsInstance(km_subdivision_names, list, "")
        self.assertIsInstance(er_subdivision_names, list, "")
        self.assertIsInstance(gl_subdivision_names, list, "")
        self.assertIsInstance(vc_subdivision_names, list, "")

    def test_subdivision_codes(self):
        """ Testing functionality for getting list of all ISO3166-2 subdivision codes. """
        expected_bq_subdivision_codes = ['BQ-BO', 'BQ-SA', 'BQ-SE']
        expected_sz_subdivision_codes = ['SZ-HH', 'SZ-LU', 'SZ-MA', 'SZ-SH']
        expected_sm_subdivision_codes = ['SM-01', 'SM-02', 'SM-03', 'SM-04', 'SM-05', 'SM-06', 'SM-07', 'SM-08', 'SM-09']
        expected_wf_subdivision_codes = ['WF-AL', 'WF-SG', 'WF-UV']
#1.)        
        bq_subdivision_codes = iso.subdivisions.subdivision_codes("BQ") #Bonaire, Sint Eustatius and Saba
        sz_subdivision_codes = iso.subdivisions.subdivision_codes("SZ") #Eswatini
        sm_subdivision_codes = iso.subdivisions.subdivision_codes("SM") #San Marino
        wf_subdivision_codes = iso.subdivisions.subdivision_codes("WF") #Wallace and Futuna 

        self.assertEqual(bq_subdivision_codes, expected_bq_subdivision_codes, "")
        self.assertEqual(sz_subdivision_codes, expected_sz_subdivision_codes, "")
        self.assertEqual(sm_subdivision_codes, expected_sm_subdivision_codes, "")
        self.assertEqual(wf_subdivision_codes, expected_wf_subdivision_codes, "")

        self.assertIsInstance(bq_subdivision_codes, list, "")
        self.assertIsInstance(sz_subdivision_codes, list, "")
        self.assertIsInstance(sm_subdivision_codes, list, "")
        self.assertIsInstance(wf_subdivision_codes, list, "")
#2.)   
        bq_subdivision_codes = iso.country.subdivision_codes("BQ") #Bonaire, Sint Eustatius and Saba
        sz_subdivision_codes = iso.country.subdivision_codes("SZ") #Eswatini
        sm_subdivision_codes = iso.country.subdivision_codes("SM") #San Marino
        wf_subdivision_codes = iso.country.subdivision_codes("WF") #Wallace and Futuna 

        self.assertEqual(bq_subdivision_codes, expected_bq_subdivision_codes, "")
        self.assertEqual(sz_subdivision_codes, expected_sz_subdivision_codes, "")
        self.assertEqual(sm_subdivision_codes, expected_sm_subdivision_codes, "")
        self.assertEqual(wf_subdivision_codes, expected_wf_subdivision_codes, "")

        self.assertIsInstance(bq_subdivision_codes, list, "")
        self.assertIsInstance(sz_subdivision_codes, list, "")
        self.assertIsInstance(sm_subdivision_codes, list, "")
        self.assertIsInstance(wf_subdivision_codes, list, "")

    def tearDown(self):
        """ Delete all iso3166-2 json objects or instances. """
        del self.all_iso3166_2_data
        del self.all_iso3166_2_min_data
    
if __name__ == '__main__':
    #run all unit tests
    unittest.main(verbosity=2)    