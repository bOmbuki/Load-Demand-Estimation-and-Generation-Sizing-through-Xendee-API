import pandas as pd
import os

"""
The provided code is designed to sort load data from Excel files. The code begins by specifying the folder path where
the Comet load profile data is stored and the folder path where the sorted data is to be stored. It then loops through
the files in the Comet folder. For each file, it reads the Excel file as a data frame and iterates through each sheet
in the file. If a column called 'time stamp' exists in the sheet, it converts all the values in that column into a
datetime format. The data in the sheet is then sorted in ascending order based on the 'time stamp' column, and the
resulting sorted data is stored in an empty list called 'sorted_data'. The sheet names are also stored in another
empty list called 'sheet_names'. Finally, the data frames in the 'sorted_data' list are written to an Excel file with
the prefix "Sorted_" added to the original name of the Comet data file. The sheet names in the Excel file are kept the
same as the original sheet names. The sorted Excel file is stored in a new folder specified by the 'sorted_folder_path'
variable, and the process is repeated for each file in the Comet folder.
"""

data_path = 'C:\\Users\\bmogaka\\Desktop\\LEAPS\\GEA\\Load Profile Test Run\\Comet Data'
#'C:\\Users\\bmogaka\\Desktop\\Fiji\\Comet Data' #Format 'C:\\Users\\bmogaka\\Desktop\\Fiji\\Comet Data'

# Get the path where the CSV files will be saved
save_path = 'C:\\Users\\bmogaka\\Desktop\\LEAPS\\GEA\\Load Profile Test Run\\Sorted Comet Data' #'C:\\Users\\bmogaka\\Desktop\\Fiji\\Sorted Comet Data'

file_list = os.listdir(data_path)

#Looping through each file in the defined file path and sorting it
for file_name in file_list:
    if file_name.endswith('xlsx'):
        file_path = os.path.join(data_path, file_name)

        # Convert the data from file i into a dataframe
        xl = pd.read_excel(file_path, sheet_name=None)

        # Empty list to store dataframes
        sorted_data = []

        # List to store sheet_names
        sheet_names = []

        # Looping through all sheets in the excel file
        for sheet_name, df in xl.items():
            if 'time_stamp' in df.columns:
                # Converting data in the time stamp column to datetime
                df['time_stamp'] = pd.to_datetime(df['time_stamp'])
                # Sort values in the data frame based on the time stamp column
                df.sort_values(by='time_stamp', inplace=True, ignore_index = True)
                # Add sorted data for each sheet into the list
                sorted_data.append(df)
                # Add sheet names into the list
                sheet_names.append(sheet_name)
            else:
                print(f"Column 'time_stamp' not in {sheet_name}")

        # Write each sorted data to a different sheet in the same Excel file
        sorted_file_name = os.path.join(save_path, f"Sorted_{file_name}")
        with pd.ExcelWriter(sorted_file_name) as writer:
            for i, df in enumerate(sorted_data):
                sheet_name = sheet_names[i]
                df.to_excel(writer, sheet_name=sheet_name, index=False)
    else:
        print(f'Invalid path: {data_path}')
