import unittest
from unittest.mock import patch, MagicMock
import os
import json
import sys

#add scripts directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from city_data import get_cities_for_subdivision, BASE_URL, USER_AGENT_HEADER

# @unittest.skip("")
class CityDataUnitTests(unittest.TestCase):
    """
    Unit tests for city_data module and get_cities_for_subdivision function with 
    mocked API calls.

    Test Cases
    ==========
    test_get_cities_success:
        test successful retrieval of cities for a valid subdivision code.
    test_get_cities_with_short_subdivision_code:
        test function with short subdivision code (e.g., 'CA' instead of 'US-CA').
    test_get_cities_empty_result:
        test handling of empty city list response.
    test_get_cities_with_proxy:
        test function with proxy settings.
    test_api_key_missing_error:
        test error when API key is not provided and not in environment.
    test_api_key_from_environment:
        test API key retrieval from environment variable.
    test_http_error_handling:
        test handling of HTTP errors from the API.
    test_timeout_handling:
        test handling of request timeout.
    test_connection_error_handling:
        test handling of connection errors.
    test_malformed_json_response:
        test handling of malformed JSON response.
    test_response_with_missing_fields:
        test handling of response with missing latitude/longitude fields.
    test_correct_url_construction: 
        test that the correct URL is constructed for the API request.
    test_correct_headers_sent:
        test that correct headers are sent with the request.
    test_timeout_parameter:
        test that timeout parameter is set correctly in the request.
    test_multiple_calls_independence:
        test that multiple calls to the function do not interfere with each other.
    """
    def setUp(self):
        """Set up test fixtures."""
        self.test_api_key = "test_api_key_12345"
        self.test_alpha2 = "US"
        self.test_subdivision_code = "US-CA"
        self.test_subdivision_code_short = "CA"
        
        #mock city data response
        self.mock_cities_response = [
            {
                "id": 1,
                "name": "Los Angeles",
                "latitude": 34.0522,
                "longitude": -118.2437
            },
            {
                "id": 2,
                "name": "San Francisco",
                "latitude": 37.7749,
                "longitude": -122.4194
            },
            {
                "id": 3,
                "name": "San Diego",
                "latitude": 32.7157,
                "longitude": -117.1611
            }
        ]
    
    @patch('city_data.requests.get')
    def test_get_cities_success(self, mock_get):
        """Test successful retrieval of cities."""
        mock_response = MagicMock()
        mock_response.json.return_value = self.mock_cities_response
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        #call test function
        result = get_cities_for_subdivision(
            self.test_alpha2,
            self.test_subdivision_code,
            api_key=self.test_api_key
        )
        expected_result = [
            {"name": "Los Angeles", "latLng": [34.0522, -118.2437]},
            {"name": "San Francisco", "latLng": [37.7749, -122.4194]},
            {"name": "San Diego", "latLng": [32.7157, -117.1611]}
        ]
        
        self.assertIsInstance(result, list, f"Result should be a list, got {type(result)}.")
        self.assertEqual(len(result), 3, f"Should return 3 cities, got {len(result)}.")
        self.assertEqual(result, expected_result, "Returned city data does not match expected.")
    
    @patch('city_data.requests.get')
    def test_get_cities_with_short_subdivision_code(self, mock_get):
        """Test function with short subdivision code (e.g., 'CA' instead of 'US-CA')."""
        mock_response = MagicMock()
        mock_response.json.return_value = self.mock_cities_response
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        #call test function
        result = get_cities_for_subdivision(
            self.test_alpha2,
            self.test_subdivision_code_short,
            api_key=self.test_api_key
        )
        
        self.assertEqual(len(result), 3, f"Should return 3 cities, got {len(result)}.")
        mock_get.assert_called_once()
    
    @patch('city_data.requests.get')
    def test_get_cities_empty_result(self, mock_get):
        """Test handling of empty city list."""
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        #call test function
        result = get_cities_for_subdivision(
            self.test_alpha2,
            self.test_subdivision_code,
            api_key=self.test_api_key
        )
  
        self.assertIsInstance(result, list, f"Result should be a list, got {type(result)}.")
        self.assertEqual(len(result), 0, f"Should return 0 cities, got {len(result)}.")
    
    @patch('city_data.requests.get')
    def test_get_cities_with_proxy(self, mock_get):
        """Test function with proxy settings."""
        mock_response = MagicMock()
        mock_response.json.return_value = self.mock_cities_response
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        proxy_settings = {
            "http": "http://proxy.example.com:8080",
            "https": "https://proxy.example.com:8080"
        }
        
        result = get_cities_for_subdivision(
            self.test_alpha2,
            self.test_subdivision_code,
            api_key=self.test_api_key,
            proxy=proxy_settings
        )
        
        # Verify proxy was passed to requests.get
        call_kwargs = mock_get.call_args[1]
        self.assertEqual(call_kwargs['proxies'], proxy_settings)
        self.assertEqual(len(result), 3)
    
    @patch('city_data.requests.get')
    def test_api_key_missing_error(self, mock_get):
        """Test error when API key is not provided and not in environment."""
        with patch.dict(os.environ, {}, clear=True):
            with patch('city_data.load_dotenv'):
                with self.assertRaises(ValueError) as context:
                    get_cities_for_subdivision(
                        self.test_alpha2,
                        self.test_subdivision_code,
                        api_key=None
                    )
                
                self.assertIn("API key", str(context.exception))
                self.assertIn("COUNTRY_STATE_CITY_API_KEY", str(context.exception))
    
    @patch('city_data.load_dotenv')
    @patch.dict(os.environ, {'COUNTRY_STATE_CITY_API_KEY': 'env_api_key'})
    @patch('city_data.requests.get')
    def test_api_key_from_environment(self, mock_get, mock_load_dotenv):
        """Test API key retrieval from environment variable."""
        mock_response = MagicMock()
        mock_response.json.return_value = self.mock_cities_response
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = get_cities_for_subdivision(
            self.test_alpha2,
            self.test_subdivision_code
        )
        
        # Verify correct API key was used
        call_kwargs = mock_get.call_args[1]
        self.assertEqual(call_kwargs['headers']['X-CSCAPI-KEY'], 'env_api_key')
        self.assertEqual(len(result), 3)
    
    @patch('builtins.print')
    @patch('city_data.requests.get')
    def test_http_error_handling(self, mock_get, mock_print):
        """Test handling of HTTP errors."""
        mock_get.side_effect = Exception("HTTP 404: Not Found")
        
        result = get_cities_for_subdivision(
            self.test_alpha2,
            self.test_subdivision_code,
            api_key=self.test_api_key
        )
        
        # Should return empty list on error
        self.assertEqual(result, [])
    
    @patch('builtins.print')
    @patch('city_data.requests.get')
    def test_timeout_handling(self, mock_get, mock_print):
        """Test handling of request timeout."""
        import requests
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
        
        result = get_cities_for_subdivision(
            self.test_alpha2,
            self.test_subdivision_code,
            api_key=self.test_api_key
        )
        
        self.assertEqual(result, [])
    
    @patch('builtins.print')
    @patch('city_data.requests.get')
    def test_connection_error_handling(self, mock_get, mock_print):
        """Test handling of connection errors."""
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        result = get_cities_for_subdivision(
            self.test_alpha2,
            self.test_subdivision_code,
            api_key=self.test_api_key
        )
        
        self.assertEqual(result, [])
    
    @patch('builtins.print')
    @patch('city_data.requests.get')
    def test_malformed_json_response(self, mock_get, mock_print):
        """Test handling of malformed JSON response."""
        mock_response = MagicMock()
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = get_cities_for_subdivision(
            self.test_alpha2,
            self.test_subdivision_code,
            api_key=self.test_api_key
        )
        
        self.assertEqual(result, [])
    
    @patch('city_data.requests.get')
    def test_response_with_missing_fields(self, mock_get):
        """Test handling of response with missing latitude/longitude fields."""
        incomplete_response = [
            {
                "id": 1,
                "name": "Los Angeles",
                "latitude": 34.0522
                # Missing longitude
            },
            {
                "id": 2,
                "name": "San Francisco"
                # Missing both lat/lng
            }
        ]
        
        mock_response = MagicMock()
        mock_response.json.return_value = incomplete_response
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = get_cities_for_subdivision(
            self.test_alpha2,
            self.test_subdivision_code,
            api_key=self.test_api_key
        )
        
        # Should still return results, with None values for missing fields
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'Los Angeles')
        self.assertIsNone(result[1]['latLng'][0])  # lat from first dict
    
    @patch('city_data.requests.get')
    def test_correct_url_construction(self, mock_get):
        """Test that the correct URL is constructed."""
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        get_cities_for_subdivision(
            "GB",
            "GB-ENG",
            api_key=self.test_api_key
        )
        
        # Verify correct URL was called
        call_args = mock_get.call_args
        expected_url = f"{BASE_URL}GB/states/ENG/cities"
        self.assertEqual(call_args[0][0], expected_url)
    
    @patch('city_data.requests.get')
    def test_correct_headers_sent(self, mock_get):
        """Test that correct headers are sent with request."""
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        get_cities_for_subdivision(
            self.test_alpha2,
            self.test_subdivision_code,
            api_key=self.test_api_key
        )
        
        call_kwargs = mock_get.call_args[1]
        headers = call_kwargs['headers']
        
        # Verify User-Agent and API key headers
        self.assertIn('User-Agent', headers)
        self.assertEqual(headers['User-Agent'], USER_AGENT_HEADER['User-Agent'])
        self.assertEqual(headers['X-CSCAPI-KEY'], self.test_api_key)
    
    @patch('city_data.requests.get')
    def test_timeout_parameter(self, mock_get):
        """Test that timeout parameter is set correctly."""
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        get_cities_for_subdivision(
            self.test_alpha2,
            self.test_subdivision_code,
            api_key=self.test_api_key
        )
        
        call_kwargs = mock_get.call_args[1]
        self.assertEqual(call_kwargs['timeout'], 15)
    
    @patch('city_data.requests.get')
    def test_multiple_calls_independence(self, mock_get):
        """Test that multiple calls don't interfere with each other."""
        mock_response = MagicMock()
        mock_response.json.return_value = self.mock_cities_response
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # First call
        result1 = get_cities_for_subdivision(
            "US",
            "US-CA",
            api_key=self.test_api_key
        )
        
        # Second call with different params
        result2 = get_cities_for_subdivision(
            "GB",
            "GB-ENG",
            api_key=self.test_api_key
        )
        
        self.assertEqual(len(result1), 3)
        self.assertEqual(len(result2), 3)
        self.assertEqual(mock_get.call_count, 2)

# @unittest.skip("")
class TestCityDataIntegration(unittest.TestCase):
    """ 
    Integration tests with real API calls (optional, requires API key).
    
    Test Cases
    ==========
    test_real_api_call:
        test real API call using several example subdivision codes.
    """
    
    def setUp(self):
        """ Set up integration test fixtures. """
        self.api_key = os.getenv('COUNTRY_STATE_CITY_API_KEY')
        self.skip_integration = not self.api_key
    
    @unittest.skipIf(os.getenv('COUNTRY_STATE_CITY_API_KEY') is None, 
                     "COUNTRY_STATE_CITY_API_KEY not set; skipping real API tests")
    def test_real_api_call(self):
        """ Test real API call e.g US-CA (California, USA). """
#1.)
        subdivision_cities = get_cities_for_subdivision("US", "US-CA", api_key=self.api_key)

        self.assertIsInstance(subdivision_cities, list)
        self.assertEqual(len(subdivision_cities), 1123)
        
        # Validate structure: each city should have 'name' as string and 'latLng' as list of 2 strings
        for city in subdivision_cities:
            self.assertIsInstance(city, dict, f"Expected city to be a dict, got {type(city)}.")
            self.assertIn('name', city, "Expected 'name' key in city object.")
            self.assertIn('latLng', city, "Expected 'latLng' key in city object.")
            
            # Validate name is a string
            self.assertIsInstance(city['name'], str, 
                                f"Expected 'name' to be a string, got {type(city['name'])} for {city['name']}.")
            
            # Validate latLng is a list of exactly 2 elements
            self.assertIsInstance(city['latLng'], list, 
                                f"Expected 'latLng' to be a list, got {type(city['latLng'])}.")
            self.assertEqual(len(city['latLng']), 2, 
                           f"Expected 'latLng' to have 2 elements, got {len(city['latLng'])} for {city['name']}.")
            
            # Validate both lat/lng are strings
            lat, lng = city['latLng']
            self.assertIsInstance(lat, str, 
                                f"Expected latitude to be a string, got {type(lat)} for {city['name']}.")
            self.assertIsInstance(lng, str, 
                                f"Expected longitude to be a string, got {type(lng)} for {city['name']}.")
            
            # Validate that lat/lng strings can be converted to floats
            try:
                lat_float = float(lat)
                lng_float = float(lng)
            except ValueError:
                self.fail(f"Expected lat/lng to be convertible to float for {city['name']}: lat={lat}, lng={lng}")
            
            # Validate latitude is within valid range (-90 to 90)
            self.assertTrue(-90 <= lat_float <= 90, 
                          f"Invalid latitude {lat_float} for {city['name']}. Expected value between -90 and 90.")
            
            # Validate longitude is within valid range (-180 to 180)
            self.assertTrue(-180 <= lng_float <= 180, 
                          f"Invalid longitude {lng_float} for {city['name']}. Expected value between -180 and 180.")
#2.)
        subdivision_cities = get_cities_for_subdivision("EG", "EG-DK", api_key=self.api_key)

        self.assertIsInstance(subdivision_cities, list)
        self.assertEqual(len(subdivision_cities), 11)
        
        # Validate structure: each city should have 'name' as string and 'latLng' as list of 2 strings
        for city in subdivision_cities:
            self.assertIsInstance(city, dict, f"Expected city to be a dict, got {type(city)}.")
            self.assertIn('name', city, "Expected 'name' key in city object.")
            self.assertIn('latLng', city, "Expected 'latLng' key in city object.")
            
            # Validate name is a string
            self.assertIsInstance(city['name'], str, 
                                f"Expected 'name' to be a string, got {type(city['name'])} for {city['name']}.")
            
            # Validate latLng is a list of exactly 2 elements
            self.assertIsInstance(city['latLng'], list, 
                                f"Expected 'latLng' to be a list, got {type(city['latLng'])}.")
            self.assertEqual(len(city['latLng']), 2, 
                           f"Expected 'latLng' to have 2 elements, got {len(city['latLng'])} for {city['name']}.")
            
            # Validate both lat/lng are strings
            lat, lng = city['latLng']
            self.assertIsInstance(lat, str, 
                                f"Expected latitude to be a string, got {type(lat)} for {city['name']}.")
            self.assertIsInstance(lng, str, 
                                f"Expected longitude to be a string, got {type(lng)} for {city['name']}.")
            
            # Validate that lat/lng strings can be converted to floats
            try:
                lat_float = float(lat)
                lng_float = float(lng)
            except ValueError:
                self.fail(f"Expected lat/lng to be convertible to float for {city['name']}: lat={lat}, lng={lng}")
            
            # Validate latitude is within valid range (-90 to 90)
            self.assertTrue(-90 <= lat_float <= 90, 
                          f"Invalid latitude {lat_float} for {city['name']}. Expected value between -90 and 90.")
            
            # Validate longitude is within valid range (-180 to 180)
            self.assertTrue(-180 <= lng_float <= 180, 
                          f"Invalid longitude {lng_float} for {city['name']}. Expected value between -180 and 180.")
#3.)
        subdivision_cities = get_cities_for_subdivision("FJ", "FJ-01", api_key=self.api_key)

        self.assertIsInstance(subdivision_cities, list)
        self.assertEqual(len(subdivision_cities), 0)
        
        # Validate structure: each city should have 'name' as string and 'latLng' as list of 2 strings
        for city in subdivision_cities:
            self.assertIsInstance(city, dict, f"Expected city to be a dict, got {type(city)}.")
            self.assertIn('name', city, "Expected 'name' key in city object.")
            self.assertIn('latLng', city, "Expected 'latLng' key in city object.")
            
            # Validate name is a string
            self.assertIsInstance(city['name'], str, 
                                f"Expected 'name' to be a string, got {type(city['name'])} for {city['name']}.")
            
            # Validate latLng is a list of exactly 2 elements
            self.assertIsInstance(city['latLng'], list, 
                                f"Expected 'latLng' to be a list, got {type(city['latLng'])}.")
            self.assertEqual(len(city['latLng']), 2, 
                           f"Expected 'latLng' to have 2 elements, got {len(city['latLng'])} for {city['name']}.")
            
            # Validate both lat/lng are strings
            lat, lng = city['latLng']
            self.assertIsInstance(lat, str, 
                                f"Expected latitude to be a string, got {type(lat)} for {city['name']}.")
            self.assertIsInstance(lng, str, 
                                f"Expected longitude to be a string, got {type(lng)} for {city['name']}.")
            
            # Validate that lat/lng strings can be converted to floats
            try:
                lat_float = float(lat)
                lng_float = float(lng)
            except ValueError:
                self.fail(f"Expected lat/lng to be convertible to float for {city['name']}: lat={lat}, lng={lng}")
            
            # Validate latitude is within valid range (-90 to 90)
            self.assertTrue(-90 <= lat_float <= 90, 
                          f"Invalid latitude {lat_float} for {city['name']}. Expected value between -90 and 90.")
            
            # Validate longitude is within valid range (-180 to 180)
            self.assertTrue(-180 <= lng_float <= 180, 
                          f"Invalid longitude {lng_float} for {city['name']}. Expected value between -180 and 180.")
#4.)
        # Test with invalid country code and invalid subdivision code
        with self.assertRaises(ValueError):
            get_cities_for_subdivision("ZZ", "ZZ-01", api_key=self.api_key)
            get_cities_for_subdivision("AB", "AB-123", api_key=self.api_key)
            get_cities_for_subdivision("DD", "", api_key=self.api_key)

if __name__ == '__main__':
    unittest.main()