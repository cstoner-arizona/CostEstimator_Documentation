(TechnologyModel)=
# Technology Model
- This class models and stores all data needed for a specific additive manufacturing technology. (e.g. Binder Jetting Sand Casting, Machining, Traditional Investment Casting)
- This class holds the data needed for switching to different technologies on the left side in the GUI. 
- This class holds all the setting data related to its specific technology.

## Inherits
[MutableMapping](https://docs.python.org/3/library/collections.abc.html#collections.abc.MutableMapping)
- The only thing this allows the object to inherit is the ability to have the `object[key] = newVal` syntax acted upon it.
- This means we can use the `__setitem__` special function to denote the functionality of `technologyObj[settingName] = newSettingValue` to be the function we call when the user enters a new value into the GUI


## Purpose/Motivation

- What problem does this solve?
	- The problem was that we needed a way to store all the data related to a technology type. 
		- Its name (e.g. Binder Jetting)
		- Its default data for every setting (i.e the [defaults json](#JsonDefaults) file)
		- Its definition for every setting (i.e. the [definitions json](#JsonDefinitions) file)
	- We also needed ways to update setting values, override original settings, calculate settings based on just 1 technology. So that is why the technology object was made, to hold all this setting data, and calculate/update settings specific to one technology.

- When would someone use this?
	- When they want to represent a additive manufacturing technology in the plugin. They would create a technology and load the data needed from the [json file](#JsonFilesInfo), then create a related [calculator](#Calculator) object. 

## Basic Usage Example

- A simple, realistic code snippet showing the most common way to use it (keep it short, just enough for the basic idea)

```python
```


## Key Methods/Functions



## Important Attributes/Properties


- What can the user access or modify?

  

## Examples Section
- More detailed usage examples (Show the common patterns)

## Notes/Warnings

- Edge cases, performance considerations, gotchas, commit mistakes people can make 
