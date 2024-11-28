import os

os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
import numpy as np
from data_utils import *
from sklearn.preprocessing import MinMaxScaler
import sys
sys.path.append("../")
from global_variable import *


###### BRUIT PREPROCESSING ######
"""Données Ohrane"""

### FUNCTION ###

def weighted_bruit_average(x):
    return pd.Series({
        "DN_wavg": round(np.average(x["DN"], weights=x["area"]), 2)
        })

# Demander si on souhaite mettre à jour la taille du fichier bruit
choice = input("""Souhaitez-vous mettre à jour taille du fichier bruit ? (OUI) ou (NON) \n""")
if choice == "OUI":
    cut_bruit(bruit_path, empreinte_path, sortie_path)





# Demander si on souhaite mettre à jour le bruit moyen par segment
choice = input("""Souhaitez-vous mettre à jour le bruit moyen par segment ? (OUI) ou (NON) \n
# ATTENTION, le temps de calcul estimé est de ~2h
#""")

# Si l'utilisateur souhaite mettre à jour le bruit moyen par segment
if choice == "OUI":
    print("Calculate noise weighted average ")
    try:
        calculate_weighted_average(edges_buffer_path, bruit_path, edges_buffer_bruit_wavg_path, "edges", "DN", weighted_bruit_average)
        print("read file")
        bruit_edges = gpd.read_file(edges_buffer_bruit_wavg_path, layer="edges")
        
        print("fill na and zeros")
        bruit_edges["DN_wavg"] = bruit_edges["DN_wavg"].fillna(0.01)
        bruit_edges["DN_wavg"] = bruit_edges["DN_wavg"].replace(0, 0.01)
        bruit_edges["DN_wavg"] = bruit_edges["DN_wavg"] * 10
        
        print("scale noise")
        scaler = MinMaxScaler(feature_range=(0, 1))  # à modifier si nécessaire
        bruit_edges["DN_wavg_scaled"] = scaler.fit_transform(bruit_edges[["DN_wavg"]])
        
        print(bruit_edges.columns)
        
        print("to file")
        bruit_edges.to_file(edges_buffer_bruit_wavg_path_no_na, layer="edges")
        
    except Exception as e:
        print(f"Erreur lors du traitement du bruit : {e}")
