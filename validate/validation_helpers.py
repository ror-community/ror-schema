import json
import sys
import jsonschema
import requests
import validators
from validate.utilities import *
import pycountry


File = None

def handle_check(name,msg=None):
    # all the validator message use this pattern
    message = {}
    if msg:
        message[name] = {'status':msg}
    return message

def validate_url(url):
    # validates url format against a library
    msg = None
    validated_url = validators.url(url)
    if not(validated_url):
        msg = "Validation Error"
    return msg

def mapped_geoname_record():
    # mapping of ror fields to geoname response fields
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

def get_geonames_response(id):
    # queries geonames api with the city geonames id as a query parameter
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

def get_record_address():
    # returns the address dictionary with the geonames city id
    address = File['addresses'][0]
    id = address['geonames_city']['id']
    return id,address

def get_relationship_info():
    # returns relationship dictionary
    return {"id": File['id'], "name": File['name'],"rel": File["relationships"]}

def compare_ror_geoname(mapped_fields,ror_address,geonames_response,msg={}):
    compare = msg
    for key, value in mapped_fields.items():
        # If value is of dict type then print
        # all key-value pairs in the nested dictionary
        if isinstance(value, dict):
            compare_ror_geoname(value,ror_address[key],geonames_response,compare)
        else:
            _,original_address = get_record_address()
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
