import os
import sys
sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../script_python")
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
import osmnx as ox
from function_utils import *
from global_variable import *

###### NETWORK SCORE CALCULATION #######
create_folder("./../output_data/network/graph/")

### GLOBAL VARIABLES ###

score_columns = ["score_prairies_prop", "score_arbustes_prop", "score_arbres_prop", "score_C_wavg_scaled", "score_eaux_prop", "score_canop"]

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
    """
    Calculate the total score for each edge based on specified score columns and add specific adjusted scores.

    Parameters:
    - input_path: Path to the input GeoPackage file containing the edge data.
    - output_path: Path where the output file with total scores will be saved.
    - score_columns: List of columns to be summed to calculate the base total score for each edge.

    The function calculates a base total score by summing the specified columns, 
    then adds specific scores like `score_ombres_08_prop`, `score_ombres_13_prop`, 
    and `score_ombres_18_prop` for different times of the day.
    
    Additionally, the scores for certain times (`08`, `13`, and `18`) are adjusted to prioritize 
    the presence of canopy scores (`score_canop`) if they are greater than a threshold (0.5).
    """
    edges = gpd.read_file(input_path, layer="edges")
    print(edges.columns)
    edges["total_score"] = edges[score_columns].sum(axis=1)
    edges["total_score_08"] = edges["total_score"] + edges["score_ombres_08_prop"]
    edges["total_score_13"] = edges["total_score"] + edges["score_ombres_13_prop"]
    edges["total_score_18"] = edges["total_score"] + edges["score_ombres_18_prop"]

    # Force passage by parcs
    edges["total_score_08"] = edges.apply(lambda x: x["score_canop"] if(x["score_canop"] > 0.5) else x["total_score_08"], axis=1)
    edges["total_score_13"] = edges.apply(lambda x: x["score_canop"] if(x["score_canop"] > 0.5) else x["total_score_13"], axis=1)
    edges["total_score_18"] = edges.apply(lambda x: x["score_canop"] if(x["score_canop"] > 0.5) else x["total_score_18"], axis=1)
    

    edges.to_file(output_path, driver="GPKG")

def all_score_edges(input_path, output_path, params):
    """
    Add multiple calculated scores to the edges based on the provided parameters.

    Parameters:
    - input_path: Path to the input GeoPackage file containing the edges layer.
    - output_path: Path where the resulting file with all calculated scores will be saved.
    - params: Dictionary containing configuration for each score calculation. 
      Each entry should include the following:
        - edges_path: Path to the edges file that contains the score data.
        - fn_cont: A function to apply on the score data (e.g., for normalization or transformation).
        - alpha: A weighting factor to adjust the score calculation (optional).

    This function reads the edges data, applies the provided transformations (using the function 
    in `fn_cont`) for each score type, and stores the resulting scores in a new column of the edges.
    Finally, it saves the updated edges to the output path.

    The function assumes that the input edges file has a specific layer structure, and it uses 
    the columns from the `params` to calculate additional scores.
    """
    
    """
    params : {
        columns1 : {
            edges_path: "path",
            fn_cont: function(),
            alpha: 1
            },
        },
        ...
    }
    """
    default_edges = gpd.read_file(input_path, layer="edges")
    
    for data_name, data_param in params.items():
        print(f"Score {data_name}")
        data = gpd.read_file(data_param["edges_path"])
        print("columns", data.columns)
        default_edges[f"score_{data_name}"] = data[data_name].apply(data_param["fn_cont"])

    default_edges.to_file(output_path, driver="GPKG", layer="edges")

def one_score_edges(input_path, output_path, params, key):
    """(Re)-calculate score for one data"""
    default_edges = gpd.read_file(input_path, layer="edges")
    data = gpd.read_file(params[key]["edges_path"])
    default_edges[f"score_{key}"] = data[key].apply(params[key]["fn_cont"])

    default_edges.to_file(output_path, driver="GPKG")

def score_distance(input_path, output_path):
    """calculate the score by distance for each edges"""
    edges = gpd.read_file(input_path)

    edges["score_distance_08"] = round(edges["total_score_08"] * edges["length"])
    edges["score_distance_13"] = round(edges["total_score_13"] * edges["length"])
    edges["score_distance_18"] = round(edges["total_score_18"] * edges["length"])

    edges.to_file(output_path, driver="GPKG")

def score_fraicheur(input_path, output_path):
    """Score from 0 to 10 in term of freshness instead of heat"""
    edges = gpd.read_file(input_path)

    min_score_08 = edges["total_score_08"].min()
    max_score_08 = edges["total_score_08"].max()
    slope_08 = (0-10)/(max_score_08-min_score_08)
    origin_ordinate_08 = -slope_08*max_score_08
    edges["freshness_score_08"] = edges["total_score_08"].apply(lambda x: round(slope_08*x+origin_ordinate_08, 2))

    min_score_13 = edges["total_score_13"].min()
    max_score_13 = edges["total_score_13"].max()
    slope_13 = (0-10)/(max_score_13-min_score_13)
    origin_ordinate_13 = -slope_13*max_score_13
    edges["freshness_score_13"] = edges["total_score_13"].apply(lambda x: round(slope_13*x+origin_ordinate_13, 2))

    min_score_18 = edges["total_score_18"].min()
    max_score_18 = edges["total_score_18"].max()
    slope_18 = (0-10)/(max_score_18-min_score_18)
    origin_ordinate_18 = -slope_18*max_score_18
    edges["freshness_score_18"] = edges["total_score_18"].apply(lambda x: round(slope_18*x+origin_ordinate_18, 2))

    edges.to_file(output_path, driver="GPKG")

def create_graph(graph_path, edges_buffered_path, graph_output_path):
    """
    Creates a graph from the provided edge and node data, applying various scores from the edges' buffered data.

    Parameters:
    - graph_path: Path to the GeoPackage containing the graph data (edges and nodes).
    - edges_buffered_path: Path to the GeoPackage containing the buffered edge scores.
    - graph_output_path: Path where the final graph should be saved.
    """
    graph_e = gpd.read_file(graph_path, layer="edges")
    graph_n = gpd.read_file(graph_path, layer="nodes")
    edges_buffered = gpd.read_file(edges_buffered_path)

    graph_e["uniqId"] = graph_e.apply(create_uniqID, axis=1)

    graph_e = graph_e.set_index(["u", "v", "key"])
    edges_buffered = edges_buffered.set_index(["u", "v", "key"])
    graph_n = graph_n.set_index(["osmid"])

    graph_e["total_score_08"] = edges_buffered["total_score_08"]
    graph_e["total_score_13"] = edges_buffered["total_score_13"]
    graph_e["total_score_18"] = edges_buffered["total_score_18"]
    graph_e["score_distance_08"] = edges_buffered["score_distance_08"]
    graph_e["score_distance_13"] = edges_buffered["score_distance_13"]
    graph_e["score_distance_18"] = edges_buffered["score_distance_18"]

    graph_e["freshness_score_08"] = edges_buffered["freshness_score_08"]
    graph_e["freshness_score_13"] = edges_buffered["freshness_score_13"]
    graph_e["freshness_score_18"] = edges_buffered["freshness_score_18"]

    G = ox.graph_from_gdfs(graph_n, graph_e)

    ox.save_graph_geopackage(G, graph_output_path)

def score_calculation_pipeline(meta_params):
    """
    Execute the score calculation pipeline for each set of parameters.

    Args:
    - meta_params (dict): Dictionary containing parameters for each calculation.
    """

    for params_name, params in meta_params.items():
        print(f"Starting score calculation for {params_name}...")
        all_score_edges(edges_buffer_path, edges_buffer_scored_path, params["params"])
        total_score(edges_buffer_scored_path, edges_buffer_total_score_path, score_columns)
        score_distance(edges_buffer_total_score_path, edges_buffer_total_score_distance_path)
        score_fraicheur(edges_buffer_total_score_distance_path, edges_buffer_total_score_distance_freshness_path)
        create_graph(metrop_network_bouding_path, edges_buffer_total_score_distance_freshness_path, params["graph_path"])

        weights_path = globpath("./score_calculation_it/weights_score.csv")

        # Check if the weights file is empty
        try:
            weights = pd.read_csv(weights_path)
        except pd.errors.EmptyDataError:
            # If the file is empty, create a new DataFrame with columns
            weights = pd.DataFrame(columns=["graph_file", "arbres", "ombres" "arbustes", "prairies", "temp", "canop", "eaux"])

        currents_weights = pd.DataFrame({
            "graph_file": params["graph_path"],
            "arbres": params["params"]["arbres_prop"]["alpha"],
            "ombres": params["params"]["ombres_08_prop"]["alpha"],
            "arbustes": params["params"]["arbustes_prop"]["alpha"],
            "prairies": params["params"]["prairies_prop"]["alpha"],
            "temp": params["params"]["C_wavg_scaled"]["alpha"],
            "canop": params["params"]["canop"]["alpha"],
            "eaux": params["params"]["eaux_prop"]["alpha"]
        }, index=[0])

        concat_weights = pd.concat([weights, currents_weights])

        concat_weights.to_csv(weights_path, index=False)


final_params = {
    "P0_01O5At0_01Ar10C0_01E5Ca" : {
        "graph_path": final_network_path,
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path_no_na,
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: x,
            "alpha": ""
            },
        },
    },
}

score_calculation_pipeline(final_params)