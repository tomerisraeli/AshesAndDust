import logging

from DataBase.data_base import DataBase
from DataParsers.elavation_parser import ElevationParser
from support.configuration_values import ConfigurationValues


# TODO: add logs


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

        logging.info("parsing elevation data")
        elevation_parser = ElevationParser(config=self.__config)
        print(self.__db.range)
        elevation_data = elevation_parser.parse(self.__db.range)
        logging.info("parsed elevation data successfully")
        self.__db.insert(elevation_data)
        logging.info("elevation data inserted to db successfully")


    def get_approximation(self, date, output_path):
        """
        get the data approximation using the data fetched and the model
        the output should be saved as raster in the given path
        :return: None
        """
        pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    app = AshesAndDust()
    app.update_data_base()
