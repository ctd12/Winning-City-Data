import pandas as pd
import os

pwd = os.getcwd()

filepath = pwd + "/case1.csv"

first_import = pd.read_csv(filepath, nrows = 10)
print(first_import)