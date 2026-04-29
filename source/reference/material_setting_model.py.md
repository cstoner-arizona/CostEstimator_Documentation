(MaterialSetting)=
# Material Setting Model
- **CostEstimator/config/models/materials/material_setting_model.py**
- This class will extend the [Setting](#SettingModel) class which provides the base level for what every setting should have. 
- This class will provide functionality for a setting object having different values for different available materials
- This is important for settings like "specific_energy_required_to_melt_metal" which will have a different kWh/kg for every material used. 
- We want this functionality so that the plugin can be more versatile for the users needs who want to use a specific supported material 
- This class is a dataclass, meaning we can define methods as `@property`{l=python} which act as attributes. e.g. `matSettingObj.value = 10 # does type validation in source code`{l=python}

## Inherits
[Setting](#SettingModel): This gives the base level needs of every setting. Name, dependents, type, formula, user_defined, min/max, unit, etc


## Purpose/Motivation

- What problem does this solve?
	- This class was made as a feature request to support multiple materials for a type of additive manufacturing technology. Supporting multiple materials is handy because it allows the user to get a more specific quote on their model, by allowing small (or large) changes in settings and computed price outputs. 
- When would someone use this?
	- When someone is adding a new setting to the plugin that will make price estimation more accurate and that setting can have different values based on the material chosen, they will use this object to store that settings data

## Key Methods/Functions
update_material_selection(material_name)
: This function will change the [material_containers](#material_container_attr) selected material to be the one given as long as its a valid name of a material within the container

get_save_format()
: Returns a dictionary of the setting name, mapped to a dictionary of the material types names mapping to their value. Dict\[settingName, Dict\[matName, matValue]]

revert()
: Changes all the values of the [material container](#material_container_attr) back to their original unchanged values, and updates is modified back to false 

set_calculated(calculated_value, override_original)
: This function probably isnt called because it doesnt make sense for a material setting to be calculated. Besides that this will attempt to set the new value of the currently selected material to the value given. Then it will determine if the new value is a actual different value before setting `self.is_modified` to true. 

\_\_getitem\_\_(item)
: it returns the value of the material name given, if the material name given is a selectable material for this material setting. 
:::{note}
Example: CostEstimator/config/resources/data/[defaults](#JsonDefaults)/investment_casting_default.json
calling `matSettingObj["316_l_stainless_steel"]`{l=python} on this material setting object below would return `7990`
```json
"casting_metal_density": {
      "alsi10mg": 2670,
      "alsi7mg0.6": 2680,
      "316_l_stainless_steel": 7990,
      "17-4_ph_stainless_steel": 7800,
      "in718": 8190,
      "in738": 8110,
      "in625": 8440
    }
```
:::

\_\_setitem\_\_(key, value)
: This will check that the key is "value" and then it will update the currently selected materials value in the [material container](#material_container_attr)

\_\_repr\_\_()
: Returns debug string for the class

\_\_str\_\_()
: Create a string from the [setting](#SettingModel)

## Important Attributes/Properties
{#material_container_attr}
`self.material_container`{l=python}
: This is a [MaterialsModel](#MaterialsModel) type. This is important because it will hold the mappings of selectable materials to their values, in addition with the currently selected material. You can think of it as window pane. It allows you to see the current selected material in the window, then you can call on it to change what is in the window and it will return the value from now on.

`self.value`{l=python} = float, int, [SettingRange](#SettingRange)
: This returns the value of the currently selected material. 
: You can also set this value using `matSettingObj.value = something`

`self.original_value`{l=python} = float, int, [SettingRange](#SettingRange) 
: This returns the original value of the currently selected material
: You can also set this value using matSettingObj.original_value = something. Which will check if the material is modified or not after this change.

`self.selectable_materials`{l=python}
: This returns a list of the names of selectable materials for this specific material setting 
:::{note}
Example: CostEstimator/config/resources/data/[defaults](#JsonDefaults)/investment_casting_default.json
calling `matSettingObj.selectable_materials` on this below would produce a list of strings \["alsi10mg", "alsi7mg0.6", ..., "in738", "in625"]
```json
"casting_metal_density": {
      "alsi10mg": 2670,
      "alsi7mg0.6": 2680,
      "316_l_stainless_steel": 7990,
      "17-4_ph_stainless_steel": 7800,
      "in718": 8190,
      "in738": 8110,
      "in625": 8440
    }
```
::: 

## Examples Section
* CostEstimator/config/models/[technology_model.py](#TechnologyModel)
```python
 def _handle_material_dependent_setting(
        self,
        category: str,
        setting_name: str,
        setting_value: Any,
        setting_schema: dict[str, Any],
        expected_type: str,
    ) -> None:
        """Handle material dependent settings."""
        if expected_type == "range":
            setting = self._create_material_range_setting(
                category, setting_name, setting_value, setting_schema
            )
        else:
            setting = self._create_material_setting(
                category, setting_name, setting_value, setting_schema
            )

        if setting:
            self.settings[setting_name] = setting
```
This shows that we have to initialize material settings differently. The creation of the setting object doesnt happen until one of those nested function calls. Lets look at the normal setting -- which assumes the value is a float or int.
```python
def _create_material_setting(
        self,
        category: str,
        setting_name: str,
        setting_value: Any,
        setting_schema: dict[str, Any],
    ) -> MaterialSetting:
        """Create a material-dependent setting."""
        return MaterialSetting(
            self.type, setting_name, category, setting_value, setting_schema
        )
```


## Notes/Warnings
None can be thought of. 