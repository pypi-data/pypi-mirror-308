import matplotlib.pyplot as plt
import numpy as np

def plot_grp_avg(df, compound_codes):
    """
    Plots the average intensities of selected compounds across different sample groups.
    
    Parameters:
        df (DataFrame): DataFrame containing the sample intensities and group labels.
        compound_codes (list): List of compound codes to be included in the plot.
    
    Returns:
        None: Displays the bar plot of average compound intensities across groups.
    """
    # Assign group labels based on sample names
    df['Group'] = df['sample'].apply(lambda x: 'wt' if 'wt' in x else 'oe1' if 'oe1' in x else 'oe2')
    
    # Select only the specified compound codes and numeric columns for averaging
    selected_compounds_df = df[['sample', 'Group'] + compound_codes]
    
    # Calculate the average intensity for each compound per group
    avg_df = selected_compounds_df.groupby('Group')[compound_codes].mean().T  # Transpose to plot compounds on x-axis
    
    # Plot the average intensities
    avg_df.plot(kind='bar', figsize=(10, 6))
    plt.title('Average Compound Intensities Across Groups')
    plt.xlabel('Compounds')
    plt.ylabel('Average Intensity')
    plt.legend(title='Group')
    plt.tight_layout()
    plt.show()

# Example usage:
# plot_group_averages(coda_df, ['c1', 'c2', 'c3', 'c4', 'c5'])
