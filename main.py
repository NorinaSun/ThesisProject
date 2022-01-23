import solver
import porta_functions as porta
import data_collection
import ip_functions as ip
import ml
import random
import os
import pandas as pd
import json

def generate_model(problem_id, num_vars, num_inequalities=2):

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

            obj_coef = ip.gen_objective_function(num_vars)
            data_collection.write_row('objective_functions',[objective_function_id,num_vars,obj_coef])
            objective_function_id += 1

def load_csv_df():
    #load all the csv's as dataframes

    original_constraints = pd.read_csv("data/original_constraints.csv")
    porta_convex_hull = pd.read_csv("data/convex_hull_porta.csv")
    ml_convex_hull = pd.read_csv("data/convex_hull_ml.csv")
    objective_functions = pd.read_csv("data/objective_functions.csv")
    convex_hull_results : pd.read_csv("data/results_convex_hull.csv")
    ml_enriched_constraints_results : pd.read_csv("data/results_ml_enriched_constraints.csv")


#the goal is to compare the generated convex hull by ML
def do_stuff():


    #the goal is to compare the generated convex hull by ML

    # try:
    #     np.array_equal(porta_convex_hull['problem_id'].unique(),ml_convex_hull['problem_id'].unique()):
    # except False as error:

    problem_array = porta_convex_hull['problem_id'].unique()

    for problem_id in problem_array:

        results = get_lhs_coef(porta_convex_hull,problem_id)
        print(f'{problem_id} : {results}')


def get_lhs_coef(tbl, problem_id):
    # get the number of vars
    lhs_string = tbl[tbl['problem_id'] == problem_id]['lhs'][0]
    lhs_list = json.loads(lhs_string)

    # get the inequality ids for the problem
    constraint_ids_list = tbl[tbl['problem_id'] == problem_id]['inequality_id'].unique()

    # get the constraints for the problem_id
    constraints = tbl.loc[(tbl['problem_id'] == problem_id)]

    #defining the final list of lists
    results = []

    for constraint_index in constraints.index:
        lhs_coef = json.loads(constraints.iloc[constraint_index]['lhs'])
        results.append(lhs_coef)
    
    return results

def get_objective_functions(tbl,num_vars):
    
    results = {}

    relevant_tbl= tbl[tbl['num_vars'] == num_vars]

    for row_index in relevant_tbl.index:
        row = relevant_tbl.iloc[row_index]
        results[row['objective_function_id']] = json.loads(row['objective_function_coefficients'])
        
    return results


def run_program(min_vars, max_vars, num_models, num_obj_func):


    #init the data files
    data_collection.set_column_names()

    #load all the data files as csv
    load_csv_df()

    #create the objective functions
    gen_objective_function_file(num_obj_func, min_vars, max_vars)

    #generate the models
    for num_vars in range(min_vars, max_vars+1):
        for model in range(num_models):
            generate_model(f'{str(num_vars)}-{str(model)}', num_vars, num_inequalities=2)
    

if __name__ == "__main__":

    min_vars = int(input("Enter the minimum number of variables you want in your models:  "))

    max_vars = int(input("Enter the maximum number of variables you want in your models:  "))

    num_models = int(input("Enter the number of models you would like to generate per variable number:  "))

    num_obj_func = int(input("Enter the number of objective functions you would like to test each model with:  "))

    print(type(min_vars))
    print(max_vars)
    print(num_models)
    print(num_obj_func)

    run_program(min_vars, max_vars, num_models, num_obj_func)