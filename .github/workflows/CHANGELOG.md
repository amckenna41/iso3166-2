# Change Log 🔄

## v1.8.1 - February 2026

### Added
- Updated accuracy of all latLng attributes for all subdivisions, using the centroid of the subdivision as the new value
- Added logo to the main readme
- Added /spec & /openapi.yml endpoints on API, added unit tests
- Added /random endpoint on API that returns a random subdivision from the >5000 available, added unit tests
- Added additional unit and integration tests for each module
- Added a output message in the custom_subdivision when adding one to ensure the user keeps track of the new subdivision accurately
- Created new history module, separating the iso3166-updates history functionalities into separate module - added unit tests
- Added remove_attribute function within main iso3166-2.py module, it allows for you to remove from memory and from the dataset any unneeded attributes, saving a load of memory
- For some of the modules in /scripts that require an API key, this key can also be put into a .env file that the module can look for
- Added additional and more informative type hints to some of the functions
- Added anomaly detection function that uses openai api to generate a CSV that outputs any anomalies or errors found in the iso3166-2.json object 
- Added integration tests that validate that each latLng value for each subdivision falls within the boundary of the country
- Added Geo module used for getting everything latLng related per subdivision including centroid, bounding box and the relevant API calls
- For the Geo module, created a cache file (iso3166_2_resources/geo_cache.csv) that stores all of the exported geographical related data per subdivision that is imported during execution, rather than having to make API calls each time
- Added additional info to the __repr__ and __str__ functions in iso3166_2
- Added wikidata package to /scripts dependencies 
- Added individual Subdivision data class to iso3166_2 package 
- Added self.alpha2 attribute in iso3166-2 package that lists the ISO 3166-1 country codes

### Changed
- Implemented more accurate method of getting lat/long via openstreetmap instead of Google Maps API
- Split several of the export functionalities in /scripts into their own modules for readability and extensibility
- In many of the test modules, split up the test class functions into integration and unit tests
- Updated history attribute within each subdivision such that it displays the history object as is in the iso3166-updates software 
- Removed the extract_lat_lng parameter - since we're using the OSM to get the 
- When exporting the data via the export pipeline. If save_each_iteration is set to True, only the JSON of the data will be exported, not the XML and CSV as well
- Updated github workflow, including adding concurrency and caching
- Changed any references to the python-iso3166 software to pycountry, as pycountry is more updated and maintained
- Removed GB-EAW GB-GBN and GB-UKM from dataset, these were previously included as they were in the remark section of GB's ISO page but not included in other ISO 3166 lists
- In main export function, removed skip latLng functionality that skips the exporting of the latLng attribute - the attribute data is now cached in a separate file so no need to be skipped

### Fixed
- Fixed accuracy of some of the latLng attribute values for some subdivisions, using the OSM as a data source rather than the previous Google Maps API 


## v1.8.0 - September 2025

### Added

- Added new file saving functionality for custom_subdivisions function
- Added API tests to /tests dir
- Added Vercel webhook to the workflow, this redeploys the API vercel app once new version of the software released from this repo
- In script dir added a metadata script that exports a plethora of useful metadata about the software and data object
- Added functionality to the iso3166-2 main software such that the subdivision_codes() and subdivision_names() functions can be called through the subscripted country code object
- Added optional 'archive' parameter to update_subdivisions() function that can be set to True/False and will archive the existing iso3166-2 object before any changes are made
- Added CSV and XML of iso3166-2 dataset to iso3166_2_resources dir on repo
- When exporting the individual data to JSON, CSV and XML, in the function you can now import an already exported JSON file to just export the CSV and XML files
- Created function that allows you to combines multiple exports into one file, use case is for when alpha_codes_range was used to export a batch of export data and you need to combine into one master file
- Added unit test that checks that each flag url is valid
- When exporting the ISO 3166-2 data, setting rest_countries_keys=* will export all of them

### Changed

- Updated MANIFEST.in file to align with updated project structure
- Fixed deprecated upload-artefact error in github workflow
- Main export function name changed in get_iso3166_2 as it was very similar to the export data function in utils
- Removed filter_attributes functionality from utils export function
- Updated all references of iso3166-flag-icons to iso3166-flags to reflect updated repository name - including for each individual flag url in object
- Removed filter_attributes functionality from update_subdivisions function
- Changed export script name from get_iso3166_2 to export_iso3166_2
- Removed any additional flags from the iso3166-1-flags dataset that aren't strictly in the ISO 3166-1, including eu, arab league, UN and XX flags
- Updated the workflow such that unit tests for specific modules are only run when changes are made to those modules rather than all tests being run. If workflow dispatch is set then all tests will be run
- Switched from using unittest framework to pytest as the tests were being run twice

### Fixed

- RestCountries keys error fixed where the keys were getting added to the same column in the csv output
- Fixed column export for csv
- Ensured all empty attributes "" are converted to null 
- Several subdivision names and local/other names still contained * the † in them 
- requests dependency missing in pyproject
- Fixed small vulnerability with try/except in metadata export module
- Fixed the bandit & package calls in workflow, passing in specific directories 

## v1.7.0 - 1.7.2 - July 2025

### Added
- Add list of cities for each subdivision using the country-states-city API
- Added __version__ attribute to Subdivisions() class
- Local names attribute added with up-to-date accurate names
- For each subdivision's local name in the localName attribute, if the attribute isn't null then add the ISO 639 language code in brackets after the value. If there are multiple local names, separate via comma 
- Function added to ISO3166_2() class that checks for the latest version of the ISO3166-2 object, returning the differences of the current version
- When adding a custom subdivision via its respective function, user can also add custom attributes to it e.g population, area etc
- In Subdivisions class, you can now create an instance of the class but exclude some of the default attributes returned per subdivisions
- Added unit tests, docs updates and examples in readme's about accessing multiple country's subdivision data via an instance of the object directly
- For the localOtherName attribute, for non-latin alphabet subdivision, added the phonetic transcriptions e.g for Chinese subdivisions, Pinyin chinese is included for each subdivision 
- Added filter query string parameter to API, allowing for specific attributes for the subdivisions to be filtered in the API GET request e.g "?filter=name,type" etc
- Added filter parameter to search function in software, allowing you to search for a subdivision, returning only a subset of desired attributes
- Added new unit tests for the filter query string parameter
- In add_local_names function, new parameter called remove_duplicate_translations added. When set to 1, any values in localOtherName column that match the same official subdivision name in the name column, remove the specific local/other name. For example, CG-7: official name in French is Likouala which is the same as it is translated in English, DO-38: official name in Spanish is Enriquillo which is similar to its English translation Enriquillo
- When importing the local names csv, an error is raised if no language code is specified for the local/other name
- Additional unit tests added for new local/other name functionality including tests that validate the language code
- In get script, prior to exporting a message is printed out which includes all the attributes to be exported
- Added parameter to local names function where you can limit the number of local/other names per subdivision attribute. This is useful for some subdivisions's which have up to 6 or 7 translations/local variants etc
- Added additional unit tests for subdivision_updates.csv
- Added extra validation on subdivision_updates.csv, ensuring alpha codes, subdivision codes and date format are the valid format etc
- The search functionality in the Python package now allows you to include a subset of subdivision attributes via the filter_attributes function parameter
- The search functionality in the Python package now allows you to search via the localOtherName attribute as well as the default name attribute. By default only the name attribute is searched over
- Language lookup custom script which creates a Language class and generates an output file of each language used in the local/other names file, including its code and name
- Language lookup csv which is a custom exported file of language codes and their associated names
- Unit tests for language lookup functionality 
- Added utilities module which contains several functions that are used across the project, rather than replicating the functions in multiple modules
- requirements.txt added to scripts directory to outline the full list of packages for export pipeline
- Add __str__ and __repr__ functions to language lookup class in export pipeline, added relevant unit tests
- Added get_alpha_codes_list & export_iso3166_2_data utility functions, cleaning up the main function - relevant unit tests added to test_utils
- Added patching to unit tests such that system outputs/print statements are not displayed from modules when running tests
- Added delete language object functionality to language lookup table
- Added user agent functionality to language lookup script
- In language lookup export function, you can now put in custom language code to export 
- In update_subdivisions module and function, you can now add custom attributes to a subdivision via the custom_attributes parameter
- Added logic to ensure the custom order of attributes in exported iso3166-2 object is maintained 
- In extract script, optional proxy functionality added to requests.get functions to help avoid 429 errors and timeout errors
- In custom subdivision function is sw, you can now pass in an object of updates attributes
- Added exclude_match_score attribute to search function that allows you to include/exclude the % match the subdivision names are to the input search terms


### Fixed
- In convert_to_alpha2 function that converts a alpha-3 or numeric code into alpha-2, if a alpha-2 code was input it returns None instead of the same input alpha-2
- Some spanish subdivision names had a "*" at the end of their name e.g ES-A, ES-NA, which has now been removed
- For filter query string param, passing in no value to it would throw an error, now it just returns all data as is
- Updated all 2 letter ISO 639 language codes in local/other names csv into their ISO 639-2/3 counterparts
- When including historical updates data when exporting for each subdivision in the get_script, the language codes within the localOtherName column are removed
- Fixed error where only the first local/other name for a specific row is being imported
- Convert to alpha_2 code function changed such that if an invalid code is input it is returned from the function and an error raised instead of just returning None/null
- In custom_subdivision function, the original subdivision data/JSON was being reimported. Now the main self.all attribute is used
- Several rows (adds, amends, deletes) removed from subdivision_updates.csv as they are implemented in base object now
- Error with None values in subdivision_updates.csv not being interpreted as None
- Fixed error with adding rest country data to subdivisions 

### Changed
- Class name of software changed from ISO3166_2() to Subdivisions()
- In get script, changed alpha_codes_from parameter to alpha_codes_from_to, allowing you to get the ISO 3166-2 data between two alpha codes inclusive. Previously, you would just input a single alpha code and get the data from it alphabetically
- In CSV with each subdivision's local name (iso3166_2_updates/local_names.csv), the localName column has been changed to localOtherName, meaning that its value can be a local translation of the subdivision name as well as just another name for it
- If a subdivision doesn't have a local name or variant of its name then the attribute is now set to null
- When adding new subdivision, latLng attribute value not explicitly required, if not provided it will be set to []
- Changed add_local_names function in the update_subdivisions.py script to add_local_other_names to reflect "other" names being added to the attribute
- local_other_names.csv contains the name column as well which is the official ISO subdivision name, added for readability of the file
- Multiple subdivision names changed to match the language of the majority of their other subdivision names e.g some Finish subdivision name's have been changed from their Swedish name into Finish to match the majority of the subdivision's being in Finish. Also Haiti has majority subdivision's in French, hence 2 are changed from HT to FR languages
- Removed the localNameSame column from subdivision_updates.csv. Changed the localName column to localOtherName, code to subdivisionCode and alpha_code to alphaCode.
- All references to localName (vars, comments, functions etc) changed to localOtherName to incorporate the new other name variants for the attribute
- During the unit tests, any test dirs/folders are exported to the tests folder itself rather than the main dir
- Split any local name related functions into their own script
- Changed language description to mention change from local name to local/other name
- Changed a couple of methods in iso3166 software into static methods
- Changed name of dir with all main and auxillary scripts from iso3166_2_scripts to scripts
- Updated the order for the local/other names per subdivision in the csv
- Changed export filenames for get_script to have a '_' before list of alpha codes rather than a '-'
- Changed calls to convert_to_alpha function in get_script such that each input alpha code is validated through it rather than just alpha-3 or numeric codes
- All references to the convert_to_alpha2 function are now used as way to validate and convert the code, raising an error if applicable
- In any unit tests that use requests library, chaanged from static user agent to using fakeuseragent package
- Rather than hard coding the list of applicable user agents to use when using the requests library, use the fake-useragent package to randomly select one
- alpha_codes_from_to parameter name changed to alpha_codes_range 
- For history attribute, iso3166-updates attribute names updated to their correct name
- Changed any print statement outputs to f strings
- Order of language lookup table output updated in export
- In get script, exclude_lat_lng parameter changed to extract_lat_lng - default of False
- tqdm loop tidied up
- iso3166_2_updates folder changed to iso3166_2_resources
- Split up several code blocks and functionalities of export script into separate functions
- Removed separate JSON imports for windows/mac
- All flag icon references on iso3166-flag-icons repo changed to link to the raw image file
- Throughout software package and API, excludeAttributes changed to filter Attributes - only include the list of attributes input
- Changed the search output attributes to all camelCasing
- Changed the parameter in /scripts from exclude_default_attributes to filter_attributes, to be more intuitive

## v1.6.1 - June 2024


### Added
- list_subdivisions endpoint added to API that returns list of all subdivision codes per country
- Unit tests for flag_url function in update_subdivisions script
- Separate function for extracting and parsing data attributes from RestCountries API
- Added raise_for_status error catcher for requests library


### Changed
- Rotate user agent headers for any scripts using requests.get 
- Contributing page on docs updated

### Fixed
- Error in request URL for RestCountries API in update_subdivisions script
- Raise TypeError if invalid data type input to export_iso3166_2 function rather than system crashing
- When getting the coordinates (latitude/longitude) per subdivision, a more granular and accurate response is ensured by appending the country name to the subdivision name when searching via the Google Maps API

## v1.6.0 - June 2024

### Added 
- New dataset object exported with flagUrl attribute now flag
- Added functionality for adding additional country-level attributes per subdivision via the RestCountries API
- Added functionality for excluding some of the default attributes that are exported for every subdivision by default 
- Added functionality for get_iso3166_2 script where you can export all data starting from a specified ISO 3166-1 alpha code alphabetically
- Parameter typing for each function
- Added more info to the error messages 
- Code coverage
- Added additional unit tests for CSV export of ISO 3166-2 dataset from get_iso3166_2 script
- Added unit tests for update_subdivisions functionality
- Added export_csv parameter to get_iso3166_2 script to allow for optional export to CSV, JSON exported by default
- Added iso3166 object filepath parameter to the ISO3166_2() class that allows for custom object to be imported on class instantiation 

### Changed 
- flagUrl attribute changed to flag in dataset
- Moved functionality for getting subdivision flag data into its own function in update_subdivisions.py script
- When exporting data using get_iso3166_2 script, export to CSV by default
- update_subdivisions script can be called by itself from the cmd line/terminal, passing in the required parameters
- Added flag/parameter to custom_subdivisions function where if set you can create a hard copy of the existing iso3166-2.json object so that you aren't directly adding/amending/deleting a subdivision from the object
- Sort rows in iso3166_2_updates/subdivision_updates.csv by date (newest first) rather than by alpha-2 country code
- Update package description
- Updated unit tests to reflect above changes and new features
- Split up jobs in build workflows into separate sections
- Added more info for each functionality with additional examples in the software and API documentation 
- Upgrade checkout action in workflow from v3 to v4
- Raise error in update_subdivisions script when trying to delete a subdivision that doesn't exist
- In unit tests, exclude latLng attribute so gmaps API isn't called when running
- When adding a custom subdivision via the respective function, the "name" and "type" attributes are no longer explicitly required

### Fixed
- In the update_subdivisions function when editing a subdivision and its actual subdivision code, the flag attribute may have erroneous or null data
- In the update_subdivisions function you can now put in the full subdivision code or just the right hand side of the code into the subdivision_code parameter
- In the update_subdivisions function when amending an existing subdivision's code, the current flag URL attribute value points to the original flag URL, check on repo if flag with new subdivision code exists, otherwise keep the value to the original
- In the update_subdivisions function when amending an existing subdivision's code, error now raised when the new subdivision code's country code does not match the original
- If a custom subdivision object is input via its respective function, latLng attribute is set to 3d.p 
- Fixed syntax of some function parameters that can take multiple data types
- Fixed parameter typing syntax for some function parameters that can be multiple data types
- Error when adding a new subdivision, now will raise an error if the input parent code is invalid/not a country subdivision
- In get_flag_url function in update_subdivision script, you can pass in the full subdivision code or just the RHS of it

## v1.5.4 - March 2024


### Added
- Add a likeness score parameter to the search functionality such that it will return one or more subdivisions that match according to the percentage of likeness
- Added custom_subdivision function where user can add a custom subdivision to the iso3166-2 object
- Add UPDATES.md file that outlines all recent subdivision changes to the ISO 3166-2 data


### Changed
- Changed data encapsulation for object, with the dataset now accessible after creating an instance of the ISO3166_2 class
- Change search functionality algorithm from difflib to thefuzz libary
- Change setup.py to pyproject.toml
- Update unit tests to reflect changes made to the software such as likeness score and searching method etc
- Change iso3166_2_updates directory to iso316_2_updates


### Fixed
- Incorrect subdivision data returning when searching for a subdivision using its name when its name had a comma in it
- GitHub repo badges not displaying correctly



## v1.4.0 - December 2023

### Added
- readthedocs documentation added
- Search for a particular subdivision via its subdivision name, finding the closest match using difflib libary
- Added dateIssued and notes columns to subdivision_updates.csv, sort by country code and then by dateIssued
- tqdm progress loop added to get_iso3166_2 script


### Changed
- Software package description updated
- Changed software license to MIT
- Remove subdivision_parent_codes function that returned this list of parent codes per subdivision


### Fixed


## v1.3.0 - December 2023

### Added
- Added subdivision_updates.csv that lists rows of updates made to the ISO 3166-2 subdivision data
- Added local_names.csv file that lists the names of each subdivision in their local languages
- lat_lng attribute added for each subdivision using the googlemaps API, set to 3d.p


### Changed
- When running unit tests on iso3166-2.json object, create a backup/archive of object before running tests


### Fixed
- Subdivision codes not sorting alphabetically in output


## <=v1.2.0 - <September 2023

### Added
- Initial software release
- Initial API release
- Added any missing iso3166-2 subdivision data to object that may have been missing from initial export
- Initial attributes include: country code, subdivision code, parent code, type and flag URL
- Created custom-built iso3166-updates software used to track all updates made by the ISO to the ISO 3166