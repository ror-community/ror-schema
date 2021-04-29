import json
import os.path
import os
import sys
import jsonschema
from jsonschema import validate
import zipfile
import requests
import validators
from config import *

def url_validation(url):
    return validators.url(url)

def schema_type(schema):
    if url_validation(schema):
        return "url"
    elif os.path.exists(schema):
        return "file"
    else:
        raise Exception(f"{schema} must either be a file or a url")

def check_path(path):
    check_path = os.path.exists(path)
    if not(check_path):
        raise Exception(f"{path} is required and must exist")

def get_schema(url=SCHEMA):
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
        data = get_schema(arg)
    return data

def validate_file(path,schema):
    if schema:
        stype = schema_type(schema)
    check_path(path)
    all_valid = False
    files = [path + "/" + file for file in os.listdir(path)]
    schema = get_schema() if schema is None else get_json(schema,stype)
    msg = {}
    for i in files:
        json = get_json(i)
        try:
            validate(instance = json, schema = schema)
        except jsonschema.exceptions.ValidationError as err:
            msg[i] = err
    all_valid = False if msg else True
    return all_valid, msg

def main():
    args = sys.argv[1:]
    if (len(args) == 0):
        help()
        exit(0)
    path = args[0]
    schema = args[1] if len(args) > 1 else None
    valid, msg = validate_file(path,schema)
    if valid:
        exit(0)
    else:
        for file, err in msg.items():
            sys.stderr.write(f"\nERROR: {file}: {err}\n")
        exit(1)

if __name__ == "__main__":
    main()
