from DataBase.DataBaseDataTypes.data_base_coordinate import DataBaseCoordinate
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

