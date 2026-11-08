
(SpecificCalculator)=
# Specific Calculator
- Each of the specific calculators will be the lowest level instantiated object for processing the calculations. 
- Each has a Dispatch Table (below) which is used to map setting names to callable functions which will update that variable 

(DispatchTable)=
## Dispatch Table
The dispatch table is a mapping from valid [json setting names](#JsonFilesInfo) to their local callable functions that will be called if that setting name ever needs. 
Here is an example of a dispatch table. 
```python
#CostEstimator/config/calculator/backends/lpbf.py
def get_dispatch(self) -> Dict[str, Callable]:  
    """  Returns the dispatch table mapping setting names to their calculation methods for LPBF printers.    """    
    return {    "support_factor": self.update_support_factor,  
                "recycling_factor": self.update_recycling_factor,  
                "material_cost_per_part": self.update_material_cost_per_part,  
                "machine_hourly_cost": self.update_machine_hourly_cost,  
                "investment_cost": self.update_investment_cost,  
                "machine_cost_per_part": self.update_machine_cost_per_part,  
                "labor_cost_per_part": self.update_labor_cost_per_part,  
                "energy_cost_per_part": self.update_energy_cost_per_part,  
                "direct_cost_per_part_excluding_labor": self.update_direct_cost_per_part_excluding_labor,  
                "post_processing_cost_per_part": self.update_post_processing_cost_per_part,  
                "yearly_maintenance_cost": self.update_yearly_maintenance_cost,  
                "maintenance_cost_per_part": self.update_maintenance_cost_per_part,  
                "annual_overhead_cost": self.update_annual_overhead_cost,  
                "overhead_rate": self.update_overhead_rate,  
                "overhead_cost_per_part": self.update_overhead_cost_per_part,  
                "total_cost_per_part": self.update_total_cost_per_part  
            }
```

(SettingUpdateMethod)=
## Update functions
```python
# CostEstimator/config/calculator/backends/binder_jetting.py
def update_total_sand_used_per_build(self, override_original: bool) -> bool:
	""" 
	.. truncated for example ..
	"""
	calculated_total_sand_used_per_build: float = self._calculate_total_sand_used_per_build(
		self.settings['sand_density'].value,
		self.settings['bounding_box_volume_of_one_part'].value,
		self.settings['batch_size'].value,
		self.settings['mold_bounding_box_factor'].value
	)
	if (
		self.settings['total_sand_used_per_build'].value 
		!= calculated_total_sand_used_per_build
	):
		self.settings['total_sand_used_per_build'].set_calculated(
			calculated_total_sand_used_per_build, override_original
		)
		return True # Newly Calc. setting was new and updated so return True
	return False # Newly Calc. setting was not new 
```
- Whenever the [depends on](#calculated-setting) attribute of a setting gets changed, then the arguments for calling the [calculate](#SettingCaculateMethod) method change so make sure to change those. 
- Whenever the **Name** of a setting gets changed you have to change the if statement in its update function 

(SettingCaculateMethod)=
## Calculate functions
{lineno-start=1 emphasize-lines="18,19"}
```python
@staticmethod
def _calculate_total_binder_used_per_build(
	stl_printed_region_volume: float, binder_saturation: float, 
	inefficiency_multiplier: SettingRange, packing_rate: SettingRange
	) -> SettingRange:
	"""
	Calculates the total_binder_used_per_build based on stl_printed_region_volume and binder_saturation and inefficiency_multiplier and packing_rate.

	Args:
		stl_printed_region_volume (float): Defined as = (4 * Part bounding box volume) - part volume
		binder_saturation (float): Used in calculating the total binder used per build. 0-100, Usually 60-100%
		inefficiency_multiplier (range): Used in calculating the total binder used per build. Usually 1.05-1.15
		packing_rate (range): Used in calculating the total binder used per build. (0-100), Usually 50-70%

	Returns:
		SettingRange: The calculated total_binder_used_per_build.
	"""
	binder_saturation = binder_saturation / 100
	packing_rate = packing_rate / 100
	return (stl_printed_region_volume*binder_saturation*inefficiency_multiplier*(1-packing_rate))/1000000
```
Notice in this example ⬆︎ that the 2 values are divided by 100, this is because for percentages or ratios it makes more sense to ask the user for a value between 0-100 rather than 0-1.0. 

{lineno-start=1 emphasize-lines="21,22"}
```python
@staticmethod
def _calculate_material_cost_per_part(
	total_sand_used_per_build: float, powder_sand_price: float, 
	total_binder_used_per_build: SettingRange, binder_price: float, 
	batch_size: int, direct_cost_of_metal_per_part: SettingRange
	) -> SettingRange:
	"""
	Calculates the material_cost_per_part based on total_sand_used_per_build and powder_sand_price and total_binder_used_per_build and binder_price and batch_size and direct_cost_of_metal_per_part.

	Args:
		total_sand_used_per_build (float):  = sand_density * bounding_box_volume_of_one_part * 4 * batch_size * mold_bounding_box_factor
		powder_sand_price (float): Price of the powder or sand material used in the binder jetting process, typically in USD per kilogram
		total_binder_used_per_build (range):  = (stl_printed_region_volume * binder_saturation * inefficiency_multiplier * (1 - packing_rate)) / 1000000
		binder_price (float): Cost of binder per Liter
		batch_size (int): No Json Description
		direct_cost_of_metal_per_part (range):  = unit_metal_cost * casting_weight_net_metal_per_part * factor_for_metal_loss

	Returns:
		SettingRange: The calculated material_cost_per_part. Returns SettingRange(min=0,max=0) if batch_size <= 0
	"""
	if batch_size <= 0:
		return SettingRange(0,0)
	return (((total_sand_used_per_build*powder_sand_price)+(total_binder_used_per_build*binder_price))/batch_size)+direct_cost_of_metal_per_part
```
Notice in this ⬆︎ example that we have a less than zero check for batch size. That is because we dont want to do a division by zero which would cause it to crash. We'd rather return a setting range that is 0-0 because that value of zero could be a user typo. 

Whenever the [depends on](#calculated-setting) attribute gets changed for a setting then the **parameters for the calculate functions must change**. Actually almost all of the this function must be changed (params, docstring, and computation)