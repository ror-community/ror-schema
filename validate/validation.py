import json
import sys
import jsonschema
import requests
import validators
from utilities import *
import pycountry

class Validate_Tests:
    def __init__(self,file):
        #instantiate validate class with json record
        self.__file = file

    def __file(self,file):
        return file

    def __validator_functions(self):
        # getting public methods for the class.
        #Do not have to hardcode functions that will be checked as all validator functions should be public
        m = [attribute for attribute in dir(self) if callable(getattr(self, attribute)) and attribute.startswith('__') is False and attribute.startswith('_') is False]
        return m

    def __handle_check(self,result,name,msg=None):
        # all the validator message use this pattern
        message = {}
        message[name] = {'result':result,'status':True}
        if not(result):
            message[name] = {'result':result,'status':msg}
        return message

    def __validate_url(self,url):
        msg = None
        validated_url = validators.url(url)
        if not(validated_url):
            msg = "Validation Error"
        return msg

    def __mapped_geoname_record(self):
        ror_to_geoname = {
              "lat": "lat",
              "lng": "lng",
              "city": "asciiName",
              "geonames_city": {
                "id": "geonameId",
                "city": "asciiName",
                "geonames_admin1": {
                    "name": "adminName1",
                    "id": "adminId1",
                    "ascii_name": "adminName1",
                    "code": ["countryCode","adminCode1"]
                },
                "geonames_admin2": {
                    "name": "adminName2",
                    "id": "adminId2",
                    "ascii_name": "adminName2",
                    "code": ["countryCode","adminCode1","adminCode2"]
                },
                "country_geonames_id": "countryId"
            }}
        return ror_to_geoname

    def __get_geonames_response(self,id):
        msg = None
        result = None
        query_params = {}
        query_params['geonameId'] = id
        query_params['username'] = GEONAMES['USER']
        url = GEONAMES['URL']
        try:
            response = requests.get(url,params=query_params)
            response.raise_for_status()
            result = json.loads(response.text)
        except requests.exceptions.RequestException as e:
            msg = "Connection Error"
        return result,msg

    def __get_record_address(self):
        address = self.__file['addresses'][0]
        id = address['geonames_city']['id']
        return id,address

    def check_links(self):
        name = str(self.check_links.__name__)
        msg = {}
        results = True
        links = self.__file['links']
        links.append(self.__file['wikipedia_url'])
        if len(links) > 0:
            for l in links:
                result = self.__validate_url(l)
                if result:
                    msg[l] = result
                    results = None
        if len(msg) == 0:
            msg = None
        return self.__handle_check(results,name,msg)

    def __compare_ror_geoname(self,mapped_fields,ror_address,geonames_response,msg={}):
        compare = msg
        for key, value in mapped_fields.items():
            # If value is of dict type then print
            # all key-value pairs in the nested dictionary
            if isinstance(value, dict):
                self.__compare_ror_geoname(value,ror_address[key],geonames_response,compare)
            else:
                _,original_address = self.__get_record_address()
                ror_value = ror_address[key] if key in ror_address else original_address[key]
                geonames_value = None
                if (key == "code"):
                    key_exists = True
                    for x in value:
                        if not(x in geonames_response):
                            key_exists = False
                    if key_exists:
                        geonames_value = ".".join([geonames_response[x] for x in value])
                else:
                    if (value in geonames_response) and (geonames_response[value] != ""):
                        geonames_value = geonames_response[value]
                    if str(ror_value) != str(geonames_value):
                        compare[key] = {"ror": ror_value, "geonames": geonames_value}
        return compare

    def check_address(self):
        name = str(self.check_address.__name__)
        id, address = self.__get_record_address()
        result = None
        compare = {}
        geonames_response,msg = self.__get_geonames_response(id)
        if geonames_response:
            mapped_fields = self.__mapped_geoname_record()
            compare = self.__compare_ror_geoname(mapped_fields,address,geonames_response)
            if len(compare) == 0:
                    result = True
        else:
            compare["ERROR"] = msg
        print(compare)
        return self.__handle_check(result,name,compare)


    def check_country_code(self):
        name = str(self.check_country_code.__name__)
        country = self.__file['country']['country_code']
        msg = None
        pcountry = pycountry.countries.get(alpha_2=country)
        if not(pcountry):
            msg = f'Country value: {country} is not in iso3166 standard'
        return self.__handle_check(pcountry,name,msg)

    def check_language_code(self):
        name = str(self.check_language_code.__name__)
        language = self.__file['labels'][0]['iso639']
        msg = None
        pylanguage = pycountry.languages.get(alpha_2=language)
        if not(pylanguage):
            msg = f'Language value: {language} is not an iso639 standard'
        return self.__handle_check(pylanguage,name,msg)

    def check_established_year(self):
        name = str(self.check_established_year.__name__)
        yr = self.__file['established']
        msg = None
        year_length = len(str(yr))
        if not(year_length > 2 and year_length < 5):
            msg = f'Year value: {yr} should be an integer between 3 and 4 digits'
        return self.__handle_check(yr,name,msg)

    def validate_all(self,all_files=None):
        me = str(self.validate_all.__name__)
        validator_functions = self.__validator_functions()
        validator_functions.remove(me)
        results = []
        for methods in validator_functions:
            validate = getattr(self, methods)
            results.append(validate())
        return results


#file = "/Users/eshadatta/test-grid-schema-test-files/valid/015m7wh34.json"
file="t.json"
with open(file, 'r') as f:
    data = json.load(f)
validate = Validate_Tests(data)
print(validate.validate_all())

#TODO:
# have getter functions for all the validation functions -- ??
# finish relationship checking
# implement geonames - done,
# url checking - done
# write tests
