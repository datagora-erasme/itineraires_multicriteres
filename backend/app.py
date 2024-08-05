import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from models.data import *
from load_graph import *
from models.itinerary import *
from global_variable import *
#from calculate_itinerary import *

app = Flask(__name__)
CORS(app)

# network_path = "./score_calculation_it/output_data/network/graph/final_network_bounding_scaled_no_na.gpkg"
# network_pickle_path = "./score_calculation_it/output_data/network/graph/final_network_bounding_scaled_no_na.pickle"
# network_multidigraph_pickle_path ="./score_calculation_it/output_data/network/graph/final_network_bounding_scaled_no_na_multidigraph.pickle"

"""
The final graph is loaded into a pickle file in order to keep it in RAM. 
It allows to reduce the time between request and response (the files took several seconds to open).
"""

G = None
G_multidigraph = None

graph_paths = {
    "frais": {
        "gpkg": final_network_path, 
        "pickle": final_network_pickle_path,
        "multidigraph_pickle": final_network_multidigraph_pickle_path
    },
    "pollen": {
        "gpkg": final_network_pollen_path,
        "pickle": final_network_pickle_pollen_path,
        "multidigraph_pickle": final_network_multidigraph_pickle_pollen_path
    },
    "bruit": {
        "gpkg": final_network_bruit_path,
        "pickle": final_network_pickle_bruit_path,
        "multidigraph_pickle": final_network_multidigraph_pickle_bruit_path
    },
    "tourisme": {
        "gpkg": final_network_tourisme_path,
        "pickle": final_network_pickle_tourisme_path,
        "multidigraph_pickle": final_network_multidigraph_pickle_tourisme_path
    }
}

G = None
G_multidigraph = None

def load_graphs(criteria):
    global G, G_multidigraph
    paths = graph_paths[criteria]
    gpkg_path = paths["gpkg"]
    pickle_path = paths["pickle"]
    multidigraph_pickle_path = paths["multidigraph_pickle"]


    print("Loading network ...")
    if os.path.isfile(pickle_path) and os.path.isfile(multidigraph_pickle_path):
        load_net = True
    else:
        load_net = create_pickles_from_graph_criteria(gpkg_path, pickle_path, multidigraph_pickle_path, criteria)
        

    if load_net:
        print("Network loaded")
        G = load_graph_from_pickle(pickle_path)
        G_multidigraph = load_graph_from_pickle(multidigraph_pickle_path)

# print("Loading network ...")
# if(os.path.isfile(final_network_pickle_path) & os.path.isfile(final_network_multidigraph_pickle_path)):
#     load_net = True
# else:
#     load_net = create_pickles_from_graph_pollen(final_network_path, final_network_pickle_path, final_network_multidigraph_pickle_path)

# if(load_net):
#     print("Network loaded")
#     G = load_graph_from_pickle(final_network_pickle_path)
#     G_multidigraph = load_graph_from_pickle(final_network_multidigraph_pickle_path)


@app.route('/data/', methods=['GET'])
def get_layers():
    """Route for layers used in the "Consulter la carte fraîcheur" functionality"""
    layer_id = request.args.get('id')
    print("request", request)
    if layer_id:
        if layer_id == "all":
            try:
                all_id = findMany()
                data = [findOne(id["id"]) for id in all_id]
                if not data:
                    return '', 404
                return jsonify(data)
            except Exception as e:
                print(e)
                return '', 500
        else:
            try:
                print("one layer")
                data = findOne(layer_id)
                if not data:
                    return '', 404
                return jsonify(data)
            except Exception as e:
                print(e)
                return '', 500
    else:
        try:
            results = findMany()
            return jsonify(results)
        except Exception as e:
            print(e)
            return '', 500

@app.route('/itinerary/', methods=['GET'])
def get_itinerary():
    """Route for itinerary calculation"""
    criteria_list = request.args.getlist("criteria[]")

    start_lat = request.args.get("start[lat]")
    start_lon = request.args.get("start[lon]")
    end_lat = request.args.get("end[lat]")
    end_lon = request.args.get("end[lon]")

    start = (float(start_lon), float(start_lat))
    end = (float(end_lon), float(end_lat))

    print(start_lat, start_lon, end_lat, end_lon, criteria_list)
    results = []
    
    try:
        for criteria in criteria_list:
            load_graphs(criteria)  #charger le graphe en fonction du critère
            
            if criteria == "frais":
                geojson_path_IF, geojson_path_length = shortest_path(G, start, end, G_multidigraph)
                results.append({
                    "id": "LENGTH",
                    "name": "Itinéraire le plus court",
                    "geojson": geojson_path_length,
                    "color": " #1b2599 "
                })
                results.append({
                    "id": "IF",
                    "name": "Itinéraire le plus au frais",
                    "geojson": geojson_path_IF, 
                    "color": "#1f8b2c"
                })
            elif criteria == "pollen":
                geojson_path_IF, geojson_path_length = shortest_path(G, start, end, G_multidigraph, 'score_distance_pollen')
                results.append({
                    "id": "LENGTH",
                    "name": "Itinéraire le plus court",
                    "geojson": geojson_path_length,
                    "color": " #1b2599 "
                })
                results.append({
                    "id": "IF",
                    "name": "Itinéraire le moins allergène",
                    "geojson": geojson_path_IF, 
                    "color": "#1f8b2c"
                })
            elif criteria == "bruit":
                geojson_path_IF, geojson_path_length = shortest_path(G, start, end, G_multidigraph, 'score_distance_bruit')
                results.append({
                    "id": "LENGTH",
                    "name": "Itinéraire le plus court",
                    "geojson": geojson_path_length,
                    "color": " #1b2599 "
                })
                results.append({
                    "id": "IF",
                    "name": "Itinéraire le moins bruyant",
                    "geojson": geojson_path_IF, 
                    "color": "#1f8b2c"
                })
            elif criteria == "tourisme":
                geojson_path_IF, geojson_path_length = shortest_path(G, start, end, G_multidigraph, 'score_distance_tourisme')
                results.append({
                    "id": "LENGTH",
                    "name": "Itinéraire le plus court",
                    "geojson": geojson_path_length,
                    "color": " #1b2599 "
                })
                results.append({
                    "id": "IF",
                    "name": "Itinéraire le plus touristique",
                    "geojson": geojson_path_IF, 
                    "color": "#1f8b2c"
                })
            
        return jsonify(results)
    except Exception as e:
        print(e)
        return '', 500

    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3002)