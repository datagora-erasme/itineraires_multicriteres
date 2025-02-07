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
from function_utils import *


###### BRUIT PREPROCESSING ######
"""Données Ohrane"""

### FUNCTION ###

# Ask if we want to update the noise file size
choice = input("""Do you want to update the noise file size? (YES) or (NO) \n""")
if choice == "YES":
    cut_empreinte(bruit_path, empreinte_path, sortie_path)


# Ask if we want to update the maximum noise per segment
choice = input("""Do you want to update the max noise per segment? (YES) or (NO) \n
# WARNING, the estimated computation time is ~2 hours
#""")


# If the user wants to update the maximum noise per segment
if choice == "YES":
    print("Calculate noise weighted average ")
    #try:
    bruit_pre(edges_buffer_path, bruit_path, edges_buffer_bruit_wavg_path, layer="edges", name="DN")
