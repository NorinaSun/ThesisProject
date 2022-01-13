import os
import random
import csv
import ThesisProject.data_collection as data_collection
import porta_functions as porta
import numpy as np
import ml
import solver

def gen_lessthan_inequality(num_vars=2):
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

def gen_iteration(problem_id, num_vars, num_inequalities=1):

    # initialize the porta file
    porta_file = porta.init_ieq_file(problem_id, num_vars)

    #generate a set of inequalities
    for num in num_inequalities:

        lhs_coef, rhs = gen_lessthan_inequality()

        # write the inequality to data file
        data_collection.write_row('constraint_tbl', [problem_id, lhs_coef, rhs] )

        # pass to ml 
        ml.fake_ml(problem_id, lhs_coef, rhs)

        # add inequality to porta file
        # create inequality
        solver.concat_var_coef(,lhs_coef)
        porta.add_ieq_inequalities(porta_file, f"{lhs} <= {rhs}")
        


        #solve everything



        



