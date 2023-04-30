import os
from typing import Tuple

import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling


def convert_projection(file_path: str, new_epsg: str) -> str:
    """
    Converts a TIFF file to a new EPSG projection and replaces the original file with the updated file.

    Args:
        file_path (str): The path to the input TIFF file.
        new_epsg (str): The new EPSG code to reproject the file to.

    Returns:
        str: The path to the updated file.

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If the new EPSG code is invalid.
    """
    # Check if the input file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"{file_path} does not exist.")
    
    # Check if the new EPSG code is valid
    try:
        int(new_epsg)
    except ValueError:
        raise ValueError("Invalid EPSG code.")

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

        # Return the path to the updated file
        return file_path
