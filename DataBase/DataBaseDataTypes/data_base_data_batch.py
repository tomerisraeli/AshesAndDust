from typing import Tuple

import numpy as np

from DataBase.DataBaseDataTypes.data_base_coordinate import DataBaseCoordinate
from DataBase.DataBaseDataTypes.data_base_data_range import DataRange
from DataBase.DataBaseDataTypes.data_base_range import DBRange
from DataBase.DataBaseDataTypes.data_base_variable import DataBaseVariable


class DBBatch:
    """
    hold a batch of data to write to the db or data that were read from the db
    """

    def __init__(self, var: DataBaseVariable, data_range: DBRange):
        """
        initialize a new db batch
        :param var: the var to hold in the batch
        """

        self.__var = var
        self.__range = data_range
        self.__data = np.full(shape=data_range.shape,
                              fill_value=self.__var.default,
                              dtype=self.__var.var_type)

    def insert(self, time: float, lat: float, lon: float, value):
        """
        insert data to the batch. the new value will override any existing value
        :param value: the value to insert
        :param time: the time coordinate of said value
        :param lat: the lat coordinate of said value
        :param lon: the lon coordinate of said value
        :return:
        """

        indices = self.__range.get_indices_approximation(time, lat, lon)
        self.__data[indices] = value

    def __getitem__(self, item: Tuple[float, float, float]):
        """
        get the stored value for the given location
        :param item: the location to check for - (time, lat, lon)
        :return:
        """

        indices = self.__range.get_indices_approximation(*item)
        return self.__data[indices]
