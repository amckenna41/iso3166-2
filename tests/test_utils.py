from scripts.utils import *
import shutil
import os
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

# @unittest.skip("Skipping utils unit tests.")
class Utils_Tests(unittest.TestCase):
    """
    Test suite for testing the utilities module that consists of various functions
    used throughout the software.

    test_convert_to_alpha2:
        testing functionality that converts any ISO 3166 alpha code into its alpha-2
        counterpart.
    test_split_preserving_quotes:
        testing function that splits a list of elements, ensuring any single quotes
        are preserved.
    test_get_flag_repo_url:
        testing functionality that gets the subdivision's flag from the 
        iso3166-flag-icons repo. 
    test_attributes_memory_usage:
        testing functionality that extracts the memory usage per attribute
        and country object within the JSON.
    test_is_latin:
        testing function that checks if an individual character is a latin
        or non-latin character.
    test_only_roman_chars:
        testing function that checks if a string contains just roman chars.
    test_get_flag_icons_url:
        testing auxiliary function used for getting the flag URL of a subdivision from the 
        iso3166-flag-icons repo.
    test_add_history:
        testing utilities function that adds the subdivision's historical data to the output.
    test_export_iso3166_2_data:
        testing utilities function that exports the subdivision data to the output files/folder.
    """ 
    @classmethod
    def setUp(self):
        """ Initialise variables and create test directories. """
        #test output folder for utils function
        self.test_utils_folder = os.path.join("tests", "test_iso3166_2_utils")
        if not (os.path.isdir(self.test_utils_folder)):
            os.makedirs(self.test_utils_folder)

        #path to test ISO 3166-2 json file
        self.test_iso3166_2_json = os.path.join("tests", "test_files", "test_iso3166-2.json")

    # @unittest.skip("")
    def test_convert_to_alpha2(self):
        """ Testing correct alpha-2 codes are output from input data. """
        test_alpha_bh = "BH" #Bahrain
        test_alpha_dj = "DJI" #Djibouti
        test_alpha_gr = "grc" #Greece
        test_alpha_ie = "372" #Ireland
        test_alpha_bh_dj_gr = "BJ, DJI, GRC"
        test_alpha_invalid1 = "ZZ"
        test_alpha_invalid2 = "ABC"
#1.)
        test_alpha_bh_converted = convert_to_alpha2(test_alpha_bh)
        self.assertEqual(test_alpha_bh_converted, "BH", f"Expected and observed alpha code do not match, got {test_alpha_bh_converted}.")
#2.)
        test_alpha_dj_converted = convert_to_alpha2(test_alpha_dj)
        self.assertEqual(test_alpha_dj_converted, "DJ", f"Expected and observed alpha code do not match, got {test_alpha_dj_converted}.")
#3.)
        test_alpha_gr_converted = convert_to_alpha2(test_alpha_gr)
        self.assertEqual(test_alpha_gr_converted, "GR", f"Expected and observed alpha code do not match, got {test_alpha_gr_converted}.")
#4.)
        test_alpha_ie_converted = convert_to_alpha2(test_alpha_ie)
        self.assertEqual(test_alpha_ie_converted, "IE", f"Expected and observed alpha code do not match, got {test_alpha_ie_converted}.")
#5.)
        with self.assertRaises(ValueError):
            convert_to_alpha2(test_alpha_bh_dj_gr)
            convert_to_alpha2(test_alpha_invalid1)
            convert_to_alpha2(test_alpha_invalid2)
#6.)
        with self.assertRaises(TypeError):
            convert_to_alpha2(123)
            convert_to_alpha2(9.02)
            convert_to_alpha2(False)

    # @unittest.skip("")
    def test_split_preserving_quotes(self):
        """ Testing the functions that splits list of elements in a string, preserving single quoted element. """
        test_name1 = "'Bruxelles-Capitale, Région de (fra)', Brussels-Capital Region (eng), Brussel (nld), Brussels (eng)"
        test_name2 = "'Distrito Capital (spa), Bogotá, D.C. (spa)', Santa Fe de Bogotá (spa)"
        test_name3 = "'Ard Mhacha, Droichead na Banna agus Creag Abhann (gle)', 'Airmagh, Bannbrig an Craigavon (ulst1239)'"
        test_name4 = "'Iúr Cinn Trá, Múrna agus An Dún (gle)', 'Newrie, Morne an Doon (ulst1239)'"
        test_name5 = "Bunker Island (eng), Bunkers Shoal (eng)" #output should equal input
#1.) 
        test_name1_output = split_preserving_quotes(test_name1)

        expected_test_name1_output = ['Bruxelles-Capitale, Région de (fra)', 'Brussels-Capital Region (eng)', 'Brussel (nld)', 'Brussels (eng)']
        self.assertEqual(test_name1_output, expected_test_name1_output, 
            f"Expected and observed function outputs do not match:\n{test_name1_output}.")
#2.) 
        test_name2_output = split_preserving_quotes(test_name2)

        expected_test_name2_output = ['Distrito Capital (spa), Bogotá, D.C. (spa)', 'Santa Fe de Bogotá (spa)']
        self.assertEqual(test_name2_output, expected_test_name2_output, 
            f"Expected and observed function outputs do not match:\n{test_name2_output}.")
#3.) 
        test_name3_output = split_preserving_quotes(test_name3)

        expected_test_name3_output = ['Ard Mhacha, Droichead na Banna agus Creag Abhann (gle)', 'Airmagh, Bannbrig an Craigavon (ulst1239)']
        self.assertEqual(test_name3_output, expected_test_name3_output, 
            f"Expected and observed function outputs do not match:\n{test_name3_output}.")
#4.) 
        test_name4_output = split_preserving_quotes(test_name4)

        expected_test_name4_output = ['Iúr Cinn Trá, Múrna agus An Dún (gle)', 'Newrie, Morne an Doon (ulst1239)']
        self.assertEqual(test_name4_output, expected_test_name4_output, 
            f"Expected and observed function outputs do not match:\n{test_name4_output}.")
#4.) 
        test_name5_output = split_preserving_quotes(test_name5)

        expected_test_name5_output = ["Bunker Island (eng)", "Bunkers Shoal (eng)"]
        self.assertEqual(test_name5_output, expected_test_name5_output, 
            f"Expected and observed function outputs do not match:\n{test_name5_output}.")
#5.)
        with self.assertRaises(TypeError):
            split_preserving_quotes(123)
            split_preserving_quotes(True)
            split_preserving_quotes(80.924)
            split_preserving_quotes(["A", "B", "C"])

    # @unittest.skip("")
    def test_get_flag_repo_url(self):
        """ Testing function that gets the URL for each subdivision  flag. """
        test_alpha_subdivision_1 = "GB-ENF" #Enfield
        test_alpha_subdivision_2 = "IT-BO" #Bologna
        test_alpha_subdivision_3 = "NL-AW" #Aruba
        test_alpha_subdivision_4 = "PL-18" #Podkarpackie
        test_alpha_subdivision_5 = "SH" #Shabeellaha Hoose (just using RHS of subdivision code)
        test_alpha_subdivision_6 = "AB-ABC" #None
        test_alpha_subdivision_7 = "123" #None
#1.)    
        test_alpha_subdivision_1_flag_url = get_flag_repo_url("GB", test_alpha_subdivision_1)
        expected_flag_url = "https://raw.githubusercontent.com/amckenna41/iso3166-flag-icons/main/iso3166-2-icons/GB/GB-ENF.svg"
        self.assertEqual(test_alpha_subdivision_1_flag_url, expected_flag_url, f"Expected and observed flag for GB-ENF do not match:\n{test_alpha_subdivision_1_flag_url}.")
#2.)
        test_alpha_subdivision_2_flag_url = get_flag_repo_url("IT", test_alpha_subdivision_2)
        expected_flag_url = "https://raw.githubusercontent.com/amckenna41/iso3166-flag-icons/main/iso3166-2-icons/IT/IT-BO.svg"
        self.assertEqual(test_alpha_subdivision_2_flag_url, expected_flag_url, f"Expected and observed flag for IT-BO do not match:\n{test_alpha_subdivision_2_flag_url}.")
#3.)
        test_alpha_subdivision_3_flag_url = get_flag_repo_url("NL", test_alpha_subdivision_3)
        expected_flag_url = "https://raw.githubusercontent.com/amckenna41/iso3166-flag-icons/main/iso3166-2-icons/NL/NL-AW.svg"
        self.assertEqual(test_alpha_subdivision_3_flag_url, expected_flag_url, f"Expected and observed flag for NL-AW do not match:\n{test_alpha_subdivision_3_flag_url}.")
#4.)
        test_alpha_subdivision_4_flag_url = get_flag_repo_url(alpha2_code="PL", subdivision_code=test_alpha_subdivision_4)
        expected_flag_url = "https://raw.githubusercontent.com/amckenna41/iso3166-flag-icons/main/iso3166-2-icons/PL/PL-18.svg"
        self.assertEqual(test_alpha_subdivision_4_flag_url, expected_flag_url, f"Expected and observed flag for PL-18 do not match:\n{test_alpha_subdivision_4_flag_url}.")
#5.)
        test_alpha_subdivision_5_flag_url = get_flag_repo_url(alpha2_code="SO", subdivision_code=test_alpha_subdivision_5)
        expected_flag_url = "https://raw.githubusercontent.com/amckenna41/iso3166-flag-icons/main/iso3166-2-icons/SO/SO-SH.svg"
        self.assertEqual(test_alpha_subdivision_5_flag_url, expected_flag_url, f"Expected and observed flag for SO-SH do not match:\n{test_alpha_subdivision_5_flag_url}.")
#6.)
        test_alpha_subdivision_6_flag_url = get_flag_repo_url(alpha2_code="AB", subdivision_code=test_alpha_subdivision_6)
        self.assertIsNone(test_alpha_subdivision_6_flag_url, f"Expected flag url output for AB-ABC to be None:\n{test_alpha_subdivision_6_flag_url}.")
#7.)
        test_alpha_subdivision_7_flag_url = get_flag_repo_url(alpha2_code="DE", subdivision_code=test_alpha_subdivision_7)
        self.assertIsNone(test_alpha_subdivision_7_flag_url, f"Expected flag url output for DE-123 to be None:\n{test_alpha_subdivision_7_flag_url}.")
#8.)
        with self.assertRaises(ValueError):
            get_flag_repo_url(alpha2_code="AA", subdivision_code="01")
            get_flag_repo_url(alpha2_code="BB", subdivision_code="BA")
            get_flag_repo_url(alpha2_code="", subdivision_code="ZZZ")
#9.)
        with self.assertRaises(TypeError):
            get_flag_repo_url(False)
            get_flag_repo_url(123)
            get_flag_repo_url(123.456)

    # @unittest.skip("")
    def test_attributes_memory_usage(self):
        """ Testing function that calculates the attribute/country object memory usage. 
        """
        attributes_memory_usage(iso3166_2_json_filepath=os.path.join("iso3166_2", "iso3166-2.json"), 
            export_folder=self.test_utils_folder, country_level_usage=True)
        attribute_memory_usage_df = pd.read_csv(os.path.join(self.test_utils_folder, "iso3166_2_attribute_memory_usage.csv"), keep_default_na=False)
        country_object_memory_usage_df = pd.read_csv(os.path.join(self.test_utils_folder, "iso3166_2_country_object_memory_usage.csv"), keep_default_na=False)
#1.)
        self.assertTrue(os.path.isfile(os.path.join(self.test_utils_folder, "iso3166_2_attribute_memory_usage.csv")), 
            f"Expected output csv of memory usage to be in test folder:\n{os.path.join(self.test_utils_folder, 'iso3166_2_attribute_memory_usage.csv')}.")
        self.assertTrue(os.path.isfile(os.path.join(self.test_utils_folder, "iso3166_2_country_object_memory_usage.csv")), 
            f"Expected output csv of memory usage to be in test folder:\n{os.path.join(self.test_utils_folder, 'iso3166_2_country_object_memory_usage.csv')}.")
#2.)
        self.assertEqual(list(attribute_memory_usage_df.columns), ["Attribute", "Size (KB)", "Percentage (%)"], f"Expected and observed columns of dataframe do not match:\n{attribute_memory_usage_df.columns}.")
        self.assertEqual(list(country_object_memory_usage_df.columns), ["Country Code", "Size (KB)", "Percentage (%)"], f"Expected and observed columns of dataframe do not match:\n{attribute_memory_usage_df.columns}.")
        self.assertEqual(len(attribute_memory_usage_df), 7, f"Expected there to be 7 rows in the output dataframe, got {len(attribute_memory_usage_df)}.")
        self.assertEqual(len(country_object_memory_usage_df), 250, f"Expected there to be 250 rows in the output dataframe, got {len(country_object_memory_usage_df)}.")
#3.)
        expected_types_attribute_memory_usage = {"Attribute": str, "Size (KB)": float, "Percentage (%)": float}
        expected_types_country_object_memory_usage = {"Country Code": str, "Size (KB)": float, "Percentage (%)": float}

        for column, expected_type in expected_types_attribute_memory_usage.items():
            incorrect_row_types = attribute_memory_usage_df[~attribute_memory_usage_df[column].map(type).eq(expected_type)]
            self.assertTrue(incorrect_row_types.empty, f"Expected all rows for column {column} to be of the expected data type. Here are the invalid rows:\n{incorrect_row_types}")
        
        for column, expected_type in expected_types_country_object_memory_usage.items():  
            incorrect_row_types = country_object_memory_usage_df[~country_object_memory_usage_df[column].map(type).eq(expected_type)]
            self.assertTrue(incorrect_row_types.empty, f"Expected all rows for column {column} to be of the expected data type. Here are the invalid rows:\n{incorrect_row_types}")
#4.)
        expected_attribute_memory_usage_df = pd.DataFrame({
            'Attribute': ['flag', 'latLng', 'localName', 'name', 'parentCode', 'type'],
            'Size (KB)': [486.921875, 299.924805, 303.771484, 279.176758, 264.918945, 270.393555],
            'Percentage (%)': [44.542632, 27.436517, 27.788404, 25.538528, 24.234252, 24.735058]
        })
        expected_rows_attribute_memory_usage_range = [
            {'Attribute': 'flag', 'Size (KB)': (486.8, 487.1), 'Percentage (%)': (44.53, 44.56)},
            {'Attribute': 'latLng', 'Size (KB)': (299.8, 300.1), 'Percentage (%)': (27.42, 27.45)},
            {'Attribute': 'localName', 'Size (KB)': (303.7, 303.9), 'Percentage (%)': (27.77, 27.80)},
            {'Attribute': 'name', 'Size (KB)': (279.1, 279.3), 'Percentage (%)': (25.52, 25.55)},
            {'Attribute': 'parentCode', 'Size (KB)': (264.8, 265.1), 'Percentage (%)': (24.22, 24.25)},
            {'Attribute': 'type', 'Size (KB)': (270.3, 270.5), 'Percentage (%)': (24.72, 24.75)},
        ]

        #iterating over each row of df and testing it lies within a range
        for index, expected in enumerate(expected_rows_attribute_memory_usage_range):
            #parse the actual expected value for the current index
            actual_expected_value = expected_attribute_memory_usage_df.iloc[index]

            self.assertEqual(actual_expected_value['Attribute'], expected['Attribute'], 
                f"Expected and observed value for attribute {actual_expected_value['Attribute']} do not match:\n{actual_expected_value}.")
            self.assertTrue(expected['Size (KB)'][0] <= actual_expected_value['Size (KB)'] <= expected['Size (KB)'][1], f"Expected Size (KB) not in specified range for row {index}.")
            self.assertTrue(expected['Percentage (%)'][0] <= actual_expected_value['Percentage (%)'] <= expected['Percentage (%)'][1], f"Expected Percentage (%) not in specified range for row {index}.")
#5.)
        expected_country_object_attribute_memory_usage_df = pd.DataFrame({
            'Country Code': ['AD', 'BG', 'MQ', 'PK', 'SY', 'SN', 'TD'],
            'Size (KB)': [1.604, 3.874, 0.034, 1.582, 2.072, 1.991, 3.335],
            'Percentage (%)': [0.0975, 0.235, 0.002, 0.096, 0.126, 0.121, 0.203]
        })

        expected_rows_country_object_attribute_memory_usage_range = [
            {'Country Code': 'AD', 'Size (KB)': (1.6, 1.7), 'Percentage (%)': (0.097, 0.1)},
            {'Country Code': 'BG', 'Size (KB)': (3.85, 3.9), 'Percentage (%)': (0.23, 0.24)},
            {'Country Code': 'MQ', 'Size (KB)': (0.03, 0.05), 'Percentage (%)': (0.001, 0.004)},
            {'Country Code': 'PK', 'Size (KB)': (1.578, 1.59), 'Percentage (%)': (0.09, 0.1)},
            {'Country Code': 'SY', 'Size (KB)': (2.06, 2.08), 'Percentage (%)': (0.12, 0.131)},
            {'Country Code': 'SN', 'Size (KB)': (1.85, 2.0), 'Percentage (%)': (0.119, 0.124)},
            {'Country Code': 'TD', 'Size (KB)': (3.330, 3.340), 'Percentage (%)': (0.2, 0.206)},
        ]

        #iterating over each row of df and testing it lies within a range
        for index, expected in enumerate(expected_rows_country_object_attribute_memory_usage_range):
            #parse the actual expected value for the current index
            actual_expected_value = expected_country_object_attribute_memory_usage_df.iloc[index]

            self.assertEqual(actual_expected_value['Country Code'], expected['Country Code'], 
                f"Expected and observed value for attribute {actual_expected_value['Country Code']} do not match:\n{actual_expected_value}.")
            self.assertTrue(expected['Size (KB)'][0] <= actual_expected_value['Size (KB)'] <= expected['Size (KB)'][1], f"Expected Size (KB) not in specified range for row {index}.")
            self.assertTrue(expected['Percentage (%)'][0] <= actual_expected_value['Percentage (%)'] <= expected['Percentage (%)'][1], f"Expected Percentage (%) not in specified range for row {index}.")
#6.)
        with self.assertRaises(OSError):
            attributes_memory_usage(iso3166_2_json_filepath=os.path.join("iso3166_2", "invalid.json"), 
                export_folder=self.test_utils_folder, country_level_usage=True)
            attributes_memory_usage(iso3166_2_json_filepath="blahblahblah", 
                export_folder=self.test_utils_folder, country_level_usage=True)

    # @unittest.skip("")
    def test_is_latin(self):
        """ Testing function that checks if an individual character is a latin or non-latin character."""
        test_latin_char1 = "A"
        test_latin_char2 = "Z"
        test_latin_char3 = "É"
        test_latin_char4 = "ñ"
        test_latin_char5 = "x"
        test_not_latin_char1 = "λ"
        test_not_latin_char2 = "あ"
        test_not_latin_char3 = "中"
        test_not_latin_char4 = "😊"
        test_not_latin_char5 = "র"
#1.)
        self.assertTrue(is_latin(test_latin_char1), "Expected result for Latin character to be true.")
        self.assertTrue(is_latin(test_latin_char2), "Expected result for Latin character to be true.")
        self.assertTrue(is_latin(test_latin_char3), "Expected result for Latin character to be true.")
        self.assertTrue(is_latin(test_latin_char4), "Expected result for Latin character to be true.")
        self.assertTrue(is_latin(test_latin_char5), "Expected result for Latin character to be true.")
#2.)
        self.assertFalse(is_latin(test_not_latin_char1), "Expected result for Latin character to be false.")
        self.assertFalse(is_latin(test_not_latin_char2), "Expected result for Latin character to be false.")
        self.assertFalse(is_latin(test_not_latin_char3), "Expected result for Latin character to be false.")
        self.assertFalse(is_latin(test_not_latin_char4), "Expected result for Latin character to be false.")
        self.assertFalse(is_latin(test_not_latin_char5), "Expected result for Latin character to be false.")

    # @unittest.skip("")
    def test_only_roman_chars(self):
        """ Testing function that checks if a string contains just roman chars. """
        test_only_roman_chars1 = "Hello"
        test_only_roman_chars2 = "Ábaco"
        test_only_roman_chars3 = "blaħblaħblaħ"
        test_only_roman_chars4 = "Praha, Hlavní město"
        test_only_roman_chars5 = "w"
        test_not_only_roman_chars1 = "عجمان"
        test_not_only_roman_chars2 = "こんにちは"
        test_not_only_roman_chars3 = "ⵙⴰⴱⵜⴰ"
        test_not_only_roman_chars4 = "Hello, عجمان"
        test_not_only_roman_chars5 = "!!..北京市"
#1.)
        self.assertTrue(only_roman_chars(test_only_roman_chars1), "Expected result for Latin character to be true.")
        self.assertTrue(only_roman_chars(test_only_roman_chars2), "Expected result for Latin character to be true.")
        self.assertTrue(only_roman_chars(test_only_roman_chars3), "Expected result for Latin character to be true.")
        self.assertTrue(only_roman_chars(test_only_roman_chars4), "Expected result for Latin character to be true.")
        self.assertTrue(only_roman_chars(test_only_roman_chars5), "Expected result for Latin character to be true.")
#2.)
        self.assertFalse(only_roman_chars(test_not_only_roman_chars1), "Expected result for Latin character to be false.")
        self.assertFalse(only_roman_chars(test_not_only_roman_chars2), "Expected result for Latin character to be false.")
        self.assertFalse(only_roman_chars(test_not_only_roman_chars3), "Expected result for Latin character to be false.")
        self.assertFalse(only_roman_chars(test_not_only_roman_chars4), "Expected result for Latin character to be false.")
        self.assertFalse(only_roman_chars(test_not_only_roman_chars5), "Expected result for Latin character to be false.")

    # @unittest.skip("")    
    def test_add_history(self):
        """ Testing adding the historical subdivision data to the output. """
        # test_history_bd_24 = "BD-24" #BD-24: Joypurhat
        test_history_ht = "HT" #HT: Haiti
        test_history_praha = "Praha" #CZ-10: Praha
        test_history_avannaata_kommunia  = "Avannaata Kommunia" #GL-AV
        test_history_ke_47 = "KE-47" #KE-47: West Pokot
        test_history_karas = "NA-KA" #NA-KA: !Karas

        #load in test-iso3166-2.json object
        with open(self.test_iso3166_2_json) as output_json:
            test_iso3166_2_json = json.load(output_json)

        #remove any history attributes if applicable, get historical data using function
        for country_code, subdivisions in test_iso3166_2_json.items():
            for subdivision_code, attributes in subdivisions.items():
                if isinstance(attributes, dict) and "history" in attributes:
                    del attributes["history"]
        
        #getting history for all subdivision objects
        test_all_history = add_history(test_iso3166_2_json)
#1.)
        test_all_history_id = test_all_history["ID"]
        test_history_id_pd_expected = ['2023-11-23: Addition of province ID-PD; Update List Source. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:ID.']
        test_history_id_pe_expected = ['2022-11-29: Addition of provinces ID-PE, ID-PS and ID-PT; Update List Source. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:ID.']
        test_history_id_ma_expected = ['2011-12-13 (corrected 2011-12-15): Codes: Maluku (geographical unit) ID-MA -> ID-ML. Description of Change: Removal of duplicate code. Source: Newsletter II-3 - https://www.iso.org/files/live/sites/isoorg/files/archive/pdf/en/iso_3166-2_newsletter_ii-3_2011-12-13.pdf.', 
                                       '2002-05-21: Subdivisions added: ID-BB Bangka Belitung. ID-BT Banten. ID-GO Gorontalo. ID-MU Maluku Utara. Subdivisions deleted: ID-TT Timor Timur (see ISO 3166-2:TL). Codes: (to correct duplicate use). ID-IJ Irian Jaya (province) -> ID-PA Papua. Description of Change: Addition of four new provinces and deletion of one (ID-TT). Inclusion of one alternative name form and one changed province name (ID-PA, formerly ID-IJ). Source: Newsletter I-2 - https://web.archive.org/web/20120131102127/http://www.iso.org/iso/iso_3166-2_newsletter_i-2_en.pdf.']

        self.assertEqual(test_all_history_id["ID-PD"]["history"], test_history_id_pd_expected, f"Expected and observed history attribute output for ID-PD do not match:\n{test_all_history_id['ID-PD']['history']}")
        self.assertEqual(test_all_history_id["ID-PE"]["history"], test_history_id_pe_expected, f"Expected and observed history attribute output for ID-PE do not match:\n{test_all_history_id['ID-PE']['history']}")
        self.assertEqual(test_all_history_id["ID-MA"]["history"], test_history_id_ma_expected, f"Expected and observed history attribute output for ID-MA do not match:\n{test_all_history_id['ID-MA']['history']}")
#2.)
        test_all_history_kp = test_all_history["KP"]
        test_history_kp_10_expected = ['2017-11-23: Change of spelling of KP-10, KP-13 (McCune-Reischauer, 1939); addition of metropolitan city KP-14; update List Source. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:KP.']
        test_history_kp_14_expected = ['2017-11-23: Change of spelling of KP-10, KP-13 (McCune-Reischauer, 1939); addition of metropolitan city KP-14; update List Source. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:KP.', '2010-02-03 (corrected 2010-02-19): Subdivisions deleted: KP-KAE Kaesong-si. KP-NAM Nampo-si. Codes: format changed . Description of Change: Administrative update, replacement of alphabetical characters with numeric characters in second code element. Source: Newsletter II-1 - https://www.iso.org/files/live/sites/isoorg/files/archive/pdf/en/iso_3166-2_newsletter_ii-1_corrected_2010-02-19.pdf.']
        test_history_kp_15_expected = ['2022-11-29: Addition of metropolitan city KP-15; Update List Source. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:KP.', '2010-02-03 (corrected 2010-02-19): Subdivisions deleted: KP-KAE Kaesong-si. KP-NAM Nampo-si. Codes: format changed . Description of Change: Administrative update, replacement of alphabetical characters with numeric characters in second code element. Source: Newsletter II-1 - https://www.iso.org/files/live/sites/isoorg/files/archive/pdf/en/iso_3166-2_newsletter_ii-1_corrected_2010-02-19.pdf.']

        self.assertEqual(test_all_history_kp["KP-10"]["history"], test_history_kp_10_expected, f"Expected and observed history attribute output for KP-10 do not match:\n{test_all_history_kp['KP-10']['history']}")
        self.assertEqual(test_all_history_kp["KP-14"]["history"], test_history_kp_14_expected, f"Expected and observed history attribute output for KP-NAM do not match:\n{test_all_history_kp['KP-14']['history']}")
        self.assertEqual(test_all_history_kp["KP-15"]["history"], test_history_kp_15_expected, f"Expected and observed history attribute output for KP-NAJ do not match:\n{test_all_history_kp['KP-15']['history']}")
#3.)
        test_all_history_me = test_all_history["ME"]
        test_history_me_22_expected = ['2014-11-03: Add two municipalities ME-22 and ME-23. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:ME.']
        test_history_me_23_expected = ['2014-11-03: Add two municipalities ME-22 and ME-23. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:ME.']
        test_history_me_24_expected = ['2019-11-22: Addition of municipality ME-24; Update List Source. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:ME.']

        self.assertEqual(test_all_history_me["ME-22"]["history"], test_history_me_22_expected, f"Expected and observed history attribute output for ME-22 do not match:\n{test_all_history_me['ME-22']['history']}")
        self.assertEqual(test_all_history_me["ME-23"]["history"], test_history_me_23_expected, f"Expected and observed history attribute output for ME-23 do not match:\n{test_all_history_me['ME-23']['history']}")
        self.assertEqual(test_all_history_me["ME-24"]["history"], test_history_me_24_expected, f"Expected and observed history attribute output for ME-24 do not match:\n{test_all_history_me['ME-24']['history']}")

    # @unittest.skip("")
    def test_export_iso3166_2_data(self):
        """ Testing functionality for exporting the output data to the export formats. """
        #load in test-iso3166-2.json object
        with open(self.test_iso3166_2_json) as output_json:
            test_iso3166_2_json = json.load(output_json)
#1.)
        export_iso3166_2_data(test_iso3166_2_json, export_filepath=os.path.join(self.test_utils_folder, "test_export_1"), export_csv=True, export_xml=True)

        self.assertTrue(os.path.isfile(os.path.join(self.test_utils_folder, "test_export_1.json")), "Expected output object to be exported to JSON.")
        self.assertTrue(os.path.isfile(os.path.join(self.test_utils_folder, "test_export_1.csv")), "Expected output object to be exported to CSV.")
        self.assertTrue(os.path.isfile(os.path.join(self.test_utils_folder, "test_export_1.xml")), "Expected output object to be exported to XML.")

        #validate column order
        test_iso3166_2_json_1 = pd.read_csv(os.path.join(self.test_utils_folder, "test_export_1.csv"))
        self.assertEqual(list(test_iso3166_2_json_1.columns), ['alphaCode', 'subdivisionCode', 'name', 'localOtherName', 'type', 'parentCode', 'flag', 'latLng'], 
                         f"Expected and observed column order for output CSV do not match:\n{list(test_iso3166_2_json_1.columns)}.")
#2.)
        export_iso3166_2_data(test_iso3166_2_json, export_filepath=os.path.join(self.test_utils_folder, "test_export_2"), export_csv=True, export_xml=False)

        self.assertTrue(os.path.isfile(os.path.join(self.test_utils_folder, "test_export_2.json")), "Expected output object to be exported to JSON.")
        self.assertTrue(os.path.isfile(os.path.join(self.test_utils_folder, "test_export_2.csv")), "Expected output object to be exported to CSV.")
        self.assertFalse(os.path.isfile(os.path.join(self.test_utils_folder, "test_export_2.xml")), "Expected output object to not be exported to XML.")

        test_iso3166_2_json_2 = pd.read_csv(os.path.join(self.test_utils_folder, "test_export_2.csv"))
        self.assertEqual(list(test_iso3166_2_json_2.columns), ['alphaCode', 'subdivisionCode', 'name', 'localOtherName', 'type', 'parentCode', 'flag', 'latLng'], 
                         f"Expected and observed column order for output CSV do not match:\n{list(test_iso3166_2_json_2.columns)}.")
#3.)
        export_iso3166_2_data(test_iso3166_2_json, export_filepath=os.path.join(self.test_utils_folder, "test_export_3"), export_csv=True, export_xml=False,
                              exclude_default_attributes="latLng,flag")

        self.assertTrue(os.path.isfile(os.path.join(self.test_utils_folder, "test_export_3.json")), "Expected output object to be exported to JSON.")
        self.assertTrue(os.path.isfile(os.path.join(self.test_utils_folder, "test_export_3.csv")), "Expected output object to be exported to CSV.")
        self.assertFalse(os.path.isfile(os.path.join(self.test_utils_folder, "test_export_3.xml")), "Expected output object to not be exported to XML.")

        #load in test-iso3166-2.json object
        with open(os.path.join(self.test_utils_folder, "test_export_3.json")) as output_json:
            test_iso3166_2_json_3 = json.load(output_json)

        #iterate over the output object and validate that the attributes are excluded
        for country_code, subdivisions in test_iso3166_2_json_3.items():
            for subdivision_code, attributes in subdivisions.items():
                self.assertTrue(all(key not in attributes for key in ("latLng", "flag")), "Expected latLng and flag attributes to be excluded from subdivision output.")

        #validate column order
        test_iso3166_2_json_3 = pd.read_csv(os.path.join(self.test_utils_folder, "test_export_3.csv"))
        self.assertEqual(list(test_iso3166_2_json_3.columns), ['alphaCode', 'subdivisionCode', 'name', 'localOtherName', 'type', 'parentCode'], 
                         f"Expected and observed column order for output CSV do not match:\n{list(test_iso3166_2_json_3.columns)}.")
#4.)
        export_iso3166_2_data(test_iso3166_2_json, export_filepath=os.path.join(self.test_utils_folder, "test_export_4"), export_csv=True, export_xml=False,
                              exclude_default_attributes="parentCode")

        self.assertTrue(os.path.isfile(os.path.join(self.test_utils_folder, "test_export_4.json")), "Expected output object to be exported to JSON.")
        self.assertTrue(os.path.isfile(os.path.join(self.test_utils_folder, "test_export_4.csv")), "Expected output object to be exported to CSV.")
        self.assertFalse(os.path.isfile(os.path.join(self.test_utils_folder, "test_export_4.xml")), "Expected output object to not be exported to XML.")

        #load in test-iso3166-2.json object
        with open(os.path.join(self.test_utils_folder, "test_export_4.json")) as output_json:
            test_iso3166_2_json_4 = json.load(output_json)

        #iterate over the output object and validate that the attributes are excluded
        for country_code, subdivisions in test_iso3166_2_json_4.items():
            for subdivision_code, attributes in subdivisions.items():
                self.assertTrue(all(key not in attributes for key in ("parentCode")), "Expected parentCode attribute to be excluded from subdivision output.")

        #validate column order
        test_iso3166_2_json_4 = pd.read_csv(os.path.join(self.test_utils_folder, "test_export_4.csv"))
        self.assertEqual(list(test_iso3166_2_json_4.columns), ['alphaCode', 'subdivisionCode', 'name', 'localOtherName', 'type', 'flag', 'latLng'], 
                        f"Expected and observed column order for output CSV do not match:\n{list(test_iso3166_2_json_4.columns)}.")

    @classmethod
    def tearDown(self):
        """ Delete any temp export folder. """
        shutil.rmtree(self.test_utils_folder)
