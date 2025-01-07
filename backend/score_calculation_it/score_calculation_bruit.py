#%%
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
import osmnx as ox
from data_utils import *
import sys
sys.path.append("../")
from global_variable import *
from sklearn.preprocessing import MinMaxScaler
from app import load_graphs
import pickle



def total_score(input_path, output_path, score_columns):
    """Calcul du score total de bruit en fonction des colonnes spécifiées"""
    edges_data = gpd.read_file(input_path)
    
    print(f"Colonnes dans {input_path} : {edges_data.columns}")
    edges_data["total_score_bruit"] = edges_data[score_columns].sum(axis=1) 
    print(f"Calcul du total_score_bruit terminé.")

    # Sauvegarder le fichier de scores
    edges_data.to_file(output_path, driver="GPKG")
    print(f"Le fichier de scores a été sauvegardé sous {output_path}.")

def score_distance(input_path, output_path):
    """Calculate the score by distance for each edge, favoring shorter segments"""
    edges_data = gpd.read_file(input_path)  

    edges_data["score_distance_bruit"] = edges_data["DN"] * edges_data["length"]
    
    print(f"Calcul du score_distance_bruit terminé.")

    # Sauvegarder le fichier des scores pondérés par la distance
    edges_data.to_file(output_path, driver="GPKG")
    print(f"Le fichier de score_distance_bruit a été sauvegardé sous {output_path}.")

def score_bruit(input_path, output_path):
    """Calculer un score de bruit de 0 à 10"""
    edges_data = gpd.read_file(input_path)
    
    min_score = edges_data["total_score_bruit"].min()  
    max_score = edges_data["total_score_bruit"].max()  
    slope = (0 - 10) / (max_score - min_score)  
    origin_ordinate = -slope * max_score  
    
    # Appliquer le calcul du score de bruit
    edges_data["bruit_score"] = edges_data["total_score_bruit"].apply(lambda x: round(slope * x + origin_ordinate, 2))

    print(f"Calcul du bruit_score terminé.")

    # Sauvegarder le fichier du score de bruit
    edges_data.to_file(output_path, driver="GPKG")
    print(f"Le fichier de bruit_score a été sauvegardé sous {output_path}.")

def create_graph_bruit(graph_path, edges_buffered_path, graph_output_path):
    """Créer un graphe avec les scores de bruit appliqués"""
    graph_e = gpd.read_file(graph_path, layer="edges")
    graph_n = gpd.read_file(graph_path, layer="nodes")
    edges_buffered_data = gpd.read_file(edges_buffered_path)
    
    graph_e = graph_e.set_index(["u", "v", "key"])
    edges_buffered_data = edges_buffered_data.set_index(["u", "v", "key"])
    graph_n = graph_n.set_index(["osmid"])

    # Appliquer les scores au graphe
    graph_e["total_score_bruit"] = edges_buffered_data["total_score_bruit"]
    graph_e["score_distance_bruit"] = edges_buffered_data["score_distance_bruit"]
    graph_e["bruit_score"] = edges_buffered_data["bruit_score"]

    # Générer le graphe 
    G = ox.graph_from_gdfs(graph_n, graph_e)

    # Sauvegarder le graphe final
    ox.save_graph_geopackage(G, graph_output_path)
    print(f"Le graphe de bruit a été sauvegardé sous {graph_output_path}")

# Exécution des fonctions
total_score(edges_buffer_bruit_wavg_path, edges_buffer_total_score_path, ["DN_scaled"])
score_distance(edges_buffer_total_score_path, edges_buffer_total_score_distance_path)
score_bruit(edges_buffer_total_score_distance_path, edges_buffer_total_score_distance_bruit_path)
create_graph_bruit(metrop_network_bouding_path, edges_buffer_total_score_distance_bruit_path, "./output_data/network/graph/final_network_bruit.gpkg")

# Télécharger les pickles pour le bruit 
load_graphs("bruit")