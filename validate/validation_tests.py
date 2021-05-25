import json
import sys
import jsonschema
import requests
import validators
from utilities import *
import pycountry


## TODO:
# check language against iso639 - done
# extract relationship id, language, country code, address dict - done
# zip all files, check relationship id against remaining files and against api
# make it so that people can either check all or pick what they want to test
# check geonames and country code - done
# check links and wikipedia_url to make sure that they are urls
# check established is a year, between 2 and 5 digits? - done

def get_language(file):
    return file['labels'][0]['iso639']

def get_relationship(file):
    return file['relationships']

def get_address(file):
    return file['addresses']

def get_country(file):
    return file['country']



def check_relationships(rel_id,path):
    return b
