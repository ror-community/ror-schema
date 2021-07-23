import json
import sys
import jsonschema
import requests
import validators
import pycountry
import validate.utilities as u
import validate.validation_helpers as vh
import validate.validate_relationships as vr

class Validate_Tests:
    def __init__(self,file):
        #instantiate validate class with json record
        vh.File = file

    def _validator_functions(self):
        # getting public methods for the class.
        #Do not have to hardcode functions that will be checked as all validator functions should be public
        m = [attribute for attribute in dir(self) if callable(getattr(self, attribute)) and attribute.startswith('_') is False]
        return m

    def check_links(self):
        # public method for url format validation
        name = str(self.check_links.__name__)
        msg = {}
        links = vh.File['links']
        links.append(vh.File['wikipedia_url'])
        # removing empty strings
        links = list(filter(None, links))
        if len(links) > 0:
            for l in links:
                result = vh.validate_url(l)
                if result:
                    msg[l] = result
        if len(msg) == 0:
            msg = None
        return vh.handle_check(name,msg)

    def check_address(self):
        # compares ror and geonames address values
        name = str(self.check_address.__name__)
        id, address = vh.get_record_address()
        result = None
        compare = {}
        geonames_response,msg = vh.get_geonames_response(id)
        if geonames_response:
            mapped_fields = vh.mapped_geoname_record()
            compare = vh.compare_ror_geoname(mapped_fields,address,geonames_response)
            if len(compare) == 0:
                    result = True
        else:
            compare["ERROR"] = msg
        return vh.handle_check(name,compare)


    def check_country_code(self):
        # checks country code
        name = str(self.check_country_code.__name__)
        country = vh.File['country']['country_code']
        msg = None
        pcountry = pycountry.countries.get(alpha_2=country)
        if not(pcountry):
            msg = f'Country value: {country} is not in iso3166 standard'
        return vh.handle_check(name,msg)

    def check_language_code(self):
        # checks language code
        name = str(self.check_language_code.__name__)
        language = vh.File['labels']
        msg = None
        if len(language) > 0:
            pylanguage = pycountry.languages.get(alpha_2=language[0]['iso639'])
            if not(pylanguage):
                msg = f'Language value: {language} is not an iso639 standard'
        return vh.handle_check(name,msg)

    def check_established_year(self):
        # checks established year
        name = str(self.check_established_year.__name__)
        yr = vh.File['established']
        msg = None
        year_length = len(str(yr)) if isinstance(yr, int) else None
        if year_length and (not(year_length > 2 and year_length < 5)):
            msg = f'Year value: {yr} should be an integer between 3 and 4 digits'
        return vh.handle_check(name,msg)

    def validate_all(self,file_path=None):
        # calling all public methods in this class and removing the current method name.
        # This enables future public methods to be called automatically as well
        method_name = str(self.validate_all.__name__)
        validator_functions = self._validator_functions()
        validator_functions.remove(method_name)
        results = []
        for methods in validator_functions:
            validate = getattr(self, methods)
            results.append(validate())
        if file_path:
            rel = vh.get_relationship_info()
            if rel['rel']:
                vr.info = {"file_path":file_path,"record_info":rel}
                msg = vr.check_relationships()
                if msg:
                    results.append({'relationships':msg})
        results = list(filter(None,results))
        return results

# write tests
