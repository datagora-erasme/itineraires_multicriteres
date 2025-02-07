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


cut_empreinte(edges_buffer_path, empreinte_path, sortie_path)