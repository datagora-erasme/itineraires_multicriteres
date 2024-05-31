import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import json
import sys
sys.path.append("../")
from global_variable import *

def findMany():
    all_data = [{
        "id": data_name,
        "name": data_param["name"],
        "marker_option": data_param["marker_option"]
    } for data_name, data_param in data_params.items() if "marker_option" in data_param and data_param["onMap"]]
    return all_data


def findOne(id):
    for data_name, data_param in data_params.items():
        if data_name == id:
            path = data_param['geojson_path']
            print(path)
            with open(path) as f:
                geojson = json.load(f)

            if("marker_option" in data_param):
                markerOption = data_param['marker_option']
                return {
                    'geojson': geojson,
                    'markerOption': markerOption,
                    'name': data_param["name"],
                    'id': id
                }
            else:
                return {
                    'geojson': geojson,
                    'name': data_param["name"],
                    'id': id
                }
    return None
