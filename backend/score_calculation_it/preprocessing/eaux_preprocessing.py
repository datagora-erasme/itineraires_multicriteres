import sys
import os
sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../script_python")
os.environ['USE_PYGEOS'] = '0'
from backend.script_python.function_utils import bufferize_with_column, calculate_area_proportion, create_folder
import geopandas as gpd
import pandas as pd
from function_utils import *
from global_variable import *

###### EAUX PREPROCESSING ######
"""Les données proviennent de deux sources : plan d'eau importants et plan d'eaux détails de datagranlyon"""

### CREATE WORKING DIRECTORY ###
create_folder("./output_data/eaux/")

### SCRIPT ###

choice = input("""
    Would you like to update the weighted network by water? YES or NO
""")

if choice == "YES":

    eaux_details = gpd.read_file(data_params["eaux_details"]["gpkg_path"])
    eaux_importants = gpd.read_file(data_params["eaux_importants"]["gpkg_path"])

    eaux_details = eaux_details.to_crs(3946)
    eaux_importants = eaux_importants.to_crs(3946)

    eaux_details["class"] = "detail"
    eaux_importants["class"] = "important"

    # TODO: This needs to be refined for a non-arbitrary choice
    eaux_details["buffer_size"] = 10
    eaux_importants["buffer_size"] = 50

    eaux = pd.concat([eaux_details, eaux_importants])

    eaux.to_file(eaux_path, driver="GPKG", layer="eaux")

    bufferize_with_column(eaux_path, eaux_buffer_path, "eaux", "buffer_size", 5)

    calculate_area_proportion(edges_buffer_path, eaux_buffer_path, "eaux", edges_buffer_eaux_prop_path, "edges")