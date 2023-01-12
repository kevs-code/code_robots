from automagica import *
import pandas as pd


class Get():
    def __init__(self):
        df = ExcelDataFrame('read_xlsx/magical.xlsx', sheet_name='Sheet1')
        df.to_csv('read_xlsx/magical.csv', sep=',')
