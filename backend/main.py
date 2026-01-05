from fastapi import FastAPI
from simulation import run_simulation

app = FastAPI(title="WareGraph API")

cached_data = run_simulation()


@app.get("/generate-data")
def generate_data():
    """
    Returns baseline (random) warehouse layout.
    """
    return {
        "layout": cached_data["random_layout"],
        "heat": cached_data["heat"],
    }


@app.get("/optimize")
def optimize():
    """
    Returns optimized layout + strongest product relationships.
    """
    return {
        "layout": cached_data["optimized_layout"],
        "heat": cached_data["heat"],
        "top_edges": cached_data["top_edges"],
    }
