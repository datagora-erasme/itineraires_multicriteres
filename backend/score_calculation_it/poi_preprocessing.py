import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import random
import pandas as pd
import multiprocessing as mp
import numpy as np
from shapely.wkt import loads, dumps
import os
import time
from data_utils import *
import sys
sys.path.append("../")
from global_variable import *
###### POI PREPROCESSING ######

"""POIs are not currently taken into account in graph weighting. 
However, the following file can be used to generate networks with the presence or absence of a POI on a segment. """

### CREATE WORKING DIRECTORIES ###
create_folder("./output_data/toilettes/")
create_folder("./output_data/fontaines/")
create_folder("./output_data/bancs/")

### FUNCTION ###
def presency(x):
    x_class = x["class"].unique().tolist()
    first_non_one = next((True for val in x_class if val != 1), False)

    return pd.Series({
        "class": first_non_one
    })

poiId = ["fontaines_potables", "fontaines_ornementales", "toilettes", "bancs"]

choice = input(f""" Choisissez parmi la liste suivante l'identifiant de la donnée que vous souhaitez mettre à jour : \n
{poiId} \n
ou entrer ALL pour tout mettre à jour
""")
               
if(choice == "ALL"):
    for id in poiId:
        print(f"Starting calculation for {id}")
        print("Reading file ...")
        data = gpd.read_file(data_params[id]["gpkg_path"])
        data["class"] = id
        data.to_file(data_params[id]["gpkg_path"], driver="GPKG", layer=id)
        print("Bufferizing ...")
        bufferize(data_params[id]["gpkg_path"], data_params[id]["buffer_path"], id, data_params[id]["buffer_size"])
        print("Calculate Presency ...")
        calculate_presency(edges_buffer_path, data_params[id]["buffer_path"], data_params[id]["edges_path"], "edges", id, presency)
elif(choice in poiId):
    print("Reading file ...")
    data = gpd.read_file(data_params[choice]["gpkg_path"])
    data["class"] = choice
    data.to_file(data_params[choice]["gpkg_path"], driver="GPKG", layer=choice)
    print("Bufferizing ... ")
    bufferize(data_params[choice]["gpkg_path"], data_params[choice]["buffer_path"], choice, data_params[choice]["buffer_size"])
    print("Calculating Presency ...")
    calculate_presency(edges_buffer_path, data_params[choice]["buffer_path"], data_params[choice]["edges_path"], "edges", choice, presency)
else:
    print("Veuillez entrer un identifiant valide")