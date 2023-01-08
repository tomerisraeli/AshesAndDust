import rasterio

from DataBase.DBConstants import DBConstants
from DataParsers.parsers_support.tif_parser import TifParser


from support.configuration_values import ConfigurationValues


class DistanceToWaterParser(TifParser):

    def __init__(self, config):
        super(DistanceToWaterParser, self).__init__(
            config,
            path=config.get_key(ConfigurationValues.Keys.DTWB_data_path),
            var=DBConstants.VAR_DTWB
        )
