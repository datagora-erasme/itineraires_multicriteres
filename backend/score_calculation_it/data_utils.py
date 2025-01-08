import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
import multiprocessing as mp
import numpy as np
from shapely.wkt import loads, dumps
from shapely.validation import make_valid
from shapely.geometry import Polygon, MultiPolygon
import os
import subprocess
from osgeo import ogr
from sklearn.preprocessing import MinMaxScaler



def create_folder(folder_path):
    exist = os.path.exists(folder_path)
    if not exist:
        os.makedirs(folder_path)
        print(f"{folder_path} created")

def clip_wrapper(chunk, overlay):
    return gpd.clip(chunk, overlay)

def dissolving(input_path, output_path, layer):
    data = gpd.read_file(input_path, layer=layer)

    disolved_data = data.dissolve()

    disolved_data.to_file(output_path, layer=layer, driver="GPKG")
    
def clip_data(edges_path, data_path, output_path, nbre_cpu, layer):
    edges = gpd.read_file(edges_path)
    data = gpd.read_file(data_path)

    data = data.to_crs(3946)

    data_chunks = np.array_split(data, nbre_cpu)
    print("start clipping")
    with mp.Pool(processes=nbre_cpu) as pool:
        clipped_chunks = pool.starmap(clip_wrapper, [(chunk, edges) for chunk in data_chunks])

    print("start concat")
    clipped_data = pd.concat(clipped_chunks)

    print("saving file")
    clipped_data.to_file(output_path, driver="GPKG", layer=layer)

def classification(input_path, output_folder, fn, data_name):
    """Separate gpkg file into several gpkg file according the the classification made by fn"""
    data = gpd.read_file(input_path)
    data["class"] = data.apply(fn, axis=1)

    classes = data["class"].unique().tolist()
    for clas in classes:
        class_gpd = data[data["class"] == clas]
        class_gpd.to_file(f"{output_folder}{data_name}_{clas}.gpkg", driver="GPKG", layer=f"{data_name}_{clas}")

def bufferize(input_path, output_path, layer, buffer_size):
    layer_gpd = gpd.read_file(input_path, layer=layer)

    layer_gpd = layer_gpd.to_crs(3946)

    buffered_features = layer_gpd.geometry.apply(lambda x: x.buffer(buffer_size))

    layer_buffer = gpd.GeoDataFrame(layer_gpd.drop("geometry", axis=1), geometry=buffered_features)
    layer_buffer.crs = layer_gpd.crs

    layer_buffer.to_file(output_path, driver="GPKG", layer=layer)

def bufferize_with_column(input_path, output_path, layer, buffer_size_column, default_value, coeff_buffer=1):
    layer_gpd = gpd.read_file(input_path, layer=layer)
    layer_gpd = layer_gpd.to_crs(3946)

    layer_gpd[buffer_size_column] = layer_gpd[buffer_size_column].fillna(default_value)

    def buffer_with_size(row):
        buffer_size = row[buffer_size_column]*coeff_buffer
        return row.geometry.buffer(buffer_size)

    buffered_features = layer_gpd.apply(buffer_with_size, axis=1)

    layer_buffer = gpd.GeoDataFrame(layer_gpd.drop("geometry", axis=1), geometry=buffered_features)
    layer_buffer.crs = layer_gpd.crs

    layer_buffer.to_file(output_path, driver="GPKG", layer=layer)

def explode_polygon(data_path, output_path):
    data = gpd.read_file(data_path)
    polygons = data.explode()
    polygons = polygons.to_crs(3946)
    polygons.to_file(output_path)

def area_prop(x):
    tot_area = x["area"].sum()
    class_area = x[x["class"] != 1]["area"].sum()
    x_class = x["class"].unique().tolist()
    x_canop = None
    canop= None
    if("indiccanop" in x.columns):
        x_canop = x["indiccanop"].unique().tolist()
        canop = next((val for val in x_canop if type(val == float)), 0)

    first_non_one = next((val for val in x_class if val != 1), "low")

    # print(class_area)

    return pd.Series({
        "prop": round(class_area/tot_area, 2),
        "area": tot_area,
        "class": first_non_one,
        "canop" : canop
        })

def calculate_area_proportion(edges_path, data_path, name, output_path, layer="sample_network", parcs=False):
    edges = gpd.read_file(edges_path, layer=layer)
    data = gpd.read_file(data_path)
    print(edges.columns)

    edges.geometry = [loads(dumps(geom, rounding_precision=3)) for geom in edges.geometry]
    data.geometry =  [loads(dumps(geom, rounding_precision=3)) for geom in data.geometry]

    overlay_edges = gpd.overlay(edges, data, how="identity", keep_geom_type=True) 

    print(overlay_edges)

    overlay_serie = gpd.GeoSeries(overlay_edges["geometry"])

    overlay_edges["area"] = overlay_serie.area

    overlay_edges[["u", "v", "key"]] = overlay_edges[["u", "v", "key"]].astype(int)

    overlay_edges = overlay_edges.set_index(["u", "v", "key"])

    overlay_edges["class"] = overlay_edges["class"].fillna(1)

    print("calculating prop area")
    grouped = overlay_edges.groupby(["u", "v", "key"], group_keys=True).apply(area_prop)

    edges = edges.set_index(["u", "v", "key"])

    edges[f"{name}_prop"] = grouped["prop"]

    if(parcs):
        edges["parcs_class"] = grouped["class"]
        edges["canop"] = grouped["canop"]

    print("to file")
    edges.to_file(output_path, driver="GPKG", layer=layer)

def calculate_many_prop(data_folder_path, edges_path, layer):
    for filename in os.listdir(data_folder_path):
        file_path = os.path.join(data_folder_path, filename)
        data_name = file_path.split("/")[3].split(".")[0]
        extention = file_path.split("/")[3].split(".")[1]
        if(extention == "gpkg"):
            calculate_area_proportion(edges_path, file_path, data_name, edges_path, layer)



def bruit_pre(edges_buffer_path, bruit_path, edges_buffer_bruit_wavg_path, layer, name):
    """Calculer la valeur de DN pour chaque segment, en gardant la valeur max de DN par segment"""
    
    try:
        print("Chargement des fichiers...")
        # Charger les fichiers GeoPackage
        edges = gpd.read_file(edges_buffer_path)
        data = gpd.read_file(bruit_path)

        # Vérifier que les colonnes et les couches existent
        print(f"Colonnes de 'edges' : {edges.columns}")
        print(f"Colonnes de 'data' (bruit) : {data.columns}")

        # Nettoyer les géométries invalides dans les DataFrames
        print("Nettoyage des géométries invalides...")
        edges['geometry'] = edges['geometry'].apply(make_valid)
        data['geometry'] = data['geometry'].apply(make_valid)

        # Ajouter une colonne DN dans edges qui contiendra la valeur maximale de bruit pour chaque géométrie d'edges
        print("Calcul de la valeur maximale de DN pour chaque segment de rue...")
        
        def get_max_dn_for_edge(edge_geometry):
            # Trouver toutes les géométries de data qui intersectent la géométrie de edge
            intersecting_data = data[data.geometry.intersects(edge_geometry)]
            
            if not intersecting_data.empty:
                # Retourner la valeur maximale de DN parmi les géométries qui s'intersectent
                return intersecting_data[name].max()
            else:
                # Si aucune intersection, retourner NaN (ou une valeur par défaut comme 0 si vous préférez)
                return None
        
        # Appliquer cette fonction à chaque géométrie dans edges
        edges[name] = edges.geometry.apply(get_max_dn_for_edge)

        # Vérifier que la colonne 'DN' a été ajoutée correctement
        print(f"Exemples de lignes avec la nouvelle colonne '{name}' :\n{edges.head()}")

        # Supprimer les lignes où la valeur de 'DN' est NaN (si aucune intersection)
        print(f"Suppression des NaN dans la colonne '{name}'...")
        edges = edges.dropna(subset=[name])
        print(f"Nombre de lignes après suppression des NaN : {len(edges)}")

        # Normalisation des valeurs de bruit avec MinMaxScaler (si nécessaire)
        print("Mise à l'échelle des valeurs de DN avec MinMaxScaler...")
        scaler = MinMaxScaler(feature_range=(0, 1))
        edges["DN_scaled"] = scaler.fit_transform(edges[[name]])
        print("Mise à l'échelle terminée.")

        # Sauvegarder les résultats dans le fichier final
        print(f"Sauvegarde du fichier prétraité sous {edges_buffer_bruit_wavg_path}...")
        edges.to_file(edges_buffer_bruit_wavg_path, driver="GPKG", layer=layer)
        print(f"Fichier prétraité sauvegardé sous {edges_buffer_bruit_wavg_path}")

    except Exception as e:
        print(f"Erreur lors du traitement du bruit : {e}")




def calculate_presency(edges_path, data_path, output_path, layer, name, fn):
    """For each edges of network detect presency of one layer"""
    edges = gpd.read_file(edges_path, layer=layer)
    data = gpd.read_file(data_path)

    edges.geometry = [loads(dumps(geom, rounding_precision=3)) for geom in edges.geometry]
    data.geometry =  [loads(dumps(geom, rounding_precision=3)) for geom in data.geometry]

    overlay_edges = gpd.overlay(edges, data, how="identity", keep_geom_type=True)

    overlay_edges[["u", "v", "key"]] = overlay_edges[["u", "v", "key"]].astype(int)

    overlay_edges = overlay_edges.set_index(["u", "v", "key"])

    overlay_edges["class"] = overlay_edges["class"].fillna(1)

    grouped = overlay_edges.groupby(["u", "v", "key"], group_keys=True).apply(fn)

    edges = edges.set_index(["u", "v", "key"])

    edges[f"{name}"] = grouped[f"class"]

    edges.to_file(output_path, driver="GPKG", layer=layer)


def create_csv_dataset(edges_path, output_path, layer):
    edges = gpd.read_file(edges_path, layer=layer)
    edges = edges.drop(["geometry", "highway", "oneway", "reversed", "from", "to", "name", "maxspeed", "lanes", "width", "service", "bridge", "ref", "junction", "tunnel", "est_width", "access"], axis=1)

    edges.to_csv(output_path)



def cut_bruit(bruit_path, empreinte_path, sortie_path):
    """Découpe la couche 'bruit' avec le territoire de 'empreinte', utilise une couche intermédiaire, et renomme le fichier final"""
    try:
        # Charger les fichiers géospatiaux
        bruit = gpd.read_file(bruit_path)
        empreinte = gpd.read_file(empreinte_path)
    except Exception as e:
        print(f"Erreur lors du chargement des fichiers géospatiaux : {e}")
        return

    # Convertir les géométries de 'bruit' et 'empreinte' en Polygones ou MultiPolygones si nécessaire
    empreinte['geometry'] = empreinte['geometry'].apply(
        lambda x: x if isinstance(x, Polygon) else x.geoms[0] if isinstance(x, MultiPolygon) else None
    )
    
    # Vérifier que les deux couches ont le même CRS
    if bruit.crs != empreinte.crs:
        empreinte = empreinte.to_crs(bruit.crs)

    # Effectuer l'opération de découpe (intersection) entre 'bruit' et 'empreinte'
    try:
        decoupe = gpd.overlay(bruit, empreinte, how='intersection')
    except Exception as e:
        print(f"Erreur lors de l'opération de découpe : {e}")
        return

    # Sauvegarder le fichier découpé sous un nom intermédiaire
    temp_output_path = "temp_output_bruit.gpkg"
    try:
        decoupe.to_file(temp_output_path, driver="GPKG")
        print(f"Fichier découpé sauvegardé sous : {temp_output_path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du fichier découpé : {e}")
        return

    # Supprimer le fichier d'entrée original
    if os.path.exists(bruit_path):
        os.remove(bruit_path)
        print(f"Le fichier d'entrée {bruit_path} a été supprimé avec succès.")
    else:
        print(f"Le fichier {bruit_path} n'existe pas et n'a pas pu être supprimé.")

    # Renommer le fichier découpé pour qu'il prenne le même nom que le fichier d'entrée
    if os.path.exists(temp_output_path):
        os.rename(temp_output_path, bruit_path)
        print(f"Le fichier découpé a été renommé en {bruit_path}.")
    else:
        print(f"Le fichier {temp_output_path} n'existe pas et n'a pas pu être renommé.")





def check_data_integrity(edges_path, bruit_path):
    """Vérifie l'intégrité des données avant le traitement"""

    # Charger les fichiers
    edges = gpd.read_file(edges_path)
    bruit = gpd.read_file(bruit_path)

    #Supprimer les doublons dans la colonne 'geometry' en gardant la première occurrence
    edges = edges.drop_duplicates(subset='geometry')
    edges_duplicates_geometry = edges[edges.duplicated(subset='geometry', keep=False)]
    # Vérification des doublons dans les géométries
    print(f"Nombre de doublons dans 'edges' pour 'geometry' : {edges.duplicated(subset='geometry').sum()}")
    print(f"Nombre de doublons dans 'bruit' pour 'geometry' : {bruit.duplicated(subset='geometry').sum()}")

    # Vérification des NaN dans la colonne DN de 'bruit'
    print(f"Nombre de NaN dans 'DN' de 'bruit' : {bruit['DN'].isna().sum()}")

    # Vérification des doublons dans les indices ['u', 'v', 'key'] dans 'edges'
    print(f"Nombre de doublons dans 'edges' pour ['u', 'v', 'key'] : {edges.duplicated(subset=['u', 'v', 'key']).sum()}")

    # Vérification des doublons dans toutes les colonnes de 'edges' et 'bruit'
    print(f"Nombre de doublons dans 'edges' (toutes colonnes) : {edges.duplicated().sum()}")
    print(f"Nombre de doublons dans 'bruit' (toutes colonnes) : {bruit.duplicated().sum()}")


def cut_edges(edges_path, empreinte_path, sortie_path):
    """Découpe la couche 'edges' avec le territoire de 'empreinte', utilise une couche intermédiaire, et renomme le fichier final"""
    try:
        # Charger les fichiers géospatiaux
        edges = gpd.read_file(edges_path)
        empreinte = gpd.read_file(empreinte_path)
    except Exception as e:
        print(f"Erreur lors du chargement des fichiers géospatiaux : {e}")
        return

    # Convertir les géométries de 'edges' et 'empreinte' en Polygones ou MultiPolygones si nécessaire
    empreinte['geometry'] = empreinte['geometry'].apply(
        lambda x: x if isinstance(x, Polygon) else x.geoms[0] if isinstance(x, MultiPolygon) else None
    )
    
    # Vérifier que les deux couches ont le même CRS
    if edges.crs != empreinte.crs:
        empreinte = empreinte.to_crs(edges.crs)

    # Effectuer l'opération de découpe (intersection) entre 'edges' et 'empreinte'
    try:
        decoupe = gpd.overlay(edges, empreinte, how='intersection')
    except Exception as e:
        print(f"Erreur lors de l'opération de découpe : {e}")
        return

    # Sauvegarder le fichier découpé sous un nom intermédiaire
    temp_output_path = "temp_output.gpkg"
    try:
        decoupe.to_file(temp_output_path, driver="GPKG")
        print(f"Fichier découpé sauvegardé sous : {temp_output_path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du fichier découpé : {e}")
        return

    # Supprimer le fichier d'entrée original
    if os.path.exists(edges_path):
        os.remove(edges_path)
        print(f"Le fichier d'entrée {edges_path} a été supprimé avec succès.")
    else:
        print(f"Le fichier {edges_path} n'existe pas et n'a pas pu être supprimé.")

    # Renommer le fichier découpé pour qu'il prenne le même nom que le fichier d'entrée
    if os.path.exists(temp_output_path):
        os.rename(temp_output_path, edges_path)
        print(f"Le fichier découpé a été renommé en {edges_path}.")
    else:
        print(f"Le fichier {temp_output_path} n'existe pas et n'a pas pu être renommé.")
