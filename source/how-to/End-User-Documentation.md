(end-user-docs)=
# How to use the plugin - End User Documentation

1. Assuming you have the Cost Estimator plugin installed in the Cura's plugins folder. Open Cura
![Pasted image 20260821123047.png|538](CuraOpened.png)

2. Then click on the file icon in the top left to select your '.stl' part file of choice from your personal computer 
![imge|500](SelectFolderIcon.png)
![img|500](how-to/MySTLFiles.png)

3. Once the part is loaded you should see it on the Cura print bed

4. If you see this error because your part is to big, follow steps 4a-4b, then continue to step 5
![img|500](how-to/PartToBigError.png)
4a. If you see a warning that the part is to big like below, then go to 'Preferences' -> 'Configure Cura...' -> 'Printers' -> 'Add New' -> UltiMaker printer -> 'Add local printer' -> 'Add a non-networked printer' and select a bigger printer that can fit the part. 
4b. Then you **must** delete the part and add it again to remove the error. Or else the plugin won't calculate

5. Then at the top click on 'Extensions' -> 'Cost Estimator' -> 'Cost Estimator Settings...'
![img|500](OpenPlugin.png)

If you don't see the 'Cost Estimator' under 'Extensions' that means the plugin was not properly installed. You want to confirm you are on Cura Version 5.10.4 - 5.11. You want to confirm that inside the Cura's file directory in the plugin directory that you see the 'CostEstimator' folder and it contains files in it. And if both of those are correct then look for the install directions you got the plugin files from to see if a step got missed. 

# Configuration Panel

6. Then opening the plugin you are faced with the configuration panel
![img|500](ConfigPanel.png)

7. You will see on the left is your technology picker. Pick the technology that you want to price estimate
![img|500](TechPicker.png)

8. Then at the top you will see a 'Material Selection' area. Select the material you want to use to create a estimate. 
![img|500](MaterialSelection.png)

9. Then have a scroll through the configurable settings in the middle. Grey settings are non-editable. Those include calculated settings and part properties. You might want to change some user-editable settings to produce a better estimate. 
For example changing your batch size to the number of parts you wish to estimate will give you a different 'cost per part' along with a 'production volume'.
If you are using a furnace based technology, you might want to change the 'Furnace Acquisition Cost' range. 
If your 'Technician Hourly Rate' is different than the default $30-35 given then you might want to change that to get a better cost estimate. 
A key thing to remember when changing settings is to change the max before the min. This is because the min will not allow you to set itself higher than the max. 

There are many more examples of what you might want to change based on how much you know coming into this. There are tool tips for each setting that give some information about the setting. Some are self explanatory. To find them, hover over the Grey question mark next to a setting. 
![img|500](ToolTip.png)

While changing settings you will find the a small yellow 'Modified' label appears towards the top of the scroll panel, and the 'Discard' / 'Save Settings' buttons turn on. You are able to swap between technologies without losing your changed settings, but if you wish to close the plugin and keep a copy of your modified settings press the 'Save Settings' button on the bottom. If you want to know more info, check out the 'User Saved Settings' section down towards the end of this document. 

If you attempt to close the plugin with unsaved-settings you will be prompted to confirm you wish to discard those changes. If you choose to discard, then any and all settings modified during that session will be discarded. That includes settings modified in technologies other than the currently selected.
![img|500](ExitingUnsavedChanges.png)

# Estimate Tab 

10. Once you change all the settings you desire, click on the 'Estimate' tab
![img|500](ClickEstimateTab.png)

11. You will see a new window that has blank info boxes. Depending on the technology, if the technology allows you to do 'Layer Slicing' you may choose that. Only 'Powder Bed Fusion', 'Printed Mold Sand Casting', and 'Printed pattern Investment Casting' have Layer Slicing estimates. 
![img|500](LayerSlicing.png)

12. Then when you are ready to calculate an estimate for that part you can press the calculate button in the bottom right. Pressing 'Calculate' will do estimates based on the last selected technology in the 'Configuration Panel' (also shown at top of Estimate tab).
![img|500](PressCalculate.png)

13. You may get this warning about the estimated part cost being less than $300. The note states that some manufactures have a minimum order value or require a minimum batch size.
![img|500](LowPartCostWarning.png)

14. Then after calculating you can see all the data filled out.
![img|500](EstimatedCost.png)
The part properties show the Volume, Mass, Surface Area.
Extents shows the bounding box demensions
Estimates gives you the time to make estimates in a switchable Minutes or Hours unit.
Cost Estimate in min and max cost
If you changed the 'Batch Size' you will see that the 'Production Cost' is different than the Cost.

Its important to know that the 'Production Cost' has expected discounts baked into its calculation.
If the 'Batch Size' is less than or equal to 50, there is no discount.
if the 'Batch Size' is between 51 and 100 inclusive, there is a 10% discount.
and if the 'Batch Size' is greater than 100, there is a 15% discount. 

The Feasibility section has 
'Lead Time Estimate' which gives you the expected amount of lead time based on the technology before you get a quote from a manufacturer. 
And has 'Part Thickness' which shows the minimum wall thickness found in the part and displays that the minimum allowed is 2mm. Have a look at the tool tip (grey question mark) for more detailed information. 

Then the Profitability section shows the sale price per part if the 'Margin' percentage on the right was added on top of the part cost. 

# Comparing Estimates

15. Now the entire point of this tool is to compare between different additive manufacturing technologies, and you can do that with the "Save" "Save As" buttons on the bottom right after calculating. 
![img|500](SaveAsButtons.png)

To use these buttons, first you press "Save" if you just want the results saved to your downloads folder as a Excel Spreadsheet. But If you want more customizability you should press the "Save As" button. 
![img|500](PressSaveAs.png)

Pressing on #1 Red Circle will prompt the center file explorer to pop up and give you more customizability in the location and type of file you store the saved data in.
#2 Red Circle you can change the name however you please
Pressing on #3 Red Circle it will drop down and show a 'PDF' option which allows your estimated results to be **appended** to the pdf. Or you can keep the Excel Workbook filetype to have the results appended to the 
#4 Red Circle: You can save this file in any location you choose.

Then after you save, you can go back to the 'Configuration Panel' -> select a different technology -> modify any settings you wish -> go back to estimate pannel -> press calculate 
and if you press 'Save' then it will **APPEND** to that previously saved file - even if it was a pdf. 
The plugin remembers to append to file even if the plugin or entire cura application is closed in efforts to be convenient.  
Here is an example of both the PDF and Excel versions of the save estimates 
**Excel**
![img|500](SaveEstimatesExcel.png)

**PDF** (put two pages onto one for smaller screenshot)
![img|500](SaveEstimatesPDF.png)


Now from here on out its up to you! You can load different parts, use different technologies, change the user-editable settings to your hearts content!

# User Saved Settings
You'll find that when you modify settings within the 'Configuration Panel' that there is a little yellow 'Modified' label in the top of the Settings rectangle, and the 'Discard' / 'Save Settings' buttons turn on. 
![img|500](ModifiedSettings.png)

When settings are modified you are able to press 'Save Settings' to save the '.json' file format of the settings to your hard disk. When pressing the 'Save Settings' button you will get a file explorer pop up to choose the file location for the 'User Settings'. The default location is in the plugins 'CostEstimator/config/resources/data/user' folder. You can choose to save it elsewhere if you'd like.
![img|500](PressedOnSaveSettings.png)

The saved version of your settings will stay with the plugins defaults until you close the Cura application and reopen it. Then you will get the plugins defaults settings and if you wish to have yours back press the 'Load Settings' button. 


Because there are special rules for each setting, and the format of the user setting files must follow the definition of the '.json' files **DO NOT MANUALLY MODIFY THE JSON FILE** because it simply wont load properly. If you wish to make changes to those saved files, press on the 'Load Settings' button, and configure them within the plugin to save back out again. 