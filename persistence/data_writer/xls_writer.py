import pandas as pd

def store_researchers(researchers):
    pd.DataFrame([researcher.to_dataframe() for researcher in researchers]).to_excel("results/researchers.xls")