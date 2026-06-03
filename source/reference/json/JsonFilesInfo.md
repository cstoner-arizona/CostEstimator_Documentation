(JsonFilesInfo)=
# Json Files Info
Json Files are the back bone of this plugin. They hold all the data needed for every additive manufacturing technology included in this plugin. 

For every technology type you need a [Definition File](#JsonDefinitions) and a [Defaults File](#JsonDefaults)

## Maintenance, Updates, Changes to Json Files 
### Name changes for json settings
If the name of a json setting changes it is required to make a sweeping change to all occurrences inside the calculator of that technology. 
1. Inside the technologies type calculator, that json name is used in the dispatch table, update/calculate functions, and any functions that update settings that depend on that settings value. Make sure to change all occurrences. 
2. Make sure that the definition and default json files for that technology have the same name
==Tip:== Do `cmd + shift + f` and paste in the old name to find all places in the CostEstimator plugin that name is used and change it

### If Technology Name Changes
if the name of a technology changes in the "metadata" of a technologies definition json:
	The `config` enum in [setting_calculator](#SettingCalculator) needs to have its updated name 


## IF CHANGES TO SETTINGS, Do These!
If any changes are made to the settings needed for computations.  
This means lets say a new parameter gets added. In my case, Alfred (the material science grad student) added a new parameter to his spreadsheet that we based the entire json off of. This new setting was called "Post processing Cost Per Part" and it relied on two other settings.

Whenever a new setting gets added, currently there are 4 things that need to be updated in code. They are

1. Create a Json Definition for it ([Rules for Json Definitions here](#JsonDefinitions))
2. Create a Json Default for it ([Rules for Json Defaults here](#JsonDefaults))
3. Go through all settings that depend on this new setting and..
    1. Update the json formula attribute to have the new setting
    2. Update the json description to have the new setting
    3. Update the json depends on attribute to hav the new setting
    4. Go to this settings update function ([More about update functions here](#SettingUpdateMethod)) and add another parameter to be passed into this settings calculate function. This "another parameter" is the new setting being added.
    5. Go to this settings calculate function ([More about calculate functions here](#SettingCaculateMethod)) and add another parameter in the signature (read the end of step 4 above). And check that if this new setting is a divisor in the new formula of this setting then make a divide by zero check. Then add the new parameter to the part of the formula it belongs for this setting
4. Create a update function for this setting ([More about update functions here](#SettingUpdateMethod))
5. Create a calculate function for this setting ([More about calculate functions here](#SettingCaculateMethod))
6. Add the json name of this new setting and the function name to the dispatch table for this setting

