import os
from data_utils import *
from data_calculation import *
#from data_informations import services, data_wfs
from calculate_itinerary_utils import *
import geopandas as gpd
import time
from datetime import datetime

start_time = time.time()
now = datetime.now()
now = now.strftime("%d%m%Y%H%M")

data_folder_path = "./data/"
data_informations_path = "./data/data_informations.json"

create_folder("./data")
create_folder("./data/backup")
if os.path.isfile(data_informations_path):
    backup_path = f"./data/backup/data_informations_{now}.json"
    with open(data_informations_path, "r") as f:
        data_informations = json.load(f)
    with open(backup_path, "w") as f:
        json.dump(data_informations, f, indent=4)
    print("### BACKUP of data_informations.json file ###")

else:
    print("### CREATE data_informations.json file ###")
    create_data_informations_file()

# print("#### LOADING ALL DATA #### \n \n")
# create_folder(data_folder_path + "gml")
# download_data_wfs("data.grandlyon_wfs", "2.0.0", data_folder_path + "gml")

# create_folder(data_folder_path + "raster")
# # download_data_wms("data.grandlyon_wms", "1.1.1", data_folder_path + "raster")

# print("#### Converting Files #### \n \n")

# create_folder(data_folder_path + "gpkg")
# print("From gml to gpkg \n")
# convert_all(data_folder_path + "gpkg/", input_extension="gml", output_extension="gpkg", driver="GPKG")

# print("From gpkg to geojson \n")
# create_folder(data_folder_path + "geojson")
# convert_all(data_folder_path + "geojson/", input_extension="gpkg", output_extension="json", driver="GeoJSON")
# convert_all(data_folder_path + "geojson/", input_extension="gpkg", output_extension="json", driver="GeoJSON", connection_type="raw")


# write_all_atributes()

# ### Attributes to remove or to add

# ## Remove
# fontaines_potables_rm = ['nom', 'gestionnaire', 'anneepose']
# # toilettes_publiques_rm = ['commune', 'voie', 'numerodansvoie', 'gestionnaire', 'observation', 'identifiant']
# toilettes_publiques_rm = []
# fontaines_ornementales_rm = ['nom', 'address', 'commune', 'insee', 'source']
# parcs_jardins_metropole_rm = ['nom', 'num', 'voie', 'codepost', 'commune', 'code_insee', 'surf_tot_m2', 'gestion', 'clos', 'acces', 'label', 'type_equip', 'eau', 'toilettes', 'chien', 'esp_can', 'openinghours', 'timePosition', 'numvoie', 'precision_horaires', 'reglement', 'ann_ouvert', 'circulation', 'photo', 'id_ariane', 'horaires', 'openinghoursspecification']
# bancs_rm = ['dossier', 'insee', 'source']
# #arbres_alignement_rm = ['timePosition','architecture', 'naturerevetement', 'mobilierurbain', 'commune', 'codeinsee', 'nomvoie', 'codefuv', 'identifiant', 'numero']
# ## Add 
# #IF = Indicateur Fraicheur
# fontaines_potables_add = {
#     "data_type": "fontaines_potables",
#     "IF_fontaines_potables" : 0.01,
#     "buffer_size" : 10
# }
# toilettes_publiques_add = {
#     "data_type": "toilettes_publiques",
#     "IF_toilettes_publiques" : 0.01,
#     "buffer_size" : 10
# }
# fontaines_ornementales_add = {
#     "data_type": "fontaines_ornementales",
#     "IF_fontaines_ornementales" : 0.01,
#     "buffer_size" : 10
# }
# parcs_jardins_metropole_add = {
#     "data_type": "parcs_jardins_metropole",
#     "IF_parcs_jardins_metropole" : 0.01,
#     "buffer_size" : 10
# }
# bancs_add = {
#     "data_type": "bancs",
#     "IF_bancs" : 0.01,
#     "buffer_size" : 10
# }
# # arbres_alignement_add = {
# #     "data_type": "arbres_alignement",
# #     "IF_arbres_alignement" : 130,
# #     "buffer_size" : 10
# # }

# write_attributes_to_add_and_remove("fontaines_potables", fontaines_potables_add, fontaines_potables_rm)
# write_attributes_to_add_and_remove("toilettes_publiques", toilettes_publiques_add, toilettes_publiques_rm)
# write_attributes_to_add_and_remove("fontaines_ornementales", fontaines_ornementales_add, fontaines_ornementales_rm)
# write_attributes_to_add_and_remove("parcs_jardins_metropole", parcs_jardins_metropole_add, parcs_jardins_metropole_rm)
# write_attributes_to_add_and_remove("bancs", bancs_add, bancs_rm)
# #write_attributes_to_add_and_remove("arbres_alignement", arbres_alignement_add, arbres_alignement_rm)

# create_folder(data_folder_path + "cleaned_data")
# remove_and_add_attributes(data_folder_path + "cleaned_data/")


# print("#### Calculating areas of influence (buffer_size) ####")

# print("#### Converting Points Shapefile into Polygons #### \n \n")
# create_folder(data_folder_path + "gpkg_buffered")
# convert_all_points_into_polygons(data_folder_path + "gpkg_buffered/")

# print("#### Calculating freshness indicators (IF) #### ")

# with open(data_informations_path, "r") as f:
#     data_informations = json.load(f)

# print("Calculating IF Temperature...")

# temp_path = data_informations["data_raw"]["temp_surface_road_raw"]["gpkg_path"]
# temp_IF_path = "./raw_data/temp_IF.gpkg"

# calculate_IF(temp_path, temp_IF_path, temp_IF, "temp_surface_road_raw")

# data_informations["data_raw"]["temp_surface_road_raw"]["recalculated_if_path"] = temp_IF_path

# print("Calculating IF vegetation")

# print(data_informations["data_raw"])
# veget_path = data_informations["data_raw"]["vegetation_raw"]["gpkg_path"]
# veget_IF_path = "./raw_data/veget_IF.gpkg"

# calculate_IF(veget_path, veget_IF_path, veget_IF, "veget_raw")

# data_informations["data_raw"]["vegetation_raw"]["recalculated_if_path"] = veget_IF_path

# print("#### Network OSM extraction ####")
# create_folder(data_folder_path +"osm")

# lyon_network_parameters = {
#     "place_name" : "Lyon, France",
#     "network_type" : "walk",
#     "bbox": None,
#     "output_file": data_folder_path+ "osm/lyon_walk_simplified.gpkg"
# }


# metrop_network_parameters = {
#     "place_name": "Lyon, France",
#     "network_type": "walk",
#     "bbox": (45.9472,45.5497, 5.0803,4.6717),
#     "output_file" : data_folder_path+ "osm/metrop_walk_simplified.gpkg"
# }

filters = (
        f'["highway"]["area"!~"yes"]'
        f'["highway"!~"abandoned|bus_guideway|construction|cycleway|motorway|trunk|planned|platform|'
        f'proposed|raceway|motorway_link|trunk_link|escape|busway"]'
        f'["foot"!~"no"]["service"!~"private"]["sidewalk"!~"no"]'
    )

metrop_network_parameters = {
    "place_name": "Lyon, France",
    "network_filters": filters,
    "bbox": (45.9472,45.5497, 5.0803,4.6717),
    "output_file" : data_folder_path+ "osm/metrop_walk_2605_2.gpkg"
}

data_informations["osm"]["network_parameters"] = metrop_network_parameters

#load_osm_network(metrop_network_parameters)

with open(data_informations_path, "w") as f:
    json.dump(data_informations, f, indent=4)

print("#### Create all weighted networks ####")

# create_all_weighted_network(metrop_network_parameters["output_file"])

print("#### Create final weigthed network #### ")

with open(data_informations_path, "r") as f:
    data_informations = json.load(f)

final_network_path = data_folder_path + "osm/final_network_0206.gpkg"

merge_networks(metrop_network_parameters["output_file"], final_network_path)

data_informations["osm"]["final_network_path"] = final_network_path

with open(data_informations_path, "w") as f:
    json.dump(data_informations, f, indent=4)

print("ALL DONE")

end_time = time.time()

execution_time = (end_time - start_time)/60
print(f"Temps d'exécution : {execution_time}")