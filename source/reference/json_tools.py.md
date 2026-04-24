(JsonTools)=

# Json Tools File
- This file provides a library of functions to help with the loading and saving of json files. 
- This file is simply a collection of functions that almost entirely relates to the handling of json files and preforming checks between [json files](#JsonFilesInfo). 
- Keep in mind that most of these functions will be called by either the [File Service](#FileService), and [Save Load Handler](#SaveLoadHandler)


## Purpose/Motivation

- What problem does this solve?
	- Abstracting the json specific problems to another file. There are a lot of places in the other IO classes that load data from json and do checks relating to it, so that functionality was put here. 

- When would someone use this?
	- When someone wants to verify that the [default data](#JsonDefaults) matches the [definition schema](#JsonDefinitions) is this files main purpose. Or when someone wants to load in json data and get it returned without coding the error checks. When someone wants to save a dictionary to json 

## Basic Usage Example

- CostEstimator/config/validator/[schema_validator.py](#SchemaValidator) 

```python
@staticmethod
def validate_schemas(schema_paths: Dict[str, str], data_paths: Dict[str, str]) -> None:
	Logger.log('d', f"...truncatedForExample...")
	for tech_type in data_paths.keys():
		Logger.log('d', f"...truncatedForExample...")
		try:
			schema_check(schema_paths[tech_type], data_paths[tech_type])
			Logger.log('d', f"...truncatedForExample...")
		except Exception as e:
			Logger.log('e', f"...truncatedForExample...")
			raise
```
In this [schema validator](#SchemaValidator) example you can see that we loop over the additive manufacturing tech types and for each of those we do a check to see that the [default json data](#JsonDefaults) matches the schema (definition) of the setting using the data from the [json definition file](#JsonDefinitions) using the Json Tools 'schema_check()' function. 


## Key Methods/Functions
schema_check(defintion_path, defaults_data_path):
: This function will go through the default data and check that every one of its keys (categories) are in the schema data. 
: throws FileNotFoundError if either file path given doesnt exist
: throws RuntimeError if deserialization of JSON files fails
: throws ValueError: If a (category) key in default data doesnt appear in the schema data
: throws TypeError if the 'check_nested()' function throws it 

deserialize_json(json_file_path): dictionary
: This function will call `json.load(file)` after opening the json file at the path given. Then it returns the dictionary that was loaded.

load_data(default_data_paths): dictionary
: The dictionary given is a map of 'tech_type_name': 'path_to_any_data'
: This function will loop over the dictionary of technology names and pull the path to the data out. Then it will deserialize the json at that path and save it in a dictionary that maps the same technology name to now the dictionary of the deserialized data. 
: This function can be called with any data to be loaded in mind, it can be the paths to the [schema definitions](#JsonDefinitions) or the paths to the [default data](#JsonDefaults), both work because this functions goal is to only return a dictionary of the tech types to any data loaded. 

serialize_json(data, file_path): bool
: This will take the data dictionary given and write it out in json file path as long as the path exists and the dictionary given is has valid type 

type_matches([definition](#JsonDefinition)\_type_str, data_value): bool
: this function will check that if the type given is "int" that the `data_value` given will be an instance of a int type for example. This works with "int", "float", "range", "string", "boolean"

check_nested([schema](#JsonDefinitions)\_dict, [default](#JsonDefaults)\_dict, path="", schema_metadata = None):
: This function will recursively check that the keys and values in the default dictionary mach the schema definition which has the expected type, number of decimals, and I think that is all that is related. This function will call a private `_validate_value` wich will confirm that the types of the [default data](#JsonDefaults) and the stored expected type in the [json definition/schema](#JsonDefinitions) match. 
: This function wont return anything, but it will long and raise and error if it doesn't end up working/matching the definition. 

skipped many private methods

get_suppored_tech_types(defintion_directory): list\[str]
: This function will loop over the files in the definition directories files and if they arent user created, pull out their metadata and get the "type" value out and add it to a list to be returned.
: This function will use the help of the `get_tech_type(file_path)` function below

get_tech_type(file_path): str
: This function will be given a file path of a [json file](#JsonFilesInfo) and it will open it, deserialize it and pull out the "type" value from the "metadata" part 

get_is_user_created(file_path): bool
: this function will check the [json file](#JsonFilesInfo) at the given path if it is marked as user created in the metadata and return true if it is, false otherwise

get_file_paths(file_directory): dictionary\[str, str]
: This function will return a dictioanry mapping the technology name to their absolute file paths if they are not user created. 
: so you could pass this function the folder of the [json defaults](#JsonFilesInfo) and it will return the technologies and the paths to the json defaults files 

get_matching_schema_path(check_file_path, schema_dir): Tuple(tech_type, schema_path)
: This functions goal is to be given a file path of a [json defaults](#JsonDefaults) file, and the path to the [json definition/schema files](#JsonDefinitions). Then it will use the type found in the given defaults data and cross check it with every [metadata](#Metadata) type in the schemas director json files, and if there is a match it will return a tuple with the technology type , path to schema file. 

get_min_max(value_0, value_1): Tuple(int|float, int|float)
: This function will return a sorted pair of the numbers given in ascending order

## Notes/Warnings
- You'll notice when you look throughout the functions, the name of each technology is entirely based on the [metadata](#Metadata) that means the naming of the files in the defaults and definitions folders do not matter. 
