import random
import numpy as np
import networkx as nx
from sklearn.cluster import SpectralClustering

CATEGORIES = {
    "Dairy": ["Milk", "Bread", "Butter", "Cheese", "Yogurt"],
    "Grains": ["Rice", "Wheat", "Lentils", "Pasta", "Flour"],
    "Produce": ["Apple", "Banana", "Tomato", "Onion", "Potato"],
    "Snacks": ["Chips", "Biscuits", "Chocolate", "Namkeen", "Cookies"],
    "Beverages": ["Soda", "Juice", "Water", "Tea", "Coffee"]
}

NUM_ORDERS = 1200


def generate_products():
    products = []
    for items in CATEGORIES.values():
        products.extend(items)
    return products


def generate_orders(products):
    """
    Realistic order simulation:
    - Category-dominant baskets
    - Zipfian popularity
    """
    popularity = np.random.zipf(1.6, len(products))
    popularity = popularity / popularity.sum()

    orders = []

    for _ in range(NUM_ORDERS):
        category = random.choice(list(CATEGORIES.keys()))
        base_items = random.sample(CATEGORIES[category], k=2)

        cross_items = np.random.choice(
            products,
            size=random.randint(1, 2),
            replace=False,
            p=popularity
        ).tolist()

        orders.append(list(set(base_items + cross_items)))

    return orders
