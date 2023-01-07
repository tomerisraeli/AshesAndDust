import unittest

import rasterio
from matplotlib import pyplot as plt

from DataBase.DBConstants import DBConstants
from DataBase.DataBaseDataTypes.data_base_range import DBRange
from DataParsers.parsers_support.tif_parser import TifParser
from DataParsers.praser_exceptions.wrong_crs_parser_exception import CrsError
from support.configuration_values import ConfigurationValues


class TestTifParser(unittest.TestCase):
    config_path = "config.ini"

    def test_crs(self):
        """
        make sure the tif parser validates the crs of the given file
        :return:
        """

        config = ConfigurationValues(TestTifParser.config_path)
        elevation_path = config.get_key(ConfigurationValues.Keys.elevation_data_path)

        right_crs = TifParser.LAT_LON_CRS
        TifParser.LAT_LON_CRS = rasterio.CRS().from_string("EPSG:31370") # set the wrong crs format
        parser = TifParser(config, elevation_path, DBConstants.VAR_ELEV)
        self.assertRaises(CrsError, lambda: parser.parse(DBRange((0, 1, 10), (0, 1, 10), (0, 1, 10))))

        TifParser.LAT_LON_CRS = right_crs # make sure to correct the crs value

    def show_elevation(self):
        config = ConfigurationValues(TestTifParser.config_path)
        elevation_path = config.get_key(ConfigurationValues.Keys.elevation_data_path)
        parser = TifParser(config, elevation_path, DBConstants.VAR_ELEV)

        batch = parser.parse(DBRange((0, 0, 1), (27, 37, 0.01), (27, 39, 0.01)))

        plt.imshow(batch.data[0], vmin=-500, vmax=3000)
        plt.show()