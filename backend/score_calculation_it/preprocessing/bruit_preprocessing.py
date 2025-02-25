import os
import sys
sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../script_python")
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from global_variable import *
from osgeo import gdal, ogr
from function_utils import *

###### BRUIT PREPROCESSING ######
"""Données Ohrane"""

### FUNCTION ###

# Ask if we want to update the noise file size
choice = input("""Do you want to update the noise file size? (YES) or (NO) \nOnly choose (YES) if bruit_decoupe_path file is not up to date with bruit.gpkg\n""")
if choice == "YES":
    cut_empreinte(bruit_path, bounding_metrop_path, bruit_decoupe_path)


# Ask if we want to update the maximum noise per segment
choice = input("""Do you want to update the max noise per segment? (YES) or (NO) \n
# WARNING, the estimated computation time is ~2 hours
#""")


# If the user wants to update the maximum noise per segment
if choice == "YES":
    print("Calculate noise weighted average ")
    #try:
    bruit_pre(edges_buffer_path, bruit_decoupe_path, edges_buffer_bruit_wavg_path, layer="edges", name="DN")
