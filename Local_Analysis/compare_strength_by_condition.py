"""
Script Name: compare_strength_by_condition.py

Description:
This script analyzes and visualizes local node strength metrics computed from fNIRS intra-brain correlation data.
It reads a CSV containing node-level strengths for each participant (baby/parent) under various conditions,
computes the average strength per node, and generates comparison plots between roles.

Key Features:
- Fixes label typos in the input data.
- Sorts nodes numerically (S1 to S18).
- Computes group-level average strength per node by condition and role.
- Saves output as a structured CSV and visualizes results using bar plots.

Inputs:
- ../Scripts/Local_strengths.csv

Outputs:
- local_comparisons_output/local_strength_condition.csv
- local_visualizations/strength_by_node_<condition>.png

Dependencies:
- Python 3.x
- pandas, seaborn, matplotlib, os
"""
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 🔹 Define path to the local strengths CSV file (relative to this script)
csv_input_path = os.path.join("..", "Scripts", "Local_strengths.csv")

# Load data from CSV
df = pd.read_csv(csv_input_path)

# Fix typo in role labels: 'perant' → 'parent'
df["Role"] = df["Role"].replace("perant", "parent")

# Sort nodes numerically (S1 to S18)
df["Node_num"] = df["Node"].str.extract(r'S(\d+)').astype(int)
df = df.sort_values("Node_num")
df.drop(columns="Node_num", inplace=True)

# 🔹 Compute average strength per (Condition, Role, Node)
summary = (
    df.groupby(["Condition", "Role", "Node"])["Strength"]
    .mean()
    .round(3)
    .reset_index()
)

# 🔹 Create output folders relative to the current script directory
output_dir = "local_comparisons_output"
plots_dir = "local_visualizations"
os.makedirs(output_dir, exist_ok=True)
os.makedirs(plots_dir, exist_ok=True)

# 🔹 Save summary as a CSV file
csv_output_path = os.path.join(output_dir, "local_strength_condition.csv")
summary.to_csv(csv_output_path, index=False)
print(f"✅ Saved summary to: {csv_output_path}")

# 🔹 Generate and save bar plots for each condition
conditions = summary["Condition"].unique()
for cond in conditions:
    plt.figure(figsize=(12, 6))
    sub = summary[summary["Condition"] == cond]
    sns.barplot(data=sub, x="Node", y="Strength", hue="Role", palette="Set2")
    plt.title(f"Average Node Strength - {cond}")
    plt.ylabel("Mean Strength")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plot_path = os.path.join(plots_dir, f"strength_by_node_{cond}.png")
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"📊 Saved plot: {plot_path}")
