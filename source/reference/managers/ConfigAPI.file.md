(ConfigAPI)=
# Config API
- This class allows for communication between the [Estimator](#Estimator) tab and the [Config Manger](#ConfigManager) through various functions listed below

## Purpose/Motivation

- What problem does this solve?
	- This class was developed to make it easier for the Estimator tab to get the information it needs without needing to know the inner workings of the [config manager](#ConfigManager) 
	- Having this class also allows us to determine if we want to emit a signal when the [Estimator](#Estimator) recoveries or updates a value like in one of the functions below

- When would someone use this?
	- They would use it for example when the [Estimator](#Estimator) slices the part and gets its STL values, the Estimator will send over those values to the [config manager](#ConfigManager) so it can update all of its settings that depend on (The low level function that does this is [here](#TechnologyProcessSTL))

## Basic Usage Example

- A simple, realistic code snippet showing the most common way to use it 

{lineno-start=0 emphasize-lines="7,8,9,10,11,12"}
```python
# CostEstimator/estimate/estimate_manager.py
def _update_config(self) -> None:
	"""
	...truncated for example...
	"""
	try:
		surfaceArea = self.solid_part.surfaceArea  # available even for non-watertight parts
		stl_settings = {
			'resin_volume_used_to_print_one_mold': surfaceArea * 8.0,
			'net_part_volume': self.partVolume * 1.5,
			'dlp_build_time': self.totalTime / 60.0,
		}
		self._config_api.input_STL_data(self.technology.type, stl_settings)
	except Exception as e:
		msg = f"Error updating config manager: {str(e)}"
		Logger.logException('e', msg)
		raise
```
This example shows that inside the [Estimator](#Estimator) after getting the specific STL values it will package them up into a dictionary and send them over to the config api to get updated in the config manager.  

## Key Methods
```{eval-rst}
.. py:method:: get_available_technologies_list(self) -> List[str]

   This returns a list of all available technologies. This list is derived from the supporeted technologies in the file service.
   This will pull the names from the json metadata under "Type". 

   :return: A list of strings that are names for the available technologies under each json metadata
   :rtype: List[str]
   
   
   


.. py:method:: get_technology(self, technology_name: str) -> Technology
   
   This returns the :ref:`Technology Object <TechnologyModel>` for the given technology name.
   
   :param str technology_name: The name of the technology requested, I belive it should match the one found in the metadata of the json files 
   :return: A technology object for the corrisponding name
   :rtype: Technology

   
   


.. py:method:: get_setting(technology_name, setting_name)

	:param str technology_name: The name of the technology to get the setting value from 
	:param str setting_name: The name of the setting w want the setting value from.
	
	This function will return the :ref:`setting <SettingModel>` object of the specific setting that was given for a specific technology.  
	
	:raise TypeError: If the tech/setting name is not a string
	:raise KeyError: If the tech/setting name does not exist 
	
	:return: The setting object of the one requested
	:rtype: :ref:`Setting Model <SettingModel>`
	
	
	
	
.. py:method:: get_all_settings(technology_name)

	:param str technology_name: The name of the technology we want all settings from 
	
	This function will return a dictionary of all the settings `[str_names::ref:`objects<SettingModel>`]` belonging to a technology. 
	
	:return: A dictionary with str keys as setting names, and values as the :ref:`setting objects<SettingModel>`
	:rtype: Dict[str, Setting]
	
	
	
	
.. py:method:: get_settings_by_category(technology_name, category)

	:param str technology_name: The technology name we want to pull settings from 
	:param str category: The category within the :ref:`json files<JsonFilesFormat>`
	
	This function will return the dictionary of all the settings `[str_names::ref:`objects<SettingModel>`]` within a category defined in the :ref:`json files<JsonFilesFormat>` for the category and technololy given. 
	
	:return: The dictionary of string setting names mapped to :ref:`setting object<SettingModel>` for the sepecific json category given
	:rtype: Dict[str, :ref:`Setting<SettingModel>`]
	




.. py:method:: input_STL_data(tech_type, new_stl_input_data)
	
	:param str tech_type: The string name of the technology type this STL data should go to 
	:param dict[str,float] new_stl_input_data: The dictionary of new stl data, stores name of settings as keys, and their corrisponding float values as values.
	
	This function will be called from the Estimator to pass in the newly   gather stl input data from the file sliced. Then from here the new stl   data will trickle down the :ref:`current technology type <ConfigManagerCurrentType>` of the :ref:`config manager <ConfigManager>` and itll update all its stl settings to have this data. Then it will recurse on the dependands of the stl settings and reclaculate them.
	
	:return: None
	
	
	
	
	
.. py:method:: shouldUseDlpForBuildTime()

	This function was created to help determine if the estimator should use the DLP method of cacluating buildtime for when the technology is Printed Pattern Investment Casting and the Technology is resin. It was determined that the build time estimate DLP uses is closer to the time it takes when we use Resin for Printed Pattern Investment Casting. Therefore to do our calculations when its Printed Pattern and SLA Resin is selected we should let the Estimator know that it should cacluate the build time using the same method it does for DLP.  
  
	This function returns True if the technology is Printed Pattern Investment casting, and the currently selected material is SLA Resin. False otherwise.  
  
	This function can be called during any part of the estimator but it will only actually matter in when its determining how to calculate build time only for the printed pattern investment casting material

	:return: True if currently selected technology is Printed Pattern Investment Casting and the currently selected material is the SLA Resin. False otherwise
	:rtype: Boolean

	:See Also: `Issue #133`__ (outside link)
	
	
__ https://github.com/users/cstoner-arizona/projects/2/views/1?filterQuery=133&pane=issue&itemId=205386745&issue=cstoner-arizona%7CCostEstimator%7C133>`
	
```



## Important Attributes/Properties

```{eval-rst}
.. py:property:: _config_manager
	:type: ConfigManager
	
	Holds a reference to the config manager for the plugin which allows the ConfigAPI to pull settings, determine functions, and use the config managers methods.
```
  

## Examples Section
- More detailed usage examples 
```python
#CostEstimator/estimate/estimate_manager.py
@pyqtSlot()  
def calc_min_cost(self):  
    """..truncated for example.."""  
    self.set_parameter_values('min')  
    try:  
        self.minCost = self._config_api.get_setting(self.technology.type, 'total_cost_per_part').value.min
```
- This examples shows getting a specific technology object from the config api

{lineno-start=0 emphasize-lines="13"}
```python
#CostEstimator/estimate/estimate_manager.py
def _update_config(self) -> None:  
    """..truncated for example.."""    
    try:  
        surfaceArea = self.solid_part.surfaceArea  # available even for non-watertight parts  
  
        stl_settings = {  
            'part_volume': self._part_volume,  
            'surface_area_of_one_part': surfaceArea,  
            'support_volume_required_for_one_part': self.support_volume,  
            'net_casting_volume_per_part': self._part_volume * 1.5,  
            'dlp_build_time': self.totalTime / 60.0,  
        }  
        self._config_api.input_STL_data(self.technology.type, stl_settings)
```
- This examples show how to send the STL based data back to the [config manager](#ConfigManager) using the ConfigAPI
## Notes/Warnings

- Edge cases, performance considerations, gotchas, commit mistakes people can make 

{#HowConfigReceviesSTLData}
![HowConfigAPIWorks.png](HowConfigAPIWorks.png)