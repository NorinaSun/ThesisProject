import os
import random
import csv
import numpy as np

def gen_inequalities(num_vars=2,max_vars=5):

    lhs = ""
    sum_lhs = 0
    inequality_list = []

    for i in range(1,num_vars+1):
            
        rand_integer = random.randint(1,11)
        sum_lhs += rand_integer
        inequality_list.extend([rand_integer])

        lhs +=  f'{rand_integer}x{i}'

        if i != num_vars:
            lhs += ' +'
        
    inequality_list.extend([0]*(max_vars-num_vars))  
    rhs = round(sum_lhs*random.uniform(0.8,1))
    inequality_list.extend([rhs])

    return (f'{lhs} <= {rhs}', inequality_list)

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

        inequality, inequality_list = gen_inequalities()
        inequality_list.insert(0,file_num)
        write_row(inequality_list)

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

def write_row(new_row):

    csv_f = open(f'ieq_file.csv', 'a',newline='')

    writer = csv.writer(csv_f)
    writer.writerow(new_row)

    csv_f.close()

def create_title(max_vars=6):

    title = ['instance']
    title.extend(["x"+str(x) for x in range(1,max_vars+1)])

    return title

def run_program(num_files):

    write_row(create_title())

    for i in range(1,num_files+1):

        num_vars = random.randrange(2,5)

        create_ieq_file(i, num_vars)
        os.system(f'bash traf ieq_file_{i}.ieq' )

        feasible_points = get_integer_points(f'ieq_file_{i}.ieq')
        create_poi_file(i, num_vars, feasible_points)
        os.system(f'bash traf poi_file_{i}.poi' )

if __name__ == "__main__":

    run_program(1)