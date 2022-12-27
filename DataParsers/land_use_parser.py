from DataBase.DataBaseDataTypes.data_base_data_batch import DBBatch
from DataBase.DataBaseDataTypes.data_base_range import DBRange
from DataParsers.parser import Parser


class LandUseParser(Parser):

    def parse(self, data_range: DBRange) -> DBBatch:
        pass
