"""
pricing_analysis.py

Main analysis for the Mozzie Cozzie pricing & positioning model.

Produces three outputs (saved to ../outputs/):
  1. cost_bridge_table.csv      - implied cost structure & margin per competitor
  2. positioning_map.png        - price vs. UPF rating, sized by weight (proxy for build quality)
  3. price_scenario_chart.png   - what happens to Mozzie Cozzie's margin & relative
                                  position under +/-10% and +/-15% price moves

Run from inside the scripts/ folder: python pricing_analysis.py
"""

import pandas as pd
import matplotlib.pyplot as plt
from cost_bridge import compute_cost_bridge

DATA_PATH = "../data/competitor_pricing.csv"
OUT_DIR = "../outputs"

FOCUS_BRAND = "Mozzie Cozzie"
FOCUS_PRODUCT = "Jumpsuit Bundle"

def load_and_process():
    df = pd.read_csv(DATA_PATH)
    df = compute_cost_bridge(df)
    return df


def save_cost_bridge_table(df: pd.DataFrame):
    cols = [
        "brand", "product", "segment", "price_gbp", "estimated_unit_cost",
        "implied_margin_gbp", "implied_margin_pct",
    ]
    df[cols].sort_values("implied_margin_pct", ascending=False).to_csv(
        f"{OUT_DIR}/cost_bridge_table.csv", index=False
    )


def plot_positioning_map(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 6))
    chart_df = df[~((df["brand"] == FOCUS_BRAND) & (df["product"] == FOCUS_PRODUCT))]
    segments = chart_df["segment"].unique()
    colors = {"sustainable_niche": "#2E7D32", "performance_niche": "#1565C0", "mass_market": "#9E9E9E"}

    for seg in segments:
        sub = chart_df[chart_df["segment"] == seg]
        ax.scatter(
            sub["upf_rating"], sub["price_gbp"],
            s=sub["weight_g"] * 2, alpha=0.6,
            c=colors.get(seg, "#666666"), label=seg, edgecolors="black", linewidths=0.5,
        )

    for _, row in chart_df.iterrows():
        ax.annotate(row["brand"], (row["upf_rating"], row["price_gbp"]),
                    fontsize=8, xytext=(5, 5), textcoords="offset points")

    ax.set_xlabel("UPF Rating (sun/insect protection)")
    ax.set_ylabel("Retail Price (GBP)")
    ax.set_title("Market Positioning: Price vs. Protection Rating\n(bubble size = fabric weight, a proxy for build/durability)")
    ax.legend(title="Segment")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}/positioning_map.png", dpi=150)
    plt.close(fig)


def run_price_scenarios(df: pd.DataFrame):
    focus = df[(df["brand"] == FOCUS_BRAND) & (df["product"] == FOCUS_PRODUCT)].iloc[0]
    base_price = focus["price_gbp"]
    unit_cost = focus["estimated_unit_cost"]

    scenarios = [-15, -10, 0, 10, 15]
    rows = []
    for pct in scenarios:
        new_price = base_price * (1 + pct / 100)
        margin_gbp = new_price - unit_cost
        margin_pct = margin_gbp / new_price * 100
        # naive competitive rank: how many competitors would Mozzie Cozzie now be more expensive than
        n_cheaper_than = (df["price_gbp"] < new_price).sum()
        rows.append({
            "price_change_pct": pct,
            "new_price_gbp": round(new_price, 2),
            "margin_gbp": round(margin_gbp, 2),
            "margin_pct": round(margin_pct, 1),
            "n_competitors_undercut": int(n_cheaper_than),
        })

    scenario_df = pd.DataFrame(rows)
    scenario_df.to_csv(f"{OUT_DIR}/price_scenarios.csv", index=False)

    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax1.bar(scenario_df["price_change_pct"].astype(str) + "%", scenario_df["margin_pct"],
            color="#2E7D32", alpha=0.8, label="Margin %")
    ax1.set_xlabel("Price Change Scenario")
    ax1.set_ylabel("Implied Margin (%)", color="#2E7D32")
    ax1.set_title(f"{FOCUS_BRAND} {FOCUS_PRODUCT}: Margin Sensitivity to Price Changes")

    ax2 = ax1.twinx()
    ax2.plot(scenario_df["price_change_pct"].astype(str) + "%", scenario_df["n_competitors_undercut"],
              color="#C62828", marker="o", label="Competitors undercut")
    ax2.set_ylabel("Number of competitors priced below", color="#C62828")

    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}/price_scenario_chart.png", dpi=150)
    plt.close(fig)

    return scenario_df


if __name__ == "__main__":
    df = load_and_process()
    save_cost_bridge_table(df)
    plot_positioning_map(df)
    scenario_df = run_price_scenarios(df)
    print("Cost bridge (sorted by implied margin %):\n")
    print(df[["brand", "product", "price_gbp", "estimated_unit_cost", "implied_margin_pct"]]
          .sort_values("implied_margin_pct", ascending=False).to_string(index=False))
    print("\nPrice scenarios for Mozzie Cozzie Jumpsuit Bundle:\n")
    print(scenario_df.to_string(index=False))
    print("\nSaved: cost_bridge_table.csv, positioning_map.png, price_scenario_chart.png, price_scenarios.csv")
