import pandas as pd
import os

# Define input and output file paths
input_folder = 'C:\\Users\\bmogaka\\Desktop\\Load Profile Estimation\\Sorted Data\\Sorted Field Data'
peak_average = 'C:\\Users\\bmogaka\Desktop\\Load Profile Estimation\\Sorted Data\\Hourly Field Data'
combined_sessions = 'C:\\Users\\bmogaka\\Desktop\\Load Profile Estimation\\Sorted Data\\Combined Sessions'
daily_demand = 'C:\\Users\\bmogaka\\Desktop\\Load Profile Estimation\\Demand\\Estimated Consumer Demand'
daily_demand_customers = "C:\\Users\\bmogaka\\Desktop\\Load Profile Estimation\\Demand\\Village Demand"

"""
The code reads sorted files from a folder containing comet data. The code uses a loop to iterate through all the files
in the input folder using os.listdir() function. For each file, the code checks if it is an Excel file by using the
.endswith(".xlsx") method. If it is an Excel file, the code proceeds to read the Excel file as a data frame using 
pd.ExcelFile() function from the pandas library. Once the Excel file is loaded as a data frame, the code creates an 
empty list to store sheet names and data frames. It then loops through each sheet in the Excel file using sheet_names 
attribute of pd.ExcelFile object. For each sheet, the code performs the following steps:
- Calculates the mean of all values for a given consumer type across the columns using df.filter(regex=...) to filter
  columns based on their names and .mean(axis=1) to calculate the row-wise mean.
- Groups the resulting mean values into sets of 60 using groupby(df.index // 60), where df.index represents the index
 (time values) of the data frame and // 60 performs integer division by 60, effectively grouping the data into hourly 
 intervals.
- Calculates the mean of these sets of 60 mean values to determine the average hourly demand for each consumer type.
- Creates a new data frame with the calculated average hourly demand values, where each consumer type is represented 
  by a different column.
- Appends the new data frame to the list of data frames.
Once all sheets in the Excel file have been processed, the code writes the output to a new Excel file using 
pd.ExcelWriter() and to_excel() functions. The output file is saved in the specified output folder with the same name 
as the original Excel file, but with "_24hr.xlsx" added to the file name. This new Excel file contains the calculated 
average hourly demand data for each consumer type across all sheets in the original Excel file.
"""

print(f'________Creating hourly demand for consumer types_______')
# Loop through all files in input folder
for file_name in os.listdir(input_folder):
    # Check if file is an Excel file
    if file_name.endswith(".xlsx"):
        # Construct input and output file paths
        input_file_path = os.path.join(input_folder, file_name)
        output_file_path = os.path.join(peak_average, file_name.replace(".xlsx", "_24hr.xlsx"))

        # Read Excel file as data frame
        excel_file = pd.ExcelFile(input_file_path)

        # Create list to store sheet names and dataframes
        sheet_names = excel_file.sheet_names
        dataframes = []

        # Loop through each sheet in the Excel file and calculate means and maxes
        for sheet_name in sheet_names:
            # Load data into a dataframe
            df = pd.read_excel(excel_file, sheet_name)

            # Calculate means and maxes for each set of columns
            hh_mean = df.filter(regex='^HH').mean(axis=1).groupby(df.index // 60).mean()
            hh_max = df.filter(regex='^HH').max(axis=1).groupby(df.index // 60).max()
            b_mean = df.filter(regex='^B').mean(axis=1).groupby(df.index // 60).mean()
            b_max = df.filter(regex='^B').max(axis=1).groupby(df.index // 60).max()
            ch_mean = df.filter(regex='^CH').mean(axis=1).groupby(df.index // 60).mean()
            ch_max = df.filter(regex='^CH').max(axis=1).groupby(df.index // 60).max()
            he_mean = df.filter(regex='^HE').mean(axis=1).groupby(df.index//60).mean()
            he_max = df.filter(regex='^HE').max(axis=1).groupby(df.index // 60).max()
            sc_mean = df.filter(regex='^SC').mean(axis=1).groupby(df.index // 60).mean()
            sc_max = df.filter(regex='^SC').max(axis=1).groupby(df.index // 60).max()

            # Combine means and maxes into a new dataframe
            new_df = pd.DataFrame({
                'hh_average': hh_mean,
                'hh_peak': hh_max,
                'b_average': b_mean,
                'b_peak': b_max,
                'ch_average': ch_mean,
                'ch_peak': ch_max,
                'he_average': he_mean,
                'he_peak': he_max,
                'sc_average': sc_mean,
                'sc_peak': sc_max
            })

            # Append new dataframe to list of dataframes
            dataframes.append(new_df)

        # Write output to Excel file
        with pd.ExcelWriter(output_file_path) as writer:
            for i, sheet_name in enumerate(sheet_names):
                dataframes[i].to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"Output saved to {output_file_path}.")

""" The purpose of this code is to identify pairs of files in the 'peak_average' directory that have matching prefixes,
where the prefix is the first 27 characters of the file name. The code creates a dictionary called 'file_dict' to store
pairs of file names that have matching prefixes. It starts by iterating through the files in the directory specified by
the 'peak_average' variable using the 'os.listdir()' function. For each file in the directory, it checks if the file
ends with the '.xlsx' extension using the 'endswith()' method. If it does, it extracts the first 27 characters (prefix) 
from the file name using slicing and stores it in a variable called 'prefix'. Next, the code iterates through the files
in the directory again using another loop. For each file, it checks if the file ends with the '.xlsx' extension and if 
the first 27 characters of the file name match the 'prefix' obtained earlier. It also ensures that the file name is not
the same as the original file name to avoid matching a file with itself. If these conditions are met, it means that
there is another file in the directory with a matching prefix. In this case, it adds the original file name as the key
and the matching file name as the value to the 'file_dict' dictionary.
"""
print(f'\n_________Combining sessions________')
# Loop through the files in the input directory
file_dict = {}
for filename in os.listdir(peak_average):
    if filename.endswith('.xlsx'):
        # Extract the first five characters of the filename
        prefix = filename[:27]
        # Check if there is another file with a matching prefix
        for other_filename in os.listdir(peak_average):
            if other_filename.endswith('.xlsx') and other_filename[:27] == prefix and other_filename != filename:
                # If there is a matching file, add it to the dictionary
                file_dict[filename] = other_filename

# Loop through the file dictionary and combine the matching files
for file1, file2 in file_dict.items():
    # Create a new workbook
    combined_workbook = pd.ExcelWriter(os.path.join(combined_sessions, file1[:27] + '_combined.xlsx'))

    # Read the two workbooks
    workbook1 = pd.read_excel(os.path.join(peak_average, file1), sheet_name=None)
    workbook2 = pd.read_excel(os.path.join(peak_average, file2), sheet_name=None)

    # Combine the sheets
    for sheet_name in workbook1.keys():
        # Combine the sheets with an empty column in between
        combined_sheet = pd.concat([workbook1[sheet_name], pd.DataFrame({'': [None] * workbook1[sheet_name].shape[0]}),
                                    workbook2[sheet_name]], axis=1)
        combined_sheet.to_excel(combined_workbook, sheet_name=sheet_name, index=False)

    # Save the combined workbook
    combined_workbook.close()
    print(f"Output saved to {combined_sessions}.")

"""
This code segment is reading sorted files from a folder containing combined session data for comet demand. For each 
sheet in the read file, it calculates the average and peak demand values for different consumer types (household, 
business, church, health, school) across columns. It then creates a new data frame with the calculated average and 
peak values. The resulting data frames for each sheet are stored in a list. Next, the code creates a new Excel workbook
to store the output data. It loops through the list of data frames and writes each data frame to a separate sheet in 
the output workbook with the sheet name same as the original sheet name in the combined session file. Finally, it saves
the output workbook to a new Excel file in a different folder with a file name based on the original sorted data file 
name appended with "_24hr_profile.xlsx". The output file is saved in the same directory as the sorted data 24-hour 
folder. The code also prints a message indicating the location of the saved output file.
"""
print(f"\n_______________Final 24 hr load profiles___________________")
#  Define the target headers
hh_average = 'hh_average'
hh_peak = 'hh_peak'
b_average = 'b_average'
b_peak = 'b_peak'
ch_average = 'ch_average'
ch_peak = 'ch_peak'
he_average = 'he_average'
he_peak = 'he_peak'
sc_average = "sc_average"
sc_peak = "sc_peak"

# Loop through all combined session sheets
for file in os.listdir(combined_sessions):
    if file.endswith('.xlsx'):
        # Read file into data frame
        combined = pd.read_excel(os.path.join(combined_sessions, file), sheet_name=None)

        # Empty list to hold dataframes for each sheet
        sheets = []

        # Loop through all sheets in the file
        for sheet_name, df in combined.items():

            if hh_average in df.columns:
                household_av = df.loc[:, df.columns.str.contains(hh_average)]
                household_average = household_av.mean(axis=1)

            if hh_peak in df.columns:
                household_p = df.loc[:, df.columns.str.contains(hh_peak)]
                household_peak = household_p.max(axis=1)

            if b_average in df.columns:
                business_av = df.loc[:, df.columns.str.contains(b_average)]
                business_average = business_av.mean(axis=1)

            if b_peak in df.columns:
                business_p = df.loc[:, df.columns.str.contains(b_peak)]
                business_peak = business_p.max(axis=1)

            if ch_average in df.columns:
                church_av = df.loc[:, df.columns.str.contains(ch_average)]
                church_average = church_av.mean(axis=1)

            if ch_peak in df.columns:
                church_p = df.loc[:, df.columns.str.contains(ch_peak)]
                church_peak = church_p.max(axis=1)

            if he_average in df.columns:
                health_av = df.loc[:, df.columns.str.contains(he_average)]
                health_average = health_av.mean(axis=1)

            if he_peak in df.columns:
                health_p = df.loc[:, df.columns.str.contains(he_peak)]
                health_peak = health_p.max(axis=1)

            if sc_average in df.columns:
                school_av = df.loc[:, df.columns.str.contains(sc_average)]
                school_average = school_av.mean(axis=1)

            if sc_peak in df.columns:
                school_p = df.loc[:, df.columns.str.contains(sc_peak)]
                school_peak = school_p.max(axis=1)

            # New dataframe with the average consumer and peak values
            demand = pd.DataFrame({
                "Household Average": household_average,
                "Household Peak": household_peak,
                "Business Average": business_average,
                "Business Peak": business_peak,
                "Church Average": church_average,
                "Church Peak": church_peak,
                "Health Average": health_average,
                "Health Peak": health_peak,
                "School Average":  school_average,
                "School Peak": school_peak
            })

            # Append new dataframe to list of sheets
            sheets.append(demand)

        # Output file
        output_workbook = pd.ExcelWriter(os.path.join(daily_demand, f'{os.path.splitext(file)[0]}_24hr_profile.xlsx'))

        # Loop all stored sheets and write to output workbook created
        for i, df in enumerate(sheets):
            sheet_name = list(combined.keys())[i]
            df.to_excel(output_workbook, sheet_name=sheet_name, index=False)

        # Close output workbook
        output_workbook.close()
        print(f"Output saved to {daily_demand}.")


"""
The provided code reads consumer data from an Excel file ('Fiji Consumers.xlsx') into a pandas DataFrame (consumer_df). 
It then loops through a directory of daily demand files, and for each file, it reads the Excel file into a dictionary 
of DataFrames (df_file). It checks if the file name without the extension exists in the index of consumer_df, and if so,
it manipulates specific columns in the sheets of df_file based on the values in consumer_df using column name mappings. 
The manipulated data is then written to a new Excel file with a modified file name in a different directory 
('daily_demand_customers') using an Excel writer object (output_workbook).
"""
print("_________________Factoring number of consumers by type_____________________")
consumer_df = pd.read_excel('Fiji Consumers.xlsx', index_col=0)
print(consumer_df)

# Define a mapping dictionary for column name mapping
column_mapping = {
    'Household Average': 'Households',
    'Business Average': 'Businesses',
    'Church Average': 'Churches',
    'Health Average': 'Health Care',
    'School Average': 'Schools',
    'Household Peak': 'Households',
    'Business Peak': 'Businesses',
    'Church Peak': 'Churches',
    'Health Peak': 'Health Care',
    'School Peak': 'Schools',
}

for file_name in os.listdir(daily_demand):
    file_name_without_ext = os.path.splitext(file_name)[0]

    if file_name_without_ext in consumer_df.index:
        df_file = pd.read_excel(os.path.join(daily_demand, file_name), sheet_name=None)
        # Create a new Excel writer object with the output folder and resulting workbook name
        output_workbook = pd.ExcelWriter(os.path.join(daily_demand_customers, f'{file_name_without_ext}_result.xlsx'))
        # Loop through sheets in df_file
        for sheet_name, sheet_data in df_file.items():
            # Loop through columns in sheet_data
            for col_name in sheet_data.columns:
                # Check if the column name is present in the mapping dictionary
                if col_name in column_mapping.keys():
                    # Get the corresponding column name from the mapping dictionary
                    col_name_mapped = column_mapping[col_name]
                    # Multiply the column by the corresponding value from consumer_df
                    sheet_data[col_name] *= consumer_df.loc[file_name_without_ext, col_name_mapped]

            # Write the resulting sheet to the new workbook with the original sheet name
            sheet_data.to_excel(output_workbook, sheet_name=sheet_name, index=False)

        # Save and close the writer
        output_workbook.close()











