import os
os.environ['USE_PYGEOS'] = '0'
import osmnx as ox
import networkx as nx
import fiona
import shapely.geometry as geom
import geopandas as gpd
import traceback
from data_utils import create_folder
import warnings
import numpy as np
import json
import pandas as pd

warnings.filterwarnings("ignore", category=UserWarning)

### Global Variables

data_informations_path = "./data/data_informations.json"

### FUNCTION TO CALCULATE IF FOR EACH DATA

def calculate_IF(input_path, output_path, fn, name):
    """Function to recalculate IF according to other attributes
    fn is the function to apply
    """
    data = gpd.read_file(input_path)

    if(name == "veget_raw"):
        print(data.columns)
        data = data.set_index(["id_gpd"])

    data[f"IF_{name}"] = data.apply(fn, axis=1)

    # if(name == "veget_raw"):
    #     data = data.set_index(["id_gpd"])

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
    
def veget_IF(row):
    """Return value of IF for temperature data"""
    if(row["vegetation_class"] == 1):
        return 0.75
    elif(row["vegetation_class"] == 2):
        return 0.75
    elif(row["vegetation_class"] == 3):
        return 0.5
    elif(row["vegetation_class"] == 4):
        return 0.01
    elif(row["vegetation_class"] == 5):
        return 0.01
    else:
        return 1

def load_osm_network(network_paramaters):
    print("Loading OSM network")

    # Retrieve the street network graph
    if(network_paramaters["bbox"] !=None):
        north, south, east, west = network_paramaters["bbox"]
        # G = ox.graph_from_bbox(north, south, east, west, network_type=network_paramaters["network_type"], simplify=True)
        G = ox.graph_from_bbox(north, south, east, west, custom_filter=network_paramaters["network_filters"], simplify=True)
    else:
        G = ox.graph_from_place(network_paramaters["place_name"], custom_filter=network_paramaters["network_filters"], simplify=False)

    G = ox.project_graph(G, to_crs="EPSG:3946")

    #G = ox.simplify_graph(G)
    #G = ox.project_graph(G)

    print("OSM network loaded, saving into file..")
    # Save the graph data as a GeoPackage file
    create_folder("./data/osm")
    ox.save_graph_geopackage(G, filepath=network_paramaters["output_file"])

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
    # weighted_edges = weighted_edges.drop_duplicates(subset=["u", "v", "key"])
    weighted_edges = weighted_edges.set_index(["u", "v", "key"])

    # print(f"default_edges: \n {default_edges.loc[(default_edges.index.get_level_values('u') == 10928012589)]}")
    print(f"weighted_edges: \n {weighted_edges.loc[(weighted_edges.index.get_level_values('u') == 10928012589)]}")

    print(f"Calculating weighted average for {layer_name} ...")

    # print(weighted_edges.loc[(weighted_edges.index.get_level_values("u") == 347474560) & (weighted_edges.index.get_level_values("v") == 1974857243)])


    # Due to intersection, there more features into the weighted_edges dataframe than the default_network one
    #The following line allows to recalculate the weighted average for one edge taking account all the "subedges"
    grouped_edges = weighted_edges.groupby(["u", "v", "key"], group_keys=True).apply(lambda x: pd.Series({
        f"IF_{layer_name}": np.average(x[f"IF_{layer_name}"], weights=x["cal_length"], returned=False)
    })).reset_index()

    # print(grouped_edges[(grouped_edges["u"] == 347474560) & (grouped_edges["v"] == 1974857243)])

    grouped_edges = grouped_edges.set_index(["u", "v", "key"])
    default_edges = default_edges.set_index(["u", "v", "key"])

    default_edges[f"IF_{layer_name}"] = grouped_edges[f"IF_{layer_name}"]

    print(f" default_edges after group : \n : {default_edges.loc[(default_edges.index.get_level_values('u') == 10928012589)]}")

    default_nodes = default_nodes.set_index(['osmid'])

    # G = ox.graph_from_gdfs(default_nodes, default_edges)

    print(f"Done. \nSaving file into {output_path}")

    # nodes, edges = ox.graph_to_gdfs(G)

    # print(f" edges after graph : \n : {edges.loc[(edges.index.get_level_values('u') == 10928012589)]}")

    default_edges.to_file(output_path, layer="edges")

    # ox.save_graph_geopackage(G, filepath=output_path)

    # new_edges = gpd.read_file(output_path, layer="edges")

    # new_edges = new_edges.set_index(["u", "v", "key"])

    # print(f" new_edges after group : \n : {new_edges.loc[(new_edges.index.get_level_values('u') == 10928012589)]}")

def join_network_layer(network_path, layer_path, layer_name, output_path):
    """This function join a network with a specific layer"""
    network_edges = gpd.read_file(network_path, layer="edges")

    layer = gpd.read_file(layer_path)

    # print(layer.head)
    # print(layer.columns)

    # if(layer_name == "temp_surface_road_raw"):
    #     layer = layer.to_crs(3946)
    # else:
    layer = layer.to_crs(network_edges.crs)

    print(f"Joining {layer_name} with osm network")

    if(layer_name != "veget_raw"):

        joined_edges = gpd.overlay(network_edges, layer, how="identity", keep_geom_type=True)

        # Convert into geoserie in order to calculate the length of the intersection

        joined_edges_serie = gpd.GeoSeries(joined_edges["geometry"])

        # joined_edges_serie = joined_edges_serie.to_crs(32631)

        joined_edges["cal_length"] = joined_edges_serie.length

        joined_edges[f"IF_{layer_name}"] = joined_edges[f"IF_{layer_name}"].fillna(1)

        # joined_edges.to_file("./temp/toil_net_joined_ident_na.gpkg", driver="GPKG")
        network_weighted_average(network_path, joined_edges, layer_name, output_path)
    
    else:
        layer_serie = gpd.GeoSeries(layer["geometry"])
        # layer_serie = layer_serie.to_crs(32631)
        layer["cal_length"] = layer_serie.length

        network_weighted_average(network_path, layer, layer_name, output_path)

#join_network_layer("./data/osm/metrop_walk_2605_2.gpkg", "./data/gpkg_buffered/toilettes_publiques_buffered.gpkg", "toilettes_publiques", "./temp/toil_net_edges_3005.gpkg")

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
    data_raw = data_informations["data_raw"]
    for d_name, d_info in data_raw.items():
        # if(d_name == "veget_raw"):
        output_path = f"./data/osm/network_{d_name}_weighted.gpkg"
        join_network_layer(default_ntf, d_info["recalculated_if_path"], d_name, output_path)
        data_informations["data_raw"][d_name]["weighted_network_path"] = output_path


    # temp = data_informations["data_raw"]["temp_surface_road_raw"]
    # path = temp["recalculated_if_path"]
    # temp_output_path = "./data/osm/network_temp_surface_road_raw_weighted.gpkg"
    # join_network_layer(default_ntf, path, "temp_surface_road_raw", temp_output_path)
    # data_informations["data_raw"]["temp_surface_road_raw"]["weighted_network_path"] = temp_output_path

    with open(data_informations_path, "w") as f:
        json.dump(data_informations, f, indent=4)

def merge_networks(default_network, output_path):
    """Merge all network together"""
    final_network = gpd.read_file(default_network, layer="edges")
    final_network_nodes = gpd.read_file(default_network, layer="nodes")
    final_network["IF"] = 0

    with open(data_informations_path, "r") as f:
        data_informations = json.load(f)

    sum_weight = 0

    final_network = final_network.set_index(["u", "v", "key"])
    final_network_nodes = final_network_nodes.set_index(["osmid"])

    # print(f"Final network NA : {final_network.isna().sum()}")
    # print(f"Is network valid : {final_network.is_valid.all()}")
    
    # WFS
    data_wfs = data_informations["data_wfs"]
    for d_name, d_info in data_wfs.items():
        weigth = d_info["weight"]
        network_path = d_info["weighted_network_path"]
        network = gpd.read_file(network_path, layer="edges")
        network = network.set_index(["u", "v", "key"])

        # print(f"Is layer valid : {network.is_valid.all()}")

        print(f"Layer : {d_name}")
        # print(f"NA : {network.isna().sum()}")
        print(f"net[IF] before NA: \n {network[f'IF_{d_name}'].loc[(network[f'IF_{d_name}'].index.get_level_values('u') == 10928012589)]}")

        network[f"IF_{d_name}"] = network[f"IF_{d_name}"].fillna(1)

        # print(f"NA fill :{network.isna().sum()}")
        if_cal = final_network["IF"] + network[f"IF_{d_name}"]*weigth
        print(f"fn[IF] : \n {final_network['IF'].loc[(final_network['IF'].index.get_level_values('u') == 10928012589)]}")
        print(f"net[IF] : \n {network[f'IF_{d_name}'].loc[(network[f'IF_{d_name}'].index.get_level_values('u') == 10928012589)]}")
        print(f" weight : {weigth}")
        print(f" if cal : \n {if_cal.loc[(if_cal.index.get_level_values('u') == 10928012589)]}")
        final_network["IF"] = if_cal
        # print(f"final network NA after weight: {final_network.isna().sum()}")
        final_network[f"IF_{d_name}"] = network[f"IF_{d_name}"]
        final_network[f"weight_{d_name}"] = weigth
        # print(f"final network NA after all : {final_network.isna().sum()}")
        sum_weight += weigth

    # RAW
    data_raw = data_informations["data_raw"]
    for d_name, d_info in data_raw.items():
        # if(d_name == "temp_surface_road_raw"):
        weigth = d_info["weight"]
        network_path = d_info["weighted_network_path"]
        network = gpd.read_file(network_path, layer="edges")
        network = network.set_index(["u", "v", "key"])

        print(f"Layer : {d_name}")
        print(f"NA : {network.isna().sum()}")

        network[f"IF_{d_name}"] = network[f"IF_{d_name}"].fillna(1)

        print(f"NA fill :{network.isna().sum()}")

        final_network["IF"] = final_network["IF"] + network[f"IF_{d_name}"]*weigth
        print(f"final network NA after weight: {final_network.isna().sum()}")
        final_network[f"IF_{d_name}"] = network[f"IF_{d_name}"]
        final_network[f"weight_{d_name}"] = weigth
        print(f"final network NA after all : {final_network.isna().sum()}")
        sum_weight += weigth
    
    final_network["IF"] = final_network["IF"] / sum_weight

    G = ox.graph_from_gdfs(final_network_nodes, final_network)

    ox.save_graph_geopackage(G, filepath=output_path)

# def manhattan_distance(node1, node2):
#     print(node1, node2)
#     x1, y1 = node1
#     x2, y2 = node2
#     return abs(x1-x2) + abs(y1-y2)

def shortest_path(graph_file_path, shortest_path_file_path, origin_point, destination_point, weight):
    # Load the graph data from the GeoPackage file
    #print(f"Loading Network from {graph_file_path}")
    gdf_edges = gpd.read_file(graph_file_path, layer='edges')
    gdf_nodes = gpd.read_file(graph_file_path, layer="nodes")

    gdf_edges = gdf_edges.set_index(['u', 'v', 'key'])
    gdf_nodes = gdf_nodes.set_index(['osmid'])

    gdf_nodes["y"] = gdf_nodes["lat"]
    gdf_nodes["x"] = gdf_nodes["lon"]

    G = ox.graph_from_gdfs(gdf_nodes, gdf_edges)

    G2 = nx.Graph(G)

    origin_node = ox.nearest_nodes(G2, X=origin_point[1], Y=origin_point[0])
    destination_node = ox.nearest_nodes(G2, X=destination_point[1], Y=destination_point[0])

    try:
        #print("Calculating shortest path ... ")
        # Calculate the shortest path using Dijkstra's algorithm
        shortest_path = nx.shortest_path(G2, source=origin_node, target=destination_node, weight=weight)

        G3 = nx.MultiDiGraph(G2)

        #print(shortest_path)

        route_edges = ox.utils_graph.get_route_edge_attributes(G3, shortest_path)

        gdf_route_edges = gpd.GeoDataFrame(route_edges, crs=G.graph['crs'], geometry='geometry')

        gdf_route_edges = gdf_route_edges.to_crs(epsg=4326)

        gdf_route_edges.to_file(shortest_path_file_path, driver='GeoJSON')

        #print("Shortest path found")

    except nx.NetworkXNoPath:
        traceback.print_exc()
        print("No path found")

#create_folder("./data/osm/shortest_path/")

#origin_point = (45.73424, 4.8593181)
# # destination_point = (45.7751805,4.8437929)

#destination_point = (45.7531827,4.8478752)

#shortest_path("./backend/script_python/data/osm/weighted_network_3946.gpkg", "./backend/script_python/data/osm/shortest_path/big_shortest_path_IF_3946.gpkg", origin_point=origin_point, destination_point=destination_point, weight="IF")
# shortest_path("./data/osm/weighted_network_3946.gpkg", "./data/osm/shortest_path/big_shortest_path_C_3946.gpkg", origin_point=origin_point, destination_point=destination_point, weight="C")
# shortest_path("./data/osm/weighted_network_3946.gpkg", "./data/osm/shortest_path/big_shortest_path_length_3946.gpkg", origin_point=origin_point, destination_point=destination_point, weight="length")

#shortest_path("./data/osm/lyon_drive.gpkg", "./data/osm/shortest_path/lyon_drive_shortest_path_2.gpkg", origin_point=origin_point, destination_point=destination_point, weight="length")
