# run_all.py
# Master script to execute the full fNIRS intra-brain analysis pipeline

import os

# Step 1: Convert .mat to .csv
os.system("python Scripts/convert_mat_to_csv.py")

# Step 2: Clean and normalize CSVs
os.system("python Scripts/clean_and_normalize_csv.py")

# Step 3: Compute correlation matrices
os.system("python Scripts/intra_brain_connectivity.py")

# Step 4: Extract graph metrics
os.system("python Scripts/extract_intra_measures.py")

# Step 5: Global metric comparisons
os.system("python analysis/compare_conditions.py")
os.system("python analysis/compare_dyadic_symmetry.py")
os.system("python analysis/compare_metric_correlations.py")
os.system("python analysis/compare_roles_by_dyad.py")

# Step 6: Local node strength analysis
os.system("python local_analysis/compare_strength_dyadic_difference.py")
os.system("python local_analysis/compare_strength_by_condition.py")

print("\nPipeline complete! You can now open 'index.html' to view results.")
