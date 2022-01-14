import os
import random
import csv
import numpy as np
import ip_functions as ip


def init_ieq_file(problem_id, num_vars):

    ieq_f = open('ieq_file_%s.ieq' % problem_id,"w")

    ieq_f.write("DIM = %s \n \n" % num_vars)
    ieq_f.write("VALID \n")
    valid = num_vars*'0 '
    ieq_f.write("%s \n \n" % valid)
    ieq_f.write("LOWER_BOUNDS \n")
    lower_bound = num_vars*'0 '
    ieq_f.write("%s \n \n" % lower_bound)
    ieq_f.write("UPPER_BOUNDS \n")
    upper_bound = num_vars*'1 '
    ieq_f.write("%s \n \n" % upper_bound)
    ieq_f.write("INEQUALITIES_SECTION \n")
    
    return ieq_f

def add_ieq_inequalities(file, num_vars, inequality):

    file.write(f"{inequality}" + "\n")
    
    for i in range(1,num_vars+1):
        file.write('x%s <= 1 \n' % i)
        file.write('x%s >= 0 \n' % i)

def end_ieq_file(file, num_vars):
    
    for i in range(1,num_vars+1):
        file.write('x%s <= 1 \n' % i)
        file.write('x%s >= 0 \n' % i)

    file.write("\nEND \n")
    file.close()
    

def create_poi_file(file_num, num_vars, int_points):

    poi_f = open('poi_file_%s.poi' % file_num,"w+")
    
    poi_f.write("DIM = %s \n \n" % num_vars)
    poi_f.write("CONV_SECTION \n")
    
    for point in int_points:
        print(*point, sep =' ', file = poi_f)

    poi_f.write("\nEND \n")
    poi_f.write("DIMENSION OF THE POLYHEDRON : %s \n \n" % num_vars )

    poi_f.close()

def get_integer_points(filename):

    with open('%s.poi' % filename) as f:
        lines = f.readlines()

    list_results = []

    for i in lines:

        if "(" in i and "/" not in i:

            value_str  = i.translate(str.maketrans("","", "()\n"))
            value_list = list(value_str.split())
            list_results.append(value_list[1:])

    return list_results


# def create_ieq_file(file_num,num_vars : int, num_inequalities=1):

#     ieq_f = open('ieq_file_%s.ieq' % file_num,"w")

#     ieq_f.write("DIM = %s \n \n" % num_vars)
#     ieq_f.write("VALID \n")
#     valid = num_vars*'0 '
#     ieq_f.write("%s \n \n" % valid)
#     ieq_f.write("LOWER_BOUNDS \n")
#     lower_bound = num_vars*'0 '
#     ieq_f.write("%s \n \n" % lower_bound)
#     ieq_f.write("UPPER_BOUNDS \n")
#     upper_bound = num_vars*'1 '
#     ieq_f.write("%s \n \n" % upper_bound)
#     ieq_f.write("INEQUALITIES_SECTION \n")

#     while num_inequalities != 0:
#         num_inequalities -= 1

#         inequality, inequality_list = ip.gen_inequalities()

#         #inequality_list.insert(0,file_num)
#         #gen.write_row(inequality_list)

#         ieq_f.write(inequality + "\n" )

#     for i in range(1,num_vars+1):
#         ieq_f.write('x%s <= 1 \n' % i)
#         ieq_f.write('x%s >= 0 \n' % i)

#     ieq_f.write("\nEND \n")
#     ieq_f.close()