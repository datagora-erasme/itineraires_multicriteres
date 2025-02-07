import sys
import os
sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../script_python")
os.environ['USE_PYGEOS'] = '0'
from backend.script_python.function_utils import bufferize_with_column, calculate_area_proportion, classification, clip_data, create_folder, dissolving
import geopandas as gpd
import pandas as pd
import os
from function_utils import *
from global_variable import *

###### CREATE WORKING DIRECTORY FOR VEGETATION #######
create_folder("./output_data/vegetation/")
create_folder("./output_data/vegetation/veget_strat/")
create_folder("./output_data/vegetation/arbres_align/")

###### VEGETATION STRATIFIEE PREPROCESSING ######

### FUNCTION ###
def veget_classification(row):
    """
    Classifies the type of vegetation based on the "vegetation_class" column.

    Parameters:
    row (pandas.Series): A row from a pandas DataFrame containing a "vegetation_class" column.

    Returns:
    str: The vegetation type as a string. Possible values are:
        - "prairie" for vegetation_class 1
        - "arbuste" for vegetation_class 2
        - "arbre" for vegetation_class 3
    """
    if(row["vegetation_class"] == 1):
        return "prairie"
    if(row["vegetation_class"] == 2):
        return "arbuste"
    if(row["vegetation_class"] == 3):
        return "arbre"
    
def arbres_align_classification(row):
    """
    Classifies the type of vegetation (tree or shrub) based on the height.

    Parameters:
    row (pandas.Series): A row from a pandas DataFrame containing the "hauteurtot" column (total height).

    Returns:
    str: The classification as a string:
        - "arbre" if the total height ("hauteurtot") is greater than 1.5 meters.
        - "arbuste" if the total height is less than or equal to 1.5 meters.
    """
    if(row["hauteurtot"] > 1.5):
        return "arbre"
    return "arbuste"
    

### SCRIPT ###

vegetation_choices = input("""Several calculations can be performed: \n
    - Clip the stratified vegetation data with the buffered pedestrian network of the metropolitan area (CLIP).\n
    WARNING: This calculation is resource-intensive with a standard configuration (~24h).
    The data for 03.07.23 is available at the location specified in the README.
    - Recalculate the proportions of vegetation on the pedestrian network segments, for example, if the alignment trees
    have been updated (PROP).\n
    WARNING, estimated computation time ~5h
""")

                           
if(vegetation_choices == "CLIP"):
    print("Dissolving network")
    dissolving(edges_buffer_path, edges_buffer_disolved_path, "edges")

    print("Clipping Végétation stratifée with dissolved network")
    clip_data(edges_buffer_disolved_path, raw_veget_strat_path, veget_strat_path, 4, "edges")

    print("Classification Vegetation stratifiee")
    classification(veget_strat_path, veget_strat_class_folder, veget_classification, "veget_strat")

###### ARBRES D'ALIGNEMENT PREPROCESSING ######
elif(vegetation_choices == "PROP"):

    print("###### ARBRES D'ALIGNEMENT ###### ")

    print("Classification arbres alignement")
    classification(arbres_align_gpkg_path, arbres_align_class_folder, arbres_align_classification, "arbres_align")

    print("Buffering arbres and arbustes align")
    bufferize_with_column(class_arbres_align_path, arbres_align_buffer_path, "arbres_align_arbre", "rayoncouro", 2.5, coeff_buffer=2)
    bufferize_with_column(class_arbustes_align_path, arbustes_align_buffer_path, "arbres_align_arbuste", "rayoncouro", 2.5, coeff_buffer=2)

    arbres_align_buffer = gpd.read_file(arbres_align_buffer_path)
    arbustes_align_buffer = gpd.read_file(arbustes_align_buffer_path)

    edges_buffer = gpd.read_file(edges_buffer_path)
    print("Clipping arbres and arbustes align")
    clip_data(edges_buffer_path, arbres_align_buffer_path, clipped_arbres_align_path, 5, "arbres_align")
    clip_data(edges_buffer_path, arbustes_align_buffer_path, clipped_arbustes_align_path, 5, "arbustes_align")

###### MERGE ARBRES ALIGNEMENT ET VEGETATION STRATIFIEE ###### 

### GLOBAL VARIABLE ###

    print("###### MERGE ARBRES ALIGNEMENT ET VEGETATION STRATIFIEE ###### ")

    print("Difference Arbres align Arbres veget")

    clipped_arbres_align = gpd.read_file(clipped_arbres_align_path)
    clipped_arbustes_align = gpd.read_file(clipped_arbustes_align_path)
    clipped_arbres_align = gpd.read_file(arbres_align_buffer_path)
    clipped_arbustes_align = gpd.read_file(arbustes_align_buffer_path)

    clipped_veget_arbres = gpd.read_file(clipped_arbres_veget_strat_path)
    clipped_veget_arbustes = gpd.read_file(clipped_arbustes_veget_strat_path)

    print("difference arbre align")
    arbres_align_diff = gpd.overlay(arbres_align_buffer, clipped_veget_arbres, how="difference", keep_geom_type=False)
    arbres_align_diff.to_file(arbres_align_veget_diff_path, driver="GPKG", layer="arbres_align")

    print("difference arbustes align")
    arbustes_align_diff = gpd.overlay(arbustes_align_buffer, clipped_veget_arbustes, how="difference", keep_geom_type=False)
    arbustes_align_diff.to_file(arbustes_align_veget_diff_path, driver="GPKG", layer="arbustes_align")

    print("merge layers")
    print("arbres")
    arbres_align_diff = gpd.read_file(arbres_align_veget_diff_path)
    veget_arbres = gpd.read_file(clipped_arbres_veget_strat_path)

    arbres_align_diff = arbres_align_diff[["geometry"]]
    arbres_align_diff["vegetation_class"] = 3
    arbres_align_diff["class"] = "arbre"

    veget_align_arbres = pd.concat([arbres_align_diff, veget_arbres])

    veget_align_arbres.to_file(merged_veget_align_arbres_path, driver="GPKG", layer="veget")

    print("arbustes")
    arbustes_align_diff = gpd.read_file(arbustes_align_veget_diff_path)
    veget_arbustes = gpd.read_file(clipped_arbustes_veget_strat_path)

    arbustes_align_diff = arbustes_align_diff[["geometry"]]
    arbustes_align_diff["vegetation_class"] = 3
    arbustes_align_diff["class"] = "arbuste"

    veget_align_arbustes = pd.concat([arbustes_align_diff, veget_arbustes])

    veget_align_arbustes.to_file(merged_veget_align_arbustes_path, driver="GPKG", layer="veget")

    ###### CALCULATE VEGETATION PROPORTION ON EDGES ######
    print("###### CALCULATE VEGETATION PROPORTION ON EDGES ######")

    print("Calculate arbres proportion")
    calculate_area_proportion(edges_buffer_path, merged_veget_align_arbres_path, "arbres", edges_buffer_arbres_prop_path, "edges")

    print("Calculate arbustes proportion")
    calculate_area_proportion(edges_buffer_path, merged_veget_align_arbustes_path, "arbustes", edges_buffer_arbustes_prop_path, "edges")
    print("Calculate prairie proportion")
    calculate_area_proportion(edges_buffer_path, clipped_prairie_veget_strat_path, "prairies", edges_buffer_prairies_prop_path, "edges")




