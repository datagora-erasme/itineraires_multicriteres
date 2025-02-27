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
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
CORS(app)

def load_graphs(criterion):
    """
    Loads the graph data for the specified criterion from pickled files.
    If the pickle files do not exist, it creates them by calling `create_pickles_from_graph_criterion()`.
    Finally, it loads the graphs from the pickled files using `load_graphs_from_pickles()`.
    
    Parameters:
    - `criterion`: The criterion to load the graph data for.
    """
    global graphs_local_cache, graph_paths
    pickle_graph_path = graph_paths[criterion]["pickle"]
    pickle_multidigraph_path = graph_paths[criterion]["multidigraph_pickle"]

    print(f"Loading network for {criterion}...")

    # Check if pickle files already exist
    if not (os.path.isfile(pickle_graph_path) and os.path.isfile(pickle_multidigraph_path)):
        print(f"Pickle files not found for {criterion}, creating them...")
        try:
            create_pickles_from_graph_criterion(criterion)
        except Exception as e:
            return

    load_graphs_from_pickles(criterion)

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
    global graph_paths

    criteria_list = request.args.getlist("criteria[]")

    start_lat = request.args.get("start[lat]")
    start_lon = request.args.get("start[lon]")
    end_lat = request.args.get("end[lat]")
    end_lon = request.args.get("end[lon]")

    start = (float(start_lon), float(start_lat))
    end = (float(end_lon), float(end_lat))

    print(start_lat, start_lon, end_lat, end_lon, criteria_list)

    origin_node, destination_node = nearest_nodes(start, end)

    results = []
    try:
        for criterion in criteria_list:
            load_graphs(criterion)  #charger le graphe en fonction du critère
            print(datetime.now(), f"Calculating itinerary for {criterion}...")

            geojson = shortest_path_criterion(criterion, origin_node, destination_node)
            path_score = path_mean_score_criterion(criterion, geojson)
            results.append({
                "id": "IF",
                "idcriteria": criterion,
                "name": graph_paths[criterion]["label"],
                "geojson": geojson, 
                "color": "#1f8b2c",
                "score": path_score
            })
            
        load_graphs("length")
        geojson = shortest_path_length(origin_node, destination_node)
        path_score = path_mean_score_length(geojson, criteria_list)
        results.append({
            "id": "LENGTH",
            "idcriteria": "length",
            "name": graph_paths["length"]["label"],
            "geojson": geojson,
            "color": " #1b2599 ",
            "score": path_score
        })

        return jsonify(results)
    except Exception as e:
        print('error:', e)
        return '', 500
    
@app.errorhandler(500)
def internal_server_error(e):
    """Handle internal server error (500) and shows custom HTML page"""
    print('error 500:', e)
    return render_template('./public/error500.html'), 500

@app.route('/force_error')
def force_error():
    """Route to force a 500 error for testing"""
    raise Exception("This is a forced error to test the 500 error handler.")


def preload_graphs():
    """    
    Preloads the graphs for different criteria (e.g. "bruit", "tourisme") into the local cache.
    It uses a thread pool executor to parallelize the loading process, and only loads the graphs if they are not already present in the cache.
    """    
    global graph_paths, graphs_local_cache

    futures = []
    with ThreadPoolExecutor() as executor:
        for criterion in graph_paths:
            pickle_graph_path = graph_paths[criterion]["pickle"]
            pickle_multidigraph_path = graph_paths[criterion]["multidigraph_pickle"]
            # Only preload if not already in cache.
            if ((pickle_graph_path not in graphs_local_cache) or (graphs_local_cache[pickle_graph_path] is None)) or ((pickle_multidigraph_path not in graphs_local_cache) or (graphs_local_cache[pickle_multidigraph_path] is None)):
                print(datetime.now(), f"Pre-loading graphs for {criterion}.")
                futures.append(executor.submit(load_graphs, criterion))
        # Wait for all tasks to finish.
        for future in futures:
            future.result()

# Pre-load graphs on application startup
preload_graphs()

# Launch application
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=3002)