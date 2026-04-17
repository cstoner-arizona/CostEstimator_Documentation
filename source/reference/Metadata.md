(Metadata)=
# Metadata Model
- This class provides a simply way to get out each part of the metadata found at the top of [both json files](#JsonFilesInfo)
- This class is a dataclass so we can define methods as "properties" which can be called like attributes of a class -- meaning with no `()` at the end. 


## Purpose/Motivation

- What problem does this solve?
	- Having to store the metadata as a dictionary we do not get any 'on-hover' hints on what is in it, but with the Metadata class we can see the available getter methods

- When would someone use this?
	- When they want to get the type of a technology json file, or get the author of the [json file](#JsonFilesInfo), or get the compatible_materials to help create a [MaterialSetting](#MaterialSetting)

## Key Methods/Functions
as_dict: Returns the dictionary format of the meta data


## Important Attributes/Properties
**Keep in mind, all this data is populated by the "metadata" dictionary at the top of** [each json file](#JsonFilesInfo)

self.type = the technology name. e.g. "Binder Jettting", "Machining"

self.file = "data" if its the [defaults json](#JsonDefaults), "definition" if its the [definitions json](#JsonDefinitions) 

self.is_user_created = boolean if the json file was first customized int he plugin, then they pressed "save file" then later in that file it would have **true** for this field in the metatdata

self.version = version number for the json file 

self.description = description of the json file

self.author = the author of the json file 

self.company = the company that created the json file

What can be modifed?
- Nothing should really be modified unless another developer overhauls a json file and they should change the company, author, version

## Examples Section
- More detailed usage examples (Show the common patterns)
CostEstimator/config/resources/data/[defaults](#JsonDefaults)/printer_pattern_investment_default.json
```json
"metadata": {
    "type": "Printed Pattern Investment Casting",
    "file": "data",
    "is_user_created": false,
    "version": "1.0",
    "description": "Default settings for Printer Pattern Investment (FDM) analysis",
    "author": "C. Stoner",
    "company": "CIMLab of University of Arizona, CADCAST",
    "compatible_materials": {
      "FDM": [
        "PLA",
        "ABS",
        "Nylon",
        "PC"
      ],
      "slurry": [
        "suspended_slurry"
      ],
      "metals": [
        "alsi10mg",
        "alsi7mg0.6",
        "316_l_stainless_steel",
        "17-4_ph_stainless_steel",
        "in718",
        "in738",
        "in625"
      ]
    }
	}
```

## Notes/Warnings
- Edge cases, performance considerations, gotchas, commit mistakes people can make 
