import json
import os
import unittest
from unittest.mock import patch, MagicMock
from scripts.history import add_history

# @unittest.skip("")
class HistoryTests(unittest.TestCase):
    """
    Unit test suite for history module using mocks.

    Test Cases
    ==========
    test_add_history: 
      test adding historical subdivision data to the output.
    """
    def setUp(self):
        """ Setup test environment. """
        #path to test ISO 3166-2 json file
        self.test_iso3166_2_json = os.path.join("tests", "test_files", "test_iso3166-2.json")

    # @unittest.skip("")    
    def test_add_history(self):
        """ Testing adding the historical subdivision data to the output. """
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
        test_history_id_pd_expected = [{'Change': 'Addition of province ID-PD; Update List Source.', 'Description of Change': '', 'Date Issued': '2023-11-23', 
                                        'Source': 'Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:ID.'}]
        test_history_id_pe_expected = [{'Change': 'Addition of provinces ID-PE, ID-PS and ID-PT; Update List Source.', 'Description of Change': '', 'Date Issued': '2022-11-29', 
                                        'Source': 'Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:ID.'}]        
        test_history_id_ma_expected = [{'Change': 'Codes: Maluku (geographical unit) ID-MA -> ID-ML.', 'Description of Change': 'Removal of duplicate code.', 'Date Issued': '2011-12-13 (corrected 2011-12-15)', 
                                        'Source': 'Newsletter II-3 - https://www.iso.org/files/live/sites/isoorg/files/archive/pdf/en/iso_3166-2_newsletter_ii-3_2011-12-13.pdf.'}, 
                                        {'Change': 'Subdivisions added: ID-BB Bangka Belitung. ID-BT Banten. ID-GO Gorontalo. ID-MU Maluku Utara. Subdivisions deleted: ID-TT Timor Timur (see ISO 3166-2:TL). Codes: (to correct duplicate use). ID-IJ Irian Jaya (province) -> ID-PA Papua.', 
                                         'Description of Change': 'Addition of four new provinces and deletion of one (ID-TT). Inclusion of one alternative name form and one changed province name (ID-PA, formerly ID-IJ).', 'Date Issued': '2002-05-21', 
                                         'Source': 'Newsletter I-2 - https://web.archive.org/web/20120131102127/http://www.iso.org/iso/iso_3166-2_newsletter_i-2_en.pdf.'}]

        self.assertEqual(test_all_history_id["ID-PD"]["history"], test_history_id_pd_expected, f"Expected and observed history attribute output for ID-PD do not match:\n{test_all_history_id['ID-PD']['history']}")
        self.assertEqual(test_all_history_id["ID-PE"]["history"], test_history_id_pe_expected, f"Expected and observed history attribute output for ID-PE do not match:\n{test_all_history_id['ID-PE']['history']}")
        self.assertEqual(test_all_history_id["ID-MA"]["history"], test_history_id_ma_expected, f"Expected and observed history attribute output for ID-MA do not match:\n{test_all_history_id['ID-MA']['history']}")
#2.)
        test_all_history_kp = test_all_history["KP"]
        test_history_kp_10_expected = [{'Change': 'Change of spelling of KP-10, KP-13 (McCune-Reischauer, 1939); addition of metropolitan city KP-14; update List Source.', 'Description of Change': '', 'Date Issued': '2017-11-23', 
                                       'Source': 'Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:KP.'}]
        test_history_kp_14_expected = [{'Change': 'Change of spelling of KP-10, KP-13 (McCune-Reischauer, 1939); addition of metropolitan city KP-14; update List Source.', 'Description of Change': '', 'Date Issued': '2017-11-23', 
                                       'Source': 'Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:KP.'}, 
                                       {'Change': 'Subdivisions deleted: KP-KAE Kaesong-si. KP-NAM Nampo-si. Codes: format changed.', 'Description of Change': 'Administrative update, replacement of alphabetical characters with numeric characters in second code element.', 
                                       'Date Issued': '2010-02-03 (corrected 2010-02-19)', 'Source': 'Newsletter II-1 - https://www.iso.org/files/live/sites/isoorg/files/archive/pdf/en/iso_3166-2_newsletter_ii-1_corrected_2010-02-19.pdf.'}]
        test_history_kp_15_expected = [{'Change': 'Addition of metropolitan city KP-15; Update List Source.', 'Description of Change': '', 'Date Issued': '2022-11-29', 
                                        'Source': 'Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:KP.'}, 
                                       {'Change': 'Subdivisions deleted: KP-KAE Kaesong-si. KP-NAM Nampo-si. Codes: format changed.', 'Description of Change': 'Administrative update, replacement of alphabetical characters with numeric characters in second code element.', 
                                       'Date Issued': '2010-02-03 (corrected 2010-02-19)', 'Source': 'Newsletter II-1 - https://www.iso.org/files/live/sites/isoorg/files/archive/pdf/en/iso_3166-2_newsletter_ii-1_corrected_2010-02-19.pdf.'}]

        self.assertEqual(test_all_history_kp["KP-10"]["history"], test_history_kp_10_expected, f"Expected and observed history attribute output for KP-10 do not match:\n{test_all_history_kp['KP-10']['history']}")
        self.assertEqual(test_all_history_kp["KP-14"]["history"], test_history_kp_14_expected, f"Expected and observed history attribute output for KP-13 do not match:\n{test_all_history_kp['KP-14']['history']}")
        self.assertEqual(test_all_history_kp["KP-15"]["history"], test_history_kp_15_expected, f"Expected and observed history attribute output for KP-15 do not match:\n{test_all_history_kp['KP-15']['history']}")
#3.)
        test_all_history_me = test_all_history["ME"]
        test_history_me_22_expected = [{'Change': 'Add two municipalities ME-22 and ME-23.', 'Description of Change': '', 'Date Issued': '2014-11-03', 
                                        'Source': 'Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:ME.'}]
        test_history_me_23_expected = [{'Change': 'Add two municipalities ME-22 and ME-23.', 'Description of Change': '', 'Date Issued': '2014-11-03', 
                                        'Source': 'Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:ME.'}]
        test_history_me_24_expected = [{'Change': 'Addition of municipality ME-24; Update List Source.', 'Description of Change': '', 'Date Issued': '2019-11-22', 
                                        'Source': 'Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:ME.'}]

        self.assertEqual(test_all_history_me["ME-22"]["history"], test_history_me_22_expected, f"Expected and observed history attribute output for ME-22 do not match:\n{test_all_history_me['ME-22']['history']}")
        self.assertEqual(test_all_history_me["ME-23"]["history"], test_history_me_23_expected, f"Expected and observed history attribute output for ME-23 do not match:\n{test_all_history_me['ME-23']['history']}")
        self.assertEqual(test_all_history_me["ME-24"]["history"], test_history_me_24_expected, f"Expected and observed history attribute output for ME-24 do not match:\n{test_all_history_me['ME-24']['history']}")
#4.)
        test_all_history_MZ = test_all_history["MZ"]
        test_all_history_PY = test_all_history["PY"]
        test_all_history_SK = test_all_history["SK"]

        for subd_code, subd_data in test_all_history_MZ.items():
            self.assertIsNone(subd_data.get("history"), 
                            f"Expected history to be None for MZ-{subd_code}, got: {subd_data.get('history')}")
        
        for subd_code, subd_data in test_all_history_PY.items():
            self.assertIsNone(subd_data.get("history"), 
                            f"Expected history to be None for PY-{subd_code}, got: {subd_data.get('history')}")
        
        for subd_code, subd_data in test_all_history_SK.items():
            self.assertIsNone(subd_data.get("history"), 
                            f"Expected history to be None for SK-{subd_code}, got: {subd_data.get('history')}")

# Run the tests
if __name__ == '__main__':
    unittest.main()