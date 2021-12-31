import os
import random
import csv
import numpy as np
import general_functions as gen
import ip_functions as ip

def create_ieq_file(file_num,num_vars,num_inequalities=1):

    ieq_f = open(f'ieq_file_{file_num}.ieq',"w")

    ieq_f.write(f"DIM = {num_vars} \n \n")
    ieq_f.write("VALID \n")
    ieq_f.write(f"{num_vars*'0 '} \n \n")
    ieq_f.write("LOWER_BOUNDS \n")
    ieq_f.write(f"{num_vars*'0 '} \n \n")
    ieq_f.write("UPPER_BOUNDS \n")
    ieq_f.write(f"{num_vars*'1 '} \n \n")
    ieq_f.write("INEQUALITIES_SECTION \n")

    while num_inequalities != 0:
        num_inequalities -= 1

        inequality, inequality_list = ip.gen_inequalities()
        inequality_list.insert(0,file_num)
        gen.write_row(inequality_list)

        ieq_f.write(inequality + "\n" )

    for i in range(1,num_vars+1):
        ieq_f.write(f'x{i} <= 1 \n')
        ieq_f.write(f'x{i} >= 0 \n')

    ieq_f.write("\nEND \n")
    ieq_f.close()

def create_poi_file(file_num, num_vars, int_points):

    poi_f = open(f'poi_file_{file_num}.poi',"w+")
    
    poi_f.write(f"DIM = {num_vars} \n \n")
    poi_f.write("CONV_SECTION \n")
    
    for point in int_points:
        print(*point, file = poi_f)

    poi_f.write("\nEND \n")
    poi_f.write(f"DIMENSION OF THE POLYHEDRON : {num_vars}\n \n")

    poi_f.close()

def get_integer_points(filename):

    with open(f'{filename}.poi') as f:
        lines = f.readlines()

    list_results = []

    for i in lines:

        if "(" in i and "/" not in i:

            value_str  = i.translate(str.maketrans("","", "()\n"))
            value_list = list(value_str.split())
            list_results.append(value_list[1:])

    return list_results