(SettingRange)=
# Setting Range Class
-  **CostEstimator/config/models/range_model.py**
- This class provides a data type to have a min and max value. This is used in the GUI to enter a minimum and maximum for a settings value.
- This class enables all possible math operations so when a range setting is being used in a math operation to calculate another setting the result is another range object.


## Purpose/Motivation

- What problem does this solve?
	- If we wanted settings to have a possible range then we would need to comput two operations, both the minimum and the maximum in the calculator. So instead of having all that extra code, we created this class to clean up the calculators code but to also have a data type that meant a settings value had a min and max.

- When would someone use this?
		- When someone sets the value of a setting object and the type is range then you will want to convert the list of 2 numbers given into a setting range and set that as the value attribute. 

## Basic Usage Example

- A simple, realistic code snippet showing the most common way to use it (keep it short, just enough for the basic idea)

```python
if self.type == "range"
	if not isinstance(value, SettingRange):
	    range_type = self.value.type
	    value = [self._convert_type(range_type.__name__, v) for v in value]
	    value = SettingRange(*value)
# CostEstimator/config/models/setting_model.py:: __setitem__()
```
For context `value` is a new value for a setting object that we will set the setting value to.
It is found that the setting is a range type, and if the new value isnt already a SettinRange then we should convert it. To do this we will go to the previously defined type of either int or float of the inner range type. Then convert our new value to that type. Then we set the value of this setting object to a SettingRange object.


## Key Methods/Functions
All of the following methods accept the `other` parameter of each function to be a type `SettingRange` or `int` or `float`
- Greater than and Equal to
- Greater than 
- Equal to (Only accepts SettingRange Objects as other)
- Not Equal to (Only accepts SettingRange Objects as other)
- Less than or Equal to 
- Less Than
- Add (e.g. SettingRange + 4)
- Reverse add (e.g. 4 + SettingRange)
- Sub
- Reverse Sub
- Multiplication
- Reverse Multiplication
- True Division
- Reverse True Division
- Floor Division (i.e. Integer Division)
- Reverse Floor Division
- Division Modulus
- Reverse Division Modules

to_list(): List[int]
: returns a list of min, max



## Important Attributes/Properties
`self.average`{l=python}
: it returns (min+max)/2

`self.type`{l=python}
: it returns the type of the inner min/max values (e.g. int or float)

  

## Examples Section
- More detailed usage examples (Show the common patterns)

{lineno-start=572 emphasize-lines="582,587"}
```python
# CostEstimator/config/models/technology_model::_create_range_setting()
def _create_range_setting(
    self,
    category: str,
	setting_name: str,
	setting_value: Any,
	setting_schema: dict[str, Any],
) -> Setting | None:
	"""Create a range setting from the given values."""
	if not self._validate_range_value(setting_value, category, setting_name):
		return None

	value_min, value_max = self._get_min_max(setting_value[0], setting_value[1])
	return Setting(
		self.type,
		setting_name,
		category,
		SettingRange(value_min, value_max),
		setting_schema,
	)

```
This examples shows how we create a SettingRange object

## Notes/Warnings
- Remember that the json [defaults](#JsonDefaults) for a SettingRange must be a list of numbers of the same type. 
