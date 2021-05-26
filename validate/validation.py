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
        if msg:
            message[name] = {'result':result,'status':msg}
        return message

    def __validate_url(self,url):
        msg = None
        validated_url = validators.url(url)
        if validated_url:
            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                msg = "Connection Error"
        else:
            msg = "Validation Error"
        return msg

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
# implement geonames,
# url checking - done
# write tests
