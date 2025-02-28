import os
from pathlib import Path
import sys
sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../script_python")
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import osmnx as ox
from global_variable import *

def prepare_edges_length():
    # Charger les fichiers GPKG
    frais = gpd.read_file(edges_buffer_total_score_distance_freshness_path)
    tourisme = gpd.read_file(edges_buffer_total_score_distance_tourisme_path)
    bruit = gpd.read_file(edges_buffer_total_score_distance_bruit_path)
    pollen = gpd.read_file(edges_buffer_total_score_distance_pollen_path)

    # Afficher les colonnes avant fusion
    print("Colonnes de frais:", frais.columns)
    print("Colonnes de tourisme:", tourisme.columns)
    print("Colonnes de bruit:", bruit.columns)
    print("Colonnes de pollen:", pollen.columns)

    # Liste des fichiers supplémentaires et colonnes à ajouter
    fichiers = [
        (tourisme, ["score_distance_tourisme", "tourisme_score"]),
        (bruit, ["score_distance_bruit", "bruit_score"]),
        (pollen, ["score_distance_pollen", "pollen_score"])
    ]

    df_final = frais.copy()
    for df, cols in fichiers:
        # Vérifier que les fichiers secondaires ont bien les colonnes "u", "v", "key"
        df_subset = df[["u", "v", "key", "geometry"] + cols]
        df_final = df_final.merge(df_subset, on=["u", "v", "key", "geometry"], how="left")

    # Liste des colonnes à conserver après fusion
    column = ["u", "v", "key", "osmid", "length", "from", "to", 
              "score_distance_13", "total_score_13", "freshness_score_13", "geometry",
              "score_distance_tourisme", "tourisme_score", 
              "score_distance_bruit", "bruit_score",
              "score_distance_pollen", "pollen_score"]

    # Sélectionner uniquement les colonnes nécessaires
    df_final = df_final[column]

    # Vérification des colonnes après filtrage
    print("Colonnes finales après filtrage:", df_final.columns)

    # Nombre de lignes après filtrage
    print(f"Nombre de lignes : {len(df_final)}")

    # Sauvegarde en GPKG
    df_final.to_file(edges_buffer_length_path, driver="GPKG")
    print(f"Fichier sauvegardé avec succès : {edges_buffer_length_path}")




def create_graph_length(graph_path, edges_buffered_path, graph_output_path):
    """Create a graph with applied noise scores and save only edges and nodes layers"""

    # Charger les nœuds et arêtes du graphe initial
    graph_e = gpd.read_file(graph_path, layer="edges")
    graph_n = gpd.read_file(graph_path, layer="nodes")

    # Charger les scores (edges_buffered_data)
    edges_buffered_data = gpd.read_file(edges_buffered_path)

    # Mettre les index sur les bonnes colonnes
    graph_e = graph_e.set_index(["u", "v", "key"])
    edges_buffered_data = edges_buffered_data.set_index(["u", "v", "key"])
    graph_n = graph_n.set_index(["osmid"])

    # Appliquer les scores aux arêtes
    for col in ["score_distance_13", "freshness_score_13", "score_distance_pollen", "pollen_score",
                "score_distance_bruit", "bruit_score", "score_distance_tourisme", "tourisme_score"]:
        if col in edges_buffered_data.columns:  # Vérifier si la colonne existe avant d'appliquer
            graph_e[col] = edges_buffered_data[col]

    # Générer le graphe
    G = ox.graph_from_gdfs(graph_n, graph_e)

    # Supprimer l'ancien fichier s'il existe
    if Path(graph_output_path).exists():
        os.remove(graph_output_path)

    # Extraire les nouveaux nœuds et arêtes
    graph_n, graph_e = ox.graph_to_gdfs(G)

    # Sauvegarder uniquement les couches `edges` et `nodes`
    graph_n.to_file(graph_output_path, layer="nodes", driver="GPKG")
    graph_e.to_file(graph_output_path, layer="edges", driver="GPKG")

    print(f"Le fichier {graph_output_path} contient uniquement les couches 'edges' et 'nodes'.")

prepare_edges_length()
create_graph_length(metrop_network_bouding_path, edges_buffer_length_path, final_network_length_path)