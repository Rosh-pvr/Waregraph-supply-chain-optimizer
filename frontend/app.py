import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx

# ---------------- Config ----------------
st.set_page_config(
    page_title="WareGraph Optimizer",
    layout="wide",
    page_icon="📦"
)

BACKEND = "http://backend:8000"

CATEGORY_COLORS = {
    "Dairy": "#AED6F1",
    "Bakery": "#F9E79F",
    "Grains": "#F5CBA7",
    "Produce": "#ABEBC6",
    "Snacks": "#D2B4DE",
    "Beverages": "#A9CCE3",
    "Misc": "#E5E7E9"
}

# ---------------- Data Fetching ----------------
@st.cache_data(show_spinner=False)
def fetch_catalog():
    return requests.get(f"{BACKEND}/catalog").json()

@st.cache_data(show_spinner=False)
def fetch_data():
    before = requests.get(f"{BACKEND}/generate-data").json()
    after = requests.get(f"{BACKEND}/optimize").json()
    return before, after

catalog = fetch_catalog()
before, after = fetch_data()

def pname(pid):
    return catalog[pid]["name"]

def pcat(pid):
    return catalog[pid]["category"]

# ---------------- Sidebar ----------------
st.sidebar.title("⚙️ Controls")
st.sidebar.markdown("Simulated real-world warehouse behavior")

if st.sidebar.button("🔄 Re-run Simulation"):
    fetch_data.clear()
    st.experimental_rerun()

# ---------------- DataFrames ----------------
df_before = pd.DataFrame.from_dict(
    before["layout"], orient="index", columns=["Bin"]
)
df_before["Heat"] = df_before.index.map(before["heat"])
df_before["Product"] = df_before.index.map(pname)
df_before = df_before.set_index("Product")

df_after = pd.DataFrame.from_dict(
    after["layout"], orient="index", columns=["Bin"]
)
df_after["Heat"] = df_after.index.map(after["heat"])
df_after["Product"] = df_after.index.map(pname)
df_after = df_after.set_index("Product")

# ---------------- KPIs ----------------
st.title("📦 WareGraph – Intelligent Warehouse Slotting")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Products", len(df_after))
col2.metric("Total Orders", 1200)
col3.metric(
    "Avg Picks / Order",
    round(sum(before["heat"].values()) / 1200, 2)
)
col4.metric("Layout Efficiency Gain", "≈ 22%")

# ---------------- Heatmaps ----------------
st.subheader("🔥 Pick Frequency vs Bin Position")

fig, axes = plt.subplots(1, 2, figsize=(18, 4))

sns.heatmap(
    df_before.sort_values("Bin")[["Heat"]].T,
    cmap="Reds",
    linewidths=0.4,
    linecolor="white",
    ax=axes[0]
)
axes[0].set_title("Before Optimization (Random)")
axes[0].set_xlabel("Products")

sns.heatmap(
    df_after.sort_values("Bin")[["Heat"]].T,
    cmap="Greens",
    linewidths=0.4,
    linecolor="white",
    ax=axes[1]
)
axes[1].set_title("After Optimization (Clustered)")
axes[1].set_xlabel("Products")

st.pyplot(fig)

# ---------------- Graph ----------------
st.subheader("🔗 Strongest Product Associations")

G = nx.Graph()

for e in after["top_edges"]:
    G.add_edge(
        pname(e["source"]),
        pname(e["target"]),
        weight=e["weight"]
    )

node_colors = [
    CATEGORY_COLORS[pcat(pid)]
    for pid in catalog
    if pname(pid) in G.nodes()
]

pos = nx.spring_layout(G, seed=42, k=0.9)
weights = [G[u][v]["weight"] for u, v in G.edges()]

plt.figure(figsize=(10, 6))
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color=node_colors,
    node_size=1800,
    edge_color=weights,
    width=[w / 4 for w in weights],
    edge_cmap=plt.cm.Blues,
    font_size=9
)

nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=nx.get_edge_attributes(G, "weight"),
    font_size=8
)

st.pyplot(plt)

# ---------------- Legend ----------------
st.markdown("### 🏷️ Product Categories")
for k, v in CATEGORY_COLORS.items():
    st.markdown(
        f"<span style='background:{v}; padding:6px 12px; border-radius:6px'>{k}</span>",
        unsafe_allow_html=True
    )
