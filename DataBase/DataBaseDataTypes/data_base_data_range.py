from DataBase.DataBaseDataTypes.data_base_coordinate import DataBaseCoordinate
from DataBase.data_base_errors import CoordinateOutOfBoundsError
from support import approximations


class DataRange:
    """
    this class represents a range of coordinates
    """

    def __init__(self, lon_range, lat_range, time_range):
        """

        :param lon_range: (tuple) range of lon values
        :param lat_range: (tuple) range of lat values
        :param time_range:  (tuple) range of time values
        """

        self.__min_lon, self.__max_lon = min(lon_range), max(lon_range)
        self.__min_lat, self.__max_lat = min(lat_range), max(lat_range)
        self.__min_time, self.__max_time = min(time_range), max(time_range)

    def __contains__(self, item: DataBaseCoordinate):
        return \
            self.__min_time <= item.time <= self.__max_time \
            and self.__min_lat <= item.lat <= self.__max_lat \
            and self.__min_lon <= item.lon <= self.__max_lon

    @property
    def lat_range(self):
        return self.__min_lat, self.__max_lat

    @property
    def lon_range(self):
        return self.__min_lon, self.__max_lon

    @property
    def time_range(self):
        return self.__min_time, self.__max_time

    @property
    def min_coord(self):
        return DataBaseCoordinate(self.__min_lon, self.__min_lat, self.__min_time)

    @property
    def max_coord(self):
        return DataBaseCoordinate(self.__max_lon, self.__max_lat, self.__max_time)

    def shape(self, lat_res, lon_res, time_res):
        """
        get the shape of the range with the given res
        :param lat_res:
        :param lon_res:
        :param time_res:
        :return:
        """

        # we want index of the max coord +1 on each dimension
        i1, i2, i3 = self.index_of(self.max_coord, lat_res, lon_res, time_res)
        return i1 + 1, i2 + 1, i3 + 1

    def index_of(self, coord: DataBaseCoordinate, lat_res, lon_res, time_res):
        """
        get the indices of the given coordinate
        :param coord:
        :param lat_res:
        :param lon_res:
        :param time_res:
        :return:
        """

        if coord not in self:
            raise CoordinateOutOfBoundsError("the given coordinate is out of the range")

        return \
            int((coord.time - self.__min_time) / time_res), \
            int((coord.lat - self.__min_lat) / lat_res), \
            int((coord.lon - self.__min_lon) / lon_res)

