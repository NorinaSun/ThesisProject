import os
import random
import csv
import numpy as np
import ip_functions as ip
import re


def init_ieq_file(problem_id, num_vars):

    ieq_f = open('ieq_%s.ieq' % problem_id,"w")

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

def end_ieq_file(file, num_vars):
    
    for i in range(1,num_vars+1):
        file.write('x%s <= 1 \n' % i)
        file.write('x%s >= 0 \n' % i)

    file.write("\nEND \n")
    file.close()
    

def create_poi_file(file_num, num_vars, int_points):

    poi_f = open('poi_%s.poi' % file_num,"w+")
    
    poi_f.write("DIM = %s \n \n" % num_vars)
    poi_f.write("CONV_SECTION \n")
    
    for point in int_points:
        print(*point, sep =' ', file = poi_f)

    poi_f.write("\nEND \n")
    poi_f.write("DIMENSION OF THE POLYHEDRON : %s \n \n" % num_vars )

    poi_f.close()

def get_porta_constraints(filename, num_vars):
    with open(filename) as f:
        lines = f.readlines()
    
    list_results = []

    for i in lines:

        #take inequality columns only
        if "(" in i:
            #extract string values
            value_str  = i.translate(str.maketrans("","", "()\n"))
            value_list = list(value_str.split())[1:]
            
            #check if vars were sticky
            for val in value_list:
                if val.count("x") > 1:

                    split_list = re.split(r'([+-])',val)
                    split_list.remove('')

                    i = 0
                    while i <= val.count("x"): #2
                        split_var = split_list[i] + split_list[i+1]
                        value_list.insert(int(i/2),split_var)
                        i += 2

                    value_list.remove(val)

            #extract the coefficients
            rhs_list = [ x for x in value_list if "x" in x ]
            coefficient_list = []

            for var in range(1,num_vars+1):
                coefficient = 0

                for val in rhs_list:
                    if f'x{var}' in val:
                        coefficient = int(float(val.replace(f'-x{var}', '-1').replace(f'+x{var}', '1').replace(f'x{var}', '')))
                        break
                
                coefficient_list.append(coefficient)

            for val in value_list:

                if '<=' in val:
                    inequality = '<='
                elif 'x' not in val and '=' not in val:
                    rhs = val

            inequality_dict = {'coef': coefficient_list, 'rhs': rhs, 'inequality': inequality}

            list_results.append(inequality_dict)

    return list_results
    
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