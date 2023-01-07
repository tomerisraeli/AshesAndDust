from typing import Tuple

from DataBase.data_base_errors import CoordinateOutOfBoundsError


class DBRange:
    def __init__(self,
                 time_range: Tuple[float, float, float],
                 lat_range: Tuple[float, float, float],
                 lon_range: Tuple[float, float, float]
                 ):
        """
        initial a DB range. every res should divide the diff between the min and the max
        :param time_range: a tuple of (min time, max time, time res)
        :param lat_range: a tuple of (min time, max time, time res)
        :param lon_range: a tuple of (min time, max time, time res)
        """

        self.__min_time, self.__max_time, self.__time_res = time_range
        self.__min_lat, self.__max_lat, self.__lat_res = lat_range
        self.__min_lon, self.__max_lon, self.__lon_res = lon_range

        # TODO: data validation

    @property
    def shape(self):
        """
        get the number of samples on each dimension
        :return: a tuple of number of time samples, number of lat samples, number of lon samples
        """
        return \
            1 + int((self.__max_time - self.__min_time) / self.__time_res), \
            1 + int((self.__max_lat - self.__min_lat) / self.__lat_res), \
            1 + int((self.__max_lon - self.__min_lon) / self.__lon_res)

    @property
    def relative_root(self):
        """
        get the root(the min coordinate) of the range
        :return: (time, lat, lon) as tuple of floats
        """
        return self.__min_time, self.__min_lat, self.__min_lon

    def get_indices_approximation(self, time, lat, lon):
        """
        get the indices to the given location in the array
        :param time:
        :param lat:
        :param lon:
        :return:
        """

        indices = \
            round((time - self.__min_time) / self.__time_res), \
            round((lat - self.__min_lat) / self.__lat_res), \
            round((lon - self.__min_lon) / self.__lon_res)

        # validate values
        if not all([0 <= indices[i] < self.shape[i] for i in range(len(indices))]):
            raise CoordinateOutOfBoundsError(
                f"the given coordinate (time: {time}, lat: {lat}, lon: {lon}) is out of range"
            )

        return indices

    def __str__(self):
        return \
            f"""
            DBRange:
            time: {self.__min_time} to {self.__max_time} with res {self.__time_res}
            lat : {self.__min_lat} to {self.__max_lat} with res {self.__lat_res}
            lon : {self.__min_lon} to {self.__max_lon} with res {self.__lon_res}
            """

