import configparser
import os.path
from typing import Any


class ConfigurationValues:
    """
    the main point of this class is to wrap the configparser and make it easier to use
    """

    # the path to the config file
    __Config_File_Path = ""

    class Keys:
        """
        to make all the values easily accessible, the key to every value should appear in this class with its section
        name then the key itself and last the default values - (section_name, key, default_value)
        """
        data_base_path = {"section": "DataBase", "key": "Data Base Path", "default": "database_sql"}

        @staticmethod
        def sections():
            return set(map(lambda t: t["section"], ConfigurationValues.Keys.values()))

        @staticmethod
        def values():
            return ConfigurationValues.Keys.__dict__.values()

    def __init__(self):
        """

        """

        # load the file and parse the data
        if not os.path.isfile(ConfigurationValues.__Config_File_Path):
            # configuration file doesnt exists
            self.__create_file()
            return

        # the next section loads the data from the file
        # if we are at this section the file must exist(we checked)

    def __create_file(self):
        """
        create a new configuration file
        if called when a configuration file already exsits it will be overwritten
        :return: None
        """
        # TODO: add a log at this point with some msg like this "creating a new configuration file"

        config = configparser.ConfigParser()
        # first, create the sections
        for section in ConfigurationValues.Keys.sections():
            config[section] = {}

        # add the keys with default values
        for value in ConfigurationValues.Keys.values():
            config[value["section"]][value["key"]] = value["default"]

        # save to file
        with open(self.__Config_File_Path, "x") as file:
            config.write(file)

    def get_key(self, key) -> Any:
        """
        get the value for the given key
        :param key:
        :return:
        """
        pass


if __name__ == '__main__':
    config = ConfigurationValues()
    path = config.get_key(ConfigurationValues.Keys.data_base_path)