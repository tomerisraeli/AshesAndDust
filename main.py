import logging

import rasterio
from matplotlib import pyplot as plt

from DataBase.DBConstants import DBConstants
from DataBase.DataBaseDataTypes.data_base_variable import DBVariable
from DataBase.data_base import DataBase
from DataParsers.distance_to_water_parser import DistanceToWaterParser
from support import loggers
from support.configuration_values import ConfigurationValues


class AshesAndDust:
    """
    the main class of the project.
    the user interfaces should use it to call the different features of the program
    """

    # the path to the __config file
    __Config_File_Path = "configuration.ini"

    def __init__(self):
        self.__config = ConfigurationValues(AshesAndDust.__Config_File_Path)
        self.__db = DataBase(self.__config)

    def update_data_base(self):
        """
        call all the parsers and insert the data to the db
        :return:
        """

        parsers = [
            # ElevationParser(config=self.__config),
            DistanceToWaterParser(config=self.__config)
        ]

        for parser in parsers:
            loggers.root_logger.info(f"parsing using {parser.__module__}")
            parsed_data = parser.parse(self.__db.range)
            loggers.root_logger.info("parsed data successfully")
            loggers.root_logger.debug("inserting data to db")
            self.__db.insert(parsed_data)
            loggers.root_logger.info("data inserted to db successfully")

    def get_spatial_data(self, var: DBVariable):
        rng = self.__db.range
        loggers.root_logger.info(f"fetching {var.name} from db for range: {rng}")
        return self.__db.load(rng, var)

    def get_approximation(self, date, output_path):
        """
        get the data approximation using the data fetched and the model
        the output should be saved as raster in the given path
        :return: None
        """
        pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING,
                        format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s")

    app = AshesAndDust()
    app.update_data_base()
    data = app.get_spatial_data(DBConstants.VAR_DTWB)
    plt.imshow(data.data[0])
    plt.show()