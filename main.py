import solver
import porta_functions as porta
import data_collection as data
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
        data.write_row('original_constraints', [problem_id, inequality, lhs_coef, rhs, "<="] )

        # pass to ml 
        ml.fake_ml(problem_id, inequality, lhs_coef, rhs, "<=")

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
    porta_results = porta.get_porta_constraints(f"poi_ieq/poi_{problem_id}.poi.ieq", num_vars)

    inequality_id = 1

    for inequality in porta_results:
        data.write_row('porta_convex_hull',[problem_id, inequality_id, inequality['coef'], inequality['rhs'], inequality['inequality']])
        inequality_id += 1

def gen_objective_function_file(num_functions, min_vars, max_vars):

    objective_function_id = 1
    
    for num_vars in range(min_vars,max_vars+1):
        for i in range(num_functions):

            obj_coef = ip.gen_objective_function(num_vars)
            data.write_row('objective_functions',[objective_function_id,num_vars,obj_coef])
            objective_function_id += 1

def get_objective_functions(num_vars):

    objective_functions = data.get_tbl('objective_functions', 'dataframe')
    
    results = {}

    relevant_tbl = objective_functions[objective_functions['num_vars'] == num_vars]

    for row_index in relevant_tbl.index:
        row = relevant_tbl.loc[row_index]
        results[row['objective_function_id']] = json.loads(row['objective_function_coefficients'])
        
    return results

def get_df_constraints(df):
    constraints_list = []
    for index, row in df.iterrows():

        constraints_list.append(
            {'inequality_id': row['inequality_id']
            , 'rhs': row['rhs']
            , 'lhs': json.loads(row['lhs'])
            , 'inequality': row['inequality']
            }
        )
    
    return constraints_list

def get_num_vars(df):

    df.reset_index(inplace=True)
    return len(json.loads(df['lhs'][0]))

    
def gen_results():

    #open all the files
    original_constraints = data.get_tbl('original_constraints', 'dataframe')
    porta_convex_hull = data.get_tbl('porta_convex_hull', 'dataframe')
    ml_convex_hull = data.get_tbl('ml_convex_hull', 'dataframe')

    objective_functions = data.get_tbl('objective_functions', 'dataframe')

    # 1. grab the problem ids
    problem_list = original_constraints['problem_id'].unique()
    
    # 2. loop through the problem ids
    for problem_id in problem_list:
        # 3. grab the respective constraints for each problem id

        #get tbl subset 
        sub_original_constraints = original_constraints[original_constraints["problem_id"] == problem_id]
        sub_porta_convex_hull = porta_convex_hull[porta_convex_hull["problem_id"] == problem_id]
        sub_ml_convex_hull = ml_convex_hull[ml_convex_hull["problem_id"] == problem_id]
    
        #get the constraints as a dict
        original_constraints_list = get_df_constraints(sub_original_constraints)
        porta_convex_hull_list = get_df_constraints(sub_porta_convex_hull)
        ml_convex_hull_list = get_df_constraints(sub_ml_convex_hull)

        print(f"here 5: {original_constraints_list}")

        # 4. grab the applicable objective functions for the problem ( can be done earlier )
        # get the number of vars
        num_vars = get_num_vars(sub_original_constraints)
        relevant_obf = get_objective_functions(num_vars)

        # 5. loop through the objective functions and run with with each constraint set
        for objective_function_id, coefs in relevant_obf.items():
            original_opt, original_runtime, = solver.run_solver(f'{problem_id}-{objective_function_id}-original', num_vars, original_constraints_list, coefs)
            porta_opt, porta_runtime, = solver.run_solver(f'{problem_id}-{objective_function_id}-porta', num_vars, porta_convex_hull_list, coefs)
            ml_opt, ml_runtime, = solver.run_solver(f'{problem_id}-{objective_function_id}-porta', num_vars, ml_convex_hull_list, coefs)

            # 6. write results to file
            data.write_row('convex_hull_results',[f'{problem_id}-{objective_function_id}'
                    , problem_id
                    , objective_function_id
                    , ml_opt
                    , porta_opt
                    ]
                )
            
            data.write_row('ml_enriched_constraints_results',[f'{problem_id}-{objective_function_id}'
                    , problem_id
                    , objective_function_id
                    , original_opt
                    , ml_opt
                    , original_runtime
                    , ml_runtime
                    ]
                )

def run_program(min_vars, max_vars, num_models, num_obj_func):

    #init the data files
    data.init_tables()

    #create the objective functions
    gen_objective_function_file(num_obj_func, min_vars, max_vars)

    #generate the models
    for num_vars in range(min_vars, max_vars+1):
        for model in range(num_models):
            generate_model(f'{str(num_vars)}-{str(model)}', num_vars, num_inequalities=2)

    #run the solver
    gen_results()


if __name__ == "__main__":

    min_vars = int(input("Enter the minimum number of variables you want in your models:  "))

    max_vars = int(input("Enter the maximum number of variables you want in your models:  "))

    num_models = int(input("Enter the number of models you would like to generate per variable number:  "))

    num_obj_func = int(input("Enter the number of objective functions you would like to test each model with:  "))

    run_program(min_vars, max_vars, num_models, num_obj_func)