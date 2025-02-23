import os
os.environ['USE_PYGEOS'] = '0'
import networkx as nx
import geopandas as gpd
import osmnx as ox
import pickle
from datetime import datetime
from global_variable import graphs_local_cache, graph_paths

def create_pickles_from_graph_criterion(criterion):
    global graphs_local_cache, graph_paths
    gpkg_path = graph_paths[criterion]["gpkg"]
    pickle_graph_path = graph_paths[criterion]["pickle"]
    pickle_multidigraph_path = graph_paths[criterion]["multidigraph_pickle"]

    """
    Load a graph into pickle files.
    Both simple graph and multidigraph are needed for the function shortest_path of the project.

    Parameters:
    - graph_path: str, path to the graph file.
    - graph_pickle_path: str, path to save the simple graph pickle file.
    - graph_multidigraph_pickle_path: str, path to save the multidigraph pickle file.
    - score_type: str, type of score ('pollen' or 'bruit') to be used for specific columns.
    """
    print(datetime.now(), f"Pickle file creation start")

    gdf_edges = gpd.read_file(gpkg_path, layer='edges')
    gdf_nodes = gpd.read_file(gpkg_path, layer="nodes")

    gdf_nodes["y"] = gdf_nodes["lat"]
    gdf_nodes["x"] = gdf_nodes["lon"]
    gdf_nodes["geometry"] = gpd.points_from_xy(gdf_nodes["x"], gdf_nodes["y"])  # Fix warning

    if criterion == 'frais':
        new_edges = gdf_edges[["u", "v", "key", "osmid", "length", "from", "to", "score_distance_13", "total_score_13", "freshness_score_13", "geometry"]]
    elif criterion == 'pollen':
        new_edges = gdf_edges[["u", "v", "key", "osmid", "length", "from", "to", "score_distance_pollen", "total_score_pollen", "pollen_score", "geometry"]]
    elif criterion == 'bruit':
        new_edges = gdf_edges[["u", "v", "key", "osmid", "length", "from", "to", "score_distance_bruit", "total_score_bruit", "bruit_score", "geometry"]]
    elif criterion == 'tourisme':
        new_edges = gdf_edges[["u", "v", "key", "osmid", "length", "from", "to", "score_distance_tourisme", "total_score_tourisme", "tourisme_score", "geometry"]]
    else:
        raise ValueError("Invalid score_type. Must be 'frais', 'pollen', 'bruit' or 'tourisme'.")

    new_edges = new_edges.set_geometry("geometry")
    new_edges.to_crs(gdf_edges.crs)

    new_edges = new_edges.set_index(["u", "v", "key"])
    gdf_nodes = gdf_nodes.set_index(['osmid'])

    G = ox.graph_from_gdfs(gdf_nodes, new_edges)

    G2 = nx.Graph(G)
    G_digraph = nx.MultiDiGraph(G2)

    with open(pickle_graph_path, "wb") as f:
        pickle.dump(G2, f, protocol=5)

    with open(pickle_multidigraph_path, "wb") as f:
        pickle.dump(G_digraph, f, protocol=5)
    
    print(datetime.now(), f"Pickle file creation end")
    
    return True

def load_graphs_from_pickles(criterion):
    """
    Loads a graph from a pickle file, caching the loaded graphs in a local cache to avoid repeated loading.
    
    Parameters:
    - `criterion`: The criterion to load the graph data for.
    
    The function first checks if the graphs are already loaded and cached. If not, it loads the graphs from the pickle files and caches them for future use.
    """
    global graphs_local_cache, graph_paths
    pickle_graph_path = graph_paths[criterion]["pickle"]
    pickle_multidigraph_path = graph_paths[criterion]["multidigraph_pickle"]


    print(datetime.now(), f"Load pickle file start.")

    if (pickle_graph_path not in graphs_local_cache) or (graphs_local_cache[pickle_graph_path] is None):
        print(datetime.now(), f"Not in cache. Loading pickle file and caching it")
        with open(pickle_graph_path, 'rb') as f:
            pickle_file = pickle.load(f)
            graphs_local_cache[pickle_graph_path] = pickle_file
    
    if (pickle_multidigraph_path not in graphs_local_cache) or (graphs_local_cache[pickle_multidigraph_path] is None):
        print(datetime.now(), f"Not in cache. Loading pickle file and caching it")
        with open(pickle_multidigraph_path, 'rb') as f:
            multidi_pickle_file = pickle.load(f)
            graphs_local_cache[pickle_multidigraph_path] = multidi_pickle_file
        
    print(datetime.now(), f"Load pickle file end.")
