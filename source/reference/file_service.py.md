(FileService)=
# File Service
- **CostEstimator/config/io/file_service.py**
- This class provides all of the directories and file paths to all important [json files](#JsonFilesInfo) and their parent directories. 
- The [technology](#TechnologyModel) for example uses this class to find the path to the [json defaults](#JsonDefaults) it will use to load the default data
- This class is a dataclass, meaning we can define methods as `@property`{l=python} which act as attributes. e.g. `settingObj.value = 10 # does type validation in source code`{l=python}

## Purpose/Motivation

- What problem does this solve?
	- It simplifies the problem of having multiple places to change when you want to change the location of the data directory because now every place that wants to know the file path can use this class 

- When would someone use this?
	- When they want the directory of the [json](#JsonFilesInfo) data or schemas

## Basic Usage Example
- Using getters to get out the directory or path of a [json defintion](#JsonDefinitions) or [json defaults](#JsonDefaults) or user data 
## Key Methods/Functions
get_all_file_paths() -> tuple of 3 dictionaries (def, default, user) mapping the name of the technology to their file path 

load_data() -> tuple of 3 dictionarys (def, default, user) mapping the tech name to a dictionary of their values in the corrisponding [json file](#JsonFIle)


## Important Attributes/Properties
{#schema_dir}
`self.schema_dir`{l=python}
: returns the string of the schema directory
: usually 'config/resources/data/definitions'

`self.schema_file_paths`{l=python}
: returns the technology names mapping to their definitions file names paths
: e.g. `{"Binder Jetting": 'config/resources/data/definitions/binder_jetting.json'}`{l=python}

`self.serialized_schema`{l=python}
: returns a dictionary mapping the name of a additive manufacturing tech type to their [json defintions](#JsonDefinitions) in dictionary form 

`self.default_data_dir`{l=python}
: returns the string of the [defaults](#JsonDefaults) directory
: usually 'config/resources/data/defaults'

`self.default_data_paths`{l=python}
: returns the technology names mapping to their defaults file names paths
: e.g. `{"Binder Jetting": 'config/resources/data/defaults/binder_jetting.json'}`{l=python}

`self.serialized_default_data`{l=python}
: returns a dictionary mapping the name of a additive manufacturing tech type to their [json defaults](#JsonDefaults) in dictionary form 

`self.user_data_dir`{l=python}
: returns the string of the users saves directory
: usually 'config/resources/data/user'

`self.user_data_paths`{l=python}
: returns the technology names mapping to their user saved defaults file names paths
: e.g. `{"Binder Jetting": 'config/resources/data/user/binder_jetting.json'}`{l=python}

`self.serialized_user_data`{l=python}
: returns a dictionary mapping the name of a additive manufacturing tech type to their [json defaults](#JsonDefaults) in dictionary form that was saved in the user file

`self.supported_technologies`{l=python}
: returns a list of the tech types pulled from the [metadata](#Metadata) of a [json definition](#JsonDefinitions) found in the [schema](#schema_dir) directory

  

## Examples Section
- The **FileService** is used a lot when we want to get a list of the supported technologies for validation (Found in ConfigManager::init). 
- This is also used a lot to pull out the paths of the [default data](#JsonDefaults) and the [definition data](#JsonDefinitions) to then load each data in the validator to do the validation. 

## Notes/Warnings
- None