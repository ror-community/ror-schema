import argparse
import validate.validation as vt
import validate.validateror as vs
import validate.utilities as u
import os
import sys
import json

def set_args():
    parser = argparse.ArgumentParser(
                    description="Script to validate ROR files",
                    epilog="IMPORTANT: While file and directory are listed as optional, one of the two must be specified for the validation suite to run. Use file to validate a single file, use dir to validate the contents of a directory")
    validate = parser.add_mutually_exclusive_group(required=True)
    validate.add_argument('-f','--file', help='process one file')
    validate.add_argument('-d','--dir', help='batch process a directory')
    parser.add_argument('-s', '--schema', help='Path or URL to schema')
    parser.add_argument('-p', '--file-path', help='Path to the rest of the files for relationship validation')
    args = parser.parse_args()
    return args

def run_validation_tests(file, path=None):
    with open(file, 'r') as f:
        data = json.load(f)
    validate = vt.Validate_Tests(data)
    validation_errors = validate.validate_all(file_path=path)
    return validation_errors

def get_files(file,dir):
    files = []
    if file:
        files.append(file)
    elif dir:
        file = []
        path = os.path.normpath(dir)
        for f in os.listdir(dir):
            file.append(f)
        files = list(map(lambda x: path+"/"+x, file))
    return files

def main():
    args = set_args()
    files = get_files(args.file,args.dir)
    schema = args.schema if args.schema else None
    path = args.file_path if args.file_path else None
    filename = ""
    messages = {}
    validation_errors = {}
    for f in files:
        filename = os.path.basename(f).split(".")[0]
        print("fn: ", filename)

        valid, msg = vs.validate_file(f,schema)
        if valid:
            errors = run_validation_tests(f,path)
            print(f"file: {f}, errors: {errors}")
            messages[filename] = errors
        else:
            for file, err in msg.items():
                messages[filename] = err
    for filename, err in messages.items():
        if len(err) > 0:
            for errors in err:
                print(f"ERROR: {filename}: {errors}\n")

if __name__ == "__main__":
    main()
