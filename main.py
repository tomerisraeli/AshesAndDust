from support.configuration_values import ConfigurationValues


# TODO: add logs


class AshesAndDust:
    """
    the main class of the project.
    the user interfaces should use it to call the different features of the program
    """

    # the path to the config file
    __Config_File_Path = "configuration.ini"

    def __init__(self):
        self.__config = ConfigurationValues(AshesAndDust.__Config_File_Path)

    def update_data_base(self):
        """
        call all the parsers and insert the data to the db

        :return:
        """
        pass

    def get_approximation(self, date, output_path):
        """
        get the data approximation using the data fetched and the model
        the output should be saved as raster in the given path
        :return: None
        """
        pass

