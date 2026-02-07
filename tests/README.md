# iso3166-2 Tests 🧪 <a name="TOP"></a>

All of the modules and functionalities of `iso3166-2` are thoroughly tested using the Python [unittest][unittest] framework. Currently there are 12 test cases made up of several unit tests.

## Module tests:

* `test_iso3166_2` - unit tests for `iso3166-2` package.
* `test_main` - unit tests for `main.py` script that pulls the ISO 3166-2 subdivision data from the data sources.
* `test_update_subdivisions` - unit tests for `update_subdivisions.py` script that is used for the streamlining of subdivision additions, changes or deletions to the ISO 3166-2 data object.
* `test_local_other_names` - unit tests for 
* `test_language_lookup` - unit tests for Language Lookup class which encapsulates all the language codes from the local/other names csv.
* `test_utils` - unit tests for `utils.py` module that has a series of utils functions used throughout project.
* `test_geo` - unit tests for `geo.py` script that exports any of the geographical data for the subdivisions.
* `test_iso3166_2_api` - unit tests for `iso3166-2` API, hosted on Vercel.
* `test_metadata` - unit tests for `metadata.py` script that exports the metadata for the software & dataset.
* `test_history` - unit tests for `history.py` script that exports the historical data per subdivision, if applicable 
* `test_restcountries_api` - unit tests for `restcountries_api.py` script that exports the country-level data via the RestCountries API, if applicable

## Running Tests

Prior to running any of the tests, ensure you have the required packages installed, all the packages can be downloaded via the requirements.txt
```bash
pip install -r tests/requirements.txt
```

To run all unittests, make sure you are in the main `iso3166-2` directory and from a terminal/cmd-line run:
```bash
python -m unittest discover tests -v
#-v produces a more verbose and useful output
```

To run a specific unit test, make sure you are in the main `iso3166-2` directory and from a terminal/cmd-line run:
```bash
python -m unittest discover tests.test_iso3166_2 -v
#-v produces a more verbose and useful output
```

[unittest]: https://docs.python.org/3/library/unittest.html