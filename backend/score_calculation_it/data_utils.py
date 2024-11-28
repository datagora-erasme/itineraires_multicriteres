import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
import multiprocessing as mp
import numpy as np
from shapely.wkt import loads, dumps
from shapely.geometry import Polygon, MultiPolygon
import os
import subprocess
from osgeo import ogr

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

def calculate_weighted_average(edges_path, data_path, output_path, layer, name, fn):
    """Calculate mean average of a variable for each edges"""
    
    print("Chargement des fichiers...")
    edges = gpd.read_file(edges_path, layer=layer)
    data = gpd.read_file(data_path)

    # Vérifier et convertir les géométries de `data` si elles ne sont pas des Polygones
    data['geometry'] = data['geometry'].apply(lambda x: x if isinstance(x, Polygon) else x.geoms[0] if isinstance(x, MultiPolygon) else None)

    # Vérifier les types de géométrie uniques dans edges et data après conversion
    print("Types de géométrie dans edges : ", edges.geometry.type.unique())
    print("Types de géométrie dans data après conversion : ", data.geometry.type.unique())


    # Nombre de lignes 
    print(f"Nombre de lignes dans edges : {len(edges)}")
    print(f"Nombre de lignes dans data : {len(data)}")

    # Voir les CRS
    print(edges.crs)
    print(data.crs)

    # Arrondissement des géométries
    print("Arrondissement des géométries...")
    edges.geometry = [loads(dumps(geom, rounding_precision=3)) for geom in edges.geometry]
    data.geometry = [loads(dumps(geom, rounding_precision=3)) for geom in data.geometry]
    print("Géométries arrondies.")

    # Calcul de l'overlay entre edges et data
    print("Calcul de l'overlay...")
    overlay_edges = gpd.overlay(edges, data, how="identity", keep_geom_type=True)
    print(f"Overlay terminé. Nombre de lignes après overlay : {len(overlay_edges)}")

    # Calcul de l'aire de chaque géométrie
    print("Calcul de l'aire des géométries dans overlay...")
    overlay_serie = gpd.GeoSeries(overlay_edges["geometry"])
    overlay_edges["area"] = overlay_serie.area
    print("Aire calculée pour chaque géométrie.")

    # Conversion des colonnes 'u', 'v', 'key' en entiers
    print("Conversion des colonnes 'u', 'v', 'key' en entier...")
    overlay_edges[["u", "v", "key"]] = overlay_edges[["u", "v", "key"]].astype(int)
    print("Conversion terminée.")

    # Réindexation de l'overlay
    print("Réindexation de overlay_edges...")
    overlay_edges = overlay_edges.set_index(["u", "v", "key"])

    # Application de la fonction fn
    print("Application de la fonction de regroupement fn...")
    grouped = overlay_edges.groupby(["u", "v", "key"], group_keys=True).apply(fn)
    print("Fonction de regroupement fn appliquée.")

    # Réindexation de edges
    print("Réindexation de edges...")
    edges = edges.set_index(["u", "v", "key"])

    # Ajout de la moyenne pondérée à edges
    print(f"Ajout de la colonne '{name}_wavg' dans edges...")
    edges[f"{name}_wavg"] = grouped[f"{name}_wavg"]
    print(f"Colonne '{name}_wavg' ajoutée.")

    # Enregistrement du fichier de sortie
    print(f"Enregistrement du fichier de sortie à {output_path}...")
    edges.to_file(output_path, driver="GPKG", layer=layer)
    print("Fichier sauvegardé avec succès.")





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
    # Charger les fichiers géospatiaux
    try:
        bruit = gpd.read_file(bruit_path)
        empreinte = gpd.read_file(empreinte_path)
    except Exception as e:
        print(f"Erreur lors du chargement des fichiers géospatiaux : {e}")
        return

    # Convertir les géométries en Polygones ou MultiPolygones si nécessaire
    bruit['geometry'] = bruit['geometry'].apply(
        lambda x: x if isinstance(x, Polygon) else x.geoms[0] if isinstance(x, MultiPolygon) else None
    )

    empreinte['geometry'] = empreinte['geometry'].apply(
        lambda x: x if isinstance(x, Polygon) else x.geoms[0] if isinstance(x, MultiPolygon) else None
    )

    # Vérifier que les deux couches ont le même CRS
    if bruit.crs != empreinte.crs:
        empreinte = empreinte.to_crs(bruit.crs)

    # Effectuer l'opération de découpe (intersection)
    decoupe = gpd.overlay(bruit, empreinte, how='intersection')

    # Sauvegarder le fichier découpé
    try:
        decoupe.to_file(sortie_path, driver="GPKG")
        print(f"Fichier découpé sauvegardé sous : {sortie_path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du fichier découpé : {e}")
        return

    # Supprimer le fichier d'origine
    if os.path.exists(bruit_path):
        os.remove(bruit_path)
        print(f"Le fichier d'origine {bruit_path} a été supprimé avec succès.")
    else:
        print(f"Le fichier {bruit_path} n'existe pas et n'a pas pu être supprimé.")

    # Renommer le fichier découpé
    if os.path.exists(sortie_path):
        os.rename(sortie_path, bruit_path)
        print(f"Le fichier a été renommé en {bruit_path}.")
    else:
        print(f"Le fichier {sortie_path} n'existe pas et n'a pas pu être renommé.")
