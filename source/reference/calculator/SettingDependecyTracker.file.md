(SettingDependencyTracker)=
# SettingDependencyTracker
- This tracks dependencies between settings for 1 printer type.
- It builds a dependency tree and provides methods to query dependencies and dependents
- This class was made to solve the problem with calculating calcualted settings in the wrong order which would produce incorrrect results based on a user defined setting beting updated. 
- When a [user defined](#user-defined-setting) setting is updated, with this class we can find the calculated settings [dependencies](#how-to-use-depends-on-attr) and update those first before recomputing the calculated setting. 

## Purpose/Motivation

- What problem does this solve?
	- Calculating settings out of order. 
	- For example lets say we have these user/calculator defined settings (User/Calculated)
		- User5 gets updated from user 
		- **Calculated12** = **User5** + User19 * User8
		- Calculated30 = **Calculated12** * **User5**
	- Then the order we want to update is `1. User5, 2. Calculated12, 3. Calculated30` or else `Calculated30` will have a bad value if its calculated before `Calculated12` is updated 

- When would someone use this?
	- When they want to get all the settings that rely on a base setting to know which settings need to be updated if that base setting is changed

## Basic Usage Example

- A simple, realistic code snippet showing the most common way to use it 

```python
# CostEstimator/config/calculator/backends/base.py
# we want to make sure we recalculate all the dependants 
queue: Queue = Queue(maxsize=0)
# Get a list of the this settings dependants and add them to the queue
setting_dependants: list[str] = self.dependency_tracker.get_direct_dependents(setting_name)
for dependant in setting_dependants:
	queue.put(dependant)
```
This example shows when we use the setting dependency tracker to get the direct parents of a setting and add it to a queue to presumably update them all later because the `setting_name` just got updated with new data


## Key Methods/Functions
```{eval-rst}
.. py:method:: __init__(self, settings: Dict[str, Setting]):
	
	This will initialize the SettingDependencyTracker and Bbuild dependency trees for a single printer type. This init will use the settings dict passed in to create a dictionary mappping the setting names to teir :ref:`depends on <how-to-use-depends-on-attr>` lists. 
	
	:param dict settings: A dictionary mapping :ref:`json setting names <how-to-use-name-attr>` to :ref:`setting objects <SettingModel>`
	
.. py:method:: has_dependencies(self, setting_name: str):

	Checks if the setting has any dependencies (children)
	
	:param str setting_name: The name of the setting we are checking

	:return: True if the setting name given has dependecies (chilren), false if not
	:rtype: boolean 
	
	
.. py:method:: has_dependents(self, setting_name: str):

	Not to be confused with `has_dependencies()`
	This checks if the setting has any DEPENDENTS (parents)
	
	:param str setting_name: The name of the setting we are checking
	:return: True if the setting name given has dependents (parents), false if not
	:rtype: boolean
	
.. py:method:: get_direct_dependents(self, setting_name: str):

	Return the list of direct dependants of this setting
	Think about this as asking "What settings RELY on this setting given?"
	
	:param str setting_name: The name of the setting we want the dependents (parents) of
	
	:return: A list of other setting names that rely on the setting name given. Or a empty list if the setting is pretty high level like 'total_cost' which has no settings reliant on itself
	:rtype: List[Str]
	
	
	
.. py:method:: get_direct_dependencies(self, setting_name: str):

	Return the list of direct dependencies of this setting
	Think about this as asking "What settings does this setting rely on?"
	
	:param str setting_name: The name of the setting we want the dependencies (children) of
	:return: A list of other setting names that this setting relies on. Or a empty list if the setting is pretty high level like 'total_cost' which has no settings reliant on itself
	:rtype: List[Str]
	
..
```


## Important Attributes/Properties

```{eval-rst}

.. py:property:: dependency_tree
	:type: dict[Str, DependencyNode]
	
	Maps setting names to DependencyNodes which hold that settings parents (dependents) and children (dependencies).
	
	
.. py:property:: dependencies
	:type: dict[str, list[str]]
	
	This property stores a mapping of setting anmes to a list of settings it depends on. Just like pulling the :ref:`depends_on <how-to-use-depends-on-attr>` list for that settings.
```


## Examples Section
- More detailed usage examples 

{lineno-start=0 emphasize-lines="9,16"}
```python
#CostEstimator/config/calculator/backends/base.py
def recalculate_dependants(self, setting_name: str, override_original: bool):
	"""..truncated for example.."""
	if self.dependency_tracker.get_direct_dependents(setting_name) is None:
		return

	queue: Queue = Queue(maxsize=0)
	# Get a list of the this settings dependants and add them to the queue
	setting_dependants: list[str] = self.dependency_tracker.get_direct_dependents(setting_name)
	for dependant in setting_dependants:
		queue.put(dependant)

	while not queue.empty():
		next_setting: str = queue.get()
		# Get a list of the this settings dependants
		setting_dependants: list[str] = self.dependency_tracker.get_direct_dependents(next_setting)
		
		for dependant in setting_dependants:
			queue.put(dependant)
		new_value = self.calculate_setting(next_setting, override_original)
```

## Notes/Warnings
There is a detailed description of how the Setting Dependency Tracker works, [here](#HowDependencySystemWorks)