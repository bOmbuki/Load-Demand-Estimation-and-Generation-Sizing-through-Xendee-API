import numpy as np
import pandas as pd
import os
import re
import plot_creator
from folder_creator import daily_demand_customers, seasons_data_sorted, yearly_demand_time_steps, xendee_inputs, load_curves

seasons_data = daily_demand_customers

average_demand = ['Household Average', 'Business Average', 'Religion Average', 'Health Average', 'School Average']
peak_demand = ['Household Peak', 'Business Peak', 'Religion Peak', 'Health Peak', 'School Peak']

# Define the date range for the DataFrame
start_date = '2023-01-01 00:00:00'
end_date = '2023-12-31 23:59:59'

# Loop through each file in the folder
for filename in os.listdir(seasons_data):
    if filename.endswith('.xlsx') or filename.endswith('.xls'):  # Check if file is an Excel file
        file_path = os.path.join(seasons_data, filename)
        excel_file = pd.ExcelFile(file_path)  # Open the Excel file
        sheet_names = excel_file.sheet_names  # Get the sheet names

        s1_weekday = pd.Series(dtype=float)
        s1_weekday_peak = pd.Series(dtype=float)
        s1_weekend = pd.Series(dtype=float)
        s1_weekend_peak = pd.Series(dtype=float)
        s2_weekday = pd.Series(dtype=float)
        s2_weekday_peak = pd.Series(dtype=float)
        s2_weekend = pd.Series(dtype=float)
        s2_weekend_peak = pd.Series(dtype=float)

        # Loop through each sheet in the Excel file
        for sheet_name in sheet_names:
            # Read the sheet into a DataFrame
            excel_df = pd.read_excel(excel_file, sheet_name=sheet_name)

            # Check if column headers in average demand and peak demand are present in excel_df
            common_cols_average = list(set(average_demand) & set(excel_df.columns))
            common_cols_peak = list(set(peak_demand) & set(excel_df.columns))

            # Calculate the sum along axis=1 for columns in average demand and store in corresponding DataFrame
            if sheet_name == 'S1_Weekday':
                mean_df = excel_df[common_cols_average].sum(axis=1)
                s1_weekday = pd.concat([s1_weekday, pd.Series(mean_df)], ignore_index=True)

            elif sheet_name == 'S2_Weekday':
                mean_df = excel_df[common_cols_average].sum(axis=1)
                s2_weekday = pd.concat([s2_weekday, pd.Series(mean_df)], ignore_index=True)

            elif sheet_name == 'S1_Weekend':
                mean_df = excel_df[common_cols_average].sum(axis=1)
                s1_weekend = pd.concat([s1_weekend, pd.Series(mean_df)], ignore_index=True)

            elif sheet_name == 'S2_Weekend':
                mean_df = excel_df[common_cols_average].sum(axis=1)
                s2_weekend = pd.concat([s2_weekend, pd.Series(mean_df)], ignore_index=True)

            # Calculate maximum value along axis=1 for columns in peak_demand and store in corresponding DataFrame
            if sheet_name == 'S1_Weekday':
                max_df = excel_df[peak_demand].sum(axis=1)
                s1_weekday_peak = pd.concat([s1_weekday_peak, pd.Series(max_df)], ignore_index=True)

            elif sheet_name == 'S2_Weekday':
                max_df = excel_df[peak_demand].sum(axis=1)
                s2_weekday_peak = pd.concat([s2_weekday_peak, pd.Series(max_df)], ignore_index=True)

            elif sheet_name == 'S1_Weekend':
                max_df = excel_df[peak_demand].sum(axis=1)
                s1_weekend_peak = pd.concat([s1_weekend_peak, pd.Series(max_df)], ignore_index=True)

            elif sheet_name == 'S2_Weekend':
                max_df = excel_df[peak_demand].sum(axis=1)
                s2_weekend_peak = pd.concat([s2_weekend_peak, pd.Series(max_df)], ignore_index=True)

            s1_concat_peak = pd.concat([s1_weekday_peak,s1_weekend_peak], axis=1)
            s1_peak = pd.Series(s1_concat_peak.max(axis=1))

            s2_concat_peak = pd.concat([s2_weekday_peak, s2_weekend_peak], axis=1)
            s2_peak = pd.Series(s2_concat_peak.max(axis=1))

        # Creating final hourly excel file for year profile generation
        daily_lp = pd.DataFrame({
            'S1_Weekday': s1_weekday,
            'S2_Weekday': s2_weekday,
            'S1_Weekend': s1_weekend,
            'S2_Weekend': s2_weekend,
            'S1_Peak': s1_peak,
            'S2_Peak': s2_peak,
        })

        # Randomizing the data frame using a random normal distribution
        for column in daily_lp.columns:
            upper_limit = 1.2 * daily_lp[column]
            lower_limit = 0.8 * daily_lp[column]
            z_score = 1.96  # Z-score for a 95% confidence interval
            scale = (upper_limit - lower_limit) / (2 * z_score)
            daily_lp[column] = np.random.normal(loc=daily_lp[column], scale=scale, size=daily_lp.shape[0])

        output_name = os.path.splitext(filename)[0] + '.xlsx'
        output_file_path = os.path.join(seasons_data_sorted, output_name)
        daily_lp.to_excel(output_file_path, index=False)

# Loop generate daily load profile curves
for file_name in os.listdir(seasons_data_sorted):
    if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
        file_path = os.path.join(seasons_data_sorted, file_name)

        # Extract village name from the file name
        match = re.search(r'Sorted_(.*?) -', file_name)

        if match:
            village_name = match.group(1).strip()

            # Read the Excel file into a DataFrame
            df = pd.read_excel(os.path.join(seasons_data_sorted, file_name))

            # Call the plotting function for the current DataFrame
            plot_creator.plot_load_curves(df, load_curves, f'{village_name} Load Curves')

# Define date ranges for two periods
start_date_period1 = pd.to_datetime('2023-01-01')
end_date_period1 = pd.to_datetime('2023-04-30 23:59:59')
start_date_period2 = pd.to_datetime('2023-05-01')
end_date_period2 = pd.to_datetime('2023-10-31 23:59:59')
start_date_period3 = pd.to_datetime('2023-11-01')
end_date_period3 = pd.to_datetime('2023-12-31 23:59:59')

# Yearly load profile generation
for file in os.listdir(seasons_data_sorted):
    if file.endswith('.xlsx') or file.endswith('.xls'):  # Check if file is an Excel file
        file_path = os.path.join(seasons_data_sorted, file)
        excel_file = pd.read_excel(file_path)  # Open the Excel file

        s1_weekday_demand = excel_file['S1_Weekday'].tolist()
        s2_weekday_demand = excel_file['S2_Weekday'].tolist()
        s1_weekend_demand = excel_file['S1_Weekend'].tolist()
        s2_weekend_demand = excel_file['S2_Weekend'].tolist()
        s1_peak_demand = excel_file['S1_Peak'].tolist()
        s2_peak_demand = excel_file['S2_Peak'].tolist()
        s3_weekday_demand = s1_weekday_demand
        s3_weekend_demand = s1_weekend_demand
        s3_peak_demand = s1_peak_demand

        # Create a list of dates within the date range
        dates = pd.date_range(start=start_date, end=end_date, freq='H')

        # Create a DataFrame with 'Date' column
        df = pd.DataFrame({'Date': dates})

        # Create a 'Time Step' column with values ranging from 0 to 23
        df['Time Step'] = df['Date'].dt.hour

        # Create empty 'Load' column
        df['Load'] = None

        # Loop through the DataFrame and fill in the 'Load' column for period 1
        for idx, row in df.iterrows():

            if start_date_period1 <= row['Date'] <= end_date_period1:
                if row['Date'].dayofweek < 5: #Weekdays (Monday to Friday)
                    if row['Date'].is_month_end and row['Date'].day == row['Date'].days_in_month:
                        df.at[idx, 'Load'] = s1_peak_demand[row['Time Step']]
                    else:
                        df.at[idx, 'Load'] = s1_weekday_demand[row['Time Step']]
                elif row['Date'].dayofweek >= 5 and row['Date'].dayofweek <= 6:
                    if row['Date'].is_month_end and row['Date'].day == row['Date'].days_in_month:
                        df.at[idx, 'Load'] = s1_peak_demand[row['Time Step']]
                    else:
                        df.at[idx, 'Load'] = s1_weekend_demand[row['Time Step']]

            elif start_date_period2 <= row['Date'] <= end_date_period2:
                if row['Date'].dayofweek < 5:
                    if row['Date'].is_month_end and row['Date'].day == row['Date'].days_in_month:
                        df.at[idx, 'Load'] = s2_peak_demand[row['Time Step']]
                    else:
                        df.at[idx, 'Load'] = s2_weekday_demand[row['Time Step']]
                elif row['Date'].dayofweek >= 5 and row['Date'].dayofweek <= 6:
                    if row['Date'].is_month_end and row['Date'].day == row['Date'].days_in_month:
                        df.at[idx, 'Load'] = s2_peak_demand[row['Time Step']]
                    else:
                        df.at[idx, 'Load'] = s2_weekend_demand[row['Time Step']]

            elif start_date_period3 <= row['Date'] <= end_date_period3:
                if row['Date'].dayofweek < 5:
                    if row['Date'].is_month_end and row['Date'] == row['Date'].days_in_month:
                        df.at[idx, 'Load'] = s3_peak_demand[row['Time Step']]
                    else:
                        df.at[idx, 'Load'] = s3_weekday_demand[row['Time Step']]
                elif row['Date'].dayofweek >= 5 and row['Date'].dayofweek <= 6:
                    if row['Date'].is_month_end and row['Date'] == row['Date'].days_in_month:
                        df.at[idx, 'Load'] = s3_peak_demand[row['Date']]
                    else:
                        df.at[idx, 'Load'] = s3_weekend_demand[row['Time Step']]

        # Save the generated load profile as an Excel file with the original filename
        output_file_name = file.replace('Session _combined_24hr_profile_result.xlsx', 'output.xlsx')
        output_file_path = os.path.join(yearly_demand_time_steps, output_file_name)
        df.to_excel(output_file_path, index=False)
        print(f"{output_file_name} 'Yearly load profile generation completed successfully!")


# Xendee inputs
print(f'\n____________Creating Xendee Inputs___________')
for file in os.listdir(yearly_demand_time_steps):
    if file.endswith('.xlsx') or file.endswith('.xls'):  # Check if file is an Excel file
        file_path = os.path.join(yearly_demand_time_steps, file)
        excel_file = pd.read_excel(file_path)

        xendee_df = excel_file.drop(['Date', 'Time Step'], axis=1)

        output_file_name = file.replace(' - output.xlsx', '.csv').replace('Sorted_', '')
        output_file_path = os.path.join(xendee_inputs, output_file_name)
        xendee_df.to_csv(output_file_path, index=False, header=False)
        print(f"{output_file_name} Xendee input file completed successfully!")

# Converting Xendee Inputs into format acceptable for the API based optimization
current_directory = os.getcwd()

# Get a list of all csv files in the Xendee inputs folder
files = os.listdir(xendee_inputs)
csv_files = [file for file in files if file.endswith('.csv')]
dfs_list = []
file_names = []

# Loop through each csv file in csv_files
for csv_file in csv_files:
    # Read the csv file into a dataframe with file name as header
    df = pd.read_csv(os.path.join(xendee_inputs, csv_file))

    # Extract the file name without the extension
    file_name = os.path.splitext(csv_file)[0]

    # Append the dataframe to a list
    dfs_list.append(df)

    # Add the file name to the file_names list
    file_names.append(file_name)

# Concatenate all the data frames in dfs_list
final_df = pd.concat(dfs_list, axis=1, keys=file_names)

# Save the final dataframe to a csv file in the current working directory
csv_file_path = os.path.join(current_directory, 'Load Profile.csv')
final_df.to_csv(csv_file_path, index=False)



