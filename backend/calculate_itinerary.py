import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import networkx as nx
import osmnx as ox
import pickle
import time
import json
import sys

def load_graph_from_pickle(pickle_path):
    # Load the graph from the pickle file
    with open(pickle_path, 'rb') as f:
        G = pickle.load(f)

    return G

# start = (4.8478, 45.7001)
# end = (5.0303, 45.7624)
startLat = float(sys.argv[1])
startLon = float(sys.argv[2])

endLat = float(sys.argv[3])
endLon = float(sys.argv[4])

start = (startLon, startLat)
end = (endLon, endLat)

# s = time.time()
# s_g = time.time()
G = load_graph_from_pickle("./data/pickle_network.pickle")
# e_g = time.time()

# s_nodes = time.time()
origin_node = ox.nearest_nodes(G, X=start[0], Y=start[1])
destination_node = ox.nearest_nodes(G, X=end[0], Y=end[1])
# e_nodes = time.time()

# s_sp = time.time()
shortest_path = nx.shortest_path(G, source=origin_node, target=destination_node, weight="IF")
# e_sp = time.time()

# s_convert_sp = time.time()
G2 = nx.MultiDiGraph(G)

route_edges = ox.utils_graph.get_route_edge_attributes(G2, shortest_path)

gdf_route_edges = gpd.GeoDataFrame(route_edges, crs=G.graph['crs'], geometry='geometry')

gdf_route_edges = gdf_route_edges.to_crs(epsg=4326)
# e_convert_sp = time.time()

geojson = json.loads(gdf_route_edges.to_json())

print(json.dumps(geojson)) #TODO : essayer d'utiliser directement route_edges

# e = time.time()

# print(f"total duration : {e-s}") # 6.55 s
# print(f"load graph duration : {e_g -s_g}") # 1.62 s
# print(f"find nodes duration : {e_nodes - s_nodes}") # 1.84 s
# print(f"shortest path duration : {e_sp - s_sp}") # 0.1 s
# print(f"convert shortest path duration : {e_convert_sp - s_convert_sp}") #3s
