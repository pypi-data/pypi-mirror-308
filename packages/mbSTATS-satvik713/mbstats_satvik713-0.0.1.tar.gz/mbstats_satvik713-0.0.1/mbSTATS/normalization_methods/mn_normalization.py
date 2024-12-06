import pandas as pd

def mn_normalization(df):
    median_values = df.iloc[:, 1:].median(axis=1)
    mn_df = df.iloc[:, 1:].div(median_values, axis=0)
    return pd.concat([df.iloc[:, 0], mn_df], axis=1)
