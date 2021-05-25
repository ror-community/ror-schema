import json
import sys
import jsonschema
from jsonschema import validate
import validators
from utilities import *

def schema_type(schema):
    if url_validation(schema):
        return "url"
    elif os.path.exists(schema):
        return "file"
    else:
        raise Exception(f"{schema} must either be a file or a url")

def validate_file(file,schema):
    if schema:
        stype = schema_type(schema)
    arg_exists(file)
    valid = False
    schema = get_file_from_url() if schema is None else get_json(schema,stype)
    msg = {}
    json = get_json(file)
    try:
        validate(instance = json, schema = schema)
    except jsonschema.exceptions.ValidationError as err:
        msg[file] = err
    valid = False if msg else True
    return valid, msg

def main():
    args = sys.argv[1:]
    if (len(args) == 0):
        help()
        exit(0)
    file = args[0]
    schema = args[1] if len(args) > 1 else None
    valid, msg = validate_file(file,schema)
    if valid:
        exit(0)
    else:
        for file, err in msg.items():
            sys.stderr.write(f"\nERROR: {file}: {err}\n")
        exit(1)

if __name__ == "__main__":
    main()
