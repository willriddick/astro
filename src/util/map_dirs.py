import os
import json

def create_map_directories(base_path, x_size, y_size):
    # Define the main folder name
    main_folder = f"{x_size}x{y_size}"
    main_folder_path = os.path.join(base_path, main_folder)

    # Define the subdirectories
    subdirectories = ["1_2", "3", "4", "5_6", "7", "8", "9_10", "11", "12", "13_14", "15"]

    # Create the main folder if it doesn't exist
    os.makedirs(main_folder_path, exist_ok=True)

    # Create each subdirectory and write the 0.json file
    for subdir in subdirectories:
        subdir_path = os.path.join(main_folder_path, subdir)
        os.makedirs(subdir_path, exist_ok=True)

        # Define the content of the 0.json file
        content = {
            "size": [x_size, y_size],
            "tiles": [{"t":"stone","v":0,"p":[1,1]}]
        }

        # Write the 0.json file
        json_file_path = os.path.join(subdir_path, "0.json")
        with open(json_file_path, 'w') as json_file:
            json.dump(content, json_file, separators=(',', ':'))

# Usage example
base_path = "maps"
x_size = 14
y_size = 10
create_map_directories(base_path, x_size, y_size)