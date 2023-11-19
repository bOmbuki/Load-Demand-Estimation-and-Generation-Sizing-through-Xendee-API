#### Load-Demand-Estimation-and-Generation-Sizing Optimization
Execute file in order sort excel ---> daily demand estimation ---> yearly LP generation ---> main
##### Sort_excel
- It loads the field collected demand estimation data from user specified folder
- It converts the values in the 'time stamp' of each sheet to a datetime format, if the column exists
- It sorts the data in each sheet by the 'time stamp' column in ascending order
- It stores the sorted data in a new folder specified by the user
