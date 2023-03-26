import logging

from matplotlib import pyplot as plt

from DataBase.DBConstants import DBConstants
from DataBase.DataBaseDataTypes.data_base_variable import DBVariable
from DataBase.data_base import DataBase
from DataParsers.distance_to_water_parser import DistanceToWaterParser
from DataParsers.elavation_parser import ElevationParser
from support import loggers
from support.configuration_values import ConfigurationValues


class AshesAndDust:
    """
    the main class of the project.
    the user interfaces should use it to call the different features of the program
    """

    # the path to the __config file

    def __init__(self, config="configuration.ini"):
        self.__config = ConfigurationValues(config)
        self.__db = DataBase(self.__config)

    def update_data_base(self):
        """
        call all the parsers and insert the data to the db
        :return:
        """

        parsers = [
            ElevationParser(config=self.__config),
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
    logging.basicConfig(level=logging.INFO,
                        format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s")

    app = AshesAndDust()
    # app.update_data_base()

    f, axarr = plt.subplots(1, 2, sharex="all", sharey="all")
    dist_to_water_data = app.get_spatial_data(DBConstants.VAR_DTWB)
    elevation_data = app.get_spatial_data(DBConstants.VAR_ELEV)

    axarr[0].imshow(dist_to_water_data.data[0])
    axarr[0].set_title("distance to major water bodies")
    axarr[1].imshow(elevation_data.data[0], vmax=3000, vmin=-500)
    axarr[1].set_title("elevation in meters")
    plt.show()
