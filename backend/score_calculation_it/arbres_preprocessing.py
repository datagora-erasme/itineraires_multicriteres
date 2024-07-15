import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
import numpy as np
from scipy.stats import norm
from data_utils import *
from shapely.geometry import Point
import sys
sys.path.append("../")
from global_variable import *

###### CREATE WORKING DIRECTORY FOR ARBRES ######

create_folder("./output_data/arbres/")

###### ARBRES PREPROCESSING ######

def map_raep(famille):
    return allergene_dict.get(famille, 0)

choice = input("Souhaitez-vous mettre à jour le réseau pondéré par les arbres ? OUI ou NON\n")

if choice.upper() == "OUI":
    #arbres d'alignements
    arbres = gpd.read_file(data_params["arbres"]["gpkg_path"])
    arbres = arbres.to_crs(3946)

    print(arbres.head())
    print(arbres.columns)

    #arbres des parcs, dataset additonnel fourni par les communes
    arbres_parcs = gpd.read_file('./input_data/arbres/arbre_vdl_opendata_juin_2024.shp')
    arbres_parcs = arbres_parcs.to_crs(epsg=3946)

    #arbres['lat'] = arbres['lat'].apply(lambda x: float(x.replace(',', '.')) if isinstance(x, str) else x)
    #arbres['lon'] = arbres['lon'].apply(lambda x: float(x.replace(',', '.')) if isinstance(x, str) else x)

    #concatenation des deux datasets
    arbres_parcs = arbres_parcs.rename(columns={'Type_en_fr': 'essencefrancais'})
    arbres_parcs = arbres_parcs.rename(columns={'Type_en_la': 'essencelatin'})
    arbres_parcs = arbres_parcs.rename(columns={'Genre': 'genre'})
    arbres_parcs = arbres_parcs.rename(columns={'Essence': 'essence'})
    arbres_parcs = arbres_parcs.rename(columns={'Hauteur_to': 'hauteurtotale_m'})

    arbres = pd.concat([arbres, arbres_parcs], ignore_index=True)

    arbres.dropna(subset=['codeinsee'], inplace=True)
    arbres['codeinsee'] = arbres['codeinsee'].round().astype(int)
    
    arbres['famille'] = arbres['essencefrancais'].str.split().str[0]
    
    allergene_dict = {
        'Noisetier': 0, 'Cyprès': 0, 'Aulne': 0, 'Peuplier': 0, 'Frêne': 0,
        'Bouleau': 0, 'Platane': 0, 'Chêne': 0, 'Charme': 0, 'Érable': 0,
        'Bacchari': 0, 'Thuya': 0, 'Noyer': 0, 'Mûrier': 0, 'Saule': 0,
        'Orme': 0, 'Hêtre': 0, 'Châtaignier': 1, 'Olivier': 3, 'Tilleul': 2,
        'Cade': 3, 'Troène': 2, 'Pin': 0,
    }
    
    arbres['raep'] = arbres['famille'].apply(map_raep)
    
    arbres = arbres[arbres['raep'] != 0]
    arbres = arbres[arbres["essencefrancais"] != "Emplacement libre"] 
    arbres = arbres.dropna(axis=1, how='all')
    
    print(arbres.head())

    arbres.to_file(arbres_classes_pollen_path, driver="GPKG", layer="arbres")

    #calcule la gaussienne pour chaque edge buffé en se basant sur l'indice allergisant (raep) des arbres
    edges_buffer = gpd.read_file(edges_buffer_path)
    edges_buffer = edges_buffer.to_crs(3946)

    print(edges_buffer.head())

    edges_buffer["arbres_weight"] = 0

    #buffers autour des arbres
    arbres['buffer'] = arbres.geometry.buffer(30)  #30 mètres
    arbres_buffer = arbres.set_geometry('buffer')

    #intersection entre les buffers des arbres et les edges_buffer
    intersections = gpd.sjoin(edges_buffer, arbres_buffer, how="inner", predicate='intersects')
    print(intersections.head())

    if not intersections.empty:
        mean_raep = intersections.groupby(['u', 'v', 'key'])['raep'].mean().reset_index()
        edges_buffer = pd.merge(edges_buffer, mean_raep, on=['u', 'v', 'key'], how='left')
        edges_buffer['arbres_weight'] = edges_buffer['raep'].fillna(0)
        edges_buffer.drop(columns=['raep'], inplace=True)

    print(edges_buffer.head())
    print(edges_buffer[edges_buffer['arbres_weight'] != 0].shape)
    print(edges_buffer[edges_buffer['arbres_weight'] == 'NULL'].shape)

    
    edges_buffer.to_file(edges_buffer_arbres_pollen_prop_path, driver="GPKG", layer="edges_buffer")