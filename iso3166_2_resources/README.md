<a name="TOP"></a>

# ISO 3166-2 Resources

This directory has a series of data/utility files required for the building of the `iso3166-2` software and dataset. More info and the purpose of each is outlined below.

* **local_other_names.csv** - CSV containing thousands of local/alternative names for the thousands of subdivisions 
* **language_lookup.json/md** - JSON and markdown files showing useful info and data about each of the languages/language codes used in the local_other_names.csv
* **UPDATES.md** - markdown displaying the individual ISO 3166-2 data updates implemented into the dataset from 2022-present, pulled from the [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) software
* **geo_cache.csv** - cache of all the geographical related export data required for the ISO 3166-2 data export in the Geo module, primarily the centroid/latLng values per subdivision, but the cache will also include the geojson, bounding box and other info per subdivision
* **geo_cache_min.csv** - simplified cache of just the latLng data for each subdivision required in the Geo module
* **iso3166-2-export.csv** - CSV version of the ISO 3166-2 JSON
* **iso3166-2-export.xml** - XML version of the ISO 3166-2 JSON
* **iso3166-2-metadata.json** - JSON containing a plethora of useful data and attributes around the iso3166-2 repository

## Local/Other Names

#### Overall, this dataset has **3,734** local/other name variations in the dataset across **434** languages for the **5,046** subdivisions. 

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



## Language Lookup

**Overall, this file has 434 individual language objects for the 5,046 subdivisions and 3,733 local/other names.**

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

## Metadata 

A plethora of metadata relating to the ISO 3166-2 dataset and repository can be exported. This metadata export file is available here `/iso3166_2_resources/iso3166-2-metadata.json`. The list of metadata attributes exported are listed below:

* Total number of countries & subdivisions 
* Dataset size (MB/KB)
* Number of null/empty attributes, mainly for localOtherName, flag and history
* Total number of attributes across the whole dataset
* Size of each individual attribute 
* Number of unique subdivision types
* Average subdivision count
* Total number of local/other names across the dataset
* Subdivisions per hemisphere (north/south, east/west)

[Back to top](#TOP)

[updates_md]: https://github.com/amckenna41/iso3166-2/blob/main/UPDATES.md