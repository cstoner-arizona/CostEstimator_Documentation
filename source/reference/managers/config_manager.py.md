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
```

### QML Slots

Contains both getters and setters which are triggered from the QML component.
Getters will get data from various data structures (mostly [Technology](#TechnologyModel)) in order to populate the QML with information such as printer technology types that are selectable, the categories (#TODO Link what category names are in JSON details) of data within each technology, and the individual parameter values with their names.
Setters will set data from a QML based input such as the dropdown box for selectable materials (#TODO Add materials cross-ref) and individual parameter values.

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

:::{hint}
:name: hint-json-string-names
The string names discussed in the functions above can be found in the JSON definitions. See [JSON Definitions](#JsonDefinitions) for more details.
:::

## Important Attributes/Properties

```{eval-rst}
.. py:property:: file_service

  :type: :ref:`FileService`

  Handles file related information and IO operations to read and write to JSON.

  ```

```{eval-rst}
.. py:property:: schema_validator

  :type: :ref:`SchemaValidator`

  Handles file structure and schema validation based on recieved file paths from :py:attr:`file_service`.
```

```{eval-rst}
.. py:property:: api

  :type: :ref:`ConfigAPI`

  Initalizes the API that will be referenced and utilized by :ref:`CostEstimator`.
  The API gives external modules a interface to use to affect data structures inside :ref:`ConfigManager`.
```

```{eval-rst}
.. py:property:: _modified

  :type: bool

  Private property which holds the boolean info if the currently selected technology has
  setting values that differ from the original value.

```

```{eval-rst}
.. py:property:: _data_schema

  :type: Dict[str, dict]

  Loaded JSON deserialized data where the string key is the technology, and the value is the deserialized JSON as a dictionary.
  Specifically for the data schemas loaded from the JSON Definitions. See also :ref:`JsonDefinitions`.
```

```{eval-rst}
.. py:property:: _default_data

  :type: Dict[str, dict]

  Loaded JSON deserialized data where the string key is the technology, and the value is the deserialized JSON as a dictionary.
  Specifically for the data defaults loaded from the JSON Defaults. See also :ref:`JsonDefaults`.
```

```{eval-rst}
.. py:property:: _user_data

  :type: Dict[str, dict]

  Loaded JSON deserialized data where the string key is the technology, and the value is the deserialized JSON as a dictionary.
  Specifically for user saved data loaded from the JSON User Data. Only ever populated if user has saved JSON data in the user directory.
```

```{eval-rst}
.. py:property:: technologies

  :type: Dict[str, :ref:`TechnologyModel`]

  Main dictionary that holds the :ref:`TechnologyModel` objects.
  The key is a string which is the name of the printer technology, the value is the actual :ref:`TechnologyModel` object itself.
```

```{eval-rst}
.. py:property:: current_type

  :type: :ref:`TechnologyModel`

  The currently selected technology that is being displayed by the configuration window.
  Gets the first Technology object from :py:attr:`technologies` when initalized to automatically select the first technology.
```


### QML Signals

```{eval-rst}
.. py:signal:: currentTypeChanged

  Emits when the technology type a user has selected in the UI has changed to a new type.
  
  Attached via notify to :py:attr:`currentType` and emitted by its setter.
```

```{eval-rst}
.. py:signal:: settingsDataDiscarded

  Emits when all user modified data has been discarded back to the set previous original value.

  Attached via notify to :py:attr:`types`.
  Emitted by :py:func:`discardChanges`, :py:func:`discardAllChanges`, and :py:attr:`currentType` setter.
```

```{eval-rst}
.. py:signal:: modifiedChanged

  Emits when any technology setting's value has been altered to be different than the stored original value of the setting.
  This means any time a user changes a setting, this signal will be emitted to QML components like the save and discard button to become enabled.

  Attached via notify to :py:attr:`modified`.
  Emitted by :py:func:`set_modified`.
```

```{eval-rst}
.. py:signal:: updateSetting

  Emits when a setting values displayed in the QML settings panel insides the text boxes requires updating to the display.
  For example, this happens when a user selects a different material for their analysis from the dropdown.

  Emitted by :py:func:`setMaterialSelection`, :py:func:`setSettingValue`, and :py:func:`refreshSettings`
```

```{eval-rst}
.. py:signal:: settingsSaved

  Emits after successful saving of the setting values to a JSON.
  Only used in :ref:`CostEstimator`, connects to a function but does nothing right now.
```

```{eval-rst}
.. py:signal:: settingsLoaded

  Emits after successful loading of the setting values from a JSON.
  Only used in :ref:`CostEstimator`, connects to a function but does nothing right now.
```


### QML Properties

```{eval-rst}
.. py:property:: types

  *Decorated with* @pyqtProperty(list, notify=settingsDataDiscarded)

  QML Property which gets a list of all printer technologies from the :py:attr:`technologies` dictionary keys.

  :type: list[str]
```

```{eval-rst}
.. py:property:: currentType

  *Decorated with* @pyqtProperty(str, notify=currentTypeChanged)

  QML property which gets reaccessed when :py:attr:`currentTypeChanged` is emitted.
  This reaccessment happens within MainPrinterConfigTab.qml to be able to change the
  right side setting menu by returning the newly selected current technology type.

  :type: str
```

```{eval-rst}
.. py:property:: modified

  *Decorated with* @pyqtProperty(bool, notify=modifiedChanged)

  QML property which is a boolean that specifies whether setting value data has been modified.
  True means data has been modified from the specified original, false means all data equals the specified original.

  :type: bool
```


## Examples Section
- More detailed usage examples (Show the common patterns)

## Notes/Warnings

- Edge cases, performance considerations, gotchas, commit mistakes people can make 
