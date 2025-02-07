import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import networkx as nx
import osmnx as ox
import random
import traceback
import math
import time
import csv
import fiona
import pandas as pd
import statistics

"""This file will not be use in production. It has been made in order to optimize
and choose the best algorithm to find the shortest path in the network"""

metrop_graph_path = "./data/osm/final_network.gpkg"
output_folder = "./script_python/optimization_files/"

output_optimization_folder = "./script_python/optimization_files/"
csv_results_path = "./script_python/optimization_files/results.csv"

ligth_network = "./script_python/optimization_files/light_network.gpkg"

def create_light_network(input_path, output_path):
    """
    Simplifies a road network by removing unnecessary columns and saves the processed network.

    Parameters:
    -----------
    input_path : str
        Path to the input GeoPackage file containing the road network with "edges" and "nodes" layers.
    output_path : str
        Path to save the processed and simplified road network as a GeoPackage.

    Returns:
    --------
    None
        The function processes the data and saves the new graph to the specified output path.
    """
    s = time.time()

    # Load edges and nodes from the input GeoPackage
    edges = gpd.read_file(input_path, layer="edges")
    nodes = gpd.read_file(input_path, layer="nodes")

    e = time.time()
    print(f"Data loading time: {(e - s) / 60:.2f} minutes")

    # Select relevant columns and set geometry
    new_edges = edges[["u", "v", "key", "osmid", "length", "from", "to", "IF", "geometry"]].set_geometry("geometry")
    new_edges.to_crs(edges.crs)

    # Set index for edges and nodes
    new_edges = new_edges.set_index(["u", "v", "key"])
    nodes = nodes.set_index(["osmid"])

    # Create graph from the modified data
    G = ox.graph_from_gdfs(nodes, new_edges)

    # Save the graph to the output file
    ox.save_graph_geopackage(G, output_path)
    # s = time.time()
    # edges = gpd.read_file(output_path, layer="edges")
    # nodes = gpd.read_file(output_path, layer="nodes")
    # e = time.time()
    # print((e-s)/60)

#create_light_network(metrop_graph_path, ligth_network)

def read_file_comparison(input_path):
    """Function to compare read_file time between different libraries
    Fiona is two times faster than geopandas
    """
    print("FIONA")
    time_fiona = []
    time_gpd = []
    for t in range(0,10):
        s_fiona = time.time()
        with fiona.open(input_path, layer="edges") as src:
            edges = gpd.GeoDataFrame(src)
            # edges = pd.DataFrame(src)
        with fiona.open(input_path, layer="nodes") as src:
            # nodes = gpd.GeoDataFrame(src)
            edges = pd.DataFrame(src)
        e_fiona = time.time()
        time_fiona.append(e_fiona-s_fiona)
        # print("reading file time fiona : ", e_fiona - s_fiona)

        print("GEOPANDAS")
        s_gpd = time.time()
        edges_gpd = gpd.read_file(input_path, layer="edges")
        nodes_gpd = gpd.read_file(input_path, layer="nodes")
        e_gpd = time.time()
        time_gpd.append(e_gpd - s_gpd)
        # print("reading file time gpd : ", e_gpd - s_gpd)

    print("FIONA moyenne : ",  statistics.mean(time_fiona)) # 6.75 secondes
    print("GEOPANDAS moyenne : ", statistics.mean(time_gpd)) # 13.88 secondes

def read_file_bbox_comparison(input_path, bbox):
    """
    Compares the loading time of a spatial dataset with and without a bounding box filter.

    This function reads the "edges" and "nodes" layers from a GeoPackage file multiple times, 
    measuring the time taken with and without a bounding box filter. It then prints the average 
    loading times for both methods.

    Parameters:
    -----------
    input_path : str
        Path to the input GeoPackage file containing the "edges" and "nodes" layers.
    bbox : tuple
        Bounding box coordinates in the format (minx, miny, maxx, maxy).

    Returns:
    --------
    None
        The function prints the average time taken for both methods.
    """
    time_ = []
    time_bbox = []

    for t in range(10):  # Run the test 10 times
        print(t)

        # Measure time for loading the full dataset
        s_ = time.time()
        with fiona.open(input_path, layer="edges") as src:
            edges = gpd.GeoDataFrame(src)
        with fiona.open(input_path, layer="nodes") as src:
            nodes = gpd.GeoDataFrame(src)
        e_ = time.time()
        time_.append(e_ - s_)

        # Measure time for loading data with a bounding box filter
        s_bbox = time.time()
        with fiona.open(input_path, layer="edges", bbox=bbox) as src:
            edges = gpd.GeoDataFrame(src)
        with fiona.open(input_path, layer="nodes", bbox=bbox) as src:
            nodes = gpd.GeoDataFrame(src)
        e_bbox = time.time()
        time_bbox.append(e_bbox - s_bbox)

    # Print average times
    print("_ moyenne : ", statistics.mean(time_))
    print("bbox moyenne : ", statistics.mean(time_bbox))

#read_file_bbox_comparison(ligth_network, bbox=bbox_lyon)

# read_file_comparison(ligth_network)



def select_random_nodes(nb_nodes, graph_path, output_start_path, output_end_path):
    """
    Selects a given number of random start and end nodes from a graph and saves them into GeoPackage files.

    Parameters:
    -----------
    nb_nodes : int
        Number of start and end nodes to randomly select.
    graph_path : str
        Path to the input GeoPackage file containing the "edges" and "nodes" layers of the graph.
    output_start_path : str
        Path to save the selected start nodes as a GeoPackage.
    output_end_path : str
        Path to save the selected end nodes as a GeoPackage.

    Returns:
    --------
    None
        The function saves the selected nodes as GeoPackage files.
    """
    # Load edges and nodes from the input GeoPackage
    edges = gpd.read_file(graph_path, layer="edges")
    nodes = gpd.read_file(graph_path, layer="nodes")

    # Set appropriate indices
    edges = edges.set_index(["u", "v", "key"])
    nodes = nodes.set_index(["osmid"])

    # Create a graph from the data
    G = ox.graph_from_gdfs(nodes, edges)

    # Randomly select start and end nodes
    start_nodes = random.sample(G.nodes, nb_nodes)
    end_nodes = random.sample(G.nodes, nb_nodes)

    # Convert selected nodes to GeoDataFrames
    start_points = gpd.GeoDataFrame(geometry=gpd.points_from_xy(
        [G.nodes[node]['x'] for node in start_nodes],
        [G.nodes[node]['y'] for node in start_nodes]
    ))

    end_points = gpd.GeoDataFrame(geometry=gpd.points_from_xy(
        [G.nodes[node]['x'] for node in end_nodes],
        [G.nodes[node]['y'] for node in end_nodes]
    ))

    # Save start and end points to GeoPackage files
    start_points.to_file(output_start_path, layer='start_points', driver='GPKG')
    end_points.to_file(output_end_path, layer='end_points', driver='GPKG')


#select_random_nodes(3, metrop_graph_path, output_folder + "start_nodes.gpkg", output_folder + "end_nodes.gpkg")

def euclidian_distance(node1, node2, G):
    """
    Computes the Euclidean distance between two nodes in a graph.

    Parameters:
    -----------
    node1 : int
        The first node identifier.
    node2 : int
        The second node identifier.
    G : networkx.Graph
        The graph containing the nodes, where each node has 'x' and 'y' coordinates.

    Returns:
    --------
    float
        The Euclidean distance between the two nodes.
    """
    (x1, y1) = G.nodes[node1]["x"], G.nodes[node1]["y"]
    (x2, y2) = G.nodes[node2]["x"], G.nodes[node2]["y"]  

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def manhattan_distance(node1, node2):
    """
    Computes the Manhattan distance between two points.

    Parameters:
    -----------
    node1 : tuple
        Coordinates (x, y) of the first point.
    node2 : tuple
        Coordinates (x, y) of the second point.

    Returns:
    --------
    float
        The Manhattan distance between the two points.
    """
    (x1, y1) = node1
    (x2, y2) = node2

    return abs(x2 - x1) + abs(y2 - y1)

def sp(graph_path, start, end, weight, shortest_path_file_path, algorithm, heuristic=None):
    """
    Computes the shortest path between two points in a graph using Dijkstra or A* algorithm 
    and saves the result in a GeoPackage file.

    Parameters:
    -----------
    graph_path : str
        Path to the input GeoPackage file containing the "edges" and "nodes" layers.
    start : tuple
        Coordinates (latitude, longitude) of the starting point.
    end : tuple
        Coordinates (latitude, longitude) of the destination point.
    weight : str
        The edge attribute to be used as a weight for shortest path computation.
    shortest_path_file_path : str
        Path to save the computed shortest path as a GeoPackage.
    algorithm : str
        The shortest path algorithm to use. Options: "Dijkstra" or "Alpha_star" (A*).
    heuristic : function, optional
        A heuristic function for the A* algorithm. Default is None.

    Returns:
    --------
    None
        The function saves the shortest path as a GeoPackage file.

    Notes:
    ------
    - Uses NetworkX for graph analysis.
    - If no path is found, an error message is printed.
    """
    # Load the graph data from the GeoPackage file
    s_file = time.time()
    with fiona.open(graph_path, layer="edges") as src:
        edges = list(src)
    
    with fiona.open(graph_path, layer="nodes") as src:
        nodes = list(src)
    
    gdf_edges = gpd.GeoDataFrame.from_features(edges, crs="EPSG:4171")
    gdf_nodes = gpd.GeoDataFrame.from_features(nodes, crs="EPSG:4171")

    e_file = time.time()
    print(f"{algorithm} reading file :  {e_file - s_file}")

    # Prepare graph structure
    gdf_edges = gdf_edges.set_index(['u', 'v', 'key'])
    gdf_nodes = gdf_nodes.set_index(['osmid'])

    # Rename coordinates
    gdf_nodes["y"] = gdf_nodes["lat"]
    gdf_nodes["x"] = gdf_nodes["lon"]

    s_graph = time.time()
    G = ox.graph_from_gdfs(gdf_nodes, gdf_edges)
    G2 = nx.Graph(G)  # Convert to undirected graph for shortest path search

    # Find nearest nodes in the graph
    origin_node = ox.nearest_nodes(G2, X=start[1], Y=start[0])
    destination_node = ox.nearest_nodes(G2, X=end[1], Y=end[0])

    e_graph = time.time()
    print(f"{algorithm} graph : {e_graph - s_graph}")

    try:
        s_ = time.time()
        
        # Compute shortest path
        if algorithm == "Dijkstra":
            shortest_path = nx.shortest_path(G2, source=origin_node, target=destination_node, weight=weight)
        elif algorithm == "Alpha_star":
            shortest_path = nx.astar_path(G2, source=origin_node, target=destination_node, weight=weight, heuristic=heuristic)

        e_ = time.time()
        print(f"{algorithm} duration : {e_ - s_}")

        # Save the shortest path to a GeoPackage file
        s_to_file = time.time()
        
        G3 = nx.MultiDiGraph(G2)
        route_edges = ox.utils_graph.get_route_edge_attributes(G3, shortest_path)
        gdf_route_edges = gpd.GeoDataFrame(route_edges, crs=G.graph['crs'], geometry='geometry')
        gdf_route_edges = gdf_route_edges.to_crs(epsg=3946)
        gdf_route_edges.to_file(shortest_path_file_path, driver='GPKG')

        e_to_file = time.time()
        print(f"{algorithm} to file : {e_to_file - s_to_file}")

    except nx.NetworkXNoPath:
        traceback.print_exc()
        print("No path found")


def optimization(graph_path, csv_results_path):
    """
    Compute shortest paths using Dijkstra and A* algorithms for multiple start and end points,
    and save the results in a CSV file.
    """
    with open(csv_results_path, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Start_X", "Start_Y", "End_X", "End_Y", "Dijkstra_sp", "Dijkstra_duration", "Astar_sp", "Astar_duration"])

        with fiona.open(output_folder + "start_nodes.gpkg", layer="start_points") as src:
            start_points = gpd.GeoDataFrame(src)
        
        with fiona.open(output_folder + "end_nodes.gpkg", layer="end_points") as src:
            end_points = gpd.GeoDataFrame(src)

        for i in range(len(start_points)):
            start = (start_points.loc[i, "geometry"]["coordinates"][1], start_points.loc[i, "geometry"]["coordinates"][0])
            end = (end_points.loc[i, "geometry"]["coordinates"][1], end_points.loc[i, "geometry"]["coordinates"][0])

            dijkstra_path = output_optimization_folder + f"sp_dijkstra/dijkstra_{i}.gpkg"
            astar_path = output_optimization_folder + f"sp_alpha_star/astar_{i}.gpkg"

            print(f"Astar {i}")
            stime_astar = time.time()
            sp(graph_path=graph_path, start=start, end=end, shortest_path_file_path=astar_path, algorithm="Alpha_star",
                heuristic=None, weight="IF")
            etime_astar = time.time()
            astar_duration = etime_astar - stime_astar
            print(f"Total A* duration: {astar_duration}")

            print(f"Dijkstra {i}")
            stime_dijkstra = time.time()
            sp(graph_path=graph_path, start=start, end=end, shortest_path_file_path=dijkstra_path, algorithm="Dijkstra", weight="IF")
            etime_dijkstra = time.time()
            dijkstra_duration = etime_dijkstra - stime_dijkstra
            print(f"Total Dijkstra duration: {dijkstra_duration}")

            writer.writerow([start[1], start[0], end[1], end[0], dijkstra_path, dijkstra_duration, astar_path, astar_duration])

optimization(ligth_network, csv_results_path)