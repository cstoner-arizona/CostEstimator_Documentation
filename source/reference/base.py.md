(BaseCalculator)=
# BaseCalculator
- **CostEstimator/config/calculator/backends/base.py**
- This class is the abstract parent class to every specific type of calculator. 
- This abstract class provides the base functionality for every specific technology calculator. The base functionality will be the same for every technologies calculator. For example the recalculation of dependents will be the same throughout all technology types so that functionality will be in this class.

## Inherits
ABC (Abstract Class)


## Purpose/Motivation
- What problem does this solve?
	- A lot of duplicated code between the Specific classes for each technology type so we put all of the shared functionality into this class, which is then inherited into the specific technologies classes.

- When would someone use this?
	- When they are creating another technology type they would want to inherit this class to have its functionality 

## Basic Usage Example

- A simple, realistic code snippet showing the most common way to use it (keep it short, just enough for the basic idea)

```python
# CostEstimator/config/calculator/backends/binder_jetting.py
class BinderJettingCalculator(BaseCalculator):
    """
    Calculator for Binder Jetting printer settings.
	...
```
This shows the specific technology type calculator inheriting the base calculator

```python
# CostEstimator/config/calculator/setting_calculator.py
def recalculate_dependants(self, setting_name: str, override_original: bool):
	"""
	...truncated for example...
	"""
	self.calculator.recalculate_dependants(setting_name, override_original)
```
This is an example from the [Setting Calculator](#SettingCaclulator) that shows that for any type of `self.calculator` (which is any specific calculator type) we can call `.recalculate_dependants(setting_name, override_original)`{l=python}

## Key Methods/Functions
\_\_init\_\_(printer_type, settings):
: The init of this base.py will accept the printer type as a string and a dictionary that maps setting names to their corresponding setting objects. 
: Then it creates a copy of the settings for itself to hold onto and it builds a dependency tracker of the settings dependents and dependency. 
: Then it finds what settings are calculated settings and saves tho 

recalculate_dependants(setting_name, override_original):
: This function is called when [technology](#TechnologyModel)s `__setitem__` is called with a new settings value.
: The reason is because, now that setting has a new value, so this function will loop over the settings that are dependent on the updated setting and call to update those settings so that the new value takes effect on all dependent settings. 

update_settings(settings):
: Creates and stores a copy of the settings (dict\[str, Setting]) passed in, recalculates the calculated settings, then now the settings are updated.

get_settings(): Dict\[str]\[Setting]
: This function just returns the current settings that are stored in this calculator

calculation_logger(many params):
: This function just sends out a log message of the new calculation result

calculate_setting(setting_name, override_original) [Setting](#SettingModel):
: This function will be given a calculated setting and it will make sure that setting
: is a valid calculated setting, then it will call to [another function](#recursively_update_setting) to recursively update all
: of this settings dependencies and then finally calculate this function. 

{#recursively_update_setting}
f


## Important Attributes/Properties


- What can the user access or modify?

  

## Examples Section
- More detailed usage examples (Show the common patterns)

## Notes/Warnings

- Edge cases, performance considerations, gotchas, commit mistakes people can make 
