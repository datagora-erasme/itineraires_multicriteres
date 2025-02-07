import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import random
import pandas as pd
import multiprocessing as mp
import numpy as np
from function_utils import *
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering

def pca_pipeline(data, features, n, scale=True):
    """
    Perform principal component analysis (PCA) on the specified data.
    
    Args:
        data (DataFrame): The DataFrame containing the data.
        features (list): List of column names to be used for PCA.
        n (int): The number of principal components to compute.
        scale (bool, optional): If True, the data will be standardized before PCA. Default is True.
    
    Returns:
        pca: The PCA object fitted to the data.
    """
    sample = data[features]
    if(scale):
        scaler = StandardScaler()
        sample_scaled = scaler.fit_transform(sample)
        sample_scaled = pd.DataFrame(data=sample_scaled, columns=sample.columns)
        sample = sample_scaled

    pca = PCA(n_components=n)
    pca.fit(sample)
    return pca

def eigein_values(pca, plot=False):
    """
    Calculate and display the eigenvalues and explained variance from the PCA.

    Args:
        pca (PCA): The PCA object that contains the results of the PCA.
        plot (bool, optional): If True, a bar plot of the explained variance is shown. Default is False.

    Returns:
        pd.DataFrame: A DataFrame containing the dimensions, explained variance, and cumulative explained variance.
    """
    eig = pd.DataFrame(
        {
            "Dimension" : ["Dim" + str(x + 1) for x in range(len(pca.explained_variance_))], 
            "Variance expliquée" : pca.explained_variance_,
            "% variance expliquée" : np.round(pca.explained_variance_ratio_ * 100),
            "% cum. var. expliquée" : np.round(np.cumsum(pca.explained_variance_ratio_) * 100)
        }
    )

    if(plot):
        eig.plot.bar(x = "Dimension", y = "% variance expliquée") # permet un diagramme en barres
        plt.text(5, 18, "17%") # ajout de texte
        plt.axhline(y = 17, linewidth = .5, color = "dimgray", linestyle = "--") # ligne 17 = 100 / 6 (nb dimensions)
        plt.show()

    print(eig)
    return eig

def coord_pca(data, pca):
    """
    Transform the data into the principal component space using the PCA model.

    Args:
        data (pd.DataFrame or np.ndarray): The data to be transformed, typically with the same features used for the PCA.
        pca (PCA): The PCA object that has been fit to the data.

    Returns:
        np.ndarray: The transformed data in the principal component space.
    """
    return pca.transform(data)

def plot_ind_pca(data, pca, nbre_dim=2, method="plotly", dim=[1, 2]):
    """
    Visualize the results of PCA by plotting the individual data points in the principal component space.

    Args:
        data (pd.DataFrame or np.ndarray): The data to be plotted, typically after performing PCA.
        pca (PCA): The PCA object that has been fit to the data.
        nbre_dim (int, optional): The number of dimensions to plot. Default is 2.
        method (str, optional): The method to use for plotting. Options are "plotly" for an interactive plot or 
                                "raw_plt" for a static plot. Default is "plotly".
        dim (list of int, optional): The dimensions to plot when using the "raw_plt" method. Default is [1, 2].

    Returns:
        None: Displays the PCA plot.
    """
    coord = coord_pca(data, pca)[:,0:nbre_dim]
    if(method == "plotly"):
        labels = {
            str(i): f"PC {i+1} ({var:.1f}%)"
            for i, var in enumerate(pca.explained_variance_ratio_[:nbre_dim] * 100)
        }

        fig = px.scatter_matrix(
            coord,
            labels=labels,
            dimensions=range(nbre_dim),
        )
        fig.update_traces(diagonal_visible=False)
        fig.show()
    
    elif(method == "raw_plt"):
        coord_df = pd.DataFrame({
            f"Dim{dim[0]}" : coord[:, dim[0]-1],
            f"Dim{dim[1]}": coord[:, dim[1]-1]
        })
        coord_df.plot.scatter(f"Dim{dim[0]}", f"Dim{dim[1]}")
        plt.xlabel(f"Dimension {dim[0]} {round(pca.explained_variance_ratio_[dim[0]-1]*100,2)}%")
        plt.ylabel(f"Dimension {dim[1]} {round(pca.explained_variance_ratio_[dim[1]-1]*100,2)}%")
        plt.show()
            

def coord_var_pca(data, pca, dim=[1, 2]):
    """
    Compute the coordinates of the variables in the PCA space, based on the principal components and their explained variance.

    Args:
        data (pd.DataFrame): The original dataset used for PCA.
        pca (PCA): The PCA object that has been fit to the data.
        dim (list of int, optional): The dimensions (principal components) to use for the correlation plot. Default is [1, 2].

    Returns:
        pd.DataFrame: A DataFrame containing the coordinates of the variables (features) on the selected principal components.
    """
    n = data.shape[0]
    p = data.shape[1]
    eigval = (n-1)/n * pca.explained_variance_
    sqrt_eigval = np.sqrt(eigval)
    corvar = np.zeros((p,p))
    for k in range(p):
        corvar[:,k] = pca.components_[k,:] * sqrt_eigval[k]
    
    coordvar = pd.DataFrame({"id": data.columns, "COR_1": corvar[:,dim[0]-1], "COR_2": corvar[:,dim[1]-1]})

    return coordvar

def plot_var_circle(coordvar):
    """
    Plot a correlation circle for the variables in PCA.

    Args:
        coordvar (pd.DataFrame): A DataFrame containing the coordinates of the variables (features) in the PCA space. 
                                  The DataFrame should have columns 'id', 'COR_1', and 'COR_2' for the variable names and their coordinates.

    This function generates a correlation circle plot that shows the contribution of each variable to the first two principal components (PC1 and PC2).
    It visualizes the relationship between variables using arrows and labels, and plots a circle of radius 1 to represent the correlation limits.
    """
    # Création d'une figure vide (avec des axes entre -1 et 1 + le titre)
    fig, axes = plt.subplots(figsize = (6,6))
    fig.suptitle("Cercle des corrélations")
    axes.set_xlim(-1, 1)
    axes.set_ylim(-1, 1)
    # Ajout des axes
    axes.axvline(x = 0, color = 'lightgray', linestyle = '--', linewidth = 1)
    axes.axhline(y = 0, color = 'lightgray', linestyle = '--', linewidth = 1)
    # Ajout des noms des variables
    for j in range(coordvar.shape[0]):
        axes.text(coordvar["COR_1"][j]+0.05,coordvar["COR_2"][j]+0.05, f"{coordvar['id'][j]} ({round(coordvar['COR_1'][j], 2)}, {round(coordvar['COR_2'][j], 2)})")
        axes.arrow(0,0,
                 coordvar["COR_1"][j],
                 coordvar["COR_2"][j],
                 lw = 2, # line width
                 length_includes_head=True, 
                 head_width=0.05,
                 head_length=0.05
                  )
    # Ajout du cercle
    plt.gca().add_artist(plt.Circle((0,0),1,color='blue',fill=False))

    plt.show()

def hclust_on_acp(data, pca):
    """
    Perform hierarchical clustering on PCA-transformed data.

    Args:
        data (pd.DataFrame or np.ndarray): The data to be clustered. It should contain the features to be used in PCA.
        pca (PCA object): The PCA model that has been fitted to the data.

    Returns:
        AgglomerativeClustering: The fitted AgglomerativeClustering object, containing the clustering result.
    
    This function applies PCA transformation to the input data and then performs hierarchical clustering (agglomerative) on the transformed data.
    The clustering is performed without predefining the number of clusters (i.e., the `n_clusters` parameter is set to `None`).
    The distance threshold is set to 0, so the algorithm will consider all points and merge them based on the hierarchical structure of the data.
    """
    hac = AgglomerativeClustering(distance_threshold=0, n_clusters=None)
    pca_data = pca.transform(data)

    return(hac.fit(pca_data))

