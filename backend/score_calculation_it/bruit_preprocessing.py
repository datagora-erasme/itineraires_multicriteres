import os

os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
import numpy as np
from data_utils import *
from sklearn.preprocessing import MinMaxScaler
import sys
sys.path.append("../")
from global_variable import *
from osgeo import gdal, ogr
import os


###### BRUIT PREPROCESSING ######
"""Données Ohrane"""

### FUNCTION ###

# Demander si on souhaite mettre à jour la taille du fichier bruit
choice = input("""Souhaitez-vous mettre à jour taille du fichier bruit ? (OUI) ou (NON) \n""")
if choice == "OUI":
    cut_bruit(bruit_path, empreinte_path, sortie_path)


# Demander si on souhaite mettre à jour le bruit max par segment
choice = input("""Souhaitez-vous mettre à jour le bruit max par segment ? (OUI) ou (NON) \n
# ATTENTION, le temps de calcul estimé est de ~2h
#""")

# Si l'utilisateur souhaite mettre à jour le bruit max par segment
if choice == "OUI":
    print("Calculate noise weighted average ")
    #try:
    bruit_pre(edges_buffer_path, bruit_path, edges_buffer_bruit_wavg_path, layer="edges", name="DN")
