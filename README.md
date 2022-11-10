# ror-schema
[JSON Schema](https://json-schema.org) document used for generating and validating ROR records.

## Background

ror_schema.json was initially generated from [GRID records](https://grid.ac/) using [genson](https://pypi.org/project/genson/). Manual edits to this inferred schema were made based on the [GRID format documentation](https://web.archive.org/web/20220608180205/https://www.grid.ac/format). Note GRID record data did not necessarily align with the format documentation in all cases, therefore ROR inherited some records that are not schema valid.

## Usage

Python package [jsonschema](https://pypi.org/project/jsonschema) can be used to validate a JSON file against ror_schema.json , ex:

    pip3 install jsonschema
    jsonschema -i test.json grid_ror_schema.json

In the context of ROR curation, ror_schema.json is used:

- As part of the [leo-form application](https://github.com/ror-community/leo-form), which is used to generate new schema-valid records. Leo is based on [JSON Forms](https://jsonforms.io/) which generates interactive UI forms from a JSON schema document.
- As part of the [validation-suite](https://github.com/ror-community/validation-suite), which is used to validate new and updated records as part of the ROR curation workflow. This suite uses jsonschema to validate records against ror-schema.json, and also performs additional steps, such as checking Geonames addresses information against the Geonames API and checking for reciprical relationships. This suite is run at several points in the curation workflow using Github actions in [ror-updates](https://github.com/ror-community/ror-updates/tree/master/.github/workflows) and [ror-records](https://github.com/ror-community/ror-records/tree/main/.github/workflows).


## Definitions and policies

For documentation of top-level metadata element definitions and policies, see [ROR Data Structure](https://ror.readme.io/docs/ror-data-structure). For additional documentation of child-level fields, see also the longer [list of fields and subfields](https://ror.readme.io/docs/advanced-search#available-fields) in the ROR record schema that can be searched using the API advanced search. 
