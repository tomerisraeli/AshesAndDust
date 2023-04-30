import numpy as np
import rasterio
from shapely.geometry import Point, LineString
import networkx as nx
import geopandas as gpd
import osmnx as ox
import fiona



def convert_projection(file_path: str, new_epsg: int) -> str:
    """
    Converts a TIFF file to a new EPSG projection and replaces the original file with the updated file.

    Args:
        file_path (str): The path to the input TIFF file.
        new_epsg (int): The new EPSG code to reproject the file to.

    Returns:
        str: The path to the updated file.

    Raises:
        FileNotFoundError: If the input file does not exist.
    """
    # Check if the input file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"{file_path} does not exist.")

    # Open the input file and get its metadata
    with rasterio.open(file_path) as src:
        # Calculate the transformation parameters for the new projection
        transform, width, height = calculate_default_transform(
            src.crs, new_epsg, src.width, src.height, *src.bounds)

        # Update the metadata with the new projection information
        kwargs = src.meta.copy()
        kwargs.update({
            "crs": new_epsg,
            "transform": transform,
            "width": width,
            "height": height,
        })

        # Create the updated file and reproject the data
        updated_file_path = f"updated_{file_path}"
        with rasterio.open(updated_file_path, "w", **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=new_epsg,
                    resampling=Resampling.bilinear
                )

        # Remove the original file and rename the updated file
        os.remove(file_path)
        os.rename(updated_file_path, file_path)

        # Open the updated file and display the image
        with rasterio.open(file_path) as src:
            plt.imshow(src.read(1))
            plt.show()

        # Return the path to the updated file
        return file_path


def get_nearest_road_shapefile(point, shapefile_path):
    """
    Get the nearest road to a given point from a shapefile.

    Args:
        point (shapely.geometry.Point): The point to find the nearest road to.
        shapefile_path (str): The path to the shapefile containing the roads.

    Returns:
        shapely.geometry.LineString: The nearest road as a LineString object.
    """
    # Load the shapefile as a GeoDataFrame
    roads = gpd.read_file(shapefile_path)

    # Convert the point to the same CRS as the roads
    point = point.to_crs(roads.crs)

    # Find the nearest road to the point
    nearest = nearest_points(point, roads.unary_union)[1]
    nearest_road = roads.distance(nearest).idxmin()

    # Return the nearest road as a LineString object
    return roads.loc[nearest_road, "geometry"]


def get_nearest_road(point: Point, network: nx.MultiDiGraph) -> LineString:
    """
    Returns the LineString of the nearest road to the given Point.

    Args:
        point (Point): The Point for which to find the nearest road.
        network (nx.MultiDiGraph): The road network graph.

    Returns:
        LineString: The LineString of the nearest road.
    """
    # Find the nearest node on the road network graph
    nearest_node = ox.get_nearest_node(network, (point.y, point.x))

    # Find the edges connected to the nearest node and their lengths
    edges = list(network.edges(nearest_node, keys=True))
    edge_lengths = [network[u][v][k]["length"] for u, v, k in edges]

    # Find the index of the shortest edge and return its geometry
    shortest_edge_idx = np.argmin(edge_lengths)
    shortest_edge = edges[shortest_edge_idx]
    return network[shortest_edge[0]][shortest_edge[1]][shortest_edge[2]]["geometry"]

def load_network(filename: str, crs: str) -> nx.MultiDiGraph:
    """Load a road network from a shapefile using NetworkX"""
    G = nx.MultiDiGraph()
    with fiona.open(filename, "r") as shapefile:
        for feature in shapefile:
            geometry = feature["geometry"]
            properties = feature["properties"]
            road_type = properties.get("type", "unknown")
            if geometry["type"] == "LineString":
                line = shape(geometry)
                G.add_edge(line.coords[0], line.coords[-1], key=properties["id"], geometry=line, type=road_type)
            elif geometry["type"] == "MultiLineString":
                for sub_line in geometry["coordinates"]:
                    line = shape({"type": "LineString", "coordinates": sub_line})
                    G.add_edge(line.coords[0], line.coords[-1], key=properties["id"], geometry=line, type=road_type)
    nx.set_edge_attributes(G, crs, name="crs")
    return G

def main():
    # Convert the projection of the input TIFF file
    tiff_path = "input.tif"
    converted_path = convert_projection(tiff_path, 2039)

    # Read the converted TIFF file
    with rasterio.open(converted_path) as src:
        # Get the affine transformation matrix
        transform = src.transform

        # Convert each pixel to a Point and find the nearest road
        for i in range(src.height):
            for j in range(src.width):
                # Get the pixel value
                value = src.read(1, window=((i, i+1), (j, j+1)))[0][0]

                # Convert the pixel to a Point
                x, y = rasterio.transform.xy(transform, i, j)
                point = Point(x, y)

                # Check if the pixel value is non-zero
                if value > 0:
                    # Find the nearest road and calculate the distance
                    road = get_nearest_road(point, network)
                    distance = point.distance(road)

                    # Print the point and its distance from the road
                    print(f"Point ({x:.4f}, {y:.4f}): {distance:.4f} meters from nearest road.")

def get_nearest_road(point: Point, network: nx.MultiDiGraph) -> LineString:
    """
    Returns the LineString of the nearest road to the given Point.

    Args:
        point (Point): The Point for which to find the nearest road.
        network (nx.MultiDiGraph): The road network graph.

    Returns:
        LineString: The LineString of the nearest road.
    """
    # Find the nearest node on the road network graph
    nearest_node = ox.get_nearest_node(network, (point.y, point.x))

    # Find the edges connected to the nearest node and their lengths
    edges = list(network.edges(nearest_node, keys=True))
    edge_lengths = [network[u][v][k]["length"] for u, v, k in edges]

    # Find the index of the shortest edge and return its geometry
    shortest_edge_idx = np.argmin(edge_lengths)
    shortest_edge = edges[shortest_edge_idx]
    return network[shortest_edge[0]][shortest_edge[1]][shortest_edge[2]]["geometry"]


def main():
    # Convert the projection of the input TIFF file
    tiff_path = "input.tif"
    converted_path = convert_projection(tiff_path, 2039)

    # Read the converted TIFF file
    with rasterio.open(converted_path) as src:
        # Get the affine transformation matrix
        transform = src.transform

        # Convert each pixel to a Point and find the nearest road
        for i in range(src.height):
            for j in range(src.width):
                # Convert the pixel to a Point
                x, y = rasterio.transform.xy(transform, i, j)
                point = Point(x, y)

                # Check if the pixel value is non-zero
                if value > 0:
                    # Find the nearest road and calculate the distance
                    road = get_nearest_road(point, network)
                    distance = point.distance(road)

                    # Print the point and its distance from the road
                    print(f"Point ({x:.4f}, {y:.4f}): {distance:.4f} meters from nearest road.")

# Define the main function
def main():
    # Load the raster data
    with rasterio.open("h20v05.tif") as src:
        crs = src.crs
        data = src.read(1)
        transform = src.transform

    # Load the road network
    network = load_network("h20v05_crs2039.shp", crs)

    # Open the plot
    fig, ax = plt.subplots(figsize=(12, 12))

    # Plot the raster data
    ax.imshow(data, cmap="gray", extent=rasterio.plot.plotting_extent(src))

    # Loop over each point clicked on the plot
    for point in get_points(ax):
        # Get the nearest road
        nearest_road = get_nearest_road(point, network)

        # Calculate the distance to the nearest road
        distance = point.distance(nearest_road)

        # Plot the point and the nearest road
        ax.plot(point.x, point.y, marker="o", color="red")
        ax.plot(*nearest_road.xy, color="blue")

        # Print the distance to the nearest road
        print(f"Distance to nearest road: {distance:.2f} meters")

    # Show the plot
    plt.show()



if __name__ == "__main__":
    main()