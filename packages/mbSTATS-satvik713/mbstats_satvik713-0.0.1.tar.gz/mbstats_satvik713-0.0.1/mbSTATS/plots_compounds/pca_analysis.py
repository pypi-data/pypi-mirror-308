import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd 

def plot_pca(df):
    """
    This function performs PCA on the provided DataFrame and plots the results with compound labels.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame containing compounds as rows and samples as columns.
    """
    # Drop 'Compounds' column for PCA
    X = df.drop(columns=['Compounds'])
    X_std = StandardScaler().fit_transform(X)

    # Perform PCA
    pca = PCA(n_components=2)
    pca_components = pca.fit_transform(X_std)

    # Create a DataFrame for PCA results
    pca_df = pd.DataFrame(pca_components, columns=['PC1', 'PC2'])
    pca_df['Compound'] = df['Compounds']

    # Plot the PCA results with compound labels
    plt.figure(figsize=(10, 8))
    plt.scatter(pca_df['PC1'], pca_df['PC2'], color='b', s=100)

    # Annotate each point with the compound name
    for i in range(pca_df.shape[0]):
        plt.text(pca_df['PC1'][i] + 0.05, pca_df['PC2'][i], pca_df['Compound'][i], fontsize=12)

    # Plot settings
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('PCA Plot of Compounds')
    plt.grid(True)
    plt.show()
