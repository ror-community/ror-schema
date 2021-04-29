SCHEMA = "https://raw.githubusercontent.com/ror-community/ror-records/v.1.2.9-rc/ror_schema.json"

GEONAMES = {}
GEONAMES['USER'] = roradmin
GEONAMES['URL'] = 'http://api.geonames.org/getJSON'

def help():
    print("To run the validator script:\n")
    print("The required argument is the path to files\n")
    print("The optional argument is the path or url to the schema. The default is the schema on the master branch of the ROR repo\n")
    print("python3 validateror.py path/to/files\n")
    print("OR\n")
    print("python3 validateror.py path/to/files path/to/schema/file\n")
    print("OR\n")
    print("python3 validateror.py path/to/files url/to/schema/\n")
