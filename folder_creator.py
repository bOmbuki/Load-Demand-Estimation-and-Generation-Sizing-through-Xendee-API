import os

def create_load_profile_estimation_folder_structure():
    """This function creates a series of folders on a user desktop, and retrieves the folder paths of each of the
    folders created."""
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    main_folder = os.path.join(desktop_path, "Load Profile Estimation")
    #field_data = os.path.join(main_folder, "Field Data")
    demand = os.path.join(main_folder, "Demand")
    sorted_data = os.path.join(main_folder, 'Sorted Data')

    demand_subfolders = [
        os.path.join(demand, "Estimated Consumer Demand"),
        os.path.join(demand, "Final Seasons Data"),
        os.path.join(demand, "Village Demand"),
        os.path.join(demand, "Xendee Inputs"),
        os.path.join(demand, "Yearly Load Profile"),
        os.path.join(demand, 'Load Curves'),
    ]

    sorted_data_subfolders = [
        os.path.join(sorted_data, "Combined Sessions"),
        os.path.join(sorted_data, "Hourly Field Data"),
        os.path.join(sorted_data, "Sorted Field Data"),
    ]

    folders = [main_folder, demand, sorted_data] + demand_subfolders + sorted_data_subfolders

    for folder in folders:
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
                print(f"Folder created: {folder}")
            except Exception as e:
                print(f"Error creating folder {folder}: {e}")
        else:
            pass
             #print(f"Folder already exists: {folder}")

    # Return the paths of the created folders
    return main_folder, demand, sorted_data, demand_subfolders, sorted_data_subfolders


#print(f'__________Creating Data Folder System___________')
folder_paths = create_load_profile_estimation_folder_structure()
#for path in folder_paths:
#    print(path)

# Get the path where the CSV files will be saved
#data_path = folder_paths[1]
save_path = folder_paths[4][2]  # Sorted Field Data Folder Path
peak_average = folder_paths[4][1]  # Hourly Field Data Folder Path
combined_sessions = folder_paths[4][0]  # Combined Sessions Folder Path
daily_demand = folder_paths[3][0]  # Estimated Demand Folder Path
daily_demand_customers = folder_paths[3][2]  # Village Demand Folder Path
seasons_data_sorted = folder_paths[3][1]  # Final Seasons Data Folder Path
yearly_demand_time_steps = folder_paths[3][4]  # Yearly Load Profile Folder Path
xendee_inputs = folder_paths[3][3]  # Xendee Inputs Folder Path
load_curves = folder_paths[3][5]  # Load Curves Folder Path

