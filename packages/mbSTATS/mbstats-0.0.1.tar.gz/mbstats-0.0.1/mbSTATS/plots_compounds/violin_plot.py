import seaborn as sns
import matplotlib.pyplot as plt

def plot_violin(df, compound_codes):
    """
    Plots a violin plot with a swarm plot overlay to visualize the distribution of compound intensities across groups.
    
    Parameters:
        df (DataFrame): DataFrame containing the compound intensity data and sample labels.
        compound_codes (list): List of compound codes to be included in the plot.
    
    Returns:
        None: Displays the violin and swarm plot.
    """
    # Assign group labels based on sample names
    df['Group'] = df['sample'].apply(lambda x: 'wt' if 'wt' in x else 'oe1' if 'oe1' in x else 'oe2')
    
    # Melt the DataFrame to long format for Seaborn plotting, using provided compound codes
    melted_df = df.melt(id_vars=['sample', 'Group'], value_vars=compound_codes,
                        var_name='Compound', value_name='Intensity')
    
    # Plot violin and swarm plots
    plt.figure(figsize=(12, 6))
    sns.violinplot(x='Compound', y='Intensity', hue='Group', data=melted_df, split=True, inner=None)
    sns.swarmplot(x='Compound', y='Intensity', hue='Group', data=melted_df, dodge=True, color='k', alpha=0.6, marker="o", edgecolor="gray")
    
    # Plot formatting
    plt.title('Distribution of Compound Intensities Across Groups')
    plt.xlabel('Compound')
    plt.ylabel('Intensity')
    plt.legend(title='Group', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

# Example usage:
# plot_violin_with_swarm(coda_df, ['c1', 'c2', 'c3', 'c4', 'c5'])
