import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# 🔹 Load the global brain measures CSV file from the Scripts folder
df = pd.read_csv("../Scripts/Global_brain_measures.csv")

# 🔹 List of global graph metrics to be analyzed
metrics = [
    "Mean Degree",
    "Mean Clustering Coefficient",
    "Global Efficiency",
    "Modularity",
    "Small-Worldness"
]

# 🔹 Compute correlation matrix between metrics (excluding rows with missing values)
df_metrics = df[metrics].dropna()
corr_matrix = df_metrics.corr()

# 🔹 Create necessary output folders
os.makedirs("comparisons_output", exist_ok=True)
os.makedirs("visualizations", exist_ok=True)

# 🔹 Save correlation matrix as CSV
corr_matrix.to_csv("comparisons_output/metrics_correlation_matrix.csv")

# 🔹 Generate heatmap of the correlation matrix
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap="YlOrBr", fmt=".2f")
plt.title("Correlation Between Global Graph Metrics")
plt.tight_layout()
plt.savefig("visualizations/metrics_correlation_heatmap.png")
plt.close()

print("✅ compare_metric_correlations completed.")
