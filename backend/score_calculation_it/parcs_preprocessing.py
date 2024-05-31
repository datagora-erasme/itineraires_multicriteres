import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
from shapely.wkt import dumps, loads

# Fonction pour créer des dossiers
def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Créer le dossier de sortie
create_folder("./output_data/parcs/")

# Chemin des données de parcs
parcs_classes_path = "./output_data/parcs/parcs_classes.gpkg"

# Demander à l'utilisateur s'il souhaite mettre à jour le réseau
choice = input("""
    Souhaitez-vous mettre à jour le réseau pondéré par les parcs ? OUI ou NON
""")
if choice.upper() == "OUI":
    print("Create parcs classes")

    parcs = gpd.read_file(data_params["parcs"]["gpkg_path"])

    parcs.to_file(parcs_classes_path, driver="GPKG", layer="parcs")

    def calculate_parc_proportion(edges_path, parcs_path, output_path, layer="edges"):
        edges = gpd.read_file(edges_path, layer=layer)
        parcs = gpd.read_file(parcs_path)

        print("Edges columns:", edges.columns)
        print("Parcs columns:", parcs.columns)

        edges.geometry = [loads(dumps(geom, rounding_precision=3)) for geom in edges.geometry]
        parcs.geometry = [loads(dumps(geom, rounding_precision=3)) for geom in parcs.geometry]

        overlay_edges = gpd.overlay(edges, parcs, how="identity", keep_geom_type=True)
        
        print("Overlay edges:", overlay_edges)

        overlay_serie = gpd.GeoSeries(overlay_edges["geometry"])
        overlay_edges["area"] = overlay_serie.area
        
        overlay_edges[["u", "v", "key"]] = overlay_edges[["u", "v", "key"]].astype(int)
        overlay_edges = overlay_edges.set_index(["u", "v", "key"])

        print("Calculating prop area")
        grouped = overlay_edges.groupby(["u", "v", "key"]).apply(
            lambda x: pd.Series({
                "prop": round(x["area"].sum() / edges.loc[(x.name[0], x.name[1], x.name[2]), "geometry"].area, 2),
            }) if (x.name[0], x.name[1], x.name[2]) in edges.index else pd.Series({"prop": 0})
        )

        edges = edges.set_index(["u", "v", "key"])
        edges["parcs_prop"] = grouped["prop"]

        print("Proportion of area calculated, sample:\n", edges["parcs_prop"].head())

        print("Writing to file")
        edges.to_file(output_path, driver="GPKG", layer=layer)

    calculate_parc_proportion(edges_buffer_path, parcs_classes_path, edges_buffer_parcs_pollen_prop_path)

    network_parcs = gpd.read_file(edges_buffer_parcs_pollen_prop_path)
    print("network_parcs.columns: ", network_parcs.columns)

    network_parcs = network_parcs.set_index(["u", "v", "key"])

    #check the distribution of 'parcs_prop'
    print("Distribution of 'parcs_prop':\n", network_parcs["parcs_prop"].describe())

    network_parcs["parcs_class"] = network_parcs.apply(lambda x: "high" if x["parcs_prop"] > 0.5 else "low", axis=1)

    #check the first few rows after classification
    print("First few rows after classification:\n", network_parcs[["parcs_prop", "parcs_class"]].head())

    network_parcs.to_file(edges_buffer_parcs_pollen_prop_path, driver="GPKG", layer="edges")
