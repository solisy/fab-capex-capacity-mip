# Fab Tool CapEx & Capacity Optimizer (MIP Prototype)
**Author:** Sol Li  
**Target Role:** Micron – Operations Research Analyst (JR87072)

## Business Context
Fab planning often needs to decide tool purchases (CapEx) and allocate capacity across process steps to meet demand at minimum cost. This prototype unifies tool-buy and flow allocation decisions under tool-capacity constraints into a reproducible decision-support model.

## Approach
- Built a **Mixed-Integer Programming (MIP)** model to choose tool purchase quantities (integer) and allocate product flow (continuous).
- Encoded **tool-capacity constraints** using processing time × flow ≤ capacity hours × tools purchased.
- Enforced **multi-step product flow consistency** (the same produced quantity must pass through each step).
- Used structured, schema-like inputs (products / steps / tool types / routes) and generated adoption-ready outputs (tables + charts).

## Outputs
- Recommended tool purchases by type (CapEx)
- Cost breakdown: CapEx vs shortage penalty
- Product-level summary: demand, produced, shortage

## Result Snapshot (one run)
- **Status:** Optimal  
- **Objective (k$):** 6000  
- **CapEx (k$):** 6000  
- **Shortage penalty (k$):** 0  
- **Model size:** 138 variables / 61 constraints  
- **Artifacts:** results/charts/tool_purchases.png, results/charts/cost_breakdown.png
