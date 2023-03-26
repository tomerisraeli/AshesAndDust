import rioxarray
import geopandas
import matplotlib.pyplot as plt

tile_list_shp = ['/Users/nuriel/PycharmProjects/AshesAndDust/AshesAndDust/dis_water/data/h20v05.shp',
                 '/Users/nuriel/PycharmProjects/AshesAndDust/AshesAndDust/dis_water/data/h21v05.shp',
                 '/Users/nuriel/PycharmProjects/AshesAndDust/AshesAndDust/dis_water/data/h21v06.shp']

geotif_of_tile = ['/Users/nuriel/PycharmProjects/AshesAndDust/AshesAndDust/dis_water/data/h20v05.tif',
                  '/Users/nuriel/PycharmProjects/AshesAndDust/AshesAndDust/dis_water/data/h21v05.tif',
                  '/Users/nuriel/PycharmProjects/AshesAndDust/AshesAndDust/dis_water/data/h21v06.tif']
# geotif_road_all_of_israel
geotif_land_use = ["/Users/nuriel/PycharmProjects/AshesAndDust/AshesAndDust/dis_water/data/dist_massive_water.tif"
    ,"/Users/nuriel/PycharmProjects/AshesAndDust/AshesAndDust/dis_water/data/dist_to_water.tif"]

for tile, tile_grid in zip(tile_list_shp, geotif_of_tile):
    geodf = geopandas.read_file(tile)
    to_match = rioxarray.open_rasterio(tile_grid)
    for land in geotif_land_use:
        xds1 = rioxarray.open_rasterio(land)  # land use
        # we clip the raster of the land use
        clipped = xds1.rio.clip(geodf.geometry.values, geodf.crs, drop=False, invert=False)  # clip the raster
        xds_repr_match = clipped.rio.reproject_match(to_match)
        data_reprojected = xds_repr_match.rio.reproject("EPSG:2039")
        plt.imshow(data_reprojected.squeeze())
        plt.show()
        plt.clf()
