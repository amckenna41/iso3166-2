from scripts.restcountries_api import get_rest_countries_country_data, get_supported_fields, RESTCOUNTRIES_BASE_URL
import unittest
from unittest.mock import patch, Mock
import requests
unittest.TestLoader.sortTestMethodsUsing = None

# @unittest.skip("")
class RestCountriesAPIUnitTests(unittest.TestCase):
    """
    Test suite for testing the RestCountries API module functions.

    Test Cases
    ==========
    test_get_supported_fields:
        testing function that returns the list of supported RestCountries API fields.
    """
    def test_get_supported_fields(self):
        """ Testing that get_supported_fields returns the correct list of API fields. """
        expected_fields = [
            "idd", "carSigns", "carSide", "continents", "currencies", "languages",
            "postalCode", "region", "startOfWeek", "subregion", "timezones", "tld", "unMember"
        ]
        
        result = get_supported_fields()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 13)
        self.assertEqual(result, expected_fields)
        
        # Verify all expected fields are present
        for field in expected_fields:
            self.assertIn(field, result)

# @unittest.skip("")
class RestCountriesAPIIntegrationTests(unittest.TestCase):
    """
    Test suite for integration tests of the RestCountries API module.

    Test Cases
    ==========
    test_get_rest_countries_country_data_success:
        testing successful API call with valid alpha-2 code.
    test_get_rest_countries_country_data_with_fields:
        testing API call with specific field filtering.
    test_get_rest_countries_country_data_invalid_code:
        testing API call with invalid alpha-2 code.
    test_get_rest_countries_country_data_network_error:
        testing API call handles network errors gracefully.
    test_get_rest_countries_country_data_timeout:
        testing API call handles timeouts properly.
    test_get_rest_countries_country_data_with_proxy:
        testing API call with proxy settings.
    """
    @patch('scripts.restcountries_api.requests.get')
    def test_get_rest_countries_country_data_success(self, mock_get):
        """ Testing successful API call returns proper country data. """
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "name": {"common": "Ireland"},
            "cca2": "IE",
            "region": "Europe",
            "population": 4937786,
            "languages": {"eng": "English", "gle": "Irish"}
        }]
        mock_get.return_value = mock_response
        
        result = get_rest_countries_country_data("IE")
        
        # Verify request was made correctly
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        self.assertIn(f"{RESTCOUNTRIES_BASE_URL}alpha/IE", call_args[0])
        
        # Verify response
        self.assertIsNotNone(result)
        self.assertEqual(result["cca2"], "IE")
        self.assertEqual(result["region"], "Europe")

    @patch('scripts.restcountries_api.requests.get')
    def test_get_rest_countries_country_data_with_fields(self, mock_get):
        """ Testing API call with field filtering returns only requested fields. """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "name": {"common": "France"},
            "cca2": "FR",
            "region": "Europe",
            "population": 65273511,
            "currencies": {"EUR": {"name": "Euro", "symbol": "€"}},
            "languages": {"fra": "French"}
        }]
        mock_get.return_value = mock_response
        
        result = get_rest_countries_country_data("FR", fields=["region", "currencies"])
        
        self.assertIsNotNone(result)
        self.assertIn("region", result)
        self.assertIn("currencies", result)
        self.assertEqual(len(result), 2)
        self.assertEqual(result["region"], "Europe")

    @patch('builtins.print')
    @patch('scripts.restcountries_api.requests.get')
    def test_get_rest_countries_country_data_invalid_code(self, mock_get, mock_print):
        """ Testing API call with invalid alpha-2 code returns None. """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        result = get_rest_countries_country_data("ZZ")
        
        self.assertIsNone(result)

    @patch('builtins.print')
    @patch('scripts.restcountries_api.requests.get')
    def test_get_rest_countries_country_data_network_error(self, mock_get, mock_print):
        """ Testing API call handles network errors and returns None. """
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")
        
        result = get_rest_countries_country_data("US")
        
        self.assertIsNone(result)

    @patch('builtins.print')
    @patch('scripts.restcountries_api.requests.get')
    def test_get_rest_countries_country_data_timeout(self, mock_get, mock_print):
        """ Testing API call handles timeout and returns None. """
        mock_get.side_effect = requests.exceptions.Timeout("Request timeout")
        
        result = get_rest_countries_country_data("DE")
        
        self.assertIsNone(result)

    @patch('scripts.restcountries_api.requests.get')
    def test_get_rest_countries_country_data_with_proxy(self, mock_get):
        """ Testing API call correctly passes proxy settings. """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"cca2": "GB", "name": {"common": "United Kingdom"}}]
        mock_get.return_value = mock_response
        
        proxy_settings = {"http": "http://proxy.example.com:8080"}
        result = get_rest_countries_country_data("GB", proxy=proxy_settings)
        
        # Verify proxy was passed to request
        call_kwargs = mock_get.call_args[1]
        self.assertEqual(call_kwargs["proxies"], proxy_settings)
        self.assertIsNotNone(result)

    @patch('scripts.restcountries_api.requests.get')
    def test_get_rest_countries_country_data_empty_response(self, mock_get):
        """ Testing API call with empty response returns None. """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        
        result = get_rest_countries_country_data("XX")
        
        self.assertIsNone(result)

    @patch('scripts.restcountries_api.requests.get')
    def test_get_rest_countries_country_data_invalid_json(self, mock_get):
        """ Testing API call with invalid JSON response returns None. """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = "not a list"
        mock_get.return_value = mock_response
        
        result = get_rest_countries_country_data("CA")
        
        self.assertIsNone(result)

# Run the tests
if __name__ == '__main__':
    unittest.main()