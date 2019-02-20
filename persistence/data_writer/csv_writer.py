import pandas as pd

def store_researchers(researchers, output="./researchers.csv"):
    pd.DataFrame([researcher.to_dataframe() for researcher in researchers]).to_csv(output)