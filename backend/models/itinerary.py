import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import networkx as nx
import osmnx as ox
import json

def shortest_path(G, start, end, G_multidigraph):
    """Find the shortest and the freshness path between start and end. \n
        The term "if" is for indicator of freshness.
    """

    origin_node = ox.nearest_nodes(G, X=start[0], Y=start[1])
    destination_node = ox.nearest_nodes(G, X=end[0], Y=end[1])

    print("Finding shortest path IF ...")

    #TODO change the weight according to the hour (8h, 13h, 18h)
    shortest_path_if = nx.shortest_path(G, source=origin_node, target=destination_node, weight="score_distance_13")

    route_edges_if = ox.utils_graph.get_route_edge_attributes(G_multidigraph, shortest_path_if)

    gdf_route_edges_if = gpd.GeoDataFrame(route_edges_if, crs=G.graph['crs'], geometry='geometry')

    #epsg = 4326 is the epsg need by Leaflet in order to display the results on the map
    gdf_route_edges_if = gdf_route_edges_if.to_crs(epsg=4326)

    geojson_if = json.loads(gdf_route_edges_if.to_json())

    print("Finding shortest path Length ...")

    shortest_path_len = nx.shortest_path(G, source=origin_node, target=destination_node, weight="length")

    route_edges_len = ox.utils_graph.get_route_edge_attributes(G_multidigraph, shortest_path_len)

    gdf_route_edges_len = gpd.GeoDataFrame(route_edges_len, crs=G.graph['crs'], geometry='geometry')

    gdf_route_edges_len = gdf_route_edges_len.to_crs(epsg=4326)

    geojson_len = json.loads(gdf_route_edges_len.to_json())

    return geojson_if, geojson_len