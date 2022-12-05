from DataBase.data_base import DataBase
from support.configuration_values import ConfigurationValues


# TODO: add logs
class AshesAndDust:
    """
    the main class of the project.
    the user interfaces should use it to call the different features of the program
    """

    def __init__(self):
        self.__config = ConfigurationValues()
        self.__data_base = DataBase()
        self.__model = None  # the model to use

        # fetchers is a list of all the fetchers in use, every fetcher should be added to here
        self.__fetchers = []

    def update_data_base(self):
        """
        call all the fetchers to update the database.

        :return:
        """

        for fetcher in self.__fetchers:
            fetcher.fetch(self.__data_base, self.__config)

    def get_approximation(self, date, output_path):
        """
        get the data approximation using the data fetched and the model
        the output should be saved as raster in the given path
        :return: None
        """
        pass


if __name__ == '__main__':
    a = AshesAndDust()
    a.update_data_base()
    a.get_approximation(0, "")
