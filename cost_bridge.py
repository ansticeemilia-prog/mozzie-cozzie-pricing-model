"""
cost_bridge.py

Estimates implied unit economics for each product in the competitor set,
using a simple cost-to-price bridge:

    retail_price = (fabric_cost + labour_cost + treatment_cost + overhead) x (1 + margin)

Since we don't have competitors' actual cost data (it's private), this
model works backwards: it uses PUBLIC/RESEARCHED cost assumptions (fabric
cost per gram, labour cost by manufacturing country, treatment cost) to
estimate a plausible implied margin for each brand. This is the same logic
consultants use for "reverse-engineered" competitor cost structures when
they don't have access to real financials.

IMPORTANT: The assumptions below are illustrative placeholders. Replace
them with figures from your own research (e.g. TENCEL supplier pricing,
UK vs. Bangladesh/Vietnam/China labour cost benchmarks, permethrin
treatment cost per unit) to make this defensible.
"""

import pandas as pd

# --- Cost assumptions (GBP) — REPLACE WITH YOUR RESEARCHED FIGURES ---

FABRIC_COST_PER_GRAM = {
    "TENCEL": 0.045,              # premium sustainable fabric
    "Nylon/Cotton blend": 0.020,
    "Polyester": 0.012,
    "Polyester blend": 0.014,
    "Nylon": 0.018,
    "Recycled polyester": 0.022,
    "Recycled nylon": 0.020,
    "Recycled polyester blend": 0.021,  # recycled inputs carry a cost premium
}

LABOUR_COST_BY_COUNTRY = {
    "UK": 8.50,          # per unit, reflecting higher UK manufacturing wages
    "Bangladesh": 1.20,
    "Vietnam": 1.80,
    "China": 1.50,
}

TREATMENT_COST = {
    "permethrin_biobased": 3.50,  # bio-based treatment premium
    "permethrin": 2.00,
    "none": 0.00,
}

CONSTRUCTION_COMPLEXITY_COST = {
    "air_gap_design": 5.00,   # extra pattern/sewing cost for Mozzie Cozzie's structural protection — estimate
    "dense_weave": 2.50,      # Páramo's dense-weave fabric — less construction complexity than Air-Gap, estimate
}

OVERHEAD_FLAT = 4.00  # packaging, logistics, QA allowance per unit


def compute_cost_bridge(df: pd.DataFrame) -> pd.DataFrame:
    """Add estimated cost components and implied margin to the dataframe."""
    df = df.copy()

    df["fabric_cost"] = df.apply(
        lambda r: r["weight_g"] * FABRIC_COST_PER_GRAM.get(r["fabric_type"], 0.015),
        axis=1,
    )
    df["labour_cost"] = df["country_of_manufacture"].map(LABOUR_COST_BY_COUNTRY).fillna(2.00)
    df["treatment_cost"] = df["insect_repellent_treatment"].map(TREATMENT_COST).fillna(0.00)
    df["overhead_cost"] = OVERHEAD_FLAT
    df["construction_cost"] = df["construction_type"].map(CONSTRUCTION_COMPLEXITY_COST).fillna(0.00)

    df["estimated_unit_cost"] = (
        df["fabric_cost"] + df["labour_cost"] + df["treatment_cost"] + df["overhead_cost"] + df["construction_cost"]
    )

    df["implied_margin_pct"] = (
        (df["price_gbp"] - df["estimated_unit_cost"]) / df["price_gbp"] * 100
    ).round(1)

    df["implied_margin_gbp"] = (df["price_gbp"] - df["estimated_unit_cost"]).round(2)

    return df


if __name__ == "__main__":
    data = pd.read_csv("../data/competitor_pricing.csv")
    result = compute_cost_bridge(data)
    print(result[["brand", "product", "price_gbp", "estimated_unit_cost", "implied_margin_pct"]])
