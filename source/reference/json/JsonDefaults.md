(JsonDefaults)=

# Json Defaults

How to set json defaults based on different types of settings

The layout of the `tech_name_default.json` file is **exactly** the same as the `tech_name_def.json` file. The only difference that all the [definition dictionaries](#init-setting-json-def-example) get replaced with the default value for that setting. Make sure that the layout of the categories and each setting are just like the [json definition](#JsonDefinitions) file. 

Currently almost no settings are `"type": int` besides "batch_size" in all technologies. So that means most of the data you see in defaults are floats (e.g. `"melt_allowance_factor": 1.2`)

All of the default data in the jsons were based off of a Excel Spread sheet that Alfred -- our material scientist -- created. 

## When modifying defaults, consider
For all examples I will be using `CostEstimator/config/resources/data/defaults/binder_jetting_def.json`

When you are modifying the defaults you must consider the type of the setting. 

{#how-to-set-each-default-setting-type}
If the type is 
- "int"
	- Then you must set the default value to be an integer python type. That means no leading decimal places
	- e.g. `"batch_size": 1`
- "float"
	- Then you must set the default value to be a float python type. That means there **must** be at least 1 number after a decimal
	- e.g. `"stl_printed_region_volume": 0.0`
	- e.g. `""melt_allowance_factor": 1.2,"`
- "range"
	- Then you must set the default value to be a list with **only** 2 values, a min and a max. 
	- It is **important that the min and max have the same types**. If one has any decimal points then the other must have at least a leading `.0` at the end. This is because the validator confirms that a ranges type is either a float or a int and it uses the types of these defaults to set its type.
	- The minimum value must be the first value in the list
	- The maximum value must be the second value in the list 
- "bool"
	- This is rare to see but if you do have a boolean type, make sure the json is typed with a lowercase `false`.
	- e.g. ""is_user_created": false"

{#setting-material-dependent-default}
### When working with material dependent setting defaults
1. You must have the value of the defaults be a dictionary. 
2. The dictionary will be filled with keys that are the name of the materials it depends one.
3. The dictionary values will be the default for that setting and that setting specific material. 
4. Remember that the [type of that setting](#how-to-set-each-default-setting-type) should match for all defaults values for all specific materials. 
Example
```json
"unit_metal_cost": {
      "alsi10mg": 50.0,
      "alsi7mg0.6": 80.0,
      "316_l_stainless_steel": 7.0,
      "in625": 45.0
    }
```
So this setting has the type of "float" because a user will be able to enter up to 2 decimals (Determined [here](#how-to-use-decimal-attr)). So each and every material should have a value that matches with the settings type. If not the validator will not allow the plugin to run. 
