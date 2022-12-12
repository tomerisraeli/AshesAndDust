from DataBase.data_base import DataBase
from DataBase.data_base_table import DataBaseTable
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
        self._db = db
        self._config = config

    def fetch(self) -> None:
        """
        fetch the data from the relevant resource and store it at the DataBase
        :param db_connection: the connection to the db, you should use it to make changes
        :return: None
        """
        pass


