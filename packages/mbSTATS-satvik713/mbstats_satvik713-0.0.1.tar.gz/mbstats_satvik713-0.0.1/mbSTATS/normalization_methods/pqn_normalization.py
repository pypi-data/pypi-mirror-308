import pandas as pd

def pqn_normalization(df):
    wt_samples = df[df['sample'].str.contains('wt', case=False)].iloc[:, 1:]
    
    if wt_samples.empty:
        raise ValueError("No WT samples found. Check the pattern for identifying WT samples.")
    
    reference = wt_samples.mean(axis=0)
    sample_medians = df.iloc[:, 1:].median(axis=1)
    
    normalized_df = df.iloc[:, 1:].div(sample_medians, axis=0)
    quotients = normalized_df.div(reference, axis=1)
    pqn_factors = quotients.median(axis=1)
    
    pqn_df = df.iloc[:, 1:].div(pqn_factors, axis=0)
    return pd.concat([df.iloc[:, 0], pqn_df], axis=1)
