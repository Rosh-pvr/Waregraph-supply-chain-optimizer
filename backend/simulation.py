"""
simulation.py

This module simulates warehouse order data and applies
Graph Theory-based slotting optimization.

Graph Interpretation:
- Nodes = Products
- Edge weight = Number of times two products appear together in orders
- Communities = Product groups frequently ordered together
"""

import random
import numpy as np
import networkx as nx
from sklearn.cluster import SpectralClustering


NUM_PRODUCTS = 50
NUM_ORDERS = 1000


def generate_products():
    return [f"Product_{i+1}" for i in range(NUM_PRODUCTS)]


def generate_orders(products):
    """
    Generate synthetic orders.
    Each order randomly contains 2–6 products.
    """
    orders = []
    for _ in range(NUM_ORDERS):
        order_size = random.randint(2, 6)
        orders.append(random.sample(products, order_size))
    return orders


def build_cooccurrence_graph(products, orders):
    """
    Build a weighted graph where:
    - Nodes = products
    - Edge weight = co-occurrence frequency
    """
    G = nx.Graph()
    G.add_nodes_from(products)

    for order in orders:
        for i in range(len(order)):
            for j in range(i + 1, len(order)):
                u, v = order[i], order[j]
                if G.has_edge(u, v):
                    G[u][v]["weight"] += 1
                else:
                    G.add_edge(u, v, weight=1)

    return G


def product_heat(orders):
    """
    Heat = how frequently a product is ordered.
    """
    heat = {}
    for order in orders:
        for item in order:
            heat[item] = heat.get(item, 0) + 1
    return heat


def random_layout(products):
    """
    Baseline layout: random bin assignment.
    """
    shuffled = products[:]
    random.shuffle(shuffled)
    return {p: i + 1 for i, p in enumerate(shuffled)}


def optimize_slotting(G, heat):
    """
    Slotting Optimization using Spectral Clustering.

    WHY GRAPH THEORY?
    -----------------
    - Products ordered together form dense subgraphs
    - Spectral clustering finds these communities
    - Communities are placed closer together in bins
    """

    products = list(G.nodes())
    index = {p: i for i, p in enumerate(products)}

    # Adjacency matrix weighted by co-occurrence
    adj = nx.to_numpy_array(G, nodelist=products, weight="weight")

    # Spectral clustering finds communities in the graph
    clustering = SpectralClustering(
        n_clusters=10,
        affinity="precomputed",
        random_state=42,
    )
    labels = clustering.fit_predict(adj)

    clusters = {}
    for product, label in zip(products, labels):
        clusters.setdefault(label, []).append(product)

    # Sort clusters internally by product heat
    final_order = []
    for cluster_products in clusters.values():
        cluster_products.sort(key=lambda p: heat[p], reverse=True)
        final_order.extend(cluster_products)

    # Assign bins 1–50
    return {p: i + 1 for i, p in enumerate(final_order)}


def top_edges(G, top_n=10):
    """
    Return top-N strongest product relationships.
    """
    edges = sorted(
        G.edges(data=True),
        key=lambda x: x[2]["weight"],
        reverse=True
    )
    return [
        {"source": u, "target": v, "weight": d["weight"]}
        for u, v, d in edges[:top_n]
    ]


def run_simulation():
    products = generate_products()
    orders = generate_orders(products)

    G = build_cooccurrence_graph(products, orders)
    heat = product_heat(orders)

    return {
        "products": products,
        "heat": heat,
        "graph": G,
        "random_layout": random_layout(products),
        "optimized_layout": optimize_slotting(G, heat),
        "top_edges": top_edges(G),
    }
