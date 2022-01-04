import os
import random
import csv
import numpy as np
import general_functions as gen
import ip_functions as ip
import porta_functions as porta
import gurobipy as gp
from gurobipy import GRB


#defining vars and constants

#defining the model
m = gp.Model("knapsack")

#adding decision vars to model
x1 = m.addVar(vtype=GRB.INTEGER, name='x1')
x2 = m.addVar(vtype=GRB.INTEGER, name='x2')
x3 = m.addVar(vtype=GRB.INTEGER, name='x3')

#setting the objective
m.setObjective(3*x1 + 4*x2 + 4*x3, GRB.MINIMIZE)

#adding constraints
m.addConstr(x1 + 2*x2 <= 12, "c1")
m.addConstr(x2 + x3 <= 13, "c2")

m.optimize()

for v in m.getVars():
    print('%s %g' % (v.VarName, v.X))

print('Obj: %g' % m.ObjVal)