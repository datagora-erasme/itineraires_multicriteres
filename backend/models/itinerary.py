from datetime import datetime
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import networkx as nx
import osmnx as ox
import json
from global_variable import graphs_local_cache, graph_paths

def nearest_nodes(start, end):
    """
    Finds the nearest nodes in the graph to the given start and end coordinates.
    
    Args:
        start (tuple): The (latitude, longitude) coordinates of the starting point.
        end (tuple): The (latitude, longitude) coordinates of the ending point.
    
    Returns:
        tuple: The nearest node IDs for the start and end points.

    Notes:
        - We use this function before shortest_path for performance reasons: Since this calculation is expensive, we do it only once.
        - The nodes are the same on all graphs. The function uses the 'frais' graph for the nearest node search, but it could be any other graph.
    """
    global graphs_local_cache, graph_paths
    pickle_graph = graphs_local_cache[graph_paths["frais"]["pickle"]] 

    print(datetime.now(), f"Preparing nodes start")

    origin_node = ox.nearest_nodes(pickle_graph, X=start[0], Y=start[1])
    destination_node = ox.nearest_nodes(pickle_graph, X=end[0], Y=end[1])

    print(datetime.now(), f"Preparing nodes end")

    return origin_node, destination_node

def shortest_path(criterion, origin_node, destination_node, weight="score_distance_13"):
    """
    Finds the shortest and the best (based on criterion) paths between the given start and destination nodes.
    
    Args:
        criterion (str): The criterion to use for the path calculation.
        origin_node (int): The ID of the starting node.
        destination_node (int): The ID of the ending node.
        weight (str, optional): The weight attribute to use for the path calculation. Defaults to "score_distance_13".
    
    Returns:
        tuple: Two GeoJSON objects representing the shortest path and the best (based on criterion) path.

    Notes:
        The term "if" is for "indicator of freshness" (i.e criterion).
    """
    global graphs_local_cache, graph_paths
    pickle_graph = graphs_local_cache[graph_paths[criterion]["pickle"]]
    pickle_multidigraph = graphs_local_cache[graph_paths[criterion]["multidigraph_pickle"]]

    #TODO change the weight according to the hour (8h, 13h, 18h)
    shortest_path_if = nx.shortest_path(pickle_graph, source=origin_node, target=destination_node, weight=weight)

    route_edges_if = ox.utils_graph.get_route_edge_attributes(pickle_multidigraph, shortest_path_if)

    gdf_route_edges_if = gpd.GeoDataFrame(route_edges_if, crs=pickle_graph.graph['crs'], geometry='geometry')

    #epsg = 4326 is the epsg need by Leaflet in order to display the results on the map
    gdf_route_edges_if = gdf_route_edges_if.to_crs(epsg=4326)

    geojson_if = json.loads(gdf_route_edges_if.to_json())

    print(datetime.now(), f"Finding shortest path Length ...")

    shortest_path_len = nx.shortest_path(pickle_graph, source=origin_node, target=destination_node, weight="length")

    route_edges_len = ox.utils_graph.get_route_edge_attributes(pickle_multidigraph, shortest_path_len)

    gdf_route_edges_len = gpd.GeoDataFrame(route_edges_len, crs=pickle_graph.graph['crs'], geometry='geometry')

    gdf_route_edges_len = gdf_route_edges_len.to_crs(epsg=4326)

    geojson_len = json.loads(gdf_route_edges_len.to_json())

    return geojson_if, geojson_len









def shortest_path_criterion(criterion, origin_node, destination_node, weight="score_distance_13"):
    """
    Finds the best (based on criterion) path between the given start and destination nodes.
    
    Args:
        criterion (str): The criterion to use for the path calculation.
        origin_node (int): The ID of the starting node.
        destination_node (int): The ID of the ending node.
        weight (str, optional): The weight attribute to use for the path calculation. Defaults to "score_distance_13".
    
    Returns:
        GeoJSON object representing the best (based on criterion) path.

    Notes:
        The term "if" is for "indicator of freshness" (i.e criterion).
    """
    global graphs_local_cache, graph_paths
    pickle_graph = graphs_local_cache[graph_paths[criterion]["pickle"]]
    pickle_multidigraph = graphs_local_cache[graph_paths[criterion]["multidigraph_pickle"]]

    #TODO change the weight according to the hour (8h, 13h, 18h)
    shortest_path_if = nx.shortest_path(pickle_graph, source=origin_node, target=destination_node, weight=weight)

    route_edges_if = ox.utils_graph.get_route_edge_attributes(pickle_multidigraph, shortest_path_if)

    gdf_route_edges_if = gpd.GeoDataFrame(route_edges_if, crs=pickle_graph.graph['crs'], geometry='geometry')

    #epsg = 4326 is the epsg need by Leaflet in order to display the results on the map
    gdf_route_edges_if = gdf_route_edges_if.to_crs(epsg=4326)

    geojson_if = json.loads(gdf_route_edges_if.to_json())

    return geojson_if



## À voir comment faire et comment envoyer le json. Avoir un graph "common" pour tous les critères pour pouvoir calculer tous les scores? 

# def shortest_path_length(origin_node, destination_node):
#     """
#     Finds the shortest path between the given start and destination nodes.
    
#     Args:
#         criterion (str): The criterion to use for the path calculation.
#         origin_node (int): The ID of the starting node.
#         destination_node (int): The ID of the ending node.
#         weight (str, optional): The weight attribute to use for the path calculation. Defaults to "score_distance_13".
    
#     Returns:
#         tuple: Two GeoJSON objects representing the shortest path and the best (based on criterion) path.

#     Notes:
#         The term "if" is for "indicator of freshness" (i.e criteron).
#     """
#     global graphs_local_cache, graph_paths
#     pickle_graph = graphs_local_cache[graph_paths[criterion]["pickle"]]
#     pickle_multidigraph = graphs_local_cache[graph_paths[criterion]["multidigraph_pickle"]]

#     print(datetime.now(), f"Finding shortest path Length ...")

#     shortest_path_len = nx.shortest_path(pickle_graph, source=origin_node, target=destination_node, weight="length")

#     route_edges_len = ox.utils_graph.get_route_edge_attributes(pickle_multidigraph, shortest_path_len)

#     gdf_route_edges_len = gpd.GeoDataFrame(route_edges_len, crs=pickle_graph.graph['crs'], geometry='geometry')

#     gdf_route_edges_len = gdf_route_edges_len.to_crs(epsg=4326)

#     geojson_len = json.loads(gdf_route_edges_len.to_json())

#     return geojson_len
