import os
import random
import csv
import numpy as np

def gen_inequalities(num_vars=2,max_vars=5):
    """
    Generates inequalities given a the number of variables to consider.

    Returns the lhs coefficients and rhs value.
    """
    sum_lhs = 0
    lhs_coef = []

    for i in range(1,num_vars+1):
            
        rand_integer = random.randint(1,11)
        sum_lhs += rand_integer
        lhs_coef.extend([rand_integer])
    
    rhs = round(sum_lhs*random.uniform(0.8,1))

    return (lhs_coef, rhs)

def gen_objective_function(num_vars, max_val = 15):
    """
    Generates a list of values the length of the given number of variables

    Optional parameter to specify the max value of 
    """

    return random.choices(range(max_val),k=num_vars)

    # commenting out the padding of the inequality for now
    #inequality_list.extend([0]*(max_vars-num_vars))  
    #inequality_list.extend([rhs])


