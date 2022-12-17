import configparser
import os.path
from typing import Any
import logging


class ConfigurationValues:
    """
    the main point of this class is to wrap the configparser and make it easier to use

    to add a new config value all you should do is
    1. add a new ket at the class Keys
    2. add the key to the values list
    * to really add it to the file, you should add this manually or delete the .ini file and let the program do
        it for you to read

    to get a value, you just need to create a new ConfigurationValues instance and use the get_key func like so

    config = ConfigurationValues("<the path of your file>")
    value = config.get_key(ConfigurationValues.Keys.data_base_path)

    # notice that the values are returned as str, you can easily parse them

    """

    class Keys:
        """
        to make all the values easily accessible, the key to every value should appear in this class with its section
        name then the key itself and last the default values - (section_name, key, default_value)
        """

        # when adding new key, make sure to add it to the values list!

        data_base_path = {"section": "DataBase", "key": "Data Base Path", "default": "data_base.nc"}
        data_base_min_lat = {"section": "DataBaseRange", "key": "min latitude", "default": "0"}
        data_base_max_lat = {"section": "DataBaseRange", "key": "max latitude", "default": "30"}
        data_base_min_lon = {"section": "DataBaseRange", "key": "min longitude", "default": "0"}
        data_base_max_lon = {"section": "DataBaseRange", "key": "max longitude", "default": "30"}
        data_base_min_time = {"section": "DataBaseRange", "key": "min time", "default": "0"}
        data_base_max_time = {"section": "DataBaseRange", "key": "max time", "default": "30"}
        lat_res = {"section": "DataBaseResolution", "key": "latitude resolution(degrees)", "default": "0.01"}
        lon_res = {"section": "DataBaseResolution", "key": "longitude resolution(degrees)", "default": "0.01"}
        time_res = {"section": "DataBaseResolution", "key": "time resolution(days)", "default": "1"}

        values = [
            data_base_path,
            data_base_max_lon, data_base_min_lon,
            data_base_max_lat, data_base_min_lat,
            data_base_max_time, data_base_min_time,
            lat_res, lon_res,
            time_res
        ]

        @staticmethod
        def sections():
            return set(map(lambda t: t["section"], ConfigurationValues.Keys.values))

    def __init__(self, config_path: str):
        """
        open the config file, if missing a new one will be created
        :param config_path:
        """

        self.__path = config_path
        self.__config = configparser.ConfigParser()
        # load the file and parse the data
        if not os.path.isfile(self.__path):
            # configuration.ini file doesnt exists
            self.__create_file()
            return

        # the next section loads the data from the file
        # if we are at this section the file must exist(we checked)
        self.__config.read(self.__path)

    def __create_file(self):
        """
        create a new configuration.ini file
        if called when a configuration.ini file already exists it will be overwritten
        :return: None
        """

        logging.warning(f"configuration.ini file is missing, creating a new one at \'{self.__path}\'")

        # first, create the sections
        for section in ConfigurationValues.Keys.sections():
            self.__config[section] = {}

        # add the keys with default values
        for value in ConfigurationValues.Keys.values:
            self.__config[value["section"]][value["key"]] = value["default"]

        # save to file
        with open(self.__path, "x") as file:
            self.__config.write(file)

    def get_key(self, key) -> Any:
        """
        get the value for the given key

        * assuming the format of the key is valid,
        * if the section or the key itself is missing form the .inc file the default value is returned
        :return: the value as string
        """

        # we first make sure that key is in the correct format and valid
        if not all([keyword in key.keys() for keyword in ["key", "section", "default"]]):
            # some keywords are missing
            msg = f"the given key({key}) is in the wrong format"
            logging.fatal(msg)
            raise KeyError(msg)
        if not key["section"] in self.__config.sections():
            logging.warning(f"section \'{key['section']}\' is missing, using default values")
            return key["default"]
        if not key["key"] in self.__config[key["section"]]:
            logging.warning(f"key \'{key['key']}\' is missing at \'{key['section']}\', using default values")
            return key["default"]

        return self.__config[key["section"]][key["key"]]
