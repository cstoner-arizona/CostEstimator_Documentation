(SettingValidator)=
# SettingValidator.py
- This class is the configuration class that holds the rules that will be used in the '[validate_setting](#ValidateSetting)' function of this class. 
- The "rule" classes that are created in `setting_validator.py`  will implement a `def validate(value, schema)` function that does a check for its specific purpose. For example the [Type Validation Rule](#TypeValidationRule) will implement `def validation` as checking if the string type in the [schema](#JsonDefinitions) is lets say "int" that the value is an instance of int and if not it'll return the False and a string of the error.

{#TypeValidationRule}
## Class TypeValidationRule
- CostEstimator/config/validator/setting_validator.py
Implements a `def validate(val, schema)` function that will check that there is a type in the schema and the type of the type is a string, then it will base the next check on the type_strings value. if its "int" it checks that the value is a instance of a int type. Then it does this for all the other possible types and returns false if not, then returns true if its valid 

# Class UnitValidationRule
- CostEstimator/config/validator/setting_validator.py
Implements a `def validate(val, schema)` that checks that the `schema['unit']` attribute is defined, even if nothing, just at least it is defined. 

# Class RangeValidationRule
- CostEstimator/config/validator/setting_validator.py
Implements  a `def validate(val, schema)` that checks that the value for this setting is not lower than the `schema['min']` attribute, and not higher than the `schema['max']` attribute. 
The value can be a int, float, range, or string (checks `schema['min_length']` instead) 

## Purpose/Motivation
- What problem does this SettingValidator class solve?
	- This decoupling breaks the validation checking down from a large class with multiple functions into multiple classes with just 1 validation function. This can be expanded rather easily if more things need to be verified about a setting.

- When would someone use this?
	- This is used on validation when the project first starts to run and load the settings


## Key Methods/Functions of Setting Validator
{#ValidateSetting}
def validate_setting(tech_type, setting_name, value, schema): list\[str]
: This function will loop over the "rule" classes and call `ruleClass.validate(val, schema)` on them all and if any errors happened it will add it to a resulting list and return it 


## Important Attributes/Properties
- What can the user access or modify?
	- Nothing really, the only thing this class is for is to call `SettingValidator.validate_setting(...)` 


## Notes/Warnings
- None
