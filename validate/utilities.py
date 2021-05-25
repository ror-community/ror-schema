import os
import zipfile
import requests
import json
import sys

DEFAULT_SCHEMA = "https://raw.githubusercontent.com/ror-community/ror-records/v.1.2.9-rc/ror_schema.json"
API_URL = "https://api.ror.org/organizations"

GEONAMES = {}
GEONAMES['USER'] = "roradmin"
GEONAMES['URL'] = 'http://api.geonames.org/getJSON'

def url_validation(url):
    return validators.url(url)

def get_file_from_url(url=DEFAULT_SCHEMA):
    rsp = requests.get(url)
    rsp.raise_for_status()
    return rsp.json()

def get_json(arg,type="file"):
    if (type == "file"):
        try:
            with open(arg, 'r') as f:
                data = json.load(f)
        except Exception as e:
            raise(e)
    elif (type == "url"):
        data = get_file_from_url(arg)
    return data

def arg_exists(arg):
    check_path = os.path.exists(arg)
    if not(check_path):
        raise Exception(f"{arg} is required and must exist")


def help():
    print("To run the validator script:\n")
    print("The required argument is the path to files\n")
    print("The optional argument is the path or url to the schema. The default is the schema on the master branch of the ROR repo\n")
    print("python3 validateror.py path/to/files\n")
    print("OR\n")
    print("python3 validateror.py path/to/files path/to/schema/file\n")
    print("OR\n")
    print("python3 validateror.py path/to/files url/to/schema/\n")
