import solver
import porta_functions as porta
import data_collection
import ip_functions as ip
import ml
import random
import os

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

    #solve everything
    

def gen_objective_function_file(num_functions, min_vars, max_vars):

    objective_function_id = 1
    
    for num_vars in range(min_vars,max_vars+1):
        for i in range(num_functions):

            obj_coef = ip.gen_objective_functions(num_vars)
            data_collection.write_row('objective_functions',[objective_function_id,num_vars,obj_coef])
            objective_function_id += 1

def run_program(num_files):


    #init
    data_collection.set_column_names()


    # for i in range(1,num_files+1):

    #     num_vars = random.randrange(2,5)

    #     porta.create_ieq_file(i, num_vars)
    #     os.system("bash traf ieq_file_%s.ieq" % i)

    #     feasible_points = porta.get_integer_points('ieq_file_%s.ieq' % i)
    #     porta.create_poi_file(i, num_vars, feasible_points)
    #     os.system('bash traf poi_file_%s.poi' % i )

    #     #moving the files to respective folders
    #     os.rename(f"ieq_file_{i}.ieq", f"ieq/ieq_file_{i}.ieq")
    #     os.rename(f"ieq_file_{i}.ieq.poi", f"ieq_poi/ieq_file_{i}.ieq")
    #     os.rename(f"poi_file_{i}.poi", f"poi/poi_file_{i}.poi")
    #     os.rename(f"poi_file_{i}.poi.ieq", f"poi_ieq/poi_file_{i}.poi")
    
    

if __name__ == "__main__":

    run_program(1)

    #json.loads(x) for string back to list