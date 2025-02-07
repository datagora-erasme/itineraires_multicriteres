import sys
import os
sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../script_python")
from backend.script_python.function_utils import create_folder
import geopandas as gpd
import pandas as pd
import numpy as np
from scipy.stats import norm
from function_utils import *
from global_variable import *

###### CREATE WORKING DIRECTORY FOR ARBRES ######
create_folder("./output_data/tourisme/")

###### TOURISME PREPROCESSING ######

choice = input("Do you want to update the network weighted by tourist POIs? YES or NO\n")

if choice.upper() == "YES":
    poi_df = gpd.read_file("./input_data/tourisme/corrige_tourisme_3946.gpkg")
    poi_df = poi_df.to_crs(3946)

    poi_df = poi_df[poi_df["type"] == 'PATRIMOINE_CULTUREL']

    print(poi_df.head())

    # Calculate the number of tourist POIs per buffered edge
    edges_buffer = gpd.read_file(edges_buffer_path)
    edges_buffer = edges_buffer.to_crs(3946)

    print(edges_buffer.head())

    edges_buffer["tourisme_weight"] = 0

    # Buffers around tourist POIs
    poi_df['buffer'] = poi_df.geometry.buffer(20)  # 20 mètres
    poi_buffer = poi_df.set_geometry('buffer')

    # Intersection between the POI buffers and the edges_buffer
    intersections = gpd.sjoin(edges_buffer, poi_buffer, how="inner", predicate='intersects')
    print(intersections.head())

    # Count the number of tourist POIs per buffered edge
    tourisme_weight = intersections.groupby(["u", "v", "key"]).size().reset_index(name='count')
    print(tourisme_weight.head())

    edges_buffer['count'] = 0.01

    edges_buffer = edges_buffer.merge(tourisme_weight, on=['u', 'v', 'key'], how='left')
    edges_buffer['count'] = edges_buffer['count_y'].fillna(0.01) * 100
    edges_buffer.drop(columns=['count_x', 'count_y'], inplace=True) 

    print(edges_buffer.head())
    print(edges_buffer[edges_buffer['count'] != 0.01].shape)
    print(edges_buffer[edges_buffer['count'] == 0.01].shape)
    print(edges_buffer['count'].describe())

    #edge_buffer_wo_zeros = edges_buffer[edges_buffer['count'] != 0]
    #print(edge_buffer_wo_zeros['count'].describe())

    # Convert columns that are not geometries into strings
    for col in edges_buffer.columns:
        if col != 'geometry':
            edges_buffer[col] = edges_buffer[col].astype(str)

    edges_buffer.to_file(edges_buffer_tourisme_prop_path, driver="GPKG", layer="edges_buffer")

