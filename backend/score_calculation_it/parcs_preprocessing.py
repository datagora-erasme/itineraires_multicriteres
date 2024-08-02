import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
from shapely.wkt import dumps, loads
from data_utils import *
import sys
sys.path.append("../")
from global_variable import *

###### CREATE WORKING DIRECTORY FOR PARCS ######

create_folder("./output_data/parcs/")

###### PARCS PREPROCESSING ######

parcs_classes_path = "./output_data/parcs/parcs_classes.gpkg"

choice = input("Souhaitez-vous mettre à jour le réseau pondéré par les parcs ? OUI ou NON\n")
if choice.upper() == "OUI":
    print("Création des classes de parcs")

    parcs = gpd.read_file(data_params["parcs"]["gpkg_path"])
    parcs["geometry"] = parcs.geometry.buffer(15)
    parcs.to_file(parcs_classes_path, driver="GPKG", layer="parcs")

    def calculate_parc_proportion(edges_path, parcs_path, output_path, layer="edges"):
        edges = gpd.read_file(edges_path, layer=layer)
        parcs = gpd.read_file(parcs_path)

        #simplify geometries to reduce errors
        edges.geometry = [loads(dumps(geom, rounding_precision=5)) for geom in edges.geometry]
        parcs.geometry = [loads(dumps(geom, rounding_precision=5)) for geom in parcs.geometry]

        #check for intersections between edges and parks
        edges["parcs_prop"] = edges.intersects(parcs.unary_union).astype(int)

        edges.reset_index().to_file(output_path, driver="GPKG", layer=layer)

    calculate_parc_proportion(edges_buffer_path, parcs_classes_path, edges_buffer_parcs_pollen_prop_path)

    network_parcs = gpd.read_file(edges_buffer_parcs_pollen_prop_path)
    network_parcs = network_parcs.set_index(["u", "v", "key"])

    #distribution de la proportion de parcs
    print("Distribution de 'parcs_prop':\n", network_parcs["parcs_prop"].describe())
    #nombre d'edges qui sont dans un parc, c'est à dire qui ont une proportion de parcs égale à 1
    print("Nombre d'edges dans un parc:", network_parcs[network_parcs["parcs_prop"] == 1].shape[0])

    network_parcs.reset_index().to_file(edges_buffer_parcs_pollen_prop_path, driver="GPKG", layer="edges")
