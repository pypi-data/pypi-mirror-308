import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.preprocessing import StandardScaler

def perform_hca(data):
    """
    Perform hierarchical clustering on the given data and plot a dendrogram.
    
    Parameters:
    data (pd.DataFrame): DataFrame with the first column as sample names and
                         the remaining columns as features.
    """
    # Separate features
    features = data.iloc[:, 1:]
    
    # Standardize the data
    scaler = StandardScaler()
    features_std = scaler.fit_transform(features)
    
    # Compute the linkage matrix for HCA
    linkage_matrix = linkage(features_std, method='ward')
    
    # Plot the dendrogram
    plt.figure(figsize=(10, 7))
    dendrogram(linkage_matrix, labels=data['sample'].values, leaf_rotation=90, leaf_font_size=10)
    plt.title("Hierarchical Clustering Dendrogram")
    plt.xlabel("Sample")
    plt.ylabel("Distance")
    plt.show()
