from DataBase.data_base import DataBase
from support.configuration_values import ConfigurationValues

"""
every resource should have a fetcher. the fetcher is responsible for fetching and updating the data in the database
"""


# TODO: add logs
class Fetcher:
    """
    this class implements the basic structure of a fetcher
    """

    def __init__(self, db, config: ConfigurationValues):
        self.__db = db
        self.__config = config

    def fetch(self) -> None:
        """
        fetch the data from the relevant resource and store it at the DataBase
        :return: None
        """
        pass

