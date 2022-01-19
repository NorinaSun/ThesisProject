import ip_functions as ip
import data_collection as data
def fake_ml(problem_id, lhs, rhs, inequality= '<='):

    # do some stuff

    # store inequality in file
    data.write_row('ml_convex_hull',[problem_id, 123, lhs, rhs, inequality])