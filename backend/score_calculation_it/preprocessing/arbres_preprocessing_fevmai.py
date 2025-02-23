import sys
import os
sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../script_python")
import geopandas as gpd
import pandas as pd
import numpy as np
from scipy.stats import norm
from function_utils import *
from shapely.geometry import Point
import requests
import json
from global_variable import *

###### CREATE WORKING DIRECTORY FOR ARBRES ######

create_folder("./../output_data/arbres/")

###### ARBRES PREPROCESSING ######

def map_raep(famille):
    """
    Maps a tree family to an allergenic index (RAEP).

    The RAEP index is retrieved from the `allergene_dict` dictionary, which 
    associates each tree family with a specific value representing its allergenic 
    potential. If the tree family is not found in `allergene_dict`, the function 
    returns 0 by default.

    Args:
        famille (str): The name of the tree family in French.

    Returns:
        int: The corresponding RAEP allergenic index.
    """
    return allergene_dict.get(famille, 0)

choice = input("Would you like to update the tree-weighted network? YES or NO\n")

if choice.upper() == "YES":
    #arbres d'alignements
    arbres = gpd.read_file(data_params["arbres"]["gpkg_path"])
    arbres = arbres.to_crs(3946)


    # Trees in Lyon's parks, additional non-public dataset provided by municipalities
    arbres_parcs = gpd.read_file('./../input_data/arbres/arbre_vdl_opendata_juin_2024.shp')
    arbres_parcs = arbres_parcs.to_crs(epsg=3946)

    # Concatenation of the two datasets
    arbres_parcs = arbres_parcs.rename(columns={'Type_en_fr': 'essencefrancais'})
    arbres_parcs = arbres_parcs.rename(columns={'Type_en_la': 'essencelatin'})
    arbres_parcs = arbres_parcs.rename(columns={'Genre': 'genre'})
    arbres_parcs = arbres_parcs.rename(columns={'Essence': 'essence'})
    arbres_parcs = arbres_parcs.rename(columns={'Hauteur_to': 'hauteurtotale_m'})

    arbres = pd.concat([arbres, arbres_parcs], ignore_index=True)


    # Trees from Rilleux, additional non-public dataset provided by the municipalities
    url = "https://download.data.grandlyon.com/files/rdata/sortons_au_frais/arbres_urbains.json"
    response = requests.get(url)
    content = response.content.decode('utf-8-sig')
    data = json.loads(content)
    values = data['values']
    df = pd.DataFrame(values)

    rilleux = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))
    rilleux.set_crs(epsg=4326, inplace=True)
    rilleux = rilleux.to_crs(3946)

    latin_to_french = {
    'Corylus': 'Noisetier',
    'Cupressus': 'Cyprès',
    'Alnus': 'Aulne',
    'Populus': 'Peuplier',
    'Fraxinus': 'Frêne',
    'Betula': 'Bouleau',
    'Platanus': 'Platane',
    'Quercus': 'Chêne',
    'Carpinus': 'Charme',
    'Acer': 'Erable',
    'Baccharis': 'Bacchari',
    'Thuja': 'Thuya',
    'Juglans': 'Noyer',
    'Morus': 'Mûrier',
    'Salix': 'Saule',
    'Ulmus': 'Orme',
    'Fagus': 'Hêtre',
    'Castanea': 'Châtaignier',
    'Olea': 'Olivier',
    'Tilia': 'Tilleul',
    'Juniperus': 'Cade',
    'Ligustrum': 'Troène',
    'Pinus': 'Pin',
    }

    rilleux['genre_fr'] = rilleux['genre'].map(latin_to_french)
    rilleux = rilleux.dropna(subset=['genre_fr'])
    rilleux = rilleux.rename(columns={'genre_fr': 'essencefrancais'})

    arbres = pd.concat([arbres, rilleux], ignore_index=True)


    arbres.dropna(subset=['codeinsee'], inplace=True)
    arbres['codeinsee'] = arbres['codeinsee'].round().astype(int)
    
    arbres['famille'] = arbres['essencefrancais'].str.split().str[0]
    
    allergene_dict = {
    'Noisetier': 3,
    'Cyprès': 5,
    'Aulne': 4,
    'Peuplier': 2,
    'Frêne': 4,
    'Bouleau': 5,
    'Platane': 3,
    'Chêne': 3,
    'Charme': 3,

    'Érable': 2,
    'Erable': 2,
    'Thuya': 1,
    'Noyer': 1,
    'Mûrier': 2,
    'Saule': 3,
    'Orme': 1,
    'Hêtre': 2,

    'Bacchari': 0,
    'Châtaignier': 0,
    'Olivier': 0,
    'Tilleul': 0,
    'Cade': 0,
    'Troène':0,
    'Pin': 0,
    }
    
    arbres['raep'] = arbres['famille'].apply(map_raep)
    
    arbres = arbres[arbres['raep'] != 0]
    arbres = arbres[arbres["essencefrancais"] != "Emplacement libre"] 
    arbres = arbres.dropna(axis=1, how='all')
    
    print(arbres.head())
    print(arbres.shape)

    arbres.to_file(arbres_classes_pollen_path, driver="GPKG", layer="arbres")

    # Calculates the average allergenic index (RAEP) for each buffered edge based on nearby trees
    edges_buffer = gpd.read_file(edges_buffer_path)
    edges_buffer = edges_buffer.to_crs(3946)

    print(edges_buffer.head())

    edges_buffer["arbres_weight"] = 0

    arbres['buffer'] = arbres.geometry.buffer(20)  #20 mètres
    arbres_buffer = arbres.set_geometry('buffer')

    # Intersection between tree buffers and edges_buffer
    intersections = gpd.sjoin(edges_buffer, arbres_buffer, how="inner", predicate='intersects')
    print(intersections.head())

    if not intersections.empty:
        mean_raep = intersections.groupby(['u', 'v', 'key'])['raep'].mean().reset_index()
        edges_buffer = pd.merge(edges_buffer, mean_raep, on=['u', 'v', 'key'], how='left')
        edges_buffer['arbres_weight'] = edges_buffer['raep'].fillna(0)
        edges_buffer['arbres_weight'] = edges_buffer['arbres_weight'].replace('NULL', 0)
        edges_buffer.drop(columns=['raep'], inplace=True)

    print(edges_buffer.head())
    print(edges_buffer[edges_buffer['arbres_weight'] != 0].shape)
    print(edges_buffer[edges_buffer['arbres_weight'] == 'NULL'].shape)

    
    edges_buffer.to_file(edges_buffer_arbres_pollen_prop_path_fevmai, driver="GPKG", layer="edges_buffer")