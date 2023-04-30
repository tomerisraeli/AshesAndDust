import os
import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import matplotlib.pyplot as plt


def convert_projection(file_path: str, new_epsg: int) -> str:
    """
    Converts a TIFF file to a new EPSG projection and replaces the original file with the updated file.

    Args:
        file_path (str): The path to the input TIFF file.
        new_epsg (int): The new EPSG code to reproject the file to.
        show_image (bool, optional): Whether to show the reprojected image. Defaults to False.

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


def main():
    convert_projection("h20v05.tif", 2039)


if __name__ == "__main__":
    main()
