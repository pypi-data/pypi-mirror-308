import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram

def plot_hca(df):
    """
    This function performs Hierarchical Clustering Analysis (HCA) on the provided DataFrame and plots the dendrogram.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame containing compounds as rows and samples as columns.
    """
    # Drop 'Compounds' column for clustering
    data_for_clustering = df.drop(columns=["Compounds"])
    
    # Perform Hierarchical Clustering
    linked = linkage(data_for_clustering, method='ward')
    
    # Create a dendrogram
    plt.figure(figsize=(10, 7))
    dendrogram(linked, labels=df['Compounds'].values, orientation='top', distance_sort='descending', show_leaf_counts=True)
    plt.title('Hierarchical Cluster Analysis Dendrogram')
    plt.xlabel('Compounds')
    plt.ylabel('Distance')
    plt.show()
