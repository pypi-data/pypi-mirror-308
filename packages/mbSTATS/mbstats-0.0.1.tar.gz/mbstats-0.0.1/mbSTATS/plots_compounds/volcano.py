import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_volcano(p_values_df, p_value_col='p-value', compound_col='Compound', fc_threshold=1, p_value_threshold=0.1):
    """
    Plots a volcano plot for the given p-values DataFrame.

    Parameters:
    p_values_df (pd.DataFrame): DataFrame containing 'Compound' and 'p-value' columns.
    p_value_col (str): Name of the column containing p-values. Default is 'p-value'.
    compound_col (str): Name of the column containing compound names. Default is 'Compound'.
    fc_threshold (float): Fold change threshold for significance. Default is 1.
    p_value_threshold (float): P-value threshold for significance. Default is 0.1.
    """
    # Calculate -log10(p-value)
    p_values_df['-log10(p-value)'] = -np.log10(p_values_df[p_value_col])

    # Identify significantly changed compounds based on thresholds
    p_values_df['Significance'] = 'Not Significant'
    p_values_df.loc[(p_values_df[p_value_col] < p_value_threshold), 'Significance'] = 'Significant'

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.scatter(p_values_df.index, p_values_df['-log10(p-value)'], c=np.where(p_values_df['Significance'] == 'Significant', 'red', 'gray'), label='Not Significant')
    plt.scatter(p_values_df[p_values_df['Significance'] == 'Significant'].index, p_values_df[p_values_df['Significance'] == 'Significant']['-log10(p-value)'], c='red', label='Significant')

    # Plot formatting
    plt.axhline(-np.log10(p_value_threshold), color='blue', linestyle='--', label=f'p-value threshold = {p_value_threshold}')
    plt.xlabel('Compounds')
    plt.ylabel('-log10(p-value)')
    plt.title('Volcano Plot')
    plt.legend()
    plt.show()
