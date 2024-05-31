import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
from data_utils import *
import sys
sys.path.append("../")
from global_variable import *

###### EAUX PREPROCESSING ######
"""Les données proviennent de deux sources : plan d'eau importants et plan d'eaux détails de datagranlyon"""

### CREATE WORKING DIRECTORY ###
create_folder("./output_data/eaux/")

### SCRIPT ###

choice = input("""
    Souhaitez-vous mettre à jour le réseau pondéré par l'eau ? OUI ou NON
""")

if (choice =="OUI"):
    eaux_details = gpd.read_file(data_params["eaux_details"]["gpkg_path"])
    eaux_importants = gpd.read_file(data_params["eaux_importants"]["gpkg_path"])

    eaux_details = eaux_details.to_crs(3946)
    eaux_importants = eaux_importants.to_crs(3946)

    eaux_details["class"] = "detail"
    eaux_importants["class"] = "important"

    # TODO à retravailler pour un choix non arbitraire
    eaux_details["buffer_size"] = 10
    eaux_importants["buffer_size"] = 50

    eaux = pd.concat([eaux_details, eaux_importants])

    eaux.to_file(eaux_path, driver="GPKG", layer="eaux")

    bufferize_with_column(eaux_path, eaux_buffer_path, "eaux", "buffer_size", 5)

    calculate_area_proportion(edges_buffer_path, eaux_buffer_path, "eaux", edges_buffer_eaux_prop_path, "edges")