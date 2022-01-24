import os
import random
import csv
import pandas as pd


def init_tables():

    if os.path.getsize(get_tbl('original_constraints','path')) == 0:
        set_column_names()


def get_tbl(tbl_name, format):

    data_mapping = {
        'original_constraints': 'data/original_constraints.csv',
        'porta_convex_hull': 'data/convex_hull_porta.csv',
        'ml_convex_hull': 'data/convex_hull_ml.csv',
        'objective_functions': 'data/objective_functions.csv',
        'convex_hull_results' : 'data/results_convex_hull.csv',
        'ml_enriched_constraints_results' : 'data/results_ml_enriched_constraints.csv'
    }

    if format == 'text':
        return open(data_mapping[tbl_name],'a')
    elif format == 'dataframe':
        return pd.read_csv(data_mapping[tbl_name])
    elif format == 'path':
        return data_mapping[tbl_name]
    else:
        raise ValueError("format not known, please use either 'text', 'dataframe', or 'path'")


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

    file = get_tbl(table,'text')
    writer = csv.writer(file)
    writer.writerow(new_row)

    file.close()

def set_column_names():
    '''
    Set the column names for the data files
    Accepts no parameters, returns nothing
    '''

    write_row('original_constraints',["problem_id","inequality_id","lhs","rhs", "inequality"])

    write_row('porta_convex_hull',["problem_id","inequality_id","lhs","rhs", "inequality"])

    write_row('ml_convex_hull',["problem_id","inequality_id","lhs","rhs", "inequality"])

    write_row('objective_functions',["objective_function_id","num_vars","objective_function_coefficients"])
    
    write_row('convex_hull_results',["id","problem_id", "objective_function_id","ml_solver","porta_solver"])

    write_row('ml_enriched_constraints_results',["id","problem_id", "objective_function_id","original_solver","ml_solver", "original_runtime","ml_runtime"])

# def create_constraint_row(id,lhs, rhs, inequality = '<='):



#     write_row('constraint_tbl', [id, lhs, rhs, inequality] )
