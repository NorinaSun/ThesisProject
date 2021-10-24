import os
import random
import numpy as np

def gen_inequalities(num_vars):

    LHS = ""
    RHS = 0

    for i in range(1,num_vars+1):
            
        rand_integer = np.random.choice(11,1,p=[0.5]+[0.05]*10)
        RHS += rand_integer[0]

        LHS +=  f'{rand_integer[0]}x{i}'

        if i != num_vars:
            LHS += ' +'

    return f'{LHS} <= {round(RHS*random.uniform(0.5,1))}'


def create_ieq_file(file_num):

    num_vars = random.randrange(2,6)
    #num_inequalities = random.randrange(2,6)
    num_inequalities = 1
    f = open(f'ieq_file_{file_num}.ieq',"w")

    f.write("DIM = 4 \n \n")
    f.write("VALID \n")
    f.write("0 0 0 0 \n \n")
    f.write("LOWER_BOUNDS \n")
    f.write("0 0 0 0 \n \n")
    f.write("UPPER_BOUNDS \n")
    f.write("1 1 1 1 \n \n")
    f.write("INEQUALITIES_SECTION \n")
    
    while num_inequalities != 0:
        f.write(gen_inequalities(num_vars) + "\n" )
        num_inequalities -= 1

    for i in range(1,num_vars+1):
        f.write(f'x{i} <= 1 \n')
        f.write(f'x{i} >= 0 \n')

    f.write("\n END \n")
    f.close()

    return f'ieq_file_{file_num}.ieq'

def run_program(num_files):

    for i in range(1,num_files+1):

        filename = create_ieq_file(i)
        os.system(f'bash traf {filename}' )

run_program(1)