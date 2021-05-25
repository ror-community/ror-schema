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

    def __get_key(self,key):
        # this is for a dictionary that is not nested
        payload = self.__file.get(key,None)
        return payload

    def __recursive_nested_lookup(self,key,file=None):
        # this is for a nested dictionary
        # this also works for an unnested dictionary
        if file is None:
            file = self.__file
        result = file.get(key)
        if result:
            return y
        for k,v in file.items():
            if isinstance(v,list):
                for i in v:
                    if isinstance(i,dict):
                        return self.__recursive_nested_lookup(key,i)
            elif isinstance(v,dict):
                return self.__recursive_nested_lookup(key,v)

    def __handle_check(self,result,name,msg):
        # all the validator message use this pattern
        message = {}
        message[name] = True
        if msg:
            message[name] = {'result':result,'status':msg}
        return message

    def check_country_code(self):
        name = str(self.check_country_code.__name__)
        country = self.__get_key('country')['country_code']
        msg = None
        pcountry = pycountry.countries.get(alpha_2=country)
        if not(pcountry):
            msg = f'Country value: {country} is not in iso3166 standard'
        return self.__handle_check(pcountry.alpha_2,name,msg)

    def check_language_code(self):
        name = str(self.check_language_code.__name__)
        language = self.__get_key('labels')[0]['iso639']
        msg = None
        pylanguage = pycountry.languages.get(alpha_2=language)
        if not(pylanguage):
            msg = f'Language value: {language} is not an iso639 standard'
        return self.__handle_check(pylanguage.alpha_2,name,msg)

    def check_established_year(self):
        name = str(self.check_established_year.__name__)
        yr = self.__get_key('established')
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


file = "/Users/eshadatta/test-grid-schema-test-files/valid/015m7wh34.json"
with open(file, 'r') as f:
    data = json.load(f)
validate = Validate_Tests(data)
print(validate.validate_all())
