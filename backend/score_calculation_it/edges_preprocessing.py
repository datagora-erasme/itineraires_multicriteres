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

# Demander si on souhaite mettre à jour la taille du fichier edges
choice = input("""Souhaitez-vous mettre à jour taille du fichier edges ? (OUI) ou (NON) \n""")
if choice == "OUI":
    cut_edges(edges_buffer_path, empreinte_path, sortie_path)