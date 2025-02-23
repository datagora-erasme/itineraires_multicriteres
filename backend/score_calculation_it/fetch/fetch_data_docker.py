import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
from owslib.wfs import WebFeatureService
import sys
sys.path.append("/app")  # Adjust this path as needed

from global_variable import *

###### FETCH DATA FROM DATAGRANDLYON ######

### GLOBAL VARIABLE ###
# geojsonOutputFormat = "application/json; subtype=geojson"
geojsonOutputFormat = "application/json"

### FUNCTION ###
def create_folder(folder_path):
    """
    Creates a new folder at the specified path if it does not already exist.

    Parameters:
    folder_path (str): The path where the new folder should be created.

    If the folder does not exist, it is created, and a confirmation message is printed.
    If the folder already exists, no action is taken.
    """
    exist = os.path.exists(folder_path)
    if not exist:
        os.makedirs(folder_path)
        print(f"{folder_path} created")

def connection_wfs(url, service_name, version):
    """
    Establishes a connection to a WFS (Web Feature Service) using the provided URL, service name, and version.

    Parameters:
    url (str): The URL of the WFS service to connect to.
    service_name (str): The name of the WFS service.
    version (str): The version of the WFS service to be used.

    Returns:
    WebFeatureService or None: Returns the WFS object if the connection is successful, or None if an error occurs.
    
    Prints:
    - A success message if the connection is established.
    - An error message if the connection fails due to a `NameError`.
    """

    """ Return a wfs object after connecting to a service thanks the url provided """
    print(f"Connecting {service_name} WFS ... ")
    wfs=None
    try:
        wfs = WebFeatureService(url, version)
        print(f"SUCCESS : Connected to {service_name}")
    except NameError:
        print(f"Error while connecting to {service_name} ... : {NameError}")

    return wfs

def download_data(params, data_name, wfs, outputFormat):
    """
    Downloads geographic data from a WFS service, saves it in both GeoPackage and GeoJSON formats, and converts its CRS.

    Parameters:
    params (dict): Dictionary containing paths and other parameters for data storage.
    data_name (str): The name of the data to download and process.
    wfs (WebFeatureService): The WFS service object used to fetch the data.
    outputFormat (str): The desired format for the downloaded data (e.g., "application/geo+json").

    Process:
    - Downloads data using WFS service with a specified filter.
    - Saves the data to GeoJSON and GeoPackage formats.
    - Converts the coordinate reference system (CRS) to both EPSG:3946 (for Lyon's metropole) and EPSG:4326 (for Leaflet).
    - Creates a folder for storing the data if it doesn't exist.

    Returns:
    None

    Side effects:
    - Creates a folder for the data if it doesn't already exist.
    - Writes the downloaded data to specified output files (GeoJSON and GeoPackage).
    """
    create_folder(f"./{data_name}/")
    print(f"Downloading {data_name}")
    data_key = params[data_name]["wfs_key"]
    gpkg_output_path = params[data_name]["gpkg_path"]
    geojson_output_path = params[data_name]["geojson_path"]

    bbox = wfs.contents[data_key].boundingBoxWGS84
    try:
        #FOR NOW BUG WIT bbox for toilettes and fontaines with datagrandlyon, when corrected : replace the following
        # line by this one : data = wfs.getfeature(typename=data_key, bbox=bbox, outputFormat=outputFormat, filter="sortBy=gid")
        data = wfs.getfeature(typename=data_key, outputFormat=outputFormat, filter="sortBy=gid")
        print(f"{data_name} fetched with sucess")
    except NameError:
        print(f"Error fetching {data_name}")

    file = open(geojson_output_path, "wb")
    file.write(data.read())
    file.close()

    data_gpd = gpd.read_file(geojson_output_path)

    #crs : 3946 more accurate crs for Lyon metropole
    data_gpkg = data_gpd.to_crs(3946)
    data_gpkg.to_file(gpkg_output_path, driver="GPKG", layer=data_name)

    #crs : 4326 for leaflet
    data_geojson = data_gpd.to_crs(4326)
    data_geojson.to_file(geojson_output_path, driver="GeoJSON")
    

def download_all_data(params, wfs, outputFormat):
    """
    Downloads all geographic data specified in the parameters, saving them in both GeoPackage and GeoJSON formats.

    Parameters:
    params (dict): Dictionary containing paths and other parameters for data storage for each data item.
    wfs (WebFeatureService): The WFS service object used to fetch the data.
    outputFormat (str): The desired format for the downloaded data (e.g., "application/geo+json").

    Process:
    - Iterates over all data names in the `params` dictionary.
    - For each data name, it fetches the data from the WFS service and saves it in GeoPackage and GeoJSON formats.
    - Converts the coordinate reference system (CRS) to both EPSG:3946 (for Lyon's metropole) and EPSG:4326 (for Leaflet).

    Returns:
    None

    Side effects:
    - Downloads and saves all the data specified in the `params` dictionary to the appropriate files.
    - Creates folders for each data item if they don't already exist.
    """
    print("FETCHING ALL DATA")
    for data_name in params.keys():
        download_data(params, data_name, wfs, outputFormat)

### SCRIPT ###

## WFS CONNECTION ##
print("WFS CONNECTION")
# data_grandlyon_wfs_url = "https://download.data.grandlyon.com/wfs/grandlyon?SERVICE=WFS&VERSION=2.0.0"
data_grandlyon_wfs_url = "https://data.grandlyon.com/geoserver/metropole-de-lyon/ows?SERVICE=WFS&VERSION=2.0.0"
data_grandlyon_wfs = connection_wfs(data_grandlyon_wfs_url, "datagrandlyon", "2.0.0")

## DATA DOWNLOAD ##

data_web = {data_name : data_param for data_name, data_param in data_params.items() if data_param["onMap"] == True}
download_all_data(data_web, data_grandlyon_wfs, geojsonOutputFormat)



