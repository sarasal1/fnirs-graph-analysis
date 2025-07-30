"""
Script Name: intra_brain_connectivity.py
Description:
This script processes pre-cleaned fNIRS time-series data (18 channels per participant)
to compute intra-brain correlation matrices for each individual (baby or parent) in each dyad and condition.
It applies a statistical threshold (p-value and correlation strength) to retain only meaningful connections.

The script then:
1. Saves a thresholded correlation matrix (.csv) per recording.
2. Converts the correlation matrix into a binary adjacency matrix.
3. Constructs a graph using NetworkX from the adjacency matrix.
4. Visualizes the intra-brain graph and saves it as a .png image.

Input:
- Folder: "csv_cleaned/"
  Each file should be named: dyad<id>_<condition>_<role>.csv
  Each file must contain 18 time-series columns (channels).

Output:
- Folder: "intra_correlation_matrices/"
    → correlation_dyad<id>_<condition>_<role>.csv
- Folder: "intra_brain_graphs/"
    → correlation_dyad<id>_<condition>_<role>.png

Parameters:
- threshold = 0.3         # Minimum correlation magnitude (|r|) to retain
- p_cutoff = 0.05         # Maximum p-value for significance

Dependencies:
- numpy, pandas, matplotlib, networkx, scipy.stats, re, os
"""
import os
import pandas as pd
import numpy as np
import networkx as nx
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import re
# === Folder Paths ===
input_folder = "csv_cleaned"
correlation_folder = "intra_correlation_matrices"
graph_folder = "intra_brain_graphs"

# Create output folders if they don't exist
os.makedirs(correlation_folder, exist_ok=True)
os.makedirs(graph_folder, exist_ok=True)

# === Thresholding Parameters ===
threshold = 0.3       # Minimum absolute correlation value to consider
p_cutoff = 0.05       # Maximum p-value to consider the correlation statistically significant

# === Collect all valid CSV files ===
all_files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]

for filename in all_files:
    # Check filename pattern: dyadID_condition_role.csv
    match = re.match(r"dyad(\d+)_([a-zA-Z]+)_([a-zA-Z]+)\.csv", filename)
    if not match:
        print(f"❌ Skipping file (bad name): {filename}")
        continue

    # Extract metadata from filename
    dyad_id, condition, role = match.groups()
    condition = condition.lower()
    role = role.lower()

    # Load time-series data
    path = os.path.join(input_folder, filename)
    df = pd.read_csv(path)

    # Validate expected number of channels (18)
    if df.shape[1] != 18:
        print(f"⚠️ Skipping {filename}: wrong shape")
        continue

    # === Compute Intra-Brain Correlation Matrix ===
    corr_matrix = np.zeros((18, 18))
    for i in range(18):
        for j in range(18):
            r, p = pearsonr(df.iloc[:, i], df.iloc[:, j])
            # Keep correlation only if statistically significant and strong enough
            if p <= p_cutoff and abs(r) >= threshold:
                corr_matrix[i, j] = r
            else:
                corr_matrix[i, j] = 0

    # === Save Correlation Matrix as CSV ===
    corr_filename = f"correlation_dyad{dyad_id}_{condition}_{role}.csv"
    corr_path = os.path.join(correlation_folder, corr_filename)
    pd.DataFrame(corr_matrix).to_csv(corr_path, index=False)

    # === Create Binary Adjacency Matrix for Graph Construction ===
    adj_matrix = (np.abs(corr_matrix) >= threshold).astype(int)
    G = nx.from_numpy_array(adj_matrix)

    # === Plot Graph ===
    plt.figure(figsize=(8, 8))
    pos = nx.spring_layout(G, seed=42, k=0.7)
    nx.draw(
        G, pos, with_labels=True,
        node_color="skyblue" if role == "baby" else "lightpink",
        node_size=600, font_size=8,
        edge_color='gray', width=1.5, alpha=0.9
    )
    plt.title(f"Intra-Brain Graph - dyad{dyad_id} {condition} {role}")

    # Save graph figure
    graph_path = os.path.join(graph_folder, corr_filename.replace(".csv", ".png"))
    plt.savefig(graph_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✅ Saved: {corr_filename} + graph")
