import os
from scipy.io import loadmat
import pandas as pd

# Define input folder containing .mat files
input_folder = "../finalproject_records"

# Define output folder for saving CSV files
output_folder = "csv_output"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Iterate over all files in the input folder
for filename in os.listdir(input_folder):
    # Process only .mat files
    if filename.endswith(".mat"):
        filepath = os.path.join(input_folder, filename)

        # Load the .mat file
        mat_data = loadmat(filepath)

        # Extract the main data key (skip internal __ keys)
        keys = [k for k in mat_data.keys() if not k.startswith("__")]
        if keys:
            data_key = keys[0]  # Assume the first relevant key holds the array
            array = mat_data[data_key]

            # Convert the NumPy array to a pandas DataFrame
            df = pd.DataFrame(array)

            # Define the output CSV file path
            output_filename = filename.replace(".mat", ".csv")
            output_path = os.path.join(output_folder, output_filename)

            # Save the DataFrame as a CSV file (without index column)
            df.to_csv(output_path, index=False)

            # Print confirmation message
            print(f"✅ Converted: {filename} → {output_filename}")
