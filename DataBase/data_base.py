from DataBase.data_base_table import DataBaseTable
from support.configuration_values import ConfigurationValues

import sqlite3
from sqlite3 import Error as SqlError
import logging


# TODO: add logs
class DataBase:

    def __init__(self, config: ConfigurationValues):
        """
        open or create a new database if it doesn't exist yet
        """
        self.__tables = [
            DataBaseTable(title="SatData", columns=[
                ("date", DataBaseTable.DataTypes.INT)
            ])
        ]

        self.__connection = DataBase.create_db_connection(config)

        # create tables
        [self.__connection.execute(table.sql_cmd_open_or_create_table) for table in self.__tables]

    def __del__(self):
        """
        properly close the connection
        :return:
        """
        logging.info(f"closed connection to DB")
        self.__connection.close()

    @staticmethod
    def create_db_connection(config: ConfigurationValues):
        """
        create a db connection
        :param config:
        :return: db connection
        """
        connection = None
        try:
            connection = sqlite3.connect(config.get_key(ConfigurationValues.Keys.data_base_path))
            logging.info(f"connected successfully to db at '{config.get_key(ConfigurationValues.Keys.data_base_path)}'")
        except SqlError as e:
            logging.fatal(f"connection to db at '{config.get_key(ConfigurationValues.Keys.data_base_path)}' failed!")
        return connection

    @property
    def cursor(self):
        return self.__connection.cursor()
