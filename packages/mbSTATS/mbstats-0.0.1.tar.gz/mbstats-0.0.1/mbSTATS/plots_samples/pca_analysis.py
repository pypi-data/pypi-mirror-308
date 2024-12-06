import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def perform_pca(data):
    """
    Perform PCA on the given data and plot the results with sample labels.
    
    Parameters:
    data (pd.DataFrame): DataFrame with the first column as sample names and
                         the remaining columns as features.
                         
    Returns:
    pd.DataFrame: DataFrame containing the PCA components.
    """
    # Separate features and target column
    features = data.iloc[:, 1:].values
    samples = data.iloc[:, 0].values
    
    # Standardize the data
    scaler = StandardScaler()
    features_std = scaler.fit_transform(features)
    
    # Perform PCA
    pca = PCA(n_components=2)  # Adjust number of components as needed
    pca_components = pca.fit_transform(features_std)
    
    # Create a DataFrame with PCA results
    pca_df = pd.DataFrame(data=pca_components, columns=['PC1', 'PC2'])
    pca_df['sample'] = samples
    
    # Plotting the PCA result
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='PC1', y='PC2', hue='sample', data=pca_df, palette="viridis", s=100)
    
    # Annotate each point with the sample name
    for i, sample in enumerate(pca_df['sample']):
        plt.text(pca_df['PC1'][i], pca_df['PC2'][i], sample, fontsize=9, ha='right')
        
    plt.title("PCA of Samples")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.legend(title="Sample Type", bbox_to_anchor=(1, 1))
    plt.show()
    
    return pca_df
