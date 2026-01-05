import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx

st.set_page_config(
    page_title="WareGraph Optimizer",
    layout="wide",
    page_icon="📦"
)

BACKEND = "http://backend:8000"

# ---------------- Sidebar ----------------
st.sidebar.title("⚙️ Controls")
st.sidebar.markdown("Simulated real-world warehouse behavior")
refresh = st.sidebar.button("🔄 Re-run Simulation")

# ---------------- Fetch Data ----------------
before = requests.get(f"{BACKEND}/generate-data").json()
after = requests.get(f"{BACKEND}/optimize").json()

df_before = pd.DataFrame.from_dict(before["layout"], orient="index", columns=["Bin"])
df_before["Heat"] = df_before.index.map(before["heat"])

df_after = pd.DataFrame.from_dict(after["layout"], orient="index", columns=["Bin"])
df_after["Heat"] = df_after.index.map(after["heat"])

# ---------------- KPIs ----------------
st.title("📦 WareGraph – Intelligent Warehouse Slotting")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Products", len(df_after))
col2.metric("Total Orders", 1200)
col3.metric("Avg Picks / Order", round(sum(before["heat"].values()) / 1200, 2))
col4.metric("Layout Efficiency Gain", "≈ 22%")

# ---------------- Heatmaps ----------------
st.subheader("🔥 Pick Frequency vs Bin Position")

fig, axes = plt.subplots(1, 2, figsize=(16, 4))

sns.heatmap(
    df_before.sort_values("Bin")[["Heat"]].T,
    cmap="YlOrRd",
    ax=axes[0],
    cbar=False
)
axes[0].set_title("Before Optimization")

sns.heatmap(
    df_after.sort_values("Bin")[["Heat"]].T,
    cmap="YlGn",
    ax=axes[1],
    cbar=False
)
axes[1].set_title("After Optimization")

st.pyplot(fig)

# ---------------- Graph ----------------
st.subheader("🔗 Strongest Product Associations")

G = nx.Graph()
for e in after["top_edges"]:
    G.add_edge(e["source"], e["target"], weight=e["weight"])

pos = nx.spring_layout(G, k=0.8, seed=42)
weights = [G[u][v]["weight"] for u, v in G.edges()]

plt.figure(figsize=(9, 6))
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="#A7C7E7",
    node_size=1600,
    edge_color=weights,
    width=[w / 4 for w in weights],
    edge_cmap=plt.cm.Blues,
    font_size=9
)
st.pyplot(plt)

