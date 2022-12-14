class DataBatch:
    """
    hold a batch of data to write to or read from the database
    """

    def __init__(self):
        self.__data = {}

    def get_data(self):
        """
        get the data as a dict where the keys are 'DataBaseCoordinate' and the values are dict with the different
        values stored
        :return:
        """
        return self.__data
