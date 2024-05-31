import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import random
import pandas as pd
import multiprocessing as mp
import numpy as np

from data_utils import *

import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering

def pca_pipeline(data, features, n, scale=True):
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
    return pca.transform(data)

def plot_ind_pca(data, pca, nbre_dim=2, method="plotly", dim=[1, 2]):
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
            

def coord_var_pca(data, pca, dim=[1,2]):
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
    hac = AgglomerativeClustering(distance_threshold=0, n_clusters=None)
    pca_data = pca.transform(data)

    return(hac.fit(pca_data))

