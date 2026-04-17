(MaterialsModel)=
# Materials Model
- **CostEstimator/config/models/materials/material_model.py**
- This class was added to better help support settings that had different values based on the material used 
:::{seealso}
[Material Dependent Settings](#material-dependent-setting)
:::
- This class provides a map for materials to their values, allowing for dynamic updates and retrieval of specific material values. 
- This class is basically treated as a value stored by the [MaterialSetting](#MaterialSetting) class. Remember that [MaterialSetting](#MaterialSetting) is a subclass of [Setting](#SettingModel).
- This class provides a method to point to a specific material that is selected by the user so when a [MaterialSetting](#MaterialSetting) is asked for its value during calculation, it will return the value of the currently selected material. 
- This class is a dataclass so we can define methods as "properties" which can be called like attributes of a class -- meaning with no `()` at the end. 


## Purpose/Motivation

- What problem does this solve?
	- This class was created so that a [MaterialSetting](#MaterialSetting) could have a dynamic value. The MaterialSetting would have needed a way to store the currently selected material so it can have that as its current value. Instead that logic was abstracted away to this class to be considered as a materials container window pane which returns the currently selected material and facilitate the changing of that selected material. 

- When would someone use this?
	- Inside the [MaterialSetting](#MaterialSetting) class this is used as a "material container"
	- It wouldn't be used much more of anywhere else 


## Key Methods/Functions

get_save_format(): This returns a dictionary `dict[str, float | int | List[int|float] ]` representation of the materials currently stored. It will go over all the materials and map the string name to their value. If the value is a setting range it converts it into a \[min, max] list before saving. 

set_calculated(calculated_value, override_original): This will change the value of the currently selected material to be the one given, then if the override_original is on that might me we are loading from a file so these values are the new defaults, we will change the original value to the one given and set `is_modified` to false.

revert(): Will do a deepcopy of the original_materials of this materials class and set that as the materials

\<Static>  check_if_modified(current_mats, original_mats): It will loop over the current and original material dictionaries and check if there are any different, and return true if there are differences, false otherwise. 

\_\_getitem\_\_(material_str): Returns the value of the material string given 

\_\_setitem\_\_(material_str, new_value): Sets the value of the material string to the one given 

\_\_len\_\_(): The number of materials 

\_\_str\_\_(): String representation of the selected-able materials 


## Important Attributes/Properties

self.value = Returns the current value of the currently selected material.

self.original_value = Returns the original value of the currently selected material.

self.type = Returns a type object of the current value of the currently selected material.

{#self.selected_material}
self.selected_material = Returns the string name of the currently selected material. You can also set this value by doing `self.selected_material = other_material_name`.

self.selectable_materials = Returns a list of all selectable materials.

{#self.materials}
self.materials = Returns a dictionary of the materials strings mapping to their true value. If a material maps to a setting range then it will have that [SettingRange](#SettingRange) object in this dictionary. You can also set this value by doing `self.materials = new_dict_with_str_map_to_values`.

self.original_materials = Returns a [self.materials](#self.materials) like dictionary but instead its the values of the original -- on init -- materials in the dictionary. 

self.is_modified = Returns if the Materials have had any of its values changed from the original. You can also set this value with a boolean.

  

## Examples Section
CostEstimator/config/models/materials/[material_setting_model](#MaterialSetting).py
```python
@property
def value(self) -> Union[float | int | SettingRange]:
    return self.material_container.value
```
The `self.material_container` is a [Materials](#MaterialsModel) object
Its using that to get outs its currently selected materials

## Notes/Warnings
- Edge cases, performance considerations, gotchas, commit mistakes people can make 
- You should think about a Materials Class as a window pane that only shows 1 material at a time. It shows the window pane material in [selected material](#self.selected_material) and uses it to pull from the materials dictionary

