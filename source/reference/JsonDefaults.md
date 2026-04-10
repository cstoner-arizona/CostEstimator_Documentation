(JsonDefaults)=

# Json Defaults

How to set json defaults based on different types of settings

The layout of the `tech_name_default.json` file is **exactly** the same as the `tech_name_def.json` file. The only difference that all the [definition dictionaries](#init-setting-json-def-example) get replaced with the default value for that setting. 

Currently almost no settings are `"type": int` besides "batch_size" in all technologies. So that means most of the data you see in defaults are floats (e.g. `"melt_allowance_factor": 1.2`)

All of the default data in the jsons were based off of a Excel Spread sheet that Alfred -- our material scientist -- created. 

# When modifying defaults, consider
For all examples I will be using `CostEstimator/config/resources/data/defaults/binder_jetting_def.json`

When you are modifying the defaults you must consider the type of the setting. 

If the type is 
- "Int"
	- Then you must set the default value to be an integer python type. That means no leading decimal places
	- e.g. `"batch_size": 1`
- "Float"
	- Then you must set the default value to be a float python type. That means there **must** be at least 1 number after a decimal
	- e.g. `"stl_printed_region_volume": 0.0`
	- e.g. ""
