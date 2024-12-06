import seaborn as sns
import matplotlib.pyplot as plt

def plot_density(df, compounds):
    """
    Plots the density of selected compound intensities across samples.
    
    Parameters:
        df (DataFrame): DataFrame containing the sample intensities.
        compounds (list): List of compound codes to include in the density plot.
    
    Returns:
        None: Displays the density plot.
    """
    # Melt the data to plot density for each compound across samples
    melted_df = df.melt(id_vars='sample', value_vars=compounds, var_name='Compound', value_name='Intensity')
    
    # Create the density plot
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=melted_df, x='Intensity', hue='Compound', fill=True, common_norm=False, palette='muted')
    plt.title('Density Plot of Selected Compound Intensities')
    plt.xlabel('Intensity')
    plt.ylabel('Density')
    plt.tight_layout()
    plt.show()

# Example usage:
# plot_density(coda_df, ['c1', 'c8', 'c6', 'c3'])
