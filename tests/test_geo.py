import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json
import pandas as pd
from iso3166_2 import Subdivisions

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from geo import Geo

# @unittest.skip("")
class GeoUnitTests(unittest.TestCase):
    """ 
    Unit tests for geo.py Geo class with mocked API calls. Uses cached Geo data
    (tests/test_files/test_geo_cache_min.csv) for testing.

    Test Cases
    ========== 
    test_geo_cache_file:
        Validates the structure, content, and integrity of the geo cache file.
    test_init_with_country_code:
        Validates Geo initialization with country codes and verifies attributes and cached data match.
    test_init_without_country_code:
        Validates Geo initialization without country code results in None for country-specific attributes.
    test_init_error_country_code:
        Validates Geo initialization raises ValueError for invalid country codes.
    test_get_lat_lng_cached:
        Validates successful latitude/longitude retrieval via cache with proper format and ranges.
    test_get_bounding_box_cached:
        Validates successful bounding box retrieval via cache with proper coordinate ranges and ordering.
    test_get_geojson_cached:
        Validates GeoJSON FeatureCollection retrieval through mocked cache data.
    test_get_perimeter_cached:
        Validates perimeter retrieval via cache returns positive numeric values or empty strings for missing data.
    test_get_neighbours_cached:
        Validates neighbor detection via cache based on bounding box overlap.
    test_get_all_cached:
        Validates combined geographical data retrieval from cache combining latLng, bbox, perimeter, and neighbours.
    test_get_statistics:
        Validates statistics calculation from cache file including completeness, counts, and spatial metrics.
    test_clear_cache:
        Validates cache clearing functionality sets cache to None.
    test_export_cache_file:
        Validates cache export creates a file with correct structure and content.
    test_str:
        Validates string representation returns formatted country name and subdivision count.
    test_repr:
        Validates detailed repr includes country code, name, subdivisions, and cache info.
    test_len:
        Validates __len__ returns correct cache entry count.
    """
    def setUp(self):
        """ Set up test fixtures. """
        self.print_patcher = patch('builtins.print'); self.print_patcher.start()
        self.temp_cache_path = os.path.join("tests", "test_files", "test_geo_cache.csv")

        # create Subdivisions instance for reference, get flattened list of subdivision codes
        self.subd = Subdivisions()
        self.subdivision_codes = list(self.subd.subdivision_codes().values())
        self.subdivision_codes = [item for sublist in self.subdivision_codes for item in sublist]

        #create Geo instance for testing
        self.geo = Geo(geo_cache_path=self.temp_cache_path, export_to_cache=False)

    # @unittest.skip("")
    def test_geo_cache_file(self):
        """ Test cache file structure, content validity, and data integrity. """
        # Load cache file into DataFrame
        cache_df = pd.read_csv(self.temp_cache_path)
        expected_columns = ['subdivisionCode', 'latLng', 'boundingBox', 'geojson', 'perimeter', 'neighbours']
        expected_row_count = 5046 
        
        # Validate row count
        self.assertEqual(len(cache_df), expected_row_count,
                        f"Expected {expected_row_count} rows, got {len(cache_df)}")
        
        # Validate column names
        self.assertEqual(list(cache_df.columns), expected_columns,
                        f"Column names mismatch. Expected {expected_columns}, got {list(cache_df.columns)}")
        
        # Validate no null values in required columns
        for col in ['subdivisionCode', 'latLng']:
            null_count = cache_df[col].isnull().sum()
            self.assertEqual(null_count, 0,
                           f"Column '{col}' has {null_count} null values")
        
        # Validate subdivision code format and uniqueness
        for idx, code in enumerate(cache_df['subdivisionCode']):
            self.assertIsInstance(code, str, f"Row {idx}: subdivisionCode must be string")
            self.assertIn(code, self.subdivision_codes, f"Row {idx}: Unknown subdivision code '{code}'")
        
        # Validate latLng format and values
        for idx, latlng in enumerate(cache_df['latLng']):
            self.assertIsInstance(latlng, str, f"Row {idx}: latLng must be string")
            parts = latlng.split(',')
            self.assertEqual(len(parts), 2,
                           f"Row {idx}: latLng '{latlng}' must be in format 'lat,lon'")
            try:
                lat = float(parts[0])
                lon = float(parts[1])
                self.assertTrue(-90 <= lat <= 90,
                              f"Row {idx}: Latitude {lat} out of range [-90, 90]")
                self.assertTrue(-180 <= lon <= 180,
                              f"Row {idx}: Longitude {lon} out of range [-180, 180]")
            except ValueError as e:
                self.fail(f"Row {idx}: latLng '{latlng}' contains invalid numbers: {e}")

        # Validate boundingBox format and values
        for idx, bbox in enumerate(cache_df['boundingBox']):
            if pd.isna(bbox) or bbox == "":
                continue  
            self.assertIsInstance(bbox, str, f"Row {idx}: boundingBox must be string")
            try:
                # Parse bounding box as JSON array string
                bbox_list = json.loads(bbox)
                self.assertIsInstance(bbox_list, list, f"Row {idx}: boundingBox must be a JSON array")
                self.assertEqual(len(bbox_list), 4,
                               f"Row {idx}: boundingBox must have 4 values, got {len(bbox_list)}")
                
                minlat, maxlat, minlon, maxlon = bbox_list
                self.assertIsInstance(minlat, (int, float), f"Row {idx}: minlat must be numeric")
                self.assertIsInstance(maxlat, (int, float), f"Row {idx}: maxlat must be numeric")
                self.assertIsInstance(minlon, (int, float), f"Row {idx}: minlon must be numeric")
                self.assertIsInstance(maxlon, (int, float), f"Row {idx}: maxlon must be numeric")
                
                self.assertTrue(-90 <= minlat <= 90,
                              f"Row {idx}: minlat {minlat} out of range [-90, 90]")
                self.assertTrue(-90 <= maxlat <= 90,
                              f"Row {idx}: maxlat {maxlat} out of range [-90, 90]")
                self.assertTrue(-180 <= minlon <= 180,
                              f"Row {idx}: minlon {minlon} out of range [-180, 180]")
                self.assertTrue(-180 <= maxlon <= 180,
                              f"Row {idx}: maxlon {maxlon} out of range [-180, 180]")
                self.assertLessEqual(minlat, maxlat,
                                   f"Row {idx}: minlat {minlat} greater than maxlat {maxlat}")
                self.assertLessEqual(minlon, maxlon,
                                   f"Row {idx}: minlon {minlon} greater than maxlon {maxlon}")
            except json.JSONDecodeError as e:
                self.fail(f"Row {idx}: boundingBox '{bbox}' is not valid JSON: {e}")
            except (ValueError, TypeError) as e:
                self.fail(f"Row {idx}: boundingBox '{bbox}' contains invalid values: {e}")
        
        # Validate geojson format
        for idx, geojson_str in enumerate(cache_df['geojson']):
            if pd.isna(geojson_str) or geojson_str == "":
                continue  
            self.assertIsInstance(geojson_str, str, f"Row {idx}: geojson must be string")
            try:
                geojson = json.loads(geojson_str)
                self.assertIsInstance(geojson, dict,
                                     f"Row {idx}: geojson must be a JSON object")
                self.assertIn('type', geojson,
                             f"Row {idx}: geojson missing 'type' key")
                self.assertEqual(geojson['type'], 'FeatureCollection',
                                f"Row {idx}: geojson 'type' must be 'FeatureCollection'")
                self.assertIn('features', geojson,
                             f"Row {idx}: geojson missing 'features' key")
                self.assertIsInstance(geojson['features'], list,
                                     f"Row {idx}: geojson 'features' must be a list")
            except json.JSONDecodeError as e:
                self.fail(f"Row {idx}: geojson is not valid JSON: {e}")
        
        # Validate perimeter format and values
        for idx, perimeter in enumerate(cache_df['perimeter']):
            if pd.isna(perimeter) or perimeter == "":
                continue  
            try:
                perimeter_value = float(perimeter)
                self.assertGreater(perimeter_value, 0,
                                 f"Row {idx}: perimeter {perimeter_value} must be positive")
            except ValueError as e:
                self.fail(f"Row {idx}: perimeter '{perimeter}' is not a valid number: {e}")
        
        # Validate neighbours format
        for idx, neighbours_str in enumerate(cache_df['neighbours']):
            if pd.isna(neighbours_str) or neighbours_str == "":
                continue  
            self.assertIsInstance(neighbours_str, str, f"Row {idx}: neighbours must be string")
            neighbours = [n.strip() for n in neighbours_str.split(',') if n.strip()]
            for neighbour_code in neighbours:
                self.assertIn(neighbour_code, self.subdivision_codes,
                             f"Row {idx}: Unknown neighbour subdivision code '{neighbour_code}'")

        # Validate all subdivision codes are present in cache
        cached_codes = set(cache_df['subdivisionCode'].tolist())
        missing_codes = set(self.subdivision_codes) - cached_codes
        self.assertTrue(len(missing_codes) == 0,
                       f"Missing subdivision codes in cache: {missing_codes}")

        # Validate no duplicate subdivision codes
        duplicates = cache_df['subdivisionCode'][cache_df['subdivisionCode'].duplicated()]
        self.assertTrue(duplicates.empty)

    # @unittest.skip("")
    def test_init_with_country_code(self):
        """ Test initialization of the Geo class with various country codes and verify attributes. """
        expected_subdivisions = {
            'AL-01': {'latlng': '40.6084,20.1089', 'bounding_box': [40.3407, 40.8752, 19.7312, 20.4488], 'perimeter': 255.91, 'neighbours': 'AL-03,AL-04,AL-05,AL-06,AL-12'},
            'AL-02': {'latlng': '41.428,19.5373', 'bounding_box': [41.2498, 41.6063, 19.3914, 19.9084], 'perimeter': 226.32, 'neighbours': 'AL-03,AL-08,AL-09,AL-11'},
            'AL-03': {'latlng': '41.0511,20.1399', 'bounding_box': [40.7069, 41.3959, 19.6734, 20.6064], 'perimeter': 330.43, 'neighbours': 'AL-01,AL-02,AL-04,AL-06,AL-09,AL-11'},
            'AL-04': {'latlng': '40.742,19.5701', 'bounding_box': [40.4154, 41.0693, 19.3136, 19.9233], 'perimeter': 301.53, 'neighbours': 'AL-01,AL-03,AL-05,AL-11,AL-12'},
            'AL-05': {'latlng': '40.1556,20.2139', 'bounding_box': [39.7845, 40.5266, 19.7802, 20.6177], 'perimeter': 327.66, 'neighbours': 'AL-01,AL-04,AL-06,AL-12'},
            'AL-06': {'latlng': '40.5859,20.7361', 'bounding_box': [40.0828, 41.092, 20.2933, 21.0574], 'perimeter': 399.76, 'neighbours': 'AL-01,AL-03,AL-05,AL-12'},
            'AL-07': {'latlng': '42.1886,20.377', 'bounding_box': [41.8148, 42.5591, 19.7982, 20.6266], 'perimeter': 330.2, 'neighbours': 'AL-08,AL-09,AL-10'},
            'AL-08': {'latlng': '41.7932,19.8891', 'bounding_box': [41.5536, 42.0327, 19.461, 20.2776], 'perimeter': 334.06, 'neighbours': 'AL-02,AL-07,AL-09,AL-10'},
            'AL-09': {'latlng': '41.6222,20.1808', 'bounding_box': [41.3368, 41.9073, 19.8123, 20.5744], 'perimeter': 283.72, 'neighbours': 'AL-02,AL-03,AL-07,AL-08,AL-10,AL-11'},
            'AL-10': {'latlng': '42.2508,19.596', 'bounding_box': [41.8402, 42.6611, 19.2808, 20.2483], 'perimeter': 420.96, 'neighbours': 'AL-07,AL-08,AL-09'},
            'AL-11': {'latlng': '41.2584,19.8303', 'bounding_box': [41.0016, 41.5154, 19.4361, 20.24], 'perimeter': 294.83, 'neighbours': 'AL-02,AL-03,AL-04,AL-09'},
            'AL-12': {'latlng': '40.1542,19.7522', 'bounding_box': [39.6449, 40.6634, 19.264, 20.3221], 'perimeter': 511.59, 'neighbours': 'AL-01,AL-04,AL-05,AL-06'},
            'DK-81': {'latlng': '56.8153,9.7273', 'bounding_box': [56.5504, 57.7522, 8.2209, 11.2002], 'perimeter': 1499.63, 'neighbours': 'DK-82'},
            'DK-82': {'latlng': '56.2356,9.2346', 'bounding_box': [55.6689, 56.8466, 8.0982, 11.663], 'perimeter': 1989.69, 'neighbours': 'DK-81,DK-83,DK-85'},
            'DK-83': {'latlng': '55.3784,9.1318', 'bounding_box': [54.7219, 55.9566, 8.0744, 10.9557], 'perimeter': 2404.56, 'neighbours': 'DK-82,DK-85'},
            'DK-84': {'latlng': '55.8616,12.3138', 'bounding_box': [54.9872, 56.2031, 11.682, 15.1574], 'perimeter': 746.26, 'neighbours': 'DK-85'},
            'DK-85': {'latlng': '55.4864,11.6913', 'bounding_box': [54.5591, 56.0106, 10.8684, 12.5536], 'perimeter': 2002.85, 'neighbours': 'DK-82,DK-83,DK-84'},
            'HT-AR': {'latlng': '19.3366,-72.4924', 'bounding_box': [18.8572, 19.8156, -73.1363, -72.2007], 'perimeter': 544.77, 'neighbours': 'HT-CE,HT-ND,HT-NO,HT-OU'},
            'HT-CE': {'latlng': '18.9908,-71.9944', 'bounding_box': [18.6847, 19.3343, -72.3647, -71.6217], 'perimeter': 394.44, 'neighbours': 'HT-AR,HT-ND,HT-NE,HT-OU'},
            'HT-GA': {'latlng': '18.5163,-74.0986', 'bounding_box': [18.3569, 18.6759, -74.4813, -73.6987], 'perimeter': 311.18, 'neighbours': 'HT-NI,HT-SD'},
            'HT-ND': {'latlng': '19.6258,-72.2699', 'bounding_box': [19.2549, 19.8796, -72.6874, -71.9702], 'perimeter': 412.6, 'neighbours': 'HT-AR,HT-CE,HT-NE,HT-NO'},
            'HT-NE': {'latlng': '19.5178,-71.8728', 'bounding_box': [19.2593, 19.7353, -72.1221, -71.6783], 'perimeter': 222.86, 'neighbours': 'HT-CE,HT-ND'},
            'HT-NI': {'latlng': '18.442,-73.3914', 'bounding_box': [18.2212, 18.5879, -73.78, -72.9949], 'perimeter': 387.15, 'neighbours': 'HT-GA,HT-OU,HT-SD,HT-SE'},
            'HT-NO': {'latlng': '19.8469,-73.059', 'bounding_box': [19.6206, 20.0896, -73.4557, -72.56], 'perimeter': 370.64, 'neighbours': 'HT-AR,HT-ND'},
            'HT-OU': {'latlng': '18.7669,-72.4387', 'bounding_box': [18.2582, 18.9771, -73.3014, -71.6952], 'perimeter': 798.38, 'neighbours': 'HT-AR,HT-CE,HT-NI,HT-SD,HT-SE'},
            'HT-SD': {'latlng': '18.2613,-73.8445', 'bounding_box': [18.0206, 18.4332, -74.452, -73.0012], 'perimeter': 576.36, 'neighbours': 'HT-GA,HT-NI,HT-OU,HT-SE'},
            'HT-SE': {'latlng': '18.2974,-72.3746', 'bounding_box': [18.0315, 18.4056, -73.0156, -71.7249], 'perimeter': 433.72, 'neighbours': 'HT-NI,HT-OU,HT-SD'},
            'RW-01': {'latlng': '-1.9534,30.114', 'bounding_box': [-2.0798, -1.7796, 29.9795, 30.2799], 'perimeter': 172.02, 'neighbours': 'RW-02,RW-03,RW-05'},
            'RW-02': {'latlng': '-1.7415,30.5404', 'bounding_box': [-2.4377, -1.0474, 29.959, 30.8991], 'perimeter': 606.57, 'neighbours': 'RW-01,RW-03,RW-05'},
            'RW-03': {'latlng': '-1.581,29.927', 'bounding_box': [-1.9128, -1.3088, 29.4503, 30.28], 'perimeter': 343.9, 'neighbours': 'RW-01,RW-02,RW-04,RW-05'},
            'RW-04': {'latlng': '-2.3799,29.2015', 'bounding_box': [-2.7434, -1.5062, 28.8617, 29.6752], 'perimeter': 516.17, 'neighbours': 'RW-03,RW-05'},
            'RW-05': {'latlng': '-2.6272,29.6063', 'bounding_box': [-2.8398, -1.7311, 29.2725, 30.0208], 'perimeter': 491.96, 'neighbours': 'RW-01,RW-02,RW-03,RW-04'},
        }
        country_names = {'AL': 'Albania', 'DK': 'Denmark', 'HT': 'Haiti', 'RW': 'Rwanda', 'SJ': 'Svalbard and Jan Mayen'}
        
        # Test initialization for multiple country codes, checking attributes and cached data
        for country_code in list(country_names.keys()):
            with self.subTest(country_code=country_code):
                geo = Geo(country_code, geo_cache_path=self.temp_cache_path)
                subdivisions = sorted([k for k in expected_subdivisions.keys() if k.startswith(country_code)])
                
                self.assertEqual(geo.country_code, country_code)
                self.assertEqual(geo.country_name, country_names[country_code])
                self.assertEqual(geo.subdivision_codes, subdivisions)
                self.assertEqual(geo.proxy, None)
                self.assertEqual(geo.verbose, False)
                self.assertEqual(geo.use_retry, True)
                self.assertEqual(geo.export_to_cache, True)
                self.assertEqual(geo.use_cache, True)
                self.assertEqual(geo.geo_cache_path, self.temp_cache_path)
                self.assertFalse(geo.geo_cache.empty)
                
                # Verify cached attribute values for subdivisions
                country_subdivisions = {k: v for k, v in expected_subdivisions.items() 
                                       if k.startswith(country_code)}
                
                # Check that each subdivision's attributes in cache match expected values
                for subdivision_code, expected_attrs in country_subdivisions.items():
                    cache_row = geo.geo_cache[geo.geo_cache['subdivisionCode'] == subdivision_code]
                    self.assertFalse(cache_row.empty, 
                                   f"Subdivision {subdivision_code} not found in cache for {country_code}")
                    
                    # Validate latLng
                    actual_latlng = cache_row.iloc[0]['latLng']
                    self.assertEqual(actual_latlng, expected_attrs['latlng'],
                                   f"latLng mismatch for {subdivision_code}: "
                                   f"expected '{expected_attrs['latlng']}', got '{actual_latlng}'")
                    
                    # Validate boundingBox
                    actual_bbox_str = cache_row.iloc[0]['boundingBox']
                    expected_bbox = expected_attrs['bounding_box']
                    actual_bbox = json.loads(actual_bbox_str)
                    self.assertEqual(actual_bbox, expected_bbox,
                                   f"boundingBox mismatch for {subdivision_code}: "
                                   f"expected {expected_bbox}, got {actual_bbox}")
                    
                    # Validate perimeter
                    actual_perimeter = cache_row.iloc[0]['perimeter']
                    expected_perimeter = expected_attrs['perimeter']
                    self.assertEqual(float(actual_perimeter), expected_perimeter,
                                   f"perimeter mismatch for {subdivision_code}: "
                                   f"expected {expected_perimeter}, got {actual_perimeter}")
                    
                    # Validate neighbours
                    actual_neighbours = cache_row.iloc[0]['neighbours']
                    expected_neighbours_str = expected_attrs['neighbours']
                    self.assertEqual(actual_neighbours, expected_neighbours_str,
                                   f"neighbours mismatch for {subdivision_code}: "
                                   f"expected '{expected_neighbours_str}', got '{actual_neighbours}'")
    
    # @unittest.skip("")
    def test_init_without_country_code(self):
        """ Test initialization without country code. """
        geo = Geo(geo_cache_path=self.temp_cache_path)
        self.assertIsNone(geo.country_code)
        self.assertIsNone(geo.country_name)
        self.assertIsNone(geo.subdivisions)
        self.assertIsNone(geo.subdivision_codes)
        self.assertEqual(geo.proxy, None)
        self.assertEqual(geo.verbose, False)
        self.assertEqual(geo.use_retry, True)
        self.assertEqual(geo.export_to_cache, True)
        self.assertEqual(geo.use_cache, True)
        self.assertEqual(geo.geo_cache_path, self.temp_cache_path)
        self.assertFalse(geo.geo_cache.empty)

    # @unittest.skip("")
    def test_init_error_country_code(self):
        """ Test initialization with erroneous country codes. """
        with self.assertRaises(ValueError):
            geo = Geo("XYZ") 
        with self.assertRaises(ValueError):
            geo = Geo("ABC")  
        with self.assertRaises(ValueError):
            geo = Geo("1234") 

    # @unittest.skip("")
    def test_get_lat_lng_cached(self):
        """ Test successful latLng retrieval via cache. """
        # Test cases with country codes and expected subdivision counts
        test_countries = {'LV': 43, 'US': 57, 'ZW': 10}
        
        # Iterate through test countries, validating latLng data
        for country_code, expected_count in test_countries.items():
            with self.subTest(country_code=country_code):
                lat_lngs = self.geo.get_lat_lng(country_code=country_code, verbose=False, export=False)
                
                # Validate return type and count
                self.assertIsInstance(lat_lngs, dict)
                self.assertEqual(len(lat_lngs), expected_count)
                
                # Validate all returned subdivision codes are valid for the country
                country_subdivision_codes = self.subd[country_code].subdivision_codes()
                lat_lngs_subdivision_codes = list(lat_lngs.keys())
                for code in country_subdivision_codes:
                    self.assertIn(code, lat_lngs_subdivision_codes,
                                 f"Invalid subdivision code '{code}' for country code '{country_code}'")
                
                # Validate latLng format and values
                for code, latlng in lat_lngs.items():
                    self.assertIsInstance(latlng, str, f"latLng value for {code} must be string")
                    
                    parts = latlng.replace(' ', '').split(',')
                    self.assertEqual(len(parts), 2, f"latLng '{latlng}' for {code} must be in format 'lat,lon'")
                    
                    try:
                        lat = float(parts[0])
                        lon = float(parts[1])
                    except ValueError:
                        self.fail(f"latLng '{latlng}' for {code} contains invalid numeric values")
                    
                    self.assertTrue(-90 <= lat <= 90, 
                                  f"Latitude {lat} for {code} is out of range [-90, 90]")
                    self.assertTrue(-180 <= lon <= 180, 
                                  f"Longitude {lon} for {code} is out of range [-180, 180]")
        
        # Test countries with no subdivisions return empty dict
        lat_lngs_ax = self.geo.get_lat_lng(country_code="AX", verbose=False, export=False)
        self.assertEqual(lat_lngs_ax, {})
        lat_lngs_bm = self.geo.get_lat_lng(country_code="BM", verbose=False, export=False)
        self.assertEqual(lat_lngs_bm, {})
        
        # Test error handling for invalid country codes
        with self.assertRaises(ValueError):
            self.geo.get_lat_lng("ABC", verbose=False, export=False)
        with self.assertRaises(ValueError):
            self.geo.get_lat_lng("123", verbose=False, export=False)

    # @unittest.skip("")
    def test_get_bounding_box_cached(self):
        """ Test successful bounding box retrieval via cache. """
        # Test cases with country codes and expected subdivision counts
        test_countries = {'CO': 33, 'HU': 43, 'ID': 45}
        
        # Iterate through test countries, validating bounding box data
        for country_code, expected_count in test_countries.items():
            with self.subTest(country_code=country_code):
                bounding_boxes = self.geo.get_bounding_box(country_code=country_code, verbose=False, export=False)
                
                # Validate return type and count
                self.assertIsInstance(bounding_boxes, dict)
                self.assertEqual(len(bounding_boxes), expected_count)
                
                # Validate all returned subdivision codes are valid for the country
                country_subdivision_codes = self.subd[country_code].subdivision_codes()
                bounding_boxes_subdivision_codes = list(bounding_boxes.keys())
                for code in country_subdivision_codes:
                    self.assertIn(code, bounding_boxes_subdivision_codes,
                                 f"Invalid subdivision code '{code}' for country code '{country_code}'")
                
                # Validate bbox format and values
                for code, bbox in bounding_boxes.items():
                    self.assertIsInstance(code, str)
                    # BoundingBox is either a list of 4 floats or empty list if not found in cache
                    self.assertIsInstance(bbox, list)
                    if bbox:  # If bbox is not empty
                        self.assertEqual(len(bbox), 4, f"BBox for {code} should have 4 values")
                        minlat, maxlat, minlon, maxlon = bbox
                        self.assertIsInstance(minlat, (int, float))
                        self.assertIsInstance(maxlat, (int, float))
                        self.assertIsInstance(minlon, (int, float))
                        self.assertIsInstance(maxlon, (int, float))
                        self.assertTrue(-90 <= minlat <= 90)
                        self.assertTrue(-90 <= maxlat <= 90)
                        self.assertTrue(-180 <= minlon <= 180)
                        self.assertTrue(-180 <= maxlon <= 180)
                        self.assertLessEqual(minlat, maxlat)
                        self.assertLessEqual(minlon, maxlon)
        
        # Test countries with no subdivisions return empty dict
        bounding_box_bv = self.geo.get_bounding_box(country_code="BV", verbose=False, export=False)
        self.assertEqual(bounding_box_bv, {})
        bounding_box_cc = self.geo.get_bounding_box(country_code="CC", verbose=False, export=False)
        self.assertEqual(bounding_box_cc, {})
        
        # Test error handling for invalid country codes
        with self.assertRaises(ValueError):
            self.geo.get_bounding_box("ABC", verbose=False, export=False)
        with self.assertRaises(ValueError):
            self.geo.get_bounding_box("123", verbose=False, export=False)

    # @unittest.skip("")
    @patch('geo.requests.get')
    def test_get_geojson_cached(self, mock_get):
        """ Test successful GeoJSON retrieval via cache - mocking call due to geojson being large. """
#1.)
        # Mock response for MX country
        mock_response_mx = MagicMock()
        mock_response_mx.json.return_value = [{
            'geojson': {'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'properties': {'name': 'MX-01'}, 'geometry': {'type': 'Polygon', 'coordinates': [[[-119.3, 37.2], [-114.1, 37.2], [-114.1, 42.0], [-119.3, 42.0], [-119.3, 37.2]]]}}]}
        }]
        mock_response_mx.raise_for_status = lambda: None
        mock_get.return_value = mock_response_mx
        
        geo_mx = Geo("MX", geo_cache_path=self.temp_cache_path)
        geojsons_mx = geo_mx.get_geojson(country_code="MX", verbose=False, export=False)
        
        # Validate return type and count
        self.assertIsInstance(geojsons_mx, dict)
        self.assertEqual(len(geojsons_mx), 32)
        self.assertTrue(mock_get.called)
        
        # Validate all returned subdivision codes are valid for the country
        mx_subdivision_codes = self.subd["MX"].subdivision_codes()
        geojsons_mx_subdivision_codes = list(geojsons_mx.keys())
        for code in mx_subdivision_codes:
            self.assertIn(code, geojsons_mx_subdivision_codes,
                         f"Invalid subdivision code '{code}' for country code 'MX'")
        
        for code, geojson in geojsons_mx.items():
            self.assertIsInstance(code, str)
            self.assertIsInstance(geojson, dict)
            self.assertIn('type', geojson)
            self.assertEqual(geojson['type'], 'FeatureCollection')
            self.assertIn('features', geojson)
            self.assertGreaterEqual(len(geojson['features']), 0)
#2.)
        # Mock response for BR country
        mock_response_br = MagicMock()
        mock_response_br.json.return_value = [{
            'geojson': {'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'properties': {'name': 'BR-01'}, 'geometry': {'type': 'Polygon', 'coordinates': [[[-50.0, -20.0], [-45.0, -20.0], [-45.0, -15.0], [-50.0, -15.0], [-50.0, -20.0]]]}}]}
        }]
        mock_response_br.raise_for_status = lambda: None
        mock_get.return_value = mock_response_br
        
        geo_br = Geo("BR", geo_cache_path=self.temp_cache_path)
        geojsons_br = geo_br.get_geojson(country_code="BR", verbose=False, export=False)
        
        # Validate return type and count
        self.assertIsInstance(geojsons_br, dict)
        self.assertEqual(len(geojsons_br), 27)
        
        # Validate all returned subdivision codes are valid for the country
        br_subdivision_codes = self.subd["BR"].subdivision_codes()
        geojsons_br_subdivision_codes = list(geojsons_br.keys())
        for code in br_subdivision_codes:
            self.assertIn(code, geojsons_br_subdivision_codes,
                         f"Invalid subdivision code '{code}' for country code 'BR'")
        
        for code, geojson in geojsons_br.items():
            self.assertIsInstance(code, str)
            self.assertIsInstance(geojson, dict)
            self.assertIn('type', geojson)
            self.assertEqual(geojson['type'], 'FeatureCollection')
            self.assertIn('features', geojson)
            self.assertGreaterEqual(len(geojson['features']), 0)
#3.)
        # Test countries with no subdivisions return empty dict
        geojsons_bv = self.geo.get_geojson(country_code="BV", verbose=False, export=False)
        self.assertEqual(geojsons_bv, {})
        geojsons_tk = self.geo.get_geojson(country_code="TK", verbose=False, export=False)
        self.assertEqual(geojsons_tk, {})
#4.)
        # Test error handling for invalid country codes
        with self.assertRaises(ValueError):
            self.geo.get_geojson("ABC", verbose=False, export=False)
        with self.assertRaises(ValueError):
            self.geo.get_geojson("123", verbose=False, export=False)

    @unittest.skip("")
    def test_get_perimeter_cached(self):
        """ Test successful perimeter retrieval via cache. """
#1.)
        perimeters_pt = self.geo.get_perimeter(country_code="PT", verbose=False, export=False)

        # Validate all returned subdivision codes are valid for the country
        pt_subdivision_codes = self.subd["PT"].subdivision_codes()
        perimeters_pt_subdivision_codes = list(perimeters_pt.keys())
        for code in pt_subdivision_codes:
            self.assertIn(code, perimeters_pt_subdivision_codes,
                         f"Invalid subdivision code '{code}' for country code 'PT'")
        
        # Validate perimeter values
        execpted_perimeters_pt = {'PT-01': 376.02, 'PT-02': 762.35, 'PT-03': 350.16, 'PT-04': 475.73, 'PT-05': 568.2, 
                                  'PT-06': 526.59, 'PT-07': 675.49, 'PT-08': 556.68, 'PT-09': 515.45, 'PT-10': 545.97, 
                                  'PT-11': 343.83, 'PT-12': 539.54, 'PT-13': 350.09, 'PT-14': 702.02, 'PT-15': 637.0, 
                                  'PT-16': 267.13, 'PT-17': 436.21, 'PT-18': 465.18, 'PT-20': 954.61, 'PT-30': 415.55}
        self.assertEqual(perimeters_pt, execpted_perimeters_pt)
#2.)
        perimeters_gr = self.geo.get_perimeter(country_code="GR", verbose=False, export=False)

        # Validate all returned subdivision codes are valid for the country
        gr_subdivision_codes = self.subd["GR"].subdivision_codes()
        perimeters_gr_subdivision_codes = list(perimeters_gr.keys())
        for code in gr_subdivision_codes:
            self.assertIn(code, perimeters_gr_subdivision_codes,
                         f"Invalid subdivision code '{code}' for country code 'GR'")
        
        # Validate perimeter values
        execpted_perimeters_gr = {'GR-69': 165.53, 'GR-A': 1174.21, 'GR-B': 956.09, 'GR-C': 568.43, 'GR-D': 627.01, 'GR-E': 1065.0, 
                                 'GR-F': 975.11, 'GR-G': 841.31, 'GR-H': 1222.02, 'GR-I': 1058.0, 'GR-J': 951.1, 'GR-K': 1153.99, 
                                 'GR-L': 3525.09, 'GR-M': 945.28}
        self.assertEqual(perimeters_gr, execpted_perimeters_gr)
#3.)
        perimeters_no = self.geo.get_perimeter(country_code="NO", verbose=False, export=False)

        # Validate all returned subdivision codes are valid for the country
        no_subdivision_codes = self.subd["NO"].subdivision_codes()
        perimeters_no_subdivision_codes = list(perimeters_no.keys())
        for code in no_subdivision_codes:
            self.assertIn(code, perimeters_no_subdivision_codes,
                         f"Invalid subdivision code '{code}' for country code 'NO'")
        
        # Validate perimeter values - all subdivisions should be included even without perimeter values
        execpted_perimeters_no = {'NO-03': 118.15, 'NO-11': 725.47, 'NO-15': 915.61, 'NO-18': 1643.75, 'NO-21': 2759.47, 'NO-22': 259.22, 
                                  'NO-30': 5.07, 'NO-34': 1375.1, 'NO-38': 0.73, 'NO-42': 808.43, 'NO-46': 1154.32, 'NO-50': 1538.68, 'NO-54': 5.93}
        self.assertEqual(perimeters_no, execpted_perimeters_no)
#4.)
        # Test countries with no subdivisions return empty dict
        perimeters_bv = self.geo.get_perimeter(country_code="BV", verbose=False, export=False)
        self.assertEqual(perimeters_bv, {})
        perimeters_fk = self.geo.get_perimeter(country_code="FK", verbose=False, export=False)
        self.assertEqual(perimeters_fk, {})
#5.)
        # Test error handling for invalid country codes
        with self.assertRaises(ValueError):
            self.geo.get_perimeter("ABC", verbose=False, export=False)
        with self.assertRaises(ValueError):
            self.geo.get_perimeter("123", verbose=False, export=False)

    # @unittest.skip("")
    def test_get_neighbours_cached(self):
        """ Test successful neighbor detection via cache. """
#1.)
        neighbours_be = self.geo.get_neighbours(country_code="BE", verbose=False, export=False)

        # Validate all returned subdivision codes are valid for the country
        be_subdivision_codes = self.subd["BE"].subdivision_codes()
        neighbours_be_subdivision_codes = list(neighbours_be.keys())
        for code in be_subdivision_codes:
            self.assertIn(code, neighbours_be_subdivision_codes,
                         f"Invalid subdivision code '{code}' for country code 'BE'")
        
        # Validate neighbours values
        expected_neighbours_be = {
            'BE-BRU': ['BE-VBR', 'BE-VLG', 'BE-VOV', 'BE-WAL', 'BE-WBR', 'BE-WHT'],
            'BE-VAN': ['BE-VBR', 'BE-VLG', 'BE-VLI', 'BE-VOV'],
            'BE-VBR': ['BE-BRU', 'BE-VAN', 'BE-VLG', 'BE-VLI', 'BE-VOV', 'BE-WAL', 'BE-WBR', 'BE-WHT', 'BE-WLG'],
            'BE-VLG': ['BE-BRU', 'BE-VAN', 'BE-VBR', 'BE-VLI', 'BE-VOV', 'BE-VWV', 'BE-WAL', 'BE-WBR', 'BE-WHT', 'BE-WLG'],
            'BE-VLI': ['BE-VAN', 'BE-VBR', 'BE-VLG', 'BE-WAL', 'BE-WBR', 'BE-WLG'],
            'BE-VOV': ['BE-BRU', 'BE-VAN', 'BE-VBR', 'BE-VLG', 'BE-VWV', 'BE-WAL', 'BE-WBR', 'BE-WHT'],
            'BE-VWV': ['BE-VLG', 'BE-VOV', 'BE-WAL', 'BE-WHT'],
            'BE-WAL': ['BE-BRU', 'BE-VBR', 'BE-VLG', 'BE-VLI', 'BE-VOV', 'BE-VWV', 'BE-WBR', 'BE-WHT', 'BE-WLG', 'BE-WLX', 'BE-WNA'],
            'BE-WBR': ['BE-BRU', 'BE-VBR', 'BE-VLG', 'BE-VLI', 'BE-VOV', 'BE-WAL', 'BE-WHT', 'BE-WLG', 'BE-WNA'],
            'BE-WHT': ['BE-BRU', 'BE-VBR', 'BE-VLG', 'BE-VOV', 'BE-VWV', 'BE-WAL', 'BE-WBR', 'BE-WNA'],
            'BE-WLG': ['BE-VBR', 'BE-VLG', 'BE-VLI', 'BE-WAL', 'BE-WBR', 'BE-WLX', 'BE-WNA'],
            'BE-WLX': ['BE-WAL', 'BE-WLG', 'BE-WNA'],
            'BE-WNA': ['BE-WAL', 'BE-WBR', 'BE-WHT', 'BE-WLG', 'BE-WLX']
        }
        self.assertEqual(neighbours_be, expected_neighbours_be)
#2.)
        neighbours_bw = self.geo.get_neighbours(country_code="BW", verbose=False, export=False)

        # Validate all returned subdivision codes are valid for the country
        bw_subdivision_codes = self.subd["BW"].subdivision_codes()
        neighbours_bw_subdivision_codes = list(neighbours_bw.keys())
        for code in bw_subdivision_codes:
            self.assertIn(code, neighbours_bw_subdivision_codes,
                         f"Invalid subdivision code '{code}' for country code 'BW'")
        
        # Validate neighbours values
        expected_neighbours_bw = {
            'BW-CE': ['BW-CH', 'BW-FR', 'BW-GH', 'BW-KG', 'BW-KL', 'BW-KW', 'BW-NE', 'BW-NW', 'BW-SP', 'BW-ST'],
            'BW-CH': ['BW-CE', 'BW-NW'],
            'BW-FR': ['BW-CE', 'BW-NE'],
            'BW-GA': ['BW-KL', 'BW-KW', 'BW-SE'],
            'BW-GH': ['BW-CE', 'BW-KG', 'BW-KW', 'BW-NW'],
            'BW-JW': ['BW-KW', 'BW-SO'],
            'BW-KG': ['BW-CE', 'BW-GH', 'BW-KW', 'BW-SO'],
            'BW-KL': ['BW-CE', 'BW-GA', 'BW-KW', 'BW-SE'],
            'BW-KW': ['BW-CE', 'BW-GA', 'BW-GH', 'BW-JW', 'BW-KG', 'BW-KL', 'BW-SE', 'BW-SO'],
            'BW-LO': ['BW-SE', 'BW-SO'],
            'BW-NE': ['BW-CE', 'BW-FR'],
            'BW-NW': ['BW-CE', 'BW-CH', 'BW-GH'],
            'BW-SE': ['BW-GA', 'BW-KL', 'BW-KW', 'BW-LO', 'BW-SO'],
            'BW-SO': ['BW-JW', 'BW-KG', 'BW-KW', 'BW-LO', 'BW-SE'],
            'BW-SP': ['BW-CE'],
            'BW-ST': ['BW-CE']
        }
        self.assertEqual(neighbours_bw, expected_neighbours_bw)
#3.)
        neighbours_gw = self.geo.get_neighbours(country_code="GW", verbose=False, export=False)

        # Validate all returned subdivision codes are valid for the country
        gw_subdivision_codes = self.subd["GW"].subdivision_codes()
        neighbours_gw_subdivision_codes = list(neighbours_gw.keys())
        for code in gw_subdivision_codes:
            self.assertIn(code, neighbours_gw_subdivision_codes,
                         f"Invalid subdivision code '{code}' for country code 'GW'")
        
        # Validate neighbours values
        expected_neighbours_gw = {
            'GW-BA': ['GW-GA', 'GW-L', 'GW-N', 'GW-OI', 'GW-QU', 'GW-S', 'GW-TO'],
            'GW-BL': ['GW-QU', 'GW-S', 'GW-TO'],
            'GW-BM': ['GW-BS', 'GW-CA', 'GW-N', 'GW-OI', 'GW-QU', 'GW-S'],
            'GW-BS': ['GW-BM', 'GW-CA', 'GW-N', 'GW-OI', 'GW-QU', 'GW-S'],
            'GW-CA': ['GW-BM', 'GW-BS', 'GW-N', 'GW-OI', 'GW-QU', 'GW-S'],
            'GW-GA': ['GW-BA', 'GW-L', 'GW-S', 'GW-TO'],
            'GW-L': ['GW-BA', 'GW-GA', 'GW-N', 'GW-OI', 'GW-QU', 'GW-S', 'GW-TO'],
            'GW-N': ['GW-BA', 'GW-BM', 'GW-BS', 'GW-CA', 'GW-L', 'GW-OI', 'GW-QU', 'GW-S'],
            'GW-OI': ['GW-BA', 'GW-BM', 'GW-BS', 'GW-CA', 'GW-L', 'GW-N', 'GW-QU', 'GW-S'],
            'GW-QU': ['GW-BA', 'GW-BL', 'GW-BM', 'GW-BS', 'GW-CA', 'GW-L', 'GW-N', 'GW-OI', 'GW-S', 'GW-TO'],
            'GW-S': ['GW-BA', 'GW-BL', 'GW-BM', 'GW-BS', 'GW-CA', 'GW-GA', 'GW-L', 'GW-N', 'GW-OI', 'GW-QU', 'GW-TO'],
            'GW-TO': ['GW-BA', 'GW-BL', 'GW-GA', 'GW-L', 'GW-QU', 'GW-S']
        }
        self.assertEqual(neighbours_gw, expected_neighbours_gw)
#4.)
        # Test countries with no subdivisions return empty dict
        neighbours_bv = self.geo.get_neighbours(country_code="BV", verbose=False, export=False)
        self.assertEqual(neighbours_bv, {})
        neighbours_gi = self.geo.get_neighbours(country_code="GI", verbose=False, export=False)
        self.assertEqual(neighbours_gi, {})
#5.)
        # Validate bidirectional neighbours relationship
        # For all subdivisions in cache with neighbours, ensure the relationship is bidirectional
        for _, row in self.geo.geo_cache.iterrows():
            subdivision_code = row['subdivisionCode']
            neighbours_str = row['neighbours']
            
            # Skip if no neighbours or empty neighbours
            if pd.isna(neighbours_str) or not neighbours_str:
                continue
            
            # Parse the comma-separated neighbours list
            neighbours_list = neighbours_str.split(',') if isinstance(neighbours_str, str) else []
            
            # For each neighbour, verify bidirectional relationship
            for neighbour_code in neighbours_list:
                if not neighbour_code:  # Skip empty strings
                    continue
                    
                neighbour_row = self.geo.geo_cache[self.geo.geo_cache['subdivisionCode'] == neighbour_code]
                if not neighbour_row.empty:
                    neighbour_neighbours_str = neighbour_row['neighbours'].values[0]
                    if pd.notna(neighbour_neighbours_str):
                        neighbour_neighbours_list = neighbour_neighbours_str.split(',') if isinstance(neighbour_neighbours_str, str) else []
                        self.assertIn(subdivision_code, neighbour_neighbours_list,
                                     f"{subdivision_code} and {neighbour_code} not bidirectional")
#6.)
        # Validate that all neighbours are valid subdivision codes for the same country
        for _, row in self.geo.geo_cache.iterrows():
            subdivision_code = row['subdivisionCode']
            neighbours_str = row['neighbours']
            
            if pd.isna(neighbours_str) or not neighbours_str:
                continue
            
            # Extract country code from subdivision (e.g., "BE-BRU" -> "BE")
            # get list of subdivison codes and neighbour list
            country_code = str(subdivision_code).split('-')[0]
            valid_codes = self.subd[country_code].subdivision_codes()
            neighbours_list = neighbours_str.split(',') if isinstance(neighbours_str, str) else []
            
            for neighbour_code in neighbours_list:
                if not neighbour_code:
                    continue
                
                # Check that neighbour is valid for the country
                self.assertIn(neighbour_code, valid_codes,
                             f"{neighbour_code} not valid for {country_code}")
                
                # Check that subdivision doesn't have itself as a neighbour
                self.assertNotEqual(subdivision_code, neighbour_code,
                                   f"{subdivision_code} cannot be its own neighbour")
#7.)
        # Test error handling for invalid country codes
        with self.assertRaises(ValueError):
            self.geo.get_neighbours("ABC", verbose=False, export=False)
        with self.assertRaises(ValueError):
            self.geo.get_neighbours("123", verbose=False, export=False)
    
    # @unittest.skip("")
    def test_get_all_cached(self):
        """ Test get_all method that combines all geographical data via cache. """
#1.)
        all_jm = self.geo.get_all(country_code="JM", verbose=False, export=False)

        # Validate return type and count
        self.assertIsInstance(all_jm, dict)
        self.assertEqual(len(all_jm), 14)

        # Validate all returned subdivision codes are valid for the country
        jm_subdivision_codes = self.subd["JM"].subdivision_codes()
        all_jm_subdivision_codes = list(all_jm.keys())
        for code in jm_subdivision_codes:
            self.assertIn(code, all_jm_subdivision_codes,
                         f"Invalid subdivision code '{code}' for country code 'JM'")

        # Validate all attributes for each subdivision
        expected_all_jm = {
            'JM-01': {'latLng': '17.9693,-76.7652', 'bounding_box': [17.9282, 17.9861, -76.8471, -76.7205], 'perimeter': 75.79, 'neighbours': ['JM-02', 'JM-14']},
            'JM-02': {'latLng': '18.059,-76.7608', 'bounding_box': [17.938, 18.1798, -76.8896, -76.6173], 'perimeter': 141.61, 'neighbours': ['JM-01', 'JM-03', 'JM-04', 'JM-05', 'JM-14']},
            'JM-03': {'latLng': '17.9716,-76.4414', 'bounding_box': [17.8502, 18.093, -76.6681, -76.183], 'perimeter': 176.59, 'neighbours': ['JM-02', 'JM-04']},
            'JM-04': {'latLng': '18.1268,-76.5374', 'bounding_box': [17.9869, 18.2668, -76.753, -76.258], 'perimeter': 184.9, 'neighbours': ['JM-02', 'JM-03', 'JM-05']},
            'JM-05': {'latLng': '18.2789,-76.9022', 'bounding_box': [18.1338, 18.4241, -77.0722, -76.6983], 'perimeter': 164.95, 'neighbours': ['JM-02', 'JM-04', 'JM-06', 'JM-14']},
            'JM-06': {'latLng': '18.3299,-77.2542', 'bounding_box': [18.1808, 18.4799, -77.4942, -76.9966], 'perimeter': 177.24, 'neighbours': ['JM-05', 'JM-07', 'JM-12', 'JM-13', 'JM-14']},
            'JM-07': {'latLng': '18.3682,-77.6044', 'bounding_box': [18.2098, 18.5116, -77.7757, -77.4416], 'perimeter': 140.64, 'neighbours': ['JM-06', 'JM-08', 'JM-11', 'JM-12', 'JM-13']},
            'JM-08': {'latLng': '18.3658,-77.8522', 'bounding_box': [18.2062, 18.5251, -77.9967, -77.7361], 'perimeter': 133.51, 'neighbours': ['JM-07', 'JM-09', 'JM-10', 'JM-11']},
            'JM-09': {'latLng': '18.3851,-78.131', 'bounding_box': [18.3072, 18.4628, -78.345, -77.9097], 'perimeter': 154.85, 'neighbours': ['JM-08', 'JM-10']},
            'JM-10': {'latLng': '18.2104,-77.9793', 'bounding_box': [18.063, 18.3578, -78.3689, -77.8757], 'perimeter': 164.84, 'neighbours': ['JM-08', 'JM-09', 'JM-11']},
            'JM-11': {'latLng': '18.0538,-77.7828', 'bounding_box': [17.8544, 18.2532, -77.9521, -77.5666], 'perimeter': 154.68, 'neighbours': ['JM-07', 'JM-08', 'JM-10', 'JM-12']},
            'JM-12': {'latLng': '18.0499,-77.511', 'bounding_box': [17.8386, 18.2444, -77.6385, -77.346], 'perimeter': 127.69, 'neighbours': ['JM-06', 'JM-07', 'JM-11', 'JM-13']},
            'JM-13': {'latLng': '17.9519,-77.2719', 'bounding_box': [17.7056, 18.2098, -77.4942, -77.125], 'perimeter': 206.51, 'neighbours': ['JM-06', 'JM-07', 'JM-12', 'JM-14']},
            'JM-14': {'latLng': '18.0472,-77.0334', 'bounding_box': [17.8379, 18.2579, -77.2193, -76.839], 'perimeter': 209.62, 'neighbours': ['JM-01', 'JM-02', 'JM-05', 'JM-06', 'JM-13']}
        }
        self.assertEqual(all_jm, expected_all_jm)
#2.)
        all_kg = self.geo.get_all(country_code="KG", verbose=False, export=False)

        # Validate return type and count
        self.assertIsInstance(all_kg, dict)
        self.assertEqual(len(all_kg), 9)

        # Validate all returned subdivision codes are valid for the country
        kg_subdivision_codes = self.subd["KG"].subdivision_codes()
        all_kg_subdivision_codes = list(all_kg.keys())
        for code in kg_subdivision_codes:
            self.assertIn(code, all_kg_subdivision_codes,
                         f"Invalid subdivision code '{code}' for country code 'KG'")

        # Validate all attributes for each subdivision
        expected_all_kg = {
            'KG-B': {'latLng': '39.7931,70.8512', 'bounding_box': [39.3886, 40.3436, 69.265, 72.5455], 'perimeter': 1053.38, 'neighbours': ['KG-O']},
            'KG-C': {'latLng': '42.6672,75.2094', 'bounding_box': [41.8432, 43.2669, 73.0465, 77.2259], 'perimeter': 1151.01, 'neighbours': ['KG-GB', 'KG-J', 'KG-N', 'KG-T', 'KG-Y']},
            'KG-GB': {'latLng': '42.8761,74.6037', 'bounding_box': [42.7156, 43.0125, 74.4549, 74.7177], 'perimeter': 150.39, 'neighbours': ['KG-C']},
            'KG-GO': {'latLng': '40.4936,72.77', 'bounding_box': [40.3989, 40.5882, 72.677, 72.8804], 'perimeter': 99.98, 'neighbours': ['KG-O']},
            'KG-J': {'latLng': '41.5107,73.2283', 'bounding_box': [40.8004, 42.2208, 70.169, 74.7371], 'perimeter': 1532.47, 'neighbours': ['KG-C', 'KG-N', 'KG-O', 'KG-T']},
            'KG-N': {'latLng': '41.3671,75.9932', 'bounding_box': [40.2798, 42.4546, 73.7118, 77.905], 'perimeter': 1712.23, 'neighbours': ['KG-C', 'KG-J', 'KG-O', 'KG-Y']},
            'KG-O': {'latLng': '40.1622,73.3667', 'bounding_box': [39.1823, 41.1422, 71.4989, 74.9106], 'perimeter': 1534.66, 'neighbours': ['KG-B', 'KG-GO', 'KG-J', 'KG-N']},
            'KG-T': {'latLng': '42.4194,72.1416', 'bounding_box': [42.048, 42.8386, 70.8652, 73.6588], 'perimeter': 719.82, 'neighbours': ['KG-C', 'KG-J']},
            'KG-Y': {'latLng': '42.0614,78.162', 'bounding_box': [41.1816, 42.9411, 75.6415, 80.2296], 'perimeter': 1309.65, 'neighbours': ['KG-C', 'KG-N']}
        }
        self.assertEqual(all_kg, expected_all_kg)
#3.)
        all_ls = self.geo.get_all(country_code="LS", verbose=False, export=False)

        # Validate return type and count
        self.assertIsInstance(all_ls, dict)
        self.assertEqual(len(all_ls), 10)

        # Validate all returned subdivision codes are valid for the country
        ls_subdivision_codes = self.subd["LS"].subdivision_codes()
        all_ls_subdivision_codes = list(all_ls.keys())
        for code in ls_subdivision_codes:
            self.assertIn(code, all_ls_subdivision_codes,
                         f"Invalid subdivision code '{code}' for country code 'LS'")

        # Validate all attributes for each subdivision
        expected_all_ls = {
            'LS-A': {'latLng': '-29.5817,27.8243', 'bounding_box': [-29.9252, -29.2755, 27.2999, 28.2506], 'perimeter': 593.67, 'neighbours': ['LS-C', 'LS-D', 'LS-E', 'LS-F', 'LS-H', 'LS-K']},
            'LS-B': {'latLng': '-28.803,28.5638', 'bounding_box': [-29.086, -28.5706, 28.2232, 28.8192], 'perimeter': 278.48, 'neighbours': ['LS-C', 'LS-D', 'LS-J']},
            'LS-C': {'latLng': '-29.0183,28.2637', 'bounding_box': [-29.3703, -28.6937, 27.639, 28.7944], 'perimeter': 607.11, 'neighbours': ['LS-A', 'LS-B', 'LS-D', 'LS-J', 'LS-K']},
            'LS-D': {'latLng': '-29.1964,27.9176', 'bounding_box': [-29.3964, -28.946, 27.5099, 28.2936], 'perimeter': 388.8, 'neighbours': ['LS-A', 'LS-B', 'LS-C', 'LS-K']},
            'LS-E': {'latLng': '-29.7893,27.4423', 'bounding_box': [-30.058, -29.5263, 27.0114, 28.0642], 'perimeter': 501.78, 'neighbours': ['LS-A', 'LS-F', 'LS-G']},
            'LS-F': {'latLng': '-30.0697,27.8039', 'bounding_box': [-30.4148, -29.7832, 27.1776, 28.5967], 'perimeter': 642.8, 'neighbours': ['LS-A', 'LS-E', 'LS-G', 'LS-H', 'LS-K']},
            'LS-G': {'latLng': '-30.3601,27.9856', 'bounding_box': [-30.678, -30.0229, 27.5574, 28.3698], 'perimeter': 382.3, 'neighbours': ['LS-E', 'LS-F', 'LS-H']},
            'LS-H': {'latLng': '-29.9657,28.7381', 'bounding_box': [-30.1701, -29.7101, 28.2236, 29.1697], 'perimeter': 385.93, 'neighbours': ['LS-A', 'LS-F', 'LS-G', 'LS-K']},
            'LS-J': {'latLng': '-29.2191,29.0351', 'bounding_box': [-29.5817, -28.756, 28.556, 29.4557], 'perimeter': 478.63, 'neighbours': ['LS-B', 'LS-C', 'LS-K']},
            'LS-K': {'latLng': '-29.5699,28.5938', 'bounding_box': [-29.8922, -29.1189, 28.0934, 29.3251], 'perimeter': 660.72, 'neighbours': ['LS-A', 'LS-C', 'LS-D', 'LS-F', 'LS-H', 'LS-J']}
        }
        self.assertEqual(all_ls, expected_all_ls)
#4.)
        # Test countries with no subdivisions return empty dict
        all_bv = self.geo.get_all(country_code="BV", verbose=False, export=False)
        self.assertEqual(all_bv, {})
        all_gi = self.geo.get_all(country_code="GI", verbose=False, export=False)
        self.assertEqual(all_gi, {})
#5.)
        # Test error handling for invalid country codes
        with self.assertRaises(ValueError):
            self.geo.get_all("ABC", verbose=False, export=False)
        with self.assertRaises(ValueError):
            self.geo.get_all("123", verbose=False, export=False)
        
    # @unittest.skip("")
    def test_get_statistics(self):
        """ Test statistics calculation with valid cache file. """
        # Use the test cache file
        stats = self.geo.get_statistics(geo_cache_filepath=self.temp_cache_path)
        
        expected_stats = {
            'cache_file': 'tests/test_files/test_geo_cache.csv',
            'cache_file_size': '552.96 KB',
            'total_entries': 5046,
            'data_completeness': {
                'complete_entries': 5032,
                'complete_percentage': 99.72,
                'empty_entries': 0,
                'empty_percentage': 0.0,
                'partial_entries': 14
            },
            'latLngs': {
                'count': 5046,
                'percentage': 100.0,
                'stats': {
                    'lats': {'min': -54.3815, 'max': 78.7199, 'mean': 26.8105, 'median': 32.6169},
                    'lons': {'min': -179.394, 'max': 179.6368, 'mean': 22.4684, 'median': 18.9215}
                }
            },
            'bounding_boxes': {
                'count': 5046,
                'percentage': 100.0,
                'widths': {'min': 0.0001, 'max': 360.0, 'mean': 2.4328, 'median': 1.0066},
                'heights': {'min': 0.0, 'max': 38.9047, 'mean': 1.4257, 'median': 0.8},
                'areas': {'min': 0.0, 'max': 10012.515, 'mean': 12.9184, 'median': 0.8016}
            },
            'perimeters': {
                'count': 5032,
                'percentage': 99.72,
                'stats': {'min': 0.03, 'max': 18456.5, 'mean': 764.45, 'median': 429.23, 'total': 3846694.27}
            }
        }
        self.assertEqual(stats, expected_stats)
        
        with self.assertRaises(FileNotFoundError):
            self.geo.get_statistics(geo_cache_filepath='/nonexistent/path/cache.csv')
    
    # @unittest.skip("")
    def test_clear_cache(self):
        """ Test cache clearing functionality. """
        geo_clear_cache = Geo(geo_cache_path=self.temp_cache_path)
        
        # Verify cache is loaded
        self.assertIsNotNone(geo_clear_cache.geo_cache)
        self.assertFalse(geo_clear_cache.geo_cache.empty)
        self.assertEqual(len(geo_clear_cache.geo_cache), 5046)
        
        # Clear the cache
        geo_clear_cache._clear_cache()
        
        # Verify cache is now None
        self.assertIsNone(geo_clear_cache.geo_cache)
        
        # Verify len() returns 0 for None cache
        self.assertEqual(len(geo_clear_cache), 0)
    
    @unittest.skip("")
    def test_export_cache_file(self):
        """ Test that cache export creates a file. """
        # Create cache data
        cache_path = os.path.join("tests", "test_files", "test_geo_cache_export.csv")
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        
        geo = Geo("US", geo_cache_path=cache_path, use_cache=False, export_to_cache=True)
        geo.geo_cache = pd.DataFrame({
            'subdivisionCode': ['US-CA'],
            'latLng': ['37.0,-120.0'],
            'boundingBox': ['[32.5,42.0,-124.5,-114.1]'],
            'geojson': [None],
            'perimeter': [2386.97],
            'neighbours': ['US-CO,US-NM,US-NV,US-UT']
        })
        
        geo._export_cache()
        
        # Check file was created
        self.assertTrue(os.path.exists(cache_path), f"Cache file was not created at {cache_path}")
        
        # Verify contents
        df = pd.read_csv(cache_path)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['subdivisionCode'], 'US-CA')
    
        # Remove the test cache file
        if os.path.exists(cache_path):
            os.remove(cache_path)

    # @unittest.skip("")
    def test_str(self):
        """ Test string representation of Geo instance. """
        geo = Geo("TZ", geo_cache_path=self.temp_cache_path)
        str_repr = str(geo)
        self.assertEqual(str_repr, "Geo(Tanzania, United Republic of [TZ]) - 31 subdivisions")
    
    # @unittest.skip("")
    def test_repr(self):
        """ Test repr representation of Geo instance. """
        geo = Geo("TZ", geo_cache_path=self.temp_cache_path)
        repr_str = repr(geo)
        self.assertEqual(repr_str, "Geo(country_code='TZ', country_name='Tanzania, United Republic of', subdivisions=31, cached_entries=5046, cache_loaded=True, verbose=False, use_cache=True, cache_path='tests/test_files/test_geo_cache.csv')")
    
    # @unittest.skip("")
    def test_len(self):
        """ Test __len__ returns cache size. """
        geo = Geo(geo_cache_path=self.temp_cache_path)
        self.assertEqual(len(geo), 5046, f"Expected length of cache to be 5046 rows, got {len(geo)}.")
        
    def tearDown(self):
        """ Clean up test fixtures. """
        self.print_patcher.stop()


# @unittest.skip("")
class GeoIntegrationTests(unittest.TestCase):
    """
    Integration tests for Geo class with real API calls. 

    Test Cases
    ==========
    test_get_latLng_real_api_call:
        test get_lat_lng with real API calls for US, GQ, UY
    test_get_bounding_box_real_api_call:
        test get_bounding_box with real API calls for BR, ES, DE
    test_get_geojson_real_api_call:
        test get_geojson with real API calls for TM, TO, VC
    test_get_perimeter_real_api_call:
        test get_perimeter with real API calls for AT, ER, IQ with cache validation
    test_get_neighbours_real_api_call:
        test get_neighbours with real API calls for BE, ZA, IN with reciprocal validation
    test_get_all_real_api_call:
        test get_all with real API calls for OM, MX, CA including comprehensive attribute validation
    """
    def setUp(self):
        """ Set up test fixtures. """
        self.print_patcher = patch('builtins.print'); self.print_patcher.start()
        # create Subdivisions instance for reference, get flattened list of subdivision codes
        self.subd = Subdivisions()
        self.subdivision_codes = list(self.subd.subdivision_codes().values())
        self.subdivision_codes = [item for sublist in self.subdivision_codes for item in sublist]

        #create Geo instance for testing
        self.geo = Geo()
    
    # @unittest.skip("")
    def test_get_latLng_real_api_call(self):
        """Test get_lat_lng with real API call making actual API requests."""
        # Test cases with country codes for real API calls
        test_countries = ['US', 'GQ', 'UY']
        
        for country_code in test_countries:
            with self.subTest(country_code=country_code):
                geo = Geo(country_code, use_cache=False)

                self.assertIsNone(geo.geo_cache, "Geo cache should not be loaded.")

                # Retrieve latLngs
                latLngs = geo.get_lat_lng(country_code=country_code, verbose=False, export=False)
                
                # Validate return type
                self.assertIsInstance(latLngs, dict)
                self.assertGreater(len(latLngs), 0)
                
                # Validate all returned subdivision codes are valid for the country
                country_subdivision_codes = self.subd[country_code].subdivision_codes()
                latLngs_subdivision_codes = list(latLngs.keys())
                
                for code in latLngs_subdivision_codes:
                    self.assertIn(code, country_subdivision_codes,
                                 f"Invalid subdivision code '{code}' for country code '{country_code}'")
                
                # Validate latLng format and values
                for code, latlng in latLngs.items():
                    self.assertIsInstance(latlng, str, f"latLng value for {code} must be string")
                    
                    # Validate latLng data is in cache
                    cached_latlng = geo.geo_cache[geo.geo_cache['subdivisionCode'] == code]['latLng'].values
                    self.assertTrue(len(cached_latlng) > 0, f"Subdivision code {code} not found in cache")
                    self.assertEqual(latlng, cached_latlng[0], 
                                   f"latLng for {code} does not match cached value")
                    
                    # Validate latLng format "lat,lon"
                    parts = latlng.replace(' ', '').split(',')
                    self.assertEqual(len(parts), 2, f"latLng '{latlng}' for {code} must be in format 'lat,lon'")
                    
                    # Validate lat and lon are floats and within valid ranges
                    try:
                        lat = float(parts[0])
                        lon = float(parts[1])
                    except ValueError:
                        self.fail(f"latLng '{latlng}' for {code} contains invalid numeric values")
                    
                    self.assertTrue(-90 <= lat <= 90, 
                                  f"Latitude {lat} for {code} is out of range [-90, 90]")
                    self.assertTrue(-180 <= lon <= 180, 
                                  f"Longitude {lon} for {code} is out of range [-180, 180]")
                    
                    # Validate other attributes are None for newly fetched latLng-only data
                    cached_row = geo.geo_cache[geo.geo_cache['subdivisionCode'] == code]
                    if not cached_row.empty:
                        bounded_box_val = cached_row['boundingBox'].values[0]
                        geojson_val = cached_row['geojson'].values[0]
                        perimeter_val = cached_row['perimeter'].values[0]
                        neighbours_val = cached_row['neighbours'].values[0]
                        
                        # Check that other attributes are None or NaN (not yet fetched)
                        self.assertTrue(bounded_box_val is None or (isinstance(bounded_box_val, float) and pd.isna(bounded_box_val)),
                                      f"boundingBox for {code} should be None or NaN, got {bounded_box_val}")
                        self.assertTrue(geojson_val is None or (isinstance(geojson_val, float) and pd.isna(geojson_val)),
                                      f"geojson for {code} should be None or NaN, got {geojson_val}")
                        self.assertTrue(perimeter_val is None or (isinstance(perimeter_val, float) and pd.isna(perimeter_val)),
                                      f"perimeter for {code} should be None or NaN, got {perimeter_val}")
                        self.assertTrue(neighbours_val is None or (isinstance(neighbours_val, float) and pd.isna(neighbours_val)),
                                      f"neighbours for {code} should be None or NaN, got {neighbours_val}")

        # Test countries with no subdivisions return empty dict
        geo_bv = Geo("BV")
        latLngs_bv = geo_bv.get_lat_lng(country_code="BV", verbose=False, export=False)
        self.assertEqual(latLngs_bv, {})
        
        geo_tk = Geo("TK")
        latLngs_tk = geo_tk.get_lat_lng(country_code="TK", verbose=False, export=False)
        self.assertEqual(latLngs_tk, {})

        # Test error handling for invalid country codes
        with self.assertRaises(ValueError):
            self.geo.get_lat_lng("ABC", verbose=False, export=False)
        with self.assertRaises(ValueError):
            self.geo.get_lat_lng("123", verbose=False, export=False)

    # @unittest.skip("")
    def test_get_bounding_box_real_api_call(self):
        """ Test get_bounding_box with real API call making actual API requests. """
        # Test cases with country codes for real API calls
        test_countries = ['BR', 'ES', 'DE']
        
        for country_code in test_countries:
            with self.subTest(country_code=country_code):
                geo = Geo(country_code=country_code)
                bounding_boxes = geo.get_bounding_box(country_code=country_code, verbose=False, export=False)
                
                # Validate return type
                self.assertIsInstance(bounding_boxes, dict)
                self.assertGreater(len(bounding_boxes), 0)
                
                # Validate all returned subdivision codes are valid for the country
                country_subdivision_codes = self.subd[country_code].subdivision_codes()
                bounding_boxes_subdivision_codes = list(bounding_boxes.keys())
                
                for code in country_subdivision_codes:
                    self.assertIn(code, bounding_boxes_subdivision_codes,
                                 f"Invalid subdivision code '{code}' for country code '{country_code}'")
                
                # Validate bbox format and values
                for code, bbox in bounding_boxes.items():
                    self.assertIsInstance(code, str)
                    # BoundingBox is either a list of 4 floats or empty list if not found
                    self.assertIsInstance(bbox, list)
                    if bbox:  # If bbox is not empty
                        self.assertEqual(len(bbox), 4, f"BBox for {code} should have 4 values")
                        minlat, maxlat, minlon, maxlon = bbox
                        self.assertIsInstance(minlat, (int, float))
                        self.assertIsInstance(maxlat, (int, float))
                        self.assertIsInstance(minlon, (int, float))
                        self.assertIsInstance(maxlon, (int, float))
                        self.assertTrue(-90 <= minlat <= 90)
                        self.assertTrue(-90 <= maxlat <= 90)
                        self.assertTrue(-180 <= minlon <= 180)
                        self.assertTrue(-180 <= maxlon <= 180)
                        self.assertLessEqual(minlat, maxlat)
                        self.assertLessEqual(minlon, maxlon)
                        
                        # Validate other attributes are None for newly fetched bounding_box-only data
                        cached_row = geo.geo_cache[geo.geo_cache['subdivisionCode'] == code]
                        if not cached_row.empty:
                            latlng_val = cached_row['latLng'].values[0]
                            geojson_val = cached_row['geojson'].values[0]
                            perimeter_val = cached_row['perimeter'].values[0]
                            neighbours_val = cached_row['neighbours'].values[0]
                            
                            # Check that other attributes are None or NaN (not yet fetched)
                            self.assertTrue(latlng_val is None or (isinstance(latlng_val, float) and pd.isna(latlng_val)),
                                          f"latLng for {code} should be None or NaN, got {latlng_val}")
                            self.assertTrue(geojson_val is None or (isinstance(geojson_val, float) and pd.isna(geojson_val)),
                                          f"geojson for {code} should be None or NaN, got {geojson_val}")
                            self.assertTrue(perimeter_val is None or (isinstance(perimeter_val, float) and pd.isna(perimeter_val)),
                                          f"perimeter for {code} should be None or NaN, got {perimeter_val}")
                            self.assertTrue(neighbours_val is None or (isinstance(neighbours_val, float) and pd.isna(neighbours_val)),
                                          f"neighbours for {code} should be None or NaN, got {neighbours_val}")
        
        # Test countries with no subdivisions return empty dict
        geo_bv = Geo("BV")
        bounding_boxes_bv = geo_bv.get_bounding_box(country_code="BV", verbose=False, export=False)
        self.assertEqual(bounding_boxes_bv, {})
        
        geo_cc = Geo("CC")
        bounding_boxes_cc = geo_cc.get_bounding_box(country_code="CC", verbose=False, export=False)
        self.assertEqual(bounding_boxes_cc, {})
    
        # Test error handling for invalid country codes
        with self.assertRaises(ValueError):
            self.geo.get_bounding_box("ABC", verbose=False, export=False)
        with self.assertRaises(ValueError):
            self.geo.get_bounding_box("123", verbose=False, export=False)

    # @unittest.skip("")
    def test_get_geojson_real_api_call(self):
        """ Test get_geojson with real API call making actual API requests. """
        # Test cases with country codes for real API calls
        test_countries = ['TM', 'TO', 'VC']
        
        for country_code in test_countries:
            with self.subTest(country_code=country_code):
                geo = Geo(country_code=country_code)
                geojsons = geo.get_geojson(country_code=country_code, verbose=False, export=False)
                
                # Validate return type
                self.assertIsInstance(geojsons, dict)
                self.assertGreater(len(geojsons), 0)
                
                # Validate all returned subdivision codes are valid for the country
                country_subdivision_codes = self.subd[country_code].subdivision_codes()
                geojsons_subdivision_codes = list(geojsons.keys())
                
                for code in geojsons_subdivision_codes:
                    self.assertIn(code, country_subdivision_codes,
                                 f"Invalid subdivision code '{code}' for country code '{country_code}'")
                
                # Validate geojson format and structure
                for code, geom in geojsons.items():
                    self.assertIsInstance(geom, dict)
                    self.assertEqual(geom['type'], 'FeatureCollection',
                                   f"GeoJSON for {code} must be a FeatureCollection")
                    self.assertIn('features', geom,
                                 f"GeoJSON for {code} must have 'features' key")
                    self.assertIsInstance(geom['features'], list)
                    
                    # Validate other attributes are None for newly fetched geojson-only data
                    cached_row = geo.geo_cache[geo.geo_cache['subdivisionCode'] == code]
                    if not cached_row.empty:
                        latlng_val = cached_row['latLng'].values[0]
                        bounded_box_val = cached_row['boundingBox'].values[0]
                        perimeter_val = cached_row['perimeter'].values[0]
                        neighbours_val = cached_row['neighbours'].values[0]
                        
                        # Check that other attributes are None or NaN (not yet fetched)
                        self.assertTrue(latlng_val is None or (isinstance(latlng_val, float) and pd.isna(latlng_val)),
                                      f"latLng for {code} should be None or NaN, got {latlng_val}")
                        self.assertTrue(bounded_box_val is None or (isinstance(bounded_box_val, float) and pd.isna(bounded_box_val)),
                                      f"boundingBox for {code} should be None or NaN, got {bounded_box_val}")
                        self.assertTrue(perimeter_val is None or (isinstance(perimeter_val, float) and pd.isna(perimeter_val)),
                                      f"perimeter for {code} should be None or NaN, got {perimeter_val}")
                        self.assertTrue(neighbours_val is None or (isinstance(neighbours_val, float) and pd.isna(neighbours_val)),
                                      f"neighbours for {code} should be None or NaN, got {neighbours_val}")
        
        # Test countries with no subdivisions return empty dict
        geo_bv = Geo("BV")
        geojsons_bv = geo_bv.get_geojson(country_code="BV", verbose=False, export=False)
        self.assertEqual(geojsons_bv, {})
        
        geo_fk = Geo("FK")
        geojsons_fk = geo_fk.get_geojson(country_code="FK", verbose=False, export=False)
        self.assertEqual(geojsons_fk, {})

        # Test error handling for invalid country codes
        with self.assertRaises(ValueError):
            geo = Geo("TM")
            geo.get_geojson("ABC", verbose=False, export=False)
        with self.assertRaises(ValueError):
            geo = Geo("TM")
            geo.get_geojson("123", verbose=False, export=False)
    
    # @unittest.skip("") 
    def test_get_perimeter_real_api_call(self):
        """ Test get_perimeter with real API call making actual API requests. """
#1.)    
        geo_at = Geo(country_code="AT")
        perimeters_at = geo_at.get_perimeter()

        # Validate all returned subdivision codes are valid for the country
        at_subdivision_codes = self.subd["AT"].subdivision_codes()
        perimeters_at_subdivision_codes = list(perimeters_at.keys())
        for code in at_subdivision_codes:
            self.assertIn(code, perimeters_at_subdivision_codes,
                         f"Invalid subdivision code '{code}' for country code 'AT'")
        
        # Validate perimeter values
        expected_perimeters_at = {'AT-1': 765.39, 'AT-2': 697.22, 'AT-3': 1046.33, 'AT-4': 898.06, 'AT-5': 781.75, 
                                  'AT-6': 945.65, 'AT-7': 1058.31, 'AT-8': 351.09, 'AT-9': 136.23}
        self.assertEqual(perimeters_at, expected_perimeters_at)
#2.)
        geo_er = Geo(country_code="ER")
        perimeters_er = geo_er.get_perimeter(country_code="ER", verbose=False, export=False)

        # Validate all returned subdivision codes are valid for the country
        er_subdivision_codes = self.subd["ER"].subdivision_codes()
        perimeters_er_subdivision_codes = list(perimeters_er.keys())
        for code in er_subdivision_codes:
            self.assertIn(code, perimeters_er_subdivision_codes,
                         f"Invalid subdivision code '{code}' for country code 'ER'")
        
        # Validate perimeter values
        expected_perimeters_er = {'ER-AN': 833.02, 'ER-DK': 1005.28, 'ER-DU': 602.29, 'ER-GB': 991.61, 'ER-MA': 193.91, 'ER-SK': 1347.7}
        self.assertEqual(perimeters_er, expected_perimeters_er)
#3.)
        geo_iq = Geo(country_code="IQ")
        perimeters_iq = geo_iq.get_perimeter()

        # Validate all returned subdivision codes are valid for the country
        iq_subdivision_codes = self.subd["IQ"].subdivision_codes()
        perimeters_iq_subdivision_codes = list(perimeters_iq.keys())
        for code in iq_subdivision_codes:
            self.assertIn(code, perimeters_iq_subdivision_codes,
                         f"Invalid subdivision code '{code}' for country code 'IQ'")
        
        print("obs")
        print(perimeters_iq)
        # Validate perimeter values
        expected_perimeters_iq = {'IQ-AN': 1827.63, 'IQ-AR': 913.74, 'IQ-BA': 1003.57, 'IQ-BB': 404.19, 'IQ-BG': 508.98, 
                                  'IQ-DA': 566.82, 'IQ-DI': 1072.24, 'IQ-DQ': 579.26, 'IQ-KA': 297.97, 'IQ-KI': 551.5, 
                                  'IQ-KR': 2026.47, 'IQ-MA': 625.98, 'IQ-MU': 1023.65, 'IQ-NA': 824.37, 'IQ-NI': 1251.37, 
                                  'IQ-QA': 500.49, 'IQ-SD': 1059.67, 'IQ-SU': 1061.93, 'IQ-WA': 730.19}
        self.assertEqual(perimeters_iq, expected_perimeters_iq)
#4.)
        # Validate other attributes are None for newly fetched perimeter-only data for all three countries
        for geo in [geo_at, geo_er, geo_iq]:
            # Iterate over entire cache and validate rows with perimeter values
            for idx, row in geo.geo_cache.iterrows():
                # Only validate rows that have a perimeter value
                if row['perimeter'] is not None and not (isinstance(row['perimeter'], float) and pd.isna(row['perimeter'])):
                    code = row['subdivisionCode']
                    latlng_val = row['latLng']
                    bounded_box_val = row['boundingBox']
                    geojson_val = row['geojson']
                    neighbours_val = row['neighbours']
                    
                    # Check that other attributes are None or NaN (not yet fetched)
                    self.assertTrue(latlng_val is None or (isinstance(latlng_val, float) and pd.isna(latlng_val)),
                                  f"latLng for {code} should be None or NaN, got {latlng_val}")
                    self.assertTrue(bounded_box_val is None or (isinstance(bounded_box_val, float) and pd.isna(bounded_box_val)),
                                  f"boundingBox for {code} should be None or NaN, got {bounded_box_val}")
                    self.assertTrue(geojson_val is None or (isinstance(geojson_val, float) and pd.isna(geojson_val)),
                                  f"geojson for {code} should be None or NaN, got {geojson_val}")
                    self.assertTrue(neighbours_val is None or (isinstance(neighbours_val, float) and pd.isna(neighbours_val)),
                                  f"neighbours for {code} should be None or NaN, got {neighbours_val}")
#5.)
        # Test countries with no subdivisions return empty dict
        perimeters_hk = Geo('HK').get_perimeter(country_code="HK", verbose=False, export=False)
        self.assertEqual(perimeters_hk, {})
        perimeters_mp = Geo("MP").get_perimeter(country_code="MP", verbose=False, export=False)
        self.assertEqual(perimeters_mp, {})
#6.)
        # Test error handling for invalid country codes
        with self.assertRaises(ValueError):
            geo = Geo()
            geo.get_perimeter("ABC", verbose=False, export=False)
        with self.assertRaises(ValueError):
            geo = Geo()
            geo.get_perimeter("123", verbose=False, export=False)

    # @unittest.skip("")
    def test_get_neighbours_real_api_call(self):
        """ Test get_neighbours with real API call making actual API requests. """
#1.)
        geo_be = Geo(country_code="BE")
        neighbours_be = geo_be.get_neighbours()

        # Validate all returned subdivision codes are valid for the country
        be_subdivision_codes = self.subd["BE"].subdivision_codes()
        neighbours_be_subdivision_codes = list(neighbours_be.keys())
        for code in neighbours_be_subdivision_codes:
            self.assertIn(code, be_subdivision_codes,
                         f"Invalid subdivision code '{code}' for country code 'BE'")
        
        # Validate neighbours format and values
        for code, neighbour_list in neighbours_be.items():
            self.assertIsInstance(neighbour_list, list)
            for neighbour_code in neighbour_list:
                self.assertIsInstance(neighbour_code, str)
                self.assertIn(neighbour_code, be_subdivision_codes,
                             f"Invalid neighbour code '{neighbour_code}' for {code} in country 'BE'")
#2.)
        geo_za = Geo(country_code="ZA")
        neighbours_za = geo_za.get_neighbours(country_code="ZA", verbose=False, export=False)

        # Validate all returned subdivision codes are valid for the country
        za_subdivision_codes = self.subd["ZA"].subdivision_codes()
        neighbours_za_subdivision_codes = list(neighbours_za.keys())
        for code in za_subdivision_codes:
            self.assertIn(code, neighbours_za_subdivision_codes,
                         f"Invalid subdivision code '{code}' for country code 'ZA'")
        
        # Validate neighbours format and values
        for code, neighbour_list in neighbours_za.items():
            self.assertIsInstance(neighbour_list, list)
            for neighbour_code in neighbour_list:
                self.assertIsInstance(neighbour_code, str)
                self.assertIn(neighbour_code, za_subdivision_codes,
                             f"Invalid neighbour code '{neighbour_code}' for {code} in country 'ZA'")
#3.)
        geo_in = Geo(country_code="IN")
        neighbours_in = geo_in.get_neighbours()

        # Validate all returned subdivision codes are valid for the country
        in_subdivision_codes = self.subd["IN"].subdivision_codes()
        neighbours_in_subdivision_codes = list(neighbours_in.keys())
        for code in neighbours_in_subdivision_codes:
            self.assertIn(code, in_subdivision_codes,
                         f"Invalid subdivision code '{code}' for country code 'IN'")
        
        # Validate neighbours format and values
        for code, neighbour_list in neighbours_in.items():
            self.assertIsInstance(neighbour_list, list)
            for neighbour_code in neighbour_list:
                self.assertIsInstance(neighbour_code, str)
                self.assertIn(neighbour_code, in_subdivision_codes,
                             f"Invalid neighbour code '{neighbour_code}' for {code} in country 'IN'")

#4.)
        # Validate other attributes are None for newly fetched neighbours-only data for all three countries
        for geo in [geo_be, geo_za, geo_in]:
            # Iterate over entire cache and validate rows with neighbours values
            for idx, row in geo.geo_cache.iterrows():
                # Only validate rows that have a neighbours value
                if row['neighbours'] is not None and not (isinstance(row['neighbours'], float) and pd.isna(row['neighbours'])):
                    code = row['subdivisionCode']
                    latlng_val = row['latLng']
                    bounded_box_val = row['boundingBox']
                    geojson_val = row['geojson']
                    perimeter_val = row['perimeter']
                    
                    # Check that other attributes are None or NaN (not yet fetched)
                    self.assertTrue(latlng_val is None or (isinstance(latlng_val, float) and pd.isna(latlng_val)),
                                  f"latLng for {code} should be None or NaN, got {latlng_val}")
                    self.assertTrue(geojson_val is None or (isinstance(geojson_val, float) and pd.isna(geojson_val)),
                                  f"geojson for {code} should be None or NaN, got {geojson_val}")
                    self.assertTrue(perimeter_val is None or (isinstance(perimeter_val, float) and pd.isna(perimeter_val)),
                                  f"perimeter for {code} should be None or NaN, got {perimeter_val}")
#5.)
        # Test countries with no subdivisions return empty dict
        neighbours_bv = Geo("GF").get_neighbours(country_code="GF", verbose=False, export=False)
        self.assertEqual(neighbours_bv, {})
        neighbours_tk = Geo("TK").get_neighbours(country_code="TK", verbose=False, export=False)
        self.assertEqual(neighbours_tk, {})
#6.)
        # Test error handling for invalid country codes
        with self.assertRaises(ValueError):
            geo = Geo().get_neighbours("ABC", verbose=False, export=False)
        with self.assertRaises(ValueError):
            geo = Geo().get_neighbours("123", verbose=False, export=False)

    # @unittest.skip("")
    def test_get_all_real_api_call(self):
        """ Test get_all with real API call. Skipping geojson retrieval for brevity. """
#1.)
        geo_om = Geo(country_code="OM")
        all_data_om = geo_om.get_all(verbose=False, export=False, skip_geojson=True)

        geo_mx = Geo(country_code="MX")
        all_data_mx = geo_mx.get_all(country_code="MX", verbose=False, export=False, skip_geojson=True)

        geo_ca = Geo(country_code="CA")
        all_data_ca = geo_ca.get_all(country_code="CA", verbose=False, export=False, skip_geojson=True)

        for country_code, all_data in [("OM", all_data_om), ("MX", all_data_mx), ("CA", all_data_ca)]:
            # Validate return type
            self.assertIsInstance(all_data, dict, f"Data for {country_code} should be dict")
            
            # Validate structure of returned data - should have all attributes
            for code, data_dict in all_data.items():
                self.assertIsInstance(data_dict, dict)
                self.assertIn('latLng', data_dict)
                self.assertIn('bounding_box', data_dict)
                self.assertIn('perimeter', data_dict)
                self.assertIn('neighbours', data_dict)
            
            # Validate latLng format and values
            for code, data_dict in all_data.items():
                latlng = data_dict['latLng']
                self.assertIsInstance(latlng, str, f"latLng for {code} should be string")
                parts = latlng.split(',')
                self.assertEqual(len(parts), 2, f"latLng for {code} should be 'lat,lon' format")
                lat, lng = float(parts[0]), float(parts[1])
                self.assertTrue(-90 <= lat <= 90, f"Latitude {lat} for {code} out of range")
                self.assertTrue(-180 <= lng <= 180, f"Longitude {lng} for {code} out of range")
            
            # Validate bounding box format and logic
            for code, data_dict in all_data.items():
                bbox = data_dict['bounding_box']
                self.assertIsInstance(bbox, list, f"bounding_box for {code} should be list")
                self.assertEqual(len(bbox), 4, f"bounding_box for {code} should have 4 values")
                minlat, maxlat, minlon, maxlon = bbox
                self.assertIsInstance(minlat, (int, float))
                self.assertIsInstance(maxlat, (int, float))
                self.assertIsInstance(minlon, (int, float))
                self.assertIsInstance(maxlon, (int, float))
                self.assertLessEqual(minlat, maxlat, f"minlat should be <= maxlat for {code}")
                self.assertLessEqual(minlon, maxlon, f"minlon should be <= maxlon for {code}")
            
            # Validate perimeter is positive float
            for code, data_dict in all_data.items():
                perimeter = data_dict['perimeter']
                self.assertIsInstance(perimeter, (int, float), f"perimeter for {code} should be numeric")
                self.assertGreater(perimeter, 0, f"perimeter for {code} should be positive")
            
            # Validate neighbours are valid codes and relationships are reciprocal
            for code, data_dict in all_data.items():
                neighbours = data_dict['neighbours']
                self.assertIsInstance(neighbours, list, f"neighbours for {code} should be list")
                for neighbour_code in neighbours:
                    self.assertIsInstance(neighbour_code, str)
                    self.assertIn(neighbour_code, all_data, 
                                 f"neighbour {neighbour_code} for {code} not found in returned data")
                    # Check reciprocal relationship
                    self.assertIn(code, all_data[neighbour_code]['neighbours'],
                                 f"{code} is neighbour of {neighbour_code} but not vice versa")
#5.)
        # Test countries with no subdivisions return empty dict
        all_data_nu = Geo("NU").get_all(country_code="NU", verbose=False, export=False, skip_geojson=True)
        self.assertEqual(all_data_nu, {})
        all_data_re = Geo("RE").get_all(country_code="RE", verbose=False, export=False, skip_geojson=True)
        self.assertEqual(all_data_re, {})
#6.)
        # Test error handling for invalid country codes
        with self.assertRaises(ValueError):
            geo = Geo()
            geo.get_all("ABC", verbose=False, export=False, skip_geojson=True)
        with self.assertRaises(ValueError):
            geo = Geo()
            geo.get_all("123", verbose=False, export=False, skip_geojson=True)

    # @unittest.skip("")
    # def test_fetch_all_country_geo_data(self):
    #     """ Test fetch_all_country_geo_data function with real API calls. """
    # pass

    def tearDown(self):
        """ Clean up test fixtures. """
        self.print_patcher.stop()

# Run the tests
if __name__ == '__main__':
    unittest.main(verbosity=2)