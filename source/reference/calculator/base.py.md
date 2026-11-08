(BaseCalculator)=
# BaseCalculator
- **CostEstimator/config/calculator/backends/base.py**
- This class is the abstract parent class to every [specific type of calculator](#SpecificCalculator). 
- This abstract class provides the base functionality for every [specific technology calculator](#SpecificCalculator). The base functionality will be the same for every technologies calculator. For example the recalculation of dependents will be the same throughout all technology types so that functionality will be in this class.
- Speaking high level functionality of this class. The importance of a calculator is because there are some [calculated settings](#calculated-setting) that must be computed and this class will have the functions and functionality to calculate those calculated settings 

## Inherits
ABC (Abstract Class)

## Purpose/Motivation
- What problem does this solve?
	- A lot of duplicated code between the Specific classes for each technology type so we put all of the shared functionality into this class, which is then inherited into the specific technologies classes.

- When would someone use this?
	- When they are creating another technology type they would want to inherit this class to have its functionality 

## Basic Usage Example

- A simple, realistic code snippet showing the most common way to use it 

```python
# CostEstimator/config/calculator/backends/binder_jetting.py
class BinderJettingCalculator(BaseCalculator):
    """
    Calculator for Binder Jetting printer settings.
	...
```
This shows the specific technology type calculator inheriting the base calculator

```python
# CostEstimator/config/calculator/setting_calculator.py
def recalculate_dependants(self, setting_name: str, override_original: bool):
	"""
	...truncated for example...
	"""
	self.calculator.recalculate_dependants(setting_name, override_original)
```
This is an example from the [Setting Calculator](#SettingCalculator) that shows that for any type of `self.calculator` (which is any specific calculator type) we can call `.recalculate_dependants(setting_name, override_original)`{l=python}

## Key Methods/Functions
```{eval-rst}
.. py:method:: __init__(printer_type: str, settings: Dict[str, Setting])
   :no-index:

   Initializes the base calculator with a printer type and settings dictionary.

   Accepts a printer type string and a dictionary mapping setting names to their corresponding
   :ref:`Setting <SettingModel>` objects. Creates an internal copy of the settings, builds a dependency tracker
   of setting dependents and dependencies, then identifies and stores all calculated settings.

   :param str printer_type: The type of printer as a string identifier.
   :param Dict[str, Setting] settings: Dictionary mapping setting names to their Setting objects.

.. py:method:: recalculate_dependants(setting_name: str, override_original: bool)

   Recalculates all settings that depend on a given setting after its value changes.

   Called when :ref:`TechnologyModel`'s ``__setitem__`` is invoked with a new setting value.
   Loops over all settings dependent on the updated setting and triggers their recalculation
   so the new value propagates to all dependents.

   :param str setting_name: The name of the setting whose value has changed.
   :param bool override_original: Whether to override the original setting value during recalculation.



.. py:method:: update_settings(settings: Dict[str, Setting])
   :no-index:

   Replaces the current settings and recalculates all calculated settings.

   Creates and stores a copy of the provided settings dictionary, then recalculates all
   calculated settings to reflect the new values.

   :param Dict[str, Setting] settings: Dictionary mapping setting names to their updated Setting objects.



.. py:method:: get_settings() -> Dict[str, Setting]
   :no-index:

   Returns the current settings stored in this calculator.

   :return: Dictionary mapping setting names to their current Setting objects.
   :rtype: Dict[str, Setting]

.. py:method:: calculation_logger(*args)

   Emits a log message with the result of a setting calculation.

   Sends a formatted log message describing the newly computed calculation result.

   :param args: Parameters providing context for the log message, such as setting name and computed value.


.. py:method:: calculate_setting(setting_name: str, override_original: bool) -> Setting

   Calculates and returns the updated value for a given calculated setting.

   Validates that the named setting is a legitimate calculated setting, then calls
   :py:meth:`_recursively_update_setting` to resolve all upstream dependencies before
   performing the final calculation.

   :param str setting_name: The name of the calculated setting to evaluate.
   :param bool override_original: Whether to override the original value during calculation.
   :return: The updated Setting object with the newly computed value.
   :rtype: See :ref:`SettingModel` for the Setting structure.
   :raises ValueError: If ``setting_name`` does not correspond to a valid calculated setting.



.. py:method:: _recursively_update_setting(setting_name, prev_updated_set, calculated_setting_names, override_original) -> Setting

	This function is called when a calculated setting is called. Imagine the setting_name 
	given is a higher level calculated function. That means it depends on other calculated 
	settings. The lower level calculated settings should be calculated/updated first and 
	then this setting should be calculated after now having its dependecies updated. 
	
	This function will solve the problem of cacluating dependcies in the wrong order. It
	will recursivly update this settings dependencies and then come back and update the 
	original settings value.
	
	:param str setting_name: The name of the calculated setting that needs to be updated.
	:param set prev_updated_set: A set of setting names that for this recursive stack have already been updated (or are userDefined) so we know not to recurse on them again.
	:param set calculated_setting_names: This holds all the setting names of calculated (formula given) settings. check the call to this function in caclulateSetting to see what it actually is.
	:param bool override_original: Overriding the original is used for when we load in a save file from the user or on initializatio. False if you are updating the settings besides those two instances.
	
	:return: A :ref:`setting object <SettingModel>` of the setting_name given after the value was (possibly) updated.
	:rtype: :ref:`Setting Object <SettingModel>`.
	
	:raises ValueError: If the setting name IS a calculated setting but doesnt have a function in the disbatch table.
	
	
	
.. py:method:: initialize_calculated_settings()

   Initializes all calculated (formula-defined) settings on startup.

   Loops over every entry in the dispatch table, runs validation checks, then calls
   :py:meth:`_recursively_update_setting` on each valid entry to resolve dependencies
   before computing the setting's value. If no settings end up being calculated, a debug
   log message is emitted.

   For :ref:`material-dependent <MaterialSetting>` settings, any such setting found in the dispatch table is
   skipped with a warning, as a :ref:`formula-calculated <calculated-setting>` setting having per-material values
   is considered a misconfiguration, it should be non-material-dependent instead.

   .. note::
      Uses ``override_original=True`` when calling
      :py:meth:`_recursively_update_setting` because this is an initialization pass.

   .. rubric:: Nested function

   .. py:function:: validation_checks_before_updating(setting_name: str) -> bool

      Validates a setting from the dispatch table before it is updated.

      Checks the following conditions, logging a warning and returning ``False`` if any match:

      1. The setting name is not present in ``formula_calculated_settings``.
      2. The setting object at that name is ``None``.
      3. The setting is an instance of :ref:`MaterialSetting <MaterialSetting>`, which is
         invalid for a formula-calculated setting.

      :param str setting_name: The name of a setting from the dispatch table.
      :return: ``True`` if the setting did not meet any invalid condition, ``False`` otherwise.
      :rtype: bool


.. py:method:: update_material_selection(material_name: str)

   Updates all :ref:`MaterialSetting <MaterialSetting>` objects that contain the given material
   to do what is listed below.

   Loops over all settings and, for each one that is a
   :ref:`MaterialSetting <MaterialSetting>`, checks whether ``material_name`` is present
   in that setting's selectable materials. If so, it calls the setting's own
   ``update_material_selection`` method to effectly change that material settings 
   materials container :ref:`currently selected material <self-selected_material>` to the one given.
   
   This functions purpose is to help calculate material settings but as far as I know its not used.

   :param str material_name: The name of the material to select.


.. py:method:: get_dispatch() -> dict

   *Decorated with* ``@abstractmethod``

   Abstract method that subclasses must implement to provide their dispatch table.

   The dispatch table maps calculated setting names to their corresponding formula
   functions, and is used by :py:meth:`initialize_calculated_settings` and
   :py:meth:`calculate_setting` to resolve which function to call for a given setting.

   :raises NotImplementedError: Always, if called on the base class without a subclass implementation.
```


## Important Attributes/Properties
```{eval-rst}
.. py:property:: DISPATCH_TABLE
   :type: Dict[str, Callable]
   
   This property holds :ref:`Calculated Json Setting Names <calculated-setting>` as keys
   and maps them to callable functions within the speicifc technologies calculator 
   that will do the calculations needed to recompute/update that setting.
   
.. py:property:: settings
	:type: Dict[str, Setting]
	
	:seealso: :ref:`Setting Object <SettingModel>`
	
	This holds a copy of the :ref:`technologies <TechnologyModel>` settings for the computation.
	It will be sent back (actually called back) once the technology object knows there might
	have been some changes.
	
	
	
.. py:property:: dependency_tracker
	:type: SettingDependencyTracker
	
	:seealso: :ref:`SettingDependencyTracker <SettingDependencyTracker>`
	
	This holds the dependency tree that maps the relationships between all settings that have dependencies.
	There might be :ref:`calculated settings <calculated-setting>` that depends on another calculated setting, 
	or another :ref:`user defined setting <user-defined-setting>`. That relationship must be known so that we 
	can preform calculations in the correct order.
	This is used in the calculate functions to get the dependants (Higher level settings that rely on user input settings).



.. py:property:: printer_type
	:type: String
	
	Holds a copy of the additive manufacturing type this calculator is used for.
	Ive only found this used for logging.
	
	
.. py:property:: formula_calculated_settings
	:type: List[Str]
	
	:seealso: :ref:`Calculated Settings Explenation <calculated-setting>`
	
	This holds all the setting names that are considered to be a calculated setting, one with a formula attribute
	and a "user_defined"=false attribute in the :ref:`json<JsonFilesInfo>`
	
```

  
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
This examples shows that **within the Technology Class** we are calling calculator methods, and it gives an example of a usage for calling 
`_recursively_update_setting()`{l=python}
## Notes/Warnings
- Remember this class is inherited by all the specific technology calculators. (e.g. CostEstimator/config/calculator/backends/binder_jetting.py)
