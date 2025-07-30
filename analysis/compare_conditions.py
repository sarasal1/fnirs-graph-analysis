import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# 🔹 Step 1: Load the CSV containing global graph measures
df_raw = pd.read_csv("../Scripts/Global_brain_measures.csv")

# 🔹 Step 2: Compute average values per Condition and Role
metrics = [
    "Mean Degree",
    "Mean Clustering Coefficient",
    "Global Efficiency",
    "Modularity",
    "Small-Worldness"
]

summary = (
    df_raw.groupby(["Condition", "Role"])[metrics]
    .mean()
    .round(3)
    .reset_index()
)

# 🔹 Step 3: Save the summary table as a CSV
summary_path = "comparisons_output/condition_comparison_summary.csv"
os.makedirs("comparisons_output", exist_ok=True)
summary.to_csv(summary_path, index=False)
print(f"✅ Saved condition comparison summary to: {summary_path}")

# 🔹 Step 4: Generate separate bar plots for each metric
df = summary
output_dir = "visualizations"
os.makedirs(output_dir, exist_ok=True)
sns.set(style="whitegrid")

for metric in metrics:
    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x="Condition", y=metric, hue="Role", palette="Set3")
    plt.title(f"{metric} by Condition and Role")
    plt.ylabel(metric)
    plt.tight_layout()
    filename = f"{metric.lower().replace(' ', '_')}_barplot.png"
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

print(f"✅ Saved individual metric plots to: {output_dir}/")
