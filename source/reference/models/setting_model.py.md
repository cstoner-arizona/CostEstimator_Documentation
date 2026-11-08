(SettingModel)=
# Setting Class
- **CostEstimator/config/models/setting_model.py**
- This object is used to hold setting data. The word "Setting" in this context is referring to the user inputed/ non-user inputed settings in the Cost Estimator GUI. An example is the "Furnace Lifetime" of Binder jetting technology tab. This Setting object will hold the type: range, if its user defined: true, the min and max input if its user defined=true. This holds the actual current data value of the setting. That is what this class is used for, hold, represent, and collect all a settings meta data along with its value. 

- This class is a dataclass, meaning we can define methods as `@property`{l=python} which act as attributes. e.g. `settingObj.value = 10 # does type validation in source code`{l=python}


## Purpose/Motivation

- What problem does this solve?
	- Having a setting class allows us to have multiple differing types of setting data. Ranges can be represented by interfacing with a [SettingRange](#SettingRange) object while integers can just as easily be stored. Whatever the needs of a setting, the setting object will work with it.

- When would someone use this?
	- Someone would use this when they are checking the type of a setting to determine if they want to have two boxes for input on a range setting through the GUI, or when they need to get a settings value to do computation.

## Basic Usage Example

- A simple, realistic code snippet showing the most common way to use it 

```python
for setting_name, setting_obj in settings.items():
# if the setting is dependant on other settings, save that relationship in this dependency tracker
if setting_obj.depends_on != None:
self.dependencies[setting_name] = setting_obj.depends_on
```

This checks if a setting object has a `depends_on` list. If it does it will save its dependencies to a dictionary. The key point is that the `.depends_on`{l=python} property is called and is defined to return None if it doesn't have it in the [json definition](#JsonDefinitions). 

## Key Methods/Functions

```{eval-rst}

.. py:function:: set_calculated(calculated_value, override_original)

   Sets this setting object's value to the new calculated value provided.

   If ``override_original`` is ``True``, the original value will also be overwritten.
   Overwriting the original is appropriate when loading settings from a user file,
   on Cost Estimator plugin initialization, or when STL inputs are loaded.

   .. note::
      This function assumes it is only called on settings marked as ``user_defined=false``
      in the JSON definitions.

   :param calculated_value: The new calculated value to assign to this setting.
   :param bool override_original: If ``True``, overwrites the original value in addition
       to the current value.
   :return: None


.. py:function:: validate()

   Raises an error if any validation errors exist for this setting, otherwise does nothing.

   .. seealso::
      Uses :ref:`SettingValidator` to check for errors.

   :return: None
   :raises ValueError: If the setting has validation errors.


.. py:function:: validate_new_value(value)

   Validates a given value against this setting without modifying ``self.value``.

   Behaves identically to :func:`validate` except it passes ``value`` to the
   :ref:`SettingValidator` rather than using ``self.value``.

   :param value: The candidate value to validate.
   :return: None
   :raises ValueError: If the provided value fails validation.


.. py:function:: revert()

   Reverts this setting to its original value and clears its modified flag.

   Sets ``self.value = self.original_value`` and ``self.is_modified = False``.

   :return: None


.. py:function:: get_save_format()

   Returns a dictionary representation of this setting suitable for writing to JSON.

   :return: A dictionary mapping the setting name to its value.
   :rtype: Dict[str, str | float | bool | List[int | float]]


.. py:function:: __setitem__(key, value)

   Enables dictionary-style assignment for a setting's ``name`` or ``value``.

   Performs type checking against the setting's original type before applying
   the new value. For example: ``settingObj["value"] = 10.0`` or
   ``settingObj["name"] = "newSettingName"``.

   :param str key: The attribute to set; must be ``"value"`` or ``"name"``.
   :param value: The new value to assign. Must match the expected type for the given key.
   :return: None
   :raises KeyError: If ``key`` is not a recognized attribute of the setting.
   :raises ValueError: If the type of ``value`` does not match the schema or expected type.


.. py:function:: reset_to_zero()

   Resets this setting's current value, original value, and modified flag to zero.

   Used to clear slice-first settings (``slice_first=True``) back to zero when
   the user reloads the plugin, preventing stale STL values from a previous session
   from persisting.

   :return: None
```
  

## Important Attributes/Properties
`type: str`{l=python}
:  Holds a string representation of the setting type just as its found in the [json definition](#JsonDefinitions)

value: float | int | str | bool | SettingRange`{l=python}
: Holds the current value of the setting
:::{seealso}
[SettingRange](#SettingRange)
:::

`is_editable: bool | None`{l=python}
: A direct mapping to the [json definition](#JsonDefinitions) `"user_defined"` attribute. Assumed to always exist, but returns None if it doesn't

`slice_first: bool | None`{l=python}
: A direct mapping to the [json definition](#JsonDefinitions) `"slice_first"` attribute. If it doesn't exist for a setting then it returns None

`description: str | None`{l=python}
:  A direct mapping to the [json definition](#JsonDefinitions) `"description"` attribute. Assumed to always exist, but returns None if it doesnt

`units: str`{l=python}
:  A direct mapping to the [json definition](#JsonDefinitions) `"unit"` attribute. Returns empty string if it doesn't exist 

`min: int | float | None`{l=python}
: A direct mapping to the [json definition](#JsonDefinitions) `"min"` attribute. Returns the minimum value -- or min length if type=str -- of the setting. Returns None if it doesn't exist

  

`max: int | float | None`{l=python}
: A direct mapping to the [json definition](#JsonDefinitions) `"max"` attribute. Returns the maximum value -- or max length if type=str -- of the setting. Returns None if it doesn't exist

`decimal: int | None`{l=python}
: A direct mapping to the [json definition](#JsonDefinitions) `"decimal"` attribute. Returns the number of decimal places for a float -- and range if it contains float -- types.

`dropdown_options: list[str] | None`{l:python}
: Returns a list of dropdown options. A direct mapping to the [json definition](#JsonDefinitions) `"options"` attribute. If `self.type!="dropdown"`{l=python} it returns none. 
:::{note}
dropdown_options is not currently used, but if used there should be little changes to get it to work throughout the CostEstimator
:::

`formula: str | None`{l=python}
: If called on a calculated setting, it returns the formula this setting is defined by. A direct mapping to the [json definition](#JsonDefinitions) `"formula"` attribute. Returns None if the setting does not have a `"formula"` json definition attribute

`is_modified: bool`{l=python}
: When a user changes a setting in the GUI this is changed to be `True` and will -- through various connections to pyqt -- enable the "Save Changes" button to light up and be enabled.



  

## Examples Section
- Blank

## Notes/Warnings
- Possible future implementation: the `self.formula`{l=python} attribute could be parsed and used to calculate the setting and replace the thousands of lines in the `CostEstimator/config/calculator` module 

- No matter what, if a setting that is `"slice_first=true"` it will override the original value when setting a new value to this setting. This is because when the config module receives the new STL values from the [Estimator](#Estimator) module, those values should be considered the originals (in my opinion). 

:::{seealso}
You can learn how the Config module receives the new STL values from the Estimator module here at [HowConfigReceviesSTLData](#HowConfigReceviesSTLData) 
:::