import pulp as pl

x = pl.LpVariable("x", lowBound=0, cat="Integer")
y = pl.LpVariable("y", lowBound=0, cat="Integer")

model = pl.LpProblem("smoke_test", pl.LpMaximize)
model += 3*x + 2*y
model += 2*x + y <= 8
model += x + 2*y <= 8

status = model.solve(pl.PULP_CBC_CMD(msg=False))
print("Status:", pl.LpStatus[status])
print("x =", int(pl.value(x)), "y =", int(pl.value(y)))
print("Objective =", pl.value(model.objective))
