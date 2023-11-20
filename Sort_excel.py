import pandas as pd
import os
from folder_funcs import folder_paths

# Data Path where field collected data is stored
data_path = folder_paths[1]

# Get the path where the CSV files will be saved
save_path = folder_paths[5][2]

file_list = os.listdir(data_path)

# Looping through each file in the defined file path and sorting it
print(f'_____________Sorting Field Data Files____________')
for file_name in file_list:
    print(f'Sorting File: {file_name}.')
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
                df['time_stamp'] = pd.to_datetime(df['time_stamp'], format='%I:%M:%S %p')
                # Sort values in the data frame based on the time stamp column
                df.sort_values(by='time_stamp', inplace=True, ignore_index = True)
                # Add sorted data for each sheet into the list
                sorted_data.append(df)
                # Add sheet names into the list
                sheet_names.append(sheet_name)
            else:
                print(f">>>Column 'time_stamp' not in workbook sheet - {sheet_name}\n")

        # Write each sorted data to a different sheet in the same Excel file
        sorted_file_name = os.path.join(save_path, f"Sorted_{file_name}")
        with pd.ExcelWriter(sorted_file_name) as writer:
            for i, df in enumerate(sorted_data):
                sheet_name = sheet_names[i]
                df.to_excel(writer, sheet_name=sheet_name, index=False)
    else:
        print(f'Invalid path: {data_path}')
