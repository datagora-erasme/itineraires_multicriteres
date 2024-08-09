#%%
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
import osmnx as ox
from data_utils import *
import sys
sys.path.append("../")
from global_variable import *

#%%
sys.path.append("../")
from global_variable import *

###### NETWORK SCORE CALCULATION #######
create_folder("./output_data/network/graph/")

edges_buffer_path = globpath("./score_calculation_it/input_data/network/edges_buffered_12_bounding.gpkg")

### GLOBAL VARIABLES ###
score_columns_tourisme = ["score_tourisme_count"]

### FUNCTIONS ###

def create_uniqID(x):
    """OSMNX invert some u and v when creating graph => create uniqId in order to make the analyse"""
    return str(x["u"])+str(x["v"])+str(x["key"])

def all_prop(input_path, params, output_path):
    """create one file with all props"""
    edges = gpd.read_file(input_path, layer="edges")
    edges["uniqId"] = edges.apply(create_uniqID, axis=1)
    edges = edges.set_index(["u", "v", "key"])
    for dataname, dataprops in params.items():
        data = gpd.read_file(dataprops["edges_path"])
        data = data.set_index(["u", "v", "key"])
        edges[dataname] = data[dataname]
    edges.to_file(output_path, layer="edges", driver="GPKG")
    
def total_score(input_path, output_path, score_columns):
    
    edges = gpd.read_file(input_path, layer="edges")
    print(edges.columns)
    edges[score_columns] = edges[score_columns].apply(pd.to_numeric, errors='coerce')
    edges["total_score_tourisme"] = edges[score_columns].sum(axis=1)

    max_score = edges["total_score_tourisme"].max()
    min_score = edges["total_score_tourisme"].min()
    edges["total_score_tourisme"] = -edges["total_score_tourisme"] + (max_score + min_score)
    print(edges["total_score_tourisme"].describe())

        
    edges.to_file(output_path, driver="GPKG")

def all_score_edges(input_path, output_path, params):
    default_edges = gpd.read_file(input_path, layer="edges")
    
    for data_name, data_param in params.items():
        print(f"Score {data_name}")
        data = gpd.read_file(data_param["edges_path"])
        default_edges[f"score_tourisme_{data_name}"] = data[data_name].apply(data_param["fn_cont"])

    default_edges.to_file(output_path, driver="GPKG", layer="edges")

def one_score_edges(input_path, output_path, params, key):
    """(Re)-calculate score for one data"""
    default_edges = gpd.read_file(input_path, layer="edges")
    data = gpd.read_file(params[key]["edges_path"])
    default_edges[f"score_tourisme_{key}"] = data[key].apply(params[key]["fn_cont"])

    default_edges.to_file(output_path, driver="GPKG")

def score_distance(input_path, output_path):
    """calculate the score by distance for each edge"""
    edges = gpd.read_file(input_path)
    
    edges["total_score_tourisme"] = pd.to_numeric(edges["total_score_tourisme"], errors='coerce')
    edges["length"] = pd.to_numeric(edges["length"], errors='coerce')

    edges["score_distance_tourisme"] = round(edges["total_score_tourisme"] * (edges["length"]*2), 2) 
    edges["score_distance_tourisme"] = edges["score_distance_tourisme"].replace(0, 0.1)
     #print(edges["score_distance_tourisme"].describe())

    edges.to_file(output_path, driver="GPKG")

def score_tourisme(input_path, output_path):
    """Score from 0 to 10"""
    edges = gpd.read_file(input_path)
    
    edges["total_score_tourisme"] = pd.to_numeric(edges["total_score_tourisme"], errors='coerce')
    
    min_score = edges["total_score_tourisme"].min()
    max_score = edges["total_score_tourisme"].max()
    slope = (0-10)/(max_score-min_score)
    origin_ordinate = 10-slope*min_score
    edges["tourisme_score"] = edges["total_score_tourisme"].apply(lambda x: round(slope*x+origin_ordinate, 2))
    #edges["tourisme_score"] = edges["tourisme_score"].apply(lambda x: 1-(x/10))
    #edges["tourisme_score"] = edges["tourisme_score"].apply(lambda x: x*10)
    print(edges["tourisme_score"].describe())
    edges.to_file(output_path, driver="GPKG")

def create_graph_tourisme(graph_path, edges_buffered_path, graph_output_path):
    graph_e = gpd.read_file(graph_path, layer="edges")
    graph_n = gpd.read_file(graph_path, layer="nodes")
    edges_buffered = gpd.read_file(edges_buffered_path)

    graph_e["uniqId"] = graph_e.apply(create_uniqID, axis=1)

    graph_e = graph_e.set_index(["u", "v", "key"])
    edges_buffered = edges_buffered.set_index(["u", "v", "key"])
    graph_n = graph_n.set_index(["osmid"])

    graph_e["total_score_tourisme"] = edges_buffered["total_score_tourisme"]
    graph_e["score_distance_tourisme"] = edges_buffered["score_distance_tourisme"]

    graph_e["tourisme_score"] = edges_buffered["tourisme_score"]

    G = ox.graph_from_gdfs(graph_n, graph_e)

    ox.save_graph_geopackage(G, graph_output_path)

params = {
    "count" : {
        "edges_path": edges_buffer_tourisme_prop_path,
        "fn_cont": lambda x: x,
        "alpha": 1
    },
}

#all_score_edges(edges_buffer_path, edges_buffer_scored_path, params)
#total_score(edges_buffer_scored_path, edges_buffer_total_score_path, score_columns_tourisme)
#score_distance(edges_buffer_total_score_path, edges_buffer_total_score_distance_path)
score_tourisme(edges_buffer_total_score_distance_path, edges_buffer_total_score_distance_tourisme_path)
create_graph_tourisme(metrop_network_bouding_path, edges_buffer_total_score_distance_tourisme_path, "./output_data/network/graph/final_network_tourisme.gpkg")
