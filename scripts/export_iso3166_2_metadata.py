import argparse
import json
import os
import pandas as pd
from collections import Counter

iso3166_2_main_metadata = {"total_countries": 0, "total_subdivisions": 0, "dataset_kb": 0, "dataset_mb": 0,
                           "total_attributes": 0, "num_unique_attributes": 0, "unique_subdivision_types": 0,
                           "average_subdivision_per_country": 0, "zero_subdivisions_total": 0,
                           "max_subdivisions_country": "", "null_attributes_total": 0, 
                           "null_local_other_name_total": 0, "null_flag_total": 0, "null_type_total": 0,
                           "null_latlng_total": 0, "null_parentcode_total": 0, "null_history_total": 0,
                           "total_local_other_entries": 0, "hemisphere_north_total": 0, "hemisphere_south_total": 0,
                           "hemisphere_east_total": 0, "hemisphere_west_total": 0} 

def export_iso3166_2_metadata(iso3166_2_filename: str, export_filename: str="iso3166-2-metadata") -> None:
    """
    Export a plethora of useful data and info about the ISO 3166-2 repository 
    and dataset and is exported to an easy to read JSON/CSV. The data included in 
    the export include:
    - total number of countries & subdivisions 
    - dataset size (MB/KB)
    - number of null/empty attributes, mainly for localOtherName, Flag and History
    - total number of attributes across the whole dataset
    - size of each individual attribute 
    - number of unique subdivision types
    - average subdivision count
    - total number of local/other names across the dataset
    - subdivisions per hemisphere (north/south, east/west)

    Parameters
    ==========
    None

    Returns
    =======
    None

    Raises
    ======
    OSError:
        If the ISO 3166-2 JSON file is not found.
    """ 
    #raise error if file not found
    if not (os.path.isfile(iso3166_2_filename)):
        raise FileNotFoundError(f"The ISO 3166-2 JSON file '{iso3166_2_filename}' was not found.")

    #import data
    with open(iso3166_2_filename, "r", encoding="utf-8") as f:
        iso3166_data = json.load(f)

    #create copy of main metadata dict
    iso3166_2_main_metadata_copy = dict(iso3166_2_main_metadata)  

    def is_nullish(v):
        """ Auxillary function that checks if the input value is nullish (None, empty string, empty list/dict). """
        if v is None:
            return True
        if isinstance(v, str) and v.strip() == "":
            return True
        if isinstance(v, (list, dict)) and len(v) == 0:
            return True
        return False    
    
    #get the file size of main data object
    try:
        file_bytes = os.path.getsize(iso3166_2_filename)
    except Exception:
        file_bytes = 0

    #add file size (KB & MB) to metadata object
    iso3166_2_main_metadata_copy["dataset_kb"] = round(file_bytes / 1024.0, 3)
    iso3166_2_main_metadata_copy["dataset_mb"] = round(iso3166_2_main_metadata_copy["dataset_kb"] / 1024.0, 3)
    
    #add total number of countries to metadata object
    total_countries = len(iso3166_data.keys())
    iso3166_2_main_metadata_copy["total_countries"] = total_countries

    #metadata counters
    total_subdivisions = 0
    zero_sub_countries = 0
    max_country = ("", -1)
    attr_union = set()
    attr_total_count = 0
    type_values = set()
    null_counts = Counter()
    local_other_total_entries = 0
    hemi_NS = Counter()  #North / South
    hemi_EW = Counter()  #East / West

    #iterate over subdivision data object, exporting the various stats/metadata 
    for alpha2, subdivs in iso3166_data.items():
        #increment zero subdivision counter
        if not subdivs:
            zero_sub_countries += 1
            #add to max tracker if needed
            if max_country[1] < 0:
                max_country = (max_country[0], 0)  # keep as-is

        #initalise per-country subdivision counter
        subdiv_count = 0

        #iterate over individual subdivision objects
        for sub_code, attrs in subdivs.items():

            #increment subdivision counters
            subdiv_count += 1
            total_subdivisions += 1

            #attribute key stats
            keys = list(attrs.keys())
            attr_union.update(keys)
            attr_total_count += len(keys)

            #get type values (unique subtype labels)
            t = attrs.get("type")
            if isinstance(t, str) and t.strip():
                type_values.add(t.strip())

            #null tracking per field + overall count of nulls
            for field in ["localOtherName", "flag", "type", "latLng", "parentCode", "history"]:
                v = attrs.get(field)
                if is_nullish(v):
                    null_counts[f"null_{field.lower()}_total"] += 1
                    null_counts["null_attributes_total"] += 1

            #total number of entries in localOtherName (comma-separated list)
            local = attrs.get("localOtherName")
            if isinstance(local, str) and local.strip():
                #split individual local/other names by comma
                entries = [p.strip() for p in local.split(",") if p.strip()]
                local_other_total_entries += len(entries)

            #get hemispheres from latLng
            latlng = attrs.get("latLng")
            if isinstance(latlng, list) and len(latlng) >= 2:
                try:
                    lat = float(latlng[0])
                    lng = float(latlng[1])
                    if lat > 0:
                        hemi_NS["North"] += 1
                    elif lat < 0:
                        hemi_NS["South"] += 1
                    if lng > 0:
                        hemi_EW["East"] += 1
                    elif lng < 0:
                        hemi_EW["West"] += 1
                except Exception:
                    #ignore malformed coords; already counted as null above
                    pass

        #track the max number of subdivisions
        if subdiv_count > max_country[1]:
            max_country = (alpha2, subdiv_count)

    #add metadata stats to main metadata object
    iso3166_2_main_metadata_copy["total_subdivisions"] = total_subdivisions
    iso3166_2_main_metadata_copy["zero_subdivisions_total"] = zero_sub_countries
    iso3166_2_main_metadata_copy["total_attributes"] = attr_total_count
    iso3166_2_main_metadata_copy["num_unique_attributes"] = len(attr_union)
    iso3166_2_main_metadata_copy["unique_subdivision_types"] = len(type_values)
    iso3166_2_main_metadata_copy["average_subdivision_per_country"] = round(
        (total_subdivisions / total_countries) if total_countries else 0.0, 3
    )
    iso3166_2_main_metadata_copy["max_subdivisions_country"] = f"{max_country[0]}:{max_country[1]}" if max_country[0] else ""

    #map null counters into meta keys
    iso3166_2_main_metadata_copy["null_attributes_total"] = null_counts.get("null_attributes_total", 0)
    iso3166_2_main_metadata_copy["null_local_other_name_total"] = null_counts.get("null_localothername_total", 0)
    iso3166_2_main_metadata_copy["null_flag_total"] = null_counts.get("null_flag_total", 0)
    iso3166_2_main_metadata_copy["null_type_total"] = null_counts.get("null_type_total", 0)
    iso3166_2_main_metadata_copy["null_latlng_total"] = null_counts.get("null_latlng_total", 0)
    iso3166_2_main_metadata_copy["null_parentcode_total"] = null_counts.get("null_parentcode_total", 0)
    iso3166_2_main_metadata_copy["null_history_total"] = null_counts.get("null_history_total", 0)

    #local other name total entries
    iso3166_2_main_metadata_copy["total_local_other_entries"] = local_other_total_entries

    #count per hemispheres
    iso3166_2_main_metadata_copy["hemisphere_north_total"] = hemi_NS.get("North", 0)
    iso3166_2_main_metadata_copy["hemisphere_south_total"] = hemi_NS.get("South", 0)
    iso3166_2_main_metadata_copy["hemisphere_east_total"] = hemi_EW.get("East", 0)
    iso3166_2_main_metadata_copy["hemisphere_west_total"] = hemi_EW.get("West", 0)

    #get JSON export name
    if (os.path.splitext(export_filename)[1].lower() != ".json"):
        export_filename = f"{export_filename}.json"

    #export metadata to JSON/CSV
    with open(export_filename, 'w', encoding='utf-8') as f:
        json.dump(iso3166_2_main_metadata_copy, f, ensure_ascii=False, indent=4)
    # export_df = pd.DataFrame([iso3166_2_main_metadata_copy])
    # export_df.to_json(export_filename, index=False, orient="records", indent=4)

if __name__ == '__main__':

    #parse input arguments using ArgParse 
    parser = argparse.ArgumentParser(description='Script for exporting metadata about the ISO 3166-2 dataset and repository.')

    parser.add_argument('-iso3166_2_filename', '--iso3166_2_filename', type=str, required=False, default=os.path.join("iso3166_2", "iso3166-2.json"), 
        help='Filename for imported ISO 3166-2 JSON file.')
    parser.add_argument('-export_filename', '--export_filename', type=str, required=False, default="iso3166-2-metadata", 
        help='Filename for metadata export file.')
    
    #parse input args
    args = parser.parse_args()

    #export ISO 3166-2 data 
    export_iso3166_2_metadata(**vars(args))