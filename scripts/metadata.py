import argparse
import json
import os
import pandas as pd
from collections import Counter
from datetime import datetime

iso3166_2_main_metadata = {"total_countries": 0, "total_subdivisions": 0, "dataset_kb": 0, "dataset_mb": 0,
                           "total_attributes": 0, "num_unique_attributes": 0, "unique_subdivision_types": 0,
                           "average_subdivision_per_country": 0, "zero_subdivisions_total": 0,
                           "max_subdivisions_country": "", "min_subdivisions_country": "", "null_attributes_total": 0,
                           "hemisphere_north_total": 0, "hemisphere_south_total": 0, "hemisphere_east_total": 0, 
                           "hemisphere_west_total": 0,
                           "attribute_stats": {
                               "name": {"total_count": 0, "null_count": 0, "populated_count": 0, "completeness_percent": 0.0},
                               "localOtherName": {"total_count": 0, "null_count": 0, "populated_count": 0, "completeness_percent": 0.0, 
                                                  "total_individual_count": 0},
                               "flag": {"total_count": 0, "null_count": 0, "populated_count": 0, "completeness_percent": 0.0},
                               "type": {"total_count": 0, "null_count": 0, "populated_count": 0, "completeness_percent": 0.0},
                               "latLng": {"total_count": 0, "null_count": 0, "populated_count": 0, "completeness_percent": 0.0},
                               "parentCode": {"total_count": 0, "null_count": 0, "populated_count": 0, "completeness_percent": 0.0},
                               "history": {"total_count": 0, "null_count": 0, "populated_count": 0, "completeness_percent": 0.0}
                           }} 

def export_metadata(iso3166_2_filename: str, export_filename: str="iso3166-2-metadata", append_timestamp: bool=False) -> None:
    """
    Export a plethora of useful data and info about the ISO 3166-2 repository 
    and dataset and is exported to an easy to read JSON/CSV. The data included in 
    the export include:
    - total number of countries & subdivisions 
    - dataset size (MB/KB)
    - number of null/empty attributes, mainly for localOtherName, flag and history
    - total number of attributes across the whole dataset
    - size of each individual attribute 
    - number of unique subdivision types
    - average subdivision count
    - total number of local/other names across the dataset
    - subdivisions per hemisphere (north/south, east/west)
    - completeness percentage for each attribute

    Parameters
    ==========
    :iso3166_2_filename: str
        the filename for the ISO 3166-2 JSON file to import.
    :export_filename: str
        the filename for the metadata export file (JSON/CSV).
    :append_timestamp: bool
        if True, append a timestamp to the export filename in the format 
        {filename}_YYYY_MM_DD_HH_MM.json. If False, use the export_filename as-is.
        Default is False.

    Returns
    =======
    None

    Raises
    ======
    FileNotFoundError:
        If the ISO 3166-2 JSON file is not found.
    TypeError:
        If latLng values cannot be converted to float.
    ValueError:
        If latLng values are outside valid coordinate ranges.
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
        """ Auxiliary function that checks if the input value is nullish (None, empty string, empty list/dict). """
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
    max_countries = []
    max_count = -1
    min_countries = []
    min_count = float('inf')
    attr_union = set()
    attr_total_count = 0
    type_values = set()
    null_counts = Counter()
    local_other_total_entries = 0
    hemi_NS = Counter()  #North / South
    hemi_EW = Counter()  #East / West
    
    #initialize attribute stats tracking
    attribute_stats = {
        "name": {"total_count": 0, "null_count": 0, "populated_count": 0},
        "localOtherName": {"total_count": 0, "null_count": 0, "populated_count": 0, "total_individual_count": 0},
        "flag": {"total_count": 0, "null_count": 0, "populated_count": 0},
        "type": {"total_count": 0, "null_count": 0, "populated_count": 0},
        "latLng": {"total_count": 0, "null_count": 0, "populated_count": 0},
        "parentCode": {"total_count": 0, "null_count": 0, "populated_count": 0},
        "history": {"total_count": 0, "null_count": 0, "populated_count": 0}
    }

    #iterate over subdivision data object, exporting the various stats/metadata 
    for alpha2, subdivs in iso3166_data.items():
        #increment zero subdivision counter
        if not subdivs:
            zero_sub_countries += 1
            #add to max tracker if needed
            if max_count < 0:
                max_count = 0  # initialize if needed

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
            
            #track individual attribute statistics
            for attr_name in ["name", "localOtherName", "flag", "type", "latLng", "parentCode", "history"]:
                attr_value = attrs.get(attr_name)
                attribute_stats[attr_name]["total_count"] += 1
                
                if is_nullish(attr_value):
                    attribute_stats[attr_name]["null_count"] += 1
                else:
                    attribute_stats[attr_name]["populated_count"] += 1

            #total number of entries in localOtherName (comma-separated list)
            local = attrs.get("localOtherName")
            if isinstance(local, str) and local.strip():
                #split individual local/other names by comma
                entries = [p.strip() for p in local.split(",") if p.strip()]
                local_other_total_entries += len(entries)

            #get hemispheres from latLng
            latlng = attrs.get("latLng")

            if isinstance(latlng, (list, tuple)) and len(latlng) >= 2:
                # try and extract the lat/lng from the list/tuple, raise value or type if malformed/invalid
                try:
                    lat = float(latlng[0])
                    lng = float(latlng[1])
                except TypeError as e:
                    raise TypeError(f"Invalid latLng type for {latlng}: {e}")
                except ValueError as e:
                    raise ValueError(f"Invalid latLng value for {latlng}: {e}")
                else:
                    # get the hemispheres if lat/lng are valid
                    if -90.0 <= lat <= 90.0 and -180.0 <= lng <= 180.0:
                        if lat > 0:
                            hemi_NS["North"] += 1
                        elif lat < 0:
                            hemi_NS["South"] += 1
                        if lng > 0:
                            hemi_EW["East"] += 1
                        elif lng < 0:
                            hemi_EW["West"] += 1

        #track the max number of subdivisions
        if subdiv_count > max_count:
            max_count = subdiv_count
            max_countries = [alpha2]
        elif subdiv_count == max_count:
            max_countries.append(alpha2)
        
        #track the min number of subdivisions
        if subdiv_count < min_count:
            min_count = subdiv_count
            min_countries = [alpha2]
        elif subdiv_count == min_count:
            min_countries.append(alpha2)

    #add metadata stats to main metadata object
    iso3166_2_main_metadata_copy["total_subdivisions"] = total_subdivisions
    iso3166_2_main_metadata_copy["zero_subdivisions_total"] = zero_sub_countries
    iso3166_2_main_metadata_copy["total_attributes"] = attr_total_count
    iso3166_2_main_metadata_copy["num_unique_attributes"] = len(attr_union)
    iso3166_2_main_metadata_copy["unique_subdivision_types"] = len(type_values)
    iso3166_2_main_metadata_copy["average_subdivision_per_country"] = round(
        (total_subdivisions / total_countries) if total_countries else 0.0, 3
    )
    max_codes = ",".join(max_countries)
    iso3166_2_main_metadata_copy["max_subdivisions_country"] = f"{max_codes}:{max_count}" if max_codes else ""
    min_codes = ",".join(min_countries)
    iso3166_2_main_metadata_copy["min_subdivisions_country"] = f"{min_codes}:{min_count}" if min_codes else ""

    #map null counters into meta keys
    iso3166_2_main_metadata_copy["null_attributes_total"] = null_counts.get("null_attributes_total", 0)

    #count per hemispheres
    iso3166_2_main_metadata_copy["hemisphere_north_total"] = hemi_NS.get("North", 0)
    iso3166_2_main_metadata_copy["hemisphere_south_total"] = hemi_NS.get("South", 0)
    iso3166_2_main_metadata_copy["hemisphere_east_total"] = hemi_EW.get("East", 0)
    iso3166_2_main_metadata_copy["hemisphere_west_total"] = hemi_EW.get("West", 0)

    #calculate completeness percentages for each attribute and populate attribute_stats
    for attr_name, stats in attribute_stats.items():
        completeness_pct = round(
            (stats["populated_count"] / stats["total_count"] * 100) 
            if stats["total_count"] > 0 else 0,
            2
        )
        #add to main metadata copy
        attr_dict = {
            "total_count": stats["total_count"],
            "null_count": stats["null_count"],
            "populated_count": stats["populated_count"],
            "completeness_percent": completeness_pct
        }
        #add total_individual_count for localOtherName
        if attr_name == "localOtherName":
            attr_dict["total_individual_count"] = local_other_total_entries
        iso3166_2_main_metadata_copy["attribute_stats"][attr_name] = attr_dict

    #get JSON export name with optional timestamp
    if append_timestamp:
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
        base_filename = os.path.splitext(export_filename)[0]
        export_filename = f"{base_filename}_{timestamp}.json"
    else:
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
    parser.add_argument('-append_timestamp', '--append_timestamp', type=bool, required=False, default=False,
        help='If True, append timestamp to export filename in format {filename}_YYYY_MM_DD_HH_MM.json. Default is False.')
    
    #parse input args
    args = parser.parse_args()

    #export ISO 3166-2 data 
    export_metadata(**vars(args))