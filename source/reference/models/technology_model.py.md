(TechnologyModel)=
# Technology Model
- **CostEstimator/config/models/technology_model.py**
- This class models and stores all data needed for a specific additive manufacturing technology. (e.g. Binder Jetting Sand Casting, Machining, Traditional Investment Casting)
- This class holds the data needed for switching to different technologies on the left side in the GUI. 
- This class holds all the setting data related to its specific technology.

## Inherits
[MutableMapping](https://docs.python.org/3/library/collections.abc.html#collections.abc.MutableMapping)
- The only thing this allows the object to inherit is the ability to have the `object[key] = newVal` syntax acted upon it.
- This means we can use the `__setitem__` special function to denote the functionality of `technologyObj[settingName] = newSettingValue` to be the function we call when the user enters a new value into the GUI
- This means we can use `technologyObj[settingName]` to also get the value out of the setting. If its a [setting range](#SettingRange) it returns a tuple of the min and max


## Purpose/Motivation

- What problem does this solve?
	- The problem was that we needed a way to store all the data related to a technology type. 
		- Its name (e.g. Binder Jetting, Machining)
		- Its default data for every setting (i.e the [defaults json](#JsonDefaults) file)
		- Its definition for every setting (i.e. the [definitions json](#JsonDefinitions) file)
	- We also needed ways to update setting values, override original settings, calculate settings based on just 1 technology. So that is why the technology object was made, to hold all this setting data, and calculate/update settings specific to one technology.

- When would someone use this?
	- When they want to represent a additive manufacturing technology in the plugin. They would create a technology and load the data needed from the [json file](#JsonFilesInfo), then create a related [calculator](#Calculator) object. 

## Basic Usage Example

- A simple, realistic code snippet showing the most common way to use it (keep it short, just enough for the basic idea)

CostEstimator/config/io/[save_load_handler](#SaveLoadHandler).py::load_settings()
```python
def load_settings(self, tech_type):
	# check file paths ..
	# validate a potential user file ..
	# get out the defintion json data ..
	# get out the defaults json data ..
	return Technology(tech_type, default_json_data, defintion_json_data)
```

CostEstimator/config/[config_manager](#ConfigManager).py::process_STL_inputs()
```python
def process_STL_inputs(new_data):
	# get out the current technology type
	currTechObj = self.technologies[self.current_type]
	currTechObj.process_STL_inputs(new_data)
```

## Key Methods/Functions
\_load\_data(): This function is called on initialization. It will be given the json dictionary of the [default data](#JsonDefaults) and the json dictionary of the [definition data](#JsonDefinitions). Then it will go over every setting in the technologies [json file](#JsonFilesInfo) and create a [setting](#SettingModel) object and store other data related to its self pulled from the json files. 

\_initialize\_calculator(): This function will create a [SettingCalculator](#SettingCalculator) which is essentially a mask or interface for the real [calculator](#Calculator). In the initialization for the SettingCalculator it creates the appropriate calculator for this technology. Then after the calculators initialization which may include calculations of [calculated settings](#calculated-setting) we as the technology object pull the calculators settings to update our own settings dictionary with the new values. 

\_\_delitem\_\_(key) : Deletes the setting name from the technology

\_\_getitem\_\_(key): Gets the [setting](#SettingModel) value from the technology model 

\_\_len\_\_(): Returns the number of settings in the technology 

\_\_setitem\_\_(settingName, value): 
: Raises SettingNotFoundError if settingName not in this technology
: It will set the value of the setting name given to the value given
: Then it will update the calculator and have the calculate recalculate any dependents if any

\_\_str\_\_(): Returns string representation of the technology instance 

get_setting_as_setting_obj(setting_name): Returns [Setting](#SettingModel) object based on setting name given 

Private method skipped (`_get_setting_by_category`)

get_setting_ATTRIBUTE(setting_name): Returns the `.ATTRIBUTE` attribute of the [Setting](#SettingModel) object based on setting name given. Replace the word ATTRIBUTE with any setting attribute and there exists a function for it

override_all_original_values(): Will go over every [setting](#SettingModel) and set its `.original_value` attribute to the `.value` attribute. Overriding its original value with its current

get_metadata(meta_type): returns the value of the "metadata" key within the [json file](#JsonFilesInfo) type given for this technology. So if `meta_type="data"` is will return this technologies [defaults json](#JsonDefaults) file "[metadata](#Metadata)" key pair value. Where as if `meta_type="schema"` it will return this technologies [definitions json](#JsonDefinitions) file metadata. 

get_all_settings(category_name): Returns a dictionary with all the [settings](#SettingModel) of a category. The keys are the setting name strings, the values are the settings value. 

get_settings_as_save_format(): Returns a dictionary that would match just like the [defaults json file](#JsonDefaults). It has meta data at the top, and categories as keys, then the values of categories would be dictionaries that hold a key:value pair of every setting. 

Private method skipped (`_format_metadata`)

Private method skipped (`_format_category`)

get_related_materials(): Returns a dictionary that maps material types (e.g. `"molds"`) to a list of the materials for that type (e.g. `["silica", "ceramic_alumina", "chromite"]`). This can be found in the metadata of the [json files](#JsonFilesInfo). 

get_all_material_dependent_settings(): Returns a dictionary mapping setting names to instances of [MaterialSettings](#MaterialSetting)

get_all_material_affected_settings(material_name): Loops over all material dependent settings and checks if it has a material name given in its selectable materials. If so it adds that to a dictionary mapping setting names to [MaterialSettings](#MaterialSetting). A selectable material  could be "silica", "alsi10mg", "in738" and the materials for a technology can be found in the [metadata](#Metadata) of the [json files](#JsonFilesInfo).

set_all_material_pointers(material_name): Loops over all material dependent settings that are affected by the material name given. Then it will update the [material setting](#MaterialSetting) to have its currently selected material be the one given. A material_name could be "silica", "alsi10mg", "in738" and the materials for a technology can be found in the [metadata](#Metadata) of the [json files](#JsonFilesInfo).

is_modified(): Returns true if any settings within the technology are modified. This is used for detecting if the "Save Settings" button in the GUI should be lit up. 

revert_all_settings(): Loops over all [setting](#SettingModel) objects for this technology and calls `setting_obj.revert()` on it which sets the `.value` to the `.original_value` and changes `.is_modified` to False

Private method skipped (`_is_valid_setting`)

\_process_setting(category, setting_name, setting_value, setting_schema): This function
will determine if the setting is a material dependent or a regular setting, then based on that it will call the corresponding function, and that corresponding function will determine if the type is a range or normal and it will call the corresponding function to create the actual [setting](#SettingModel) object and saving it in `self.settings[setting_name] = setting_obj`

Private method skipped (`_handle_regular_setting`)

Private method skipped (`_handle_material_dependent_setting`)

Private method skipped (`_create_material_range_setting`)

Private method skipped (`_create_material_setting`)

Private method skipped (`_create_range_setting`)

Private method skipped (`_create_normal_setting`)

(TechnologyProcessSTL)=
process_STL_inputs(new_stl_input_data): This function takes a dictionary of setting names that are based on STL sliced data from Cura and their values. It will loop over all the setting names to update their values, and after each setting we update we will recalculate that settings dependents so the higher up [calculated settings](#calculated-setting) get updated. 

Private method skipped (`_validate_range_value`)

reset_slice_first_settings_to_zero(): This function will loop over all setting objects in this technology  
and for each "slice_first"=True setting it will set it to zero.  
This function is not used the first time the plugin is launched because all stl  
values are already zero. But each time after that this function will be called.  
See issue #101 on github

## Important Attributes/Properties
self.type: str 
: the name of the technology, it should be pulled from the meta data key in the [json files](#JsonFilesInfo)

self.\_related_materials: dict\[str, list\[str]] 
: Holds the material types : list of materials section that can be found in the meta data key in the [json files](#JsonFilesInfo)
CostEstimator/config/resources/data/[defaults](#JsonDefaults)/binder\_jetting_default.json
```json
"metadata": {
    ...
    "compatible_materials": {
	    ------- vvv -----
      "molds": [
        "silica",
        "ceramic_alumina",
        "chromite"
      ],
      "binders": [
        "furan",
        "phenolic",
        "inorganic_foundry"
      ],
      "metals": [
        "alsi10mg",
        "alsi7mg0.6",
        "316_l_stainless_steel",
        "in625"
      ]
    }
	    ------- ^^^ -----
  }
 
```

{#TechnologiesSelfCalculator}
self.calculator: [SettingCalculator](#SettingCalculator) 
: A setting calculator object that will hold inside itself the actual [Calculator](#Calculator) object. The reason for the mask/interface style of SettingCalculator is because we didnt want the logic of choosing the correct calculator inside the technology object. 

self.settings: dict\[str, [Setting](#SettingModel)] 
: A dictionary that holds the [json names](#how-to-use-name-attr) and maps to the [Setting Object](#SettingModel) for that setting. This is used a lot for calling to update a value and then recursively update their dependents. Or is used to save the newly calculated settings from the calculator

self.\_metadata: tuple([Metadata](#Metadata), Metadata)
: A tuple of [metadata](#Metadata) objects. This 0th index is the meta data from the [json defaults](#JsonDefaults), The 1st index is the meta data from the [json definitions](#JsonDefinitions). The metadata can be found at the top of any json file, default or defnition. It holds name, author, compatible materials, file type ("data" means defaults), description, etc. 

self.categories: list\[str] 
: A list of strings that are categories in this technologies json file. For example it includes the strings from "configuration", slicing_configuration", "material_cost", ..., "post_processing_cost", "total_cost" which could be found in the [json files](#JsonFilesInfo) for that technology


## Examples Section
- Can be found in the [ConfigManager](#ConfigManager)

## Notes/Warnings
- None for this class 
