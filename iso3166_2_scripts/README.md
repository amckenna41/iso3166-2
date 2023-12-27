# Scripts for exporting and updating all ISO 3166-2 data

The [`get_iso3166_2.py`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_scripts/get_iso3166_2.py) script is used for pulling and exporting the latest ISO 3166-2 data from the vairous data sources and the [`update_subdivisions.py`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_scripts/update_subdivisions.py) script is used for adding/amending/deleting subdivisions to the `iso3166-2` software and object.

Requirements (get_iso3166_2.py)
------------------------------
* [python][python] >= 3.8
* [iso3166-2][iso3166_2] >= 1.5.0
* [requests][requests] >= 2.28.1
* [iso3166][iso3166] >= 2.1.1
* [pycountry][pycountry] >= 22.3.5
* [googlemaps][googlemaps] >= 4.10.0
* [tqdm][tqdm] >= 4.64.0
* [natsort][natsort] >= 8.4.0
* [pandas][pandas] >= 1.4.3
* [numpy][numpy] >= 1.23.2

Usage (get_iso3166_2.py)
------------------------
The script `get_iso3166_2.py` is used for gathering and exporting subdivision data for ALL countries to the JSON object. It uses the [pycountry][pycountry] and [googlemaps][googlemaps] packages to gather and export all the required subdivision info. Calling the script using its default parameters will gather all the data for ALL countries, but the <i>alpha2_codes</i> parameter can be set to pull the latest data for a specific list of one or more countries (the alpha-3 code can also be input, which is then converted into its 2 letter alpha-2 counterpart).

To download all of the latest ISO 3166-2 subdivision data for all countries, from the main repo dir, run the `get_iso3166_2.py` in a terminal or command line below; (the script takes around <em>1 hour and 40 mins</em> to execute):

```bash
python3 iso3166_2_scripts/get_iso3166_2.py --json_filename=iso3166_2.json --output_folder=iso3166_2 --verbose

#--alpha2_codes: list of 1 or more 2 letter alpha-2 country codes (if not specified then all country codes will be used).
#--json_filename: output filename for exported JSONs.
#--output_folder: output folder to store JSONs.
#--verbose: if set to 1 then the progress of the ISO 3166-2 data export will be output.
```

To download all of the latest ISO 3166-2 subdivision data for Germany, Portugal and Spain (the data will be exported to a JSON called iso3166_2-DE,ES,PT.json):
```bash
python3 iso3166_2_scripts/get_iso3166_2.py --alpha2_codes=DE,PT,ES --json_filename=iso3166_2.json 
```

Requirements (update_subdivisions.py)
-------------------------------------
* [python][python] >= 3.8
* [iso3166][iso3166] >= 2.1.1
* [natsort][natsort] >= 8.4.0
* [pandas][pandas] >= 1.4.3
* [numpy][numpy] >= 1.23.2

Usage (update_subdivisions.py)
------------------------------
The script [`update_subdivisions.py`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_scripts/update_subdivisions.py) has the `update_subdivision()` function that was created to streamline the addition/amendment/deletion to any of the subdivisions in the data object. The function can accept an individual subdivision change by passing in all the required attribute values to the function directly. Alternatively, a <b>CSV</b> file with rows of the individual changes can be passed in, allowing for hundreds of changes to be made in one go. 

The primary input parameters to the `update_subdivision()` function are: <i>alpha2_code, subdivision_code, name, local_name, type, latLng, parent_code, flag_url</i> and <i>delete</i>. The first eight parameters represent the data to be added/changed to the specified country code and subdivision code (<i>alpha2_code, subdivision_code</i>) and <i>delete</i> is a boolean flag that should be set (0/1) if the input subdivision is to be deleted - by default this will be 0. For any addition, amendment or deletion, the <i>country_code</i> and <i>subdivision_code</i> parameters are required, but the remainder of the parameters are optional. If these optional parameters are not set then they will be set null, in the case of an addition or deletion, or remain as their previous values in the case of an amendment.  

As mentioned, you can also pass in a <b>CSV</b> with rows of all the changes to be made to the subdivision object. The <b>CSV</b> has the same columns as the aforementioned function parameters, but additionally has the <i>localNameSpelling, notes</i> and <i>dateIssued</i> columns. <i>localNameSpelling</i> should be set to 1 if the subdivision local name is the same as its name, if the column is empty or 0 then the subdivision will take the value specified by the <i>localName</i> column. <i>notes</i> just contains a small description about the addition/amendment/deletion being made and <i>dateIssued</i> is the date that the subdivision change was communicated by the ISO. 

```python
from iso3166_2_scripts.update_subdivisions import *

#adding Timimoun Province of Algeria (DZ-49) to ISO 3166-2 object (from newsletter 2022-11-29)
update_subdivision("DZ", "DZ-49", name="Timimoun", local_name="ولاية تيميمون", type="Province", latLng=[29.263, 0.241], parent_code=None, flag_url=None)

#adding Waterford County of Ireland (IE-WD) to ISO 3166-2 object - subdivision already present so no changes made
update_subdivision("IE", "IE-WD", "Waterford", local_name="Port Láirge", type="County", latLng=[52.260, -7.110], parent_code="IE-M", flag_url="https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/IE/IE-WD.png")
#iso.update_subdivision("IE", "IE-WD") - this will also work as only the first 2 params requried

#amending the subdivision name of subdivision FI-17 from Satakunda to Satakunta (from newsletter 2022-11-29)
update_subdivision("FI", "FI-17", name="Satakunta")

#deleting FR-GP (Guadeloupe) and (FR-MQ Martinique) subdivisions 
update_subdivision("FR", "FR-GP", delete=1)
update_subdivision("FR", "FR-MQ", delete=1)

#error raised as both country_code and subdivision_code parameters required
update_subdivision(type="region", latLng=[], parent_code=None)

#passing in a csv with rows of subdivision additions/updates/deletions
update_subdivision(subdivision_csv="new_subdivisions.csv")
```

[python]: https://www.python.org/downloads/release/python-360/
[requests]: https://requests.readthedocs.io/
[iso3166]: https://github.com/deactivated/python-iso3166
[iso3166_2]: https://github.com/amckenna41/iso3166-2
[pycountry]: https://github.com/flyingcircusio/pycountry
[rest]: https://restcountries.com/
[googlemaps]: https://github.com/googlemaps/google-maps-services-python
[tqdm]: https://github.com/tqdm/tqdm
[natsort]: https://pypi.org/project/natsort/
[pandas]: https://pandas.pydata.org/
[numpy]: https://numpy.org/
[iso3166-updates]: https://github.com/amckenna41/iso3166-updates
[flag_icons_repo]: https://github.com/amckenna41/iso3166-flag-icons