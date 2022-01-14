import os
import random
import csv

def write_row(table, new_row):
    '''
    Data tables are defined in a dictionary, accepts a table name and row values, writes row to table.

    Table options:
        - original_constraints
        - porta_convex_hull
        - ml_convex_hull
        - objective_functions
        - convex_hull_results
        - ml_enriched_constraints_results
    '''

    data_table = {
        'original_constraints': open('data/original_constraints.csv', 'a'),
        'porta_convex_hull': open('data/porta_convex_hull.csv', 'a'),
        'ml_convex_hull': open('data/ml_convex_hull.csv', 'a'),
        'objective_functions': open('data/objective_functions.csv', 'a'),
        'convex_hull_results' : open('data/convex_hull_results.csv','a'),
        'ml_enriched_constraints_results' : open('data/ml_enriched_constraints_results.csv','a')
    }
    
    writer = csv.writer(data_table[table])
    writer.writerow(new_row)

    data_table[table].close()

def set_column_names():
    '''
    Set the column names for the data files
    Accepts no parameters, returns nothing
    '''

    write_row('original_constraints',["problem_id","lhs","rhs", "inequality"])

    write_row('porta_convex_hull',["problem_id","lhs","rhs", "inequality"])

    write_row('ml_convex_hull',["problem_id","lhs","rhs", "inequality"])

    write_row('objective_functions',["objective_function_id","objective_function_coefficients"])
    
    write_row('convex_hull_results',["id","problem_id", "objective_function_id","ml_solver","porta_solver"])

    write_row('ml_enriched_constraints_results',["id","problem_id", "objective_function_id","original_solver","ml_solver", "original_runtime","ml_runtime"])

# def create_constraint_row(id,lhs, rhs, inequality = '<='):



#     write_row('constraint_tbl', [id, lhs, rhs, inequality] )
