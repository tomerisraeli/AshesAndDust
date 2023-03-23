import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

def convert_projection(file: str, new_epsg: str) -> str:
    """
    Converts a TIFF file to a new EPSG projection and saves the result as a new file.

    @param file: The name of the input TIFF file.
    @type file: str
    @param new_epsg: The new EPSG code to reproject the file to.
    @type new_epsg: str

    @return: The name of the new file.
    @rtype: str
    """
    # Open the input file and get its metadata
    with rasterio.open(file) as src:
        # Calculate the transformation parameters for the new projection
        transform, width, height = calculate_default_transform(
            src.crs, new_epsg, src.width, src.height, *src.bounds)
        # Update the metadata with the new projection information
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': new_epsg,
            'transform': transform,
            'width': width,
            'height': height
        })

        # Create the new file and reproject the data
        with rasterio.open(f'new_{file}.tif', 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=new_epsg,
                    resampling=Resampling.bilinear)   
            # Return the name of the new file
            return f'new_{file}.tif'