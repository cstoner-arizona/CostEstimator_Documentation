(Calculator)=

How the Calculators work/are connected.

[Technology](#TechnologyModel) --calls on-> [SettingCalculator](#SettingCalculator) \<Interface> methods --which direct to-> [SpecificCalculator](#SpecificCalculator) object that inherits [Base](#BaseCalculator).py

The Setting Calculator is like a interface, it talks more about it in [here](#SettingCalculator)