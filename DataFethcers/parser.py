from DataBase.data_base_data_batch import DataBatch
from support.configuration_values import ConfigurationValues


class Parser:
    """
    this class implements the basic structure of a parser. you should create a new parser for each file type
    """

    def __init__(self, config: ConfigurationValues):
        self._config = config

    def parse(self, file) -> DataBatch:
        """
        parse the data from the relevant resource
        :return: a DataBatch storing the new parsed data
        """
        pass


