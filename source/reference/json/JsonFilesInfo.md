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
	The `config` enum in setting_calculator needs to have its updated name 
