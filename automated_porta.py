import porta_functions as porta
import general_functions as gen
import ip_functions as ip
import random
import os

def run_program(num_files):

    gen.write_row(gen.create_title())

    for i in range(1,num_files+1):

        num_vars = random.randrange(2,5)

        porta.create_ieq_file(i, num_vars)
        os.system(f'bash traf ieq_file_{i}.ieq' )

        feasible_points = porta.get_integer_points(f'ieq_file_{i}.ieq')
        porta.create_poi_file(i, num_vars, feasible_points)
        os.system(f'bash traf poi_file_{i}.poi' )

if __name__ == "__main__":

    run_program(1)