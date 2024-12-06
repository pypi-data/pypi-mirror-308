import pandas as pd

def tsn_normalization(df):
    tsn_df = df.iloc[:, 1:].div(df.iloc[:, 1:].sum(axis=1), axis=0)
    return pd.concat([df.iloc[:, 0], tsn_df], axis=1)
