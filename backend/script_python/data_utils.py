import os
os.environ['USE_PYGEOS'] = '0'
from owslib.wfs import WebFeatureService
from owslib.wms import WebMapService
import geopandas as gpd
import json
import fiona

import os

# # Get the absolute path of the current file
# absolute_path = os.path.abspath(__file__)

# # Get the directory name of the current file
# directory_name = os.path.dirname(absolute_path)

# # Get the relative path of the current file
# relative_path = os.path.relpath(absolute_path)

# print("Absolute path:", absolute_path)
# print("Directory name:", directory_name)
# print("Relative path:", relative_path)


data_informations_path = "./data/data_informations.json"

def create_data_informations_file():
    """ Fonction to instantiate data_informations.json file """

    data_informations = {
        "services" : {
            "data.grandlyon_wfs": "https://download.data.grandlyon.com/wfs/grandlyon?SERVICE=WFS&VERSION=2.0.0",
            "data.grandlyon_wms" : "https://download.data.grandlyon.com/wms/grandlyon?VERSION=1.3.0&SERVICE=WMS"
        },
        "osm": {
            "network_parameters": {  
            }
        },
        "data_wfs" : {
            "fontaines_potables": {
                "name": "Fontaines potables",
                "wfs_key": "ms:epo_eau_potable.epobornefont",
                "service": "data.grandlyon_wfs",
                "marker_option": {
                "iconUrl": "droplet.svg",
                "iconRetinaUrl": "droplet.svg",
                "popupAnchor":  [-0, -0],
                "iconSize": [40,40],
                "clusterCountStyle" : "position:absolute;top:20px;left:-9px;color:white;font-weight:bold;"
                }
            },
            "toilettes_publiques": {
                "name": "Toilettes publiques",
                "wfs_key": "ms:adr_voie_lieu.adrtoilettepublique_latest",
                "service": "data.grandlyon_wfs",
                "marker_option": {
                "iconUrl": "toilet.svg",
                "iconRetinaUrl": "toilet.svg",
                "popupAnchor":  [-0, -0],
                "iconSize": [40,40],
                "clusterCountStyle" : "position:absolute;top:48px;left:-6px;color:black;font-weight:bold;"
                }
            },
            "fontaines_ornementales": {
                "name": "Fontaines ornementales",
                "wfs_key": "ms:adr_voie_lieu.adrfontaineornem_latest",
                "service": "data.grandlyon_wfs",
                "marker_option": {
                "iconUrl": "fountain.svg",
                "iconRetinaUrl": "fountain.svg",
                "popupAnchor":  [-0, -0],
                "iconSize": [40,40],
                "clusterCountStyle" : "position:absolute;top:48px;left:0px;color:black;font-weight:bold;"
            }
            },
            "parcs_jardins_metropole": {
                "name": "Parcs et jardins",
                "wfs_key": "ms:com_donnees_communales.comparcjardin_1_0_0",
                "service": "data.grandlyon_wfs",
            },
            "bancs": {
                "name": "Bancs",
                "wfs_key": "ms:adr_voie_lieu.adrbanc_latest",
                "service": "data.grandlyon_wfs",
                "marker_option": {
                "iconUrl": "bench.svg",
                "iconRetinaUrl": "bench.svg",
                "popupAnchor":  [-0, -0],
                "iconSize": [25,25],
                "clusterCountStyle": "position:absolute;top:0px;left:-10px;color:black;font-weight:bold;"
            }
            },
            # "arbres_alignement": {
            #     "wfs_key": "ms:abr_arbres_alignement.abrarbre",
            #     "service": "data.grandlyon_wfs",
            # },
            # à mettre dans un second temps 
            # "hauteur_batiment": {
            #     "wfs_key": "ms:fpc_fond_plan_communaut.fpctoit_2018",
            #     "service": "data.grandlyon_wfs"
            # }
                
        },
        "data_wms": {
            "vegetation_stratifie" : {
                "wms_key": "MNC_class_2022_INT1U",
                "service" : "data.grandlyon_wms",
                "width" : 3500,
                "height": 3640,
                "format" : "png",
                "transparent" : True,
                "srs": "EPSG:4171"
            }
        },
        "data_raw" : {
            # "vegetation_stratifie_raw" : {
            #     "name": "Végétation stratifiée",
            #     "gpkg_path": "./backend/script_python/data/raw_data/vegetation_stratifie.gpkg"
            # },
            "temp_surface_road_raw": {
                "name": "Température de surface",
                "gpkg_path": "./raw_data/temp_surface.gpkg"
            },
        #     "joined_if": {
        #         "name" : "Calque fraîcheur",
        #         "gpkg_path": "./backend/script_python/data/raw_data/joined_if_3946.gpkg",
        # }
        }
    }

    with open(data_informations_path, "w") as f:
        json.dump(data_informations, f, indent=4)


def create_folder(folder_path):
    """
    Creates a folder at the specified path if it does not already exist.
    
    Parameters:
    -----------
    folder_path : str
        The path where the folder should be created.
    
    Returns:
    --------
    None
        The function creates the folder and prints a message if the folder is created.
    """
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

    return wfs

def connection_wms(url, service_name, version):
    """ Return a wms object after connecting to a service thanks the url provided """
    print(f"Connecting {service_name} WMS ... ")
    wms=None
    try:
        wms = WebMapService(url, version)
        print(f"SUCCESS : Connected to {service_name}")
    except NameError:
        print(f"Error while connecting to {service_name} ... : {NameError}")

    return wms

def download_data_wfs(service_name, version, path):
    """ load a list of data from one specific service 
        the data are stored in a json file as a dictionnary wich elements have the folowing form : 

        "data_name" : {
            "wfs_key" : 'key',
            "service" : 'service_name',
            "download_path": "path/file.gml"
        }
    """

    with open(data_informations_path, "r") as f:
        data_informations = json.load(f)

    data_wfs = data_informations["data_wfs"]
    services = data_informations["services"]

    wfs = connection_wfs(services[f"{service_name}"], service_name, version)

    for d_name, d_info in data_wfs.items():
        if(d_info["service"] == service_name):

            print(f"### {d_name} ###")

            # the boundingBox define the area where the data should belong to
            box = wfs.contents[f"{d_info['wfs_key']}"].boundingBoxWGS84

            print(f"fetching {d_name} ..")
            try:
                new_data = wfs.getfeature(typename=f"{d_info['wfs_key']}", bbox=box)
                print(f"SUCCESS")
            except NameError:
                print(f"Error while fetching {d_name} from {service_name}... : {NameError}")


            print(f"writing {d_name} GML file into {path} \n")

            #write file into given folder (path)
            file = open(f"{path}/{d_name}.gml", "wb")
            file.write(new_data.read())
            file.close()

            #store download path into data_informations.json
            data_informations["data_wfs"][d_name]["gml_path"] = f"{path}/{d_name}.gml"

    # re-write data_informations.json => store all download path
    with open(data_informations_path, "w") as f:
        json.dump(data_informations, f, indent=4)


def download_data_wms(service_name, version, path):
    """ load a list of data from one specific service 
        the data are stored in a json file as a dictionnary wich elements have the folowing form : 

        "data_name" : {
            "wfs_key" : 'key',
            "service" : 'service_name',
            "download_path": "path/file.gml"
        }
    """

    with open(data_informations_path, "r") as f:
        data_informations = json.load(f)

    data_wms = data_informations["data_wms"]
    services = data_informations["services"]

    wms = connection_wms(services[f"{service_name}"], service_name, version)

    for d_name, d_info in data_wms.items():
        if(d_info["service"] == service_name):

            print(f"### {d_name} ###")

            # the boundingBox define the area where the data should belong to
            box = wms.contents[f"{d_info['wms_key']}"].boundingBoxWGS84

            print(f"fetching {d_name} ..")
            print(d_info['wms_key'])
            try:
                img = wms.getmap(layers=[f"{d_info['wms_key']}"], bbox=box, 
                                 size=(d_info["width"], d_info["height"]), srs=d_info["srs"], format=f"image/{d_info['format']}" ,
                                   transparent=d_info["transparent"])
                print(f"SUCCESS")
            except NameError:
                print(f"Error while fetching {d_name} from {service_name}... : {NameError}")


            print(f"writing {d_name} Raster file into {path} \n")

            #write file into given folder (path)
            file = open(f"{path}/{d_name}.{d_info['format']}", "wb")
            file.write(img.read())
            file.close()

            #store download path into data_informations.json
            data_informations["data_wms"][d_name][f"{d_info['format']}_path"] = f"{path}/{d_name}.{d_info['format']}"

    # re-write data_informations.json => store all download path
    with open(data_informations_path, "w") as f:
        json.dump(data_informations, f, indent=4)


def convert_file(input_path, output_path, driver, input_extension = "gml", output_extension='gpkg', folder=False):
    """Convert file type
    If folder = TRUE, all of the files of the given folder are converted to the desired format. 
    Careful about the path : either a folder or a file one. 
    """
    print("converting ... ")
    if(folder):
        for filename in os.listdir(input_path):
            print(f"filename : {filename}")
            if filename.endswith(input_extension):
                # Read input GML file into a GeoDataFrame
                gdf = gpd.read_file(os.path.join(input_path, filename))

                if(driver == "GeoJSON"):
                    # 4326 is crs of OSM => used to project data on leaflet
                    gdf = gdf.to_crs(epsg=4326)
                    print("CRS of GEOJSON: ", gdf.crs)
                
                if(driver == "GPKG"):
                    gdf = gdf.to_crs(epsg=3946)
                
                # Set output file path and name
                output_name = filename.replace(input_extension, output_extension)
                new_output_path = os.path.join(output_path, output_name)

                # Write GeoDataFrame to output Shapefile
                gdf.to_file(new_output_path, driver=driver)

                print("Done, all GML files converted into GPKG")
    else:

        gdf = gpd.read_file(input_path)
        if(driver == "GeoJSON"):
            # 4326 is crs of OSM => used to project data on leaflet
            gdf = gdf.to_crs(epsg=4326)
        if(driver == "GPKG"):
            gdf = gdf.to_crs(epsg=3946)
        gdf.to_file(output_path, driver=driver)
        print(f"Done, {input_path} converted into {output_extension}")

def convert_all(output_path_folder, input_extension, output_extension, driver, connection_type="wfs"):

    """Convert all data stored in data_informations from input format to ouput format"""

    with open(data_informations_path, "r") as f:
        data_informations = json.load(f)
    
    data = data_informations[f'data_{connection_type}']
    for d_name, d_info in data.items():
        download_path = d_info[f"{input_extension}_path"]
        if(download_path.endswith(input_extension)):
            new_path = f"{output_path_folder}{d_name}.{output_extension}"
            convert_file(download_path, new_path, input_extension=input_extension, output_extension=output_extension, driver=driver)
            if(driver == "GeoJSON"):
                data_informations[f"data_{connection_type}"][d_name][f"geo{output_extension}_path"] = new_path
            else:
                data_informations[f"data_{connection_type}"][d_name][f"{output_extension}_path"] = new_path

    with open(data_informations_path, "w") as f:
        json.dump(data_informations, f, indent=4)

def points_to_polygon(point_path, polygon_path):
    """
        Computes the convex hull of a point shapefile and converts it to a polygon shapefile
    """

    points = gpd.read_file(point_path)

    # change temporarily the CRS (projection system) because buffering need meter
    # points.to_crs(epsg=3857)

    # Create a buffer around each point
    buffered_points = points.buffer(points["buffer_size"])

    # Convert the buffered points to polygons
    polygons = buffered_points.geometry.apply(lambda x: x.convex_hull)

    # Create a new GeoDataFrame with the polygon geometry and any additional attributes from the original points shapefile
    polygon_gdf = gpd.GeoDataFrame(points.drop('geometry', axis=1), geometry=polygons, crs=3946)

    # final_polygon = polygon_gdf.to_crs(epsg=4171)

    polygon_gdf.to_file(polygon_path, driver="GPKG")

def convert_all_points_into_polygons(output_path_folder):
    """ Convert all shapefile with Points Type into Polygons """

    with open(data_informations_path, "r") as f:
        data_informations = json.load(f)

    for d_name, d_info in data_informations["data_wfs"].items():
        original_gpkg_file = gpd.read_file(d_info["cleaned_data_path"])
        #if(original_gpkg_file.geom_type[0] == "Point"):
        buffered_path = f"{output_path_folder}{d_name}_buffered.gpkg"

        print(f"Converting {d_name} into Polygons ... ")

        points_to_polygon(d_info["cleaned_data_path"], buffered_path)
        data_informations["data_wfs"][d_name]["buffered_path"] = buffered_path

    
    with open(data_informations_path, "w") as f:
        json.dump(data_informations, f, indent=4)
            

def get_attributes_list(file_path):
    file = gpd.read_file(file_path)
    attribute_list = list(file.columns)
    return(attribute_list)

def write_all_atributes():
    """ Write into data_informations.json all attributes of the layer """

    print("Writing all attributes into data_informations.json file ...")

    with open(data_informations_path, "r") as f:
        data_informations = json.load(f)

    data_wfs = data_informations['data_wfs']
    for d_name, d_info in data_wfs.items():
        #the shape file is the original file containing all attributes
        file_path = data_wfs[d_name]["gpkg_path"]
        attribute_list = get_attributes_list(file_path)
        #print(f"{d_name} = {attribute_list}")
        data_informations["data_wfs"][d_name]["all_attributes"] = attribute_list

    with open(data_informations_path, "w") as f:
        json.dump(data_informations, f, indent=4)

    print("DONE")

def write_attributes_to_add_and_remove(data_name, attributes_to_add, attributes_to_remove):
    """ Write into data_informations.json all attributes to add or remove for one data
        attributes_to_add is a dictionnary with the pair key, values, 
        attributes_to_remove is a list of attributes

        attributes_to_add = {
            attribute1 : default_value1
            attribute2 : default_value2
        }
        attributes_to_remove = ["attribute1", "attribute2"]
    """

    with open(data_informations_path, "r") as f: 
        data_informations = json.load(f)

    data_informations['data_wfs'][data_name]['attributes_to_remove'] = attributes_to_remove
    data_informations['data_wfs'][data_name]['attributes_to_add'] = attributes_to_add

    with open(data_informations_path, "w") as f:
        json.dump(data_informations, f, indent=4)
    

def remove_attributes(input_path, output_path, attributes_to_remove):
    file = gpd.read_file(input_path)
    file = file.drop(attributes_to_remove, axis=1)
    file.to_file(output_path)

def add_attributes(input_path, output_path, attributes_to_add):
    """attributes_to_add should be a dictionnary with the following structure : 
    
    attributes_to_add = {
        'new_attribute1': [1, 2, 3],
        'new_attribute2': ['a', 'b', 'c']
    }

    This function can be used to update the attributes
    
    """
    file = gpd.read_file(input_path)

    for attribute_name, values in attributes_to_add.items():
        file[attribute_name] = values
    
    file.to_file(output_path)

def remove_and_add_attributes(output_path_folder):
    """
    Removes specified attributes and adds new attributes to the GeoPackage files.
    
    For each dataset in the 'data_wfs' section of the configuration, this function:
    1. Removes the listed attributes from the input GeoPackage.
    2. Adds the new attributes to the GeoPackage.
    3. Saves the modified GeoPackage to the output folder.
    4. Updates the path to the cleaned dataset in the configuration file.

    Parameters:
    -----------
    output_path_folder : str
        The folder where the cleaned GeoPackages will be saved.

    Returns:
    --------
    None
        The function modifies the GeoPackage files and updates the configuration.
    """
    
    with open(data_informations_path, "r") as f:
        data_informations = json.load(f)

    data_wfs = data_informations["data_wfs"]
    for d_name, d_info in data_wfs.items():
        print(f"Remove and Add attributes for {d_name}")
        input_path = d_info["gpkg_path"]
        output_path = f"{output_path_folder}{d_name}_cleaned.gpkg"
        remove_attributes(input_path, output_path, d_info["attributes_to_remove"])
        add_attributes(output_path, output_path, d_info["attributes_to_add"])

        data_informations["data_wfs"][d_name]["cleaned_data_path"] = output_path
    
    with open(data_informations_path, "w") as f:
        json.dump(data_informations, f, indent=4)


def print_layers_name(folder_path):
    """
    Prints the names of the layers in all GeoPackage files (.gpkg) within a given folder.
    
    For each GeoPackage file in the specified folder, the function:
    1. Opens the file.
    2. Retrieves the names of the layers.
    3. Prints the file path and layer names.

    Parameters:
    -----------
    folder_path : str
        The path to the folder containing the GeoPackage files.
    
    Returns:
    --------
    None
        The function prints the paths and layer names to the console.
    """
    for filename in os.listdir(folder_path):
        if filename.endswith(".gpkg"):
            file_path = os.path.join(folder_path, filename)
            print(file_path)
            with fiona.open(file_path) as gpkg:
                layer_names = fiona.listlayers(file_path)
                print(f"{filename} : {layer_names}")


def extract_attributes(gdf, index):
    """
    Extracts attributes (non-geometry columns) from a GeoDataFrame for a given index.
    
    This function iterates through all columns in the GeoDataFrame and collects the
    values of all columns except for the "geometry" column, returning them as a dictionary.

    Parameters:
    -----------
    gdf : geopandas.GeoDataFrame
        The GeoDataFrame from which attributes are to be extracted.
    
    index : int
        The index of the row in the GeoDataFrame for which attributes are extracted.
    
    Returns:
    --------
    dict
        A dictionary containing the attributes (column names as keys and their values as values) 
        for the specified index.
    """
    attributes = {}
    for column in gdf.columns:
        if column != "geometry":
            attributes[column] = gdf.loc[index, column]
    return attributes

def filter_dictionnary(dictionnary, filter):
    """
    Filters the given dictionary by checking if the filter string is present in the keys.

    This function creates a new dictionary that includes only the key-value pairs where the
    key contains the specified filter string.

    Parameters:
    -----------
    dictionnary : dict
        The dictionary to be filtered.
    
    filter : str
        The string to check for presence in the dictionary keys.

    Returns:
    --------
    dict
        A filtered dictionary containing only the items where the key contains the filter string.
    """
    return {k: v for k, v in dictionnary.items() if filter in k}

def convert_gpkg_into_geojson(input_path, output_path):
    """
    Converts a GeoPackage file (.gpkg) into a GeoJSON file (.geojson).

    This function reads a GeoPackage file, reprojects its contents to the EPSG:4326 coordinate 
    reference system (commonly used by Leaflet), and saves it as a GeoJSON file.

    Parameters:
    -----------
    input_path : str
        The path to the input GeoPackage file.
    
    output_path : str
        The path to save the output GeoJSON file.
    
    Returns:
    --------
    None
        The function saves the converted GeoJSON file to the specified output path.
    """
    gdf = gpd.read_file(input_path)

    # 4326 is the CRS of OSM, used to project data for Leaflet
    gdf = gdf.to_crs(epsg=4326)

    print("Converting GPKG into GeoJSON")
    gdf.to_file(output_path, driver='GeoJSON')
    print("Done")


# create_folder("./data/geojson")
#convert_gpkg_into_geojson("./data/osm/shortest_path/big_shortest_path_IF_3946.gpkg", "./data/geojson/sp_IF_3946.json")
#convert_gpkg_into_geojson("./data/raw_data/joined_if_3946.gpkg", "./pocwa-init/src/data/joined_if_3946.json")

# convert_gpkg_into_geojson("./data/gpkg/bancs.gpkg", "./data/geojson/bancs.json")

# convert_gpkg_into_geojson("./data/gpkg/fontaines_ornementales.gpkg", "./data/geojson/fontaines_ornementales.json")

# convert_gpkg_into_geojson("./data/gpkg/fontaines_potables.gpkg", "./data/geojson/fontaines_potables.json")

# convert_gpkg_into_geojson("./data/gpkg/parcs_jardins_metropole.gpkg", "./data/geojson/parcs_jardins_metropole.json")

# convert_gpkg_into_geojson("./data/gpkg/toilettes_publiques.gpkg", "./data/geojson/toilettes_publiques.json")