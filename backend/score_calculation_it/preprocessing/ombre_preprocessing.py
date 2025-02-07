#%%
import sys
import os
sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../script_python")
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import time
from t4gpd.sun.STHardShadow import STHardShadow
from datetime import datetime, timedelta
from t4gpd.commons.DatetimeLib import DatetimeLib
from function_utils import *
from global_variable import *

#%%
###### CREATE WORKING DIRECTORY FOR OMBRES ######
create_folder("./output_data/ombres/")

##### FUNCTION #####
def overlay_intersect(edges_path, data_path, output_path):
    """
    This function performs a spatial intersection between two geospatial datasets: one representing edges and the other representing some data.
    It reads both datasets, computes the intersection of their geometries, and creates a new GeoDataFrame that stores the intersection results.
    The result includes a "class" column populated with the "datetime" from the intersection dataset, and the geometry from the intersection itself.
    Finally, the resulting GeoDataFrame is saved to a file.

    Parameters:
    edges_path (str): The file path to the edges dataset (GeoPackage or other supported format).
    data_path (str): The file path to the data dataset (GeoPackage or other supported format).
    output_path (str): The file path where the result of the intersection should be saved.

    Returns:
    None: The function saves the intersection result to the output_path.
    """
    data = gpd.read_file(data_path)
    edges = gpd.read_file(edges_path)

    intersection = gpd.overlay(edges, data, how="intersection", keep_geom_type=False)
    data_intersect = gpd.GeoDataFrame()
    data_intersect["class"] = intersection["datetime"]
    data_intersect["geometry"] = intersection["geometry"]
    data_intersect.to_file(output_path, layer="edges", driver="GPKG")

##### SCRIPT #####

#%%

choice = input("""
    Would you like to update the shadow data? YES or NO.
    To do so, make sure that the building data is in the correct location (see README.md).
    The script is designed to run for the date of June 21, 2023, at 8:00 AM, 1:00 PM, and 6:00 PM.
    WARNING: The estimated computation time is ~7 hours.
""")

if (choice == "YES"):
    ## CALCULATE BUILDINGS SHADOWS OF LYON METROPOLE ###
    bat = gpd.read_file(data_params["batiments"]["gpkg_path"])
    bat = bat.to_crs(3946)

    valid_geometry = bat.make_valid()
    bat["geometry"] = valid_geometry

    start = time.time()
    print("reading file ...")

    datetimes = [datetime(2023, 6, 21, 8), datetime(2023, 6, 21, 20), timedelta(hours=5)]
    datetimes = DatetimeLib.generate(datetimes)
    print("start calculate shadows")
    shadows = STHardShadow(bat, datetimes, occludersElevationFieldname='htotale',
        altitudeOfShadowPlane=0, aggregate=True, tz=None, model='pysolar').run()

    shadows = shadows.to_crs(3946)
    print("save file")
    shadows.to_file(shadows_path, driver="GPKG", layer="shadow")

# end = time.time()

# duration = (end-start)/60
# print("duration : ", duration) # around 4 hours

    ###### SPLIT SHADOWS INTO SCHEDULE ######
    shadows = gpd.read_file(shadows_path)

    shadows_08 = shadows[shadows["datetime"] == "2023-06-21 08:00:00+00:00"]
    shadows_13 = shadows[shadows["datetime"] == "2023-06-21 13:00:00+00:00"]
    shadows_18 = shadows[shadows["datetime"] == "2023-06-21 18:00:00+00:00"]

    shadows_08.to_file(shadows_08_path)
    shadows_13.to_file(shadows_13_path)
    shadows_18.to_file(shadows_18_path)

    ##### CLIP SHADOWS WITH EDGES #####
    print("##### CLIP SHADOWS WITH EDGES #####")
    print("8h")
    clip_data(edges_buffer_path, shadows_08_path, shadows_08_clipped_path, 4, "ombres")
    print("13h")
    clip_data(edges_buffer_path, shadows_13_path, shadows_13_clipped_path, 4, "ombres")
    print("18h")
    clip_data(edges_buffer_path, shadows_18_path, shadows_18_clipped_path, 4, "ombres")

    #### EXPLODE SHADOWS INTO SEVERAL POLYGONS #####
    print("##### EXPLODE SHADOWS INTO SEVERAL POLYGONS #####")
    print("8h")
    explode_polygon(shadows_08_clipped_path, shadows_08_explode_path)
    print("13h")
    explode_polygon(shadows_13_clipped_path, shadows_13_explode_path)
    print("18h")
    explode_polygon(shadows_18_clipped_path, shadows_18_explode_path)

    #### CALCULATE INTERSECTION #####
    print("##### CALCULATE INTERSECTION #####")
    print("8h")
    overlay_intersect(edges_buffer_path, shadows_08_explode_path, shadows_08_intersect_path)
    print("13h")
    overlay_intersect(edges_buffer_path, shadows_13_explode_path, shadows_13_intersect_path)
    print("18h")
    overlay_intersect(edges_buffer_path, shadows_18_explode_path, shadows_18_intersect_path)


    #### CALCULATE SHADOWS PROPORTION ON EDGES ######
    print("###### CALCULATE SHADOWS PROPORTION ON EDGES ######")

    print("Calculate shadows proportion")
    print("8h")
    calculate_area_proportion(edges_buffer_path, shadows_08_intersect_path, "ombres", edges_buffer_ombres_08_prop_path, "edges")
    print("13h")
    calculate_area_proportion(edges_buffer_path, shadows_13_intersect_path, "ombres", edges_buffer_ombres_13_prop_path, "edges")
    print("13h")
    calculate_area_proportion(edges_buffer_path, shadows_18_intersect_path, "ombres", edges_buffer_ombres_18_prop_path, "edges")

#%%
    ombre_13 = gpd.read_file(edges_buffer_ombres_13_prop_path)
    ombre_13 = ombre_13.rename(columns={"ombres_prop": "ombres_13_prop"})
    ombre_13.to_file(edges_buffer_ombres_13_prop_path, driver="GPKG", layer="edges")

    ombre_18 = gpd.read_file(edges_buffer_ombres_18_prop_path)
    ombre_18 = ombre_18.rename(columns={"ombres_prop": "ombres_18_prop"})
    ombre_18.to_file(edges_buffer_ombres_18_prop_path, driver="GPKG", layer="edges")
# %%
