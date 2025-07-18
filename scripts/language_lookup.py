import pandas as pd
import os
import re
import json
from thefuzz import process, fuzz
from fake_useragent import UserAgent
from unidecode import unidecode
from urllib.parse import unquote_plus
import pycountry
import requests
from bs4 import BeautifulSoup
try:
    from utils import *
except:
    from scripts.utils import *

class LanguageLookup:
    """
    The Language class is used for generating the language lookup table which contains useful info about the languages
    for each subdivision's local/other name in the local_other_names.csv dataset. The exported table has the following
    attributes:

    - name: official language name 
    - scope: the linguistic breadth or classification level the language represents and how broadly or narrowly the 
        code applies within the hierarchy of human languages. Its categories are Individual, Macrolanguage, Dialect,
        Collective, Family and Level 1 Language. 
    - type: describes the status or temporal nature of the language and reflects the vitality or origin of the language. 
        Its categories include Living, Extinct, Ancient, Historical and Constructed.
    - source: source URL for the language data/database.
    - countries: list of country codes that the individual language code features in in the local/other names dataset. 
        Not that this list is only if the language features in the local/other name attribute and not the name attribute,
        e.g for Danish (dan), DK will not be included in countries because although its "name" is in Danish, there are
        no local/other names in Danish.
    - total: total count of individual subdivisions that the language code features in.
    
    The class also encapsulates additional specific functionality, including fetching language details, storing language 
    exception data, searching languages via their language name or country name and adding/deleting a language to the lookup.

    Parameters
    ========== 
    :imported_file_name: str (default=None)
        name of csv file name with local/other subdivision names. This can be left blank if the lookup table is already
        exported, but the filename should be passed in before this.
    :language_lookup_filename: str (default="language_lookup")
        name of exported language lookup file.

    Methods
    =======
    export_language_lookup(export_filename: str="", export: bool=True):
        export full language lookup table to class and or jsons/csv/markdown.
    export_language_data(language_code: str):
        export the name, scope and type for a given language code.
    search_language_lookup(language_name: str, likeness_score: int=100):
        search for specific language object via its name. The likeness score can be amended to bring back multiple
        language results and expand the search space.
    filter_by_scope(scope):
        filter language dataset by scope.
    filter_by_type(type):
        filter language dataset by type.
    get_country_language_data(country_code: str):
        get the language data per country via its input country code.
    add_language_code(new_language_object: dict={}, code: str="", name: str="", scope: str="", type_: str="", countries: str=None, total: int=0, source: str=None, export=True):
        add custom language object to lookup table.
    delete_language_code(code: str="", export: bool=True):
        delete language object from lookup table.
    export_language_source():
        export the source URL(s) for the inputted language code.
    get_iso_639_urls():
        get the URL for the ISO 639-2 or ISO 639-3 language codes.
    __getitem__(code):
        get language code from object instance using its language code.
    __len__():
        get total number of language codes in object.
    __repr__():
        get object representation of instance.
    __str__():
        get string representation of instance. 
    """
    def __init__(self, imported_file_name: str=None, language_lookup_filename: str="language_lookup"):
        self.imported_file_name = imported_file_name if imported_file_name else os.path.join("iso3166_2_resources", "local_other_names.csv")
        self.language_lookup_filename = os.path.splitext(language_lookup_filename)[0]
        self.all_language_data = {} 

        #read in json or csv of language data if already exported, json takes priority
        if (os.path.isfile(self.language_lookup_filename + ".json")):
            with open(self.language_lookup_filename + ".json", 'r') as fp:
                self.all_language_data = json.load(fp) 
    
        elif (os.path.isfile(self.language_lookup_filename + ".csv")):
            self.all_language_data = pd.read_csv(self.language_lookup_filename + ".csv")
            self.all_language_data = self.all_language_data.set_index("code").to_dict(orient="index")

        #initialise object to store language sources
        self.iso_639_language_source_urls = {}  

        '''
        The below object is a dict of language codes that aren't available in the ISO 639 list of languages. These are usually small 
        sub-regional languages or dialects that aren't added to the ISO 639 list as of yet. Primarily the language codes are from the 
        Glottlog database of languages, a database that provides information about the world's languages, dialects, and linguistic families.
        But there are several instances of codes from the IETF language tags and Linguist database. 

        In the object, category is similar to scope in the normal ISO 639 database, representing the general classification or 
        nature of the language. The available categories are A (artificial language), D (dialect), F (family), L1 (level 1 language).
        Type represents status or nature of the language, the available types are C (constructed language) and L (living).
        '''
        self.language_exceptions = {
            "algh1238": {"name": "Algherese Catalan", "category": "D", "type": "L", "source": "https://glottolog.org/resource/languoid/id/algh1238"},
            "berr1239": {"name": "Berrichon", "category": "D", "type": "L", "source": "https://glottolog.org/resource/languoid/id/berr1239"},
            "bunj1247": {"name": "Bunjevac", "category": "D", "type": "L", "source": "https://glottolog.org/resource/languoid/id/bunj1247"},
            "brab1243": {"name": "Brabantian", "category": "D", "type": "L", "source": "https://glottolog.org/resource/languoid/id/brab1243"},
            "cang1245": {"name": "Cangin", "category": "F", "type": "L", "source": "https://glottolog.org/resource/languoid/id/cang1245"},
            "chao1238": {"name": "Teochew Min", "category": "D", "type": "L", "source": "https://glottolog.org/resource/languoid/id/chao1238"},
            "cico1238": {"name": "Cicolano-Reatino-Aquilano", "category": "D", "type": "L", "source": "https://glottolog.org/resource/languoid/id/cico1238"},
            "de-at": {"name": "Austrian German", "category": "D", "type": "L", "source": "https://support.elucidat.com/hc/en-us/articles/6068623875217-IETF-language-tags"},
            "east2276": {"name": "Eastern Lombard", "category": "D", "type": "L", "source": "https://glottolog.org/resource/languoid/id/east2276"},
            "fuzh1239": {"name": "Houguan", "category": "D", "type": "L", "source": "https://glottolog.org/resource/languoid/id/fuzh1239"},
            "gall1275": {"name": "Gallo", "category": "D", "type": "L", "source": "https://glottolog.org/resource/languoid/id/gall1275"},
            "high1290": {"name": "High Alemannic", "category": "D", "type": "L", "source": "https://glottolog.org/resource/languoid/id/high1290"},
            "79-aaa-gap": {"name": "Taiwanese Hakka", "category": "D", "type": "L", "source": "http://www.hortensj-garden.org/index.php?tnc=1&tr=lsr&nid=79-aaa-gap"},
            "ita-tus": {"name": "Tuscan", "category": "D", "type": "L", "source": "https://web.archive.org/web/20221015065035/http://multitree.org/codes/ita-tus"},  
            "juri1235": {"name": "YurÃƒÂ­", "category": "L1", "type": "L", "source": "https://glottolog.org/resource/languoid/id/juri1235"},
            "mila1243": {"name": "Milanese", "category": "D", "type": "L", "source": "https://glottolog.org/resource/languoid/id/mila1243"},
            "mone1238": {"name": "Milanese", "category": "D", "type": "L", "source": "https://glottolog.org/resource/languoid/id/mone1238"},
            "pera1260": {"name": "Perak Malay", "category": "D", "type": "L", "source": "https://glottolog.org/resource/languoid/id/pera1260"},
            "pala1356": {"name": "Palawa Kani", "category": "A", "type": "C", "source": "https://glottolog.org/resource/languoid/id/pala1356"},
            "poit1240-sant1407": {"name": "PoitevinÃ¢â‚¬â€œSaintongeais", "category": "D", "type": "L", "source": "https://glottolog.org/resource/languoid/id/poit1240, https://glottolog.org/resource/languoid/id/sant1407"},
            "sant1407": {"name": "Saintongeais", "category": "D", "type": "L", "source": "https://glottolog.org/resource/languoid/id/sant1407"},
            "resi1246": {"name": "Resia", "category": "D", "type": "L", "source": "https://glottolog.org/resource/languoid/id/resi1246"},
            "mori1267": {"name": "Moriori", "category": "L1", "type": "L", "source": "https://glottolog.org/resource/languoid/id/mori1267"},
            "sama1302": {"name": "Sama-Bajaw", "category": "F", "type": "L", "source": "https://glottolog.org/resource/languoid/id/sama1302"},
            "soth1248": {"name": "Sotho-Tswana", "category": "F", "type": "L", "source": "https://glottolog.org/resource/languoid/id/soth1248"},
            "suba1253": {"name": "Subanen", "category": "F", "type": "L", "source": "https://glottolog.org/resource/languoid/id/suba1253"},
            "taib1240": {"name": "Taiwanese Mandarin", "category": "D", "type": "L", "source": "https://glottolog.org/resource/languoid/id/taib1240"},
            "taib1242": {"name": "Taiwanese Hokkien", "category": "D", "type": "L", "source": "https://glottolog.org/resource/languoid/id/taib1242"},
            "ulst1239": {"name": "Ulster Scots", "category": "D", "type": "L", "source": "https://glottolog.org/resource/languoid/id/ulst1239"},
            "west2343": {"name": "Western Lombard", "category": "D", "type": "L", "source": "https://glottolog.org/resource/languoid/id/west2343"},
            "paha1256": {"name": "Pahang Malay", "category": "D", "type": "L", "source": "https://glottolog.org/resource/languoid/id/paha1256"}
            }

        #add language exceptions to main language object
        # self.all_language_data.update(self.language_exceptions)
    
        #object of all language codes and their data
        self.all_language_codes = list(self.all_language_data.keys())

    def export_language_lookup(self, export_filename: str="", export: bool=True, input_language_code: str="") -> None:
        """
        Export a language lookup table for the 400+ languages listed in the other/local 
        names attribute for the thousands of subdivisions in the dataset. The lookup table 
        will have the language code, its name, type, scope and the countries/subdivisions 
        that the language is present in. 

        Parameters
        ==========
        :export_filename: str (default="")
            filename for language lookup table export. If no value input then 
            the value of the class attribute self.language_lookup_filename will
            be used. 
        :export: bool (default=True): 
            whether to export the language lookup table or just encapsulate in the class instance.
        :input_language_code: str (default="")
            custom language code/list of codes to export to the export filename. 
            By default it'll be empty meaning all language codes from the localOtherNames.csv
            will be exported. Mainly created for testing individual language code exports.

        Returns
        =======
        None

        Raises
        ======
        ValueError:
            Local/other name entry missing corresponding language code.
        """
        #if export filename parameter empty (by default), set its value to the class attribute
        if (export_filename == ""):
            export_filename = self.language_lookup_filename
        
        #import csv with local/other subdivision names
        local_other_name_csv = pd.read_csv(self.imported_file_name, keep_default_na=False)
        
        #exported dict of language code and name/scope/type etc   
        language_lookup_dict = {}

        #object of all ISO 639 source URLs, call function if empty object
        if (self.iso_639_language_source_urls == {}):
            self.iso_639_language_source_urls = self.get_iso_639_urls()
        
        #iterate over all subdivision rows in local_other_names.csv
        for index, row in local_other_name_csv.iterrows():

            #skip row if no value for local/other name
            if (row is None):
                continue

            #preserve any items in the list of local/other names that are surrounded by quotes 
            local_other_names_split = split_preserving_quotes(row['localOtherName'])

            #iterate over each name, get its bracketed language code and create language code object for it
            for name in local_other_names_split:
                #parse the language code from the brackets
                match = re.match(r'(.+?)\((.+?)\)', name.strip())

                #raise error if local/other name doesn't have language code in brackets
                if not match:
                    raise ValueError(f"Each local/other name entry should have the corresponding language code in brackets:\n{row}")

                #get language code from regex
                language_code = match.group(2).strip()

                #if custom language code, skip current language that it's not equal to 
                if (input_language_code != "" and input_language_code != language_code):
                    continue

                #if language code and data already in object, just append the current country code to the attribute and increment the total counter
                if (language_code in language_lookup_dict):
                        
                    #append country code if not already present in attribute, increment total counter
                    if row["alphaCode"] not in language_lookup_dict[language_code]["countries"]:
                        language_lookup_dict[language_code]["countries"] += ("," + row["alphaCode"])
                    language_lookup_dict[language_code]["total"] += 1 

                #create new entry for language code in object 
                else:
                    language_lookup_dict[language_code] = {}
                    language_name_scope_type = self.export_language_data(language_code)
                    language_lookup_dict[language_code]["name"] = re.sub(r"[\(\[\{].*?[\)\]\}]", "", language_name_scope_type["name"]).strip()
                    language_lookup_dict[language_code]["scope"] = language_name_scope_type["scope"]
                    language_lookup_dict[language_code]["type"] = language_name_scope_type["type"]
                    language_lookup_dict[language_code]["countries"] = row["alphaCode"]
                    language_lookup_dict[language_code]["total"] = 1
                    language_lookup_dict[language_code]["source"] = self.export_language_source(language_code)
    
        #output object column order
        column_order = ["code", "name", "scope", "type", "countries", "total", "source"]


        #convert language dict to dataframe, reset index, reorder columns and sort by language code
        language_lookup_df = pd.DataFrame.from_dict(language_lookup_dict, orient='index').reset_index()
        language_lookup_df.rename(columns={'index': 'code'}, inplace=True)
        language_lookup_df = language_lookup_df.sort_values(by='code', ascending=True)
        # language_lookup_df = language_lookup_df.reindex(sorted(column_order), axis=1)

        #order dict's language codes alphabetically 
        language_lookup_dict = dict(sorted(language_lookup_dict.items()))

        #remove extension from file export name, if applicable 
        export_filename = os.path.splitext(export_filename)[0]

        #export language lookup data to json, markdown and csv
        if (export):
            #convert object to markdown
            language_lookup_markdown = language_lookup_df.to_markdown(index=False)

            #export to the various formats (json, md & csv)
            with open(export_filename + ".json", 'w') as fp:
                json.dump(language_lookup_dict, fp, indent=4)
            with open(export_filename + '.md', 'w') as f:
                f.write(language_lookup_markdown)
            language_lookup_df.to_csv(export_filename + ".csv", columns=column_order, index=False)

        #set class attribute to df of all language data 
        self.all_language_data = language_lookup_dict

    def export_language_data(self, code: str) -> dict:
        """
        Get the name, scope and type/category for input language code.

        Parameters
        ==========
        :code: str
            language code.

        Returns
        =======
        :language_data: dict
            object of language name, scope and type.

        Raises
        ======
        TypeError:
            Language code input parameter is not of correct data type.
        ValueError:
            Language code input parameter not found in list of available language codes.
        """
        #raise error if input code isn't a string
        if not (isinstance(code, str)):
            raise TypeError(f"Expected input language code to be a string, got {type(code)}.")

        #objects for converting letter representations of scope and type into their full name form
        scope_conversion = {"A": "Artificial", "C": "Collective", "D": "Dialect", "F": "Family", "I": "Individual", "L1": "Level 1 Language", "M": "Macrolanguage", "S": "Special"}
        type_conversion = {"A": "Ancient", "C": "Constructed", "E": "Extinct", "H": "Historical", "L": "Living"}

        #lowercase language code
        code = code.lower()

        #get language object for inputted code from pycountry package
        language = pycountry.languages.get(alpha_2=code) or pycountry.languages.get(alpha_3=code)

        # get the language source for the language code
        # source = self.export_language_source(code) 
        
        #extract name, scope and type from pycountry language object
        if (language):        
            scope_code = getattr(language, "scope", None)
            type_code = getattr(language, "type", None)
            return {"name": language.name, "scope": scope_conversion.get(scope_code, ""), "type": type_conversion.get(type_code, "")}

        #if language object not found, look for the same code within the language family part of the package 
        language_family = pycountry.language_families.get(alpha_3=code)

        #if language family object found, return its data
        if (language_family):
            return {"name": language_family.name, "scope": "Collective" if not hasattr(language_family, "scope") else language_family.scope, "type": "Living" if not hasattr(language_family, "type") else language_family.type}
        
        #if language or language family not found, search through object of language exceptions and return its data, otherwise raise an error 
        if (code in self.language_exceptions):
            return {"name": self.language_exceptions[code]["name"], "scope": scope_conversion[self.language_exceptions[code]["category"]], "type": type_conversion[self.language_exceptions[code]["type"]]}
        else:
            raise ValueError(f"Language code {code} not found in ISO 639, Glottolog or other databases for subdivision.")

    def search_language_lookup(self, language_name: str, likeness_score: int=100) -> dict:
        """ 
        Get the language object by searching via its name. By default the function looks 
        for an exact matching language name (likeness score=100), but the likeness score 
        can be reduced to return multiple language matches and increase the search space, 
        if applicable. 
        
        Parameters
        ==========
        :language_name: str
            name of language to search for.
        :likeness_score: float/int (default=1)
            percentage of likeness list of languages have to be to input 
            name, 100 being an exact match and 50 being a 50% likeness etc. 
            By default a score of 100 is used meaning only exact language name
            matches are returned.

        Returns
        =======
        :output_languages: dict/list
            object of sought language data. Can also return a list of multiple matching 
            language objects.
        
        Raises
        ======
        TypeError:
            Language name input parameter is not of correct data type.
        ValueError:
            The language lookup data should be exported before searching.
        """
        #raise error if name parameter isn't a string
        if not (isinstance(language_name, str)):
            raise TypeError(f"Input subdivision name should be of type str, got {type(language_name)}.")

        #set likeness value to 100 if invalid or out of range value input
        if not (1 < likeness_score < 100):
            likeness_score = 100

        #object to store the subdivision name and its corresponding language code (name: code)
        all_language_names = {}

        #list to store all language names
        all_language_names_list = []
        
        #raise error if language data hasn't been exported into object yet
        if (self.all_language_data == {}):
            raise ValueError("Language lookup files not available or haven't been exported, run the export_language_lookup function.")

        #iterate over all language data, appending to a list of language names, also create a dict of language names and their codes
        for language in self.all_language_data:
            if not (unidecode(self.all_language_data[language]["name"].lower().replace(' ', '')) in list(all_language_names.keys())):
                all_language_names[unidecode(unquote_plus(self.all_language_data[language]["name"]).lower().replace(' ', ''))]  = []
                all_language_names[unidecode(unquote_plus(self.all_language_data[language]["name"]).lower().replace(' ', ''))].append({"name": self.all_language_data[language]["name"], "code": language})
            else:
                all_language_names[unidecode(unquote_plus(self.all_language_data[language]["name"]).lower().replace(' ', ''))].append({"name": self.all_language_data[language]["name"], "code": language})
            all_language_names_list.append(unidecode(unquote_plus(self.all_language_data[language]["name"]).lower().replace(' ', '')))

        #remove any unicode, quotes or whitespace from name, lowercase 
        language_name = unidecode(unquote_plus(language_name)).replace(' ', '').lower()

        #sort all language names' codes
        language_names = sorted([language_name])
        
        #split multiple language names into list
        language_names = language_names[0].split(',')

        #object to keep track of matching language objects and their data
        output_languages =  {}

        #iterate over all input language names, and find matching language object
        for lang in language_names: 
            
            #using thefuzz library, get all language objects that match the input language names
            all_language_name_matches = process.extract(lang, all_language_names_list, scorer=fuzz.ratio) #partial_ratio
            name_matches = []

            #iterate over all found language name matches, look for exact matches, if none found then look for ones that have likeness score>=80
            for match in all_language_name_matches:
                #use default likeness score of 100 (exact) followed by 80 if no exact matches found
                if (likeness_score == 100):
                    if (match[1] == 100):
                        name_matches.append(match[0])
                    elif (match[1] >= 80):
                        name_matches.append(match[0])
                else:
                    if (match[1] >= likeness_score):
                        name_matches.append(match[0])

            #iterate over all language name matches and get corresponding language object from dataset
            for lan in range(0, len(name_matches)): 
                for obj in range(0, len(all_language_names[name_matches[lan]])):
                    #create temp object for language and its data attributes, with its language code as key
                    language = self.all_language_data[all_language_names[name_matches[lan]][obj]["code"]]
                    #append language data and its attributes to the output object
                    output_languages[all_language_names[name_matches[lan]][obj]["code"]] = language

        return output_languages            

    def filter_by_scope(self, scope: str) -> dict:
        """ Filter language data by language scope. """
        return {k: v for k, v in self.all_language_data.items() if v["scope"].lower() == scope.lower()}

    def filter_by_type(self, type: str) -> dict:
        """ Filter language data by language type. """
        return {k: v for k, v in self.all_language_data.items() if v["type"].lower() == type.lower()}
    
    def get_country_language_data(self, country_code: str) -> dict:
        """ 
        Return list of language objects that feature the input country
        code in the "countries" attribute, which means that the language
        object features within the local/other name attribute of one of 
        these country's subdivisions. The input code can be the ISO 3166 
        2 letter or 3 letter alpha-2 and alpha-3 or the numeric codes.
        
        Parameters
        ==========
        :country_code: str
            str or list of 1 or more ISO 3166 alpha-2, alpha-3 or numeric country
            codes to get language data for.

        Returns
        ======= 
        :country_language_data: dict
            object of language data per country.
        
        Raises
        ======
        TypeError:
            Country code input parameter is not of correct data type.
        ValueError:
            Invalid alpha-2 country code.
        """
        #raise error if country code input is not string
        if not (isinstance(country_code, str)):
            raise TypeError(f"Invalid data type for country code input parameter: {type(country_code)}.")
        
        #split and convert each code into its applicable alpha-2, ignoring whitespace, raise error if invalid code
        input_codes = [code.strip() for code in country_code.split(",")]
        try:
            valid_language_codes = {convert_to_alpha2(code) for code in input_codes}
        except ValueError as e:
            raise ValueError(f"One or more invalid country codes: {e}")
        
        #object storing list of languages with input country code
        country_language_data = {}

        #iterate over each language data row, searching for those with inputted country codes, add to object
        for code, language in self.all_language_data.items():
            language_countries = set(language["countries"].split(","))
            if valid_language_codes & language_countries: 
                country_language_data[code] = language
            
        return country_language_data

    def add_language_code(self, new_language_object: dict={}, code: str="", name: str="", scope: str="", type_: str="", 
                          countries: str="", total: int=0, source: str="", export: bool=True) -> None:
        """ 
        Add a custom language object to the language lookup table. The function
        can accept a dict of the attributes and their values, any missing attributes
        will be set to "". You can also pass in the individual attributes via their 
        function parameters. For both ways of inputting to the object, the language 
        code and name are required, all other attributes are optional. The object will 
        be added to the self.all_language_data attribute and exported to the same lookup 
        table file. The language code will also be added to the all_language_codes class
        variable. 

        Note that adding a custom language code/object to the lookup table will make your 
        version out of sync with the original. Run the delete_language_code function to 
        remove any added custom languages.

        Parameters
        ==========
        :new_language_object: dict (default={})
            dict of new language object to add to lookup table.
        :code: str (default="")
            language code.
        :name: str (default="")
            language name.
        :scope: str (default="")
            language scope.
        :type_: str (default="")
            language type.
        :countries: str/list (default="")
            list of alpha-2 country codes that the language features in.
        :total: int (default=0)
            total number of subdivisions that the language features in.
        :source: str (default="")
            source for language, if applicable. 
        :export: bool (default=True)
            export the language object with the new code to the json, csv and & md files.

        Returns
        =======
        None

        Raises
        ======
        ValueError:
            Language code and name parameters are required and can't be empty.
            Language code input already present in the language lookup object.
        """
        #if full object of new language object, parse and add the full object to lookup else get language data from individual parameters
        if new_language_object:
            
            #get individual attributes from language object
            code = new_language_object.get("code", code) or ""
            name = new_language_object.get("name", name) or ""
            scope = new_language_object.get("scope", scope)
            type_ = new_language_object.get("type", type_)
            countries = new_language_object.get("countries", countries)
            total = new_language_object.get("total", total)
            source = new_language_object.get("source", source)
        else:
            #set code and name parameters
            code = code or ""
            name = name or ""

        #raise error if code or name attributes not in input parameters
        if (code == "" or name == ""):
            raise ValueError("Language code and name parameters are required and can't be empty.")

        #raise type error if input language code and name aren't strings
        if (not isinstance(code, str) or not isinstance(name, str)):
            raise TypeError("Language code and name must both be a string.")

        #lowercase language code
        code = code.lower()
        
        #raise error if language code already in object
        if (code in list(self.all_language_data)):
            raise ValueError(f"Language code {code} already present in language object.")
        
        #add language object to main language lookup
        self.all_language_data[code.lower()] = {"name": name, "scope": scope, "type": type_, "countries": countries, "total": total, "source": source}

        #append new code to object of all language codes
        self.all_language_codes.append(code)

        print(f"Adding language code {code} to Language Lookup table:\n{self.all_language_data[code]}.")

        #export new language to files 
        if (export):
            #export updated language object to json, csv and markdown
            with open(self.language_lookup_filename + ".json", "w") as file:
                json.dump(self.all_language_data, file, indent=4) 
            pd.DataFrame.from_dict(self.all_language_data, orient='index').to_csv(self.language_lookup_filename + ".csv", index=False)

            #set language code as index for CSV output
            self.all_language_data = self.all_language_data.set_index("code").to_dict(orient="index")

            #convert language dict to dataframe, reset index, reorder columns and sort by language code
            language_lookup_df = pd.DataFrame.from_dict(self.all_language_data, orient='index').reset_index()
            language_lookup_df.rename(columns={'index': 'code'}, inplace=True)
            language_lookup_df = language_lookup_df.sort_values(by='code', ascending=True)
            language_lookup_dict = dict(sorted(language_lookup_dict.items()))

            #convert object to markdown
            language_lookup_markdown = language_lookup_df.to_markdown(index=False)
            with open(self.language_lookup_filename + '.md', 'w') as f:
                f.write(language_lookup_markdown)

    def delete_language_code(self, code: str="", export: bool=True) -> None:
        """ 
        Delete a previously added custom language object or an already existing one
        from the language lookup table. Only the language code is required for 
        input. The object will be deleted from the self.all_language_data attribute 
        and exported to the same lookup table file (if the export bool is set to True).
        The language code will also be removed from the all_language_codes var.
        
        Note that deleting an already existing language code/object from the lookup 
        table will make your version out of sync with the original. 

        Parameters
        ==========
        :code: str (default="")
            language code.
        :export: bool (default=True)
            export the language object with the removed code to the json, csv and & md files.

        Returns
        =======
        None

        Raises
        ======
        ValueError:
            Language code parameter required and can't be empty.
            Language code not present in lookup table.
        """
        #language code must be a non-empty string
        if not code or not isinstance(code, str):
            raise ValueError("Language code must be a non-empty string.")
        
        #lowercase language code
        code = code.lower()

        #input language code not found in lookup table data
        if (code not in self.all_language_data):
            raise ValueError(f"Language code '{code}' not found in language lookup.")

        print(f"Deleting language code {code} from Language Lookup table:\n{self.all_language_data[code]}.")

        #delete the object from lookup table & language code list var
        del self.all_language_data[code]
        self.all_language_codes.remove(code)

        #export new language to files 
        if (export):
            #export updated language object to json, csv and markdown
            with open(self.language_lookup_filename + ".json", "w") as file:
                json.dump(self.all_language_data, file, indent=4) 
            pd.DataFrame.from_dict(self.all_language_data, orient='index').to_csv(self.language_lookup_filename + ".csv", index=False)

            #set language code as index for CSV output
            self.all_language_data = self.all_language_data.set_index("code").to_dict(orient="index")

            #convert language dict to dataframe, reset index, reorder columns and sort by language code
            language_lookup_df = pd.DataFrame.from_dict(self.all_language_data, orient='index').reset_index()
            language_lookup_df.rename(columns={'index': 'code'}, inplace=True)
            language_lookup_df = language_lookup_df.sort_values(by='code', ascending=True)
            language_lookup_dict = dict(sorted(language_lookup_dict.items()))

            #convert object to markdown
            language_lookup_markdown = language_lookup_df.to_markdown(index=False)
            with open(self.language_lookup_filename + '.md', 'w') as f:
                f.write(language_lookup_markdown)

    def export_language_source(self, language_code: str) -> str:
        """ 
        Get the source URLs for input language.

        Parameters
        ==========
        :language_code: str
            language code.

        Returns
        =======
        :language_source: str
            source for language object.
        """
        #call function to get object of ISO 639 language source urls, if object not initialised
        if (self.iso_639_language_source_urls == {}):
            self.iso_639_language_source_urls = self.get_iso_639_urls()

        #source for ISO 639-3 languages (3 letter language codes), ISO 639 code but no code found in https://www.loc.gov/standards/iso639-2/php/langcodes_name.php
        if (language_code not in self.language_exceptions) and (language_code not in self.iso_639_language_source_urls):
            language_source = "https://iso639-3.sil.org/code/" + language_code
        elif (language_code not in self.language_exceptions and language_code in self.iso_639_language_source_urls):
            language_source = "https://iso639-3.sil.org/code/" + language_code + ", " + "https://www.loc.gov/standards/iso639-2/php/langcodes_name.php?code_ID=" + self.iso_639_language_source_urls[language_code]
        #source for languages in list of language exceptions
        else:
            language_source = self.language_exceptions[language_code]["source"]
        
        return language_source
    
    @staticmethod   
    def get_iso_639_urls() -> dict:
        """
        Static method to get all language codes and their corresponding dropdown IDs on the ISO 639 
        language code search page: https://www.loc.gov/standards/iso639-2/php/langcodes_name.php.        

        Parameters
        ========== 
        None

        Returns
        =======
        :iso_639_language_source_urls: dict
            object of ISO 639 language codes and their source URLs.
        """
        #set random user-agent string for requests library to avoid detection, using fake-useragent package
        user_agent = UserAgent()
        user_agent_header = user_agent.random

        #use requests library to get language code page data
        iso_639_2_url = "https://www.loc.gov/standards/iso639-2/php/langcodes-search.php"
        response = requests.get(iso_639_2_url, headers={"User-Agent": user_agent_header})

        #scrape language code url using bs4
        soup = BeautifulSoup(response.text, 'html.parser')

        #get list of #CODE_IDs for 2 letter (alpha 2) and 3 letter (alpha 3) language code
        alpha_2_dropdown = soup.find('select', {'name': 'code_ID'})
        alpha_3_dropdown = soup.find('select', {'name': 'code_ID'})

        #create objects of each language's ISO 639 code and its dropdown #Code_id
        alpha_2_codes = {option.text: option['value'] for option in alpha_2_dropdown.find_all('option')}
        alpha_3_codes = {option.text: option['value'] for option in alpha_3_dropdown.find_all('option')}

        #merge the 2 dicts of codes
        iso_639_language_source_urls = {**alpha_2_codes, **alpha_3_codes}

        return iso_639_language_source_urls

    def __getitem__(self, language_code: str) -> dict:
        """
        Get language data for inputted language using its language code.
        This function uses the Map class to make the instance object of the 
        class subscriptable. It can accept 1 or more language codes and 
        return the data for each. 

        Parameters
        ==========
        :language_code: str
            language code/codes for desired language data.

        Returns
        =======
        :language_lookup_dict: dict
            dict object of language data for inputted language code/codes.

        Raises
        ======
        ValueError:
            Language code not found in list of available language codes.

        Usage
        =====
        from language_lookup import *

        #create instance of Language Lookup class
        lang_lookup = LanguageLookup()

        #get language data for Latvian
        lang_lookup["lav"]

        #get language data for Spanish
        lang_lookup["spa"]

        #get language data for Arabic, English and Irish
        lang_lookup["ara,eng,gle"]
        """
        #all input language codes should be lower case, split into multiple codes, if applicable
        language_code = language_code.lower().replace(' ', '').split(',')

        #object to store exported language data
        language_lookup_dict = {}

        #iterate over list of input language codes, get language data for each, raise error if invalid 
        for code in range(0, len(language_code)):

            #raise error if input code not found in list of valid codes
            if (not (language_code[code] in self.all_language_codes) and not (language_code[code] in list(self.language_exceptions.keys()))):
                raise ValueError(f"Input language code not found in list of valid codes or exceptions: {language_code[code]}.")
            
            #add each code to language object
            language_lookup_dict[language_code[code]] = {}

            #create Map class instance of individual language object
            lang_data = Map(self.all_language_data[language_code[code]])

            #recursively map any nested dicts
            for key in lang_data:
                if isinstance(lang_data[key], dict):
                    lang_data[key] = Map(lang_data[key])
            language_lookup_dict[language_code[code]] = lang_data

        #sort keys in output dict
        language_lookup_dict = dict(sorted(language_lookup_dict.items()))

        #convert into instance of Map class so keys can be accessed via dot notation
        language_lookup_dict = Map(language_lookup_dict)

        #if single language object in output, return it as list            
        if (len(language_lookup_dict) == 1):
            return list(language_lookup_dict.values())[0]

        return language_lookup_dict

    def __len__(self) -> int:
        """ Return total number of language codes in lookup table. """
        return len(self.all_language_data)

    def __repr__(self) -> str:
        """ String representation of instance object. """
        return f"<LanguageLookup(file='{self.language_lookup_filename}', languages={len(self.all_language_data) if isinstance(self.all_language_data, dict) else len(self.all_language_data)})>"

    def __str__(self) -> str:
        """ Friendly string representation of instance object. """
        return f"LanguageLookup instance with {len(self.all_language_data) if isinstance(self.all_language_data, dict) else len(self.all_language_data)} languages from '{self.language_lookup_filename}'."
    
class Map(dict):
    """
    Class that accepts a dict and allows you to use dot notation to access
    members of the dictionary. 
    
    Parameters
    ==========
    :dict
        input dictionary to convert into instance of map class so the keys/vals
        can be accessed via dot notation.

    Usage
    =====
    # create instance of map class
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    # Add new key
    m.new_key = 'Hello world!'
    # Or
    m['new_key'] = 'Hello world!'
    # Update values
    m.new_key = 'Yay!'
    # Or
    m['new_key'] = 'Yay!'
    # Delete key
    del m.new_key
    # Or
    del m['new_key']

    References
    ==========
    [1]: https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary
    """
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v
        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]