import random
import pandas as pd
from pathlib import Path

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

def main(out_dir: str = "data"):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    products = [f"P{i}" for i in range(1, 9)]   # 8 products
    steps = [f"S{i}" for i in range(1, 7)]      # 6 process steps
    tool_types = [f"T{i}" for i in range(1, 6)] # 5 tool types

    # products.csv
    prod_rows = []
    for p in products:
        demand = random.randint(80, 200)
        penalty = random.choice([80, 120, 160])  # shortage penalty per unit (toy)
        prod_rows.append((p, demand, penalty))
    pd.DataFrame(prod_rows, columns=["product_id", "demand", "penalty_per_unit"]).to_csv(out / "products.csv", index=False)

    # steps.csv
    pd.DataFrame([(s, i+1) for i, s in enumerate(steps)], columns=["step_id", "sequence"]).to_csv(out / "steps.csv", index=False)

    # tool_types.csv
    tool_rows = []
    for t in tool_types:
        capex = random.choice([400, 600, 800, 1000, 1200])  # in k$ (toy)
        cap_hours = random.choice([800, 1000, 1200, 1400])  # hours per period
        max_buy = random.choice([2, 3, 4])
        tool_rows.append((t, capex, cap_hours, max_buy))
    pd.DataFrame(tool_rows, columns=["tool_type", "capex_cost_k", "cap_hours_per_period", "max_buy"]).to_csv(out / "tool_types.csv", index=False)

    # routes.csv: eligibility + process times
    route_rows = []
    for p in products:
        for s in steps:
            eligible = random.sample(tool_types, k=random.choice([2, 3]))
            for t in eligible:
                pt = round(random.uniform(0.8, 2.2), 2)  # hours per unit
                route_rows.append((p, s, t, pt))
    pd.DataFrame(route_rows, columns=["product_id", "step_id", "tool_type", "process_time_hours_per_unit"]).to_csv(out / "routes.csv", index=False)

    print(f"Wrote synthetic data to: {out.resolve()}")
    for f in sorted(out.glob("*.csv")):
        print(" -", f.name)

if __name__ == "__main__":
    main()
