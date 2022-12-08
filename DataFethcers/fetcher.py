from DataBase.data_base import DataBase
from support.ConfigurationValues.configuration_values import ConfigurationValues

"""
every resource should have a fetcher. the fetcher is responsible for fetching and updating the data in the database
"""


# TODO: add logs
class Fetcher:
    """
    this class implements the basic structure of a fetcher
    """

    @staticmethod
    def fetch(db: DataBase, config: ConfigurationValues) -> None:
        """
        fetch the data from the relevant resource and store it at the DataBase
        :param config:
        :param db:
        :return:
        """
        pass

    @staticmethod
    def get_last_update(db: DataBase):
        """
        get the last date data was fetched from the resource
        :param db:
        :return: date
        """
        pass
