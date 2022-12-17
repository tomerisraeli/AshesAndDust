import numpy as np

from DataBase.DataBaseDataTypes.data_base_coordinate import DataBaseCoordinate
from DataBase.DataBaseDataTypes.data_base_data_range import DataRange
from DataBase.DataBaseDataTypes.data_base_variable import DataBaseVariable


class DataBatch:
    """
    hold a batch of data to write the db ot data that were read from the db
    """

    def __init__(self):
        """
        create a new data batch
        """
        self.__data = []

    def insert(self, coordinate: DataBaseCoordinate, values):
        """
        insert new data to the batch. the last value added to each coordinate is the one used
        :param coordinate: the coordinate of the data
        :param values: a dict where the keys are DataBaseVariable and the values are at the DataBaseVariable matching
            type
        :return: None
        """
        self.__data.append((coordinate, values))

    @property
    def data(self):
        return self.__data
