from DataBase.DataBaseDataTypes.data_base_data_batch import DBBatch
from DataBase.DataBaseDataTypes.data_base_range import DBRange
from DataParsers.parser import Parser

import rasterio
import rasterio.plot

from DataParsers.praser_exceptions.wrong_crs_parser_exception import CrsError
from support.configuration_values import ConfigurationValues
from tqdm import tqdm


class TifParser(Parser):
    """
    a general .tif parser
    """

    LAT_LON_CRS = rasterio.CRS().from_string("WGS84")

    def __init__(self, config: ConfigurationValues, path, var, band=1):
        """
        initialize a new .tif parser

        :param config: the config values
        :param path: the path of the tif file
        :param var: the db var relevant to the raster
        :param band: the band in which the data is saved on at the raster
        """

        super().__init__(config)
        self.__path = path
        self.__var = var
        self.__band = band

    def parse(self, data_range: DBRange) -> DBBatch:
        with rasterio.open(self.__path) as raster:
            # validate file crs
            if not raster.crs == TifParser.LAT_LON_CRS:
                raise CrsError(f"the given .tif file is at the wrong crs ({raster.crs}) "
                               f"it should be {TifParser.LAT_LON_CRS}")

            result = DBBatch(self.__var, data_range)

            self.__populate_batch(raster, result)
            return result

    def __populate_batch(self, raster, batch):
        """
        insert the data to the batch
        :param raster:
        :return:
        """

        lat_res = (raster.bounds.top - raster.bounds.bottom) / raster.shape[0]
        lon_res = (raster.bounds.right - raster.bounds.left) / raster.shape[1]

        data = raster.read(self.__band)

        for lon_index in range(raster.shape[0]):
            for lat_index in range(raster.shape[1]):
                batch.insert(time=0,
                             lat=raster.bounds.bottom + lat_index * lat_res,
                             lon=raster.bounds.left + lon_index * lon_res,
                             value=data[lon_index, lat_index])
