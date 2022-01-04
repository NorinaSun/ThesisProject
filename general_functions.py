import os
import random
import csv
import numpy as np

def write_row(new_row):

    csv_f = open('ieq_file.csv', 'a')

    writer = csv.writer(csv_f)
    writer.writerow(new_row)

    csv_f.close()

def create_title(max_vars=6):

    title = ['instance']
    title.extend(["x"+str(x) for x in range(1,max_vars+1)])

    return title