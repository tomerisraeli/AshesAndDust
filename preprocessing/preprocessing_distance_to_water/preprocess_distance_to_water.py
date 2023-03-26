import rioxarray
import geopandas
import matplotlib.pyplot as plt

from preprocessing.data_preprocess import DataPreprocess


class DistanceToWaterPreprocess(DataPreprocess):
    @staticmethod
    def fetch():
        # TODO: make sure the file exists at the main raw data directory
        pass

    @staticmethod
    def preprocess():
        # TODO: load paths from config file using support\configuration_values
        tile_list_shp = ['/Users/tomerisraeli/Library/CloudStorage/GoogleDrive-tomer.israeli.43@gmail.com/My Drive/year_2/Magdad/data/tiles/h20v05_crs2039.shp',
                         '/Users/tomerisraeli/Library/CloudStorage/GoogleDrive-tomer.israeli.43@gmail.com/My Drive/year_2/Magdad/data/tiles/h21v05_crs2039.shp',
                         '/Users/tomerisraeli/Library/CloudStorage/GoogleDrive-tomer.israeli.43@gmail.com/My Drive/year_2/Magdad/data/tiles/h21v06_crs2039.shp']

        geotif_of_tile = ['/Users/tomerisraeli/Library/CloudStorage/GoogleDrive-tomer.israeli.43@gmail.com/My Drive/year_2/Magdad/data/tiles/h20v05.tif',
                          '/Users/tomerisraeli/Library/CloudStorage/GoogleDrive-tomer.israeli.43@gmail.com/My Drive/year_2/Magdad/data/tiles/h21v05.tif',
                          '/Users/tomerisraeli/Library/CloudStorage/GoogleDrive-tomer.israeli.43@gmail.com/My Drive/year_2/Magdad/data/tiles/h21v06.tif']

        geotif_of_data = ["/Users/tomerisraeli/Library/CloudStorage/GoogleDrive-tomer.israeli.43@gmail.com/My Drive/year_2/Magdad/data/dist_to_water/dist_massive_water.tif"]

        for tile, tile_grid in zip(tile_list_shp, geotif_of_tile):
            clip = geopandas.read_file(tile)
            to_match = rioxarray.open_rasterio(tile_grid).rio.reproject("EPSG:2039")
            for data in geotif_of_data:
                data_geotif = rioxarray.open_rasterio(data)
                data_geotif = data_geotif.rio.reproject("EPSG:2039")

                # we clip the raster of the land use
                data_geotif = data_geotif.rio.clip(clip.geometry.values, clip.crs, drop=False, invert=False)  # clip the raster
                data_geotif = data_geotif.rio.reproject_match(to_match)
                # data_geotif = data_geotif.rio.reproject("EPSG:2039")
                plt.imshow(data_geotif.squeeze())
                plt.show()
                plt.clf()

        # TODO: save files as netcdf


if __name__ == '__main__':
    DistanceToWaterPreprocess.preprocess()
