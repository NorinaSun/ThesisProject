import os
import random
import csv
import numpy as np
import data_collection as data
import ip_functions as ip
import porta_functions as porta
import time
import gurobipy as gp
from gurobipy import GRB



#defining the model
def def_model(problem_id):

    return gp.Model(f"knapsack_{problem_id}")


#adding decision vars to model
def add_decision_vars(model, num_vars):
    variable_dict = {}
    for i in range(1,num_vars+1):
        variable_dict["x%s" %i] = model.addVar(vtype=GRB.INTEGER, name="x%s" %i)

    return variable_dict


#setting the objective
def concat_var_coef(variables, co_list):

    if type(variables) == list:
        results = ""

        for coefficient, variable in zip(co_list, variables):
            results += f"{coefficient}{variable}"
            
            if variable != variables[len(variables)-1]:
                results += " + "
        
    elif type(variables) == dict:
        results = []

        for coefficient, variable in zip(co_list, variables):
            elm = coefficient*variables[variable]
            results.append(elm)

    return results

def set_objective(model, variable_dict, obj_func_coefs, method = GRB.MAXIMIZE):

    vars = concat_var_coef(variable_dict, obj_func_coefs)
    
    model.setObjective(gp.quicksum(vars), method)


# adding constraints
def add_constraint(model, variable_dict, co_list, rhs, inequality='<='):
    
    vars = concat_var_coef(variable_dict, co_list)

    if inequality == '<=':
        model.addConstr(gp.quicksum(vars) <= rhs)
    elif inequality == '>=':
        model.addConstr(gp.quicksum(vars) >= rhs)
    else:
        raise AttributeError('Inequality passed is not valid. Try "less than" or "greater than"')
        
# actually running the model
def run_solver(iteration, num_vars, constraints, obj_func_coefs):
    
    # create the model
    m = gp.Model(f"model_{iteration}")

    # adding the decision variables
    variable_dict = add_decision_vars(m, num_vars)

    # setting the objective
    set_objective(m, variable_dict, obj_func_coefs)

    #adding the constraints
    for constraint in constraints:
        add_constraint(m
            , variable_dict
            , constraint["lhs"]
            , constraint["rhs"]
            , constraint['inequality']
        )

    start_time = time.time()
    m.optimize()
    run_time = time.time() - start_time

    return m.ObjVal, run_time
