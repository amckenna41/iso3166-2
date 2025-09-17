import iso3166
from iso3166_2 import *
import requests
import os
from fake_useragent import UserAgent
from jsonschema import validate, ValidationError
from importlib.metadata import metadata
from bs4 import BeautifulSoup
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

# @unittest.skip("")
class ISO3166_2_API_Tests(unittest.TestCase):
    """
    Test suite for testing ISO 3166-2 api created to accompany the iso3166-2 Python software package. 
    The API has 6 main endpoints:
    - /api/all
    - /api/alpha
    - /api/subdivision
    - /api/search
    - /api/country_name
    - /api/list_subdivisions
    
    Test Cases
    ==========
    test_homepage_endpoint:
        testing main endpoint that returns the homepage and API documentation. 
    test_all_endpoint:
        testing correct data and attributes are returned from the /all API endpoint, which returns all the available 
        ISO 3166-2 data.  
    test_all_endpoint_duplicates:
        testing that no duplicate subdivision objects are returned for the /all API endpoint.
    test_json_schema_all_endpoint:
        testing JSON schema for all data using /api/all endpoint.
    test_all_endpoint_individual_totals:
        testing the individual total number of subdivision data per country from /api/all endpoint.  
    test_all_endpoint_null_values:
        testing that the name and type attributes for all subdivisions are not null.
    test_all_endpoint_parent_codes:
        testing that for all subdivisions, their parent codes are valid within that subdivision's parent country.
    test_alpha_endpoint:
        testing correct data and attributes are returned from the /alpha API endpoint using a variety of alpha-2, 
        alpha-3 or numeric code inputs.
    test_subdivision_endpoint:
        testing correct data and attributes are returned from the /subdivision API endpoint using a variety of 
        subdivision code inputs.
    test_search_endpoint:
        testing correct data and attributes are returned from the /search API endpoint using a variety of 
        search terms.
    test_country_name_endpoint:
        testing correct data and attributes are returned from the /country_name API endpoint using a variety of 
        country name inputs.
    test_list_subdivisions:
        testing correct data and attributes are returned from the /list_subdivisions API endpoint, which returns all 
        the ISO 3166-2 subdivision codes for each country or subset of input countries.
    test_version:
        testing the correct and up-to-date version of the iso3166-2 software is being used by the API.
    """
    def setUp(self):
        """ Initialise test variables, import json. """
        #initialise User-agent header for requests library 
        self.__version__ = metadata('iso3166-2')['version']
        user_agent = UserAgent()
        self.user_agent_header = {"User-Agent": user_agent.random, 'Accept': 'application/json'}

        #url endpoints for API
        self.api_base_url = "https://iso3166-2-api.vercel.app/api/"
        self.alpha_base_url = self.api_base_url + "alpha/"
        self.subdivision_base_url = self.api_base_url + "subdivision/"
        self.search_base_url = self.api_base_url + "search/"
        self.country_name_base_url = self.api_base_url + "country_name/"
        self.all_base_url = self.api_base_url + "all"
        self.list_subdivisions_base_url = self.api_base_url + "list_subdivisions"
        self.version_base_url = self.api_base_url + "version"

        #list of keys that should be in subdivisions key of output object
        self.correct_subdivision_keys = ["name", "localOtherName", "type", "parentCode", "latLng", "flag", "history"]

        #base url for subdivision flags
        self.flag_base_url = "https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/"

        #create instance of ISO 3166-2 class
        self.iso3166_2_data = Subdivisions()

        #call /api/all endpoint to get all data from API - saved as class variable to alleviate multiple calls
        self.test_request_all = requests.get(self.all_base_url, headers=self.user_agent_header)

        #turn off tqdm progress bar functionality when running tests
        os.environ["TQDM_DISABLE"] = "1"

    # @unittest.skip("")
    def test_homepage_endpoint(self):
        """ Testing contents of main /api endpoint that returns the homepage and API documentation. """
        test_request_main = requests.get(self.api_base_url, headers=self.user_agent_header, timeout=(3.05, 27))
        soup = BeautifulSoup(test_request_main.content, 'html.parser')
#1.)    
        # version = soup.find(id='version').text.split(': ')[1] #need to get this using selenium as version and last-updated is dynamically retrieved in frontend
        # last_updated = soup.find(id='last-updated').text.split(': ')[1]
        author = soup.find(id='author').text.split(': ')[1]

        # self.assertEqual(version, "1.8.0", f"Expected API version to be 1.8.0, got {version}.") 
        # self.assertEqual(last_updated, "September 2025", f"Expected last updated date to be September 2025, got {last_updated}.")
        self.assertEqual(author, "AJ", f"Expected author to be AJ, got {author}.")
#2.)
        section_list_menu = soup.find(id='section-list-menu').find_all('li')
        correct_section_menu = ["About", "Attributes", "Query String Parameters", "Endpoints", "All", "Alpha Code", "Subdivision", "Search", "Country Name", "List Subdivisions", "Contributing", "Credits"]
        for li in section_list_menu:
            self.assertIn(li.text.strip(), correct_section_menu, f"Expected list element {li} to be in list.")

    # @unittest.skip("Skipping /all endpoint tests to not overload server.")
    def test_all_endpoint(self):
        """ Test /all endpoint which returns all subdivision data for all ISO 3166 countries. """
#1.)    
        test_request_all = self.test_request_all.json()

        self.assertIsInstance(test_request_all, dict, f"Expected output object of API to be of type dict, got {type(self.test_request_all)}.")
        self.assertEqual(len(test_request_all), 250, f"Expected there to be 250 elements in output object, got {len(test_request_all)}.")
        self.assertEqual(self.test_request_all.status_code, 200, f"Expected 200 status code from request, got {self.test_request_all.status_code}.")
        self.assertEqual(self.test_request_all.headers["content-type"], "application/json", f"Expected Content type to be application/json, got {self.test_request_all.headers['content-type']}.")
#2.)
        for alpha2 in list(test_request_all.keys()):
            self.assertIn(alpha2, iso3166.countries_by_alpha2, f"Alpha-2 code {alpha2} not found in list of available country codes.")
            for subd in test_request_all[alpha2]:
                self.assertIn(subd, self.iso3166_2_data.subdivision_codes(alpha2), f"Subdivision code {subd} not found in list of available subdivision codes.")
#3.)
        total_subdivision_objects = sum(len(subd) for subd in test_request_all.values())
        self.assertEqual(total_subdivision_objects, 5049, f"Expected and observed total subdivisions do not match, got {total_subdivision_objects}.")
#4.)
        test_all_request_filter = requests.get(self.all_base_url, headers=self.user_agent_header, params={"filter": "flag, type"}).json() #filtering out all attributes but flag and type

        for alpha_code in test_all_request_filter:
            for subd in test_all_request_filter[alpha_code]:
                self.assertEqual(list(test_all_request_filter[alpha_code][subd].keys()), ["flag", "type"], 
                    f"Expected subdivision attributes to just include the flag attribute, got {list(test_all_request_filter[alpha_code][subd].keys())}.")
#5.)
        test_all_request_limit = requests.get(self.all_base_url, headers=self.user_agent_header, params={"limit": "10"}).json() #limiting to 10 countries
        self.assertEqual(len(test_all_request_limit), 10, "Expected output object to contain 10 countries, got {len(test_all_request_limit)}.")
#6.)
        # test_request_all_invalid_attribute = requests.get(self.all_base_url, headers=self.user_agent_header, params={"filter": "invalid_attribute"}).json() #invalid attribute input
        # test_request_all_invalid_attribute_expected = {"message": f"Invalid attribute name input to filter query string parameter: invalid_attribute. Refer to the list of supported attributes: name, localOtherName, type, parentCode, flag, latLng, history.", "path": f'{self.all_base_url}?filter=invalid_attribute', "status": 400}
        # self.assertEqual(test_request_all_invalid_attribute, test_request_all_invalid_attribute_expected, f"Expected and observed output error object do not match:\n{test_request_all_invalid_attribute}.")

    # @unittest.skip("")
    def test_all_endpoint_duplicates(self):
        """ Testing /api/all endpoint has no duplicate subdivision objects. """
#1.)
        for country_code, subdiv in self.test_request_all.json().items():
            subdivision_dicts = list(subdiv.values())
            unique_subdivisions = {json.dumps(subd, sort_keys=True) for subd in subdivision_dicts}
            self.assertEqual(len(unique_subdivisions), len(subdivision_dicts), f"Duplicates found in subdivision objects for country {country_code}:\n{subdiv}")

    # @unittest.skip("")
    def test_json_schema_all_endpoint(self):
        """ Testing the schema format of the ISO 3166-2 JSON object from the /all endpoint. """
        schema = {
            "type": "object",
            "patternProperties": {
                "^[A-Z]{2}$": {  # Country code like VE, US, GB
                    "type": "object",
                    "patternProperties": {
                        "^[A-Z]{2,3}-[A-Z0-9]{1,}$": {  # Subdivision code like VE-A, GB-ENG
                            "type": "object",
                            "properties": {
                                "flag": {"type": ["string", "null"]},
                                "latLng": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "minItems": 2,
                                    "maxItems": 2,
                                },
                                "localOtherName": {"type": ["string", "null"]},
                                "name": {"type": "string"},
                                "parentCode": {"type": ["string", "null"]},
                                "type": {"type": "string"},
                                "history": {"type": ["array", "null"]},
                            },
                            "required": ["name", "type", "latLng"],
                            "additionalProperties": False,
                        }
                    },
                    "additionalProperties": False,
                }
            },
            "additionalProperties": False,
        }
        try:
            validate(instance=self.test_request_all.json(), schema=schema)
        except ValidationError as e:
            self.fail(f"JSON schema for /all endpoint output validation failed: {e.message}.")

    # @unittest.skip("")
    def test_all_endpoint_individual_totals(self):
        """ Testing individual country-level subdivision totals from /api/all endpoint. """
        #expected subdivision counts per country
        expected_counts = {
            'AD': 7, 'AE': 7, 'AF': 34, 'AG': 8, 'AI': 0, 'AL': 12, 'AM': 11, 'AO': 18, 'AQ': 0, 'AR': 24,
            'AS': 0, 'AT': 9, 'AU': 8, 'AW': 0, 'AX': 0, 'AZ': 78, 'BA': 3, 'BB': 11, 'BD': 72, 'BE': 13,
            'BF': 58, 'BG': 28, 'BH': 4, 'BI': 18, 'BJ': 12, 'BL': 0, 'BM': 0, 'BN': 4, 'BO': 9, 'BQ': 3,
            'BR': 27, 'BS': 32, 'BT': 20, 'BV': 0, 'BW': 16, 'BY': 7, 'BZ': 6, 'CA': 13, 'CC': 0, 'CD': 26,
            'CF': 17, 'CG': 12, 'CH': 26, 'CI': 14, 'CK': 0, 'CL': 16, 'CM': 10, 'CN': 34, 'CO': 33,
            'CR': 7, 'CU': 16, 'CV': 24, 'CW': 0, 'CX': 0, 'CY': 6, 'CZ': 90, 'DE': 16, 'DJ': 6, 'DK': 5,
            'DM': 10, 'DO': 42, 'DZ': 58, 'EC': 24, 'EE': 94, 'EG': 27, 'EH': 0, 'ER': 6, 'ES': 69, 'ET': 13,
            'FI': 19, 'FJ': 19, 'FK': 0, 'FM': 4, 'FO': 0, 'FR': 124, 'GA': 9, 'GB': 224, 'GD': 7, 'GE': 12,
            'GF': 0, 'GG': 0, 'GH': 16, 'GI': 0, 'GL': 5, 'GM': 6, 'GN': 41, 'GP': 0, 'GQ': 10, 'GR': 14,
            'GS': 0, 'GT': 22, 'GU': 0, 'GW': 12, 'GY': 10, 'HK': 0, 'HM': 0, 'HN': 18, 'HR': 21, 'HT': 10,
            'HU': 43, 'ID': 45, 'IE': 30, 'IL': 6, 'IM': 0, 'IN': 36, 'IO': 0, 'IQ': 19, 'IR': 31, 'IS': 72,
            'IT': 126, 'JE': 0, 'JM': 14, 'JO': 12, 'JP': 47, 'KE': 47, 'KG': 9, 'KH': 25, 'KI': 3, 'KM': 3,
            'KN': 16, 'KP': 13, 'KR': 17, 'KW': 6, 'KY': 0, 'KZ': 20, 'LA': 18, 'LB': 8, 'LC': 10, 'LI': 11,
            'LK': 34, 'LR': 15, 'LS': 10, 'LT': 70, 'LU': 12, 'LV': 43, 'LY': 22, 'MA': 87, 'MC': 17,
            'MD': 37, 'ME': 25, 'MF': 0, 'MG': 6, 'MH': 26, 'MK': 80, 'ML': 11, 'MM': 15, 'MN': 22, 'MO': 0,
            'MP': 0, 'MQ': 0, 'MR': 15, 'MS': 0, 'MT': 68, 'MU': 12, 'MV': 21, 'MW': 31, 'MX': 32, 'MY': 16,
            'MZ': 11, 'NA': 14, 'NC': 0, 'NE': 8, 'NF': 0, 'NG': 37, 'NI': 17, 'NL': 18, 'NO': 13, 'NP': 7,
            'NR': 14, 'NU': 0, 'NZ': 17, 'OM': 11, 'PA': 14, 'PE': 26, 'PF': 0, 'PG': 22, 'PH': 99, 'PK': 7,
            'PL': 16, 'PM': 0, 'PN': 0, 'PR': 0, 'PS': 16, 'PT': 20, 'PW': 16, 'PY': 18, 'QA': 8, 'RE': 0,
            'RO': 42, 'RS': 32, 'RU': 83, 'RW': 5, 'SA': 13, 'SB': 10, 'SC': 27, 'SD': 18, 'SE': 21, 'SG': 5,
            'SH': 3, 'SI': 212, 'SJ': 0, 'SK': 8, 'SL': 5, 'SM': 9, 'SN': 14, 'SO': 18, 'SR': 10, 'SS': 10,
            'ST': 7, 'SV': 14, 'SX': 0, 'SY': 14, 'SZ': 4, 'TC': 0, 'TD': 23, 'TF': 0, 'TG': 5, 'TH': 78,
            'TJ': 5, 'TK': 0, 'TL': 13, 'TM': 6, 'TN': 24, 'TO': 5, 'TR': 81, 'TT': 15, 'TV': 8, 'TW': 22,
            'TZ': 31, 'UA': 27, 'UG': 139, 'UM': 9, 'US': 57, 'UY': 19, 'UZ': 14, 'VA': 0, 'VC': 6, 'VE': 25,
            'VG': 0, 'VI': 0, 'VN': 63, 'VU': 6, 'WF': 3, 'WS': 11, 'XK': 0, 'YE': 22, 'YT': 0, 'ZA': 9,
            'ZM': 10, 'ZW': 10
        }
#1.)
        for code, expected_count in expected_counts.items():
            actual_count = len(self.test_request_all.json().get(code, []))
            self.assertEqual(actual_count, expected_count, 
                f"Incorrect subdivision total for code {code}. Expected {expected_count}, got {actual_count}.")

    # @unittest.skip("")
    def test_all_endpoint_null_values(self):
        """ Testing for all subdivision objects, the name and type attributes are not None. """
#1.)
        test_request_all = self.test_request_all.json()
        for alpha2 in list(test_request_all.keys()):
            for subd in test_request_all[alpha2]:
                self.assertIsNotNone(test_request_all[alpha2][subd]["name"], 
                    f"Expected subdivision name to not be None, got {test_request_all[alpha2][subd]['name']}.")
                self.assertIsNotNone(test_request_all[alpha2][subd]["type"], 
                    f"Expected subdivision type to not be None, got {test_request_all[alpha2][subd]['type']}.")
            
    # @unittest.skip("")
    def test_all_endpoint_parent_codes(self):
        """ Testing that for all subdivisions their parent codes are valid codes within the subdivision object. """
#1.)
        test_request_all = self.test_request_all.json()
        for alpha2 in list(test_request_all.keys()):
            for subd in test_request_all[alpha2]:
                if not (test_request_all[alpha2][subd]["parentCode"] is None):
                    self.assertIn(test_request_all[alpha2][subd]["parentCode"], list(test_request_all[alpha2].keys()), 
                        f"Parent code for {subd} ({test_request_all[alpha2][subd]['parentCode']}) not found in list of subdivision codes for {alpha2}:\n{list(test_request_all[alpha2].keys())}.")

    # @unittest.skip("")
    def test_alpha_endpoint(self):
        """ Testing /alpha endpoint, return all ISO 3166 subdivision data from input alpha-2, alpha-3 or numeric code/codes. """
        test_alpha2_au = "AU" #Australia
        test_alpha3_lux = "LUX" #Luxembourg
        test_alpha3_pa_rw = "PAN, RWA" #Panama, Rwanda
        test_numeric_740_752 = "740, 752" #Suriname, Sweden
        test_alpha2_alpha3_numeric_ir_kgz_446 = "IR, KGZ, 446" #Iran, Kyrgyzstan, Macao
        test_alpha2_filter_au = "name"     #testing filter query string parameter
        test_alpha3_filter_lux = "type, parentCode, flag" 
        test_alpha_error_1 = "ABCDE"
        test_alpha_error_2 = "12345"
        test_alpha_error_3 = ""
#1.)
        test_alpha_request_au = requests.get(self.alpha_base_url + test_alpha2_au, headers=self.user_agent_header).json() #Australia

        self.assertEqual(list(test_alpha_request_au.keys()), ["AU-ACT", "AU-NSW", "AU-NT", "AU-QLD", "AU-SA", "AU-TAS", "AU-VIC", "AU-WA"], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_alpha_request_au.keys())}.")   
        for subd in test_alpha_request_au:            
            if not (test_alpha_request_au[subd]["flag"] is None):
                self.assertEqual(os.path.splitext(test_alpha_request_au[subd]["flag"])[0], self.flag_base_url + "AU/" + subd, 
                    f"Expected flag URL to be {self.flag_base_url + 'AU/' + subd}, got {os.path.splitext(test_alpha_request_au[subd]['flag'])[0]}.") 
                self.assertEqual(requests.get(test_alpha_request_au[subd]["flag"], headers=self.user_agent_header).status_code, 200, 
                    f"Flag URL invalid: {test_alpha_request_au[subd]['flag']}.")
            for key in list(test_alpha_request_au[subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, f"Attribute {key} not found in list of correct attributes:\n{self.correct_subdivision_keys}.")

        #AU-NSW - New South Wales 
        test_alpha_request_au_nsw_expected = {"name": "New South Wales", "localOtherName": "NSW (eng), The First State (eng), The Premier State (eng)", "parentCode": None, "type": "State", 
                    "latLng": [-31.253, 146.921], "flag": "https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/AU/AU-NSW.svg", 
                    "history": ["2004-03-08: Codes: New South Wales: AU-NS -> AU-NSW. Queensland: AU-QL -> AU-QLD. Tasmania: AU-TS -> AU-TAS. Victoria: AU-VI -> AU-VIC. Australian Capital Territory: AU-CT -> AU-ACT. Description of Change: Change of subdivision code in accordance with Australian Standard AS 4212-1994. Source: Newsletter I-6 - https://web.archive.org/web/20081218103224/http://www.iso.org/iso/iso_3166-2_newsletter_i-6_en.pdf."]}      
        self.assertEqual(test_alpha_request_au["AU-NSW"], test_alpha_request_au_nsw_expected, 
                f"Expected subdivision object doesn't match observed object:\n{test_alpha_request_au['AU-NSW']}.")
        #AU-QLD - Queensland
        test_alpha_request_au_qld_expected = {"name": "Queensland", "localOtherName": "Qld (eng), The Sunshine State (eng)", "parentCode": None, "type": "State", 
                "latLng": [-22.575, 144.085], "flag": "https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/AU/AU-QLD.svg",
                "history": ["2004-03-08: Codes: New South Wales: AU-NS -> AU-NSW. Queensland: AU-QL -> AU-QLD. Tasmania: AU-TS -> AU-TAS. Victoria: AU-VI -> AU-VIC. Australian Capital Territory: AU-CT -> AU-ACT. Description of Change: Change of subdivision code in accordance with Australian Standard AS 4212-1994. Source: Newsletter I-6 - https://web.archive.org/web/20081218103224/http://www.iso.org/iso/iso_3166-2_newsletter_i-6_en.pdf."]} 
        self.assertEqual(test_alpha_request_au["AU-QLD"], test_alpha_request_au_qld_expected, 
                f"Expected subdivision object doesn't match observed object:\n{test_alpha_request_au['AU-QLD']}.")
#2.) 
        test_alpha_request_lux = requests.get(self.alpha_base_url + test_alpha3_lux, headers=self.user_agent_header).json() #Luxembourg

        self.assertEqual(list(test_alpha_request_lux.keys()), ["LU-CA", "LU-CL", "LU-DI", "LU-EC", "LU-ES", "LU-GR", "LU-LU", "LU-ME", "LU-RD", "LU-RM", "LU-VD", "LU-WI"], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_alpha_request_lux.keys())}.")   
        for subd in test_alpha_request_lux:
            if not (test_alpha_request_lux[subd]["flag"] is None):
                self.assertEqual(os.path.splitext(test_alpha_request_lux[subd]["flag"])[0], self.flag_base_url + "LU/" + subd, 
                    f"Expected flag URL to be {self.flag_base_url + 'LUX/' + subd}, got {os.path.splitext(test_alpha_request_lux[subd]['flag'])[0]}.") 
                self.assertEqual(requests.get(test_alpha_request_lux[subd]["flag"], headers=self.user_agent_header).status_code, 200, 
                    f"Flag URL invalid: {test_alpha_request_lux[subd]['flag']}.")
            for key in list(test_alpha_request_lux[subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, f"Attribute {key} not found in list of correct attributes:\n{self.correct_subdivision_keys}.") 

        #LU-CA - Capellen
        test_alpha_request_lux_ca_expected = {"name": "Capellen", "localOtherName": "Capellen (deu), Kapellen (ltz)", "parentCode": None, "type": "Canton", 
                "latLng": [49.646, 5.991], "flag": None,
                "history": ["2015-11-27: Addition of cantons LU-CA, LU-CL, LU-DI, LU-EC, LU-ES, LU-GR, LU-LU, LU-ME, LU-RD, LU-RM, LU-VD, LU-WI; update List Source. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:LU."]} 
        self.assertEqual(test_alpha_request_lux["LU-CA"], test_alpha_request_lux_ca_expected, 
                f"Expected subdivision object doesn't match observed object:\n{test_alpha_request_lux['LU-CA']}.")
        
        #LU-WI - Luxembourg
        test_alpha_request_lux_wi_expected = {"name": "Wiltz", "localOtherName": "Wiltz (deu), Wolz (ltz)", "parentCode": None, "type": "Canton", 
                "latLng": [49.966, 5.932], "flag": "https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/LU/LU-WI.svg",
                "history": ['2015-11-27: Addition of cantons LU-CA, LU-CL, LU-DI, LU-EC, LU-ES, LU-GR, LU-LU, LU-ME, LU-RD, LU-RM, LU-VD, LU-WI; update List Source. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:LU.']} 
        self.assertEqual(test_alpha_request_lux["LU-WI"], test_alpha_request_lux_wi_expected, 
                f"Expected subdivision object doesn't match observed object:\n{test_alpha_request_lux['LU-WI']}.")
#3.)
        test_alpha_request_pa_rw = requests.get(self.alpha_base_url + test_alpha3_pa_rw, headers=self.user_agent_header).json() #Panama and Rwanda

        self.assertEqual(list(test_alpha_request_pa_rw.keys()), ["PA", "RW"], 
            f"Expected output object of API to contain only the PA and RW keys, got {list(test_alpha_request_pa_rw.keys())}.")
        self.assertEqual(list(test_alpha_request_pa_rw["PA"].keys()), ["PA-1", "PA-10", "PA-2", "PA-3", "PA-4", "PA-5", "PA-6", "PA-7", "PA-8", "PA-9", "PA-EM", "PA-KY", "PA-NB", "PA-NT"], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_alpha_request_pa_rw['PA'].keys())}.")   
        self.assertEqual(list(test_alpha_request_pa_rw["RW"].keys()), ["RW-01", "RW-02", "RW-03", "RW-04", "RW-05"], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_alpha_request_pa_rw['RW'].keys())}.")   
        for subd in test_alpha_request_pa_rw["PA"]:
            if not (test_alpha_request_pa_rw["PA"][subd]["flag"] is None):
                self.assertEqual(os.path.splitext(test_alpha_request_pa_rw["PA"][subd]["flag"])[0], self.flag_base_url + "PA/" + subd, 
                    f"Expected flag URL to be {self.flag_base_url + 'PA/' + subd}, got {os.path.splitext(test_alpha_request_pa_rw['PA'][subd]['flag'][0])}.") 
                self.assertEqual(requests.get(test_alpha_request_pa_rw["PA"][subd]["flag"], headers=self.user_agent_header).status_code, 200, 
                    f"Flag URL invalid: {test_alpha_request_pa_rw['PA'][subd]['flag']}.")
            for key in list(test_alpha_request_pa_rw["PA"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, f"Attribute {key} not found in list of correct attributes:\n{self.correct_subdivision_keys}.") 
        for subd in test_alpha_request_pa_rw["RW"]:
            if not (test_alpha_request_pa_rw["RW"][subd]["flag"] is None):
                self.assertEqual(os.path.splitext(test_alpha_request_pa_rw["RW"][subd]["flag"])[0], self.flag_base_url + "RW/" + subd, 
                    f"Expected flag URL to be {self.flag_base_url + 'RW/' + subd}, got {os.path.splitext(test_alpha_request_pa_rw['RW'][subd]['flag'])[0]}.") 
                self.assertEqual(requests.get(test_alpha_request_pa_rw["RW"][subd]["flag"], headers=self.user_agent_header).status_code, 200, 
                    f"Flag URL invalid: {test_alpha_request_pa_rw['RW'][subd]['flag']}.")
            for key in list(test_alpha_request_pa_rw["RW"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, f"Attribute {key} not found in list of correct attributes:\n{self.correct_subdivision_keys}.") 

        #PA-4 - Chiriquí
        test_alpha_request_pa_4_expected = {"name": "Chiriquí", "localOtherName": "Chiriqui (eng)", "parentCode": None, "type": "Province", 
                "latLng": [8.387, -82.28], "flag": "https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-4.svg", "history": None} 
        self.assertEqual(test_alpha_request_pa_rw["PA"]["PA-4"], test_alpha_request_pa_4_expected, 
                f"Expected subdivision object doesn't match observed object:\n{test_alpha_request_pa_rw['PA']['PA-4']}.")
        #RW-03 - Northern 
        test_alpha_request_rw_03_expected = {"name": "Northern", "localOtherName": "Nord (fra), Amajyaruguru (kin), Noordelijke (nld)", "parentCode": None, "type": "Province", 
                "latLng": [-1.656, 29.882], "flag": None, "history": ["2015-11-27: Change of spelling of RW-01, RW-02, RW-03, RW-04, RW-05; addition of category name in kin; update List Source. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:RW."]} 
        self.assertEqual(test_alpha_request_pa_rw["RW"]["RW-03"], test_alpha_request_rw_03_expected, 
                f"Expected subdivision object doesn't match observed object:\n{test_alpha_request_pa_rw['RW']['RW-03']}.")
#4.)
        test_alpha_request_740_752  = requests.get(self.alpha_base_url + test_numeric_740_752, headers=self.user_agent_header).json() #740 - Suriname, 752 - Sweden

        self.assertEqual(list(test_alpha_request_740_752.keys()), ["SE", "SR"], 
            f"Expected output object of API to contain SR and SE keys, got {list(test_alpha_request_740_752.keys())}.")
        self.assertEqual(list(test_alpha_request_740_752["SE"].keys()), ['SE-AB', 'SE-AC', 'SE-BD', 'SE-C', 'SE-D', 'SE-E', 'SE-F', 'SE-G', 'SE-H', 'SE-I', 'SE-K', \
                                                                   'SE-M', 'SE-N', 'SE-O', 'SE-S', 'SE-T', 'SE-U', 'SE-W', 'SE-X', 'SE-Y', 'SE-Z'], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_alpha_request_740_752['SE'].keys())}.")   
        self.assertEqual(list(test_alpha_request_740_752["SR"].keys()), ["SR-BR", "SR-CM", "SR-CR", "SR-MA", "SR-NI", "SR-PM", "SR-PR", "SR-SA", "SR-SI", "SR-WA"], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_alpha_request_740_752['SR'].keys())}.")   
        for subd in test_alpha_request_740_752["SR"]:
            if not (test_alpha_request_740_752["SR"][subd]["flag"] is None):
                self.assertEqual(os.path.splitext(test_alpha_request_740_752["SR"][subd]["flag"])[0], self.flag_base_url + "SR/" + subd, 
                    f"Expected flag URL to be {self.flag_base_url + 'SR/' + subd}, got {os.path.splitext(test_alpha_request_740_752['SR'][subd]['flag'])[0]}.") 
                self.assertEqual(requests.get(test_alpha_request_740_752["SR"][subd]["flag"], headers=self.user_agent_header).status_code, 200, 
                    f"Flag URL invalid: {test_alpha_request_740_752['SR'][subd]['flag']}.")
            for key in list(test_alpha_request_740_752["SR"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, f"Attribute {key} not found in list of correct attributes:\n{self.correct_subdivision_keys}.") 
        for subd in test_alpha_request_740_752["SE"]:
            if not (test_alpha_request_740_752["SE"][subd]["flag"] is None):
                self.assertEqual(os.path.splitext(test_alpha_request_740_752["SE"][subd]["flag"])[0], self.flag_base_url + "SE/" + subd, 
                    f"Expected flag URL to be {self.flag_base_url + 'SE/' + subd}, got {os.path.splitext(test_alpha_request_740_752['SE'][subd]['flag'])[0]}.") 
                self.assertEqual(requests.get(test_alpha_request_740_752["SE"][subd]["flag"], headers=self.user_agent_header).status_code, 200, 
                    f"Flag URL invalid: {test_alpha_request_740_752['SE'][subd]['flag']}.")
            for key in list(test_alpha_request_740_752["SE"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, f"Attribute {key} not found in list of correct attributes:\n{self.correct_subdivision_keys}.") 

        #SR-SI - Sipaliwini
        test_alpha_request_740_752_expected = {"name": "Sipaliwini", "localOtherName": None, "parentCode": None, "type": "District", 
                "latLng": [3.657, -56.204], "flag": None, "history": None} 
        self.assertEqual(test_alpha_request_740_752["SR"]["SR-SI"], test_alpha_request_740_752_expected, 
                f"Expected subdivision object doesn't match observed object:\n{test_alpha_request_740_752['SR']['SR-SI']}.")
        #SE-I - Gotlands
        test_alpha_request_740_752_expected = {"name": "Gotlands län [SE-09]", "localOtherName": "Gotland (eng)", "parentCode": None, "type": "County", 
                "latLng": [57.531, 18.69], "flag": "https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/SE/SE-I.svg", "history": None} 
        self.assertEqual(test_alpha_request_740_752["SE"]["SE-I"], test_alpha_request_740_752_expected, 
                f"Expected subdivision object doesn't match observed object:\n{test_alpha_request_740_752['SE']['SE-I']}.")
#5.)
        test_alpha_request_ir_kgz_446  = requests.get(self.alpha_base_url + test_alpha2_alpha3_numeric_ir_kgz_446, headers=self.user_agent_header).json() #Iran, Kyrgyzstan, Macao

        self.assertEqual(list(test_alpha_request_ir_kgz_446.keys()), ["IR", "KG", "MO"], 
            f"Expected output object of API to contain IT, KG and MO keys, got {list(test_alpha_request_ir_kgz_446.keys())}.")
        self.assertEqual(list(test_alpha_request_ir_kgz_446["IR"].keys()), ['IR-00', 'IR-01', 'IR-02', 'IR-03', 'IR-04', 'IR-05', 'IR-06', 'IR-07', 'IR-08', 'IR-09', 'IR-10', 'IR-11', 'IR-12', 'IR-13', 'IR-14', \
                                                                      'IR-15', 'IR-16', 'IR-17', 'IR-18', 'IR-19', 'IR-20', 'IR-21', 'IR-22', 'IR-23', 'IR-24', 'IR-25', 'IR-26', 'IR-27', 'IR-28', 'IR-29', 'IR-30'], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_alpha_request_ir_kgz_446['IR'].keys())}.")   
        self.assertEqual(list(test_alpha_request_ir_kgz_446["KG"].keys()), ['KG-B', 'KG-C', 'KG-GB', 'KG-GO', 'KG-J', 'KG-N', 'KG-O', 'KG-T', 'KG-Y'], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_alpha_request_ir_kgz_446['KG'].keys())}.")   
        self.assertEqual(list(test_alpha_request_ir_kgz_446["MO"].keys()), [], "Expected no subdivision codes in output object.") 
        
        for subd in test_alpha_request_ir_kgz_446["IR"]:
            if not (test_alpha_request_ir_kgz_446["IR"][subd]["flag"] is None):
                self.assertEqual(os.path.splitext(test_alpha_request_ir_kgz_446["IR"][subd]["flag"])[0], self.flag_base_url + "IR/" + subd, 
                    f"Expected flag URL to be {self.flag_base_url + 'IR/' + subd}, got {os.path.splitext(test_alpha_request_ir_kgz_446['IR'][subd]['flag'])[0]}.") 
                self.assertEqual(requests.get(test_alpha_request_ir_kgz_446["IR"][subd]["flag"], headers=self.user_agent_header).status_code, 200, 
                    f"Flag URL invalid: {test_alpha_request_ir_kgz_446['IR'][subd]['flag']}.")
            for key in list(test_alpha_request_ir_kgz_446["IR"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, f"Attribute {key} not found in list of correct attributes:\n{self.correct_subdivision_keys}.") 
        for subd in test_alpha_request_ir_kgz_446["KG"]:
            if not (test_alpha_request_ir_kgz_446["KG"][subd]["flag"] is None):
                self.assertEqual(os.path.splitext(test_alpha_request_ir_kgz_446["KG"][subd]["flag"])[0], self.flag_base_url + "KG/" + subd, 
                    f"Expected flag URL to be {self.flag_base_url + 'KG/' + subd}, got {os.path.splitext(test_alpha_request_ir_kgz_446['KG'][subd]['flag'])[0]}.") 
                self.assertEqual(requests.get(test_alpha_request_ir_kgz_446["KG"][subd]["flag"], headers=self.user_agent_header).status_code, 200, 
                    f"Flag URL invalid: {test_alpha_request_ir_kgz_446['KG'][subd]['flag']}.")
            for key in list(test_alpha_request_ir_kgz_446["KG"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, f"Attribute {key} not found in list of correct attributes:\n{self.correct_subdivision_keys}.") 
#6.)
        test_alpha_request_au_filter = requests.get(self.alpha_base_url + test_alpha2_au, headers=self.user_agent_header, params={"filter": test_alpha2_filter_au}).json() #Australia - filtering out all attributes but name
        
        self.assertEqual(list(test_alpha_request_au_filter.keys()), ["AU-ACT", "AU-NSW", "AU-NT", "AU-QLD", "AU-SA", "AU-TAS", "AU-VIC", "AU-WA"], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_alpha_request_au.keys())}.")   
        for subd in test_alpha_request_au_filter:
            self.assertEqual(list(test_alpha_request_au_filter[subd].keys()), ["name"], 
                f"Expected subdivision attributes to just include the name attribute, got {list(test_alpha_request_au_filter.keys())}.")
#7.)
        test_alpha_request_lux_filter = requests.get(self.alpha_base_url + test_alpha3_lux, headers=self.user_agent_header, params={"filter": test_alpha3_filter_lux}).json() #Luxembourg - filtering out all attributes but type, parentCode and flag
        
        self.assertEqual(list(test_alpha_request_lux_filter.keys()), ["LU-CA", "LU-CL", "LU-DI", "LU-EC", "LU-ES", "LU-GR", "LU-LU", "LU-ME", "LU-RD", "LU-RM", "LU-VD", "LU-WI"], 
            f"Expected list of subdivision codes doesn't match output:\n{list(test_alpha_request_lux_filter.keys())}.")   
        for subd in test_alpha_request_lux_filter:
            self.assertEqual(list(test_alpha_request_lux_filter[subd].keys()), ["flag", "parentCode", "type"], 
                f"Expected subdivision attributes to just include the type, parentCode and flag attributes, got {list(test_alpha_request_lux_filter[subd].keys())}.")
#8.)
        test_alpha_request_pa_rw_filter_all = requests.get(self.alpha_base_url + test_alpha3_pa_rw, headers=self.user_agent_header, params={"filter": "*"}).json()  #PA, RW - including all attributes via the wildcard '*' symbol
        
        self.assertEqual(list(test_alpha_request_pa_rw_filter_all.keys()), ["PA", "RW"], 
            f"Expected output object of API to contain only the PA and RW keys, got {list(test_alpha_request_pa_rw_filter_all.keys())}.")
        for alpha2 in test_alpha_request_pa_rw_filter_all:
            for subd in test_alpha_request_pa_rw_filter_all[alpha2]:
                self.assertEqual(list(test_alpha_request_pa_rw_filter_all[alpha2][subd].keys()), ['flag', 'history', 'latLng', 'localOtherName', 'name', 'parentCode', 'type'], 
                    f"Expected subdivision attributes to include all available attributes, got {list(test_alpha_request_pa_rw_filter_all[alpha2][subd].keys())}.")
#9.) 
        test_alpha_request_error1 = requests.get(self.alpha_base_url + test_alpha_error_1, headers=self.user_agent_header).json() #ABCDE
        test_alpha_request_error1_expected = {"message": f"Invalid ISO 3166-1 country code input {test_alpha_error_1}.", "path": self.alpha_base_url + test_alpha_error_1, "status": 400}
        self.assertEqual(test_alpha_request_error1, test_alpha_request_error1_expected, f"Expected and observed output error object do not match:\n{test_alpha_request_error1}.")
#10.)
        test_alpha_request_error2 = requests.get(self.alpha_base_url + test_alpha_error_2, headers=self.user_agent_header).json() #12345
        test_alpha_request_error2_expected = {"message": f"Invalid ISO 3166-1 country code input {test_alpha_error_2}.", "path": self.alpha_base_url + test_alpha_error_2, "status": 400}
        self.assertEqual(test_alpha_request_error2, test_alpha_request_error2_expected, f"Expected and observed output error object do not match:\n{test_alpha_request_error2}.")
#11.)
        test_alpha_request_error3 = requests.get(self.alpha_base_url + test_alpha_error_3, headers=self.user_agent_header).json() #""
        test_alpha_request_error3_expected = {"message": "The ISO 3166-1 alpha input parameter cannot be empty. Please pass in at least one alpha country code.", "path": self.alpha_base_url + test_alpha_error_3, "status": 400}
        self.assertEqual(test_alpha_request_error3, test_alpha_request_error3_expected, f"Expected and observed output error object do not match:\n{test_alpha_request_error3}.")
    
    # @unittest.skip("")
    def test_subdivision_endpoint(self):
        """ Testing /subdivision endpoint, return all ISO 3166 subdivision data from input subdivision code/codes. """
        test_subdivision_jm_05 = "JM-05"
        test_subdivision_pa_03 = "PA-3"
        test_subdivision_ss_ew = "SS-EW"
        test_subdivision_tv_nkf_nit_tj_du = "TV-NKF, tv-nit, TJ-DU"
        test_subdivision_filter_ss_ew = "name,latLng"   #testing filter query string parameter
        test_subdivision_filter_tv_nkf_nit_tj_du = "flag,localOtherName"
        test_subdivision_gb_xyz = "GB-XYZ"
        test_subdivision_xx_yy = "XX-YY"
#1.)
        test_subdivision_request_jm_05 = requests.get(self.subdivision_base_url + test_subdivision_jm_05, headers=self.user_agent_header).json() #JM-05 (Saint Mary)
        test_subdivision_request_jm_05_expected = {"JM": {"JM-05": {"name": "Saint Mary", "localOtherName": "Sent Mary (jam)", "parentCode": None, 
            "type": "Parish", "latLng": [18.309, -76.964], "flag": None, "history": None}}}
        
        self.assertEqual(test_subdivision_request_jm_05, test_subdivision_request_jm_05_expected, 
            f"Expected subdivision object doesn't match observed object:\n{test_subdivision_request_jm_05['JM']['JM-05']}")
#2)
        test_subdivision_request_pa_3 = requests.get(self.subdivision_base_url + test_subdivision_pa_03, headers=self.user_agent_header).json() #PA-3 - Colón
        test_subdivision_request_pa_3_expected = {"PA": {"PA-3": {"name": "Colón", "localOtherName": "Colon (eng)", "parentCode": None, 
            "type": "Province", "latLng": [9.359, -79.9], "flag": "https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-3.svg", "history": None}}}
        
        self.assertEqual(test_subdivision_request_pa_3, test_subdivision_request_pa_3_expected, 
            f"Expected subdivision object doesn't match observed object:\n{test_subdivision_request_pa_3['PA']['PA-3']}")
#3.)
        test_subdivision_request_ss_ew = requests.get(self.subdivision_base_url + test_subdivision_ss_ew, headers=self.user_agent_header).json() #SS-EW - Western Equatoria
        test_subdivision_request_ss_ew_expected = {"SS": {"SS-EW": {"name": "Western Equatoria", "localOtherName": "The Green State (eng)", "parentCode": None, 
            "type": "State", "latLng": [5.347, 28.299], "flag": "https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/SS/SS-EW.png", "history": None}}}

        self.assertEqual(test_subdivision_request_ss_ew, test_subdivision_request_ss_ew_expected, 
            f"Expected subdivision object doesn't match observed object:\n{test_subdivision_request_ss_ew['SS']['SS-EW']}")
#4.)
        test_subdivision_request_tv_nkf_nit_tj_du = requests.get(self.subdivision_base_url + test_subdivision_tv_nkf_nit_tj_du, headers=self.user_agent_header).json() #TV-NKF: Western Equatoria, TV-NIT: Niutao, TJ-DU: Dushanbe
        test_subdivision_request_tv_nkf_nit_tj_du_expected = {
            'TJ': {
                'TJ-DU': {
                    'flag': None,
                    'history': [
                        '2015-02-12: Removed the reference to Dushanbe in remark part 2; correct spelling of DU. '
                        '(Remark part 2: Remark: The deletion of the region Karategin left one part of the country without name '
                        'and without code in this part of ISO 3166. This section of the country is designated districts under '
                        'republic administration (tgk: nohiyahoi tobei jumhurí) and comprises 13 districts (tgk: nohiya) which '
                        'are administered directly by the central government at first-order level). Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:TJ.',
                        '2014-11-03: Subdivision added: TJ-DU. Description of Change: Add 1 capital territory TJ-DU. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:TJ.'
                    ],
                    'latLng': [38.56, 68.787],
                    'localOtherName': 'Душанбe (tgk), Душанбe (rus), Dushanbe (eng), Dyushambe (eng), Stalinabad (eng)',
                    'name': 'Dushanbe', 'parentCode': None, 'type': 'Capital territory'
                }
            },
            'TV': {
                'TV-NIT': {
                    'flag': None, 'history': None, 'latLng': [-6.106, 177.344],
                    'localOtherName': None, 'name': 'Niutao', 'parentCode': None, 'type': 'Island council'
                },
                'TV-NKF': {
                    'flag': None, 'history': None, 'latLng': [-8, 178.5],
                    'localOtherName': None, 'name': 'Nukufetau', 'parentCode': None, 'type': 'Island council'
                }
            }
        }

        self.assertEqual(test_subdivision_request_tv_nkf_nit_tj_du, test_subdivision_request_tv_nkf_nit_tj_du_expected, 
            f"Expected subdivision object doesn't match observed object:\n{test_subdivision_request_tv_nkf_nit_tj_du}")
#6.)
        test_subdivision_request_ss_ew_filter = requests.get(self.subdivision_base_url + test_subdivision_ss_ew, headers=self.user_agent_header, params={"filter": test_subdivision_filter_ss_ew}).json() #SS-EW - filtering out all attributes but name and latLng

        self.assertEqual(list(test_subdivision_request_ss_ew_filter.keys()), ["SS"], 
            f"Expected output object of API to contain only the SS key, got {list(test_subdivision_request_ss_ew_filter.keys())}.")
        self.assertEqual(list(test_subdivision_request_ss_ew_filter['SS']["SS-EW"].keys()), ["latLng", "name"], 
            f"Expected subdivision attributes to just include the name and latLng attributes, got {list(test_subdivision_request_ss_ew_filter.keys())}.")
#7.)
        test_subdivision_request_tv_nkf_nit_tj_du_filter = requests.get(self.subdivision_base_url + test_subdivision_tv_nkf_nit_tj_du, headers=self.user_agent_header, params={"filter": test_subdivision_filter_tv_nkf_nit_tj_du}).json() #TV-NKF, TV-NIT, TJ-DU - filtering out all attributes flag and localOtherName

        self.assertEqual(list(test_subdivision_request_tv_nkf_nit_tj_du_filter.keys()), ["TJ", "TV"], 
            f"Expected output object of API to contain only the TV and TJ keys, got {list(test_subdivision_request_tv_nkf_nit_tj_du_filter.keys())}.")
        self.assertEqual(list(test_subdivision_request_tv_nkf_nit_tj_du_filter['TV']["TV-NKF"].keys()), ["flag", "localOtherName"], 
            f"Expected subdivision attributes to just include the localOtherName and flag attributes, got {list(test_subdivision_request_tv_nkf_nit_tj_du_filter['TV']['TV-NKF'].keys())}.")
        self.assertEqual(list(test_subdivision_request_tv_nkf_nit_tj_du_filter['TV']["TV-NIT"].keys()), ["flag", "localOtherName"], 
            f"Expected subdivision attributes to just include the localOtherName and flag attributes, got {list(test_subdivision_request_tv_nkf_nit_tj_du_filter['TV']['TV-NIT'].keys())}.")
        self.assertEqual(list(test_subdivision_request_tv_nkf_nit_tj_du_filter['TJ']["TJ-DU"].keys()), ["flag", "localOtherName"], 
            f"Expected subdivision attributes to just include the localOtherName and flag attributes, got {list(test_subdivision_request_tv_nkf_nit_tj_du_filter['TJ']['TJ-DU'].keys())}.")
#8.)
        test_subdivision_request_pa_03_filter_all = requests.get(self.subdivision_base_url + test_subdivision_pa_03, headers=self.user_agent_header, params={"filter": "*"}).json()  #PA-3 - including all attributes via the wildcard '*' symbol

        self.assertEqual(list(test_subdivision_request_pa_03_filter_all.keys()), ["PA"], 
            f"Expected output object of API to contain only the PA-3 key, got {list(test_subdivision_request_pa_03_filter_all.keys())}.")
        self.assertEqual(list(test_subdivision_request_pa_03_filter_all['PA']["PA-3"].keys()), ['flag', 'history', 'latLng', 'localOtherName', 'name', 'parentCode', 'type'], 
            f"Expected subdivision attributes to just include all available attributes, got {list(test_subdivision_request_pa_03_filter_all['PA']['PA-3'].keys())}.")
#9.)       
        test_subdivision_request_gb_xyz = requests.get(self.subdivision_base_url + test_subdivision_gb_xyz, headers=self.user_agent_header).json() #GB-XYZ
        test_subdivision_request_gb_xyz_expected = {"message": f"Subdivision code {test_subdivision_gb_xyz} not found in list of available subdivisions for GB.", "path": self.subdivision_base_url + test_subdivision_gb_xyz, "status": 400}
        self.assertEqual(test_subdivision_request_gb_xyz, test_subdivision_request_gb_xyz_expected, f"Expected and observed output error object do not match:\n{test_subdivision_gb_xyz}.")
#10.)
        test_subdivision_request_xx_yy = requests.get(self.subdivision_base_url + test_subdivision_xx_yy, headers=self.user_agent_header).json() #XX-YY
        test_subdivision_request_xx_yy_expected = {"message": f"Subdivision code {test_subdivision_xx_yy} not found in list of available subdivisions for XX.", "path": self.subdivision_base_url + test_subdivision_xx_yy, "status": 400}
        self.assertEqual(test_subdivision_request_xx_yy, test_subdivision_request_xx_yy_expected, f"Expected and observed output error object do not match:\n{test_subdivision_xx_yy}.")
#11.)
        # test_subdivision_request_invalid_attribute = requests.get(self.subdivision_base_url + test_subdivision_jm_05, headers=self.user_agent_header, params={"filter": "invalid_attribute"}).json() #invalid attribute input
        # test_subdivision_request_invalid_attribute_expected = {"message": f"Invalid attribute name input to filter query string parameter: invalid_attribute. Refer to the list of supported attributes: name, localOtherName, type, parentCode, flag, latLng, history.", 
        #                                                        "path": f"{self.subdivision_base_url + test_subdivision_jm_05}?filter=invalid_attribute", "status": 400}
        # self.assertEqual(test_subdivision_request_invalid_attribute, test_subdivision_request_invalid_attribute_expected, f"Expected and observed output error object do not match:\n{test_subdivision_request_invalid_attribute}.")
 
    # @unittest.skip("")
    def test_search_endpoint(self):
        """ Testing /search endpoint, return all ISO 3166 subdivision data from input subdivision search terms. """
        test_search_name_azua = "Azua" #DO-02
        test_search_name_cakaudrove = "Cakaudrove" #FJ-03
        test_search_name_gelderland_overijssel = "Gelderland, Overijssel" #NL-GE, NL-OV
        test_search_name_ciudad = "Ciudad"
        test_search_name_south = "South"
        test_search_name_madrid_armaghcity = "Madrid, Comunidad de, Armagh City, Banbridge and Craigavon" #ES-MD, GB-ABC
        test_search_name_cakaudrove_filter = "type"    #testing filter query string parameter
        test_search_name_gelderland_overijssel_filter = "name,flag"
        test_search_name_error1 = "blahblahblah"
        test_search_name_error2 = "1234"
        test_search_name_error3 = ""
#1.)    
        test_search_name_request_azua = requests.get(self.search_base_url + test_search_name_azua, headers=self.user_agent_header).json() #DO-02 - Azua
        test_search_name_request_azua_expected = {"DO": {"DO-02": {"name": "Azua", "localOtherName": "Azua (eng)", "parentCode": "DO-41", 
            "type": "Province", "latLng": [18.453, -70.735], "flag": "https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/DO/DO-02.png", "history": None}}}

        self.assertEqual(test_search_name_request_azua, test_search_name_request_azua_expected, 
            f"Expected subdivision object doesn't match observed object:\n{test_search_name_request_azua}")
#2.)
        test_search_name_request_cakaudrove = requests.get(self.search_base_url + test_search_name_cakaudrove, headers=self.user_agent_header).json() #FJ-03 - Cakaudrove
        test_search_name_request_cakaudrove_expected = {"FJ": {"FJ-03": {"name": "Cakaudrove", "localOtherName": None, "parentCode": "FJ-N", 
            "type": "Province", "latLng": [-16.581, 179.512], "flag": None, "history": [
        "2016-11-15: Assign parent subdivision to FJ-01, FJ-02, FJ-03, FJ-04, FJ-05, FJ-06, FJ-07, FJ-08, FJ-09, FJ-10, FJ-11, FJ-12, FJ-13, FJ-14. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:FJ."]}}}

        self.assertEqual(test_search_name_request_cakaudrove, test_search_name_request_cakaudrove_expected, 
            f"Expected subdivision object doesn't match observed object:\n{test_search_name_request_cakaudrove}")
#3.)
        test_search_name_request_gelderland_overijssel = requests.get(self.search_base_url + test_search_name_gelderland_overijssel, headers=self.user_agent_header).json() #NL-GE - Gelderland, NL-OV - Overijssel
        test_search_name_request_gelderland_overijssel_expected = {'NL': {'NL-GE': {'flag': 'https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/NL/NL-GE.svg', 'history': None, 'latLng': [52.045, 5.872], 
            'localOtherName': 'Guelders (eng)', 'name': 'Gelderland', 'parentCode': None, 'type': 'Province'}, 'NL-OV': {'flag': 'https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/NL/NL-OV.svg', 
            'history': None, 'latLng': [52.439, 6.502], 'localOtherName': 'Oberyssel (deu), Oaveriessel (nds), Across the IJssel (eng)', 'name': 'Overijssel', 'parentCode': None, 'type': 'Province'}}}

        self.assertEqual(test_search_name_request_gelderland_overijssel, test_search_name_request_gelderland_overijssel_expected, 
            f"Expected subdivision object doesn't match observed object:\n{test_search_name_request_gelderland_overijssel}")
#4.)        
        test_search_name_request_ciudad_likeness = requests.get(self.search_base_url + test_search_name_ciudad, headers=self.user_agent_header, params={"likeness": "60", "excludeMatchScore": 0}).json() #Ciudad - likeness score of 60, include the Match Score attribute
        test_search_name_request_ciudad_likeness_expected = [{'countryCode': 'ES', 'flag': 'https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ES/ES-CR.svg', 'history': None, 'latLng': [38.985, -3.927], 'localOtherName': None, 'matchScore': 75, 
            'name': 'Ciudad Real', 'parentCode': 'ES-CM', 'subdivisionCode': 'ES-CR', 'type': 'Province'}, {'countryCode': 'AO', 'flag': None, 'history': None, 'latLng': [-5.571, 12.198], 'localOtherName': 'Kabinda (kon), Portuguese Congo (eng)', 'matchScore': 62, 'name': 'Cabinda', 
            'parentCode': None, 'subdivisionCode': 'AO-CAB', 'type': 'Province'}, {'countryCode': 'MX', 'flag': 'https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/MX/MX-CMX.png', 
            'history': ['2017-11-23: Typographical correction of MX-CMX; update List source. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:MX.', '2016-11-15: Change of subdivision code from MX-DIF to MX-CMX; change of name of MX-CMX, MX-COA, MX-MIC, MX-VER; addition of local variation of MX-COA, MX-MIC, MX-VER; update list source. Source: Online Browsing Platform (OBP) - https://www.iso.org/obp/ui/#iso:code:3166:MX.'], 
            'latLng': [19.433, -99.133], 'localOtherName': 'Mexico City (eng), CDMX (spa), Monda (oto), Mexihco Hueyaltepetl (nhn), U noj kaajil México (yua), CDMX (eng), La Ciudad de los Palacios (spa), The City of Palaces (eng)', 'matchScore': 60, 'name': 'Ciudad de México', 'parentCode': None, 'subdivisionCode': 'MX-CMX', 'type': 'Federal entity'}]

        self.assertEqual(test_search_name_request_ciudad_likeness, test_search_name_request_ciudad_likeness_expected, 
            f"Expected subdivision object doesn't match observed object:\n{test_search_name_request_ciudad_likeness}")
#5.)
        test_search_name_request_south_likeness_filter = requests.get(self.search_base_url + test_search_name_south, headers=self.user_agent_header, params={"likeness": "70", "filter": "name"}).json() #South - likeness score of 60, including only the name attribute
        test_search_name_request_south_likeness_filter_expected = {'BW': {'BW-SE': {'name': 'South East'}, 'BW-SO': {'name': 'Southern'}}, 'CM': {'CM-SU': {'name': 'South'}}, 'GB': {'GB-SLG': {'name': 'Slough'}, 'GB-SWK': {'name': 'Southwark'}}, 'IE': {'IE-LH': {'name': 'Louth'}}, 'NZ': {'NZ-STL': {'name': 'Southland'}}, 
                                                                    'RW': {'RW-05': {'name': 'Southern'}}, 'SG': {'SG-04': {'name': 'South East'}, 'SG-05': {'name': 'South West'}}, 'SL': {'SL-S': {'name': 'Southern'}}, 'ZM': {'ZM-07': {'name': 'Southern'}}}

        self.assertEqual(test_search_name_request_south_likeness_filter, test_search_name_request_south_likeness_filter_expected, f"Expected and observed output objects do not match:\n{test_search_name_request_south_likeness_filter}.")
#6.)
        test_search_name_request_madrid_armaghcity = requests.get(self.search_base_url + test_search_name_madrid_armaghcity, headers=self.user_agent_header, params={"filter": "flag,parentCode,type,localOtherName,latLng,name"}).json() #ES-MD - Madrid, GB-ABC - Armagh City, Banbridge and Craigavon, filter for all attributes except history
        test_search_name_request_madrid_armaghcity_es_md_expected = {'ES': {'ES-MD': {'flag': 'https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ES/ES-MD.svg', 'latLng': [40.417, -3.581], 'localOtherName': 'Community of Madrid (eng)', 'name': 'Madrid, Comunidad de', 'parentCode': None, 'type': 'Autonomous community'}}, 
                                                                     'GB': {'GB-ABC': {'flag': 'https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/GB/GB-ABC.png', 'latLng': [54.393, -6.456], 'localOtherName': "'Ard Mhacha, Droichead na Banna agus Creag Abhann (gle)', 'Airmagh, Bannbrig an Craigavon (ulst1239)'", 
                                                                                       'name': 'Armagh City, Banbridge and Craigavon', 'parentCode': 'GB-NIR', 'type': 'District'}}}

        self.assertEqual(test_search_name_request_madrid_armaghcity, test_search_name_request_madrid_armaghcity_es_md_expected, 
            f"Expected subdivision object doesn't match observed object:\n{test_search_name_request_madrid_armaghcity}")
#7.)
        test_search_name_request_cakaudrove_filter = requests.get(self.search_base_url + test_search_name_cakaudrove, headers=self.user_agent_header, params={"filter": test_search_name_cakaudrove_filter}).json() #FJ-03 - filtering out all attributes but type
        test_search_name_request_cakaudrove_filter_expected = {"FJ": {"FJ-03": {"type": "Province"}}}

        self.assertEqual(test_search_name_request_cakaudrove_filter, test_search_name_request_cakaudrove_filter_expected, f"Expected and observed output objects do not match:\n{test_search_name_request_cakaudrove_filter}.")
#8.)
        test_search_name_request_gelderland_overijssel_filter = requests.get(self.search_base_url + test_search_name_gelderland_overijssel, headers=self.user_agent_header, params={"filter": test_search_name_gelderland_overijssel_filter}).json()  #NL-GE, NL-OV - filtering out all attributes type and flag
        test_search_name_request_gelderland_overijssel_expected = {'NL': {'NL-GE': {'flag': 'https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/NL/NL-GE.svg', 'name': 'Gelderland'}, 'NL-OV': {'flag': 'https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/NL/NL-OV.svg', 'name': 'Overijssel'}}}

        self.assertEqual(test_search_name_request_gelderland_overijssel_filter, test_search_name_request_gelderland_overijssel_expected, f"Expected and observed output objects do not match:\n{test_search_name_request_gelderland_overijssel_filter}.")
#9.)
        test_search_name_request_ciudad_likenesss_filter_all = requests.get(self.search_base_url + test_search_name_ciudad, headers=self.user_agent_header, params={"filter": "*", "likeness": "50", "excludeMatchScore": 0}).json()  #Ciudad - including all attributes via the wildcard '*' symbol and a likeness score of 50%, include the Match Score in output
        
        observed_subdivision_codes = [item["subdivisionCode"] for item in test_search_name_request_ciudad_likenesss_filter_all]
        expected_subdivision_codes = ['ES-CR', 'AO-CAB', 'MX-CMX', 'ZW-MI', 'AZ-CUL', 'CO-CAU', 'DZ-09', 'ES-CE', 'JP-12', 'ME-05', 'ML-8', 'MT-11', 'MT-34', 'NR-07', 'PE-PIU', 'TO-03', 'US-ID', 'AZ-CAL', 'BD-12', 'BS-CI', 'CH-NW', 'MA-CHI', 'MX-CHH', 'SI-196', 'AO-LUA', 'BS-IN', 'CO-CAL', 'DM-03', 'DZ-21', 
                                      'ES-CU', 'ES-MU', 'ET-SI', 'GB-CMD', 'GB-SND', 'GD-02', 'GN-D', 'GN-KD', 'GT-20', 'LC-08', 'LV-022', 'LV-091', 'MA-ERR', 'MD-OC', 'MW-CR', 'MX-COL', 'NI-CI', 'PG-CPK', 'PH-IFU', 'PT-09', 'SI-036', 'TV-NIT', 'TW-CYI', 'TW-CYQ', 'UG-217', 'UG-218', 'UG-324', 'UG-417', 
                                      'VC-03', 'VE-L', 'YE-HU']
        
        self.assertEqual(observed_subdivision_codes, expected_subdivision_codes, 
            f"Expected output object of API does not contain the expected subdivision keys, got {observed_subdivision_codes}.")
      
        #iterate ovr all search results, validating correct keys/attributes
        expected_keys = {"flag", "latLng", "localOtherName", "name", "parentCode", "type", "history", "subdivisionCode", "countryCode", "matchScore"}
        for obj in test_search_name_request_ciudad_likenesss_filter_all:
            actual_keys = set(obj.keys())
            self.assertEqual(actual_keys, expected_keys, f"Expected keys {expected_keys}, but got {actual_keys} for subdivision {obj.get('subdivisionCode')}")
#10.)
        test_request_subdivision_name_error1 = requests.get(self.search_base_url + test_search_name_error1, headers=self.user_agent_header).json() #blahblahblah
        test_request_subdivision_name_error1_expected = {'Message': f"No matching subdivision data found with the given search term(s): {test_search_name_error1}. Try using the query string parameter '?likeness' and reduce the likeness score to expand the search space, '?likeness=30' will return subdivision data that have a 30% match to the input name. The current likeness score is set to 100."}
        self.assertEqual(test_request_subdivision_name_error1, test_request_subdivision_name_error1_expected, f"Expected and observed output error object do not match:\n{test_request_subdivision_name_error1}.")
#11.)
        test_request_subdivision_name_error2 = requests.get(self.search_base_url + test_search_name_error2, headers=self.user_agent_header).json() #1234        
        test_request_subdivision_name_error2_expected = {'Message': f"No matching subdivision data found with the given search term(s): {test_search_name_error2}. Try using the query string parameter '?likeness' and reduce the likeness score to expand the search space, '?likeness=30' will return subdivision data that have a 30% match to the input name. The current likeness score is set to 100."}
        self.assertEqual(test_request_subdivision_name_error2, test_request_subdivision_name_error2_expected, f"Expected and observed output error object do not match:\n{test_request_subdivision_name_error2}.")
#12.)
        test_request_subdivision_name_error3 = requests.get(self.search_base_url + test_search_name_error3, headers=self.user_agent_header).json() #""        
        test_request_subdivision_name_error3_expected = {'message': 'The search input parameter cannot be empty. Please pass in at least one search term.', 'path': 'https://iso3166-2-api.vercel.app/api/search/', 'status': 400}
        self.assertEqual(test_request_subdivision_name_error3, test_request_subdivision_name_error3_expected, f"Expected and observed output error object do not match:\n{test_request_subdivision_name_error3}.")
#13.)
        # test_request_subdivision_name_invalid_attribute = requests.get(self.search_base_url + test_search_name_azua, headers=self.user_agent_header, params={"filter": "invalid_attribute"}).json() #invalid attribute input  
        # test_request_subdivision_name_invalid_attribute_expected = {'message': 'Invalid attribute name input to filter query string parameter: invalid_attribute. Refer to the following list of supported attributes: name, localOtherName, type, parentCode, flag, latLng, history, matchScore, countryCode, subdivisionCode, matchScore, countryCode, subdivisionCode.', 
        #                                                              'path': 'https://iso3166-2-api.vercel.app/api/all', 'status': 400}
        # self.assertEqual(test_request_subdivision_name_invalid_attribute, test_request_subdivision_name_invalid_attribute_expected, f"Expected and observed output error object do not match:\n{test_request_subdivision_name_invalid_attribute}.")

    # @unittest.skip("Skipping /country_name endpoint tests.") 
    def test_country_name_endpoint(self):
        """ Testing /country_name endpoint, return all ISO 3166 subdivision data from input country name/names. """
        test_country_name_bj = "Benin"
        test_country_name_tj = "Tajikistan"
        test_country_name_sd = "Sudan"
        test_country_name_ml_ni = "Mali, Nicaragua"
        test_country_name_tj_filter = "parentCode"  #testing filter query string parameter
        test_country_name_ml_ni_filter = "type,flag,name,localOtherName"
        test_country_name_error1 = "ABCDEF"
        test_country_name_error2 = "12345"
#1.)
        test_request_country_name_bj = requests.get(self.country_name_base_url + test_country_name_bj, headers=self.user_agent_header).json() #Benin

        self.assertEqual(list(test_request_country_name_bj.keys()), ["BJ"], 
            f"Expected output object of API to contain only the BJ key, got {list(test_request_country_name_bj.keys())}.")
        self.assertEqual(list(test_request_country_name_bj["BJ"].keys()), ["BJ-AK", "BJ-AL", "BJ-AQ", "BJ-BO", "BJ-CO", "BJ-DO", "BJ-KO", "BJ-LI", "BJ-MO", "BJ-OU", "BJ-PL", "BJ-ZO"], 
            f"Expected subdivision keys do not match output:\n{list(test_request_country_name_bj['BJ'].keys())}.")   

        for subd in test_request_country_name_bj["BJ"]:
            if not (test_request_country_name_bj["BJ"][subd]["flag"] is None):
                self.assertEqual(os.path.splitext(test_request_country_name_bj["BJ"][subd]["flag"])[0], self.flag_base_url + "BJ/" + subd, 
                    f'Expected flag URL to be {self.flag_base_url + "BJ/" + subd}, got {os.path.splitext(test_request_country_name_bj["BJ"][subd]["flag"])[0]}.') 
                self.assertEqual(requests.get(test_request_country_name_bj["BJ"][subd]["flag"], headers=self.user_agent_header).status_code, 200, 
                    f'Flag URL invalid: {test_request_country_name_bj["BJ"][subd]["flag"]}.')
            for key in list(test_request_country_name_bj["BJ"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, f"Attribute {key} not found in list of correct attributes:\n{self.correct_subdivision_keys}.") 
#2.)    
        test_request_country_name_tj = requests.get(self.country_name_base_url + test_country_name_tj, headers=self.user_agent_header).json() #Tajikistan

        self.assertEqual(list(test_request_country_name_tj.keys()), ["TJ"], 
            f"Expected output object of API to contain only the TJ key, got {list(test_request_country_name_tj.keys())}.")
        self.assertEqual(list(test_request_country_name_tj["TJ"].keys()), ["TJ-DU", "TJ-GB", "TJ-KT", "TJ-RA", "TJ-SU"],
            f"Expected subdivision keys do not match output:\n{list(test_request_country_name_tj['TJ'].keys())}.")   

        for subd in test_request_country_name_tj["TJ"]:
            if not (test_request_country_name_tj["TJ"][subd]["flag"] is None):
                self.assertEqual(os.path.splitext(test_request_country_name_tj["TJ"][subd]["flag"])[0], self.flag_base_url + "TJ/" + subd, 
                    f'Expected flag URL to be {self.flag_base_url + "TJ/" + subd}, got {os.path.splitext(test_request_country_name_tj["TJ"][subd]["flag"])[0]}.') 
                self.assertEqual(requests.get(test_request_country_name_tj["TJ"][subd]["flag"], headers=self.user_agent_header).status_code, 200, 
                    f'Flag URL invalid: {test_request_country_name_tj["TJ"][subd]["flag"]}.')
            for key in list(test_request_country_name_tj["TJ"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, f"Attribute {key} not found in list of correct attributes:\n{self.correct_subdivision_keys}.") 
#3.) 
        test_request_country_name_sd = requests.get(self.country_name_base_url + test_country_name_sd, headers=self.user_agent_header).json() #Sudan

        self.assertEqual(list(test_request_country_name_sd.keys()), ["SD"], 
            f"Expected output object of API to contain only the SD key, got {list(test_request_country_name_sd.keys())}.")
        self.assertEqual(list(test_request_country_name_sd["SD"].keys()), 
            ["SD-DC", "SD-DE", "SD-DN", "SD-DS", "SD-DW", "SD-GD", "SD-GK", "SD-GZ", "SD-KA", "SD-KH", \
             "SD-KN", "SD-KS", "SD-NB", "SD-NO", "SD-NR", "SD-NW", "SD-RS", "SD-SI"],
            f"Expected subdivision keys do not match output:\n{list(test_request_country_name_sd['SD'].keys())}.")   
    
        for subd in test_request_country_name_sd["SD"]:
            if not (test_request_country_name_sd["SD"][subd]["flag"] is None):
                self.assertEqual(os.path.splitext(test_request_country_name_sd["SD"][subd]["flag"])[0], self.flag_base_url + "SD/" + subd, 
                    f'Expected flag URL to be {self.flag_base_url + "SD/" + subd}, got {os.path.splitext(test_request_country_name_sd["SD"][subd]["flag"])[0]}.') 
                self.assertEqual(requests.get(test_request_country_name_sd["SD"][subd]["flag"], headers=self.user_agent_header).status_code, 200, 
                    f'Flag URL invalid: {test_request_country_name_sd["SD"][subd]["flag"]}.')
            for key in list(test_request_country_name_sd["SD"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, f"Attribute {key} not found in list of correct attributes:\n{self.correct_subdivision_keys}.") 
#4.)
        test_request_country_name_ml_ni = requests.get(self.country_name_base_url + test_country_name_ml_ni, headers=self.user_agent_header).json() #Mali and Nicaragua

        self.assertEqual(list(test_request_country_name_ml_ni.keys()), ["ML", "NI"], 
            f"Expected output object of API to contain only the ML and NI keys, got {list(test_request_country_name_ml_ni.keys())}.")
        self.assertEqual(list(test_request_country_name_ml_ni["ML"].keys()), ["ML-1", "ML-10", "ML-2", "ML-3", "ML-4", "ML-5", "ML-6", "ML-7", "ML-8", "ML-9", "ML-BKO"],
            f"Expected subdivision keys do not match output:\n{list(test_request_country_name_ml_ni['ML'].keys())}.")   
        self.assertEqual(list(test_request_country_name_ml_ni["NI"].keys()), 
            ["NI-AN", "NI-AS", "NI-BO", "NI-CA", "NI-CI", "NI-CO", "NI-ES", "NI-GR", "NI-JI", "NI-LE", "NI-MD", "NI-MN", "NI-MS", "NI-MT", "NI-NS", "NI-RI", "NI-SJ"],
            f"Expected subdivision keys do not match output:\n{list(test_request_country_name_ml_ni['NI'].keys())}.")   
    
        for subd in test_request_country_name_ml_ni["ML"]:          
            if not (test_request_country_name_ml_ni["ML"][subd]["flag"] is None):
                self.assertEqual(os.path.splitext(test_request_country_name_ml_ni["ML"][subd]["flag"])[0], self.flag_base_url + "ML/" + subd, 
                    f'Expected flag URL to be {self.flag_base_url + "ML/" + subd}, got {os.path.splitext(test_request_country_name_ml_ni["ML"][subd]["flag"])[0]}.') 
                self.assertEqual(requests.get(test_request_country_name_ml_ni["ML"][subd]["flag"], headers=self.user_agent_header).status_code, 200, 
                    f'Flag URL invalid: {test_request_country_name_ml_ni["ML"][subd]["flag"]}.')
            for key in list(test_request_country_name_ml_ni["ML"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, f"Attribute {key} not found in list of correct attributes:\n{self.correct_subdivision_keys}.")

        for subd in test_request_country_name_ml_ni["NI"]: 
            if not (test_request_country_name_ml_ni["NI"][subd]["flag"] is None):
                self.assertEqual(os.path.splitext(test_request_country_name_ml_ni["NI"][subd]["flag"])[0], self.flag_base_url + "NI/" + subd, 
                    f'Expected flag URL to be {self.flag_base_url + "NI/" + subd}, got {os.path.splitext(test_request_country_name_ml_ni["NI"][subd]["flag"])[0]}.') 
                self.assertEqual(requests.get(test_request_country_name_ml_ni["NI"][subd]["flag"], headers=self.user_agent_header).status_code, 200, 
                    f'Flag URL invalid: {test_request_country_name_ml_ni["NI"][subd]["flag"]}.')
            for key in list(test_request_country_name_ml_ni["NI"][subd].keys()):
                self.assertIn(key, self.correct_subdivision_keys, f"Attribute {key} not found in list of correct attributes:\n{self.correct_subdivision_keys}.") 
#6.)
        test_country_name_request_tj_filter = requests.get(self.country_name_base_url + test_country_name_tj, headers=self.user_agent_header, params={"filter": test_country_name_tj_filter}).json() #Tajikistan- filtering out all attributes but parentCode

        self.assertEqual(list(test_country_name_request_tj_filter.keys()), ["TJ"], 
            f"Expected output object of API to contain only the TJ key, got {list(test_country_name_request_tj_filter.keys())}.")
        self.assertEqual(list(test_country_name_request_tj_filter["TJ"].keys()), ["TJ-DU", "TJ-GB", "TJ-KT", "TJ-RA", "TJ-SU"],
            f"Expected subdivision keys do not match output:\n{list(test_country_name_request_tj_filter['TJ'].keys())}.")   
        for subd in test_country_name_request_tj_filter["TJ"]:
            self.assertEqual(list(test_country_name_request_tj_filter["TJ"][subd].keys()), ["parentCode"], 
                f"Expected subdivision attributes to just include the parentCode attribute, got {list(test_country_name_request_tj_filter['TJ'][subd].keys())}.")
#7.)
        test_country_name_request_ml_ni_filter = requests.get(self.country_name_base_url + test_country_name_ml_ni, headers=self.user_agent_header, params={"filter": test_country_name_ml_ni_filter}).json()  #Mali, Nicaragua - filtering out all attributes but type, flag, name and localOtherName

        self.assertEqual(list(test_country_name_request_ml_ni_filter.keys()), ["ML", "NI"], 
            f"Expected output object of API to contain only the ML and NI keys, got {list(test_country_name_request_ml_ni_filter.keys())}.")
        for subd in test_country_name_request_ml_ni_filter["ML"]:
            self.assertEqual(list(test_country_name_request_ml_ni_filter["ML"][subd].keys()), ["flag", "localOtherName", "name", "type"], 
                f"Expected subdivision attributes to just include the type, flag, name and localOtherName attributes, got {list(test_country_name_request_ml_ni_filter['ML'][subd].keys())}.")
        for subd in test_country_name_request_ml_ni_filter["NI"]:
            self.assertEqual(list(test_country_name_request_ml_ni_filter["NI"][subd].keys()), ["flag", "localOtherName", "name", "type"], 
                f"Expected subdivision attributes to just include the type, flag, name and localOtherName attributes, got {list(test_country_name_request_ml_ni_filter['NI'][subd].keys())}.")
#8.)
        test_country_name_request_sd_filter_all = requests.get(self.country_name_base_url + test_country_name_sd, headers=self.user_agent_header, params={"filter": "*"}).json()  #Sudan - including all attributes via the wildcard '*' symbol

        self.assertEqual(list(test_country_name_request_sd_filter_all.keys()), ["SD"], 
            f"Expected output object of API to contain only the SD key, got {list(test_country_name_request_sd_filter_all.keys())}.")
        for subd in test_country_name_request_sd_filter_all["SD"]:
            self.assertEqual(list(test_country_name_request_sd_filter_all["SD"][subd].keys()), ['flag', 'history', 'latLng', 'localOtherName', 'name', 'parentCode', 'type'], 
                f"Expected subdivision attributes to just include all the default attributes, got {list(test_country_name_request_sd_filter_all['SD'][subd].keys())}.")
#9.)
        test_request_country_name_error1 = requests.get(self.country_name_base_url + test_country_name_error1, headers=self.user_agent_header).json() #ABCDEF
        test_request_country_name_error1_expected = {"message": f"Invalid country name input: {test_country_name_error1.title()}.", "path": test_request_country_name_error1["path"], "status": 400}
        self.assertEqual(test_request_country_name_error1, test_request_country_name_error1_expected, f"Expected and observed output error object do not match:\n{test_request_country_name_error1}.")
#10.)
        test_request_country_name_error2 = requests.get(self.country_name_base_url + test_country_name_error2, headers=self.user_agent_header).json() #12345
        test_request_country_name_error2_expected = {"message": f"Invalid country name input: {test_country_name_error2.title()}.", "path": test_request_country_name_error2["path"], "status": 400}
        self.assertEqual(test_request_country_name_error2, test_request_country_name_error2_expected, f"Expected and observed output error object do not match:\n{test_request_country_name_error2}.")
#11.)
        # test_request_country_name_error3 = requests.get(self.country_name_base_url + test_country_name_sd, headers=self.user_agent_header, params={"filter": "invalid_attribute"}).json() #invalid attribute input
        # test_request_country_name_error3_expected = {"message": "Invalid attribute name input to filter query string parameter: invalid_attribute. Refer to the list of supported attributes: name, localOtherName, type, parentCode, flag, latLng, history", "path": test_request_country_name_error3["path"], "status": 400}
        # self.assertEqual(test_request_country_name_error3, test_request_country_name_error3_expected, f"Expected and observed output error object do not match:\n{test_request_country_name_error3}.")
    
    # @unittest.skip("")
    def test_list_subdivisions_endpoint(self):
        """ Testing /list_subdivisions endpoint, return all ISO 3166 subdivision codes for each country. """
#1.)
        test_request_list_subdivisions = requests.get(self.list_subdivisions_base_url, headers=self.user_agent_header).json()

        self.assertEqual(len(test_request_list_subdivisions), 250, 
            f"Expected output object of API to be of length 250, got {len(test_request_list_subdivisions)}.")
        for alpha2 in list(test_request_list_subdivisions.keys()):
            self.assertIn(alpha2, iso3166.countries_by_alpha2, 
                f"Alpha-2 code {alpha2} not found in list of available country codes.")
            for subd in test_request_list_subdivisions[alpha2]:
                self.assertIn(subd, self.iso3166_2_data.subdivision_codes(alpha2), 
                    f"Subdivision code {subd} not found in list of available subdivision codes for {alpha2}.")
#2.)
        test_request_list_subdivisions_de = requests.get(f'{self.list_subdivisions_base_url}/DE', headers=self.user_agent_header).json()
        self.assertEqual(len(test_request_list_subdivisions_de), 16, f"Expected there to be 16 total subdivisions for DE, got {len(test_request_list_subdivisions_de)}.")
#3.)
        test_request_list_subdivisions_hu = requests.get(f'{self.list_subdivisions_base_url}/HU', headers=self.user_agent_header).json()
        self.assertEqual(len(test_request_list_subdivisions_hu), 43, f"Expected there to be 43 total subdivisions for HU, got {len(test_request_list_subdivisions_hu)}.")
#4.)
        test_request_list_subdivisions_pw = requests.get(f'{self.list_subdivisions_base_url}/PW', headers=self.user_agent_header).json()
        self.assertEqual(len(test_request_list_subdivisions_pw), 16, f"Expected there to be 16 total subdivisions for PW, got {len(test_request_list_subdivisions_pw)}.")
#5.)
        test_request_list_subdivisions_error1 = requests.get(f'{self.list_subdivisions_base_url}/ABC', headers=self.user_agent_header).json() 
        test_request_list_subdivisions_error1_expected = {"message": f"Invalid ISO 3166-1 country code input ABC.", "path": f'{self.list_subdivisions_base_url}/ABC', "status": 400}
        self.assertEqual(test_request_list_subdivisions_error1, test_request_list_subdivisions_error1_expected, f"Expected and observed output error object do not match:\n{test_request_list_subdivisions_error1}.")
#6.)
        test_request_list_subdivisions_error2 = requests.get(f'{self.list_subdivisions_base_url}/ZZ', headers=self.user_agent_header).json() 
        test_request_list_subdivisions_error2_expected = {"message": f"Invalid ISO 3166-1 country code input ZZ.", "path": f'{self.list_subdivisions_base_url}/ZZ', "status": 400}
        self.assertEqual(test_request_list_subdivisions_error2, test_request_list_subdivisions_error2_expected, f"Expected and observed output error object do not match:\n{test_request_list_subdivisions_error2}.")

    # @unittest.skip("")
    def test_version(self):
        """ Testing the correct version of the iso3166-2 software is being used by the API. """
#1.)
        iso3166_2_api_version = requests.get(self.version_base_url, headers=self.user_agent_header).content.decode("utf-8")
        self.assertEqual(iso3166_2_api_version, self.__version__, f"Expected and observed version of the iso3166-2 software do not match {iso3166_2_api_version}.")

if __name__ == '__main__':
    #run all unit tests
    unittest.main(verbosity=2)  