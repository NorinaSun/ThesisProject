import os
import random
import csv
import numpy as np

def gen_inequalities(num_vars=2,max_vars=5):
    """
    Generates inequalities given a the number of variables to consider.

    Returns the inquality in a string format for porta, and as a list for gurobi.

    """

    lhs = ""
    sum_lhs = 0
    inequality_list = []

    for i in range(1,num_vars+1):
            
        rand_integer = random.randint(1,11)
        sum_lhs += rand_integer
        inequality_list.extend([rand_integer])

        lhs +=  f'{rand_integer}x{i}'

        if i != num_vars:
            lhs += ' +'
    
    
    rhs = round(sum_lhs*random.uniform(0.8,1))

    # commenting out the padding of the inequality for now
    #inequality_list.extend([0]*(max_vars-num_vars))  
    #inequality_list.extend([rhs])

    return ('%s <= %s' % (lhs,rhs), inequality_list, rhs)
