import json
import os.path
import os
import sys
import jsonschema
import requests
import validators
from config import *
import pycountry


## TODO:
# check language against iso639
# extract relationship id, language, country code, address dict
# zip all files, check relationship id against remaining files and against api
# make it so that people can either check all or pick what they want to test
# then see if you can export this out to a library; see if you can do this on Monday
