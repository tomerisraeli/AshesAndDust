from support import approximations


class DataBaseCoordinate:
    """
    hold a data coordinate with lon, lat and an optional date(seconds since 1.1.1970)
    """

    def __init__(self, lon, lat, time=None):
        self.__lon = lon
        self.__lat = lat
        self.__time = time  # if None, the coordinate is matched to the data of the lon\lat that is const over time

    @property
    def is_timed(self):
        """
        check if the data is spatial only or also timed
        :return:
        """
        return self.__time is not None

    def fit(self, lon_res, lat_res, time_res, reference_point):
        """
        fit the coordinate to a discrete coordinate system matching the given values
        :param lon_res: the jumps at the lon axes
        :param lat_res: the jumps at the lat axes
        :param time_res: the jumps at the time axes
        :param reference_point: a valid coordinate at the desired coordinate system
        :return: None
        """

        self.__lat = approximations.discrete_approximation(lat_res, reference_point.__lat, self.__lat)
        self.__lon = approximations.discrete_approximation(lon_res, reference_point.__lon, self.__lon)
        self.__time = approximations.discrete_approximation(time_res, reference_point.__time, self.__time)

    @property
    def lon(self):
        return self.__lon

    @property
    def lat(self):
        return self.__lat

    @property
    def time(self):
        return self.__time
