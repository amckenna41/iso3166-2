from scripts.local_other_names import *
from scripts.language_lookup import *
from scripts.utils import *
from iso3166_2 import *
import iso3166
import pandas as pd
import os
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

# @unittest.skip("Skipping local/other name unit tests.")
class Local_Other_Name_Tests(unittest.TestCase):
    """
    Test suite for testing the database of local/other names for each subdivision in the 
    respective files and the auxiliary script used for generating the files and various
    validation checks.

    test_local_other_names_total:
        testing correct total number of rows in CSV.
    test_local_other_names_csv_columns:
        testing correct columns in CSV.
    test_local_other_names_unique:
        testing each row in CSV is unique.
    test_valid_local_other_names_alpha_subdivision_codes_names:
        testing valid country and subdivision codes, as well as subdivision names in CSV.
    test_local_other_names_data:
        testing various row values in csv.
    test_iso3166_2_local_other_names:
        testing local/other names and names in csv match those in attribute of main iso3166-2 object.
    test_valid_language_codes:
        testing each language code in local/other name attribute is valid.
    test_validate_local_other_names:
        testing each row's local/other names are in valid format, including brackets and length.
    test_duplicate_translations:
        testing there are no duplicate local/other names within each row.
    """ 
    @classmethod
    def setUp(self):
        """ Initialise variables and import relevant csv/jsons. """
        self.local_other_names_csv_filepath = os.path.join("tests", "test_files", "test_local_other_names.csv")
        self.local_other_names_df = pd.read_csv(self.local_other_names_csv_filepath, keep_default_na=False)

        self.language_obj = LanguageLookup(imported_file_name=self.local_other_names_csv_filepath, 
            language_lookup_filename=os.path.join("tests", "test_files", "test_language_lookup.json"))

        #create instance of Subdivisions class from iso3166-2 software
        self.iso3166_2_obj = Subdivisions()

    # @unittest.skip("")
    def test_local_other_names_total(self):
        """ Testing correct number of rows in local/other names CSV. """
        self.assertEqual(len(self.local_other_names_df), 5049, f"Expected 5049 rows in the local/other names dataframe, got {len(self.local_other_names_df)}.")

    # @unittest.skip("")
    def test_local_other_names_csv_columns(self):
        """ Testing correct columns in local/other names CSV. """
        self.assertEqual(list(self.local_other_names_df.columns), ["alphaCode", "subdivisionCode", "name" ,"localOtherName"], 
            f"Expected and observed columns do not match {list(self.local_other_names_df.columns)}.")

    # @unittest.skip("")
    def test_local_other_names_unique(self):
        """ Testing each row is unique in CSV. """
        duplicate_rows = self.local_other_names_df.duplicated()
        self.assertFalse(duplicate_rows.any(), f"Found {duplicate_rows.sum()} duplicate rows in the CSV.")

    # @unittest.skip("")
    def test_valid_local_other_names_alpha_subdivision_codes_names(self):
        """ Testing valid country and subdivision codes as well as subdivision names for each row. """
#1.)
        country_codes_to_check = self.local_other_names_df["alphaCode"]
        invalid_country_codes = country_codes_to_check[~country_codes_to_check.isin(list(iso3166.countries_by_alpha2.keys()))]
        self.assertTrue(invalid_country_codes.empty, f"Expected all country codes to be valid ISO 3166-1 alpha-2 codes:\n{invalid_country_codes}.")
#2.)    
        all_subdivision_codes = [code for codes in self.iso3166_2_obj.subdivision_codes().values() for code in codes]
        subdivisions_codes_to_check = self.local_other_names_df["subdivisionCode"]
        invalid_subdivision_codes = subdivisions_codes_to_check[~subdivisions_codes_to_check.isin(all_subdivision_codes)]
        self.assertTrue(invalid_subdivision_codes.empty, f"Expected all subdivision codes to be valid ISO 3166-2 subdivision codes:\n{invalid_subdivision_codes}.")
#3.)
        #get list of valid subdivision names from iso3166-2.json dataset & compare with "name" column in local/other names csv
        all_subdivision_names = [code for codes in self.iso3166_2_obj.subdivision_names().values() for code in codes]
        filtered_df = self.local_other_names_df[~self.local_other_names_df["name"].str.contains(r"[\*\†]", regex=True)] #filter out any names with '*' or '†' in them
        subdivisions_names_to_check = filtered_df["name"]
        invalid_mask = ~subdivisions_names_to_check.isin(all_subdivision_names)
        invalid_rows = filtered_df[invalid_mask]

        #validate each subdivision name is valid, if invalid output descriptive error message
        if not invalid_rows.empty:
            error_list = []
            for idx, row in invalid_rows.iterrows():
                code = row["subdivisionCode"]
                alpha2 = code.split("-")[0] if "-" in code else None
                subdivision_data = self.iso3166_2_obj.all[alpha2][code]

                #strip "*" and "†" from both names
                cleaned_old_name = re.sub(r"[\*\†]", "", row["name"]).strip()
                cleaned_new_name = re.sub(r"[\*\†]", "", subdivision_data["name"]).strip()

                #append erroneous row with the relevant subdivision info to the error list object
                if cleaned_old_name != cleaned_new_name:
                    error_list.append(f"Row {idx}: subdivisionCode='{code}', oldName (in local_other_names)='{row['name']}', newName (in exported iso3166-2.json)={subdivision_data['name']}")

            self.assertTrue(len(error_list) == 0, f"Expected all subdivision names to be valid ISO 3166-2 subdivision names:\n\n{error_list}")
                    
    # @unittest.skip("")
    def test_local_other_names_data(self):
        """ Testing various row values in local/other names csv. """
        test_local_other_name_az_zaq = "AZ-ZAQ" #Zaqatala
        test_local_other_name_cd_kn = "CD-KN" #Kinshasa
        test_local_other_name_es_ar = "ES-AR" #Aragón
        test_local_other_name_ga_2 = "GA-2" #Haut-Ogooué
        test_local_other_name_gb_lnd = "GB-LND" #City of London
        test_local_other_name_ph_bas = "PH-BAS" #Basilan
#1.)    
        test_local_other_name_az_zaq_expected = "Zagatala (eng), Закатала мухъ (ava), Закаталайни район (tkr)"
        local_other_name_az_zaq = self.local_other_names_df.loc[self.local_other_names_df['subdivisionCode'] == test_local_other_name_az_zaq]["localOtherName"].values[0]
        self.assertEqual(local_other_name_az_zaq, test_local_other_name_az_zaq_expected, 
            f"Local/other name row value for AZ-ZAQ is incorrect:\n{local_other_name_az_zaq}.")
#2.)    
        test_local_other_name_cd_kn_expected = "Kinshasa (eng), Kinsásá (lin), Kin la belle (fra), Kin the beautiful (eng)"
        local_other_name_cd_kn = self.local_other_names_df.loc[self.local_other_names_df['subdivisionCode'] == test_local_other_name_cd_kn]["localOtherName"].values[0]
        self.assertEqual(local_other_name_cd_kn, test_local_other_name_cd_kn_expected, 
            f"Local/other name row value for CD-KN is incorrect:\n{local_other_name_cd_kn}.")
#3.)    
        test_local_other_name_es_ar_expected = "Aragon (eng), Aragón (arg), Aragó (cat)"
        local_other_name_es_ar = self.local_other_names_df.loc[self.local_other_names_df['subdivisionCode'] == test_local_other_name_es_ar]["localOtherName"].values[0]
        self.assertEqual(local_other_name_es_ar, test_local_other_name_es_ar_expected, 
            f"Local/other name row value for ES-AR is incorrect:\n{local_other_name_es_ar}.")
#4.)    
        test_local_other_name_ga_2_expected = "Upper Ogooué (eng)"
        local_other_name_ga_2 = self.local_other_names_df.loc[self.local_other_names_df['subdivisionCode'] == test_local_other_name_ga_2]["localOtherName"].values[0]
        self.assertEqual(local_other_name_ga_2, test_local_other_name_ga_2_expected, 
            f"Local/other name row value for GA-2 is incorrect:\n{local_other_name_ga_2}.")
#5.)    
        test_local_other_name_gb_lnd_expected = "The City (eng), The Square Mile (eng)"
        local_other_name_gb_lnd = self.local_other_names_df.loc[self.local_other_names_df['subdivisionCode'] == test_local_other_name_gb_lnd]["localOtherName"].values[0]
        self.assertEqual(local_other_name_gb_lnd, test_local_other_name_gb_lnd_expected, 
            f"Local/other name row value for GB-LND is incorrect:\n{local_other_name_gb_lnd}.")
#6.)    
        test_local_other_name_ph_bas_expected = "Basilan (tgl), Basilan (fil), Basilan (cbk), Wilayah Basilanin (yka), Wilaya sin Basilan (tsg)"
        local_other_name_ph_bas = self.local_other_names_df.loc[self.local_other_names_df['subdivisionCode'] == test_local_other_name_ph_bas]["localOtherName"].values[0]
        self.assertEqual(local_other_name_ph_bas, test_local_other_name_ph_bas_expected, 
            f"Local/other name row value for GB-LND is incorrect:\n{local_other_name_ph_bas}.")

    # @unittest.skip("Need to rerun script and export full dataset again.")  
    def test_iso3166_2_local_other_names(self):
        """ Testing local/other names and names csv values match those in main iso3166-2 object. """
#1.)
        for index, row in self.local_other_names_df.iterrows():
            #run assertion based on if localOtherName is None or ''
            if (self.iso3166_2_obj.all[row["alphaCode"]][row["subdivisionCode"]]["localOtherName"] is None):
                self.assertIsNone(self.iso3166_2_obj.all[row["alphaCode"]][row["subdivisionCode"]]["localOtherName"], 
                    f"Expected localOtherName attribute value to be None for {row['subdivisionCode']}, got:\n{self.iso3166_2_obj.all[row['alphaCode']][row['subdivisionCode']]['localOtherName']}.")
            else:
                self.assertEqual(self.iso3166_2_obj.all[row["alphaCode"]][row["subdivisionCode"]]["localOtherName"], row["localOtherName"],
                    f"Current value for localOtherName attribute for subdivision {row['subdivisionCode']} does not match that in the local_other_names.csv:\n"
                    f"ISO 3166-2 object: {self.iso3166_2_obj.all[row['alphaCode']][row['subdivisionCode']]['localOtherName']}, Local/Other Names CSV: {row['localOtherName']}\n\n{row}")
#2.)        
            if ("*" in row["name"] or "†" in row["name"]):
                self.assertEqual(self.iso3166_2_obj.all[row["alphaCode"]][row["subdivisionCode"]]["name"], row["name"],
                    f"Current value for name attribute for subdivision {row['subdivisionCode']} does not match that in the local_other_names.csv:\n"
                    f"ISO 3166-2 object: {self.iso3166_2_obj.all[row['alphaCode']][row['subdivisionCode']]['name']},Local/Other Names CSV: {row['name']}\n\n{row}")

    # @unittest.skip("")
    def test_valid_language_codes(self):
        """ Testing each local/other name has a valid language code. """
        valid_language_codes = self.language_obj.all_language_codes
#1.)
        #iterate over local/other name column, testing each language code is valid 
        for index, row in self.local_other_names_df["localOtherName"].items():
            
            #skip current row if localOtherName attribute null
            if (row is None):
                continue

            #split multiple local/other name translations into comma separated list, preserve single quoted elements
            local_other_names_split  = split_preserving_quotes(row)

            #validate each language code
            for name in local_other_names_split:
                match = re.match(r'(.+?)\((.+?)\)', name.strip())
                language_code = match.group(2).strip()
                self.assertIn(language_code, valid_language_codes, f"Expected language code {language_code} to be in list of valid codes.")
                         
    # @unittest.skip("")
    def test_validate_local_other_names(self):
        """ Testing local/other subdivision names are in valid format. """
        #iterate over local/other name column, testing each language code is valid 
        for index, row in self.local_other_names_df[self.local_other_names_df["localOtherName"].notnull()].iterrows():
            local_other_name = row["localOtherName"]

            #skip current row if localOtherName attribute null
            if (local_other_name is None):
                continue

            #split multiple local/other name translations into comma separated list, preserve single quoted elements, iterate over each
            local_other_names_split  = split_preserving_quotes(local_other_name)
            for name in local_other_names_split:
#1.)
                self.assertTrue(len(name) <= 100, f"Expected local/other name to be less than 100 characters long: {name}. (Length: {len(name)}).")
#2.)
                match = re.fullmatch(r".+ \([^\s()]{2,20}\)", name) #re.fullmatch(r".+ \([a-z]{2,3}\)", name)
                self.assertTrue(match, f"Invalid format for localOtherName entry '{name}' in row {index}:\n{local_other_name}:\n{row}")

    # @unittest.skip("")
    def test_duplicate_translations(self):
        """ Testing any duplicate subdivision names & translations are removed from output/csv. """
#1.)
        #iterate over local/other name column, testing each language code is valid 
        for index, row in self.local_other_names_df["localOtherName"].items():
            
            #skip current row if localOtherName attribute null
            if (row is None):
                continue

            #split multiple local/other name translations into comma separated list, preserve single quoted elements
            local_other_names_split = split_preserving_quotes(row)

            duplicates = [name for name in local_other_names_split if local_other_names_split.count(name) > 1]
            self.assertEqual(len(duplicates), 0, f"Expected there to be no duplicate values for the current row for the local/other name attribute:\n{local_other_names_split}.")