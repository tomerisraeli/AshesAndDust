from DataBase.DBConstants import DBConstants
from DataBase.DataBaseDataTypes.data_base_data_batch import DBBatch
from DataBase.DataBaseDataTypes.data_base_range import DBRange
from DataParsers.parsers_support.tiff_raster import TifParser

import rasterio.plot

from support.configuration_values import ConfigurationValues


class ElevationParser(TifParser):

    def __init__(self, config):
        super(ElevationParser, self).__init__(
            config,
            path=config.get_key(ConfigurationValues.Keys.elevation_data_path),
            var=DBConstants.VAR_ELEV
        )

