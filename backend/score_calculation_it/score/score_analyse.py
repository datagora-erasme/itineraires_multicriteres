#%%
import os
import sys
sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../script_python")
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import random
import pandas as pd
import multiprocessing as mp
import numpy as np
import osmnx as ox
import networkx as nx
import pickle
from function_utils import *
from shapely.geometry import Polygon

from scipy.stats import ttest_rel

from score_calculation import *

from global_variable import *

#%%
## FUNCTION : 
def load_network(network_path, pickle_path, network_multidigraph_pickle_path):
    """
    Load a network from a given geographical dataset, process the data, and save the network as pickled objects.
    
    Parameters:
    - network_path (str): The path to the network data file (GeoPackage format).
    - pickle_path (str): The path where the simple graph (nx.Graph) will be saved as a pickle file.
    - network_multidigraph_pickle_path (str): The path where the multi-directed graph (nx.MultiDiGraph) will be saved as a pickle file.
    
    Returns:
    - bool: True if the network is successfully processed and saved, otherwise False.
    
    This function reads the 'edges' and 'nodes' layers from the specified network file, processes the network data,
    creates a graph using the `osmnx` library, and stores both a simple graph and a multi-directed graph in pickle files.
    """
    gdf_edges = gpd.read_file(network_path, layer='edges')
    gdf_nodes = gpd.read_file(network_path, layer="nodes")

    gdf_nodes["y"] = gdf_nodes["lat"]
    gdf_nodes["x"] = gdf_nodes["lon"]

    #remove unecessary columns in order to lightened the network
    new_edges = gdf_edges[["u", "v", "key", "osmid", "uniqId", "length", "from", "to", "total_score_08", "total_score_13", "total_score_18", "freshness_score", "score_distance_08", "score_distance_13","score_distance_18", "geometry"]].set_geometry("geometry")
    new_edges.to_crs(gdf_edges.crs)

    new_edges = new_edges.set_index(["u", "v", "key"])
    gdf_nodes = gdf_nodes.set_index(['osmid'])

    G = ox.graph_from_gdfs(gdf_nodes, new_edges)

    G2 = nx.Graph(G)
    # G2 = nx.MultiDiGraph(G)

    G_digraph = nx.MultiDiGraph(G2)

    with open(pickle_path, "wb") as f:
        pickle.dump(G2, f)

    with open(network_multidigraph_pickle_path, "wb") as f:
        pickle.dump(G_digraph, f)
    return True

def load_graph_from_pickle(pickle_path):
    """
    Load a graph from a pickle file.
    
    Parameters:
    - pickle_path (str): The path to the pickle file containing the graph.
    
    Returns:
    - G (networkx.Graph or networkx.MultiDiGraph): The graph object loaded from the pickle file.
    
    This function opens the given pickle file and loads the graph object stored in it using the pickle module.
    """
    # Load the graph from the pickle file
    with open(pickle_path, 'rb') as f:
        G = pickle.load(f)

    return G

def shortest_path(G, start, end, G_multidigraph, index, global_gdf, zone_id="Non", total_score_column="total_score_13", min_dist=200, max_dist=4000):
    """
    Finds the shortest path between two nodes in a graph using both the 'total_score_column' and 'length' for path weighting.
    It adds the resulting paths to the global GeoDataFrame if the length of the path is within the specified range.

    Parameters:
    - G (networkx.Graph): The main graph to calculate the shortest path.
    - start (tuple): The starting coordinates (longitude, latitude).
    - end (tuple): The destination coordinates (longitude, latitude).
    - G_multidigraph (networkx.MultiDiGraph): The multigraph with multiple edges between nodes, used for routing.
    - index (int): An identifier to tag the resulting route.
    - global_gdf (GeoDataFrame): The global GeoDataFrame where the results will be appended.
    - zone_id (str, optional): The zone identifier to tag the resulting route. Default is "Non".
    - total_score_column (str, optional): The column to use for the path weight. Default is "total_score_13".
    - min_dist (float, optional): The minimum path length (in meters) for inclusion. Default is 200.
    - max_dist (float, optional): The maximum path length (in meters) for inclusion. Default is 4000.

    Returns:
    - global_gdf (GeoDataFrame): The updated GeoDataFrame with the added shortest paths.
    """
    origin_node = ox.nearest_nodes(G, X=start[0], Y=start[1])
    destination_node = ox.nearest_nodes(G, X=end[0], Y=end[1])

    print("Finding shortest path IF ...")
    print("total score column : ", total_score_column)

    shortest_path_if = nx.shortest_path(G, source=origin_node, target=destination_node, weight=total_score_column)

    # print("shortest_path_if:", shortest_path_if)

    route_edges_if = ox.utils_graph.route_to_gdf(G_multidigraph, shortest_path_if)

    # print("route_edges_if: ", route_edges_if)

    gdf_route_edges_if = gpd.GeoDataFrame(route_edges_if, crs=G.graph['crs'], geometry='geometry')

    gdf_route_edges_if = gdf_route_edges_if.to_crs(epsg=4326)

    gdf_route_edges_if["type"] = "IF"
    gdf_route_edges_if["id_it"] = index
    gdf_route_edges_if["zone_id"] = zone_id

    gdf_route_edges_if = gdf_route_edges_if.reset_index()
    gdf_route_edges_if = gdf_route_edges_if.set_index(["u", "v", "key", "type", "id_it"])

    print("Finding shortest path Length ...")

    shortest_path_len = nx.shortest_path(G, source=origin_node, target=destination_node, weight="length")

    route_edges_len = ox.utils_graph.route_to_gdf(G_multidigraph, shortest_path_len)

    gdf_route_edges_len = gpd.GeoDataFrame(route_edges_len, crs=G.graph['crs'], geometry='geometry')

    gdf_route_edges_len = gdf_route_edges_len.to_crs(epsg=4326)

    gdf_route_edges_len["type"] = "LEN"
    gdf_route_edges_len["id_it"] = index
    gdf_route_edges_len["zone_id"] = zone_id

    gdf_route_edges_len = gdf_route_edges_len.reset_index()
    gdf_route_edges_len = gdf_route_edges_len.set_index(["u", "v", "key", "type", "id_it"])

    sum_distance = gdf_route_edges_len["length"].sum()

    if(sum_distance >= min_dist and sum_distance <= max_dist):
        global_gdf = pd.concat([global_gdf, gdf_route_edges_if])
        global_gdf = pd.concat([global_gdf, gdf_route_edges_len])

    return global_gdf

def clip_graph_nodes_from_zone(zone, graph_n):
    """
    Clips graph nodes from a zone.

    Parameters:
    - zone (GeoDataFrame): The zone (polygon) that will be used to clip the nodes.
    - graph_n (GeoDataFrame): The nodes of the graph, assumed to be points with a 'geometry' column.

    Returns:
    - clipped_nodes (GeoDataFrame): The nodes that fall within the specified zone.
    """
    zone = zone.to_crs(3946)
    graph_n = graph_n.to_crs(3946)
    clipped_nodes = graph_n.overlay(zone, how="intersection")
    return clipped_nodes


def create_random_itineraries(nodes, graph, multidigraph, n_itineraries, global_gdf, zone_id, total_score_column, min_dist=200, max_dist=4000):
    """
    Create random itineraries by selecting random start and end nodes, and finding the shortest paths.

    Parameters:
    - nodes (GeoDataFrame): Nodes of the graph with latitudes and longitudes.
    - graph (NetworkX graph): The base graph.
    - multidigraph (MultiDiGraph): The graph with multi-edge support.
    - n_itineraries (int): Number of itineraries to generate.
    - global_gdf (GeoDataFrame): The global GeoDataFrame to store the resulting itineraries.
    - zone_id (str): Identifier for the zone to which the itinerary belongs.
    - total_score_column (str): The column used to calculate path weight (e.g., score or length).
    - min_dist (float): Minimum path distance.
    - max_dist (float): Maximum path distance.

    Returns:
    - global_gdf (GeoDataFrame): Updated GeoDataFrame containing all itineraries.
    """
    ## SELECT RANDOM POINTS
    nodes = nodes.set_index(["osmid"])

    if(len(nodes) < n_itineraries):
        n_itineraries = int(len(nodes)/2)-1

    random_nodes = nodes.sample(n=n_itineraries)
    start_nodes = random_nodes[0:round((n_itineraries)/2)]
    end_nodes = random_nodes[round((n_itineraries)/2):n_itineraries]

    count = 0

    for i in range(0,round(n_itineraries/2)):
        print(f"It {i} .. ")
        start = (start_nodes.iloc[i]["lon"], start_nodes.iloc[i]["lat"])
        end = (end_nodes.iloc[i]["lon"], end_nodes.iloc[i]["lat"])
        # print(start, end)
        global_gdf = shortest_path(graph, start, end, multidigraph, count, global_gdf, zone_id, total_score_column, min_dist=min_dist, max_dist=max_dist)
        count+=1

    return global_gdf

def extract_frequency_scores(itineraries):
    """
    Extracts frequency and associated scores for each edge in the given itineraries,
    separating the itineraries into "IF" and "LEN" types. The itineraries are aggregated 
    by edge based on their identifiers and scores.

    Args:
        itineraries (GeoDataFrame): A GeoDataFrame containing itineraries with columns 
                                    such as 'u', 'v', 'key', 'total_score_08', 'total_score_13',
                                    'total_score_18', 'geometry', and 'type'.

    Returns:
        freq_edges_if (GeoDataFrame): A GeoDataFrame containing the frequency and scores of edges 
                                      for "IF" type itineraries, with columns:
                                      'uniqId', 'count', 'score_08', 'score_13', 'score_18', and 'geometry'.
        freq_edges_len (GeoDataFrame): A GeoDataFrame containing the frequency and scores of edges 
                                       for "LEN" type itineraries, with columns:
                                       'uniqId', 'count', 'score_08', 'score_13', 'score_18', and 'geometry'.
    """
    print(itineraries)
    
    itineraries_if = itineraries[itineraries["type"] == "IF"]
    itineraries_len = itineraries[itineraries["type"] == "LEN"]

    freq_edges_if = gpd.GeoDataFrame({
        "uniqId": itineraries_if.groupby(["u", "v", "key"])["uniqId"].apply(lambda x: x.unique()[0]),
        "count": itineraries_if.groupby(["u", "v", "key"])["total_score_08"].count(),
        "score_08": itineraries_if.groupby(["u", "v", "key"])["total_score_08"].apply(lambda x: round(x.unique()[0],3)),
        "score_13": itineraries_if.groupby(["u", "v", "key"])["total_score_13"].apply(lambda x: round(x.unique()[0],3)),
        "score_18": itineraries_if.groupby(["u", "v", "key"])["total_score_18"].apply(lambda x: round(x.unique()[0],3)),
        "geometry": itineraries_if.groupby(["u", "v", "key"])["geometry"].apply(lambda x: x.unique()[0])
    })

    freq_edges_len = gpd.GeoDataFrame({
        "uniqId": itineraries_len.groupby(["u", "v", "key"])["uniqId"].apply(lambda x: x.unique()[0]),
        "count": itineraries_len.groupby(["u", "v", "key"])["total_score_08"].count(),
        "score_08": itineraries_len.groupby(["u", "v", "key"])["total_score_08"].apply(lambda x: round(x.unique()[0],3)),
        "score_13": itineraries_len.groupby(["u", "v", "key"])["total_score_13"].apply(lambda x: round(x.unique()[0],3)),
        "score_18": itineraries_len.groupby(["u", "v", "key"])["total_score_18"].apply(lambda x: round(x.unique()[0],3)),
        "geometry": itineraries_len.groupby(["u", "v", "key"])["geometry"].apply(lambda x: x.unique()[0])
    })

    return freq_edges_if, freq_edges_len

def calculate_mean_prop(it, score_column):
    """Calculate the mean proportion of one column for a given itinerary"""
    return round(sum(it[score_column]*it["length"])/sum(it["length"]), 2)

def calculate_mean_score(it, score_column):
    """Calculate the mean score for a given itinerary"""
    return round(sum(it[score_column])/sum(it["length"]), 2)

def create_df_mean_score(itineraries_path, output_path, score_column):
    "calculate mean score for every itineraries of a file"
    itineraries = gpd.read_file(itineraries_path)
    
    it_score = itineraries[["id_it", "type", score_column, "length", "zone_id"]].groupby(["id_it", "type", "zone_id"], axis=0).apply(lambda x: calculate_mean_score(x, score_column)).reset_index(name="score")
    it_length = itineraries[["id_it", "type", score_column, "length", "zone_id"]].groupby(["id_it", "type", "zone_id"], axis=0).apply(lambda x: round(sum(x["length"]),2)).reset_index(name="total_length")
    it_score["total_length"] = it_length["total_length"]

    print("it_score: ", it_score)
    it_score.to_csv(output_path)

def convert_score_on_ten(x, max):
    """
    Converts a given score `x` to a scale of 0-10 based on the provided maximum score `max`.

    Args:
        x (float): The score to be converted.
        max (float): The maximum possible score that corresponds to a 10 on the scale.

    Returns:
        float: The converted score on a scale of 0-10.
    """
    return (10/max)*x

def create_df_mean_value_by_columns(itineraries_path, edges_path, output_path, columns, total_score_column, max_score):
    """Calculate the mean proportion or score by itineraries"""

    edges_it = gpd.read_file(itineraries_path)
    edges = gpd.read_file(edges_path)
    edges_it = edges_it.set_index(["uniqId"])
    edges = edges.set_index(["uniqId"])

    edges_sample = edges.loc[edges_it.index.to_list()]

    edges_it[columns] = edges_sample[columns]
    it_grouped = edges_it.groupby(["id_it", "type"], axis=0)
    itineraries =  pd.DataFrame({})
    for column in columns: 
        itineraries[f"mean_{column}"] = it_grouped.apply(lambda x: calculate_mean_prop(x, column))

    itineraries["total_length"] = it_grouped.apply(lambda x: round(sum(x["length"]), 2))
    itineraries["mean_score"] = it_grouped.apply(lambda x: calculate_mean_score(x, total_score_column))
    itineraries["score_10"] = convert_score_on_ten(itineraries["mean_score"], max_score)

    itineraries.to_csv(output_path)

def test_students(group1, group2):
    """In order to compare the mean between the distribution of group 1 and group 2"""
    return ttest_rel(group1, group2)

def d_cohen(group1, group2):
    """In order to know if there is a size effect"""
    mean1 = np.mean(group1)
    mean2 = np.mean(group2)

    var1 = np.var(group1, ddof=1)
    var2 = np.var(group2, ddof=2)
    
    n1 = len(group1)
    n2 = len(group2)

    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))

    return (mean1 - mean2) / pooled_std

def distance_cost(group1, group2):
    """Calculate the distance cost between itineraries"""
    d1 = np.array(group1["total_length"])
    d2 = np.array(group2["total_length"])

    percent_diff = ((d2-d1)/d1)*100

    return round(np.mean(percent_diff),2)

def get_bounds(data):
    """
    Extracts the bounding box of the given GeoDataFrame or spatial data.

    Args:
        data (GeoDataFrame): A GeoDataFrame containing spatial data.

    Returns:
        tuple: A tuple containing the minimum x (minx), minimum y (miny),
               maximum x (maxx), and maximum y (maxy) coordinates of the bounding box.
    """
    bounds = data.total_bounds
    minx, miny, maxx, maxy = bounds
    return minx, miny, maxx, maxy

def create_grid(input_path, cell_size, output_path):
    """
    Creates a grid of polygons (cells) within the bounding box of the input GeoDataFrame,
    clips the grid to the boundaries of the input data, and saves the result as a GeoPackage.

    Args:
        input_path (str): Path to the input shapefile or GeoDataFrame.
        cell_size (float): Size of each cell in the grid.
        output_path (str): Path to save the output GeoPackage file.

    Returns:
        None
    """
    print("read file")
    data = gpd.read_file(input_path)
    minx, miny, maxx, maxy = get_bounds(data)
    x_range = np.arange(minx, maxx, cell_size)
    y_range = np.arange(miny, maxy, cell_size)
    polygons = []
    print("create grid")
    for x in range(len(x_range) - 1):
        for y in range(len(y_range) - 1):
            polygon = Polygon([
                (x_range[x], y_range[y]),
                (x_range[x + 1], y_range[y]),
                (x_range[x + 1], y_range[y + 1]),
                (x_range[x], y_range[y + 1]),
                (x_range[x], y_range[y])
            ])
            polygons.append(polygon)
    grid = gpd.GeoSeries(polygons, crs="EPSG:3946")
    grid = gpd.GeoDataFrame(geometry=grid)
    grid_clipped = gpd.clip(grid, data)
    print("save grid")
    grid_clipped.to_file(output_path, layer="grid", driver="GPKG")

def create_random_nodes(zones_path, input_graph_path, n_itineraries, output_nodes_start_path, output_nodes_end_path):
    """Extract pairs of nodes in order to keep ind stat : itineraries, defined by departure and arrival"""
    zones = gpd.read_file(zones_path)
    zones_index = [38,32,31,29,30,35,25,27,24,22]
    print(zones)
    graph_n = gpd.read_file(input_graph_path, layer="nodes")
    graph_n = graph_n.to_crs(3946)
    start_nodes = gpd.GeoDataFrame()
    end_nodes = gpd.GeoDataFrame()
    for i in zones_index:
        print(i)
        zone = gpd.GeoDataFrame(zones.loc[i-1], geometry=zones.loc[i-1], crs="EPSG:3946")
        intersection = graph_n.overlay(zone, how="intersection", keep_geom_type=True)
        intersection = intersection.reset_index()
        clipped_nodes = gpd.GeoDataFrame({"osmid": intersection["osmid"], "x": intersection["x"], "y": intersection["y"], "lat": intersection["lat"], "lon": intersection["lon"]}, geometry=intersection["geometry"], crs="EPSG:3946")

        print("clipped_nodes", clipped_nodes)
        random_nodes = clipped_nodes.sample(n=n_itineraries)
        sn = random_nodes[0:round((n_itineraries)/2)]
        en = random_nodes[round((n_itineraries)/2):n_itineraries]

        start_nodes = pd.concat([start_nodes, sn])
        end_nodes = pd.concat([end_nodes, en])
    
    start_nodes.to_file(output_nodes_start_path, driver="GPKG", layer="nodes")
    end_nodes.to_file(output_nodes_end_path, driver="GPKG", layer="nodes")

def pipeline_generate_dataset_new(params, nodes_start_path, end_nodes_path, total_score_column, min_dist, max_dist, hour):
    """
    Generates a dataset for each data source specified in the params dictionary. It reads input files for start and end nodes, 
    loads graph data, generates itineraries, calculates frequency scores, and then produces several outputs including datasets, 
    frequency analysis, and mean values.

    Args:
        params (dict): Dictionary containing parameters for data sources and their graph paths.
        nodes_start_path (str): Path to the shapefile containing the starting nodes.
        end_nodes_path (str): Path to the shapefile containing the ending nodes.
        total_score_column (str): Name of the column used to score paths.
        min_dist (float): Minimum distance for path inclusion.
        max_dist (float): Maximum distance for path inclusion.
        hour (str): The hour of analysis used to generate output paths.

    Returns:
        None
    """
    start_nodes = gpd.read_file(nodes_start_path)
    end_nodes = gpd.read_file(end_nodes_path)
    n_itineraries = len(start_nodes)

    columns = ["prairies_prop", "arbustes_prop", "arbres_prop", "C_wavg_scaled", "eaux_prop", "canop", "ombres_08_prop", "ombres_13_prop", "ombres_18_prop"]

    for data_name, data_params in params.items():
        create_folder(f"output_data/analyse/{data_name}/{hour}")
        g_pickle_path = f"output_data/analyse/{data_name}/{hour}/graph_{data_name}.pickle"
        g_multi_pickle_path = f"output_data/analyse/{data_name}/{hour}/graph_{data_name}_multi.pickle"
        load_network(f"{data_params['graph_path']}", g_pickle_path, g_multi_pickle_path)
        G = load_graph_from_pickle(g_pickle_path)
        MG = load_graph_from_pickle(g_multi_pickle_path)
        global_gdf = gpd.GeoDataFrame()
        count=0

        for i in range(0,round(n_itineraries/2)):
            print(f"It {i} .. ")
            start = (start_nodes.iloc[i]["lon"], start_nodes.iloc[i]["lat"])
            end = (end_nodes.iloc[i]["lon"], end_nodes.iloc[i]["lat"])
            global_gdf = shortest_path(G, start, end, MG, count, global_gdf, total_score_column=total_score_column, min_dist=min_dist, max_dist=max_dist)
            count+=1
        
        global_gdf.to_file(f"output_data/analyse/{data_name}/{hour}/dataset_{data_name}.gpkg")
        global_gdf = gpd.read_file(f"output_data/analyse/{data_name}/{hour}/dataset_{data_name}.gpkg")

        frequency_if, frequency_len = extract_frequency_scores(global_gdf)

        frequency_if.to_file(f"output_data/analyse/{data_name}/{hour}/frequency_if_{data_name}.gpkg", driver="GPKG", layer="frequency")
        frequency_len.to_file(f"output_data/analyse/{data_name}/{hour}/frequency_len_{data_name}.gpkg", driver="GPKG", layer="frequency")

        max_score = np.max(global_gdf[total_score_column])

        create_df_mean_value_by_columns(f"output_data/analyse/{data_name}/{hour}/dataset_{data_name}.gpkg", "output_data/analyse/edges_all_prop.gpkg", f"output_data/analyse/{data_name}/{hour}/mean_value_by_it{data_name}.csv", columns, total_score_column, max_score)
        create_df_mean_score(f"output_data/analyse/{data_name}/{hour}/dataset_{data_name}.gpkg", f"output_data/analyse/{data_name}/{hour}/mean_score{data_name}.csv", total_score_column)

        if(os.path.exists(g_pickle_path)):
            os.remove(g_pickle_path)
        if(os.path.exists(g_multi_pickle_path)):
            os.remove(g_multi_pickle_path)



## GLOBAL VARIABLES
grid_path = "./output_data/analyse/grid.gpkg"
output_nodes_start_path = "./output_data/analyse/selected_start_nodes.gpkg"
output_nodes_end_path = "./output_data/analyse/selected_end_nodes.gpkg"

#%%
# create_grid(bounding_metrop_path, 4000, grid_path)

# create_random_nodes(grid_path, final_network_path, 400, output_nodes_start_path, output_nodes_end_path)

pipeline_generate_dataset_new(final_params, output_nodes_start_path, output_nodes_end_path, "score_distance_13", 300, 4000, "13h")
