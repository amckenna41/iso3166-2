import iso3166_2 as iso
import iso3166
import os
import json
import flag
import getpass
import time
import pycountry
from tqdm import tqdm
from datetime import datetime
from operator import itemgetter
import requests
from google.cloud import storage
from flask import jsonify
import googlemaps

#initialise version 
__version__ = "1.1.0"

#initalise User-agent header for requests library 
USER_AGENT_HEADER = {'User-Agent': 'iso3166-2/{} ({}; {})'.format(__version__,
                                       'https://github.com/amckenna41/iso3166-2', getpass.getuser())}

#initialise google maps client 
gmaps = googlemaps.Client(key=os.environ["GOOGLE_MAPS_API_KEY"])

def export_iso3166_2(verbose=1):
    """
    Export the two ISO 3166-2 jsons with fields including all subdivisions related data using the pycountry
    library and all country data using the restcountries api (https://restcountries.com/). The 
    iso3166-2.json stores all country data + subdivisions data, the iso3166-2-min.json contains just 
    country name, 2 letter alpha2 code and subdivisions.

    Parameters
    ----------
    :verbose: int (default=1)
        Set to 1 to print out progress of export functionality, 0 will not print progress.

    Returns
    -------
    :latest_iso3166_2_updates: dict
        dict of all of the latest ISO 3166-2 data pulled from data sources.
    :latest_iso3166_2_min_updates: dict
        minified dict of all of the latest ISO 3166-2 data pulled from data sources.
    """
    print("Exporting ISO 3166-2 country data....")

    #get list of all 2 letter alpha2 codes
    all_alpha2 = sorted(list(iso3166.countries_by_alpha2.keys()))

    #base url for rest countries api
    base_restcountries_url = "https://restcountries.com/v3.1/alpha/"

    #base url for flag icons repo
    flag_icons_base_url = "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/"

    #objects to store all country output data
    latest_country_data = {}
    latest_country_data_min = {}

    #start counter
    start = time.time() 

    #iterate over all country codes, getting country and subdivision info, append to json objects
    for alpha2 in tqdm(all_alpha2, unit=" ", position=0, mininterval=45, miniters=10):
        
        #get rest countries api url 
        country_url = base_restcountries_url + alpha2.upper()
        
        #get country info from restcountries api
        rest_countries_response = requests.get(country_url, stream=True, headers=USER_AGENT_HEADER)
        
        #if endpoint returns a non 200 status code skip to next iteration
        if (rest_countries_response.status_code != 200):
            continue

        #kosovo not in pycountry package as it has no associated subdivisions, manually set params
        if (alpha2 == "XK"):
            countryName = "Kosovo"
            allSubdivisions = []
        else:
            #get country name and list of its subdivisions using pycountry library 
            countryName = pycountry.countries.get(alpha_2=alpha2).name
            allSubdivisions = list(pycountry.subdivisions.get(country_code=alpha2))
        
        #print out progress if verbose set to true
        if (verbose):
            print("{} ({})".format(countryName, alpha2))

        #add all country data from rest countries api response to json object
        latest_country_data[alpha2] = rest_countries_response.json()[0]
        
        #for min json object, create empty object with alpha2 as key
        latest_country_data_min[alpha2] = {}

        #create subdivisions and country name keys in json objects
        latest_country_data[alpha2]["subdivisions"] = {}
        
        sortedDict = {}

        #iterate over all countrys' subdivisions, assigning subdiv code, name, type, parent code, flag_url and each subdivisions
        # latitude and longitude, where applicable, for both objects
        for subd in allSubdivisions:
            
            #get subdivision coordinates using googlemaps api python client
            gmaps_latlng = gmaps.geocode(subd.name + ", " + countryName, region=alpha2, language="en")

            #set coordinates to None if not found using maps api
            if (gmaps_latlng != []):
                subdivision_coords = [gmaps_latlng[0]['geometry']['location']['lat'], gmaps_latlng[0]['geometry']['location']['lng']]
            else:
                subdivision_coords = None

            latest_country_data[alpha2]["subdivisions"][subd.code] = {}
            latest_country_data[alpha2]["subdivisions"][subd.code]["name"] = subd.name
            latest_country_data[alpha2]["subdivisions"][subd.code]["type"] = subd.type
            latest_country_data[alpha2]["subdivisions"][subd.code]["parent_code"] = subd.parent_code
            latest_country_data[alpha2]["subdivisions"][subd.code]["latlng"] = subdivision_coords

            latest_country_data_min[alpha2][subd.code] = {}
            latest_country_data_min[alpha2][subd.code]["name"] = subd.name
            latest_country_data_min[alpha2][subd.code]["type"] = subd.type
            latest_country_data_min[alpha2][subd.code]["parent_code"] = subd.parent_code
            latest_country_data_min[alpha2][subd.code]["latlng"] = subdivision_coords

            #list of flag file extensions in order of preference 
            flag_file_extensions = ['.svg', '.png', '.jpeg', '.jpg', '.gif']

            #iterate over all image extensions checking existence of flag in repo
            for extension in range(0, len(flag_file_extensions)):
                
                #url to flag in iso3166-flag-icons repo
                alpha2_flag_url = flag_icons_base_url + alpha2 + "/" + subd.code + flag_file_extensions[extension]
                
                #if subdivision has a valid flag in flag icons repo set to its GitHub url
                if (requests.get(alpha2_flag_url, headers=USER_AGENT_HEADER).status_code != 404):
                    latest_country_data[alpha2]["subdivisions"][subd.code]["flag_url"] = alpha2_flag_url
                    latest_country_data_min[alpha2][subd.code]["flag_url"] = alpha2_flag_url
                    break
                #if searched for flag using all possible extensions set to None in object
                elif (extension == 4):
                    latest_country_data[alpha2]["subdivisions"][subd.code]["flag_url"] = None
                    latest_country_data_min[alpha2][subd.code]["flag_url"] = None

        #sort subdivision codes in json objects in alphabetical/numerical order
        latest_country_data[alpha2]["subdivisions"] = dict(sorted(latest_country_data[alpha2]["subdivisions"].items()))
        latest_country_data_min[alpha2] = dict(sorted(latest_country_data_min[alpha2].items()))

    #stop counter and calculate elapsed time
    end = time.time()           
    elapsed = end - start
    
    if (verbose):
        print('\n##########################################################')
        print('Elapsed Time for exporting all ISO 3166-2 data: {0:.2f} minutes.'.format(elapsed / 60))

    return latest_country_data, latest_country_data_min

def check_iso3166_2_main(request):
    """
    Google Cloud Function that checks for any updates within specified date range
    for the iso3166-2 API. It uses the accompanying iso3166-2 Python
    software package to web scrape all ISO 3166 country and subdivision data from
    the various sources used by the iso3166-2 package, it then checks for any
    changes/updates to the data in the specified date range.

    If any updates are found that are not already present in the JSON object
    within the GCP Storage bucket then a GitHub Issue is automatically created in the 
    iso3166-2 repository that itself stores all the latest info and data relating to the 
    ISO 3166-2 standard. Additionally, if changes are found then the ISO 3166-2 JSON file 
    in the GCP Storage bucket is updated which is the data source for the iso3166-2 
    Python package and accompanying API.

    Parameters
    ----------
    :request : (flask.Request)
       HTTP request object.
    
    Returns
    -------
    :success_message/error_message : json
       jsonified response indicating whether the Function has completed successfully or
       an error has arose during execution.
    """
    #json object storing the error message and status code 
    error_message = {}
    error_message["status"] = 400

    #json object storing the success message and status code
    success_message = {}
    success_message["status"] = 200

    #get list of any input parameters to function
    request_json = request.get_json()

    #get current date and time on function execution
    current_datetime = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), "%Y-%m-%d")
    
    #get list of all country's 2 letter alpha-2 codes
    alpha2_codes = sorted(list(iso3166.countries_by_alpha2.keys()))

    #sort codes in alphabetical order and uppercase
    alpha2_codes.sort()
    alpha2_codes = [code.upper() for code in alpha2_codes]

    #get latest ISO 3166-2 data for both json objects
    latest_iso3166_2, latest_iso3166_2_min = export_iso3166_2()
    
    def update_json(latest_iso3166_2):
        """
        If changes have been found for any countrys in the ISO 3166-2 using the 
        check_iso3166_2_main function then the JSON in the storage bucket is 
        updated with the new JSON and the old one is stored in an archive folder 
        on the same bucket.

        Parameters
        ----------
        :latest_iso3166_2 : dict
            object with all the latest ISO 3166-2 country data using the various
            data sources from the export_iso3166_2() function.

        Returns
        -------
        :updates_found : bool
            bool to track if updates/changes have been found in ISO 3166-2 objects.
        individual_updates_json: dict
            dictionary of individual ISO 3166-2 updates that aren't in existing 
            updates object in JSON.
        """
        #initialise storage client
        storage_client = storage.Client()
        try:
            #create a bucket object for the bucket
            bucket = storage_client.get_bucket(os.environ["BUCKET_NAME"])
        except google.cloud.exceptions.NotFound:
            error_message["message"] = "Error retrieving ISO 3166-2 data json storage bucket: {}.".format(os.environ["BUCKET_NAME"])
            return jsonify(error_message), 400
        #create blob objects from the filepath for the two 
        blob = bucket.blob(os.environ["BLOB_NAME"])  
        # blob_min = bucket.blob(os.environ["BLOB_NAME_MIN"])  

        # **probs don't need to use min object, cause it derives from main object...
        #raise error if updates file not found in bucket
        if not (blob.exists()):
            raise ValueError("Error retrieving ISO 3166-2 data json: {}.".format(os.environ["BLOB_NAME"]))
        
        #download current ISO 3166-2 JSON file from storage bucket 
        current_iso3166_2_data = json.loads(blob.download_as_string(client=None))
        # current_iso3166_2_data_min = json.loads(blob_min.download_as_string(client=None))

        #set new json object to original one imported from gcp storage
        updated_json = current_iso3166_2_data
        updates_found = False

        #seperate object that holds individual updates found for ISO 3166-2 data, used in create_issue function
        individual_updates_json = {}

        #iterate over all data in object, if update/row not found in original json, pulled from GCP storage, 
        # append to new updated_json object
        for code in latest_iso3166_2:   
            individual_updates_json[code] = []
            for update in latest_iso3166_2[code]:
                if not (update in current_iso3166_2_data[code]):
                    updated_json[code].append(update)
                    updates_found = True
                    individual_updates_json[code].append(update)

            #if current alpha-2 code has no updates associated with it, remove from temp object
            if (individual_updates_json[code] == []):
                individual_updates_json.pop(code, None)

        #if updates found in new updates json compared to current one
        if (updates_found):

            #temp path for exported json
            tmp_updated_json_path = os.path.join("/tmp", os.environ["BLOB_NAME"])
            # tmp_updated_json_path_min = os.path.join("/tmp", os.environ["BLOB_NAME_MIN"])
            
            #export updated json to temp folder
            with open(tmp_updated_json_path, 'w', encoding='utf-8') as output_json:
                json.dump(latest_iso3166_2, output_json, ensure_ascii=False, indent=4)
                
            #export updated json to temp folder
            with open(tmp_updated_json_path, 'w', encoding='utf-8') as output_json:
                json.dump(latest_iso3166_2_min, output_json, ensure_ascii=False, indent=4)

            #create blob for updated JSON
            blob = bucket.blob(os.environ["BLOB_NAME"])
            # blob_min = bucket.blob(os.environ["BLOB_NAME_MIN"])

            #move current ISO 3166-2 jsons in bucket to an archive folder, append datetime to it
            archive_filepath = os.environ["ARCHIVE_FOLDER"] + "/" + os.path.splitext(os.environ["BLOB_NAME"])[0] \
                + "_" + str(current_datetime.strftime('%Y-%m-%d')) + ".json"
            # archive_filepath_min = os.path.splitext(archive_filepath)[0] + "-min.json"

            #create blob for archive updates json 
            archive_blob = bucket.blob(archive_filepath)
            
            #upload old ISO 3166-2 jsons to archive folder 
            archive_blob.upload_from_filename(tmp_updated_json_path)

            #upload new updated json using gcp sdk, replacing current updates json 
            blob.upload_from_filename(tmp_updated_json_path)

        return updates_found, individual_updates_json
        
    def create_issue(latest_iso3166_2):
        """
        Create a GitHub issue on the iso3166-2, iso3166-updates and 
        iso3166-flag-icons repository, using the GitHub api, if any updates/changes 
        are made to any entries in the ISO 3166-2. The Issue will be formatted in 
        a way to clearly outline any of the updates/changes to be made to the JSONs 
        in the iso3166-2, iso3166-updates and iso3166-flag-icons repos. 

        Parameters
        ----------
        :latest_iso3166_2 : json
           json object with all listed iso3166-2 updates after month date filter
           applied.
        :month_range : int
            number of past months updates were pulled from.

        Returns
        -------
        :message : str
            response message from GitHub api post request.

        References
        ----------
        [1]: https://developer.github.com/v3/issues/#create-an-issue
        """
        issue_json = {}
        issue_json["title"] = "ISO 3166-2 Updates: " + str(current_datetime.strftime('%Y-%m-%d')) + " (" + ', '.join(list(latest_iso3166_2)) + ")" 
        
        #body of Github Issue
        body = "# ISO 3166-2 Updates\n"

        #get total sum of updates for all countrys in json
        total_updates = sum([len(latest_iso3166_2[code]) for code in latest_iso3166_2])
        total_countries = len(latest_iso3166_2)
        
        #change body text if more than 1 country 
        if (total_countries == 1):
            body += "### " + str(total_updates) + " updates found for " + str(total_countries) + " country between the "
        else:
            body += "### " + str(total_updates) + " updates found for " + str(total_countries) + " countries between the "

        #display number of updates for countrys and the date period
        # body += "### " + str(total_updates) + " updates found for " + str(total_countries) + " countries between the " + str(month_range) + " month period of " + \
        #     str((current_datetime + relativedelta(months=-month_range)).strftime('%Y-%m-%d')) + " to " + str(current_datetime.strftime('%d-%m-%Y')) + ".\n"

        #iterate over updates in json, append to updates object
        for code in list(latest_iso3166_2.keys()):
            
            #header displaying current country name, code and flag icon using emoji-country-flag library
            body += "\n### " + "Country - " + iso3166.countries_by_alpha2[code].name + " (" + code + ") " + flag.flag(code) + ":\n"

            row_count = 0

            #iterate over all update rows for each country in object, appending to html body
            for row in latest_iso3166_2[code]:
                
                #increment row count which numbers each country's updates if more than 1
                if (len(latest_iso3166_2[code]) > 1):
                    row_count = row_count + 1
                    body += str(row_count) + ".)"

                #output all row field values 
                for key, val in row.items():
                    body += "<ins>" + str(key) + ":</ins> " + str(val) + "<br>"

        #add attributes to data json 
        issue_json["body"] = body
        issue_json["assignee"] = "amckenna41"
        issue_json["labels"] = ["iso3166-updates", "iso3166", "iso366-2", "subdivisions", "iso3166-flag-icons", str(current_datetime.strftime('%Y-%m-%d'))]

        #api url and headers
        issue_url = "https://api.github.com/repos/" + os.environ["github-owner"] + "/" + os.environ["github-repo-1"] + "/issues"
        issue_url_2 = "https://api.github.com/repos/" + os.environ["github-owner"] + "/" + os.environ["github-repo-2"] + "/issues"
        # issue_url_3 = "https://api.github.com/repos/" + os.environ["github-owner"] + "/" + os.environ["github-repo-3"] + "/issues"
        headers = {'Content-Type': "application/vnd.github+json", 
            "Authorization": "token " + os.environ["github-api-token"]}

        #make post request to github repos using api
        requests.post(issue_url, data=json.dumps(issue_json), headers=headers)
        requests.post(issue_url_2, data=json.dumps(issue_json), headers=headers)
        # requests.post(issue_url_3, data=json.dumps(issue_json), headers=headers)

    #if update object not empty (i.e there are updates), call update_json and create_issue functions
    if (latest_iso3166_2 != {}):
        updates_found, filtered_updates = update_json(latest_iso3166_2)
    if (updates_found):
        create_issue(filtered_updates)
        print("ISO 3166-2 updates found and successfully exported.")
        success_message["message"] = "ISO 3166-2 updates found and successfully exported."
    else:
        print("No ISO 3166-2 updates found.")
        success_message["message"] = "No ISO 3166-2 updates found."

    return jsonify(success_message), 200