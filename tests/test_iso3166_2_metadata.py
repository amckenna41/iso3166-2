from scripts.export_iso3166_2_metadata import export_iso3166_2_metadata
import os
import shutil
import json
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

# @unittest.skip("")
class ISO3166_2_Metadata_Tests(unittest.TestCase):
    """
    Test suite for testing the export_iso3166_2_metadata.py script
    that exports useful metadata/stats about the iso3166-2 dataset.

    Test Cases
    ==========
    test_iso3166_2_metadata:
        testing correct stats & metadata for the iso3166-2 repo/dataset.
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
    def test_iso3166_2_metadata(self):
        """ Test correct stats & metadata for the iso3166-2 repo/dataset. """
        
        #export metadata
        export_iso3166_2_metadata(self.iso3166_2_filepath, export_filename=self.iso3166_2_metadata_export)

        #import exported metadata
        with open(self.iso3166_2_metadata_export, "r", encoding="utf-8") as f:
            test_metadata = json.load(f)

        #check metadata values
        self.assertEqual(test_metadata["total_countries"], 250)
        self.assertEqual(test_metadata["total_subdivisions"], 5049)
        self.assertEqual(test_metadata["dataset_kb"], 2845.956)
        self.assertEqual(test_metadata["dataset_mb"], 2.779)
        self.assertEqual(test_metadata["total_attributes"], 35343)
        self.assertEqual(test_metadata["num_unique_attributes"], 7)
        self.assertEqual(test_metadata["unique_subdivision_types"], 112)
        self.assertEqual(test_metadata["average_subdivision_per_country"], 20.196)
        self.assertEqual(test_metadata["zero_subdivisions_total"], 50)
        self.assertEqual(test_metadata["max_subdivisions_country"], "GB:224")
        self.assertEqual(test_metadata["null_attributes_total"], 10741)
        self.assertEqual(test_metadata["null_local_other_name_total"], 1312)
        self.assertEqual(test_metadata["null_flag_total"], 2205)
        self.assertEqual(test_metadata["null_type_total"], 0)
        self.assertEqual(test_metadata["null_latlng_total"], 0)
        self.assertEqual(test_metadata["null_latlng_total"], 0)
        self.assertEqual(test_metadata["null_parentcode_total"], 3593)
        self.assertEqual(test_metadata["null_history_total"], 3631)
        self.assertEqual(test_metadata["total_local_other_entries"], 8275)
        self.assertEqual(test_metadata["hemisphere_north_total"], 4381)
        self.assertEqual(test_metadata["hemisphere_south_total"], 668)
        self.assertEqual(test_metadata["hemisphere_east_total"], 3646)
        self.assertEqual(test_metadata["hemisphere_west_total"], 1403)

    @classmethod
    def tearDown(self):
        """ Delete any temp export folder. """
        shutil.rmtree(self.test_output_dir)

if __name__ == '__main__':  
    #run all unit tests
    unittest.main(verbosity=2)    