import numpy as np

from DataBase.DataBaseDataTypes.data_base_coordinate import DataBaseCoordinate
from DataBase.DataBaseDataTypes.data_base_data_range import DataRange
from DataBase.DataBaseDataTypes.data_base_variable import DataBaseVariable


class DataBatch:
    """
    hold a batch of data to write the db ot data that were read from the db
    """

    def __init__(self, var: DataBaseVariable):
        """
        create a new data batch
        """
        self.__data = {}
        self.__var = var

    def insert(self, coordinate: DataBaseCoordinate, value):
        """
        insert new data to the batch if coordinate already exits, data is updated
        :param coordinate: the coordinate of the data
        :param value: the value of the coordinate
        :return: None
        """

        self.__data[coordinate] = value

    def get(self, lat_res, lon_res, time_res, data_range: DataRange = None):
        """
        get a 3d matrix of the given var (time, lat, lon) with th associated value for each coordinate
        :param lat_res:
        :param time_res:
        :param lon_res:
        :param data_range: the range to read, if None the full range is taken
        :return: a 3d matrix and the offset - the min coordinate
        """

        if data_range is None:
            data_range = self.batch_range

        # fill the result with default values
        data_arr = np.full(shape=data_range.shape(lat_res, lon_res, time_res),
                           fill_value=self.__var.default,
                           dtype=self.__var.var_type)

        for coord, value in self.__data.items():
            if coord in data_range:
                data_arr[data_range.index_of(coord, lat_res, lon_res, time_res)] = value
        return data_arr, data_range.min_coord

    @property
    def batch_range(self):
        """
        get the data range of the DataBatch (the min one)
        :return:
        """

        return DataRange(
            lat_range=(
                min(self.__data.keys(), key=lambda c: c.lat).lat,
                max(self.__data.keys(), key=lambda c: c.lat).lat
            ), lon_range=(
                min(self.__data.keys(), key=lambda c: c.lon).lon,
                max(self.__data.keys(), key=lambda c: c.lon).lon
            ), time_range=(
                min(self.__data.keys(), key=lambda c: c.time).time,
                max(self.__data.keys(), key=lambda c: c.time).time
            )
        )

    @property
    def data(self):
        return self.__data

    @property
    def var(self):
        return self.__var

    def __getitem__(self, item: DataBaseCoordinate):
        return self.__data[item]
