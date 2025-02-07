import sys
import os
sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../script_python")
os.environ['USE_PYGEOS'] = '0'
from backend.script_python.function_utils import create_folder
import geopandas as gpd
import pandas as pd
from shapely.wkt import dumps, loads
from function_utils import *
from global_variable import *

###### CREATE WORKING DIRECTORY FOR PARCS ######

create_folder("./output_data/parcs/")

###### PARCS PREPROCESSING ######

parcs_classes_path = "./output_data/parcs/parcs_classes.gpkg"

choice = input("Do you want to update the weighted network by parks? YES or NO\n")
if choice.upper() == "YES":
    print("Creating park classes")

    parcs = gpd.read_file(data_params["parcs"]["gpkg_path"])
    parcs["geometry"] = parcs.geometry.buffer(15)
    parcs.to_file(parcs_classes_path, driver="GPKG", layer="parcs")

    def calculate_parc_proportion(edges_path, parcs_path, output_path, layer="edges"):
        """
    Calculates the proportion of each edge that intersects with parks and assigns a score to each edge 
    based on the intersection. The score is multiplied by 5 for the edges that intersect with parks.

    Args:
        edges_path (str): The file path to the edges data (GeoPackage file).
        parcs_path (str): The file path to the parks data (GeoPackage file).
        output_path (str): The file path where the updated edges data will be saved.
        layer (str, optional): The name of the layer in the GeoPackage for the edges data. Defaults to "edges".

    Returns:
        None: The function updates the edges file with the park proportion score.
    """
        edges = gpd.read_file(edges_path, layer=layer)  
        parcs = gpd.read_file(parcs_path)

    # Simplifies the geometries to avoid memory errors
        edges.geometry = [loads(dumps(geom, rounding_precision=5)) for geom in edges.geometry]
        parcs.geometry = [loads(dumps(geom, rounding_precision=5)) for geom in parcs.geometry]

    # Checks the intersections between the edges and the parks
        edges["parcs_prop"] = edges.intersects(parcs.unary_union).astype(int)
        edges["parcs_prop"] = edges["parcs_prop"] * 5

        edges.reset_index().to_file(output_path, driver="GPKG", layer=layer)


    calculate_parc_proportion(edges_buffer_path, parcs_classes_path, edges_buffer_parcs_pollen_prop_path)

    network_parcs = gpd.read_file(edges_buffer_parcs_pollen_prop_path)
    network_parcs = network_parcs.set_index(["u", "v", "key"])

    print("Distribution de 'parcs_prop':\n", network_parcs["parcs_prop"].describe())
    # Number of edges that are within a park, meaning they have a park proportion equal to 5
    print("Nombre d'edges dans un parc:", network_parcs[network_parcs["parcs_prop"] == 5].shape[0])

    network_parcs.reset_index().to_file(edges_buffer_parcs_pollen_prop_path, driver="GPKG", layer="edges")
