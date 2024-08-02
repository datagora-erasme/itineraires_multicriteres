import os
import geopandas as gpd
import pandas as pd
import numpy as np
from scipy.stats import norm
from data_utils import *
import sys

sys.path.append("../")
from global_variable import *

###### CREATE WORKING DIRECTORY FOR ARBRES ######
create_folder("./output_data/tourisme/")

###### TOURISME PREPROCESSING ######

choice = input("Souhaitez-vous mettre à jour le réseau pondéré par les POI touristiques ? OUI ou NON\n")

if choice.upper() == "OUI":
    poi_df = gpd.read_file("./input_data/tourisme/corrige_tourisme_3946.gpkg")
    poi_df = poi_df.to_crs(3946)

    poi_df = poi_df[poi_df["type"] == 'PATRIMOINE_CULTUREL']

    print(poi_df.head())

    #calcule le nombre de POI touristiques par edge buffé
    edges_buffer = gpd.read_file(edges_buffer_path)
    edges_buffer = edges_buffer.to_crs(3946)

    print(edges_buffer.head())

    edges_buffer["tourisme_weight"] = 0

    #buffers autour des POI touristiques
    poi_df['buffer'] = poi_df.geometry.buffer(10)  #10 mètres
    poi_buffer = poi_df.set_geometry('buffer')

    #intersection entre les buffers des POI et les edges_buffer
    intersections = gpd.sjoin(edges_buffer, poi_buffer, how="inner", predicate='intersects')
    print(intersections.head())

    #compte le nombre de POI touristiques par edge buffé
    tourisme_weight = intersections.groupby(["u", "v", "key"]).size().reset_index(name='count')
    print(tourisme_weight.head())

    edges_buffer['count'] = 0.01

    edges_buffer = edges_buffer.merge(tourisme_weight, on=['u', 'v', 'key'], how='left')
    edges_buffer['count'] = edges_buffer['count_y'].fillna(0.01)
    edges_buffer.drop(columns=['count_x', 'count_y'], inplace=True)

    #multiplier le count par une grande valeur pour meilleure discrimination
    #voir s'il faut inverser, avoir le score le plus grand qui va avoir le score final le plus petit?

    print(edges_buffer.head())
    print(edges_buffer[edges_buffer['count'] != 0.01].shape)
    print(edges_buffer[edges_buffer['count'] == 0.01].shape)
    print(edges_buffer['count'].describe())

    #edge_buffer_wo_zeros = edges_buffer[edges_buffer['count'] != 0]
    #print(edge_buffer_wo_zeros['count'].describe())

    #converti les colonnes qui ne sont pas des géométries en chaînes de caractères
    for col in edges_buffer.columns:
        if col != 'geometry':
            edges_buffer[col] = edges_buffer[col].astype(str)

    edges_buffer.to_file(edges_buffer_tourisme_prop_path, driver="GPKG", layer="edges_buffer")

