import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 🔹 Load the global brain metrics CSV file
df = pd.read_csv("../Scripts/Global_brain_measures.csv")

# 🔹 Define the list of graph metrics to compare
metrics = [
    "Mean Degree",
    "Mean Clustering Coefficient",
    "Global Efficiency",
    "Modularity",
    "Small-Worldness"
]

# 🔹 Compute absolute differences between baby and parent for each dyad and each metric
rows = []
for dyad in df["Dyad"].unique():
    sub = df[df["Dyad"] == dyad]
    if set(sub["Role"]) != {"baby", "perant"}:
        continue
    baby = sub[sub["Role"] == "baby"].iloc[0]
    parent = sub[sub["Role"] == "perant"].iloc[0]
    for metric in metrics:
        if pd.notna(baby[metric]) and pd.notna(parent[metric]):
            diff = abs(baby[metric] - parent[metric])
            rows.append({
                "Dyad": dyad,
                "Metric": metric,
                "Absolute Difference": round(diff, 3)
            })

# 🔹 Create DataFrame and save results as CSV in comparisons_output folder
df_sym = pd.DataFrame(rows)
os.makedirs("comparisons_output", exist_ok=True)
df_sym.to_csv("comparisons_output/dyadic_symmetry_results.csv", index=False)

# 🔹 Generate a bar plot: average absolute difference per metric across dyads
summary = df_sym.groupby("Metric")["Absolute Difference"].mean().sort_values()
plt.figure(figsize=(8, 5))
sns.barplot(x=summary.index, y=summary.values, palette="coolwarm")
plt.title("Dyadic Symmetry: Average Absolute Difference per Metric")
plt.ylabel("Avg |Difference|")
plt.xticks(rotation=30)
plt.tight_layout()

# 🔹 Save the plot to visualizations folder
os.makedirs("visualizations", exist_ok=True)
plt.savefig("visualizations/dyadic_symmetry_avgdiff.png")
plt.close()

print("✅ compare_dyadic_symmetry completed.")
