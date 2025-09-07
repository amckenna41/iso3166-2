# iso3166-2 Tests 🧪 <a name="TOP"></a>

All of the modules and functionalities of `iso3166-2` are thoroughly tested using the Python [unittest][unittest] framework. Currently there are 7 test cases with X unit tests functions made up of several unit tests.

## Module tests:

* `test_iso3166_2` - unit tests for `iso3166-2` package.
* `test_export_iso3166_2` - unit tests for `export_iso3166_2.py` script that pulls the ISO 3166-2 subdivision data from the data sources.
* `test_update_subdivisions` - unit tests for `update_subdivisions.py` script that is used for the streamlining of subdivision additions, changes or deletions to the ISO 3166-2 data object.
* `test_local_other_names` - unit tests for 
* `test_language_lookup` - unit tests for Language Lookup class which encapsulates all the language codes from the local/other names csv.
* `test_utils` - unit tests for `utils.py` module that has a series of utily functions used throughout project.
* `test_iso3166_2_api` - unit tests for `iso3166-2` API, hosted on Vercel.

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