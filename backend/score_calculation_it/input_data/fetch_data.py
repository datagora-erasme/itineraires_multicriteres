import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
from owslib.wfs import WebFeatureService
import sys
sys.path.append("../../")
from global_variable import *

###### FETCH DATA FROM DATAGRANDLYON ######

### GLOBAL VARIABLE ###
# geojsonOutputFormat = "application/json; subtype=geojson"
geojsonOutputFormat = "application/json"

### FUNCTION ###
def create_folder(folder_path):
    exist = os.path.exists(folder_path)
    if not exist:
        os.makedirs(folder_path)
        print(f"{folder_path} created")

def connection_wfs(url, service_name, version):
    """ Return a wfs object after connecting to a service thanks the url provided """
    print(f"Connecting {service_name} WFS ... ")
    wfs=None
    try:
        wfs = WebFeatureService(url, version)
        print(f"SUCCESS : Connected to {service_name}")
    except NameError:
        print(f"Error while connecting to {service_name} ... : {NameError}")
    print(url)
    return wfs

def download_data(params, data_name, wfs, outputFormat):
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
        print(data)
        print(f"{data_name} fetched with success")
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
    

def download_all_data(parametre, wfs, outputFormat):
    print("FETCHING ALL DATA")
    for data_name in parametre.keys():
        download_data(parametre, data_name, wfs, outputFormat)

### SCRIPT ###

## WFS CONNECTION ##
print("WFS CONNECTION")
# data_grandlyon_wfs_url = "https://download.data.grandlyon.com/wfs/grandlyon?SERVICE=WFS&VERSION=2.0.0"
data_grandlyon_wfs_url = "https://data.grandlyon.com/geoserver/metropole-de-lyon/ows?SERVICE=WFS&VERSION=2.0.0"
data_grandlyon_wfs = connection_wfs(data_grandlyon_wfs_url, "datagrandlyon", "2.0.0")

# tourisme WFS
#data_grandlyon_tourisme_wfs_url = "https://data.grandlyon.com/geoserver/wfs"
#data_grandlyon_tourisme_wfs = connection_wfs(data_grandlyon_tourisme_wfs_url, "datagrandlyon", "2.0.0")



## DATA DOWNLOAD ##

fetching_choice = input("\n Voulez-vous télécharger toutes (ALL) les données, une seule (ONE) ou seulement les données à afficher sur l'application web (WEB_ONLY) ? \n Veuillez entrer ALL, ONE ou WEB_ONLY selon votre choix : ")
print("Data Download")

if(fetching_choice == "ALL"):
### Download all data ###
    download_all_data(data_params, data_grandlyon_wfs, geojsonOutputFormat)
    #download_all_data(data_params_tourisme, data_grandlyon_tourisme_wfs, geojsonOutputFormat)

elif(fetching_choice == "ONE"):
###  download a specific data ###
    available_data = [data_name for data_name in data_params.keys()]
    data_choice = input(f"Veuilez choisir un identifiant de données parmi la liste suivante : {available_data} : \n")

    if(data_choice in available_data):
        download_data(data_params, data_choice, data_grandlyon_wfs, geojsonOutputFormat)
    else:
        print("Veuillez entrer un identifiant présent dans la liste")
elif(fetching_choice == "WEB_ONLY"):
    data_web = {data_name : data_param for data_name, data_param in data_params.items() if data_param["onMap"] == True}
    download_all_data(data_web, data_grandlyon_wfs, geojsonOutputFormat)
else:
    print("VEUILLEZ entrer un choix valide (ALL, ONE ou WEB_ONLY)")


"""
wfs_url="
https://ows.region-bretagne.fr/geoserver/rb/wfs?service=wfs&request=getCapabilities
"
response=requests.get(wfs_url).content 
    
"""
