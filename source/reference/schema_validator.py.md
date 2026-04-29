(SchemaValidator)=
# SchemaValidator
- **CostEstimator/config/validator/schema_validator.py**
- This class will help with confirming that the [json definitions](#JsonDefinitions) are in the correct file structures with all the expected tech types in a folder, also checking that for each technology settings [defaults](#JsonDefaults) align with the [definitions](#JsonDefinitions), then finally also checking that the user saved file matches with its corresponding 



## Purpose/Motivation

- What problem does this solve?
	- When we were updating the [jsons](#JsonFilesInfo) for this project we would make human mistakes, this wont let us make those mistakes anymore because it runs before the main plugin starts and crashes if it encounters an error 

## Key Methods/Functions
validate_file_structure(supported_tech_types): 
: Ensures that every supported tech type is found in the keys of a dictionary mapping technology names to their [json definitions](#JsonDefinitions) file path. 

validate_schemas(schema_paths, data_paths):
: This function will loop over the data types shared in these two dictionaries and confirm the [default data](#JsonDefaults) holds to the standard defined in the [json definitions](#JsonDefinitions). 

validate_user_file(file_path, schema_dir, expected_type):
: This function will confirm there is a [json schema](#JsonDefinitions) for the file path given and that the received resulting type matches expected. then it will get the [default data](#JsonDefaults) stored in the user file and do a schema check based on the schema found earlier. 


## Important Attributes/Properties
None, it just holds static methods



## Notes/Warnings
- None
