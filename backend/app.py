import os
import sys 
sys.path.append("../")
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
    """
    Loads a graph based on a given criteria by either loading from existing pickle files or 
    creating new pickle files if they do not exist.

    This function first checks if the pickle files for the specified criteria are already 
    available. If they exist, the function loads the graph from these files. If not, it attempts 
    to create the pickle files from the original graph data stored in a GeoPackage file. 
    The function will then load the graph from the created pickle files.

    Parameters:
    -----------
    criteria : str
        The criteria used to identify the specific graph to be loaded (e.g., network type, area, etc.).

    Returns:
    --------
    None
        The function loads the graph data into the global variables `G` and `G_multidigraph`, 
        representing the graph and its multidigraph version, respectively. If the network cannot 
        be loaded, it prints an error message.
    
    Notes:
    -----
    - The function relies on external helper functions: `create_pickles_from_graph_criteria`, 
      `load_graph_from_pickle`.
    - Pickle files are expected to be stored at paths defined in the `graph_paths` dictionary 
      for the given `criteria`.
    """    
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
    """
    Route for retrieving layer data used in the "Consulter la carte fraîcheur" functionality.

    This function handles requests for specific layer data based on the provided layer ID. 
    It can return either a single layer or all layers if the 'id' parameter is set to "all". 
    If no 'id' is provided, it returns all available layers.

    Parameters:
    -----------
    None

    Returns:
    --------
    - If successful, returns a JSON response with the layer data.
    - If no data is found, returns an empty response with a 404 status.
    - In case of an error, returns an empty response with a 500 status.

    Notes:
    -----
    - This function interacts with external functions: `findMany`, `findOne`.
    - The `request.args.get('id')` is used to get the 'id' parameter from the request.
    """    """Route for layers used in the "Consulter la carte fraîcheur" functionality"""
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
    """
    Route for itinerary calculation based on various criteria (e.g., "frais", "pollen", "bruit", "tourisme").
    
    This function computes itineraries between a start and end point for multiple criteria provided in the request. 
    It loads the graph based on the specified criteria and calculates two types of itineraries:
    1. The shortest path ("LENGTH").
    2. The best path based on the specific criteria (e.g., least pollen, least noise, most scenic, etc. - "IF").

    Parameters:
    -----------
    - criteria[] (list of str): A list of criteria that determine how the itinerary should be calculated.
    - start[lat] (float): Latitude of the starting point.
    - start[lon] (float): Longitude of the starting point.
    - end[lat] (float): Latitude of the destination point.
    - end[lon] (float): Longitude of the destination point.

    Returns:
    --------
    - A JSON response with a list of itinerary results for each criteria. Each result contains:
        - id: The ID for the type of itinerary (LENGTH or IF).
        - idcriteria: The ID for the criteria used (e.g., frais, pollen).
        - name: A descriptive name for the itinerary.
        - geojson: The GeoJSON path for the calculated itinerary.
        - color: A color code for displaying the itinerary on a map.

    Notes:
    -----
    - The `load_graphs` function loads the network graph based on the specified criteria.
    - The `shortest_path` function calculates the itineraries based on the loaded graph.
    - If no valid criteria are found or if an error occurs, the request will return a 500 status.
    """
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