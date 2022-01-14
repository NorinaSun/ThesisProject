import porta_functions as porta
import data_collection
import ip_functions as ip
import solver
import ml
import random
import os

def gen_iteration(problem_id, num_vars, num_inequalities=2):

    #init
    data_collection.set_column_names()

    # initialize the porta file
    porta_file = porta.init_ieq_file(problem_id, num_vars)

    #generate a set of inequalities
    for inequality in range(num_inequalities):

        lhs_coef, rhs = ip.gen_lessthan_inequality()

        # write the inequality to data file
        data_collection.write_row('original_constraints', [problem_id, lhs_coef, rhs, "<="] )

        # pass to ml 
        ml.fake_ml(problem_id, lhs_coef, rhs)

        # add inequality to porta file
        # create inequality
        lhs = solver.concat_var_coef([f'x:{i}' for i in range(1, num_vars+1)],lhs_coef)
        porta.add_ieq_inequalities(porta_file, num_vars, f"{lhs} <= {rhs}")
        
        

        #solve everything



def run_program(num_files):

    #commenting out data collection functionality for now
    #gen.write_row(gen.create_title())

    for i in range(1,num_files+1):

        num_vars = random.randrange(2,5)

        porta.create_ieq_file(i, num_vars)
        os.system("bash traf ieq_file_%s.ieq" % i)

        feasible_points = porta.get_integer_points('ieq_file_%s.ieq' % i)
        porta.create_poi_file(i, num_vars, feasible_points)
        os.system('bash traf poi_file_%s.poi' % i )

        #moving the files to respective folders
        os.rename(f"ieq_file_{i}.ieq", f"ieq/ieq_file_{i}.ieq")
        os.rename(f"ieq_file_{i}.ieq.poi", f"ieq_poi/ieq_file_{i}.ieq")
        os.rename(f"poi_file_{i}.poi", f"poi/poi_file_{i}.poi")
        os.rename(f"poi_file_{i}.poi.ieq", f"poi_ieq/poi_file_{i}.poi")
    
    

if __name__ == "__main__":

    run_program(1)

    #json.loads(x) for string back to list