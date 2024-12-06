from mbSTATS.data_preparation import load_csv_data
from mbSTATS.final_df_prep import create_summary_dataframe  # Import the function from final_df_prep.py
from mbSTATS.normalization_methods.tsn_normalization import tsn_normalization
from mbSTATS.normalization_methods.mn_normalization import mn_normalization
from mbSTATS.normalization_methods.coda_normalization import coda_normalization
from mbSTATS.normalization_methods.pqn_normalization import pqn_normalization
from mbSTATS.pval_calculation import calculate_p_values
from mbSTATS.pval_plot import plot_p_values
from mbSTATS.plots_samples.pca_analysis import perform_pca
from mbSTATS.plots_samples.hca_analysis import perform_hca
from mbSTATS.plots_samples.correlation_analysis import plot_correlation_matrix_samples
from mbSTATS.df_convert import convert
from mbSTATS.plots_compounds.hca_analysis import plot_hca
from mbSTATS.plots_compounds.pca_analysis import plot_pca
from mbSTATS.plots_compounds.correlation_matrix import plot_correlation_matrix
from mbSTATS.plots_compounds.volcano import plot_volcano
from mbSTATS.plots_samples.pls_da import pls_da_plot
from mbSTATS.plots_samples.components_inv import investigate
from mbSTATS.plots_compounds.rf_feature_imp import rf_features
from mbSTATS.plots_compounds.heatmap_comp_v_samp import generate_heatmap
from mbSTATS.plots_compounds.violin_plot import plot_violin
from mbSTATS.plots_compounds.grp_avg import plot_grp_avg
from mbSTATS.plots_compounds.comp_density import plot_density


folders = ["/home/satvik/Thesis/csv/wt", "/home/satvik/Thesis/csv/oe", "/home/satvik/Thesis/csv/oe2"]
column_names = [
    "Start_Time", "End_Time", "Retention_Time", "Ion_Mode", 
    "Intensity", "Area_Percentage", "Adjusted_Intensity", 
    "Adjusted_Area_Percentage", "Peak_Width", "Flag", 
    "Compound_Name", "CAS_Number", "Similarity_Score"
]

try:
    # Load the dataframes using the load_csv_data function
    dataframes = load_csv_data(folders, column_names)
    print("Dataframes loaded:", list(dataframes.keys()))  # This should show loaded dataframe names
    
    # Now, test the create_summary_dataframe function using the loaded dataframes
    summary_df, compound_to_code = create_summary_dataframe(dataframes)
    
    # Print the summary dataframe to check the results
    print("Summary DataFrame:")
    print(summary_df)

    print("Compounds to code:")
    print(compound_to_code)

    # Example usage with a DataFrame, `df`:
    tsn_normalized_df = tsn_normalization(summary_df)
    mn_normalized_df = mn_normalization(summary_df)
    coda_normalized_df = coda_normalization(summary_df)
    pqn_normalized_df = pqn_normalization(summary_df)

    p_values_df = calculate_p_values(tsn_normalized_df)
    print(p_values_df)
    plot_p_values(p_values_df, th=0.1)

    print("TSN Normalized DataFrame:", tsn_normalized_df)
    print("MN Normalized DataFrame:", mn_normalized_df)
    print("CODA Normalized DataFrame:", coda_normalized_df)
    print("PQN Normalized DataFrame:", pqn_normalized_df)

    pca_results = perform_pca(tsn_normalized_df)  # PCA analysis and plot with sample names
    perform_hca(tsn_normalized_df)                # HCA dendrogram plot
    corr_matrix = plot_correlation_matrix_samples(tsn_normalized_df)  # Correlation matrix heatmap

    converted_df = convert(coda_normalized_df)
    print("converted dataframe: ", converted_df)

    plot_hca(converted_df)
    plot_pca(converted_df)
    plot_correlation_matrix(converted_df)

    plot_volcano(p_values_df)
    pls_da_plot(tsn_normalized_df)
    investigate(tsn_normalized_df, 5)
    rf_features(tsn_normalized_df)
    generate_heatmap(tsn_normalized_df)
    plot_violin(tsn_normalized_df, ['c1', 'c2', 'c3'])
    plot_grp_avg(tsn_normalized_df, ['c1', 'c2', 'c3'])
    plot_density(tsn_normalized_df, ['c1', 'c2', 'c3'])
    
except (FileNotFoundError, ValueError) as e:
    print(f"Error: {e}")




