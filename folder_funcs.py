import os

def create_load_profile_estimation_folder_structure():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    main_folder = os.path.join(desktop_path, "Load Profile Estimation")
    field_data = os.path.join(main_folder, "Field Data")
    demand = os.path.join(main_folder, "Demand")
    sorted_data = os.path.join(main_folder, 'Sorted Data')

    demand_subfolders = [
        os.path.join(demand, "Estimated Consumer Demand"),
        os.path.join(demand, "Final Seasons Data"),
        os.path.join(demand, "Village Demand"),
        os.path.join(demand, "Xendee Inputs"),
        os.path.join(demand, "Yearly Load Profile"),
    ]

    sorted_data_subfolders = [
        os.path.join(sorted_data, "Combined Sessions"),
        os.path.join(sorted_data, "Hourly Field Data"),
        os.path.join(sorted_data, "Sorted Field Data"),
    ]

    folders = [main_folder, field_data, demand, sorted_data] + demand_subfolders + sorted_data_subfolders

    for folder in folders:
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
                print(f"Folder created: {folder}")
            except Exception as e:
                print(f"Error creating folder {folder}: {e}")
        else:
            print(f"Folder already exists: {folder}")

    # Return the paths of the created folders
    return main_folder, field_data, demand, sorted_data, demand_subfolders, sorted_data_subfolders

print(f'__________Creating Data Folder System___________')
folder_paths = create_load_profile_estimation_folder_structure()

def get_main_folder_path():
    return folder_paths[0]

def get_field_data_path():
    return folder_paths[1]

def get_demand_path():
    return folder_paths[2]

def get_sorted_data_path():
    return folder_paths[3]

def get_estimated_consumer_demand_path():
    return folder_paths[4][0]

def get_final_seasons_data_path():
    return folder_paths[4][1]

def get_village_demand_path():
    return folder_paths[4][2]

def get_xendee_inputs_path():
    return folder_paths[4][3]

def get_yearly_load_profile_path():
    return folder_paths[4][4]

def get_combined_sessions_path():
    return folder_paths[5][0]

def get_hourly_field_data_path():
    return folder_paths[5][1]

def get_sorted_field_data_path():
    return folder_paths[5][2]
