<a name="TOP"></a>

# ISO 3166-2 Resources

This directory has a series of data/utility files required for the building of the `iso3166-2` software and dataset. More info and the purpose of each is outlined below.

* **local_other_names.csv** - CSV containing thousands of local/alternative names for the thousands of subdivisions 
* **subdivision_updates.csv** - CSV of new subdivisions, amendments to existing subdivisions as well as deletion of subdivisions required for the dataset
* **language_lookup.json/md** - JSON and markdown files showing useful info and data about each of the languages/language codes used in the local_other_names.csv
* **UPDATES.md** - markdown displaying the individual ISO 3166-2 data updates implemented into the dataset from 2022-present, pulled from the [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) software

## Local/Other Names

#### Overall, this dataset has **3,738** local/other name variations in the dataset across **434** languages for the **5,049** subdivisions. 

The [`local_other_names.csv`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_resources/local_other_names.csv) file stores the **local translation** for each subdivision in different languages relevant to the region/subdivision. It also has any **alternative variants** of its name that it may be known as, including **nicknames**, **abbreviations** or **colloquial** names. For each local/other name, the ISO 639 3 letter language code is appended in brackets to it. Although, for some smaller regional dialects and unofficially recognised languages an ISO 639 code unavailable, so the [`Glottolog`](https://glottolog.org/) or other language databases (e.g [`IETF`](https://support.elucidat.com/hc/en-us/articles/6068623875217-IETF-language-tags)) code is used instead.

<!-- e.g berr1239 for the Berrichon dialect of France, ulst1239 for the Ulster Scots dialect of Ireland and cico1238 for the Cicolano-Reatino-Aquilano dialect of Italy. The file is sorted by alpha-2 country code. -->

The [`local_other_names.csv`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166-2-updates/local_other_names.csv) file has the below columns:

* **alphaCode** - ISO 3166-1 alpha-2 country code
* **subdivisionCode** - subdivision code
* **name** - subdivision name
* **localOtherName** - subdivision local translation or alternative name variant with the 2 letter/3 letter ISO 639 language code in brackets

### E.g; Burgenland of Austria (AT-1)  

| alphaCode | subdivisionCode | name | localOtherName | 
| --------- | --------------- | ---- | -------------- | 
| AT        | AT-1            | Burgenland        | "Burgenland (eng), Őrvidék (hun), Gradišće (hrv), Burgnland (bar), Gradiščanska (slv), Hradsko (slk)" | 

### E.g; Bresckaja voblasć of Bulgaria (BY-BR)

| alphaCode | subdivisionCode | name | localOtherName | 
| --------- | --------------- | ---- | -------------- | 
| BY        | BY-BR           | Bresckaja voblasć | "Брэсцкая вобласць (bel), Brestskaya voblasts (bel), Brest (eng)" | 

### E.g; Hautes-Pyrénées of France (FR-65)  

| alphaCode | subdivisionCode | name | localOtherName | 
| --------- | --------------- | ---- | -------------- | 
| FR        | FR-65           | Hautes-Pyrénées   | "Nauts Pirenèus (oci), Hauts Pirenèus (oci), Altos Pirineos (spa), Alts Pirineus (cat), Upper Pyrenees (eng)" | 


### E.g; Vilniaus apskritis of Lithuania (LT-VL)  

| alphaCode | subdivisionCode | name | localOtherName | 
| --------- | --------------- | ---- | -------------- | 
| LT        | LT-VL           | Vilniaus apskritis   | "Vilnius County (eng), Capital Region (eng), Sostinės regionas (lit)" | 


## Subdivision Updates

**Overall, this file has ~500 individual subdivision additions/deletions/amendments for the >5000 subdivisions.**

The [`subdivision_updates.csv`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_resources/subdivision_updates.csv) file maintains and tracks all of the latest and accurate ISO 3166-2 data changes for the `iso3166-2` JSON object in the software, from 2022 onwards. New subdivisions, amendments to existing subdivisions as well as deletions of subdivisions are appended to the CSV file. During execution of the main `scripts/export_iso3166_2.py` script, this CSV is read in and the relevant changes are implemented to the exported objects. 

The purpose for the creation of this script and dataset was that several of the data sources for the subdivision data was out-of-date, inaccurate or missing in comparison to the true list of ISO 3166-2 data. Therefore this file ensures during the exporting process that the dataset is **accurate**, **up-to-date** and **reliable**.

The [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) custom-built software was used to extract these latest ISO 3166-2 subdivision changes for all countries. It uses a variety of data sources to pull the latest, most accurate and reliable ISO 3166 changes data, and is available via a Python software package and a RESTful API. The changes listed for a country are then appended to the end of the aforementioned CSV file which can then be input into the `update_subdivision()` function. The CSV file is sorted by date, with the newest changes being appended to the end. Individual updates can also be passed into the `update_subdivision()` function using its input parameters.

The [`subdivision_updates.csv`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_resources/subdivision_updates.csv) file has the below columns:
* **alphaCode** - ISO 3166-1 alpha-2 country code
* **subdivisionCode** - subdivision code
* **name** - subdivision name
* **localOtherName** - subdivision local name translation or alternative variant of its name with the ISO 639 language code in brackets
* **type** - subdivision type
* **parentCode** - subdivision parent code
* **flag** - subdivision flag URL from [`iso3166-flags`](https://github.com/amckenna41/iso3166-flags) repo (a custom-built repo with over 3500 individual subdivision flags)
* **latLng** - subdivision latitude/longitude
* **customAttributes** - object of custom attributes and their values e.g population, gdp, hdi etc
* **delete** - set to 1 if subdivision is to be deleted
* **notes** - some info about the change being made (addition, amendment or deletion)
* **dateIssued** - date the subdivision change was communicated, according to the ISO, in YYYY-MM-DD format

The [UPDATES.md][updates_md] file contains all of the ISO 3166 updates/changes from 2022 onwards, as pulled from the [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) repo. It differs from the [`subdivision_updates.csv`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_resources/subdivision_updates.csv) as not all updates/changes published by the ISO result in a direct subdivision data change. 

### E.g; Adding the DZ-49 and DZ-50 subdivisions to Algeria 

| alphaCode | subdivisionCode | localOtherName                  | name                | type     | parent_code | flag | latLng          | customAttributes | delete | notes                         | dateIssued  |
|-----------|------------------|----------------------------------|----------------------|----------|-------------|------|------------------|------------------|--------|-------------------------------|-------------|
| DZ        | DZ-49           | تيميمون (ar)                     | Timimoun            | Province |             |      | [29.262, 0.241]  |                  | 0      | Adding DZ-49 subdivision      | 2022-11-29  |
| DZ        | DZ-50           | ولاية برج باجي مختار (ar)        | Bordj Badji Mokhtar | Province |             |      | [21.680, 0.944]  |                  | 0      | Adding DZ-50 subdivision      | 2022-11-29  |


### E.g; Deleting the FR-GF and FR-GP subdivisions from France:
| alphaCode | subdivisionCode | localOtherName | name | type | parent_code | flag | latLng | customAttributes | delete | notes                      | dateIssued  |
|-----------|------------------|----------------|------|------|-------------|------|--------|------------------|--------|----------------------------|-------------|
| FR        | FR-GF           |                |      |      |             |      |        |                  | 1      | Deleting FR-GF subdivision | 2021-11-25  |
| FR        | FR-GP           |                |      |      |             |      |        |                  | 1      | Deleting FR-GP subdivision | 2021-11-25  |


### E.g; Updating parent code and custom population attribute for LT-43:

| alphaCode | subdivisionCode | localOtherName | name | type | parent_code | flag | latLng | customAttributes | delete | notes                      | dateIssued  |
|-----------|------------------|----------------|------|------|-------------|------|--------|------------------|--------|----------------------------|-------------|
| LT        | LT-43           |                |      |      |    LT-SA         |      |        |       {"population": 112581}          | 0      | Updating LT-43 parent subdivision code & population custom attribute | 2025-01-01  |



## Language Lookup

**Overall, this file has 434 individual language objects for the 5,049 subdivisions and 3,738 local/other names.**

The `scripts/language_lookup.py` script exports the the [`language_lookup.md`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_resources/language_lookup.md) and [`language_lookup.json`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_resources/language_lookup.json) files. These files act as reference data for the over **3,700** local/other name variants within the [`local_other_names.csv`](https://github.com/amckenna41/iso3166-2/blob/main/iso3166_2_resources/local_other_names.csv) dataset, with each name having a referenced language code in brackets.  All of this language data is encapsulated within the `LanguageLookup` class that allows for access to the language data as well as additional functionality to add, delete, amend a language object, search and re-export the data.

The files exported are mainly used as a reference and are not explicitly utilised within the `iso3166-2` software or API.

For each language object it contains the following attribute:

* **code** - language code, primarily the officially recognized 3 letter ISO 639-2 code although several codes from other language databases such as the Glottolog and IETF are used
* **name** - official language name
* **scope** - the general classification or nature of the language. The available scopes/categories are A (artificial language), C (collective), D (dialect), F (family), I (individual), L1 (level 1 language), M (macrolanguage) and S (special)
* **type** - status or nature of the language, the available types are A (ancient), C (constructed), E (extinct), H (historical) and L (living)
* **sources** - source URLs for language
* **countries** - list of alpha-2 country codes that the language features in, in the local/other names csv
* **total** - total number of subdivisions that the language features in, in the local/other names csv

### E.g; Catalan (cat)


| code      | name         | scope       | type   | source    | countries | total |
| --------- | -------------| ----------- | ------ | --------- | --------- | ----- |
| cat       | Catalan      |  Individual | Living | https://iso639-3.sil.org/code/cat, https://www.loc.gov/standards/iso639-2/php/langcodes_name.php?code_ID=75 | ES,FR | 11 | 

### E.g; Danish (dan)

| code      | name         | scope       | type   | source    | countries | total |
| --------- | -------------| ----------- | ------ | --------- | --------- | ----- | 
| dan       | Danish       | Individual  | Living | https://iso639-3.sil.org/code/dan, https://www.loc.gov/standards/iso639-2/php/langcodes_name.php?code_ID=109 | DK,DE,EE,DL  | 7 | 


### E.g; Taiwanese Mandarin (taib1240)

| code      | name         | scope       | type   | source    | countries | total |
| --------- | -------------| ----------- | ------ | --------- | --------- | ----- | 
| taib1240       | Taiwanese Mandarin       | Dialect  | Living | https://iso639-3.sil.org/code/dan, https://www.loc.gov/standards/iso639-2/php/langcodes_name.php?code_ID=109 | TW  | 7 | 

[Back to top](#TOP)

[updates_md]: https://github.com/amckenna41/iso3166-2/blob/main/UPDATES.md
