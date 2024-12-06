import numpy as np
import pandas as pd 

def clr_transformation(row):
    epsilon = 1e-9  # Small value to prevent log(0)
    log_values = np.log(row + epsilon)
    geometric_mean = np.exp(log_values.mean())
    return log_values - np.log(geometric_mean)

def coda_normalization(df):
    coda_df = df.iloc[:, 1:].apply(clr_transformation, axis=1)
    return pd.concat([df.iloc[:, 0], coda_df], axis=1)