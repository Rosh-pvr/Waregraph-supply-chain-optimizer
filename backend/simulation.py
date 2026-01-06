import random
import numpy as np
import networkx as nx
from sklearn.cluster import 



# ---------- Product Master (Realistic SKU Catalog) ----------

PRODUCT_CATALOG = {
    "P001": {"name": "Milk", "category": "Dairy"},
    "P002": {"name": "Bread", "category": "Bakery"},
    "P003": {"name": "Butter", "category": "Dairy"},
    "P004": {"name": "Cheese", "category": "Dairy"},
    "P005": {"name": "Rice", "category": "Grains"},
    "P006": {"name": "Lentils", "category": "Grains"},
    "P007": {"name": "Oil", "category": "Grains"},
    "P008": {"name": "Apple", "category": "Produce"},
    "P009": {"name": "Banana", "category": "Produce"},
    "P010": {"name": "Tomato", "category": "Produce"},
    "P011": {"name": "Chips", "category": "Snacks"},
    "P012": {"name": "Biscuits", "category": "Snacks"},
    "P013": {"name": "Chocolate", "category": "Snacks"},
    "P014": {"name": "Soda", "category": "Beverages"},
    "P015": {"name": "Juice", "category": "Beverages"},
}

# pad to 50 products if needed
while len(PRODUCT_CATALOG) < 50:
    pid = f"P{len(PRODUCT_CATALOG)+1:03d}"
    PRODUCT_CATALOG[pid] = {
        "name": f"Item_{pid}",
        "category": "Misc"
    }


CATEGORIES = {
    "Dairy": ["Milk", "Bread", "Butter", "Cheese", "Yogurt"],
    "Grains": ["Rice", "Wheat", "Lentils", "Pasta", "Flour"],
    "Produce": ["Apple", "Banana", "Tomato", "Onion", "Potato"],
    "Snacks": ["Chips", "Biscuits", "Chocolate", "Namkeen", "Cookies"],
    "Beverages": ["Soda", "Juice", "Water", "Tea", "Coffee"]
}

NUM_ORDERS = 1200


def generate_products():
    return list(PRODUCT_CATALOG.keys())

def product_name(pid):
    return PRODUCT_CATALOG[pid]["name"]

def product_category(pid):
    return PRODUCT_CATALOG[pid]["category"]



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
