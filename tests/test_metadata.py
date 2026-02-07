from scripts.metadata import export_metadata
import os
import shutil
import json
import unittest
from jsonschema import validate, ValidationError
unittest.TestLoader.sortTestMethodsUsing = None

# @unittest.skip("")
class ISO3166_2_Metadata_Tests(unittest.TestCase):
    """
    Test suite for testing the export_metadata.py script
    that exports useful metadata/stats about the iso3166-2 dataset.

    Test Cases
    ==========
    test_iso3166_2_metadata_export:
        Testing correct stats & metadata for the iso3166-2 repo/dataset.
    test_invalid_filepath:
        Testing handling of invalid ISO 3166-2 filepath.
    test_export_metadata_with_timestamp:
        Testing export_metadata with append_timestamp=True.
    test_metadata_json_schema:
        Testing that metadata JSON adheres to the expected schema.
    """
    @classmethod
    def setUp(self):
        """ Initialise test variables, import json. """
        self.test_output_dir = os.path.join("tests", "test_output_dir")
        self.iso3166_2_filepath = os.path.join("tests", "test_files", "test_iso3166-2.json")
        self.iso3166_2_metadata_export = os.path.join("tests", "test_output_dir", "test_iso3166-2-metadata.json")
        
        #create output dir if not already present
        if not (os.path.isdir(self.test_output_dir)):
            os.makedirs(self.test_output_dir)

    # @unittest.skip("")
    def test_iso3166_2_metadata_export(self):
        """ Test correct stats & metadata for the iso3166-2 repo/dataset. """
        
        #export metadata
        export_metadata(self.iso3166_2_filepath, export_filename=self.iso3166_2_metadata_export)

        #import exported metadata
        with open(self.iso3166_2_metadata_export, "r", encoding="utf-8") as f:
            test_metadata = json.load(f)

        #check metadata values
        self.assertEqual(test_metadata["total_countries"], 249)
        self.assertEqual(test_metadata["total_subdivisions"], 5046)
        self.assertEqual(test_metadata["dataset_kb"], 3482.215)
        self.assertEqual(test_metadata["dataset_mb"], 3.401)
        self.assertEqual(test_metadata["total_attributes"], 35322)
        self.assertEqual(test_metadata["num_unique_attributes"], 7)
        self.assertEqual(test_metadata["unique_subdivision_types"], 110)
        self.assertEqual(test_metadata["average_subdivision_per_country"], 20.265)
        self.assertEqual(test_metadata["zero_subdivisions_total"], 49)
        self.assertEqual(test_metadata["max_subdivisions_country"], "GB:221")
        self.assertEqual(test_metadata["min_subdivisions_country"], "AI,AQ,AS,AW,AX,BL,BM,BV,CC,CK,CW,CX,EH,FK,FO,GF,GG,GI,GP,GS,GU,HK,HM,IM,IO,JE,KY,MF,MO,MP,MQ,MS,NC,NF,NU,PF,PM,PN,PR,RE,SJ,SX,TC,TF,TK,VA,VG,VI,YT:0")
        self.assertEqual(test_metadata["null_attributes_total"], 10735)
        self.assertEqual(test_metadata["hemisphere_north_total"], 4371)
        self.assertEqual(test_metadata["hemisphere_south_total"], 675)
        self.assertEqual(test_metadata["hemisphere_east_total"], 3632)
        self.assertEqual(test_metadata["hemisphere_west_total"], 1414)
        
        #check attribute_stats for 'name' attribute
        self.assertIn("attribute_stats", test_metadata)
        self.assertIsInstance(test_metadata["attribute_stats"], dict)
        name_stats = test_metadata["attribute_stats"]["name"]
        self.assertEqual(name_stats["total_count"], 5046)
        self.assertEqual(name_stats["null_count"], 0)
        self.assertEqual(name_stats["populated_count"], 5046)
        self.assertEqual(name_stats["completeness_percent"], 100.0)
        
        #check attribute_stats for 'localOtherName' attribute
        local_other_stats = test_metadata["attribute_stats"]["localOtherName"]
        self.assertEqual(local_other_stats["total_count"], 5046)
        self.assertEqual(local_other_stats["null_count"], 1312)
        self.assertEqual(local_other_stats["populated_count"], 3734)
        self.assertEqual(local_other_stats["completeness_percent"], 74.0)
        self.assertEqual(local_other_stats["total_individual_count"], 8270)

        #check attribute_stats for 'flag' attribute
        flag_stats = test_metadata["attribute_stats"]["flag"]
        self.assertEqual(flag_stats["total_count"], 5046)
        self.assertEqual(flag_stats["null_count"], 2203)
        self.assertEqual(flag_stats["populated_count"], 2843)
        self.assertEqual(flag_stats["completeness_percent"], 56.34)
        
        #check attribute_stats for 'type' attribute
        type_stats = test_metadata["attribute_stats"]["type"]
        self.assertEqual(type_stats["total_count"], 5046)
        self.assertEqual(type_stats["null_count"], 0)
        self.assertEqual(type_stats["populated_count"], 5046)
        self.assertEqual(type_stats["completeness_percent"], 100.0)
        
        #check attribute_stats for 'latLng' attribute
        latlng_stats = test_metadata["attribute_stats"]["latLng"]
        self.assertEqual(latlng_stats["total_count"], 5046)
        self.assertEqual(latlng_stats["null_count"], 0)
        self.assertEqual(latlng_stats["populated_count"], 5046)
        self.assertEqual(latlng_stats["completeness_percent"], 100.0)
        
        #check attribute_stats for 'parentCode' attribute
        parent_code_stats = test_metadata["attribute_stats"]["parentCode"]
        self.assertEqual(parent_code_stats["total_count"], 5046)
        self.assertEqual(parent_code_stats["null_count"], 3590)
        self.assertEqual(parent_code_stats["populated_count"], 1456)
        self.assertEqual(parent_code_stats["completeness_percent"], 28.85)
        
        #check attribute_stats for 'history' attribute
        history_stats = test_metadata["attribute_stats"]["history"]
        self.assertEqual(history_stats["total_count"], 5046)
        self.assertEqual(history_stats["null_count"], 3630)
        self.assertEqual(history_stats["populated_count"], 1416)
        self.assertEqual(history_stats["completeness_percent"], 28.06)

    def test_invalid_filepath(self):
        """ Test handling of invalid ISO 3166-2 filepath. """
        invalid_filepath = os.path.join("tests", "test_files", "non_existent_file.json")
        with self.assertRaises(FileNotFoundError):
            export_metadata(invalid_filepath, export_filename=self.iso3166_2_metadata_export)
    
    def test_export_metadata_with_timestamp(self):
        """ Test export_metadata with append_timestamp=True. """
        export_metadata(self.iso3166_2_filepath, export_filename=self.iso3166_2_metadata_export, append_timestamp=True)
        
        #check if file with timestamp exists
        base_filename = os.path.splitext(self.iso3166_2_metadata_export)[0]
        found_file = False
        for filename in os.listdir(self.test_output_dir):
            if filename.startswith(os.path.basename(base_filename)) and filename.endswith(".json"):
                found_file = True
                break
        self.assertTrue(found_file, "Exported metadata file with timestamp not found.")

    # @unittest.skip("")
    def test_metadata_json_schema(self):
        """ Test that metadata JSON adheres to the expected schema. """
        #export metadata
        export_metadata(self.iso3166_2_filepath, export_filename=self.iso3166_2_metadata_export)

        #import exported metadata
        with open(self.iso3166_2_metadata_export, "r", encoding="utf-8") as f:
            test_metadata = json.load(f)

        #define the metadata schema
        schema = {
            "type": "object",
            "properties": {
                "total_countries": {"type": "integer", "minimum": 0},
                "total_subdivisions": {"type": "integer", "minimum": 0},
                "dataset_kb": {"type": "number", "minimum": 0},
                "dataset_mb": {"type": "number", "minimum": 0},
                "total_attributes": {"type": "integer", "minimum": 0},
                "num_unique_attributes": {"type": "integer", "minimum": 0},
                "unique_subdivision_types": {"type": "integer", "minimum": 0},
                "average_subdivision_per_country": {"type": "number", "minimum": 0},
                "zero_subdivisions_total": {"type": "integer", "minimum": 0},
                "max_subdivisions_country": {"type": "string"},
                "min_subdivisions_country": {"type": "string"},
                "null_attributes_total": {"type": "integer", "minimum": 0},
                "hemisphere_north_total": {"type": "integer", "minimum": 0},
                "hemisphere_south_total": {"type": "integer", "minimum": 0},
                "hemisphere_east_total": {"type": "integer", "minimum": 0},
                "hemisphere_west_total": {"type": "integer", "minimum": 0},
                "attribute_stats": {
                    "type": "object",
                    "patternProperties": {
                        ".*": {
                            "type": "object",
                            "properties": {
                                "total_count": {"type": "integer", "minimum": 0},
                                "null_count": {"type": "integer", "minimum": 0},
                                "populated_count": {"type": "integer", "minimum": 0},
                                "completeness_percent": {"type": "number", "minimum": 0, "maximum": 100},
                                "total_individual_count": {"type": "integer", "minimum": 0}
                            },
                            "required": ["total_count", "null_count", "populated_count", "completeness_percent"],
                            "additionalProperties": False
                        }
                    },
                    "additionalProperties": False
                }
            },
            "required": [
                "total_countries", "total_subdivisions", "dataset_kb", "dataset_mb",
                "total_attributes", "num_unique_attributes", "unique_subdivision_types",
                "average_subdivision_per_country", "zero_subdivisions_total",
                "max_subdivisions_country", "min_subdivisions_country", "null_attributes_total",
                "hemisphere_north_total", "hemisphere_south_total", "hemisphere_east_total",
                "hemisphere_west_total", "attribute_stats"
            ],
            "additionalProperties": False
        }

        #validate metadata against schema
        try:
            validate(instance=test_metadata, schema=schema)
        except ValidationError as e:
            self.fail(f"Metadata JSON schema validation failed: {e.message}.")

    @classmethod
    def tearDown(self):
        """ Delete any temp export folder. """
        shutil.rmtree(self.test_output_dir)

if __name__ == '__main__':  
    #run all unit tests
    unittest.main(verbosity=2)    