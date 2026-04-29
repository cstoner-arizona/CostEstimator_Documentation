(SaveLoadHandler)=
# Save Load Handler
- **CostEstimator/config/io/save_load_handler.py**
- This class will work with the json_tools to facilitate saving and loading the state of technologies settings to/from json. 
- It only implements two functions, save and load
- This class will be used to handle the saving and loading of only custom users data that is saved from the plugin and loaded later 


## Purpose/Motivation

- What problem does this solve?
	- This class will provide the functionality needed to save and load the technology objects settings to and from json files 

- When would someone use this?
	- When the want to save a custom users settings they inputed. Or when they want to load in a custom users settings. Or when they want to just load in the default settings for a technology

## Basic Usage Example

- A simple, realistic code snippet showing the most common way to use it (keep it short, just enough for the basic idea)
CostEstimator/config/[config_manager.py](#ConfigManager)
```python
 # Use SaveLoadHandler.load_settings to return a Technology if successful, get status if not.
loaded_technology : Technology | SaveLoadStatus = SaveLoadHandler(
            self.file_service.user_data_dir,
            self.file_service.schema_dir
        ).load_settings(tech_type)
```
This will use the SaveLoadHandler to go to the CostEstimator/config/resources/data/user directory to load the user saved [defaults](#JsonDefaults) data and use the schema directory of the plugin to validate the user defaults are valid and if they are then the SaveLoadHandler will create a [technology](#TechnologyModel) object and return it if all went well.


## Key Methods/Functions
save_settings(technologyObj): [SaveLoadStatus](#SaveLoadStatusEnum)
: This function will be given a [technology object](#TechnologyModel), it will attempt to save all the settings of this technology object to a file name of a 'lowercase, space replaced with underscore . json' version of the technology name to the [user data directory](#user_data_dir) for this specific save load handler.
: if there are any problems with the save then it will return a [SaveLoadStatus](#SaveLoadStatusEnum).FAILURE. But if the user cancels the pick file location dialog back then it will return a SaveLoadStatus.CANCELLED

load_settings(tech_type_str): [Technology](#TechnologyModel) | [SaveLoadStatus](#SaveLoadStatusEnum)
: This function will be given the name of a additive manufacturing technology. It will prompt the user for which file on their pc they want to load. If the user cancels it will return a [SaveLoadStatus](#SaveLoadStatusEnum).CANCELLED. After getting the file it will validate the custom user saved [defaults](#JsonDefaults) matches the expected [schema definitions](#JsonDefinitions) and if all is well then it will return the technology object that has the settings of that user saved file 

## Important Attributes/Properties
{#SaveLoadStatusEnum}
SaveLoadStatus(Enum): 
: This is used to return to the [config manager](#ConfigManager) wether the save/load went well, or was canclled, or failed. A save could fail if the user doesnt specify a location, it could fail if a technology object doesnt have a 'name' attribute for example. 

{#user_data_dir}
`self._user_data_dir`{l=python}
: This holds the directory of the custom users data. Usually "CostEstimator/config/resources/data/user"

`self._schema_dir`{l=python}
: This holds the directory of the [json definitions files](#JsonDefinitions). Usually "CostEstimator/config/resources/data/[definitions](#JsonDefinitions)"

  

## Notes/Warnings
- Remember that this class is only for saving and loading custom user set [json defaults](#JsonDefaults) data.
