class DataBaseCoordinate:
    """
    hold a data coordinate with lon, lat and an optional date(seconds since 1.1.1970)
    """

    def __init__(self, lon, lat, date=None):
        self.__lon = lon
        self.__lat = lat
        self.__date = date  # if None, the coordinate is matched to the data of the lon\lat that is const over time

    @property
    def is_timed(self):
        """
        check if the data is spatial only or also timed
        :return:
        """
        return self.__date is not None
