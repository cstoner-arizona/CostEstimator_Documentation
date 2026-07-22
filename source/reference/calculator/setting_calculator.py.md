(SettingCalculator)=
# SettingCalculator
- This class was made so the [Technology](#TechnologyModel) did not have to implement the logic of figuring out what Specific type of calculator was needed to be created for that specific technology model. 
- This class will be held as a [self.calculator](#TechnologiesSelfCalculator) attribute of the [Technology](#TechnologyModel) object. and when the technology object wants to use calculator methods it will call __this__ classes methods which in return call the **actual** [calculator](#BaseCalculator) class. 
- Think of it like this `Technology -> SettingCalculator <Interface> -> SpecificCalculator object that inherits Base.py` 


## Purpose/Motivation

- What problem does this solve?
	- This class was created because we didnt want the bloated switch case for creating the specific technology inside the Technology Model.

- When would someone use this?
	- They would be required to use this interface styled class inside the Technology Interface 

## Basic Usage Example

- A simple, realistic code snippet showing the most common way to use it (keep it short, just enough for the basic idea)
{lineno-start=1 emphasize-lines="13,16,19"}
```python
# CostEstimator/config/models/technology_model.py
def __setitem__(self, setting_name, value, /):
	"""
	... truncated for example ... 
	"""
	Logger.log( ..truncated..)

	if setting_name not in self.settings:
		raise SettingNotFoundError(self.type, setting_name)
	self.settings[setting_name]["value"] = value

	# pass the current settings to the calculator
	self.calculator.update_settings(self.settings)  

	# tell calculator to recalculate dependants
	self.calculator.recalculate_dependants(setting_name, False)

	# now pull back the updated settings
	self.settings = self.calculator.get_settings()

```


## Key Methods/Functions
```{eval-rst}

.. py:method:: __init__(printer_type: str, settings: Dict[str, Setting])

   Initializes the SettingCalculator instance and selects the appropriate calculator based on the printer type. We call this appropriate calculator  ":ref:`inner calculator <inner-calculator>`" throughout the functions. 

   :param str printer_type:  The type of printer for which calculations are performed.
   :param Dict[str, Setting] settings: Dictionary mapping setting names to their Setting objects.
   
   :raises ValueError: When the printer type name given does not match the ones in the config module
   
   
   
.. py:method:: recalculate_dependants(self, setting_name: str, override_original: bool) 
    :no-index:
   
    This function will be given an assumed user defined setting and it will call on a recursive function inside the :ref:`Base calculator <BaseCalculator>` to handle all of the recalculating
    
    :param str setting_name: The name of any setting. It might have other settings relying on it 
    :param bool override_original: This argument is used for when initialization of the plugin is happening (it'll be True) or when a user loads their own settings (it'll be True). this argument will override the original value stored in the settings that are calculated. 
    

    
.. py:method:: get_settings(self)
	
	
	This method will return the inner calculated settings dictionary 
	
	:return: A dictionary of Setting names (str) mapping to the :ref:`Settings <SettingModel>` (:ref:`Setting <SettingModel>` ) from the :ref:`actuall <BaseCalculator>` calculator.
	:rtype: Dict[Str, Setting]
	
	

.. py:method:: update_settings(self, current_settings: Dict[str, Setting]))

	This will call the :ref:`inner calculator <SpecificCalculator>` s `update_settings(current_settings)` which will simply create a copy of the settings passed in from the :ref:`technology <TechnologyModel>` and store it. This class DOES NOT do the storing, im only describing what the inner caclulator would do
	
	:param dict[str, Setting] current_settings: This is a map of setting names to their :ref:`Setting Objects <SettingModel>`
	
	

.. py:method:: calculate_setting_value(self, setting_name: str)

	this function will be givin a setting name that is expected to be a :ref:`Caclulated Setting <calculated-setting>` and it will call upon the :ref:`inner calculator <inner-calculator>` to calculate the setting name given. It will recursively update this settings dependencies first, then it will calculate itself after all of those are updated. 
	
	:param str setting_name: The string setting name of the setting that is wanted to be calculated again. 
	
	
.. py:method:: rerun_initialization_on_gui_reopen(self)
	See issue #101 in github
        This function will tell the actual calculator to initialize its values again after the user opened the Plugin for its 2+ time. This function will be called because after the technology resets all of its slice first = true settings to zero it should recalculate any and all settings to what they would show if the user just launched cura and launched the plugin for the first time.

        A key example is Powder bed fusion "Machine Cost Per part" on the first launch is 80 - 1800 for some reason. Keep in mind at this point the user hasnt even loaded in a part. Its just like that. When working on issue #101 I want to make sure that the values -- even if weird -- are the exact same as if they launch it the first time.
```



## Important Attributes/Properties

{#inner-calculator}
self.calculator 
: Its type could be any of the specific calculators inheriting from [base calculator](#BaseCalculator). BinderJettingCalculator, DlpCalculator, LpbfCalculator, InvestmentCalculator, SandCastingCalculator, MachiningCalculator, PrinterPatternInvestmentCalculator.
: Each of the specific calculators has its own [dispatch table](#DispatchTable) which mapps setting names for that calculator to the function that will update that setting in the settings held in this calculator

  

## Examples Section
{lineno-start=1 emphasize-lines="14,17"}
```python
# CostEstimator/config/models/technology_model.py
def process_STL_inputs(self, new_stl_input_data: dict[str, float]) -> None:
	"""
	.. truncated for example ..
	"""
	# .. truncated for example ..
	for stl_setting_name in new_stl_input_data:
		# we pull the new stl data
		new_stl_value: float = new_stl_input_data[stl_setting_name]
		# we put the new value in the setting name
		self.settings[stl_setting_name]["value"] = new_stl_value
		
		# then we pass the new settings data to the calculator so it has the most up to date info
		self.calculator.update_settings(self.settings)

		# Recalculate all the dependants of the stl input variable
		self.calculator.recalculate_dependants(stl_setting_name, False)
```
This examples shows that **within the Technology Class** we are **always** setting calculator methods, and it gives an example of a usage for calling. 
`recalculator_dependants()`{l=python} which is used on initilization of the STL inputs (and it other places too)

## Notes/Warnings
- This file (`setting_calculator.py`) has a inner `class config(Enum)` class which is used for mapping the technology names that are stored within in the [metadata](#Metadata) of each [json file](#JsonFilesInfo). So whenever a json file has its technology name changed then it will need to also be updated inside this config. If they are not updated to match then the switch case used for generating the technology model specific calculator will not create a calculator. 
