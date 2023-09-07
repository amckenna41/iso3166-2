import iso3166
import os
import json
import flag
import getpass
import time
from collections import OrderedDict
import natsort
import pycountry
from tqdm import tqdm
from datetime import datetime
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

#json object storing the error message and status code 
error_message = {}
error_message["status"] = 400

#json object storing the success message and status code
success_message = {}
success_message["status"] = 200

#get current date and time on function execution
current_datetime = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), "%Y-%m-%d")

def check_iso3166_2_main(request):
    """
    Google Cloud Function that pulls the latest ISO 3166 from the various data
    sources, comparing against the existing ISO 3166 object for any new/missing data.
    It uses the get_iso3166_2.py script to web scrape all country's ISO 3166 data
    from the various data sources, checking for any new/missing ISO 3166 not present
    in the blob/object on GCP Storage.
    
    If any new/missing data is found that is not already present in the JSON object
    within the GCP Storage bucket then a GitHub Issue is automatically created that 
    tabulates and formats all the latest data in the iso3166-2 repository that itself 
    stores all the latest info and data relating to the ISO 3166 standard. Additionally, 
    if changes are found then the ISO 3166 JSON file in the GCP Storage bucket is updated 
    which is the data source for the iso3166-2 Python package and accompanying API.

    Parameters
    ----------
    :request : flask.Request
        Flask request object.
    
    Returns
    -------
    :success_message/error_message : json
       jsonified response indicating whether the Function has completed successfully or
       an error has arose during execution.
    """
    #initialise storage client
    storage_client = storage.Client()
    try:
        #create a bucket object for the bucket, raise error if env var not set or bucket not found
        if (os.environ.get("BUCKET_NAME") is None or os.environ.get("BUCKET_NAME") == ""):
            error_message["message"] = "Bucket name environment variable not set."
            return jsonify(error_message), 400
        bucket = storage_client.get_bucket(os.environ["BUCKET_NAME"])
    except google.cloud.exceptions.NotFound:
        error_message["message"] = "Error retrieving updates data json storage bucket: {}.".format(os.environ["BUCKET_NAME"])
        return jsonify(error_message), 400
    
    #create a blob object from the filepath, raise error if env var not set
    if (os.environ.get("BLOB_NAME") is None or os.environ.get("BLOB_NAME") == ""):
        error_message["message"] = "Blob name environment variable not set."
        return jsonify(error_message), 400
    blob = bucket.blob(os.environ["BLOB_NAME"])  
    
    #raise error if iso3166-2 file not found in bucket
    if not (blob.exists()):
        raise ValueError("Error retrieving ISO 3166 data json: {}.".format(os.environ["BLOB_NAME"]))
    
    #download current ISO 3166 JSON file from storage bucket 
    current_iso3166_2 = json.loads(blob.download_as_string(client=None))

    #get create_issue bool env var which determines if GitHub Issues are created each time new/missing ISO 3166 data is found
    if (os.environ.get("CREATE_ISSUE") is None or os.environ.get("CREATE_ISSUE") == ""):
        create_issue = True
    else:
        create_issue = os.environ["CREATE_ISSUE"]

    #parse alpha-2 country code/codes from request json
    input_alpha2 = request.args.get("ALPHA_2")

    #use all alpha-2 country codes if env var empty else use specificed alpha-2 codes
    if (input_alpha2 is None or input_alpha2 == ['']):
        #get list of all country's 2 letter alpha-2 codes
        alpha2_codes = sorted(list(iso3166.countries_by_alpha2.keys()))
    else:
        alpha2_codes = input_alpha2.replace(' ', '').split(',')

    #sort codes into alphabetical order and uppercase
    alpha2_codes.sort()
    alpha2_codes = [code.upper() for code in alpha2_codes]

    #get latest ISO 3166 data for both json objects
    latest_iso3166_2 = export_iso3166_2(alpha2_codes=alpha2_codes)
    
    #return all updates and new/missing data from newly exported latest_iso3166_2 compared with current one being used in API
    updates_found, new_iso3166_2, missing_individual_updates, previous_iso3166_updates = update_json(current_iso3166_2, latest_iso3166_2)

    #temp path for exported json
    tmp_updated_json_path = os.path.join("/tmp", os.environ["BLOB_NAME"])

    #export updated json to temp folder
    with open(tmp_updated_json_path, 'w', encoding='utf-8') as output_json:
        json.dump(new_iso3166_2, output_json, ensure_ascii=False, indent=4)

    #create blob for updated ISO 3166 JSON
    blob = bucket.blob(os.environ["BLOB_NAME"])

    #upload new updated json using gcp sdk, replacing current updates json 
    blob.upload_from_filename(tmp_updated_json_path)
    
    #if updates found, update blob object on GCP storage and create GitHub Issue outlining new data found
    if (updates_found):

        #move current ISO 3166 jsons in bucket to an archive folder, append datetime to it
        if (os.environ.get("ARCHIVE_FOLDER") is None or os.environ.get("ARCHIVE_FOLDER") == ""):
            os.environ["ARCHIVE_FOLDER"] = "archive_iso3166_2"

        #move current ISO 3166 json in bucket to an archive folder, append datetime to it
        archive_filepath = os.path.splitext(os.environ["BLOB_NAME"])[0] \
            + "_" + str(current_datetime.strftime('%Y-%m-%d')) + ".json"
        
        #export updated json to temp folder
        with open(os.path.join("/tmp", archive_filepath), 'w', encoding='utf-8') as output_json:
            json.dump(current_iso3166_2, output_json, ensure_ascii=False, indent=4)

        #create blob for archive updates json 
        archive_blob = bucket.blob(os.path.join(os.environ["ARCHIVE_FOLDER"], archive_filepath))

        #upload old ISO 3166 json to archive folder 
        archive_blob.upload_from_filename(os.path.join("/tmp", archive_filepath))

        #create GitHub Issue on relevant repositories if any new data found
        if (create_issue):
            create_github_issue(missing_individual_updates, previous_iso3166_updates)
            success_message["message"] = "New ISO 3166 data found and successfully exported to bucket and GitHub Issues created."
            print(success_message["message"])
        else:
            success_message["message"] = "New ISO 3166 data found and successfully exported to bucket."
            print(success_message["message"])
    else:
        success_message["message"] = "No new ISO 3166 updates found."
        print(success_message["message"])

    return jsonify(success_message), 200

def export_iso3166_2(alpha2_codes="", verbose=1):
    """
    Export the latest ISO 3166 data including all subdivision related data using the pycountry
    library and all country data using the restcountries api (https://restcountries.com/). Also get the
    lat/longitude info for each country and subdivision using the Google Maps API. The exported data
    is returned and used to compare against the current data object in the GCP Storage bucket. The full 
    list of attributes being exported can be viewed on the main repo in the ATTRIBUTES.md file. Code 
    taken from the same function in the get_iso3166_2.py script.

    Parameters
    ----------
    :alpha2_codes: str (default="")
        string of 1 or more 2 letter alpha-2 country codes to pull their latest ISO 3166 data.
    :verbose: int (default=1)
        Set to 1 to print out progress of export functionality, 0 will not print progress.

    Returns
    -------
    :all_country_data : dict
        object storing all exported ISO 3166 country data.
    """
    def convert_to_alpha2(alpha3_code):
        """ 
        Convert an ISO 3166 country's 3 letter alpha-3 code into its 2 letter
        alpha-2 counterpart. 

        Parameters 
        ----------
        :alpha3_code: str
            3 letter ISO 3166-1 alpha-3 country code.
        
        Returns
        -------
        :iso3166.countries_by_alpha3[alpha3_code].alpha2: str
            2 letter ISO 3166 alpha-2 country code. 
        """
        #return None if 3 letter alpha-3 code not found
        if not (alpha3_code in list(iso3166.countries_by_alpha3.keys())):
            return None
        else:
            #use iso3166 package to find corresponding alpha-2 code from its alpha-3 code
            return iso3166.countries_by_alpha3[alpha3_code].alpha2
    
    #iterate over all codes, validating they're valid, convert alpha-3 to alpha-2 if applicable
    for code in range(0, len(alpha2_codes)):

        #convert 3 letter alpha-3 code into its 2 letter alpha-2 counterpart
        if len(alpha2_codes[code]) == 3:
            alpha2_codes[code] = convert_to_alpha2(alpha2_codes[code])
        
        #raise error if invalid alpha-2 code found
        if (alpha2_codes[code] not in list(iso3166.countries_by_alpha2.keys())):
            raise ValueError("Input alpha-2 country code {} not found.".format(alpha2_codes[code]))
    
    all_alpha2 = alpha2_codes

    if (verbose):
        print("Exporting {} ISO 3166 country's data.".format(len(all_alpha2)))
        print('#####################################\n')

    #base url for rest countries api
    base_restcountries_url = "https://restcountries.com/v3.1/alpha/"

    #base url for flag icons repo
    flag_icons_base_url = "https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons/"

    #object to store all country output data
    all_country_data = {}
    
    #start counter
    start = time.time() 

    #if less than 5 input alpha-2 codes then don't display progress bar, or print elapsed time
    tqdm_disable = False
    if (len(all_alpha2) < 5):
        tqdm_disable = True

    #iterate over all country codes, getting country and subdivision info, append to json objects
    for alpha2 in tqdm(all_alpha2, disable=tqdm_disable):
        
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
            if (tqdm_disable):
                print("{} ({})".format(countryName, alpha2))
            else:
                print(" - {} ({})".format(countryName, alpha2))

        #add all country data from rest countries api response to json object
        all_country_data[alpha2] = rest_countries_response.json()[0]

        #round latitude/longitude coords to 3 d.p
        all_country_data[alpha2]["latlng"] = [round(all_country_data[alpha2]["latlng"][0], 3), round(all_country_data[alpha2]["latlng"][1], 3)]

        #round area (km^2) to nearest whole number
        all_country_data[alpha2]["area"] = int(all_country_data[alpha2]["area"])

        #create subdivisions and country name keys in json objects
        all_country_data[alpha2]["subdivisions"] = {}
        
        #iterate over all countrys' subdivisions, assigning subdiv code, name, type and parent code and flag URL, where applicable for both json objects
        for subd in allSubdivisions:
            
            #get subdivision coordinates using googlemaps api python client
            gmaps_latlng = gmaps.geocode(subd.name + ", " + countryName, region=alpha2, language="en")

            #set coordinates to None if not found using maps api, round to 3 decimal places
            if (gmaps_latlng != []):
                subdivision_coords = [round(gmaps_latlng[0]['geometry']['location']['lat'], 3), round(gmaps_latlng[0]['geometry']['location']['lng'], 3)]
            else:
                subdivision_coords = None

            all_country_data[alpha2]["subdivisions"][subd.code] = {}
            all_country_data[alpha2]["subdivisions"][subd.code]["name"] = subd.name
            all_country_data[alpha2]["subdivisions"][subd.code]["type"] = subd.type
            all_country_data[alpha2]["subdivisions"][subd.code]["parent_code"] = subd.parent_code
            all_country_data[alpha2]["subdivisions"][subd.code]["latlng"] = subdivision_coords

            #list of flag file extensions in order of preference 
            flag_file_extensions = ['.svg', '.png', '.jpeg', '.jpg', '.gif']

            #iterate over all image extensions checking existence of flag in repo
            for extension in range(0, len(flag_file_extensions)):
                
                #url to flag in iso3166-flag-icons repo
                alpha2_flag_url = flag_icons_base_url + alpha2 + "/" + subd.code + flag_file_extensions[extension]
                
                #if subdivision has a valid flag in flag icons repo set to its GitHub url, else set to None
                if (requests.get(alpha2_flag_url, headers=USER_AGENT_HEADER).status_code != 404):
                    all_country_data[alpha2]["subdivisions"][subd.code]["flag_url"] = alpha2_flag_url
                    break
                elif (extension == 4):
                    all_country_data[alpha2]["subdivisions"][subd.code]["flag_url"] = None

        #sort subdivision codes in json objects in natural alphabetical/numerical order using natsort library
        all_country_data[alpha2]["subdivisions"] = dict(OrderedDict(natsort.natsorted(all_country_data[alpha2]["subdivisions"].items())))
    
        #sort keys in main output dict into alphabetical order
        all_country_data[alpha2] = {key: value for key, value in sorted(all_country_data[alpha2].items())}

    #stop counter and calculate elapsed time
    end = time.time()           
    elapsed = end - start
    
    if (verbose and not tqdm_disable):
        print('\n##########################################################')
        print('Elapsed Time for exporting all ISO 3166 data: {0:.2f} minutes.'.format(elapsed / 60))
        
    return all_country_data

def update_json(current_iso3166_2, latest_iso3166_2):
    """
    Iterate through the latest ISO 3166 data exported using the export_iso3166_2
    function. Add any new/missing changes found to the updated_json object that
    aren't in the current JSON object currently being used by the iso3166-2 API.
    Also keep track of the individual new/missing updates found per country and 
    their previous values, to be used in the create_github_issue() function when 
    communicating the latest updates.

    Parameters
    ----------
    :current_iso3166_2 : dict
        object with all the current ISO 3166 data that is currently used in the 
        software and API.
    :latest_iso3166_2 : dict
        object with all the latest ISO 3166 country data using the various
        data sources from the export_iso3166_2() function.

    Returns
    -------
    :updates_found : bool
        bool to track if updates/changes have been found in ISO 3166 objects.
    :updated_json : dict 
        object of all the up-to-date ISO 3166 data including any new/missing
        data found.
    :individual_updates_json : dict
        dictionary of individual ISO 3166 updates that aren't in existing 
        updates object in JSON.
    :previous_iso3166_2_updates : dict
        if new/missing data are found for a particular attribute, it's previous
        values are stored in this object and returned, to be used in the 
        create_github_issue() function.
    """
    #set new json object to original one imported from gcp storage
    updated_json = current_iso3166_2
    updates_found = False

    #seperate object that holds individual updates found for ISO 3166 data, used in create_issue function
    individual_iso3166_2_updates = {}
    
    #object to keep track of previous attribute values if new value found for them
    previous_iso3166_2_updates = {}

    #iterate over all data in object, if row not found in original json, pulled from GCP storage, 
    # append to new updated_json object
    for code in latest_iso3166_2:   
        individual_iso3166_2_updates[code] = {}
        previous_iso3166_2_updates[code] = {}
        for update in latest_iso3166_2[code]:

            #if key/attribute not found in existing object then add to new ISO 3166 object with correct value, if applicable
            if not (update in current_iso3166_2[code]):
                updated_json[code][update] = latest_iso3166_2[code][update]
                individual_iso3166_2_updates[code][update] = latest_iso3166_2[code][update]
                previous_iso3166_2_updates[code][update] = "No listed value"
                updates_found = True
            
            #update new ISO 3166 object with the new value present in latest data from export function, if applicable
            if (latest_iso3166_2[code][update] != current_iso3166_2[code][update]):
                updated_json[code][update] = latest_iso3166_2[code][update]
                individual_iso3166_2_updates[code][update] = latest_iso3166_2[code][update]
                previous_iso3166_2_updates[code][update] = current_iso3166_2[code][update]
                updates_found = True

        #if current alpha-2 code has no updates associated with it, remove from individual_iso3166_2_updates object
        if (individual_iso3166_2_updates[code] == {}):
            individual_iso3166_2_updates.pop(code, None)
    
        #if current alpha-2 code has no updates associated with it, remove from previous_iso3166_2_updates object
        if (previous_iso3166_2_updates[code] == {}):
            previous_iso3166_2_updates.pop(code, None)

    #sort object keys into natural order using natsort
    updated_json = dict(OrderedDict(natsort.natsorted(updated_json.items())))
    individual_iso3166_2_updates = dict(OrderedDict(natsort.natsorted(individual_iso3166_2_updates.items())))
    previous_iso3166_2_updates = dict(OrderedDict(natsort.natsorted(previous_iso3166_2_updates.items())))

    return updates_found, updated_json, individual_iso3166_2_updates, previous_iso3166_2_updates

def create_github_issue(individual_iso3166_2_updates, previous_iso3166_updates):
    """
    Create a GitHub issue on the repositories specified by the GITHUB_REPOS env var,
    using the GitHub api, if any updates/changes were found in the ISO 3166 that aren't 
    in the current object. The Issue will be formatted and tabulated in a way to 
    clearly outline any of the updates/changes to be made to the JSONs.

    Parameters
    ----------
    :individual_iso3166_2_updates : dict
        object of all the new/missing individual country data found from the 
        update_json() function.
    :previous_iso3166_updates : dict
        if new/missing data are found for a particular attribute, it's previous
        values are stored in this object and returned, to be used in the 
        create_github_issue() function.

    Returns
    -------
    None

    References
    ----------
    [1]: https://developer.github.com/v3/issues/#create-an-issue
    """
    issue_json = {}
    issue_json["title"] = "ISO 3166 Data: " + str(current_datetime.strftime('%Y-%m-%d')) + " (" + \
        ', '.join(list(individual_iso3166_2_updates.keys()))+ ")"

    #body of GitHub Issue
    body = "# ISO 3166 Data Updates\n"

    #get total sum of updates for all countrys in json
    total_country_updates = sum([len(individual_iso3166_2_updates[code]) for code in individual_iso3166_2_updates])
    total_missing_updates = len(individual_iso3166_2_updates)

    #append any updates data to body
    if (total_country_updates != 0):

        #display number of updates for countrys and the date period
        body += "<h2>" + str(total_country_updates) + " missing update(s) found for " + str(total_missing_updates) + " country/countries</h2>"

        #iterate over updates in json, append to updates object
        for code in list(individual_iso3166_2_updates.keys()):
            
            #header displaying current country name, code and flag icon using emoji-country-flag library
            body += "<h3>" + iso3166.countries_by_alpha2[code].name + " (" + code + ") " + flag.flag(code) + ":</h3>"

            #create table element to store output data, including each attribute name, its new value and its previous value
            body += "<table><tr><th>Attribute</th><th>Value Before</th><th>Value After</th></tr>"

            #iterate over all update rows for each country in object, appending to table row 
            for key, val in individual_iso3166_2_updates[code].items():

                temp_previous_value = previous_iso3166_updates[code][key]
                body += "<tr>"
                
                #if value in object is not of type string then convert to string
                if (isinstance(val, list)):
                    val = ''.join(val)
                if (isinstance(val, dict) or isinstance(val, bool) or isinstance(val, int) or isinstance(val, float)):
                    val = str(val)
                if (isinstance(previous_iso3166_updates[code][key], list)):
                    temp_previous_value = ''.join(previous_iso3166_updates[code][key])
                if (isinstance(previous_iso3166_updates[code][key], dict) or isinstance(previous_iso3166_updates[code][key], bool) \
                    or isinstance(previous_iso3166_updates[code][key], int) or isinstance(previous_iso3166_updates[code][key], float)):
                    temp_previous_value = str(previous_iso3166_updates[code][key])
                
                body += "<td>" + key + "</td><td>" + temp_previous_value + "</td><td>" + val + "</td>"
                body += "</tr>"
    
            #close table element 
            body += "</table>"

    #add attributes to data json 
    issue_json["body"] = body
    issue_json["assignee"] = "amckenna41"
    issue_json["labels"] = ["iso3166-updates", "iso", "iso3166", "iso366-2", "subdivisions", "iso3166-flag-icons", str(current_datetime.strftime('%Y-%m-%d'))]

    #raise error if GitHub related env vars not set
    if (os.environ.get("GITHUB_OWNER") is None or os.environ.get("GITHUB_OWNER") == "" or \
        os.environ.get("GITHUB_API_TOKEN") is None or os.environ.get("GITHUB_API_TOKEN") == ""):
        error_message["message"] = "GitHub owner name and or API token environment variables not set."
        return jsonify(error_message), 400
    
    #http request headers for GitHub API
    headers = {'Content-Type': "application/vnd.github+json", 
        "Authorization": "token " + os.environ["GITHUB_API_TOKEN"]}
    github_repos = os.environ.get("GITHUB_REPOS")
    
    #make post request to create issue in repos using GitHub api url and headers, if github_repo env vars set
    if not (github_repos is None and github_repos != ""): 
        #split into list of repos 
        github_repos = github_repos.replace(' ', '').split(',')

        #iterate over each repo listed in env var, making post request with issue_json data 
        for repo in github_repos:
            
            issue_url = "https://api.github.com/repos/" + os.environ["GITHUB_OWNER"] + "/" + repo + "/issues"
            github_request = requests.post(issue_url, data=json.dumps(issue_json), headers=headers)    

            #print error message if success status code not returned            
            if (github_request.status_code != 200):  
                if (github_request.status_code == 401):
                    print("Authorisation issue when creating GitHub Issue in repository {}, could be an issue with the GitHub PAT.".format(repo))
                else:
                    print("Issue when creating GitHub Issue in repository {}, got status code {}.".format(repo, github_request.status_code))   