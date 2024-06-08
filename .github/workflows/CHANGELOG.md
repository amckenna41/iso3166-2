# Change Log

## 1.7.0 - TBC

### Added
- Add list of cities for each subdivision using the country-states-city API
- Added __version__ attribute to ISO3166_2() class

## v1.6.1 - June 2024


### Added
- list_subdivisions endpoint added to API that returns list of all subdivision codes per country
- Unit tests for flag_url function in update_subdivisions script
- Separate function for extracting and parsing data attributes from RestCountries API
- Added raise_for_status error catcher for requests library


### Changed
- Rotate user agent headers for any scripts using requests.get 


### Fixed
- Error in request URL for RestCountries API in update_subdivisions script
- Raise TypeError if invalid data type input to export_iso3166_2 function rather than system crashing


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