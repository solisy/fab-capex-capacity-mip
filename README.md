# Fab Tool CapEx + Capacity + Product Flow Optimizer (MIP Prototype)

> Note: Most of my prior work has been in internal systems/data environments.  
> This is a small public prototype to demonstrate my modeling approach and decision-support packaging.


A small, reproducible decision-support prototype that selects tool purchases (CapEx proxy) and allocates product flow through multi-step process routing under tool-capacity constraints.

## Why this matters
Fab planning often needs to answer:
- What tool purchases (CapEx) are required to meet demand?
- How should product volume be allocated across eligible tools/steps under capacity limits?
- What is the cost tradeoff between CapEx investment and shortage risk?

This prototype demonstrates a Mixed-Integer Programming (MIP) formulation for tool-buy decisions and flow allocation, producing an adoption-ready output package (tables + charts).

## Model (high level)
**Decision variables**
- `buy_t` (integer): number of tools to purchase for each tool type `t`
- `x_p,s,t` (continuous): product `p` volume at step `s` assigned to eligible tool type `t`
- `short_p` (continuous): unmet demand for product `p`

**Objective**
Minimize: CapEx + shortage penalty

**Constraints**
- Demand balance: `produced_p + short_p = demand_p`
- Flow conservation: same `produced_p` must pass through each step
- Tool capacity: sum(process_time * flow) <= (capacity_hours * tools_bought)

## Data schema (synthetic)
CSV files in `data/`:
- `products.csv`: demand and shortage penalty per product
- `steps.csv`: ordered process steps
- `tool_types.csv`: CapEx cost and capacity hours per tool type
- `routes.csv`: eligibility map + processing time per unit

## Quick demo (local)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python src/generate_data.py
python src/solve_capex_mip.py
python src/report.py

## How to run
Create/activate venv, then:
```bash
python src/generate_data.py
python src/solve_capex_mip.py
python src/report.py


```
Outputs saved to `results/`:
- `solution_summary.csv`
- `tool_buy.csv`
- `product_summary.csv`
- `charts/tool_purchases.png`
- `charts/cost_breakdown.png`

## Example result (from one run)
- Status: Optimal
- Objective (k$): 6000
- CapEx (k$): 6000
- Shortage (k$): 0
- Vars / Constraints: 138 / 61

## Next extensions (roadmap)
- Multi-period / rolling-horizon planning
- Demand uncertainty with scenario optimization
- Yield / rework modeling
- Larger instances & decomposition/heuristics
