from DataBase.DataBaseDataTypes.data_base_data_batch import DBBatch
from DataBase.DataBaseDataTypes.data_base_range import DBRange
from support.configuration_values import ConfigurationValues


class Parser:
    """
    this class implements the basic structure of a parser. you should create a new parser for each file type
    """

    def __init__(self, config: ConfigurationValues):
        self._config = config

    def parse(self, data_range: DBRange) -> DBBatch:
        """
        parse the data from the relevant resource
        :return: a DataBatch storing the new parsed data
        """
        pass


