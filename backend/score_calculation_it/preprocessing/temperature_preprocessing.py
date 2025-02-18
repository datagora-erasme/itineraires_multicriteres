import sys
import os
sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../script_python")
os.environ['USE_PYGEOS'] = '0'
from backend.script_python.function_utils import calculate_weighted_average
import geopandas as gpd
import pandas as pd
import numpy as np
import os
from function_utils import *
from sklearn.preprocessing import MinMaxScaler
from global_variable import *

###### CREATE WORKING DIRECTORY FOR TEMPERATURE ######

###### TEMPERATURE PREPROCESSING ######
"""Data from QGIS calculation to estimate surface temperature from a Landsat capture"""

### FUNCTION ###

def weighted_temp_average(x):
    """
    Calculate the weighted average temperature based on the 'C' values and their corresponding areas.

    Parameters:
    x (pandas.Series): A pandas Series containing temperature data ('C') and area data ('area').

    Returns:
    pandas.Series: A Series containing the weighted average temperature ('C_wavg') rounded to 2 decimal places.
    """
    return pd.Series({
        "C_wavg": round(np.average(x["C"], weights=x["area"]), 2)
        })
    
choice = input("""Do you wish to update the average temperature per segment? (YES) or (NO) \n
    WARNING, the estimated computation time is ~2 hours
""")

if(choice == "YES"):
    print("Calculate Temperature weighted average ")
    calculate_weighted_average(edges_buffer_path, temperature_path, edges_buffer_temp_wavg_path, "edges", "C", weighted_temp_average)

    print("read file")
    temp_edges = gpd.read_file(edges_buffer_temp_wavg_path, layer="edges")

    print("fill na")
    temp_edges["C_wavg"] = temp_edges["C_wavg"].fillna(33)

    print("scale temp")

    scaler = MinMaxScaler(feature_range=(0, 1))

    temp_edges["C_wavg_scaled"] = scaler.fit_transform(temp_edges[["C_wavg"]])

    print(temp_edges.columns)


    print("to file")
    temp_edges.to_file(edges_buffer_temp_wavg_path_no_na, layer="edges")