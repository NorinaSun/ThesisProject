import porta_functions as porta
import general_functions as gen
import ip_functions as ip
import random
import os

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