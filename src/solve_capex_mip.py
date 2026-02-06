from __future__ import annotations
import pandas as pd
import pulp as pl
from pathlib import Path

def load_data(data_dir: str = "data"):
    d = Path(data_dir)
    products = pd.read_csv(d / "products.csv")
    steps = pd.read_csv(d / "steps.csv").sort_values("sequence")
    tools = pd.read_csv(d / "tool_types.csv")
    routes = pd.read_csv(d / "routes.csv")

    P = products["product_id"].tolist()
    S = steps["step_id"].tolist()
    T = tools["tool_type"].tolist()

    demand = dict(zip(products["product_id"], products["demand"]))
    penalty = dict(zip(products["product_id"], products["penalty_per_unit"]))
    capex = dict(zip(tools["tool_type"], tools["capex_cost_k"]))
    cap_hours = dict(zip(tools["tool_type"], tools["cap_hours_per_period"]))
    max_buy = dict(zip(tools["tool_type"], tools["max_buy"]))

    pt = {(r.product_id, r.step_id, r.tool_type): float(r.process_time_hours_per_unit) for r in routes.itertuples()}
    elig = {(p, s): [] for p in P for s in S}
    for (p, s, t), _ in pt.items():
        elig[(p, s)].append(t)

    return P, S, T, demand, penalty, capex, cap_hours, max_buy, pt, elig

def solve(data_dir: str = "data", results_dir: str = "results"):
    P, S, T, demand, penalty, capex, cap_hours, max_buy, pt, elig = load_data(data_dir)

    # Decision vars
    y = {t: pl.LpVariable(f"buy_{t}", lowBound=0, upBound=int(max_buy[t]), cat="Integer") for t in T}
    x = {(p, s, t): pl.LpVariable(f"x_{p}_{s}_{t}", lowBound=0)
         for p in P for s in S for t in elig[(p, s)]}
    u = {p: pl.LpVariable(f"short_{p}", lowBound=0) for p in P}
    produced = {p: pl.LpVariable(f"produced_{p}", lowBound=0) for p in P}

    model = pl.LpProblem("fab_capex_capacity_flow", pl.LpMinimize)

    # Objective
    model += pl.lpSum(capex[t] * y[t] for t in T) + pl.lpSum(penalty[p] * u[p] for p in P)

    # Flow constraints: same qty through each step
    for p in P:
        for s in S:
            model += pl.lpSum(x[(p, s, t)] for t in elig[(p, s)]) == produced[p], f"flow_{p}_{s}"
        model += produced[p] + u[p] == demand[p], f"demand_{p}"

    # Capacity constraints per tool type
    for t in T:
        model += pl.lpSum(pt[(p, s, t)] * x[(p, s, t)]
                         for p in P for s in S if (p, s, t) in pt) <= cap_hours[t] * y[t], f"cap_{t}"

    status = model.solve(pl.PULP_CBC_CMD(msg=False))

    res_dir = Path(results_dir)
    res_dir.mkdir(parents=True, exist_ok=True)

    tool_buy = pd.DataFrame([{
        "tool_type": t,
        "buy_qty": float(pl.value(y[t])),
        "capex_cost_k": capex[t],
        "cap_hours_per_period": cap_hours[t],
        "capex_spend_k": float(pl.value(y[t])) * capex[t],
    } for t in T])

    prod = pd.DataFrame([{
        "product_id": p,
        "demand": demand[p],
        "produced": float(pl.value(produced[p])),
        "shortage": float(pl.value(u[p])),
        "penalty_per_unit": penalty[p],
        "shortage_cost": float(pl.value(u[p])) * penalty[p],
    } for p in P])

    summary = pd.DataFrame([{
        "status": pl.LpStatus[status],
        "objective_total_k": float(pl.value(model.objective)),
        "capex_total_k": float(tool_buy["capex_spend_k"].sum()),
        "shortage_total_k": float(prod["shortage_cost"].sum()),
        "num_vars": model.numVariables(),
        "num_constraints": model.numConstraints(),
    }])

    tool_buy.to_csv(res_dir / "tool_buy.csv", index=False)
    prod.to_csv(res_dir / "product_summary.csv", index=False)
    summary.to_csv(res_dir / "solution_summary.csv", index=False)

    print("Solved. Status:", pl.LpStatus[status])
    print(summary.to_string(index=False))
    print("Saved:", (res_dir / "solution_summary.csv").resolve())

if __name__ == "__main__":
    solve()
