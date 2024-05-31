import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
from fancyimpute import IterativeImputer
import numpy as np
from sklearn.metrics import r2_score
import pandas as pd
import json
import fiona
from data_utils import *
import time

##### PCA IMPUTATION FOR Nan values ######
"""
    Some columns have missing values such as the rayoncouronne one
    Rather than inputing a default value, this is better to imput values based on the other columns. 
    For example two trees of the same species planted at the same time will have most likely the same rayoncouronne.

"""

def pca_multiple_imputation(file_path, column_to_impute):
    print(f"PCA imputation for {file_path} on column {column_to_impute} ... ")
    # read in data
    data = gpd.read_file(file_path)

    # create a copy of the data for imputation
    impute_data = data.copy()

    # impute missing values with iterative imputation
    imputer = IterativeImputer()
    imputed_data = imputer.fit_transform(impute_data[[column_to_impute]])

    impute_data.loc[:, column_to_impute] = imputed_data

    impute_data.to_file(file_path, driver="GPKG")


##### BUFFERING #####

"""
    I choose to make one function per data for the buffer calculation because I hope we'll find / use more accurate attributes 
    to calculate the influence area such as the "rayoncouronne_m" for the trees.

"""

def trees_calculate_buffer_size(file_path, default_buffer_size = 10, default=False):
    print("Calculating tree buffer size")
    trees = gpd.read_file(file_path)

    if(default):
       trees["buffer_size"] = default_buffer_size
    else:
        #buffer size can be a formula between several fields
        trees["buffer_size"] = trees["rayoncouronne_m"]
        
    trees.to_file(file_path, driver="GPKG")

##### Freshness Indicator #####

""" Some data have a more complex freshness Indicator such as the trees
"""


##### Merge Data #####

def merge_data(chunksize):
    print("Merging data into one file ... ")
    with open("./data_informations.json", "r") as f: 
        data_informations = json.load(f)
    
    file_paths = []

    for d_name, d_info in data_informations["data_wfs"].items():
        file_paths.append(d_info["buffered_path"])

    for d_name, d_info in data_informations["raw_data"].items():
        file_paths.append(d_info["path"])

    merged_data = gpd.GeoDataFrame()

    # iterate over each file and append to merged_data
    for file_path in file_paths:
        # read in the data
        for chunk in gpd.read_file(file_path, chunksize=chunksize, driver="GPKG"):
        # append to merged_data
            merged_data = gpd.GeoDataFrame(pd.concat([merged_data, chunk], ignore_index=True))

    # write merged data to a new file
    merged_data.to_file('./data/merged.gpkg', driver='GPKG')

def calculate_IF(poly1, poly2):
    """Function to calculate final IF

    Formula to work on, for now a simple sum
    """

    filtered_poly1 = filter_dictionnary(poly1, "IF_")
    filtered_poly2 = filter_dictionnary(poly2, "IF_")

    IF=0
    for k1, v1 in filtered_poly1.items():
        if(v1):
            IF+=v1
    for k2, v2 in filtered_poly2.items():
        if(v2):
            IF+=v2
    
    return IF

def write_IF():
    """ This function recalate an IF for each polygon / intersection between the polygons into the merged data"""

    print("Calculating IF ... ")

    data = gpd.read_file('./data/merged.gpkg')

    # iterate over the polygons
    for i, poly1 in data.iterrows():
        # iterate over the remaining polygons
        for j, poly2 in data.iloc[i+1:].iterrows():
            # check for intersection
            if poly1.geometry.intersects(poly2.geometry):

                poly1_attributes = extract_attributes(data, i)
                poly2_attributes = extract_attributes(data, j)

                IF = calculate_IF(poly1_attributes, poly2_attributes)

                # update the field value for both polygons
                data.at[i, 'IF'] = IF
                data.at[j, 'IF'] = IF

    #write the updated data back to the gpkg file
    data.to_file('./data/merged_if.gpkg', driver='GPKG')

# start_time = time.time()
# write_IF()
# end_time = time.time()

# duration = (end_time - start_time) / 60

# print(f'duration : {duration}')

def extract_intersection(input_path, output_path):
    print("extraction of intersection ...")
    data = gpd.read_file(input_path)
    intersections = gpd.overlay(data, data, how="intersection")
    intersections.to_file(output_path)

def extract_difference(input_path, output_path):
    print("extraction of differences")
    data = gpd.read_file(input_path)
    intersections = gpd.overlay(data, data, how="difference")
    intersections.to_file(output_path)


# extract_intersection("./data/merged.gpkg", "./data/merged_inter.gpkg")
# extract_difference("./data/merged.gpkg", "./data/merged_diff.gpkg")

# start_time = time.time()
# merge_data(10000)
# end_time = time.time()

# duration = (end_time - start_time) / 60

# print(f'duration : {duration}')

