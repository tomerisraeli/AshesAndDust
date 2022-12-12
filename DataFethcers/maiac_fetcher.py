from DataBase.data_base import DataBase
from DataFethcers.fetcher import Fetcher


class MaiacFetcher(Fetcher):

    def fetch(self) -> None:
        """
        fetch data from MAIAC and add it to the db
        :return:
        """
        print(DataBase.Tables.maiac_table.sql_cmd_insert(["123"]))

        self._db.connection.execute(DataBase.Tables.maiac_table.sql_cmd_insert(["123"]))


