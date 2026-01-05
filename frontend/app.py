import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx

BACKEND_URL = "http://backend:8000"

st.title("📦 WareGraph – Warehouse Slotting Optimizer")

# Fetch data
before = requests.get(f"{BACKEND_URL}/generate-data").json()
after = requests.get(f"{BACKEND_URL}/optimize").json()

df_before = pd.DataFrame.from_dict(
    before["layout"], orient="index", columns=["Bin"]
)
df_before["Heat"] = df_before.index.map(before["heat"])

df_after = pd.DataFrame.from_dict(
    after["layout"], orient="index", columns=["Bin"]
)
df_after["Heat"] = df_after.index.map(after["heat"])

# Heatmaps
st.subheader("📊 Warehouse Layout Heatmaps")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.heatmap(
    df_before.sort_values("Bin")[["Heat"]].T,
    ax=axes[0],
    cmap="Reds",
    cbar=False
)
axes[0].set_title("Before Optimization (Random)")

sns.heatmap(
    df_after.sort_values("Bin")[["Heat"]].T,
    ax=axes[1],
    cmap="Greens",
    cbar=False
)
axes[1].set_title("After Optimization (Clustered)")

st.pyplot(fig)

# Graph visualization
st.subheader("🔗 Strongest Product Relationships")

G = nx.Graph()
for e in after["top_edges"]:
    G.add_edge(e["source"], e["target"], weight=e["weight"])

pos = nx.spring_layout(G, seed=42)

plt.figure(figsize=(8, 6))
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="lightblue",
    node_size=1500,
    font_size=8,
)
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

st.pyplot(plt)
