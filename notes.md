Following code inferred schema from grid dump:
```
import json
from genson import SchemaBuilder

builder = SchemaBuilder()
filename = "grid.json"
with open(filename, 'r') as f:
    datastore = json.load(f)
    builder.add_object(datastore)

schema = builder.to_schema()
with open("test_ror_schema.json",'w') as f:
  f.write(json.dumps(schema))
  ```
 
added enum values for status and types


`pip3 install jsonschema`

`jsonschema -i test.json grid_ror_schema.json`


Next steps:

1. Tests will be required for the following:
   * Check that relationship IDs exist or records for that have been created in the current dump

