from DataBase.data_base_coordinate import DataBaseCoordinate
from DataBase.data_base_data_batch import DataBatch
from support.configuration_values import ConfigurationValues


class DataBaseValue:
    def __init__(self):
        pass


# TODO: add logs
class DataBase:
    """
    manage the access to the database which is saved as Netcdf
    """

    def __init__(self, config: ConfigurationValues):
        """
        :param config:
        """
        # TODO: open the database at the path saved at the config file
        # TODO: create a new file if doesnt exists

        self.__time_resolution = 1  # TODO: read the time resolution from config file
        self.__spatial_resolution = 1  # TODO: read the spacial resolution from config file

    def insert(self, data: DataBatch):
        """
        insert a new data batch to database, if the data already exists it should be overwritten
        :param data: the batch of data to enter
        :return: None
        """
        # TODO: implement
        pass

    def load(self, coordinates):
        """
        load data from the database
        :param coordinates: the coordinates to load data for
        :return: batch of data with the coordinates that were found in the database and there values
        """
        # TODO: implement
        pass

    @property
    def time_resolution(self):
        return self.__time_resolution

    @property
    def spatial_resolution(self):
        return self.__spatial_resolution

    @property
    def reference_coordinate(self):
        """
        get a coordinate that exists in the database. since the coordinates in the database are saved at const
        distance and time we must get a reference coordinate to create other valid coordinates.
        :return: an arbitrary coordinate from the database
        """
        #TODO: implement
        return DataBaseCoordinate(0, 0, 0)
