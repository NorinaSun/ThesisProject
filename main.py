import solver
import porta_functions as porta
import data_collection
import ip_functions as ip
import ml
import random
import os
import pandas as pd
import json

def gen_iteration(problem_id, num_vars, num_inequalities=2):

    # initialize the porta file
    porta_file = porta.init_ieq_file(problem_id, num_vars)

    #generate a set of inequalities
    for inequality in range(num_inequalities):

        lhs_coef, rhs = ip.gen_lessthan_inequality(num_vars)

        # write the inequality to data file
        data_collection.write_row('original_constraints', [problem_id, inequality, lhs_coef, rhs, "<="] )

        # pass to ml 
        ml.fake_ml(problem_id, lhs_coef, rhs)

        # add inequality to porta file
        # create inequality
        lhs = solver.concat_var_coef([f'x{i}' for i in range(1, num_vars+1)],lhs_coef)
        porta.add_ieq_inequalities(porta_file, num_vars, f"{lhs} <= {rhs}")
        

    #end the porta file
    porta.end_ieq_file(porta_file, num_vars)

    #now do the whole bash traf thing
    os.system(f"bash traf ieq_{problem_id}.ieq")

    feasible_points = porta.get_integer_points(f'ieq_{problem_id}.ieq')
    porta.create_poi_file(problem_id, num_vars, feasible_points)
    os.system(f'bash traf poi_{problem_id}.poi' )

    #moving the files to respective folders
    os.rename(f"ieq_{problem_id}.ieq", f"ieq/ieqs_{problem_id}.ieq")
    os.rename(f"ieq_{problem_id}.ieq.poi", f"ieq_poi/ieqs_{problem_id}.ieq.poi")
    os.rename(f"poi_{problem_id}.poi", f"poi/poi_{problem_id}.poi")
    os.rename(f"poi_{problem_id}.poi.ieq", f"poi_ieq/poi_{problem_id}.poi.ieq")

    #store porta results in data file
    porta_results = porta.get_constraints(f"poi_ieq/poi_{problem_id}.poi.ieq", num_vars)

    inequality_id = 1

    for inequality in porta_results:
        data_collection.write_row('porta_convex_hull',[problem_id, inequality_id, inequality['coef'], inequality['rhs'], inequality['inequality']])
        inequality_id += 1

def gen_objective_function_file(num_functions, min_vars, max_vars):

    objective_function_id = 1
    
    for num_vars in range(min_vars,max_vars+1):
        for i in range(num_functions):

            obj_coef = ip.gen_objective_functions(num_vars)
            data_collection.write_row('objective_functions',[objective_function_id,num_vars,obj_coef])
            objective_function_id += 1

#the goal is to compare the generated convex hull by ML
def do_stuff():

    #load all the csv's as dataframes

    original_constraints = pd.read_csv("data/original_constraints.csv")
    porta_convex_hull = pd.read_csv("data/convex_hull_porta.csv")
    ml_convex_hull = pd.read_csv("data/convex_hull_ml.csv")
    objective_functions = pd.read_csv("data/objective_functions.csv")

    #the goal is to compare the generated convex hull by ML

    # try:
    #     np.array_equal(porta_convex_hull['problem_id'].unique(),ml_convex_hull['problem_id'].unique()):
    # except False as error:

    problem_array = porta_convex_hull['problem_id'].unique()

    for problem_id in problem_array():

        # get the number of vars
        lhs_string = porta_convex_hull[porta_convex_hull['problem_id'] == problem_id]['lhs'][0]
        lhs_list = json.loads(lhs_string)

        # get the number of constraints for this problem id
        num_constraints = len(porta_convex_hull[porta_convex_hull['problem_id'] == problem_id]['inequality_id'])

        # get the actual constraints 
        constraints = porta_convex_hull.loc[(porta_convex_hull['problem_id'] == problem_id)]
            
    json.loads(porta_convex_hull.loc[(porta_convex_hull['problem_id'] == 1234)]['lhs']).tolist()


        # objective_function_coefs = objective_functions[objective_functions['num_vars'] == num_vars]

        # for objective_function in 

        # solver.run_solver(problem_id, )
        


def run_program(num_files):


    #init
    data_collection.set_column_names()
    
    

if __name__ == "__main__":

    run_program(1)

    #json.loads(x) for string back to list