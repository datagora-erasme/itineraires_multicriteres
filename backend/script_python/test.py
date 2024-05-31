# Fichier de test : remove pour la prod

# tests sur la standardization des valeurs de fraîcheurs pour le network

import os
os.environ['USE_PYGEOS'] = '0'
import osmnx as ox
import networkx as nx

import shapely.geometry as geom
import geopandas as gpd

from data_utils import create_folder

import numpy as np
import pandas as pd

import time

import json


start_time = time.time()

data_informations_path = "./data/data_informations.json"

# data_folder_path = "./data/osm/lyon_walk_simplified.gpkg"

default_ntf = "./data/osm/lyon_walk_simplified.gpkg"

# weighted_ntf = "./backend/data/osm/joined_temp_road_veget.gpkg"

# cf = "./backend/script_python/data/raw_data/joined_if_3946.gpkg"

# op = "./backend/data/osm/test_sd.gpkg"

# g = "./backend/data/osm/test_weighted.gpkg"

# edge_veget = "./backend/data/osm/joined_edges_veget.gpkg"

# veget = "./backend/script_python/data/raw_data/vegetation_stratifie.gpkg"

temp = "./script_python/data/raw_data/temp_surface.gpkg"

temp_w = "./script_python/data/raw_data/network_temp_test.gpkg"

c_IF = "./script_python/data/raw_data/temp_IF.gpkg"

# edge_temp = "./backend/data/osm/joined_temp_edges.gpkg"

def split_network_edges(network_path, output_path):
    # Read in the osm network GeoDataFrame
    edges_network = gpd.read_file(network_path, layer="edges")

    # Create a new empty GeoDataFrame to store the subedges
    subedges = gpd.GeoDataFrame()

    # Loop over each edge in the osm network
    for index, row in edges_network.iterrows():
        # Get the geometry of the edge as a LineString
        edge_geom = row.geometry

        # Divide the edge into subsegments of approximately 1 meter
        subsegments = list(edge_geom.interpolate(n, normalized=True) for n in range(1, int(edge_geom.length)))

        # Create a new GeoDataFrame with the subsegments and copy over the attributes from the original edge
        subedges = subedges.append(gpd.GeoDataFrame({'id': [row.id]*len(subsegments),
                                                    'attribute1': [row.attribute1]*len(subsegments),
                                                    'attribute2': [row.attribute2]*len(subsegments),
                                                    'geometry': subsegments}))

    # Reset the index of the subedges GeoDataFrame
    subedges = subedges.reset_index(drop=True)

    subedges.to_file(output_path, driver="GPKG")

def calculate_IF(input_path, output_path, fn, name):
    """Function to recalculate IF according to other attributes
    fn is the function to apply
    """
    data = gpd.read_file(input_path)

    data[f"IF_{name}"] = data.apply(fn, axis=1)

    data.to_file(output_path, driver="GPKG")

def temp_IF(row):
    """Return value of IF for temperature data"""
    if(row["C"] < 25):
        return 0
    elif(25 <= row["C"] < 30):
        return 0.25
    elif(30 <= row["C"] < 35):
        return 0.5
    elif(35 <= row["C"] < 40):
        return 0.75
    else:
        return 1
    
# def null_IF(row, column_name, value):
#     """Replace null by value IF """
#     if(row[column_name] == None):
#         return value
#     else: 
#         return row[column_name]
    
#calculate_IF(temp, c_IF, temp_IF, "temp_surface_road_raw")

# with open(data_informations_path, "r") as f:
#     data_informations = json.load(f)

# data_informations["data_raw"]["temp_surface_road_raw"]["weighted_network_path"] = c_IF

# with open(data_informations_path, "w") as f:
#     json.dump(data_informations, f, indent=4)


def network_weighted_average(default_network, weighted_edges, layer_name, output_path):
    """This function calculate the weighted average for one attribute of one edge
    for the OSM network.

    For example, if for one segment we have 3 kind of vegetation, we want to calculate 
    the weighted average of the vegetation for this segment 
    """

    default_edges = gpd.read_file(default_network, layer="edges")

    default_nodes = gpd.read_file(default_network, layer="nodes")

    # For some reason pandas convert u, v and key into float for weighted_edges
    weighted_edges[["u", "v", "key"]] = weighted_edges[["u", "v", "key"]].astype(int)

    print(f"Calculating weighted average for {layer_name} ...")

    # Due to intersection, there more features into the weighted_edges dataframe than the default_network one
    #The following line allows to recalculate the weighted average for one edge taking account all the "subedges"
    grouped_edges = weighted_edges.groupby(["u", "v", "key"], group_keys=True).apply(lambda x: pd.Series({
        f"IF_{layer_name}": np.average(x[f"IF_{layer_name}"], weights=x["cal_length"])
    })).reset_index()

    grouped_edges = grouped_edges.set_index(["u", "v", "key"])
    default_edges = default_edges.set_index(["u", "v", "key"])

    default_edges[f"IF_{layer_name}"] = grouped_edges[f"IF_{layer_name}"]

    default_nodes = default_nodes.set_index(['osmid'])

    G = ox.graph_from_gdfs(default_nodes, default_edges)

    print(f"Done. \nSaving file into {output_path}")

    ox.save_graph_geopackage(G, filepath=output_path)


def join_network_layer(network_path, layer_path, layer_name, output_path):
    """This function join a network with a specific layer"""
    network_edges = gpd.read_file(network_path, layer="edges")

    layer = gpd.read_file(layer_path)

    layer = layer.to_crs(network_edges.crs)

    print(f"Joining {layer_name} with osm network")

    joined_edges = gpd.overlay(network_edges, layer, how="intersection", keep_geom_type=True)

    # Convert into geoserie in order to calculate the length of the intersection

    joined_edges_serie = gpd.GeoSeries(joined_edges["geometry"])

    joined_edges_serie = joined_edges_serie.to_crs(32631)

    joined_edges["cal_length"] = joined_edges_serie.length

    joined_edges.to_file("./data/osm/joined_edges_temp.gpkg", driver="GPKG")

    network_weighted_average(default_ntf, joined_edges, layer_name, output_path)

#join_network_layer(default_ntf, c_IF, "temp_surface_road_raw", temp_w)

def create_all_weighted_network(default_ntf):
    """Create a weighted network for each kind of data"""
    with open(data_informations_path, "r") as f:
        data_informations = json.load(f)
    
    ## WFS
    data_wfs = data_informations["data_wfs"]

    for d_name, d_info in data_wfs.items():
        output_path = f"./data/osm/network_{d_name}_weighted.gpkg"
        join_network_layer(default_ntf, d_info["buffered_path"], d_name, output_path)
        data_informations["data_wfs"][d_name]["weighted_network_path"] = output_path

    ## RAW
    temp = data_informations["data_raw"]["temp_surface_road_raw"]
    path = temp["recalculated_if_path"]
    temp_output_path = "./data/osm/network_temp_surface_road_raw_weighted.gpkg"
    join_network_layer(default_ntf, path, "temp_surface_road_raw", temp_output_path)
    data_informations["data_raw"]["temp_surface_road_raw"]["weighted_network_path"] = temp_output_path

    with open(data_informations_path, "w") as f:
        json.dump(data_informations, f, indent=4)

#create_all_weighted_network(default_ntf)

def merge_networks(default_network, output_path):
    """Merge all network together"""
    final_network = gpd.read_file(default_network, layer="edges")
    final_network_nodes = gpd.read_file(default_network, layer="nodes")
    final_network["IF"] = 0

    with open(data_informations_path, "r") as f:
        data_informations = json.load(f)

    count = 0
    
    # WFS
    data_wfs = data_informations["data_wfs"]
    for d_name, d_info in data_wfs.items():
        count+=1
        network_path = d_info["weighted_network_path"]
        network = gpd.read_file(network_path, layer="edges")
        network[f"IF_{d_name}"] = network[f"IF_{d_name}"].fillna(0)
        final_network["IF"] = final_network["IF"] + network[f"IF_{d_name}"]
        final_network[f"IF_{d_name}"] = network[f"IF_{d_name}"]

    # RAW
    data_raw = data_informations["data_raw"]
    for d_name, d_info in data_raw.items():
        if(d_name == "temp_surface_road_raw"):
            count+=1
            network_path = d_info["weighted_network_path"]
            network = gpd.read_file(network_path, layer="edges")
            network[f"IF_{d_name}"] = network[f"IF_{d_name}"].fillna(0)
            final_network["IF"] = final_network["IF"] + network[f"IF_{d_name}"]
            final_network[f"IF_{d_name}"] = network[f"IF_{d_name}"]
    
    final_network["IF"] = final_network["IF"] / count

    final_network = final_network.set_index(["u", "v", "key"])
    final_network_nodes = final_network_nodes.set_index(["osmid"])

    G = ox.graph_from_gdfs(final_network_nodes, final_network)

    ox.save_graph_geopackage(G, filepath=output_path)

# merge_networks(default_ntf, "./data/osm/final_network.gpkg")


end_time = time.time()

execution_time = (end_time - start_time)/60
print(f"Temps d'exécution : {execution_time}")