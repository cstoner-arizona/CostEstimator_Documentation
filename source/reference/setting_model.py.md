(SettingModel)=
# Setting

- This object is used to hold setting data. The word "Setting" in this context is referring to the user inputed/ non-user inputed settings in the Cost Estimator Gui. An example is the "Furance Lifetime" of Binder jetting technology tab. This Setting object will hold the type: range, if its user defined: true, the min and max input if its user defined=true. This holds the actual current data value of the setting. That is what this class is used for, hold, represent, and collect all a settings meta data along with its value. 

- This class is a dataclass, meaning we can define methods as `@property`{l=python} which act as attributes. e.g. `settingObj.value = 10 # does type validation in source code`{l=python}

  

## Purpose/Motivation

- What problem does this solve?
	- Having a setting class allows us to have multiple differing types of setting data. Ranges can be represented by interfacing with a [SettingRange](#SettingRange) object while integers can just as easily be stored. Whatever the needs of a setting, the setting object will work with it.

- When would someone use this?
	- Someone would use this when they are checking the type of a setting to determine if they want to have two boxes for input on a range setting through the GUI, or when they need to get a settings value to do computation.

  

## Basic Usage Example

- A simple, realistic code snippet showing the most common way to use it (keep it short, just enough for the basic idea)

```python
for setting_name, setting_obj in settings.items():
# if the setting is dependant on other settings, save that relationship in this dependency tracker
if setting_obj.depends_on != None:
self.dependencies[setting_name] = setting_obj.depends_on

```

This checks if a setting object has a `depends_on` list. If it does it will save its dependencies to a dictionary. The key point is that the `.depends_on`{l=python} property is called and is defined to return None if it doesn't have it in the [json scema](#JsonScema). 

## Key Methods/Functions

set_calculated(calculated_value, override_original): 
: Given a new calculated value it sets this setting objects value to be the new value given. If `override_original` is set to `True` then the original value will be overwriten. You might want to overwrite a original when you are settings file from the user, or on CostEstimator plugin initialization, or when STL inputs are loaded because it makes sense for them to be loaded as originals. 
: This function assumes  it is only called on settings marked as `user_defined=false` in the [json definitions](#JsonDefinitions). 

  

validate():
: This function will do nothing besides raise an error whenever we try to validate this setting and there were errors. 
:::{seealso}
This uses the [SettingValidator](#SettingValidator) to check for errors.
:::

validate_new_value(value):
: Works just like `validate()` above but instead of pulling the self.value when calling the [SettingValidator](#SettingValidator) it will pass in the `value` given. 
  
revert():
: This function will set the `self.value = self.original_value`{l=python} and `self.is_modified = False`{l=python} 

get_save_format(): -> `Dict[str, str|float|bool| List[int|float] ]`
: This returns a dictionary mapping the setting name to its value to be suitable for writing to json 

`__setitem__(key,value)`:
: This will allow a dictionary type of notation when changing a settings name or value e.g. `settingObj["value"] = 10.0`{l=python}. This function will do type checking against its original given type and what the new `value` givens type is before setting `self.value`{l=python} to the new value. Same for `settingObj["name"] = "newSettingName"`{l=python}
: This function raises KeyError, or ValueError if the types of the inputs don't match the schema or expected type of the setting

  

## Important Attributes/Properties
`type: str`{l:python}
:  Holds a string representation of the setting type just as its found in the [json definition](#JsonDefinitions)

value: float | int | str | bool | SettingRange`{l:python}
: Holds the current value of the setting
:::{seemore}
[SettingRange](#SettingRange)
:::

`is_editable: bool | None`{l:python}
: A direct mapping to the [json definition](#JsonDefinitions) `"user_defined"` attribute. Assumed to always exist, but returns None if it doesn't

`slice_first: bool | None`{l:python}
: A direct mapping to the [json definition](#JsonDefinitions) `"slice_first"` attribute. If it doesn't exist for a setting then it returns None

`description: str | None`{l:python}
:  A direct mapping to the [json definition](#JsonDefinitions) `"description"` attribute. Assumed to always exist, but returns None if it doesnt

`units: str`{l:python}
:  A direct mapping to the [json definition](#JsonDefinitions) `"unit"` attribute. Returns empty string if it doesn't exist 

`min: int | float | None`{l:python}
: A direct mapping to the [json definition](#JsonDefinitions) `"min"` attribute. Returns the minimum value -- or min length if type=str -- of the setting. Returns None if it doesn't exist

  

`max: int | float | None`{l:python}
: A direct mapping to the [json definition](#JsonDefinitions) `"max"` attribute. Returns the maximum value -- or max length if type=str -- of the setting. Returns None if it doesn't exist

`decimal: int | None`{l:python}
: A direct mapping to the [json definition](#JsonDefinitions) `"decimal"` attribute. Returns the number of decimal places for a float -- and range if it contains float -- types.

`dropdown_options: list[str] | None`{l:python}
: Returns a list of dropdown options. A direct mapping to the [json definition](#JsonDefinitions) `"options"` attribute. If `self.type!="dropdown"`{l=python} it returns none. 
:::{note}
This is not currently used, but if used there should be little changes to get it to work throughout the CostEstimator
:::

`formula: str | None`{l:python}
: If called on a calculated setting, it returns the formula this setting is defined by. A direct mapping to the [json definition](#JsonDefinitions) `"formula"` attribute. Returns None if the setting does not have a `"formula"` json definition attribute

`is_modified: bool`{l=python}
: When a user changes a setting in the GUI this is changed to be `True` and will -- through various connections to pyqt -- enable the "Save Changes" button to light up and be enabled.


- What can the user access or modify?

  

## Examples Section
- More detailed usage examples (Show the common patterns)

## Notes/Warnings

- Edge cases, performance considerations, gotchas, commit mistakes people can make 

- Possible future implementation: the `self.formula`{l=python} attribute could be parsed and used to calculate the setting and replace the thousands of lines in the `CostEstimator/config/calculator` module 

- No matter what, if a setting that is `"slice_first=true"` it will override the original value when setting a new value to this setting. This is because when the config module receives the new STL values from the [Estimator](#Estimator) module, those values should be considered the originals (in my opinion). 

:::{seealso}
You can learn how the Config module receives the new STL values from the Estimator module here at [HowConfigReceviesSTLData](#HowConfigReceviesSTLData) 
:::