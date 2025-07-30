"""
Script Name: compare_strength_by_dyad.py

Description:
This script compares local node strengths between baby and parent participants across dyads.
It reads the precomputed node strengths from fNIRS intra-brain analysis and:
1. Calculates the strength difference (baby - parent) for each node in each dyad.
2. Saves the results in a structured CSV file.
3. Visualizes the average difference across all dyads as a bar plot.

Inputs:
- ../Scripts/Local_strengths.csv

Outputs:
- local_comparisons_output/local_strength_dyad_comparison.csv
- local_visualizations/strength_difference_by_node.png

Dependencies:
- Python 3.x
- pandas, seaborn, matplotlib
"""
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 🔹 Load CSV from Scripts directory
csv_input_path = os.path.join("..", "Scripts", "Local_strengths.csv")
df = pd.read_csv(csv_input_path)

# Fix typo in Role column: 'perant' → 'parent'
df["Role"] = df["Role"].replace("perant", "parent")

# 🔹 Compute strength differences between baby and parent for each dyad and node
results = []
dyads = df["Dyad"].unique()
nodes = sorted(df["Node"].unique())

for dyad in dyads:
    sub = df[df["Dyad"] == dyad]
    for node in nodes:
        node_data = sub[sub["Node"] == node]
        # Ensure both roles exist for this node in this dyad
        if set(node_data["Role"]) != {"baby", "parent"}:
            continue
        baby_val = node_data[node_data["Role"] == "baby"]["Strength"].values[0]
        parent_val = node_data[node_data["Role"] == "parent"]["Strength"].values[0]
        diff = baby_val - parent_val
        results.append({
            "Dyad": dyad,
            "Node": node,
            "Baby Strength": round(baby_val, 3),
            "Parent Strength": round(parent_val, 3),
            "Difference (Baby - Parent)": round(diff, 3)
        })

df_diff = pd.DataFrame(results)

# 🔹 Create local folders for saving outputs (relative to current script)
output_dir = "local_comparisons_output"
plots_dir = "local_visualizations"
os.makedirs(output_dir, exist_ok=True)
os.makedirs(plots_dir, exist_ok=True)

# 🔹 Save comparison table as CSV
csv_output_path = os.path.join(output_dir, "local_strength_dyad_comparison.csv")
df_diff.to_csv(csv_output_path, index=False)
print("✅ Saved CSV to:", csv_output_path)

# 🔹 Plot: average strength difference per node (Baby - Parent)
avg_diff = df_diff.groupby("Node")["Difference (Baby - Parent)"].mean().sort_index()

plt.figure(figsize=(10, 6))
sns.barplot(x=avg_diff.index, y=avg_diff.values, palette="coolwarm")
plt.axhline(0, linestyle="--", color="gray")
plt.title("Average Strength Difference (Baby - Parent) per Node")
plt.ylabel("Mean Difference")
plt.xlabel("Node")
plt.tight_layout()

plot_path = os.path.join(plots_dir, "strength_difference_by_node.png")
plt.savefig(plot_path, dpi=300)
plt.close()

print("✅ Saved plot to:", plot_path)
