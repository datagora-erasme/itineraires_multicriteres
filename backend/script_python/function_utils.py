from datetime import datetime
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
import multiprocessing as mp
import numpy as np
from shapely.wkt import loads, dumps
from shapely.validation import make_valid
from shapely.geometry import Polygon, MultiPolygon
import subprocess
from osgeo import ogr
from sklearn.preprocessing import MinMaxScaler

def create_folder(folder_path):
    """
    Create a folder at the specified path if it does not already exist.

    Args:
        folder_path (str): The path of the folder to create.

    Returns:
        None
    """
    exist = os.path.exists(folder_path)
    if not exist:
        os.makedirs(folder_path)
        print(f"{folder_path} created")

def clip_wrapper(chunk, overlay):
    """
    Clips a GeoDataFrame to the spatial extent of another GeoDataFrame.

    Args:
        chunk (GeoDataFrame): The GeoDataFrame to be clipped.
        overlay (GeoDataFrame): The GeoDataFrame used as the clipping boundary.

    Returns:
        GeoDataFrame: The clipped GeoDataFrame.
    """
    return gpd.clip(chunk, overlay)

def dissolving(input_path, output_path, layer):
    """
    Dissolves geometries within a GeoDataFrame based on shared attributes.

    Args:
        input_path (str): The path to the input vector file.
        output_path (str): The path to save the dissolved output file.
        layer (str): The layer name to read from the input file.

    Returns:
        None: The function saves the dissolved GeoDataFrame to a file.
    """
    data = gpd.read_file(input_path, layer=layer)

    dissolved_data = data.dissolve()

    dissolved_data.to_file(output_path, layer=layer, driver="GPKG")
    
def clip_data(edges_path, data_path, output_path, nbre_cpu, layer):
    # nbre_cpu_max = os.cpu_count()
    print(datetime.now(), f"Number of CPU cores in use: {nbre_cpu}")
    """
    Clips spatial data using a multiprocessing approach to improve performance.

    Args:
        edges_path (str): Path to the vector file containing the clipping boundaries.
        data_path (str): Path to the vector file containing the data to be clipped.
        output_path (str): Path where the clipped data will be saved.
        nbre_cpu (int): Number of CPU cores to use for parallel processing.
        layer (str): The layer name for the output file.

    Returns:
        None: The function processes and saves the clipped data to a GeoPackage file.
    """
    edges = gpd.read_file(edges_path)
    data = gpd.read_file(data_path)

    data = data.to_crs(3946)  # Convert data to coordinate reference system EPSG:3946

    data_chunks = np.array_split(data, nbre_cpu)
    print("Start clipping")

    with mp.Pool(processes=nbre_cpu) as pool:
        clipped_chunks = pool.starmap(clip_wrapper, [(chunk, edges) for chunk in data_chunks])

    print("Start concatenation")
    clipped_data = pd.concat(clipped_chunks)

    print("Saving file")
    clipped_data.to_file(output_path, driver="GPKG", layer=layer)

def classification(input_path, output_folder, fn, data_name):
    """
    Separates a GeoPackage file into multiple GeoPackage files based on a classification function.

    Args:
        input_path (str): Path to the input GeoPackage file.
        output_folder (str): Directory where the classified GeoPackage files will be saved.
        fn (function): A function that assigns a class to each row of the dataset.
        data_name (str): Base name for the output files.

    Returns:
        None: The function processes and saves classified subsets as separate GeoPackage files.
    """
    data = gpd.read_file(input_path)
    data["class"] = data.apply(fn, axis=1)  # Apply classification function to each row

    classes = data["class"].unique().tolist()
    for clas in classes:
        class_gpd = data[data["class"] == clas]
        class_gpd.to_file(
            f"{output_folder}{data_name}_{clas}.gpkg", 
            driver="GPKG", 
            layer=f"{data_name}_{clas}"
        )

def bufferize(input_path, output_path, layer, buffer_size):
    """
    Applies a buffer to the geometries in a GeoPackage layer and saves the result.

    Args:
        input_path (str): Path to the input GeoPackage file.
        output_path (str): Path where the buffered data will be saved.
        layer (str): The layer name to read from the input file.
        buffer_size (float): The buffer distance to apply to the geometries.

    Returns:
        None: The function processes and saves the buffered geometries to a GeoPackage file.
    """
    layer_gpd = gpd.read_file(input_path, layer=layer)

    layer_gpd = layer_gpd.to_crs(3946)  # Convert to CRS EPSG:3946 for accurate buffering

    buffered_features = layer_gpd.geometry.apply(lambda x: x.buffer(buffer_size))

    layer_buffer = gpd.GeoDataFrame(layer_gpd.drop("geometry", axis=1), geometry=buffered_features)
    layer_buffer.crs = layer_gpd.crs  # Maintain the correct CRS

    layer_buffer.to_file(output_path, driver="GPKG", layer=layer)

def bufferize_with_column(input_path, output_path, layer, buffer_size_column, default_value, coeff_buffer=1):
    """
    Applies a variable buffer to geometries in a GeoPackage layer based on a specified column.

    Args:
        input_path (str): Path to the input GeoPackage file.
        output_path (str): Path where the buffered data will be saved.
        layer (str): The layer name to read from the input file.
        buffer_size_column (str): Name of the column containing buffer sizes for each feature.
        default_value (float): Default buffer size to use if a value is missing in the column.
        coeff_buffer (float, optional): Coefficient to multiply the buffer size (default is 1).

    Returns:
        None: The function processes and saves the buffered geometries to a GeoPackage file.
    """
    layer_gpd = gpd.read_file(input_path, layer=layer)
    layer_gpd = layer_gpd.to_crs(3946)  # Convert CRS for accurate buffering

    # Fill missing values in the buffer column with the default value
    layer_gpd[buffer_size_column] = layer_gpd[buffer_size_column].fillna(default_value)

    
    def buffer_with_size(row):
        """
        Applies a buffer to a geometry based on a row's buffer size value.

        Args:
            row (Series): A row from the GeoDataFrame.

        Returns:
            Geometry: The buffered geometry.
        """
        buffer_size = row[buffer_size_column] * coeff_buffer
        return row.geometry.buffer(buffer_size)

    # Apply buffer function to each row
    buffered_features = layer_gpd.apply(buffer_with_size, axis=1)

    # Create a new GeoDataFrame with buffered geometries
    layer_buffer = gpd.GeoDataFrame(layer_gpd.drop("geometry", axis=1), geometry=buffered_features)
    layer_buffer.crs = layer_gpd.crs  # Maintain the correct CRS

    # Save the buffered geometries to a new GeoPackage file
    layer_buffer.to_file(output_path, driver="GPKG", layer=layer)

def explode_polygon(data_path, output_path):
    """
    Splits MultiPolygon geometries into individual Polygon features 
    and saves the result to a new GeoPackage file.

    Args:
        data_path (str): Path to the input vector file containing polygons.
        output_path (str): Path where the exploded polygons will be saved.

    Returns:
        None: The function processes and saves the individual polygons to a file.
    """
    data = gpd.read_file(data_path)

    # Explode MultiPolygons into individual Polygons
    polygons = data.explode(index_parts=False)  # Avoids creating multi-index

    # Convert CRS to EPSG:3946
    polygons = polygons.to_crs(3946)

    # Save the resulting polygons to a new file
    polygons.to_file(output_path, driver="GPKG")

def area_prop(x):
    """
    Computes the proportion of non-class-1 areas in a dataset and extracts relevant attributes.

    Args:
        x (DataFrame): A pandas DataFrame containing at least the columns "area" and "class".
                       Optionally, it may contain the column "indiccanop".

    Returns:
        Series: A pandas Series with the following computed values:
            - "prop" (float): Proportion of the area where class != 1.
            - "area" (float): Total area sum.
            - "class" (int/str): First non-1 class found, otherwise "low".
            - "canop" (float/int/None): First valid float value from "indiccanop", if available.
    """
    tot_area = x["area"].sum()  # Compute total area
    class_area = x[x["class"] != 1]["area"].sum()  # Compute area where class is not 1

    x_class = x["class"].unique().tolist()
    x_canop = None
    canop = None

    # Extract unique values from 'indiccanop' if available
    if "indiccanop" in x.columns:
        x_canop = x["indiccanop"].unique().tolist()
        canop = next((val for val in x_canop if isinstance(val, float)), 0)

    # Find the first non-1 class, otherwise default to "low"
    first_non_one = next((val for val in x_class if val != 1), "low")

    return pd.Series({
        "prop": round(class_area / tot_area, 2),
        "area": tot_area,
        "class": first_non_one,
        "canop": canop
    })

def calculate_area_proportion(edges_path, data_path, name, output_path, layer="sample_network", parcs=False):
    """
    Computes the proportion of a specific area type (from 'data_path') within network edges (from 'edges_path').

    Args:
        edges_path (str): Path to the GeoPackage file containing the network edges.
        data_path (str): Path to the GeoPackage file containing the spatial data to compare.
        name (str): Name prefix for the proportion column in the output file.
        output_path (str): Path where the processed data will be saved.
        layer (str, optional): The layer name to read from the network file (default is "sample_network").
        parcs (bool, optional): If True, additional attributes ('parcs_class' and 'canop') will be saved.

    Returns:
        None: The function processes and saves the computed area proportions to a GeoPackage file.
    """
    # Load edges and data layers
    edges = gpd.read_file(edges_path, layer=layer)
    data = gpd.read_file(data_path)

    print(f"Loaded edges columns: {edges.columns}")  # Debugging output

    # Reduce floating-point precision errors by rounding geometries
    edges.geometry = edges.geometry.apply(lambda geom: loads(dumps(geom, rounding_precision=3)))
    data.geometry = data.geometry.apply(lambda geom: loads(dumps(geom, rounding_precision=3)))

    # Perform spatial overlay to find intersections between edges and data
    overlay_edges = gpd.overlay(edges, data, how="identity", keep_geom_type=True)

    print("Overlay operation completed")

    # Compute area of intersected geometries
    overlay_edges["area"] = overlay_edges.geometry.area

    # Ensure edge index columns are of integer type
    overlay_edges[["u", "v", "key"]] = overlay_edges[["u", "v", "key"]].astype(int)

    # Set index for grouping
    overlay_edges = overlay_edges.set_index(["u", "v", "key"])

    # Fill missing class values with 1
    overlay_edges["class"] = overlay_edges["class"].fillna(1)

    print("Calculating area proportions...")

    # Group by edges and apply area proportion function
    grouped = overlay_edges.groupby(["u", "v", "key"], group_keys=True).apply(area_prop)

    # Ensure edges have the same index for merging results
    edges = edges.set_index(["u", "v", "key"])

    # Store computed proportions in the edges dataset
    edges[f"{name}_prop"] = grouped["prop"]

    # If 'parcs' option is enabled, store additional attributes
    if parcs:
        edges["parcs_class"] = grouped["class"]
        edges["canop"] = grouped["canop"]

    print("Saving processed data to file...")

    # Save the updated edges data to a GeoPackage file
    edges.to_file(output_path, driver="GPKG", layer=layer)

    print("File saved successfully!")


def calculate_weighted_average(edges_path, data_path, output_path, layer, name, fn):
    """Calculate mean average of a variable for each edges"""
    edges = gpd.read_file(edges_path, layer=layer)
    data = gpd.read_file(data_path)

    edges.geometry = [loads(dumps(geom, rounding_precision=3)) for geom in edges.geometry]
    data.geometry =  [loads(dumps(geom, rounding_precision=3)) for geom in data.geometry]

    overlay_edges = gpd.overlay(edges, data, how="identity", keep_geom_type=True)

    overlay_serie = gpd.GeoSeries(overlay_edges["geometry"])

    overlay_edges["area"] = overlay_serie.area

    overlay_edges[["u", "v", "key"]] = overlay_edges[["u", "v", "key"]].astype(int)

    overlay_edges = overlay_edges.set_index(["u", "v", "key"])

    grouped = overlay_edges.groupby(["u", "v", "key"], group_keys=True).apply(fn)

    edges = edges.set_index(["u", "v", "key"])

    edges[f"{name}_wavg"] = grouped[f"{name}_wavg"]

    edges.to_file(output_path, driver="GPKG", layer=layer)

def calculate_many_prop(data_folder_path, edges_path, layer):
    """
    Computes area proportions for multiple GeoPackage files in a folder 
    and updates a network edges file.

    Args:
        data_folder_path (str): Path to the folder containing multiple GeoPackage files.
        edges_path (str): Path to the GeoPackage file containing the network edges.
        layer (str): The layer name to read from the network file.

    Returns:
        None: The function processes and updates the edges file with area proportions.
    """
    for filename in os.listdir(data_folder_path):
        file_path = os.path.join(data_folder_path, filename)

        # Ensure the file is a GeoPackage before proceeding
        if filename.endswith(".gpkg"):
            # Extract data name from file path
            data_name = os.path.splitext(filename)[0]

            print(f"Processing: {file_path} -> {data_name}")

            # Compute area proportion and update edges file
            calculate_area_proportion(edges_path, file_path, data_name, edges_path, layer)

    print("All GeoPackage files processed successfully.")




def bruit_pre(edges_buffer_path, bruit_path, edges_buffer_bruit_wavg_path, layer, name):
    """
    Computes the maximum noise (DN) value for each road segment based on spatial noise data.

    Args:
        edges_buffer_path (str): Path to the GeoPackage file containing road segments with buffers.
        bruit_path (str): Path to the GeoPackage file containing noise data.
        edges_buffer_bruit_wavg_path (str): Path to save the processed GeoPackage file.
        layer (str): The name of the layer in the GeoPackage file.
        name (str): The column name in the noise dataset representing the DN (noise level).

    Returns:
        None: The function processes the data and saves the results in a GeoPackage file.
    """
    try:
        print("Loading files...")
        # Load GeoPackage files
        edges = gpd.read_file(edges_buffer_path)
        data = gpd.read_file(bruit_path)

        # Check if columns and layers exist
        print(f"Columns in 'edges': {edges.columns}")
        print(f"Columns in 'data' (noise): {data.columns}")

        # Clean invalid geometries in both DataFrames
        print("Cleaning invalid geometries...")
        edges["geometry"] = edges["geometry"].apply(make_valid)
        data["geometry"] = data["geometry"].apply(make_valid)

        # Compute the maximum DN value for each road segment
        print("Calculating the maximum DN value for each road segment...")
        
        def get_max_dn_for_edge(edge_geometry):
            """
            Finds the maximum DN value for a given road segment by checking intersecting noise polygons.

            Args:
                edge_geometry (Geometry): The geometry of the road segment.

            Returns:
                float: The maximum DN value among intersecting noise polygons, or None if no intersection.
            """
            intersecting_data = data[data.geometry.intersects(edge_geometry)]
            return intersecting_data[name].max() if not intersecting_data.empty else None

        # Apply the function to each road segment
        edges[name] = edges.geometry.apply(get_max_dn_for_edge)

        # Check that the new column has been added correctly
        print(f"Sample rows with the new '{name}' column:\n{edges.head()}")

        # Drop rows where DN is NaN (if no intersection found)
        print(f"Removing NaN values in the '{name}' column...")
        edges = edges.dropna(subset=[name])
        print(f"Number of rows after NaN removal: {len(edges)}")

        # Normalize DN values using MinMaxScaler (if needed)
        print("Scaling DN values using MinMaxScaler...")
        scaler = MinMaxScaler(feature_range=(0, 1))
        edges["DN_scaled"] = scaler.fit_transform(edges[[name]])
        print("Scaling completed.")

        # Save the processed data to the output file
        print(f"Saving the processed file to {edges_buffer_bruit_wavg_path}...")
        edges.to_file(edges_buffer_bruit_wavg_path, driver="GPKG", layer=layer)
        print(f"Processed file successfully saved to {edges_buffer_bruit_wavg_path}")

    except Exception as e:
        print(f"Error processing noise data: {e}")




def calculate_presency(edges_path, data_path, output_path, layer, name, fn):
    """
    Detects the presence of a specific spatial layer for each edge in a network.

    Args:
        edges_path (str): Path to the GeoPackage file containing the network edges.
        data_path (str): Path to the GeoPackage file containing the spatial data to check.
        output_path (str): Path to save the updated GeoPackage file.
        layer (str): The layer name to read from the network file.
        name (str): The column name to store the presence result.
        fn (function): A function to apply to the grouped data to determine presence.

    Returns:
        None: The function processes the data and saves the results to a GeoPackage file.
    """
    print("Loading files...")
    edges = gpd.read_file(edges_path, layer=layer)
    data = gpd.read_file(data_path)

    print("Cleaning geometries to avoid floating-point precision errors...")
    edges.geometry = edges.geometry.apply(lambda geom: loads(dumps(geom, rounding_precision=3)))
    data.geometry = data.geometry.apply(lambda geom: loads(dumps(geom, rounding_precision=3)))

    print("Performing spatial overlay to detect layer presence...")
    overlay_edges = gpd.overlay(edges, data, how="identity", keep_geom_type=True)

    print("Converting edge IDs to integer type...")
    overlay_edges[["u", "v", "key"]] = overlay_edges[["u", "v", "key"]].astype(int)

    print("Setting index for proper grouping...")
    overlay_edges = overlay_edges.set_index(["u", "v", "key"])

    print("Filling missing class values with default 1...")
    overlay_edges["class"] = overlay_edges["class"].fillna(1)

    print("Applying the presence detection function...")
    grouped = overlay_edges.groupby(["u", "v", "key"], group_keys=True).apply(fn)

    print("Updating edges with calculated presence values...")
    edges = edges.set_index(["u", "v", "key"])
    edges[name] = grouped["class"]

    print(f"Saving updated file to {output_path}...")
    edges.to_file(output_path, driver="GPKG", layer=layer)

    print("Processing completed successfully!")


def create_csv_dataset(edges_path, output_path, layer):
    """
    Creates a CSV dataset from a GeoPackage file by removing unnecessary spatial and road attributes.

    Args:
        edges_path (str): Path to the GeoPackage file containing the network edges.
        output_path (str): Path to save the resulting CSV file.
        layer (str): The layer name to read from the GeoPackage file.

    Returns:
        None: The function processes the data and saves the CSV file.
    """
    try:
        print("Loading edges data...")
        edges = gpd.read_file(edges_path, layer=layer)

        # List of columns to drop
        columns_to_drop = [
            "geometry", "highway", "oneway", "reversed", "from", "to", "name", "maxspeed",
            "lanes", "width", "service", "bridge", "ref", "junction", "tunnel", "est_width", "access"
        ]

        # Drop only existing columns to prevent errors
        columns_to_drop = [col for col in columns_to_drop if col in edges.columns]
        
        print(f"Dropping columns: {columns_to_drop}")
        edges = edges.drop(columns=columns_to_drop, axis=1)

        print(f"Saving dataset to {output_path}...")
        edges.to_csv(output_path, index=False)

        print("CSV dataset created successfully!")

    except Exception as e:
        print(f"Error creating CSV dataset: {e}")



def cut_empreinte(bruit_path, empreinte_path, sortie_path):
    """
    Extracts only the area of interest (Métropole de Lyon) from the noise dataset 
    by clipping it with the provided footprint layer.

    Args:
        bruit_path (str): Path to the GeoPackage file containing the noise dataset.
        empreinte_path (str): Path to the GeoPackage file containing the footprint of the desired area.
        sortie_path (str): Path where the clipped dataset will be saved.

    Returns:
        None: The function processes and saves the clipped data.
    """
    try:
        print("Loading spatial datasets...")
        bruit = gpd.read_file(bruit_path)
        empreinte = gpd.read_file(empreinte_path)
    except Exception as e:
        print(f"Error loading spatial datasets: {e}")
        return

    print("Cleaning geometries: converting MultiPolygons to Polygons where needed...")
    bruit["geometry"] = bruit["geometry"].apply(
        lambda x: x if isinstance(x, Polygon) else x.geoms[0] if isinstance(x, MultiPolygon) else None
    )
    empreinte["geometry"] = empreinte["geometry"].apply(
        lambda x: x if isinstance(x, Polygon) else x.geoms[0] if isinstance(x, MultiPolygon) else None
    )

    # Ensure both datasets have the same CRS
    if bruit.crs != empreinte.crs:
        print(f"Reprojecting empreinte to match the CRS of bruit ({bruit.crs})...")
        empreinte = empreinte.to_crs(bruit.crs)

    # Perform spatial intersection
    print("Performing spatial intersection to extract the area of interest...")
    try:
        decoupe = gpd.overlay(bruit, empreinte, how="intersection")
    except Exception as e:
        print(f"Error during spatial overlay operation: {e}")
        return

    # Save the clipped dataset
    try:
        decoupe.to_file(sortie_path, driver="GPKG")
        print(f"Clipped dataset saved at: {sortie_path}")
    except Exception as e:
        print(f"Error saving the clipped dataset: {e}")
        return

    # Delete the original noise dataset if it exists
    if os.path.exists(bruit_path):
        try:
            os.remove(bruit_path)
            print(f"Original file {bruit_path} successfully deleted.")
        except Exception as e:
            print(f"Error deleting original file {bruit_path}: {e}")
    else:
        print(f"File {bruit_path} does not exist, skipping deletion.")

    # Rename the clipped dataset to replace the original file
    if os.path.exists(sortie_path):
        try:
            os.rename(sortie_path, bruit_path)
            print(f"File renamed to {bruit_path}.")
        except Exception as e:
            print(f"Error renaming file {sortie_path} to {bruit_path}: {e}")
    else:
        print(f"File {sortie_path} does not exist, skipping renaming.")




def check_data_integrity(edges_path, bruit_path):
    """
    Checks the integrity of spatial datasets before processing.

    Args:
        edges_path (str): Path to the GeoPackage file containing the road network.
        bruit_path (str): Path to the GeoPackage file containing noise data.

    Returns:
        None: Prints out various data integrity checks.
    """
    try:
        print("Loading datasets...")
        edges = gpd.read_file(edges_path)
        bruit = gpd.read_file(bruit_path)

        print("Checking for duplicate geometries...")
        edges_duplicates = edges.duplicated(subset="geometry").sum()
        bruit_duplicates = bruit.duplicated(subset="geometry").sum()
        print(f"Duplicate geometries in 'edges': {edges_duplicates}")
        print(f"Duplicate geometries in 'bruit': {bruit_duplicates}")

        # Remove duplicate geometries in 'edges', keeping the first occurrence
        if edges_duplicates > 0:
            print("Removing duplicate geometries in 'edges'...")
            edges = edges.drop_duplicates(subset="geometry")

        print("Checking for missing values in noise data (DN column)...")
        if "DN" in bruit.columns:
            bruit_nan = bruit["DN"].isna().sum()
            print(f"Missing values in 'DN' column of 'bruit': {bruit_nan}")
        else:
            print("Warning: 'DN' column not found in 'bruit' dataset!")

        print("Checking for duplicate edge IDs (['u', 'v', 'key'])...")
        if all(col in edges.columns for col in ["u", "v", "key"]):
            edges_id_duplicates = edges.duplicated(subset=["u", "v", "key"]).sum()
            print(f"Duplicate edge IDs in 'edges': {edges_id_duplicates}")
        else:
            print("Warning: One or more index columns ['u', 'v', 'key'] are missing in 'edges'!")

        print("Checking for full duplicate rows in datasets...")
        edges_full_duplicates = edges.duplicated().sum()
        bruit_full_duplicates = bruit.duplicated().sum()
        print(f"Fully duplicate rows in 'edges': {edges_full_duplicates}")
        print(f"Fully duplicate rows in 'bruit': {bruit_full_duplicates}")

        print("Data integrity check completed.")

    except Exception as e:
        print(f"Error during data integrity check: {e}")