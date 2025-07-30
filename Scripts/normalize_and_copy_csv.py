import os
import shutil

# Define input and output folders
input_folder = "csv_output"
output_folder = "csv_cleaned"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

renamed_count = 0

# Iterate over all files in the input folder
for filename in os.listdir(input_folder):
    # Skip non-CSV files
    if not filename.endswith(".csv"):
        continue

    # Normalize filename: convert to lowercase and fix known typos
    fixed_name = filename.lower()
    fixed_name = fixed_name.replace("insrtuct", "instruct")

    # Validate filename structure: should start with "dyad" and contain exactly two underscores
    if not fixed_name.startswith("dyad") or fixed_name.count("_") != 2:
        print(f" Skipping invalid file: {filename}")
        continue

    # Construct full source and destination paths
    src = os.path.join(input_folder, filename)
    dst = os.path.join(output_folder, fixed_name)

    # Copy the file to the cleaned folder only if it doesn't already exist there
    if not os.path.exists(dst):
        shutil.copyfile(src, dst)
        renamed_count += 1
        print(f"Copied & renamed: {filename} → {fixed_name}")
    else:
        print(f" Already exists: {fixed_name}")

# Print summary
print(f"\nTotal cleaned files: {renamed_count}")
print(f"Clean files saved to: {output_folder}")
