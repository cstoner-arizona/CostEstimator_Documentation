# SettingDependencyTracker
- This tracks dependencies between settings for 1 printer type.
- It builds a dependency tree and provides methods to query dependencies and dependents
- This class was made to solve the problem with calculating calcualted settings in the wrong order which would produce incorrrect results based on a user defined setting beting updated. 
- When a [user defined](#user-defined-setting) setting is updated, with this class we can find the calculated settings [dependencies](#how-to-use-depends-on-attr) and update those first before recomputing the calculated setting. 

## Purpose/Motivation

- What problem does this solve?
	- Calculating settings out of order. 
	- For example lets say we have 
		- User5 gets updated from user 
		- **Calculated12** = **User5** + User19 * User8
		- Calculated30 = **Calculated12** * **User5**
	- Then the order we want to update is `User5, Calculated12, Calculated30` or else `Calculated30` will have a bad value if its calculated before `Calculated12` is updated 

- When would someone use this?
	- When they want to get all the settings that rely on a base setting to know which settings need to be updated if that base setting is changed

## Basic Usage Example

- A simple, realistic code snippet showing the most common way to use it (keep it short, just enough for the basic idea)

```python
# CostEstimator/config/calculator/setting
# we want to make sure we recalculate all the dependants 
queue: Queue = Queue(maxsize=0)
# Get a list of the this settings dependants and add them to the queue
setting_dependants: list[str] = self.dependency_tracker.get_direct_dependents(setting_name)
for dependant in setting_dependants:
	queue.put(dependant)
```
This example shows that we use 


## Key Methods/Functions
```{eval-rst}
.. py:method:: __

```


## Important Attributes/Properties


- What can the user access or modify?

  

## Examples Section
- More detailed usage examples (Show the common patterns)

## Notes/Warnings

- Edge cases, performance considerations, gotchas, commit mistakes people can make 
