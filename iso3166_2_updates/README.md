# ISO 3166-2 Subdivision Updates

This directory maintains and tracks all of the latest ISO 3166-2 data added to the `iso3166-2` JSON object in the software, from 2022 onwards. New subdivisions, amendments to existing subdivisions as well as deletions of subdivisions are appended to the CSV file [`subdivision_updates.csv`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166-2-updates/subdivision_updates.csv). When updated subdivision data is to be added, the script `iso3166_2_scripts/get_iso3166_2.py` is called which pulls in the [`subdivision_updates.csv`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166-2-updates/subdivision_updates.csv) and makes the relevant addition, amendment or deletion to the subdivision data object.

The [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) custom-built software was used to extract these latest ISO 3166-2 subdivision changes for all countries. It uses a variety of data sources to pull the latest changes data, and is available via a Python software package and an API. The changes listed for a country are then appended to the end of the aforementioned CSV file which can then be input into the `update_subdivision()` function. The [`subdivision_updates.csv`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166-2-updates/subdivision_updates.csv) file is sorted by date, with the newest changes being appended to the end. Individual updates can also be passed into the `update_subdivision()` function using its input parameters.

The `subdivision_updates.csv` file has the below columns:
* alpha_code (ISO 3166-1 alpha-2 country code).
* code (subdivision code).
* name (subdivision name).
* localName (subdivision local name).
* type (subdivision type).
* parentCode (subdivision parent code).
* flag (subdivision flag URL from [`iso3166-flag-icons`](https://github.com/amckenna41/iso3166-flag-icons) repo).
* latLng (subdivision latitude/longitude).
* localNameSame (whether subdivision local name is the same as its name in English).
* delete (set to 1 if subdivision is to be deleted).
* notes (some info about the change being made).
* dateIssued (date the subdivision change was communicated, according to the ISO).

All changes made are also logged and appended to the [UPDATES.md][updates_md] file.

## For example, adding the DZ-49 and DZ-50 subdivisions to Algeria:

| alpha_code | code  | localName | name | type | parent_code | flag | latLng | localNameSame | delete | notes | dateIssued |
|--------------|-------|-----------|------|------|-------------|------|--------|-------------------|--------|-------|------------|
| DZ           | DZ-49 | تيميمون | Timimoun | Province |   |   | [29.262, 0.241] |  0 |  0 | Adding DZ-49 subdivision | 2022-11-29 | 
| DZ | DZ-50 | ولاية برج باجي مختار | Bordj Badji Mokhtar | Province |   |   | [21.680, 0.944] |  0 |  0 | Adding DZ-50 subdivision | 2022-11-29 |

## Local Names

> Local names functionality in development

Additionally, the [`localNames.csv`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166-2-updates/local_names.csv) file stores the local name for each subdivision. Many of the subdivisions have the same local name as subdivision name that's listed in the ISO 3166-2, but many also have a differing local name, especially for parts of the world which do not use the Latin script. The file is sorted by alpha-2 country code.

The `local_names.csv` file has the below columns:

* alpha_code (ISO 3166-1 alpha-2 country code).
* subdivision_code (subdivision code).
* name (Subdivision name).
* localName (subdivision local name).
* sameName (set this to 1 if a subdivision's name and local name are the same e.g for English speaking countries).
<!-- * localNameOther (a dict of subdivision names and other local translations e.g Finland has local translations in Finish and Swedish, South Africa has local translations in Afrikaans, Sotho, Swahili and Ndebele etc). -->

[updates_md]: https://github.com/amckenna41/iso3166-2/blob/main/UPDATES.md