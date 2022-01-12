import os
import random
import csv
import numpy as np

def write_row(table, new_row):

    data_table = {
        'constraint_tbl': open('constraints.csv', 'a'),
        'objective_function_tbl': open('objective_function.csv', 'a'),
        'convex_hull' : open('convext_hull.csv','a'),
        'ml_enriched_constraints' : open('ml_enriched_constraints.csv','a')
    }
    
    writer = csv.writer(data_table[table])
    writer.writerow(new_row)

    data_table[table].close()

def create_title(max_vars=6):

    title = ['instance']
    title.extend(["x"+str(x) for x in range(1,max_vars+1)])

    return title

def set_column_names():

    write_row('constraint_tbl',["problem_id","constraint"])

    write_row('objective_function_tbl',["objective_function_id","objective_function"])
    
    write_row('convex_hull',["id","problem_id", "objective_function_id","ml_solver","porta_solver"])

    write_row('ml_enriched_constraints',["id","problem_id", "objective_function_id","original_solver","ml_solver", "original_runtime","ml_runtime"])

