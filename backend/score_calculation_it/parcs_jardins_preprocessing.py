import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import os
from data_utils import *
import sys
sys.path.append("../")
from global_variable import *

###### CREATE WORKING DIRECTORY FOR PARCS ET JARDINS ######
create_folder("./output_data/parcs/")

###### PARCS ET JARDINS PREPROCESSING ######
"""Données issue des parcs et jardins avec indice de canopée"""

parcs_classes_path = "./output_data/parcs/parcs_canop_classes.gpkg"

choice = input("""
    Souhaitez-vous mettre à jour le réseau pondéré par les parcs ? OUI ou NON
""")
if(choice=="OUI"):
    print("Create parcs classes") 

    parcs = gpd.read_file(data_params["parcs_canop"]["gpkg_path"])

    parcs["indiccanop"] = parcs["indiccanop"].str.replace(",", ".").astype(float)

    parcs["class"] = parcs["indiccanop"].apply(lambda x: "low" if x<0.34 else("medium" if x>=0.34 and x<0.63 else "high"))

    parcs.to_file(parcs_classes_path, driver="GPKG", layer="parcs")

    calculate_area_proportion(edges_buffer_path, parcs_classes_path, "parcs", edges_buffer_parcs_prop_path,layer="edges", parcs=True)

    network_parcs = gpd.read_file(edges_buffer_parcs_prop_path)

    print("network_parcs.columns : ", network_parcs.columns)

    network_parcs = network_parcs.set_index(["u", "v", "key"])  

    network_parcs["parcs_class"] = network_parcs.apply(lambda x: x["parcs_class"] if (x["parcs_prop"] > 0.5) else "low", axis=1)

    network_parcs["canop"] = network_parcs["canop"].fillna(0)

    network_parcs.to_file(edges_buffer_parcs_prop_path, driver="GPKG", layer="edges")