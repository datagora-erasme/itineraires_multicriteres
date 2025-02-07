import os
### GLOBAL VARIABLES OF THE PROJECT ###

base_path = os.path.dirname(os.path.abspath(__file__))

def globpath(path):
    """
    Join the given relative path with the base directory path of the script.
    
    Parameters:
    path (str): The relative path to be joined.
    
    Returns:
    str: The absolute path formed by joining the base path and the given path.
    """
    return os.path.join(base_path, path)

### BOUDING LYON METROPOLE PATH ###
bounding_metrop_path = globpath("./score_calculation_it/input_data/bounding_metrop.gpkg")

### NETWORK PATH ###
metrop_network_bouding_path = globpath("./score_calculation_it/input_data/network/metrop_network_bounding.gpkg")

### GRAPH PATH ###
final_network_path = globpath("./score_calculation_it/output_data/network/graph/final_network_P0_01O5At0_01Ar10C0_01E5Ca.gpkg")
final_network_pickle_path = globpath("./score_calculation_it/output_data/network/graph/final_network_P0_01O5At0_01Ar10C0_01E5Ca.pickle")
final_network_multidigraph_pickle_path = globpath("./score_calculation_it/output_data/network/graph/final_network_P0_01O5At0_01Ar10C0_01E5Ca_multidigraph.pickle")

final_network_pollen_path = globpath("./score_calculation_it/output_data/network/graph/final_network_pollen.gpkg")
final_network_pickle_pollen_path = globpath("./score_calculation_it/output_data/network/graph/final_network_pollen.pickle")
final_network_multidigraph_pickle_pollen_path = globpath("./score_calculation_it/output_data/network/graph/final_network_pollen_multidigraph.pickle")

final_network_pollen_fevmai_path = globpath("./score_calculation_it/output_data/network/graph/final_network_pollen_fevmai.gpkg")
final_network_pickle_pollen_fevmai_path = globpath("./score_calculation_it/output_data/network/graph/final_network_pollen_fevmai.pickle")
final_network_multidigraph_pickle_pollen_fevmai_path = globpath("./score_calculation_it/output_data/network/graph/final_network_pollen_fevmai_multidigraph.pickle")

final_network_bruit_path = globpath("./score_calculation_it/output_data/network/graph/final_network_bruit.gpkg")
final_network_pickle_bruit_path = globpath("./score_calculation_it/output_data/network/graph/final_network_bruit.pickle")
final_network_multidigraph_pickle_bruit_path = globpath("./score_calculation_it/output_data/network/graph/final_network_bruit_multidigraph.pickle")

final_network_tourisme_path = globpath("./score_calculation_it/output_data/network/graph/final_network_tourisme.gpkg")
final_network_pickle_tourisme_path = globpath("./score_calculation_it/output_data/network/graph/final_network_tourisme.pickle")
final_network_multidigraph_pickle_tourisme_path = globpath("./score_calculation_it/output_data/network/graph/final_network_tourisme_multidigraph.pickle")

### EDGES PATH ###
edges_buffer_path = globpath("./score_calculation_it/input_data/network/edges_buffered_12_bounding.gpkg")
edges_buffer_disolved_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_dissolved_path.gpkg")

edges_buffer_arbres_prop_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_arbres_prop_bounding.gpkg")
edges_buffer_arbustes_prop_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_arbustes_prop_bounding.gpkg")
edges_buffer_prairies_prop_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_prairies_prop_bounding.gpkg")

edges_buffer_temp_wavg_path =globpath("./score_calculation_it/output_data/network/edges/edges_buffered_temp_wavg_bounding.gpkg")
edges_buffer_temp_wavg_path_no_na = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_temp_wavg_bounding_no_na.gpkg")

edges_buffer_ombres_08_prop_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_ombres_08_prop_bounding.gpkg")
edges_buffer_ombres_13_prop_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_ombres_13_prop_bounding.gpkg")
edges_buffer_ombres_18_prop_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_ombres_18_prop_bounding.gpkg")

edges_buffer_parcs_prop_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_parcs_prop_canop_bounding.gpkg")

edges_buffer_eaux_prop_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_eaux_prop_bounding.gpkg")

edges_buffer_arbres_pollen_prop_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffer_arbres_pollen_prop_path.gpkg")
edges_buffer_arbres_pollen_prop_path_fevmai = globpath("./score_calculation_it/output_data/network/edges/edges_buffer_arbres_pollen_prop_path_fevmai.gpkg")

edges_buffer_parcs_pollen_prop_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffer_parcs_pollen_prop_path.gpkg")

edges_buffer_scored_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_scored_bounding.gpkg")

edges_buffer_total_score_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_total_score_bounding.gpkg")
edges_buffer_total_score_distance_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_total_score_distance_bounding.gpkg")
edges_buffer_total_score_distance_freshness_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_total_score_distance_freshness_bounding.gpkg")
edges_buffer_total_score_distance_pollen_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_total_score_distance_pollen_bounding.gpkg")
edges_buffer_total_score_distance_bruit_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_total_score_distance_bruit_bounding.gpkg")
edges_buffer_total_score_distance_tourisme_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_total_score_distance_tourisme_bounding.gpkg")

edges_buffer_bruit_wavg_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_bruit_wavg_bounding.gpkg")
edges_buffer_bruit_wavg_path_no_na = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_bruit_wavg_bounding_no_na.gpkg")

edges_buffer_tourisme_prop_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_tourisme_prop_bounding.gpkg")

### DATA PATH ###
#### VEGETATION ####
raw_veget_strat_path = globpath("./score_calculation_it/input_data/vegetation/raw_veget_strat.gpkg")
veget_strat_path = globpath("./score_calculation_it/input_data/vegetation/clipped_veget_12.gpkg")
veget_strat_class_folder = globpath("./score_calculation_it/output_data/vegetation/veget_strat/")
clipped_arbres_veget_strat_path = globpath("./score_calculation_it/output_data/vegetation/veget_strat/veget_strat_arbre.gpkg")
clipped_arbustes_veget_strat_path = globpath("./score_calculation_it/output_data/vegetation/veget_strat/veget_strat_arbuste.gpkg")
clipped_prairie_veget_strat_path = globpath("./score_calculation_it/output_data/vegetation/veget_strat/veget_strat_prairie.gpkg")

arbres_align_gpkg_path = globpath("./score_calculation_it/input_data/arbres/arbres.gpkg")
arbres_align_class_folder = globpath("./score_calculation_it/output_data/vegetation/arbres_align/")
class_arbres_align_path = globpath("./score_calculation_it/output_data/vegetation/arbres_align/arbres_align_arbre.gpkg")
class_arbustes_align_path = globpath("./score_calculation_it/output_data/vegetation/arbres_align/arbres_align_arbuste.gpkg")

arbres_align_buffer_path = globpath("./score_calculation_it/output_data/vegetation/arbres_align/class_arbres_align_buffer_2.gpkg")
arbustes_align_buffer_path = globpath("./score_calculation_it/output_data/vegetation/arbres_align/class_arbustes_align_buffer_2.gpkg")

clipped_arbres_align_path = globpath("./score_calculation_it/output_data/vegetation/arbres_align/clipped_arbres_align.gpkg")
clipped_arbustes_align_path = globpath("./score_calculation_it/output_data/vegetation/arbres_align/clipped_arbustes_align.gpkg")

arbres_align_veget_diff_path = globpath("./score_calculation_it/output_data/vegetation/arbres_align/diff_arbres_align_veget_2.gpkg")
arbustes_align_veget_diff_path = globpath("./score_calculation_it/output_data/vegetation/arbres_align/diff_arbustes_align_veget_2.gpkg")

merged_veget_align_arbres_path = globpath("./score_calculation_it/output_data/vegetation/merged_veget_align_arbres_2.gpkg")
merged_veget_align_arbustes_path = globpath("./score_calculation_it/output_data/vegetation/merged_veget_align_arbustes_2.gpkg")

#### TEMPERATURE ####
temperature_path = globpath("./score_calculation_it/input_data/temperature/temperature_surface.gpkg")

#### SHADOWS ####
shadows_08_clipped_path = globpath("./score_calculation_it/output_data/ombres/ombres_08_metrop_clipped.gpkg")
shadows_13_clipped_path = globpath("./score_calculation_it/output_data/ombres/ombres_13_metrop_clipped.gpkg")
shadows_18_clipped_path = globpath("./score_calculation_it/output_data/ombres/ombres_18_metrop_clipped.gpkg")

shadows_08_explode_path = globpath("./score_calculation_it/output_data/ombres/ombres_08_metrop_explode.gpkg")
shadows_13_explode_path = globpath("./score_calculation_it/output_data/ombres/ombres_13_metrop_explode.gpkg")
shadows_18_explode_path = globpath("./score_calculation_it/output_data/ombres/ombres_18_metrop_explode.gpkg")

shadows_08_intersect_path = globpath("./score_calculation_it/output_data/ombres/intersect_ombres_edges_08.gpkg")
shadows_13_intersect_path = globpath("./score_calculation_it/output_data/ombres/intersect_ombres_edges_13.gpkg")
shadows_18_intersect_path = globpath("./score_calculation_it/output_data/ombres/intersect_ombres_edges_18.gpkg")

shadows_path = globpath("./score_calculation_it/output_data/ombres/ombres_metrop.gpkg")
shadows_08_path = globpath("./score_calculation_it/output_data/ombres/ombres_08_metrop.gpkg")
shadows_13_path = globpath("./score_calculation_it/output_data/ombres/ombres_13_metrop.gpkg")
shadows_18_path = globpath("./score_calculation_it/output_data/ombres/ombres_18_metrop.gpkg")

#### EAUX ####
eaux_path = globpath("./score_calculation_it/output_data/eaux/eaux.gpkg")
eaux_buffer_path = globpath("./score_calculation_it/output_data/eaux/eaux_buffered.gpkg")

#### POLLEN ####
arbres_classes_pollen_path = globpath("./score_calculation_it/output_data/arbres/arbres.gpkg")

#### BRUIT ####
bruit_path = globpath("./score_calculation_it/input_data/bruit/bruit.gpkg")
sortie_path = globpath("./score_calculation_it/input_data/bruit/ouche_decoupee.gpkg")

#### EMPREINTE ####
empreinte_path = globpath("./score_calculation_it/input_data/empreinte/empreinte.gpkg")

### DATA PARAMS ###
data_params = {
    "batiments" : {
        "wfs_key": "metropole-de-lyon:fpc_fond_plan_communaut.fpctoit_2018",
        "gpkg_path": globpath("./score_calculation_it/input_data/batiments/batiments.gpkg"),
        "geojson_path": globpath("./score_calculation_it/input_data/batiments/batiments.json"),
        "onMap": False #should not be displayed on map
    },
    "parcs": {
        "name": "Parcs et jardins",
        "wfs_key": "metropole-de-lyon:com_donnees_communales.comparcjardin_1_0_0",
        "gpkg_path": globpath("./score_calculation_it/input_data/parcs/parcs.gpkg"),
        "geojson_path": globpath("./score_calculation_it/input_data/parcs/parcs.json"),
        "onMap": True,
        "marker_option": {
            "iconUrl": "arbre.svg"
        },
    },
    "parcs_canop": {
        "wfs_key": "metropole-de-lyon:evg_esp_veg.evgparcindiccanope_latest",
        "gpkg_path": globpath("./score_calculation_it/input_data/parcs/parcs_canop.gpkg"),
        "geojson_path": globpath("./score_calculation_it/input_data/parcs/parcs_canop.json"),
        "onMap": False
    },
    "fontaines_potables": {
        "name": "Fontaines potables",
        "wfs_key": "metropole-de-lyon:adr_voie_lieu.adrbornefontaine_latest",
        "gpkg_path": globpath("./score_calculation_it/input_data/fontaines_potables/fontaines_potables.gpkg"),
        "geojson_path": globpath("./score_calculation_it/input_data/fontaines_potables/fontaines_potables.json"),
        "edges_path": globpath("./score_calculation_it/output_data/network/edges/edges_buffered_fontaines_potables.gpkg"),
        "buffer_path": globpath("./score_calculation_it/output_data/fontaines/fontaines_potables_buffered.gpkg"),
        "buffer_size": 30,
        "onMap": True,
        "marker_option": {
            "iconUrl": "droplet.svg",
            "iconRetinaUrl": "droplet.svg",
            "popupAnchor": [
                0,
                0
            ],
            "iconSize": [
                40,
                40
            ],
            "clusterCountStyle": "position:absolute;top:20px;left:-9px;color:white;font-weight:bold;"
        },
    },
    "fontaines_ornementales": {
        "name": "Fontaines ornementales",
        "wfs_key": "metropole-de-lyon:adr_voie_lieu.adrfontaineornem_latest",
        "gpkg_path": globpath("./score_calculation_it/input_data/fontaines_ornementales/fontaines_ornementales.gpkg"),
        "geojson_path": globpath("./score_calculation_it/input_data/fontaines_ornementales/fontaines_ornementales.json"),
        "edges_path": globpath("./score_calculation_it/output_data/network/edges/edges_buffered_fontaines_ornementales.gpkg"),
        "buffer_path": globpath("./score_calculation_it/output_data/fontaines/fontaines_ornementales_buffered.gpkg"),
        "buffer_size": 25,
        "onMap": True,
        "marker_option": {
            "iconUrl": "fountain.svg",
            "iconRetinaUrl": "fountain.svg",
            "popupAnchor": [
                0,
                0
            ],
            "iconSize": [
                40,
                40
            ],
            "clusterCountStyle": "position:absolute;top:48px;left:0px;color:black;font-weight:bold;"
        },
    },
    "toilettes": {
        "name": "Toilettes publiques",
        "wfs_key": "metropole-de-lyon:adr_voie_lieu.adrtoilettepublique_latest",
        "gpkg_path": globpath("./score_calculation_it/input_data/toilettes/toilettes.gpkg"),
        "geojson_path": globpath("./score_calculation_it/input_data/toilettes/toilettes.json"),
        "edges_path": globpath("./score_calculation_it/output_data/network/edges/edges_buffered_toilette.gpkg"),
        "buffer_path": globpath("./score_calculation_it/output_data/toilettes/toilettes_buffered.gpkg"),
        "buffer_size": 20,
        "onMap": True,
        "marker_option": {
            "iconUrl": "toilet.svg",
            "iconRetinaUrl": "toilet.svg",
            "popupAnchor": [
                0,
                0
            ],
            "iconSize": [
                40,
                40
            ],
            "clusterCountStyle": "position:absolute;top:48px;left:-6px;color:black;font-weight:bold;"
        },
    },
    # "tourisme": {
    #     "name": "Tourisme",
    #     "wfs_key": "metropole-de-lyon:apd_apidae.apdlieutourisme_latest",
    #     "gpkg_path": globpath("./score_calculation_it/input_data/tourisme/corrige_tourisme_3946.gpkg"),
    #     "geojson_path": globpath("./score_calculation_it/input_data/tourisme/patrimoine_tourisme_3946.json"),
    #     "edges_path": globpath("./score_calculation_it/output_data/network/edges/edges_buffered_tourisme.gpkg"),
    #     "buffer_path": globpath("./score_calculation_it/output_data/tourisme/tourisme_buffered.gpkg"),
    #     "buffer_size": 20,
    #     "onMap": True,
    #     "marker_option": {
    #         "iconUrl": "building.svg",
    #         "iconRetinaUrl": "building.svg",
    #         "popupAnchor": [
    #             0,
    #             0
    #         ],
    #         "iconSize": [
    #             40,
    #             40
    #         ],
    #         "clusterCountStyle": "position:absolute;top:48px;left:-6px;color:black;font-weight:bold;"
    #     },
    #},
    "eaux_details": {
        "wfs_key" : "metropole-de-lyon:fpc_fond_plan_communaut.fpcplandeaudetail",
        "gpkg_path": globpath("./score_calculation_it/input_data/eaux_details/eaux_details.gpkg"),
        "geojson_path": globpath("./score_calculation_it/input_data/eaux_details/eaux_details.json"),
        "onMap": False
    },
    "eaux_importants": {
        "wfs_key": "metropole-de-lyon:fpc_fond_plan_communaut.fpcplandeau",
        "gpkg_path": globpath("./score_calculation_it/input_data/eaux_importants/eaux_importants.gpkg"),
        "geojson_path": globpath("./score_calculation_it/input_data/eaux_importants/eaux_importants.json"),
        "onMap": False
    },
    "bancs": {
        "name": "Bancs",
        "wfs_key": "metropole-de-lyon:adr_voie_lieu.adrbanc_latest",
        "gpkg_path": globpath("./score_calculation_it/input_data/bancs/bancs.gpkg"),
        "geojson_path": globpath("./score_calculation_it/input_data/bancs/bancs.json"),
        "edges_path": globpath("./score_calculation_it/output_data/network/edges/edges_buffered_bancs.gpkg"),
        "buffer_path": globpath("./score_calculation_it/output_data/bancs/bancs_buffered.gpkg"),
        "buffer_size": 10,
        "onMap": True,
        "marker_option": {
            "iconUrl": "bench.svg",
            "iconRetinaUrl": "bench.svg",
            "popupAnchor": [
                0,
                0
            ],
            "iconSize": [
                25,
                25
            ],
            "clusterCountStyle": "position:absolute;top:40px;left:0px;color:white;background-color:#d6eff8;font-weight:bold;"
        },
    },
    "arbres" : {
        "name": "Arbres d'alignement",
        "wfs_key": "metropole-de-lyon:abr_arbres_alignement.abrarbre",
        "gpkg_path": globpath("./score_calculation_it/input_data/arbres/arbres.gpkg"),
        "geojson_path": globpath("./score_calculation_it/input_data/arbres/arbres.json"),
        "onMap": False
    },
        "ambroisie": {
        "wfs_key": "metropole-de-lyon:toodego.signalement",
        "gpkg_path": globpath("./score_calculation_it/input_data/ambroisie/ambroisie.gpkg"),
        "geojson_path": globpath("./score_calculation_it/input_data/ambroisie/ambroisie.json"),
        "onMap": False
    },
    "empreinte" : {
        "wfs_key": "metropole-de-lyon:adr_voie_lieu.adrmetropole",
        "gpkg_path": globpath("./score_calculation_it/input_data/empreinte/empreinte.gpkg"),
        "geojson_path": globpath("./score_calculation_it/input_data/empreinte/empreinte.json"),
        "onMap": False
    },
    

}