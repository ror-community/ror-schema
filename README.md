# ror-schema
[JSON Schema](https://json-schema.org) document used for generating and validating ROR records.

## Usage

Python package [jsonschema](https://pypi.org/project/jsonschema) can be used to validate a JSON file against ror_schema.json , ex:

    pip3 install jsonschema
    jsonschema -i test.json ror_schema_v2_0.json

In the context of ROR curation, ror_schema.json and ror_schema_v2_0.json are used:

- As part of the [leo-form application](https://github.com/ror-community/leo-form), which is used to generate new schema-valid records. Leo is based on [JSON Forms](https://jsonforms.io/) which generates interactive UI forms from a JSON schema document. **leo-form is deprecated as of April 2024**
- As part of the [ror-api](https://github.com/ror-community/ror-api), create, update and bulkupdate functionality, which is used to create new/updated records as part of the ROR curation workflow. Whenever records are created or updated, they are validated against the schema.
- As part of the [validation-suite](https://github.com/ror-community/validation-suite), which is used to validate new and updated records as part of the ROR curation workflow. This suite uses jsonschema to validate records against ror-schema.json or ror_schema_v2_0.json, and also performs additional steps, such as checking Geonames addresses information against the Geonames API and checking for reciprical relationships. This suite is run at several points in the curation workflow using Github actions in [ror-updates](https://github.com/ror-community/ror-updates/tree/master/.github/workflows) and [ror-records](https://github.com/ror-community/ror-records/tree/main/.github/workflows).


## Schema versions

### Versioning policy
In 2024, schema versioning was introduced, and the first new version is ror_schema_v2_0.json. The schema is versioned per [ROR's schema versioning policy](https://ror.readme.io/docs/schema-versions)

### v1.0/no version
Schema file: [ror_schema.json](https://github.com/ror-community/ror-schema/blob/master/ror_schema.json)
Documentation: https://ror.readme.io/docs/data-structure

The first ROR schema was originally unversionsed and is now referred to as 1.0. ror_schema.json was initially generated from [GRID records](https://grid.ac/) using [genson](https://pypi.org/project/genson/). Manual edits to this inferred schema were made based on the [GRID format documentation](https://web.archive.org/web/20220608180205/https://www.grid.ac/format). Note GRID record data did not necessarily align with the format documentation in all cases, therefore ROR inherited some records that are not schema valid.

### v2.0
Schema file: https://github.com/ror-community/ror-schema/blob/master/ror_schema_v2_0.json
Documentation: https://ror.readme.io/v2/docs/data-structure

v2.0 includes several major changes (fields added, fields removed/restructured). These changes were determined based on multiple rounds of community feedback. See https://ror.readme.io/docs/schema-v2