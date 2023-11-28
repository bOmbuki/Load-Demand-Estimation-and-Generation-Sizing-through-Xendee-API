#### NB: Prior to executing the main.py, one has to define the folder path to where the field data is stored to the data_path variable in Sort_excel.py
#### API username and password shared via email
#### Load-Demand-Estimation-and-Generation-Sizing Optimization
- This code converts daily minute kilowatt demand data from the field into hourly data, adds random noise, creates load curves, and estimates yearly demand 
  data for Xendee microgrid optimization.
##### Data Description
- The data is a spreadsheet with how much electricity different rural customers use every minute in a day.
- The customers are: households, schools, businesses, religious establishments, and health centers.
- The spreadsheet has four sheets, each for a different combination of season and day type.
   - Sheet 1: Season 1 weekday
   - Sheet 2: Season 1 weekend
   - Sheet 3: Season 2 weekday
   - Sheet 4: Season 2 weekend
- One location can have multiple related datasets, each from a different collection point in time.
##### Sort_excel
- The code sorts the field data by time from midnight to midnight for each sheet (season and day type) and saves the output into a new folder called Sorted 
  Field Data (all expected to be in the same format based on a provided template)
##### daily_LoadProfile
For each file and each sheet in the sorted data folder:
 - The code calculates the average and peak electricity demand for each customer type in each hour of the day for each sheet (season and day type).
 - The code merges the matching datasets for each site and finds the typical and peak demand per customer type for each site.
 - The code multiplies the demand per customer type by the number of customers in each site and saves the results in Village Demand Folder. 
##### yearly_demand
For each file in the Village Demand Folder:
 - Calculates the total and peak demand for each season and day type (sheet).
 - Combines the demand data into one file. 
 - Adds random noise to the data using a normal distribution
 - Creates load curves and a yearly demand time series from the noisy data (saved in Load curves and Xendee 
   input folders respectively)
Merges all the time series data into one file for use in generation optimization
##### folder_creator.py and plot_creator.py
- folder_creator.py has a function that creates a system of folders that will store the preprocessed data at all stages on one's desktop
- plot_creator.py has a function that is called to create the load curves for each proposed microgrid site.
##### api_Optimization
- This section of code is a takes the merged times series data, location data, solar irradiance data from NASA or NREL, and the cost of various generation 
  technologies (batteries, generators and solar arrays), communicates to the Xendee servers through and API and thereby facilitating batch asset selection and generation 
  sizing optimization.
##### main.py
- This is used to run all the scripts sequentially.

