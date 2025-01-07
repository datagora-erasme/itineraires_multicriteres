import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
from models.data import *
from load_graph import *
from models.itinerary import *
from global_variable import *

app = Flask(__name__)
CORS(app)

"""
The final graph is loaded into a pickle file in order to keep it in RAM. 
It allows to reduce the time between request and response (the files took several seconds to open).
"""

G = None
G_multidigraph = None

current_month = datetime.now().month
print("current_month", current_month)

graph_paths = {
    "frais": {
        "gpkg": final_network_path, 
        "pickle": final_network_pickle_path,
        "multidigraph_pickle": final_network_multidigraph_pickle_path
    },
    "pollen": {
        "gpkg": final_network_pollen_fevmai_path if current_month >= 2 and current_month <= 5 else final_network_pollen_path,  
        "pickle": final_network_pickle_pollen_fevmai_path if current_month >= 2 and current_month <= 5 else final_network_pickle_pollen_path,
        "multidigraph_pickle": final_network_multidigraph_pickle_pollen_fevmai_path if current_month >= 2 and current_month <= 5 else final_network_multidigraph_pickle_pollen_path
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

    print(f"Loading network for {criteria}...")

    # Vérifiez si les fichiers pickle existent déjà
    if os.path.isfile(pickle_path) and os.path.isfile(multidigraph_pickle_path):
        print(f"Pickle files found for {criteria}, loading them.")
        load_net = True
    else:
        print(f"Pickle files not found for {criteria}, creating them...")
        try:
            load_net = create_pickles_from_graph_criteria(gpkg_path, pickle_path, multidigraph_pickle_path, criteria)
            if load_net:
                print(f"Pickle files for {criteria} created successfully.")
            else:
                print(f"Failed to create pickle files for {criteria}.")
        except Exception as e:
            print(f"Error while creating pickle files for {criteria}: {e}")
            load_net = False

    if load_net:
        print(f"Network loaded successfully for {criteria}.")
        G = load_graph_from_pickle(pickle_path)
        G_multidigraph = load_graph_from_pickle(multidigraph_pickle_path)
    else:
        print(f"Network loading failed for {criteria}.")



@app.route('/data/', methods=['GET'])
def get_layers():
    """Route for layers used in the "Consulter la carte fraîcheur" functionality"""
    layer_id = request.args.get('id')
    print("request", request)
    if layer_id:
        if layer_id == "all":
            print("tourisme all")
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
            print("tourisme")
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
                    "idcriteria": "fraislength",
                    "name": "Itinéraire le plus court",
                    "geojson": geojson_path_length,
                    "color": " #1b2599 "
                })
                results.append({
                    "id": "IF",
                    "idcriteria": "frais",
                    "name": "Itinéraire le plus au frais",
                    "geojson": geojson_path_IF, 
                    "color": "#1f8b2c"
                })
            elif criteria == "pollen":
                geojson_path_IF, geojson_path_length = shortest_path(G, start, end, G_multidigraph, 'score_distance_pollen')
                results.append({
                    "id": "LENGTH",
                    "idcriteria": "pollenlength",
                    "name": "Itinéraire le plus court",
                    "geojson": geojson_path_length,
                    "color": " #1b2599 "
                })
                results.append({
                    "id": "IF",
                    "idcriteria": "pollen",
                    "name": "Itinéraire le moins allergène",
                    "geojson": geojson_path_IF, 
                    "color": "#1f8b2c"
                })
            elif criteria == "bruit":
                geojson_path_IF, geojson_path_length = shortest_path(G, start, end, G_multidigraph, 'score_distance_bruit')
                results.append({
                    "id": "LENGTH",
                    "idcriteria": "bruitlength",
                    "name": "Itinéraire le plus court",
                    "geojson": geojson_path_length,
                    "color": " #1b2599 "
                })
                results.append({
                    "id": "IF",
                    "idcriteria": "bruit",
                    "name": "Itinéraire le moins bruyant",
                    "geojson": geojson_path_IF, 
                    "color": "#1f8b2c"
                })
            elif criteria == "tourisme":
                geojson_path_IF, geojson_path_length = shortest_path(G, start, end, G_multidigraph, 'score_distance_tourisme')
                results.append({
                    "id": "LENGTH",
                    "idcriteria": "tourismelength",
                    "name": "Itinéraire le plus court",
                    "geojson": geojson_path_length,
                    "color": " #1b2599 "
                })
                results.append({
                    "id": "IF",
                    "idcriteria": "tourisme",
                    "name": "Itinéraire le plus touristique",
                    "geojson": geojson_path_IF, 
                    "color": "#1f8b2c"
                })
            
        return jsonify(results)
    except Exception as e:
        print(e)
        return '', 500
    
@app.errorhandler(500)
def internal_server_error(e):
    """Handle internal server error (500) and shows custom HTML page"""
    return render_template('./public/error500.html'), 500

@app.route('/force_error')
def force_error():
    """Route to force a 500 error for testing"""
    raise Exception("This is a forced error to test the 500 error handler.")

# Lancer appli
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3002)