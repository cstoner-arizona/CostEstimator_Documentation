(ConfigManager)=
# ConfigManager
- **CostEstimator/config/config_manager.py**
- This class manages the connection between PyQt6 GUI objects seen in the plugin within the configuration page and the internal data structures (e.g. [Technology Model](#TechnologyModel))

## Inherits
[QObject](https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtcore/qobject.html#QObject)
- Utilizes PyQt6 framework to create signals and slots that are used in connection to the GUI items

## Purpose/Motivation

- What problem does this solve?
  - The problem this solves is the creation of a GUI for the plugin that allows users to edit data relating to the estimation process.
	- This creates the configuration window GUI in which users can configure relevant data for each respective printing technology type which will be used in the estimation process.

- When would someone use this?
	- This class is only used once within the main [CostEstimator](#CostEstimator) where it is linked to Cura and ready to be utilized by users using the plugin.

## Basic Usage Example

- This is an example of how a developer would add the [ConfigManager](#ConfigManager) to Cura and link the relevant QML Component (TODO: Link Relevant QML Component)

```python
...
self._config_window_qml = os.path.join(
  os.path.dirname(os.path.abspath(__file__)),
  "config",
  "resources",
  "qml",
  "PrinterConfigWindow.qml"
)
self._config_manager = ConfigManager()
# Requires Path to QML File and QObject
self._config_window = self._application.createQmlComponent(
  self._config_window_qml,
  {"configManager": self._config_manager}
)
...
```


## Key Methods/Functions

The functions utilized are mostly QML Slots that are triggered by GUI elements. Whenever something utilizes the `@pyqtSlot` decorator, it is most likely only ever used within the relevant QML for the config window.

### Init

A large number of activities happen upon initialization that it requires its own section.

### Functions

```{eval-rst}
.. py:function:: create_technology_models(data_dict: Dict[str, dict], schema_dict: Dict[str, dict])

   *Decorated with* ``@staticmethod``

   Creates :ref:`TechnologyModel` instances for each technology type using provided data and schema dictionaries.

   :param Dict[str, dict] data_dict: Dictionary mapping technology types to their data. 
   :param Dict[str, dict] schema_dict: Dictionary mapping technology types to their schemas.
   :return: Dictionary of technology type to Technology instance, or None if no models created.
   :rtype: Dict[str, Technology] or None
   :raises ValueError: If data_dict or schema_dict is empty, or if a technology type in data_dict is not present in schema_dict.
   :raises TypeError: If data_dict or schema_dict are not a dictionary, or if an invalid technology type is encountered.
   
   
.. py:function:: process_STL_inputs(new_stl_input_data: dict[str, float])

   Processes STL input data by forwarding it to the currently selected technology.

   Called from ``Config_api.py`` after the estimator passes sliced STL file data
   into ``config_api.inputSTLData()``. The data is then forwarded to the currently
   selected technology to update its relevant settings.

   .. note::
      This function assumes the dictionary given has the proper types for all keys and values.

   :param dict[str, float] new_stl_input_data: STL setting names as keys and their
       corresponding sliced float values.
   :return: None


.. py:function:: reset_all_slice_first_settings_to_zero()

   Resets all slice-first JSON settings to zero across every technology.

   Iterates over all technologies and calls ``reset_slice_first_settings_to_zero()``
   on each, then calls ``refreshSettings()``. This ensures STL values from a previously
   calculated part do not persist when the Cost Estimator plugin is reopened, even if
   the same part is reloaded.

   .. seealso::
      GitHub Issue #101

   :return: None
```

### QML Slots

Contains both getters and setters which are triggered from the QML component.
Getters will get data from various data structures (mostly [Technology](#TechnologyModel)) in order to populate the QML with information such as printer technology types that are selectable, the categories (e.g. "machine_cost", "material_cost") of data within each technology, and the individual parameter values with their names.
Setters will set data from a QML based input such as the dropdown box for selectable materials (e.g. "In718", "FDM:PLA") and individual parameter values.

:::{note}
:name: qml-slot-annotations
QML Slots require their own decorator/annotation in order to be used by QML. This reference will detail both the `@pyqtSlot` and the function definition.
:::

:::{seealso}
:name: seealso-qvariant
:class: dropdown
The type `QVariant` is used within the `@pyqtSlot` decorator syntax as a way to unionize Python logic with C++ objects that PyQt6 is built off of. For example, a `list` object in Python needs to be translated to an `array` within C++ and a `QVariant` is used to account for this different. (Note that usage in `@pyqtSlot` must surround `QVariant` with `'`). See PyQt6 [`QVariant`](https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtcore/qvariant.html#QVariant) for further information.
:::

#### Getters

```{py:method} getAllCategories(tech_type: str)

*Decorated with* `@pyqtSlot(str, result='QVariant')`

Returns a `list[str]` which are category names given a valid printing technology as a string (see [hint](#hint-json-string-names) to find string names). Example of this list `["configuration","slicing_configuration","material_cost","machine_cost",...`.

```

```{py:method} getCategorySettingNames(tech_type: str, category: str)

*Decorated with* `@pyqtSlot(str, str, result='QVariant')`

Returns names of all settings in a specific category given the valid printing technology name as a string and a valid category name contained in the technology as a string.
```

```{py:method} getCategorySettingNames(tech_type: str, category: str)

*Decorated with* `@pyqtSlot(str, str, result='QVariant')`

Returns names of all settings in a specific category given the valid printing technology name as a string and a valid category name contained in the technology as a string.
```

```{eval-rst}
.. py:function:: getSettingType(tech_type: str, setting_name: str)

   *Decorated with* ``@pyqtSlot(str, str, result=str)``

   Returns a setting's type as a string given the valid printing technology name as a string and a valid setting name contained in the technology as a string.
   If no matching technology or setting name is found, then returns an empty string `""`.

   :param str tech_type: Printing technology name as a string
   :param str setting_name: Name of the setting contained in the printer technology as a string
   :return: The setting's type as a string. Will be same as defined in :ref:`hint-json-string-names`.
   :rtype: str
```

```{eval-rst}
.. py:method:: getSettingEditableStatus(tech_type: str, setting_name: str)

   *Decorated with* ``@pyqtSlot(str, str, result=bool)``

   This will check if a specific setting for a given tech type is user-editable (user defined).
   This is used to determine if they box in the config manager GUI should be editable. 

   :param str tech_type: Printing technology name as a string
   :param str setting_name: The name of the setting we want to check
   :return: True if the setting is user defined, false if not (calculated, stl, buildtime)
   :rtype: Boolean
```

```{eval-rst}
.. py:method:: getSettingDescription(tech_type: str, setting_name: str)

   *Decorated with* ``@pyqtSlot(str, str, result=str)``

   Get the description of a specific setting for a given printing type.

   :param str tech_type: Printing technology name as a string
   :param str setting_name: The name of the setting we want to check
   :return: The string description stored in the 
   :rtype: Str
```

```{eval-rst}
.. py:method:: getSettingValue(tech_type: str, setting_name: str)

   *Decorated with* ``@pyqtSlot(str, str, result='QVariant')``

   Get the value of a specific setting within a technology.

   :param str tech_type: Printing technology name as a string
   :param str setting_name: The name of the setting we want to check
   :return: The value of the setting as a QVariant. Could be Int, Float, List for ranges, or String for config settings. 
   :rtype: QVariant
```

```{eval-rst}
.. py:method:: getSettingUnits(tech_type: str, setting_name: str)

   *Decorated with* ``@pyqtSlot(str, str, result=str)``

   Get the json defined units of a specific setting within a technology.

   :param str tech_type: Printing technology name as a string
   :param str setting_name: The name of the setting we want to check
   :return: math units of the setting. (e.g. "kg" "$" "kW/hr")
   :rtype: String
```

```{eval-rst}
.. py:method:: getSettingDecimalPlaces(tech_type: str, setting_name: str)

   *Decorated with* ``@pyqtSlot(str, str, result=str)``

   Get the json defined units of a specific setting within a technology.

   :param str tech_type: Printing technology name as a string
   :param str setting_name: The name of the setting we want to check
   :return: math units of the setting. (e.g. "kg" "$" "kW/hr")
   :rtype: String
```

```{eval-rst}
.. py:method:: getSettingDecimalPlaces(tech_type: str, setting_name: str)

   *Decorated with* ``@pyqtSlot(str, str, result=int)``

   Get the number of decimal places defined within the json for a specific setting.

   :param str tech_type: Printing technology name as a string
   :param str setting_name: The name of the setting we want to check
   :return: The number of decimal places for the requested setting, or 0 if not found
   :rtype: int
```

```
.. py:method:: getSettingMinimum(tech_type: str, setting_name: str)

   *Decorated with* ``@pyqtSlot(str, str, result='QVariant')``

   Get the minimum value for a specific setting for a given printing type.

   :param str tech_type: The type of tech to query.
   :param str setting_name: The name of the setting to retrieve the minimum value for.
   :return: The minimum value of the requested setting, or 0 if not found.
   :rtype: int | float
```

```
.. py:method:: getSettingMaximum(tech_type: str, setting_name: str)

   *Decorated with* ``@pyqtSlot(str, str, result='QVariant')``

   Get the maximum value for a specific setting for a given printing type.

   :param str tech_type: The type of tech to query.
   :param str setting_name: The name of the setting to retrieve the maximum value for.
   :return: The maximum value of the requested setting, or 0 if not found.
   :rtype: int | float
```

```{eval-rst}
.. py:method:: getSettingSTLState(tech_type: str, setting_name: str)

   *Decorated with* ``@pyqtSlot(str, str, result=bool)``

   This function will help the GUI determine if it should show "Press calculate to see" or not based on if the tech_type given has up to date stl data based on wether the plugin was just opened. Once the user presses Calculate then the stl data will appear. 

   :param str tech_type: Printing technology name as a string
   :param str setting_name: The name of the setting we want to check
   :return: True if the setting name given is a STL based setting AND the technology given has received up to date STL data from the estimator tab. False if not a STL setting, False if not up to date STL data.
   :rtype: Boolean
```

```{eval-rst}
.. py:method:: getTechnologyMaterialTypes(tech_type: str)

   *Decorated with* ``@pyqtSlot(str, result='QVariant')``

   Returns a list of the material types (material groups) for the technology. For example DLP has "resin" and "metal" so it will return those in a list.

   :param str tech_type: Printing technology name as a string
   :return: A list of the material types (material groups) for that technology. e.g. ["metal","resin"]
   :rtype: QVariant
```


#### Functional Slots

```{eval-rst}
.. py:method:: saveSettings(tech_type: str)

   *Decorated with* ``@pyqtSlot(str, result=int)``

   This will save settings for a specific technology type once the user presses "Save Changes". It saves it out to the user json. The SaveLoadHandler will ask the user for the save location down the line.

   :param str tech_type: Printing technology name as a string
   :return: The status of the save, Success, Failure, Cancelled.
   :rtype: int
```

```{eval-rst}
.. py:method:: loadSettings(tech_type: str)

   *Decorated with* ``@pyqtSlot(str, result=int)``

   Within the SaveLoadHandler it will ask the user to pick a filename to load, it loads it, then returns the loaded_technoogy as a Technology object. Then this function puts that object in the dictionary of technologies. 

   :param str tech_type: Printing technology name as a string
   :return: The status of the load, Success, Failure, Cancelled.
   :rtype: int
```

:::{hint}
:name: hint-json-string-names
The string names discussed in the functions above can be found in the JSON definitions. See [JSON Definitions](#JsonDefinitions) for more details.
:::

## Important Attributes/Properties

```{eval-rst}
.. py:property:: file_service
   :type: FileService
```

### QML Signals

### QML Properties

- What can the user access or modify?

  

## Examples Section
- More detailed usage examples (Show the common patterns)

## Notes/Warnings

- Edge cases, performance considerations, gotchas, commit mistakes people can make 
![OnInitialization.png](OnInitialization.png)
