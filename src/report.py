import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

def main(results_dir="results"):
    r = Path(results_dir)
    tool = pd.read_csv(r / "tool_buy.csv")
    summary = pd.read_csv(r / "solution_summary.csv")

    charts = r / "charts"
    charts.mkdir(parents=True, exist_ok=True)

    # Tool purchases
    plt.figure()
    plt.bar(tool["tool_type"], tool["buy_qty"])
    plt.title("Recommended Tool Purchases (qty)")
    plt.xlabel("Tool Type")
    plt.ylabel("Buy Quantity")
    plt.tight_layout()
    plt.savefig(charts / "tool_purchases.png", dpi=200)
    plt.close()

    # Cost breakdown
    capex = float(summary["capex_total_k"].iloc[0])
    shortage = float(summary["shortage_total_k"].iloc[0])

    plt.figure()
    plt.bar(["CapEx", "Shortage Penalty"], [capex, shortage])
    plt.title("Objective Cost Breakdown (k$)")
    plt.ylabel("Cost (k$)")
    plt.tight_layout()
    plt.savefig(charts / "cost_breakdown.png", dpi=200)
    plt.close()

    print("Charts saved to:", charts.resolve())

if __name__ == "__main__":
    main()
