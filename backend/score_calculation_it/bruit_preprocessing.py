import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
import numpy as np
import os
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
    
choice = input("""Souhaitez-vous mettre à jour le bruit moyen par segment ? (OUI) ou (NON) \n
    ATTENTION, le temps de calcul estimé est de ~2h
""")

if(choice == "OUI"):
    print("Calculate noise weighted average ")
    calculate_weighted_average(edges_buffer_path, bruit_path, edges_buffer_bruit_wavg_path, "edges", "DN", weighted_bruit_average)

    print("read file")
    bruit_edges = gpd.read_file(edges_buffer_bruit_wavg_path, layer="edges")

    print("fill na and zeros")
    bruit_edges["DN_wavg"] = bruit_edges["DN_wavg"].fillna(0.01)
    bruit_edges["DN_wavg"] = bruit_edges["DN_wavg"].replace(0, 0.01)

    print("scale noise")

    scaler = MinMaxScaler(feature_range=(0, 1)) #à modifier ?

    bruit_edges["DN_wavg_scaled"] = scaler.fit_transform(bruit_edges[["DN_wavg"]])

    print(bruit_edges.columns)


    print("to file")
    bruit_edges.to_file(edges_buffer_bruit_wavg_path_no_na, layer="edges")