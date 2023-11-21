import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

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
        os.path.join(demand, 'Load Curves'),
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

# Function to plot load curves
def plot_load_curves(df, output_folder, file_name):
    # Generate x-axis values with higher resolution
    hours_high_res = np.linspace(0, 23, 1000)

    # Create a figure and axes for subplots
    fig, axs = plt.subplots(2, 1, figsize=(10, 12))  # 2 rows, 1 column

    # Subplot 1: S1
    axs[0].set_title('Load Curves - S1')
    for i, column in enumerate(['S1_Weekday', 'S1_Weekend', 'S1_Peak']):
        spline = interp1d(np.arange(24), df[column], kind='quadratic')
        interpolated_curve = spline(hours_high_res)
        color = 'brown' if i == 0 else 'blue' if i == 1 else 'green'
        max_value = df[column].max()
        axs[0].plot(hours_high_res, interpolated_curve, label=f'{column} (Peak: {max_value:.2f})', color=color, linewidth=2)

    axs[0].set_xticks(np.arange(0, 24, 1))
    axs[0].set_xticklabels([str(int(h)) for h in np.arange(0, 24, 1)], rotation=45)
    axs[0].set_xlabel('Hour')
    axs[0].set_ylabel('Load(kW)')
    axs[0].legend()
    axs[0].grid()

    # Subplot 2: S2
    axs[1].set_title('Load Curves - S2')
    for i, column in enumerate(['S2_Weekday', 'S2_Weekend', 'S2_Peak']):
        spline = interp1d(np.arange(24), df[column], kind='quadratic')
        interpolated_curve = spline(hours_high_res)
        color = 'brown' if i == 0 else 'blue' if i == 1 else 'green'
        max_value = df[column].max()
        axs[1].plot(hours_high_res, interpolated_curve, label=f'{column} (Peak: {max_value:.2f})', color=color, linewidth=2)

    axs[1].set_xticks(np.arange(0, 24, 1))
    axs[1].set_xticklabels([str(int(h)) for h in np.arange(0, 24, 1)], rotation=45)
    axs[1].set_xlabel('Hour')
    axs[1].set_ylabel('Load(kW)')
    axs[1].legend()
    axs[1].grid()

    # Adjust layout
    plt.tight_layout()

    # Save the figure to the specified folder
    output_file_path = os.path.join(output_folder, f'{file_name}.png')
    plt.savefig(output_file_path)

    # Show the plot (optional)
    #plt.show()

    # Close figure
    plt.close()

print(f'__________Creating Data Folder System___________')
folder_paths = create_load_profile_estimation_folder_structure()
#for path in folder_paths:
    #print(path)

