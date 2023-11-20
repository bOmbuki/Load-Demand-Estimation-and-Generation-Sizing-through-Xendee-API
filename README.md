#### Load-Demand-Estimation-and-Generation-Sizing Optimization
Execute file in order sort excel ---> daily demand estimation ---> yearly LP generation ---> main
##### Sort_excel
- It reads the field collected minute demand estimation data from user specified folder.
- It converts the values in the 'time stamp' column of each sheet to a datetime format, if the column exists.
- It sorts the data in each sheet by the 'time stamp' column in ascending order.
- It stores the sorted data in a new folder specified by the user.
##### daily_LoadProfile
- Reads the sorted field data files.
- For each sheet:
   - It computes the mean and finds the max value of each specific consumer type in each row and groups these averages into sets of 60 (hourly sets).
   - The means and max values of these sets are combined to form a new dataframe forming 24hr load demand estimates.
   - It then reads the stored 24hr load demand estimates and finds matching pairs (each site can have several datasets), and combines them into single files. 
   - The collated data is then processed by finding the averages and max values for each specified consumer for each row, thereby finding the typical and peak 
     per consumer type.
   - It then reads a file that defines the number of consumers per village/site surveyed per type and finds the typical and peaks total daily demand per
     consumer type using product operation, and the output is stored in a user defined folder.
##### yearly_demand
- This code processes typical and peak daily demand per consumer.
- It goes through the outpufiles from daily_LoadProfile. For each sheet (sheet have the typical and peak demands for different seasons in the surveyed sites)
    - The typical demand per for different consumer types are summed together and the data stored in lists i.e., season 1 and season 2 - typical and peak demands for weekday and weekends.
    - These sums are stored in lists.
    - Loops are used to populate new excel files with the data contained in the list. For everyweekday in a select year, the average demand in a specified season are used to demand values for week days and peak values are used to populate the hourly demand for the weekends.
