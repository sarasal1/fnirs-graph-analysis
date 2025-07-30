import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# 🔹 Load the global brain metrics CSV file
df = pd.read_csv("../Scripts/Global_brain_measures.csv")

# 🔹 List of graph metrics to compare
metrics = [
    "Mean Degree",
    "Mean Clustering Coefficient",
    "Global Efficiency",
    "Modularity",
    "Small-Worldness"
]

# 🔹 Compare each dyad's baby vs parent values for each metric
results = []
for dyad in df["Dyad"].unique():
    sub = df[df["Dyad"] == dyad]
    if set(sub["Role"]) != {"baby", "perant"}:
        continue
    baby = sub[sub["Role"] == "baby"].iloc[0]
    parent = sub[sub["Role"] == "perant"].iloc[0]
    for metric in metrics:
        if pd.notna(baby[metric]) and pd.notna(parent[metric]):
            winner = (
                "baby" if baby[metric] > parent[metric]
                else "parent" if parent[metric] > baby[metric]
                else "tie"
            )
            results.append({
                "Dyad": dyad,
                "Metric": metric,
                "Baby": round(baby[metric], 3),
                "Parent": round(parent[metric], 3),
                "Higher": winner
            })

# 🔹 Create a DataFrame and save results to CSV inside comparisons_output
df_result = pd.DataFrame(results)
os.makedirs("comparisons_output", exist_ok=True)
df_result.to_csv("comparisons_output/dyad_role_comparisons.csv", index=False)

# 🔹 Create summary bar plot: who had the higher value per metric
summary = df_result.groupby(["Metric", "Higher"]).size().unstack().fillna(0)
summary.plot(kind="bar", figsize=(10, 6), colormap="Set2")
plt.title("Who Has Higher Value? Parent vs Baby (per Metric)")
plt.ylabel("Number of Dyads")
plt.xticks(rotation=30)
plt.tight_layout()

# 🔹 Save the plot inside visualizations folder
os.makedirs("visualizations", exist_ok=True)
plt.savefig("visualizations/baby_vs_parent_comparison.png")
plt.close()

print("✅ compare_roles_by_dyad completed.")
