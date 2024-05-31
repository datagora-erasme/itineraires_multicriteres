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

###### CREATE WORKING DIRECTORY FOR TEMPERATURE ######

###### TEMPERATURE PREPROCESSING ######
"""Données issue de calcul QGIS pour estimer la T° de surface à partir d'une capture Landsat"""

### FUNCTION ###

def weighted_temp_average(x):
    return pd.Series({
        "C_wavg": round(np.average(x["C"], weights=x["area"]), 2)
        })
    
choice = input("""Souhaitez-vous mettre à jour la température moyenne par segment ? (OUI) ou (NON) \n
    ATTENTION, le temps de calcul estimé est de ~2h
""")

if(choice == "OUI"):
    print("Calculate Temperature weighted average ")
    calculate_weighted_average(edges_buffer_path, temperature_path, edges_buffer_temp_wavg_path, "edges", "C", weighted_temp_average)

    print("read file")
    temp_edges = gpd.read_file(edges_buffer_temp_wavg_path, layer="edges")

    print("fill na")
    temp_edges["C_wavg"] = temp_edges["C_wavg"].fillna(33)

    print("scale temp")

    scaler = MinMaxScaler(feature_range=(0, 1))

    temp_edges["C_wavg_scaled"] = scaler.fit_transform(temp_edges[["C_wavg"]])

    print(temp_edges.columns)


    print("to file")
    temp_edges.to_file(edges_buffer_temp_wavg_path_no_na, layer="edges")