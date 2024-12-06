import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_correlation_matrix_samples(data):
    """
    Plot the correlation matrix of the given data.
    
    Parameters:
    data (pd.DataFrame): DataFrame with the first column as sample names and
                         the remaining columns as features.
                         
    Returns:
    pd.DataFrame: Correlation matrix of the features.
    """
    # Extract features and calculate correlation matrix
    features = data.iloc[:, 1:]
    correlation_matrix = features.corr()
    
    # Plot the correlation matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", square=True)
    plt.title("Correlation Matrix")
    plt.show()
    
    return correlation_matrix
