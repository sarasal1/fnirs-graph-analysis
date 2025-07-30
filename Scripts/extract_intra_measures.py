"""
Script Name: extract_intra_measures.py

Description:
This script computes both **global** and **local** graph-theoretical metrics for intra-brain networks
based on 18×18 correlation matrices derived from fNIRS hyperscanning data.

The input files are correlation matrices (.csv) for each participant (baby or parent) under a given condition.
Two types of analyses are performed:
1. Global metrics per brain graph: mean degree, clustering coefficient, global efficiency, modularity, and small-worldness.
2. Local metrics per node: node strength (sum of absolute correlations) per channel.

Each section of the script:
- Extracts dyad, condition, and role from filenames.
- Computes the relevant measures using NetworkX and NumPy.
- Saves results into structured CSV files.
- Generates interactive HTML summary tables for visualization.

Inputs:
- Folder: "intra_correlation_matrices/"
  → Files named as: correlation_dyad<id>_<condition>_<role>.csv

Outputs:
- Global graph metrics:
    → "Global_brain_measures.csv"
    → "Global_brain_measures_report.html"
- Local node strengths:
    → "Local_strengths.csv"
    → "local_brain_measures_report.html"

Dependencies:
- Python 3.x
- numpy, pandas, networkx, community, matplotlib
"""

import os
import pandas as pd
import numpy as np
import networkx as nx
import community as community_louvain

# === Setup: Folders and Output Filenames ===
correlation_folder = "intra_correlation_matrices"
output_csv = "Global_brain_measures.csv"
local_output_csv = "Local_strengths.csv"

# === Global Graph Metrics Calculation ===
all_files = [f for f in os.listdir(correlation_folder) if f.endswith(".csv")]
results = []

for filename in all_files:
    try:
        # Extract metadata from filename
        parts = filename.replace("correlation_", "").replace(".csv", "").split("_")
        dyad, condition, role = parts[0], parts[1], parts[2]

        # Load correlation matrix
        df = pd.read_csv(os.path.join(correlation_folder, filename))
        corr_matrix = df.values

        # Thresholding to create binary adjacency matrix (|r| ≥ 0.3)
        adj_matrix = (np.abs(corr_matrix) >= 0.3).astype(int)
        G = nx.from_numpy_array(adj_matrix)

        # Global graph metrics
        degrees = dict(G.degree()).values()
        degree_mean = np.mean(list(degrees)) if degrees else np.nan

        clustering = nx.clustering(G)
        clustering_mean = np.mean(list(clustering.values())) if clustering else np.nan

        try:
            efficiency = nx.global_efficiency(G)
        except:
            efficiency = np.nan

        try:
            if G.number_of_edges() > 0:
                partition = community_louvain.best_partition(G)
                modularity = community_louvain.modularity(partition, G)
            else:
                modularity = np.nan
        except:
            modularity = np.nan

        try:
            path_length = nx.average_shortest_path_length(G)
            smallworldness = clustering_mean / path_length if path_length > 0 else np.nan
        except:
            smallworldness = np.nan

        # Append results
        results.append({
            "Dyad": dyad,
            "Condition": condition,
            "Role": role,
            "Mean Degree": round(degree_mean, 3),
            "Mean Clustering Coefficient": round(clustering_mean, 3),
            "Global Efficiency": round(efficiency, 3),
            "Modularity": round(modularity, 3),
            "Small-Worldness": round(smallworldness, 3)
        })

        print(f"✅ Done (global): {filename}")

    except Exception as e:
        print(f"❌ Error (global) in {filename}: {str(e)}")

# Save global metrics as CSV
summary_df = pd.DataFrame(results)
summary_df = summary_df.sort_values(by=["Dyad", "Role"])
summary_df.to_csv(output_csv, index=False)

# Generate HTML report for global graph metrics
html_global = "Global_brain_measures_report.html"
with open(html_global, "w", encoding="utf-8") as f:
    f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Intra-Brain Graph Measures</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; background-color: #f9f9f9; }}
        h1 {{ text-align: center; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; text-align: center; }}
        th {{ background-color: #f0f0f0; }}
        tr:nth-child(even) {{ background-color: #fbfbfb; }}
    </style>
</head>
<body>
    <h1>Intra-Brain Graph Measures (Global)</h1>
    <table>
        <tr>{''.join(f'<th>{col}</th>' for col in summary_df.columns)}</tr>
        {''.join('<tr>' + ''.join(f'<td>{val}</td>' for val in row) + '</tr>' for row in summary_df.values)}
    </table>
</body>
</html>""")
print("📄 Saved HTML report (global) to:", html_global)

# =======================================
# Part 2: Local Node Strength Calculation
# =======================================

local_results = []

for filename in all_files:
    try:
        # Extract metadata from filename
        parts = filename.replace("correlation_", "").replace(".csv", "").split("_")
        dyad, condition, role = parts[0], parts[1], parts[2]

        # Load correlation matrix
        df = pd.read_csv(os.path.join(correlation_folder, filename))
        corr_matrix = df.values

        # Compute node strength: sum of absolute correlations per node
        strength_per_node = np.sum(np.abs(corr_matrix), axis=1)

        for node_index, strength in enumerate(strength_per_node):
            local_results.append({
                "Dyad": dyad,
                "Condition": condition,
                "Role": role,
                "Node": f"S{node_index+1}",
                "Strength": round(strength, 3)
            })

        print(f"✅ Done (local): {filename}")

    except Exception as e:
        print(f"❌ Error (local) in {filename}: {str(e)}")

# Save local strengths as CSV
df_local = pd.DataFrame(local_results)
df_local.to_csv(local_output_csv, index=False)

# Generate HTML report for local strengths
html_local = "local_brain_measures_report.html"
with open(html_local, "w", encoding="utf-8") as f:
    f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Local Brain Node Strengths</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; background-color: #f0f8ff; }}
        h1 {{ text-align: center; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; text-align: center; }}
        th {{ background-color: #4a90e2; color: white; }}
        tr:nth-child(even) {{ background-color: #eef4fc; }}
    </style>
</head>
<body>
    <h1>Local Brain Graph Measures (Node Strengths)</h1>
    <table>
        <tr>{''.join(f'<th>{col}</th>' for col in df_local.columns)}</tr>
        {''.join('<tr>' + ''.join(f'<td>{val}</td>' for val in row) + '</tr>' for row in df_local.values)}
    </table>
</body>
</html>""")
print("📄 Saved HTML report (local) to:", html_local)
