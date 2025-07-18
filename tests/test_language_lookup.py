from scripts.language_lookup import *
import shutil
import requests
import os
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

class Language_Lookup_Tests(unittest.TestCase):
    """
    Test suite for testing the language lookup script & class which generates several 
    export files for each of the languages used in the local/other name attribute.
    The suite also tests the auxiliary functions of the class.

    test_language_lookup:
        testing individual data objects generated from the language lookup function.
    test_language_source_urls: 
        testing that the sources for all language objects are valid.
    test_get_language_data:
        testing function that gets individual language data per input language code.
    test_filter_by_scope:
        testing function that filters the langauge data by scope.
    test_filter_by_type:
        testing function that filters the langauge data by type.
    test_export_language_data: 
        testing exporting the name, scope/category and type of languages from their code.
    test_export_language_lookup:
        testing full language lookup export functionality.
    test_valid_language_codes:
        testing all language codes are valid.
    test_language_exceptions:
        testing all language code exceptions (those not in ISO 639 standard).
    test_country_language_data:
        testing correct language objects are returned per country code. 
    test_language_lookup_search:
        testing searching by language name functionality.
    test_language_lookup_markdown:
        testing validity and format of language lookup markdown file.
    test_language_lookup_csv:
        testing validity and format of language lookup csv file.
    test_add_language_code:
        testing adding a new custom language object from lookup.
    test_delete_language_code:
        testing deleting a language object from lookup.
    test_len:
        testing len() function that gets the total number of language codes in object.
    test_repr:
        testing object representation of class instance.
    test_str:
        testing string object representation of class instance.
    """ 
    @classmethod
    def setUp(self):
        """ Initialise variables and import relevant jsons. """
        self.test_language_lookup_name = "test_language_lookup"
        self.test_directory = os.path.join("tests", "test_files")
        self.test_output_directory = os.path.join("tests", "test_language_lookup")
        self.local_other_names_csv_path = os.path.join(self.test_directory, "test_local_other_names.csv")   

        #create test directory
        if not (os.path.isdir(self.test_output_directory)):
            os.makedirs(self.test_output_directory)

        #instance of Language Lookup class, get all data object 
        self.language_obj = LanguageLookup(imported_file_name=self.local_other_names_csv_path, language_lookup_filename=os.path.join(self.test_directory, self.test_language_lookup_name))
        self.language_lookup = self.language_obj.all_language_data

        #list of glottlog, linguist and IETF language code exceptions
        self.language_code_exceptions = ["algh1238", "berr1239", "bunj1247", "brab1243", "cang1245", "chao1238", "cico1238", "de-at", "east2276", "fuzh1239", 
            "gall1275", "high1290", "79-aaa-gap", "ita-tus", "juri1235", "mila1243", "mone1238", "pera1260", "pala1356", "poit1240-sant1407", "sant1407", 
            "resi1246", "mori1267", "sama1302", "soth1248", "suba1253", "taib1240", "taib1242", "ulst1239", "west2343", "paha1256"
        ]
        # self.language_obj.export_language_lookup(export_filename="language_lookup", export=True)

        #patch sys.stdout such that any print statements/outputs from the individual test cases aren't run
        # self.patcher = patch('sys.stdout', new_callable=io.StringIO)
        # self.mock_stdout = self.patcher.start()

#     @unittest.skip("")
    def test_get_language_data(self):
        """ Testing function for retrieving language data per input code. """
        language_code_jpn = "JPN" #Japanese
        language_code_kaz = "KAZ" #Kazakh
        language_code_kor = "kor" #Korean
        language_code_rus_sgd_sqi = "rus, sgd, sqi" #Russian, Suriganon, Albanian
        language_code_taib1240 = "taib1240" #Taiwanese Mandarin
        language_code_zho = "zho" #Chinese
#1.)
        language_data_jpn = self.language_obj[language_code_jpn]
        expected_language_data_jpn = {'name': 'Japanese', 'scope': 'Individual', 'type': 'Living', "countries": "JP,MH,PW,TW", "total": 75, 'source': "https://iso639-3.sil.org/code/jpn, https://www.loc.gov/standards/iso639-2/php/langcodes_name.php?code_ID=216"}    
        self.assertEqual(language_data_jpn, expected_language_data_jpn, f"Expected and observed language data object do not match: {language_data_jpn}.")
#2.)
        language_data_kaz = self.language_obj[language_code_kaz]
        expected_language_data_kaz = {'name': 'Kazakh', 'scope': 'Individual', 'type': 'Living', "countries": "KZ,RU", "total": 22, 'source': "https://iso639-3.sil.org/code/kaz, https://www.loc.gov/standards/iso639-2/php/langcodes_name.php?code_ID=229"}    
        self.assertEqual(language_data_kaz, expected_language_data_kaz, f"Expected and observed language data object do not match: {language_data_kaz}.")
#3.)
        language_data_kor = self.language_obj[language_code_kor]
        expected_language_data_kor = {'name': 'Korean', 'scope': 'Individual', 'type': 'Living', "countries": "KP,KR,RU", "total": 64, 'source': "https://iso639-3.sil.org/code/kor, https://www.loc.gov/standards/iso639-2/php/langcodes_name.php?code_ID=242"}     
        self.assertEqual(language_data_kor, expected_language_data_kor, f"Expected and observed language data object do not match: {language_data_kor}.")
#4.)
        language_data_rus_sgd_sqi = self.language_obj[language_code_rus_sgd_sqi]
        expected_language_data_rus_sgd_sqi = {"rus": {'name': 'Russian', 'scope': 'Individual', 'type': 'Living', "countries": "BY,GE,HU,KG,KZ,LV,MD,RU,TJ,TM,UA,US,UZ", "total": 185, 'source': "https://iso639-3.sil.org/code/rus, https://www.loc.gov/standards/iso639-2/php/langcodes_name.php?code_ID=379"},
                                              "sgd": {'name': 'Surigaonon', 'scope': 'Individual', 'type': 'Living', "countries": "PH", "total": 2, 'source': "https://iso639-3.sil.org/code/sgd"},
                                              "sqi": {'name': 'Albanian', 'scope': 'Macrolanguage', 'type': 'Living', "countries": "AL,ME,MK,RS,TR", "total": 48, 'source': "https://iso639-3.sil.org/code/sqi, https://www.loc.gov/standards/iso639-2/php/langcodes_name.php?code_ID=14"}}        
        self.assertEqual(language_data_rus_sgd_sqi, expected_language_data_rus_sgd_sqi, f"Expected and observed language data object do not match: {language_data_rus_sgd_sqi}.")
#5.)
        language_data_taib1240 = self.language_obj[language_code_taib1240]
        expected_language_data_taib1240 = {'name': 'Taiwanese Mandarin', 'scope': 'Dialect', 'type': 'Living', 'source': "https://glottolog.org/resource/languoid/id/taib1240", "total": 4, "countries": "TW"}       
        self.assertEqual(language_data_taib1240, expected_language_data_taib1240, f"Expected and observed language data object do not match: {language_data_taib1240}.")
#6.)
        language_data_zho = self.language_obj[language_code_zho]
        expected_language_data_zho = {'name': 'Chinese', 'scope': 'Macrolanguage', 'type': 'Living', 'source': "https://iso639-3.sil.org/code/zho, https://www.loc.gov/standards/iso639-2/php/langcodes_name.php?code_ID=84", "total": 130, "countries": "CN,ID,MY,RU,SG,TH,TW,VN"}        
        self.assertEqual(language_data_zho, expected_language_data_zho, f"Expected and observed language data object do not match: {language_data_zho}.")
#7.)
        with self.assertRaises(ValueError):
            self.language_obj["abb"]
            self.language_obj["dee"]
            self.language_obj["123"]
            self.language_obj["code"]

#     @unittest.skip("")
    def test_filter_by_scope(self):
        """ Testing functionality that allows you to filter the language data by scope. """
#1.)
        test_individual = self.language_obj.filter_by_scope("Individual")
        self.assertEqual(len(test_individual), 366, "Expected there to be 366 language objects with Individual Scope.")
#2.)
        test_macrolanguage = self.language_obj.filter_by_scope("Macrolanguage")
        self.assertEqual(len(test_macrolanguage), 33, "Expected there to be 33 language objects with Macrolanguage Scope.")
#3.)
        test_dialect = self.language_obj.filter_by_scope("Dialect")
        self.assertEqual(len(test_dialect), 24, "Expected there to be 24 language objects with Dialect Scope.")
#4.)
        test_collective = self.language_obj.filter_by_scope("Collective")
        self.assertEqual(len(test_collective), 4, "Expected there to be 4 language objects with Collective Scope.")
#5.)
        test_family = self.language_obj.filter_by_scope("Family")
        self.assertEqual(len(test_family), 4, "Expected there to be 4 language objects with Family Scope.")
#6.)
        test_l1 = self.language_obj.filter_by_scope("Level 1 Language")
        self.assertEqual(len(test_l1), 2, "Expected there to be 2 language objects with Level 1 Language Scope.")
#7.)
        # with self.assertRaises(ValueError):
        #         test_error = self.language_obj.filter_by_scope("abc")
        #         test_error2 = self.language_obj.filter_by_scope("123")
        #         test_error3 = self.language_obj.filter_by_scope("randomScope")

#     @unittest.skip("")
    def test_filter_by_type(self):
        """ Testing functionality that allows you to filter the language data by type. """
#1.)
        test_living = self.language_obj.filter_by_type("Living")
        self.assertEqual(len(test_living), 420, "Expected there to be 420 language objects with Living Type.")
#2.)
        test_extinct = self.language_obj.filter_by_type("Extinct")
        self.assertEqual(len(test_extinct), 5, "Expected there to be 5 language objects with Extinct Type.")
#3.)
        test_ancient = self.language_obj.filter_by_type("Ancient")
        self.assertEqual(len(test_ancient), 2, "Expected there to be 2 language objects with Ancient Type.")
#4.)
        test_historical = self.language_obj.filter_by_type("Historical")
        self.assertEqual(len(test_historical), 6, "Expected there to be 6 language objects with Historical Type.")
#5.)
        test_constructed = self.language_obj.filter_by_type("Constructed")
        self.assertEqual(len(test_constructed), 1, "Expected there to be 1 language object with Constructed Type.")
#6.)
        # with self.assertRaises(ValueError):
        #         test_error = self.language_obj.filter_by_type("abc")
        #         test_error2 = self.language_obj.filter_by_type("123")
        #         test_error3 = self.language_obj.filter_by_type("randomType")

    @unittest.skip("")
    def test_export_language_lookup(self):
        """ Testing the exporting of the full language lookup table to json, csv and markdown files. """
#1.)
        #create new instance of language lookup table class
        lang_lookup = LanguageLookup(imported_file_name=self.local_other_names_csv_path)
        lang_lookup.export_language_lookup(export_filename=os.path.join(self.test_output_directory, "test_language_lookup1"), export=True)

        self.assertTrue(os.path.isfile(os.path.join(self.test_output_directory, "test_language_lookup1.json")), 
                        f"Expected language lookup file to be exported: {os.path.join(self.test_output_directory, 'test_language_lookup1.json')}.")
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_directory, "test_language_lookup1.csv")), 
                    f"Expected language lookup file to be exported: {os.path.join(self.test_output_directory, 'test_language_lookup1.csv')}.")   
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_directory, "test_language_lookup1.md")), 
                    f"Expected language lookup file to be exported: {os.path.join(self.test_output_directory, 'test_language_lookup1.md')}.") 
        self.assertIsNotNone(lang_lookup.all_language_data, "Expected all_language_data object to be populated from function.")
#2.)
        #create new instance of language lookup table class
        lang_lookup = LanguageLookup(imported_file_name=self.local_other_names_csv_path)
        lang_lookup.export_language_lookup(export_filename=os.path.join(self.test_output_directory, "test_language_lookup2"), export=True)

        self.assertTrue(os.path.isfile(os.path.join(self.test_output_directory, "test_language_lookup2.json")), 
                        f"Expected language lookup file to be exported: {os.path.join(self.test_output_directory, 'test_language_lookup2.json')}.")
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_directory, "test_language_lookup2.csv")), 
                    f"Expected language lookup file to be exported: {os.path.join(self.test_output_directory, 'test_language_lookup2.csv')}.")
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_directory, "test_language_lookup2.md")), 
                    f"Expected language lookup file to be exported: {os.path.join(self.test_output_directory, 'test_language_lookup2.md')}.")
        self.assertIsNotNone(lang_lookup.all_language_data, "Expected all_language_data object to be populated from function.")
#3.)
        #create new instance of language lookup table class
        lang_lookup = LanguageLookup(imported_file_name=self.local_other_names_csv_path)
        lang_lookup.export_language_lookup(export_filename=os.path.join(self.test_output_directory, "test_language_lookup3"), export=True)

        self.assertTrue(os.path.isfile(os.path.join(self.test_output_directory, "test_language_lookup3.json")), 
                        f"Expected language lookup file to be exported: {os.path.join(self.test_output_directory, 'test_language_lookup3.json')}.")
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_directory, "test_language_lookup3.csv")), 
                    f"Expected language lookup file to be exported: {os.path.join(self.test_output_directory, 'test_language_lookup3.csv')}.")
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_directory, "test_language_lookup3.md")), 
                    f"Expected language lookup file to be exported: {os.path.join(self.test_output_directory, 'test_language_lookup3.md')}.")
        self.assertIsNotNone(lang_lookup.all_language_data, "Expected all_language_data object to be populated from function.")
#4.)
        #create new instance of language lookup table class
        lang_lookup = LanguageLookup(imported_file_name=self.local_other_names_csv_path)
        lang_lookup.export_language_lookup(export_filename=os.path.join(self.test_output_directory, "test_language_lookup4.json"), export=False)

        self.assertFalse(os.path.isfile(os.path.join(self.test_output_directory, "test_language_lookup4.json")), 
                        f"Expected language lookup file to be exported: {os.path.join(self.test_output_directory, 'test_language_lookup4.json')}.")
        self.assertFalse(os.path.isfile(os.path.join(self.test_output_directory, "test_language_lookup4.csv")), 
                    f"Expected language lookup file to be exported: {os.path.join(self.test_output_directory, 'test_language_lookup4.csv')}.")
        self.assertFalse(os.path.isfile(os.path.join(self.test_output_directory, "test_language_lookup4.md")), 
                    f"Expected language lookup file to be exported: {os.path.join(self.test_output_directory, 'test_language_lookup4.md')}.")
        self.assertIsNotNone(lang_lookup.all_language_data, "Expected all_language_data object to be populated from function.")

#     @unittest.skip("")
    def test_export_language_data(self):
        """ Testing function for exporting the name, scope/category and type of languages from their code. """
        language_code_abk = "abk" #Abkhazian
        language_code_cal = "CAL" #Carolinian
        language_code_fry = "fry" #Western Frisian
        language_code_mri = "mri" #Maori
        language_code_fuzh1239 = "fuzh1239" #Houguan
#1.)
        language_data_abk = self.language_obj.export_language_data(language_code_abk)
        expected_language_data_abk = {'name': 'Abkhazian', 'scope': 'Individual', 'type': 'Living'}
        self.assertEqual(language_data_abk, expected_language_data_abk, f"Expected and observed language data object do not match: {language_data_abk}.")
#2.)
        language_data_cal = self.language_obj.export_language_data(language_code_cal)
        expected_language_data_cal = {'name': 'Carolinian', 'scope': 'Individual', 'type': 'Living'}
        self.assertEqual(language_data_cal, expected_language_data_cal, f"Expected and observed language data object do not match: {language_data_cal}.")
#3.)
        language_data_fry = self.language_obj.export_language_data(language_code_fry)
        expected_language_data_fry = {'name': 'Western Frisian', 'scope': 'Individual', 'type': 'Living'}
        self.assertEqual(language_data_fry, expected_language_data_fry, f"Expected and observed language data object do not match: {language_data_fry}.")
#4.)
        language_data_mri = self.language_obj.export_language_data(language_code_mri)
        expected_language_data_mri = {'name': 'Maori', 'scope': 'Individual', 'type': 'Living'}
        self.assertEqual(language_data_mri, expected_language_data_mri, f"Expected and observed language data object do not match: {language_data_mri}.")
#5.)
        language_data_fuzh1239 = self.language_obj.export_language_data(language_code_fuzh1239)
        expected_language_data_fuzh1239 = {'name': 'Houguan', 'scope': 'Dialect', 'type': 'Living'}
        self.assertEqual(language_data_fuzh1239, expected_language_data_fuzh1239, f"Expected and observed language data object do not match: {language_data_fuzh1239}.")   
#6.)
        with self.assertRaises(ValueError):
            self.language_obj.export_language_data("abb")
            self.language_obj.export_language_data("dee")
            self.language_obj.export_language_data("123")
#7.)
        with self.assertRaises(TypeError):
            self.language_obj.export_language_data(123)
            self.language_obj.export_language_data(40.5)
            self.language_obj.export_language_data(True)

#     @unittest.skip("")
    def test_valid_language_codes(self):
        """ Testing each language code/key of the lookup table is valid. """ 
        #iterate over all language codes, append to list of valid codes
        all_languages = []
        for lang in pycountry.languages:
            if (hasattr(lang, "alpha_2")):
                all_languages.append(lang.alpha_2)
            all_languages.append(lang.alpha_3)
#1.)
        language_exceptions = self.language_code_exceptions
        language_exceptions.extend(["ber", "kar", "nah", "oto", "79-aaa-gap", "de-AT"]) #append language excpetions
        for lang in self.language_obj.all_language_codes:
            #skip language code exceptions including language families and glottolog
            if (lang in language_exceptions):
                continue
            self.assertIn(lang, all_languages, f"Expected language code to be a valid code and in the list of available language codes {lang}.")
            self.assertTrue(len(lang) >= 3, f"Expected all language codes to be minimum 3 characters long, {lang}.")

#     @unittest.skip("")
    def test_language_exceptions(self):
        """ Testing list of language exceptions (those not in ISO 639 standard). """
#1.)
        self.assertEqual(set(self.language_obj.language_exceptions), set(self.language_code_exceptions), 
            f"Expected language code exceptions list do not match:\n{self.language_obj.language_exceptions}.")   

    @unittest.skip("Skipping to not overload test instance.") 
    def test_language_lookup_sources(self):
        """ Testing that the source URLS for all language lookup objects are valid. """
        language_lookup_bcl = "bcl"   #Central Bikol
        language_lookup_cico1238 = "cico1238" #Cicolano-Reatino-Aquilano
        language_lookup_chr = "chr" #Cherokee
        language_lookup_fry = "fry" #western Frisian 
        language_lookup_gil = "gil" #Gilbertese 
#1.)
        # for lang in self.language_lookup:
        #     source_urls = self.language_obj[lang]["source"].split(",")
        #     for url in source_urls:
        #         self.assertEqual(requests.get(url).status_code, 200, f"Expected source URL to be valid, got invalid status code: {url}.")
#2.)
        source_urls_bcl = self.language_obj[language_lookup_bcl]["source"].split(",")
        for url in source_urls_bcl:
            self.assertEqual(requests.get(url).status_code, 200, f"Expected source URL to be valid, got invalid status code: {url}.")
#3.)
        source_urls_cico1238 = self.language_lookup[language_lookup_cico1238]["source"].split(",")
        for url in source_urls_cico1238:
            self.assertEqual(requests.get(url).status_code, 200, f"Expected source URL to be valid, got invalid status code: {url}.")
#4.)
        source_urls_chr = self.language_lookup[language_lookup_chr]["source"].split(",")
        for url in source_urls_chr:
            self.assertEqual(requests.get(url).status_code, 200, f"Expected source URL to be valid, got invalid status code: {url}.")
#5.)
        source_urls_fry = self.language_lookup[language_lookup_fry]["source"].split(",")
        for url in source_urls_fry:
            self.assertEqual(requests.get(url).status_code, 200, f"Expected source URL to be valid, got invalid status code: {url}.")
#6.)
        source_urls_gil = self.language_lookup[language_lookup_gil]["source"].split(",")
        for url in source_urls_gil:
            self.assertEqual(requests.get(url).status_code, 200, f"Expected source URL to be valid, got invalid status code: {url}.")

#     @unittest.skip("") 
    def test_country_language_data(self):
        """ Testing correct language objects are returned from input ISO 3166 country codes. """
        country_language_lookup_cn = "CN" #China
        country_language_lookup_my = "MY" #Malaysia
        country_language_lookup_pk = "PAK" #Pakistan
        country_language_lookup_qa_rs_za = "Qa,SRB,710" #Qatar, Serbia, South Africa
        country_language_lookup_sc = "690" #Seychelles
#1.)
        country_language_lookup_cn_language_data = self.language_obj.get_country_language_data(country_language_lookup_cn)
        country_language_lookup_cn_language_data_expected = ["eng", "fuzh1239", "gan", "hak", "iii", "nan", "uig", "wuu", "zha", "zho"]

        self.assertIsInstance(country_language_lookup_cn_language_data, dict, 
            f"Expected output object of country function to be a dict, got {type(country_language_lookup_cn_language_data)}.")
        self.assertEqual(list(country_language_lookup_cn_language_data.keys()), country_language_lookup_cn_language_data_expected, 
            f"Observed and expected output language codes do not match:\n{list(country_language_lookup_cn_language_data.keys())}.")
#2.)    
        country_language_lookup_my_language_data = self.language_obj.get_country_language_data(country_language_lookup_my)
        country_language_lookup_my_language_data_expected = ['ara', 'eng', 'mcm', 'meo', 'mfa', 'msa', 'nan', 'paha1256', 'pera1260', 'tam', 'tha', 'zho', 'zmi']

        self.assertIsInstance(country_language_lookup_my_language_data, dict, 
            f"Expected output object of country function to be a dict, got {type(country_language_lookup_my_language_data)}.")
        self.assertEqual(list(country_language_lookup_my_language_data.keys()), country_language_lookup_my_language_data_expected, 
            f"Observed and expected output objects do not match:\n{list(country_language_lookup_my_language_data.keys())}.")
#3.)
        country_language_lookup_pk_language_data = self.language_obj.get_country_language_data(country_language_lookup_pk)
        country_language_lookup_pk_language_data_expected = ['eng', 'hnd', 'pus', 'urd']

        self.assertIsInstance(country_language_lookup_pk_language_data, dict, 
            f"Expected output object of country function to be a dict, got {type(country_language_lookup_pk_language_data)}.")
        self.assertEqual(list(country_language_lookup_pk_language_data.keys()), country_language_lookup_pk_language_data_expected, 
            f"Observed and expected output objects do not match:\n{list(country_language_lookup_pk_language_data.keys())}.")
#4.)
        country_language_lookup_qa_rs_za_language_data = self.language_obj.get_country_language_data(country_language_lookup_qa_rs_za)
        country_language_lookup_qa_rs_za_language_data_expected = ['afr', 'ara', 'bunj1247', 'eng', 'hrv', 'hun', 'nbl', 'nso', 'ron', 'rsk', \
                                                                   'slk', 'sot', 'soth1248', 'sqi', 'srp', 'ssw', 'tsn', 'tso', 'ven', 'xho', 'zul']

        self.assertIsInstance(country_language_lookup_qa_rs_za_language_data, dict, 
            f"Expected output object of country function to be a dict, got {type(country_language_lookup_qa_rs_za_language_data)}.")
        self.assertEqual(list(country_language_lookup_qa_rs_za_language_data.keys()), country_language_lookup_qa_rs_za_language_data_expected, 
            f"Observed and expected output objects do not match:\n{list(country_language_lookup_qa_rs_za_language_data.keys())}.")
#5.)
        country_language_lookup_sc_language_data = self.language_obj.get_country_language_data(country_language_lookup_sc)
        country_language_lookup_sc_language_data_expected = ['crs', 'fra']

        self.assertIsInstance(country_language_lookup_sc_language_data, dict, 
            f"Expected output object of country function to be a dict, got {type(country_language_lookup_sc_language_data)}.")
        self.assertEqual(list(country_language_lookup_sc_language_data.keys()), country_language_lookup_sc_language_data_expected, 
            f"Observed and expected output objects do not match:\n{list(country_language_lookup_sc_language_data.keys())}.")
#6.)
        with self.assertRaises(ValueError):
            self.language_obj.get_country_language_data("FR,GB,HU")
            self.language_obj.get_country_language_data("ABC")
            self.language_obj.get_country_language_data("dw")
            self.language_obj.get_country_language_data("123")
#7.)
        with self.assertRaises(TypeError):
            self.language_obj.get_country_language_data(100)
            self.language_obj.get_country_language_data(False)
            self.language_obj.get_country_language_data(2.6)

#     @unittest.skip("")
    def test_language_lookup_search(self):
        """ Testing the search by language name functionality. """
        language_lookup_azerbaijani = "Azerbaijani"
        language_lookup_hebrew = "Hebrew"
        language_lookup_komi = "Komi"
        language_lookup_norwegian = "Norwegian"
        language_lookup_serbian_slovakian = "Serbian, Slovakian"
        language_lookup_invalid1 = "Vulcan"
        language_lookup_invalid2 = "High Valyrian"
        language_lookup_invalid3 = "Simlish"
#1.)
        language_lookup_azerbaijani_language_data = self.language_obj.search_language_lookup(language_lookup_azerbaijani)
        language_lookup_azerbaijani_language_data_expected = {'aze': {'name': 'Azerbaijani', 'scope': 'Macrolanguage', 'type': 'Living', 
            'countries': 'AZ,GE,RU,TR', 'total': 6, 'source': 'https://iso639-3.sil.org/code/aze, https://www.loc.gov/standards/iso639-2/php/langcodes_name.php?code_ID=39'}}

        self.assertEqual(language_lookup_azerbaijani_language_data, language_lookup_azerbaijani_language_data_expected, 
            f"Observed and expected output objects do not match:\n{language_lookup_azerbaijani_language_data}.")
#2.)
        language_lookup_hebrew_language_data = self.language_obj.search_language_lookup(language_lookup_hebrew)
        language_lookup_hebrew_language_data_expected = {'heb': {'name': 'Hebrew', 'scope': 'Individual', 'type': 'Living', 'countries': 'IL,PS', 
            'total': 15, 'source': 'https://iso639-3.sil.org/code/heb, https://www.loc.gov/standards/iso639-2/php/langcodes_name.php?code_ID=184'}}

        self.assertEqual(language_lookup_hebrew_language_data, language_lookup_hebrew_language_data_expected, 
            f"Observed and expected output objects do not match:\n{language_lookup_hebrew_language_data}.")
#3.)
        language_lookup_komi_language_data = self.language_obj.search_language_lookup(language_lookup_komi)
        language_lookup_komi_language_data_expected = {}

        self.assertEqual(language_lookup_komi_language_data, language_lookup_komi_language_data_expected, 
            f"Observed and expected output objects do not match:\n{language_lookup_komi_language_data}.")
#4.)
        #including a likeness score to increase the search space - all Norwegian related languages should return 
        language_lookup_norwegian_language_data = self.language_obj.search_language_lookup(language_lookup_norwegian, likeness_score=70)
        language_lookup_norwegian_language_data_expected = {'nor': {'name': 'Norwegian', 'scope': 'Macrolanguage', 'type': 'Living', 'countries': 'NO', 
            'total': 8, 'source': 'https://iso639-3.sil.org/code/nor, https://www.loc.gov/standards/iso639-2/php/langcodes_name.php?code_ID=331'}, 'nob': 
            {'name': 'Norwegian Bokmål', 'scope': 'Individual', 'type': 'Living', 'countries': 'NO', 'total': 14, 'source': 'https://iso639-3.sil.org/code/nob, https://www.loc.gov/standards/iso639-2/php/langcodes_name.php?code_ID=328'}, 
            'nno': {'name': 'Norwegian Nynorsk', 'scope': 'Individual', 'type': 'Living', 'countries': 'NO', 'total': 2, 'source': 'https://iso639-3.sil.org/code/nno, https://www.loc.gov/standards/iso639-2/php/langcodes_name.php?code_ID=327'}, 
            'kat': {'name': 'Georgian', 'scope': 'Individual', 'type': 'Living', 'countries': 'AZ,GE,TR', 'total': 17, 'source': 'https://iso639-3.sil.org/code/kat, https://www.loc.gov/standards/iso639-2/php/langcodes_name.php?code_ID=158'}}

        self.assertEqual(language_lookup_norwegian_language_data, language_lookup_norwegian_language_data_expected, 
            f"Observed and expected output objects do not match:\n{language_lookup_norwegian_language_data}.")
#5.)
        #including a likeness score to increase the search space
        language_lookup_serbian_language_data = self.language_obj.search_language_lookup(language_lookup_serbian_slovakian, likeness_score=80)
        language_lookup_serbian_language_data_expected = {'srp': {'name': 'Serbian', 'scope': 'Individual', 'type': 'Living', 'countries': 'BA,HU,ME,RO,RS', 'total': 43, 'source': 'https://iso639-3.sil.org/code/srp, https://www.loc.gov/standards/iso639-2/php/langcodes_name.php?code_ID=390'}, 
            'slk': {'name': 'Slovak', 'scope': 'Individual', 'type': 'Living', 'countries': 'AT,HU,RO,RS', 'total': 28, 'source': 'https://iso639-3.sil.org/code/slk, https://www.loc.gov/standards/iso639-2/php/langcodes_name.php?code_ID=406'}}

        self.assertEqual(language_lookup_serbian_language_data, language_lookup_serbian_language_data_expected, 
            f"Observed and expected output objects do not match:\n{language_lookup_serbian_language_data}.")
#6.)
        self.assertEqual(self.language_obj.search_language_lookup(language_lookup_invalid1), {}, "Expected no language lookup search results.")
        self.assertEqual(self.language_obj.search_language_lookup(language_lookup_invalid2), {}, "Expected no language lookup search results.")
        self.assertEqual(self.language_obj.search_language_lookup(language_lookup_invalid3), {}, "Expected no language lookup search results.")
#7.)
        language_lookup_instance = LanguageLookup(language_lookup_filename="")
        with self.assertRaises(ValueError):
            language_lookup_instance.search_language_lookup(language_lookup_invalid1)
            language_lookup_instance.search_language_lookup(language_lookup_invalid2)
            language_lookup_instance.search_language_lookup(language_lookup_invalid3)
#8.)
        with self.assertRaises(TypeError):
            self.language_obj.search_language_lookup(123)
            self.language_obj.search_language_lookup(False)
            self.language_obj.search_language_lookup(82.6)

#     @unittest.skip("")
    def test_language_lookup_markdown(self):
        """ Testing exported markdown language lookup table. """
        #read in markdown file for testing
        with open(os.path.join("tests", "test_files", "test_language_lookup.md"), 'r', encoding='utf-8', errors='ignore') as file:
            markdown_content = file.read()

        #extract rows
        lines = [line.strip() for line in markdown_content.strip().splitlines() if line.strip().startswith("|")]
        if len(lines) < 2:
            return [], []

        #extract headers
        header = [col.strip() for col in lines[0].strip("|").split("|")]
        rows = []

        #iterate over each row in markdown, extracting rows
        for line in lines[2:]:  # skip header and separator
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) == len(header):
                rows.append(dict(zip(header, cells)))
#1.)
        self.assertIsNotNone(rows, "Expected markdown table to not be None.")
#2.)
        expected_headers = ['code', 'name', 'scope', 'type', 'countries', 'total', 'source']
        self.assertEqual(header, expected_headers, f"Expected and observed table headers do not match: {header}.")
#3.)
        self.assertEqual(len(rows), 434, f"Expected 434 data rows in the markdown table, got {len(rows)}.")
#4.)
        #testing there are no empty cells in table
        for i, row in enumerate(rows, start=1):
            for key, val in row.items():
                if (key == "countries"): #countries attribute can be empty
                    continue
                self.assertTrue(val, f"Expected no cells to be empty, found empty value found in row {i}:\n'{row}'.")
#5.)
        #testing no duplicates
        seen = set()
        duplicates = []
        for row in rows:
            row_tuple = tuple(row.items())
            if row_tuple in seen:
                duplicates.append(row)
            seen.add(row_tuple)
        self.assertEqual(len(duplicates), 0, f"Duplicate rows found:\n{duplicates}")
#6.)
        #testing valid language scope & types
        valid_scopes = {"Individual", "Dialect", "Macrolanguage", "Special", "Collective", "Family", "Level 1 Language", "Artificial"}
        valid_types = {"Living", "Extinct", "Ancient", "Constructed", "Historical", "Special"}

        for i, row in enumerate(rows, start=1):
            self.assertIn(row["scope"], valid_scopes, f"Unexpected scope in row {i}: {row['scope']}")
            self.assertIn(row["type"], valid_types, f"Unexpected type in row {i}: {row['type']}")
#7.)
        #testing all country codes are valid in countries column
        valid_country_codes = list(iso3166.countries_by_alpha2.keys())
        for i, row in enumerate(rows, start=1):
            countries_field = row["countries"].strip()
            if not countries_field:
                continue  #skip if empty
            codes = [code.strip() for code in countries_field.split(",")]
            for code in codes:
                self.assertIn(code, valid_country_codes, f"Invalid country code '{code}' in row {i}:\n{row}")
#8.)
        #testing individual language rows/objects
        test_row_1 = rows[40]
        expected_test_row_1 = {'code': 'brab1243', 'name': 'Brabantian', 'scope': 'Dialect', 'type': 'Living', 'countries': 'NL', 'total': '1', 
                               'source': 'https://glottolog.org/resource/languoid/id/brab1243'}
        self.assertEqual(test_row_1, expected_test_row_1, f"Expected and observed language code data do not match:\n{test_row_1}.")

        test_row_2 = rows[57]
        expected_test_row_2 = {'code': 'chao1238', 'name': 'Teochew Min', 'scope': 'Dialect', 'type': 'Living', 'countries': 'TH', 'total': '7', 
                               'source': 'https://glottolog.org/resource/languoid/id/chao1238'}
        self.assertEqual(test_row_2, expected_test_row_2, f"Expected and observed language code data do not match:\n{test_row_2}.")

        test_row_3 = rows[71]
        expected_test_row_2 = {'code': 'crb', 'name': 'Island Carib', 'scope': 'Individual', 'type': 'Extinct', 'countries': 'FR,TT', 'total': '4', 
                               'source': 'https://iso639-3.sil.org/code/crb'}
        self.assertEqual(test_row_3, expected_test_row_2, f"Expected and observed language code data do not match:\n{test_row_3}.")

        test_row_4 = rows[82]
        expected_test_row_4 = {'code': 'deu', 'name': 'German', 'scope': 'Individual', 'type': 'Living', 'countries': 'BE,CH,DE,DK,EE,FR,HU,IT,LT,LU,LV,NL,PG,RO,SI,SK', 'total': '99', 
                               'source': 'https://iso639-3.sil.org/code/deu, https://www.loc.gov/standards/iso639-2/php/langcodes_name.php?code_ID=160'}
        self.assertEqual(test_row_4, expected_test_row_4, f"Expected and observed language code data do not match:\n{test_row_4}.")

        test_row_5 = rows[212]
        expected_test_row_5 = {'code': 'liv', 'name': 'Liv', 'scope': 'Individual', 'type': 'Living', 'countries': 'LV', 'total': '5', 
                               'source': 'https://iso639-3.sil.org/code/liv'}
        self.assertEqual(test_row_5, expected_test_row_5, f"Expected and observed language code data do not match:\n{test_row_5}.")
    
#     @unittest.skip("")
    def test_language_lookup_csv(self):
        """ Testing exported csv language lookup table. """
        #read in csv file for testing
        language_lookup_csv = pd.read_csv(os.path.join("tests", "test_files", "test_language_lookup.csv"), keep_default_na=False)
#1.)
        expected_columns = {"code", "name", "scope", "type", "source", "countries", "total"}
        self.assertEqual(set(language_lookup_csv.columns), expected_columns, f"Expected and observed columns do not match:\n{set(language_lookup_csv.columns)}.")
#2.)
        self.assertEqual(len(language_lookup_csv), 434, f"Expected 434 data rows in the CSV, got {len(language_lookup_csv)}.")
#3.)
        for col in ["code", "name", "scope", "type", "source", "total"]:
            self.assertFalse(language_lookup_csv[col].isnull().any(), f"Null values found in column: {col}")
#4.)
        #testing valid language scope & types
        valid_scopes = {"Individual", "Dialect", "Macrolanguage", "Special", "Collective", "Family", "Level 1 Language", "Artificial"}
        valid_types = {"Living", "Extinct", "Ancient", "Constructed", "Historical", "Special"}

        self.assertTrue(language_lookup_csv["scope"].isin(valid_scopes).all(), "Invalid scope values found in CSV.")
        self.assertTrue(language_lookup_csv["type"].isin(valid_types).all(), "Invalid type values found in CSV.")
#5.)
        #testing all country codes are valid in countries column
        valid_codes = set(iso3166.countries_by_alpha2.keys())
        for i, countries in enumerate(language_lookup_csv["countries"]):
            if pd.isna(countries) or countries.strip() == "":
                continue
            codes = [code.strip() for code in countries.split(",")]
            for code in codes:
                self.assertIn(code, valid_codes,  f"Invalid country code '{code}' in row {i}:\n{language_lookup_csv.iloc[i].to_dict()}")
#6.)
        #ensure there are no duplicate language codes
        duplicates = language_lookup_csv["code"][language_lookup_csv["code"].duplicated()].tolist()
        self.assertEqual(len(duplicates), 0, f"Duplicate language codes found: {duplicates}")  
#7.)
        #testing individual language rows/objects
        test_row_1 = language_lookup_csv[language_lookup_csv["code"] == "crb"].iloc[0].to_dict()
        expected_test_row_1 = {'code': 'crb', 'name': 'Island Carib', 'scope': 'Individual', 'type': 'Extinct', 'countries': 'FR,TT', 'total': 4, 
                               'source': 'https://iso639-3.sil.org/code/crb'}
        self.assertEqual(test_row_1, expected_test_row_1, f"Expected and observed language code data do not match:\n{test_row_1}.")

        test_row_2 = language_lookup_csv[language_lookup_csv["code"] == "fkv"].iloc[0].to_dict()
        expected_test_row_2 = {'code': 'fkv', 'name': 'Kven Finnish', 'scope': 'Individual', 'type': 'Living', 'countries': 'NO', 'total': 1, 
                               'source': 'https://iso639-3.sil.org/code/fkv'}
        self.assertEqual(test_row_2, expected_test_row_2, f"Expected and observed language code data do not match:\n{test_row_2}.")

        test_row_3 = language_lookup_csv[language_lookup_csv["code"] == "ita-tus"].iloc[0].to_dict()
        expected_test_row_3 = {'code': 'ita-tus', 'name': 'Tuscan', 'scope': 'Dialect', 'type': 'Living', 'countries': 'IT', 'total': 1, 
                               'source': 'https://web.archive.org/web/20221015065035/http://multitree.org/codes/ita-tus'}
        self.assertEqual(test_row_3, expected_test_row_3, f"Expected and observed language code data do not match:\n{test_row_3}.")

        test_row_4 = language_lookup_csv[language_lookup_csv["code"] == "mori1267"].iloc[0].to_dict()
        expected_test_row_4 = {'code': 'mori1267', 'name': 'Moriori', 'scope': 'Level 1 Language', 'type': 'Living', 'countries': 'NZ', 'total': 1, 
                               'source': 'https://glottolog.org/resource/languoid/id/mori1267'}
        self.assertEqual(test_row_4, expected_test_row_4, f"Expected and observed language code data do not match:\n{test_row_4}.")

        test_row_5 = language_lookup_csv[language_lookup_csv["code"] == "nya"].iloc[0].to_dict()
        expected_test_row_5 = {'code': 'nya', 'name': 'Nyanja', 'scope': 'Individual', 'type': 'Living', 'countries': 'MW', 'total': 31, 
                               'source': 'https://iso639-3.sil.org/code/nya, https://www.loc.gov/standards/iso639-2/php/langcodes_name.php?code_ID=335'}
        self.assertEqual(test_row_5, expected_test_row_5, f"Expected and observed language code data do not match:\n{test_row_5}.")

#     @unittest.skip("")
    def test_add_language_code(self):
        """ Testing adding a new language to the language lookup. """
        language_lookup_clingon = {"code": "CLI", "name": "Clingon", "scope": "Individual", "type": "Artificial", "countries": "GB, IE", "total": 0, "source": ""}
        language_lookup_elvish = {"code": "ELV", "name": "Elvish", "scope": "Individual", "type": "Artificial", "source": ""}
        language_lookup_furbish = {"code": "FIR", "name": "Furbish", "scope": "Individual", "type": "Artificial"}
#1.)    
        self.language_obj.add_language_code(language_lookup_clingon, export=False)
        
        language_lookup_clingon_expected = {'name': 'Clingon', 'scope': 'Individual', 'type': 'Artificial', 'countries': 'GB, IE', 'total': 0, 'source': ''}
        self.assertEqual(language_lookup_clingon_expected, self.language_obj["CLI"], f"Expected Clingon language object to be in main language lookup table:\n{language_lookup_clingon}.")
        self.assertIn("cli", self.language_obj.all_language_codes, "Expected new cli language code to be in all_language_codes object.")
#2.)
        self.language_obj.add_language_code(language_lookup_elvish, export=False)
        language_lookup_elvish_expected = {"name": "Elvish", "scope": "Individual", "type": "Artificial", "countries": "", "total": 0,  "source": ""}
        self.assertEqual(language_lookup_elvish_expected, self.language_obj["ELV"], f"Expected Elvish language object to be in main language lookup table:\n{language_lookup_clingon}.")
        self.assertIn("elv", self.language_obj.all_language_codes, "Expected new elv language code to be in all_language_codes object.")
#3.)
        self.language_obj.add_language_code(language_lookup_furbish, export=False)
        language_lookup_furbish_expected = {"name": "Furbish", "scope": "Individual", "type": "Artificial", "countries": "", "total": 0, "source": ""}
        self.assertEqual(language_lookup_furbish_expected, self.language_obj["FIR"], f"Expected Furbish language object to be in main language lookup table:\n{language_lookup_furbish}.")
        self.assertIn("fir", self.language_obj.all_language_codes, "Expected new fur language code to be in all_language_codes object.")
#4.)
        self.language_obj.add_language_code(name="Ewokese", code="EWK", export=False)
        language_lookup_ewokese_expected = {"name": "Ewokese", "scope": "", "type": "", "countries": "", "total": 0, "source": ""}
        self.assertEqual(language_lookup_ewokese_expected, self.language_obj["EWK"], f"Expected Ewokese language object to be in main language lookup table:\n{language_lookup_ewokese_expected}.")
        self.assertIn("ewk", self.language_obj.all_language_codes, "Expected new ewk language code to be in all_language_codes object.")
#5.)
        self.language_obj.add_language_code(name="Simlish", code="SIM", export=False)
        language_lookup_simlish_expected = {"name": "Simlish", "scope": "", "type": "", "countries": "", "total": 0, "source": ""}
        self.assertEqual(language_lookup_simlish_expected, self.language_obj["SIM"], f"Expected Simlish language object to be in main language lookup table:\n{language_lookup_simlish_expected}.")
        self.assertIn("sim", self.language_obj.all_language_codes, "Expected new sim language code to be in all_language_codes object.")
#6.)
        with self.assertRaises(ValueError):
            self.language_obj.add_language_code()
            self.language_obj.add_language_code(name="abc")
            self.language_obj.add_language_code(code="abc")
            self.language_obj.add_language_code(name="abc", code="")
            self.language_obj.add_language_code(new_language_object={}, name="new language", code="")
#7.)
        with self.assertRaises(TypeError):
            self.language_obj.add_language_code(name="name1", code=123)
            self.language_obj.add_language_code(code=56.8)
            self.language_obj.add_language_code(name=False)

#     @unittest.skip("")
    def test_delete_language_code(self):
        """ Testing deletion of language code from the language lookup. """
#1.)
        self.language_obj.delete_language_code("deu", export=False)
        self.assertNotIn("deu", self.language_obj.all_language_data)
        self.assertNotIn("deu", self.language_obj.all_language_codes)
#2.)
        self.language_obj.delete_language_code("ibo", export=False)
        self.assertNotIn("ibo", self.language_obj.all_language_data)
        self.assertNotIn("ibo", self.language_obj.all_language_codes)
#3.)
        self.language_obj.delete_language_code("jje", export=False)
        self.assertNotIn("jje", self.language_obj.all_language_data)
        self.assertNotIn("jje", self.language_obj.all_language_codes)
#4.)
        self.language_obj.delete_language_code("mila1243", export=False)
        self.assertNotIn("mila1243", self.language_obj.all_language_data)
        self.assertNotIn("mila1243", self.language_obj.all_language_codes)
#5.)
        self.language_obj.delete_language_code("olo", export=False)
        self.assertNotIn("olo", self.language_obj.all_language_data)
        self.assertNotIn("olo", self.language_obj.all_language_data)
#6.)
        with self.assertRaises(ValueError):
            self.language_obj.delete_language_code("aaa", export=False)
            self.language_obj.delete_language_code("123", export=False)
            self.language_obj.delete_language_code("zzz", export=False)

    # @unittest.skip("")
    def test_len(self):
        """ Testing len() class function that outputs total number of languages. """
        self.assertEqual(len(self.language_obj), 434, 
            f"Expected and observed total number of language codes do not match:\n{len(self.language_obj)}.")

    # @unittest.skip("")
    def test_str(self):
        """ Testing string representation of class instance. """
        self.assertEqual(str(self.language_obj), f"LanguageLookup instance with 434 languages from 'tests/test_files/test_language_lookup'.", 
            f"Expected and observed string representation of object does not match:\n{str(self.language_obj)}.")

    # @unittest.skip("")
    def test_repr(self):
        """ Testing object representation of class instance. """
        self.assertEqual(repr(self.language_obj), f"<LanguageLookup(file='tests/test_files/test_language_lookup', languages=434)>", 
            f"Expected and observed representation of object does not match:\n{repr(self.language_obj)}.")

    @classmethod
    def tearDown(self):
        """ Remove any temporary test folders/files. """
        shutil.rmtree(self.test_output_directory) 