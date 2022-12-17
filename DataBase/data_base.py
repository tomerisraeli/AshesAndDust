import logging
import os

import numpy as np
from netCDF4 import Dataset
from DataBase.DataBaseDataTypes.data_base_coordinate import DataBaseCoordinate
from DataBase.DataBaseDataTypes.data_base_data_batch import DataBatch
from DataBase.DataBaseDataTypes.data_base_data_range import DataRange
from DataBase.DataBaseDataTypes.data_base_variable import DataBaseVariable
from support.configuration_values import ConfigurationValues


class DataBase:
    """
    manage the access to the database which is saved as Netcdf
    you may want to  learn more about NetCDF at
        'https://unidata.github.io/python-training/workshop/Bonus/netcdf-writing'
    """

    class Constants:
        NETCDF_FORMAT = "NETCDF4_CLASSIC"

        """
        DIMENSIONS
        constant of all the dimensions in the db
        """
        DIM_LAT = "lat"
        DIM_LON = "lon"
        DIM_TIME = "time"

        """
        VARIABLES
        consts of all the vars in the db
        """
        VAR_LAT = DataBaseVariable("lat", np.float32, (DIM_LAT,), "degrees north", "latitude")
        VAR_LON = DataBaseVariable("lon", np.float32, (DIM_LAT,), "degrees east", "longitude")
        VAR_TIME = DataBaseVariable("time", np.float64, (DIM_TIME,), "hours since 1970-01-01", "time")
        VAR_TEMP = DataBaseVariable("temp", np.float64, (DIM_TIME, DIM_LAT, DIM_LON), "C", "air temp")

        ALL_VARIABLES = [VAR_LAT, VAR_LON, VAR_TIME, VAR_TEMP]

    def __init__(self, config: ConfigurationValues):
        """
        :param config:
        """

        self.__nc_file = DataBase.__open_or_create_netcdf_file(config)

        self.__lat_res = self.__nc_file.lat_res
        self.__lon_res = self.__nc_file.lon_res
        self.__time_res = self.__nc_file.time_res
        self.__root_coord = DataBaseCoordinate(self.__nc_file.root_lon,
                                               self.__nc_file.root_lat,
                                               self.__nc_file.root_time)

    @staticmethod
    def __create_file(ds, config):
        """
        create the file with all the data and variables
        :return:
        """
        # first, we create the dimensions of the file
        ds.createDimension(DataBase.Constants.DIM_TIME, None)
        ds.createDimension(DataBase.Constants.DIM_LAT, 10)
        ds.createDimension(DataBase.Constants.DIM_LON, 10)

        # add all variables
        for var in DataBase.Constants.ALL_VARIABLES:
            file_var = ds.createVariable(var.name, var.var_type, var.dimensions)
            file_var.units = var.units
            file_var.long_name = var.full_name

        # insert size and resolution
        ds.lat_res = float(config.get_key(ConfigurationValues.Keys.lat_res))
        ds.lon_res = float(config.get_key(ConfigurationValues.Keys.lon_res))
        ds.time_res = float(config.get_key(ConfigurationValues.Keys.time_res))
        ds.root_lon = float(config.get_key(ConfigurationValues.Keys.data_base_min_lon))
        ds.root_lat = float(config.get_key(ConfigurationValues.Keys.data_base_min_lat))
        ds.root_time = float(config.get_key(ConfigurationValues.Keys.data_base_min_time))

    def __del__(self):
        """
        properly close the db file
        :return: None
        """
        logging.info("closing db file")
        self.__nc_file.close()

    @staticmethod
    def __open_or_create_netcdf_file(config: ConfigurationValues):
        """
        open (if exists) or create a new NetCDF file at the given path
        if the file exists the program assumes it is in valid format
        :param config: the configuration data
        :return: the DataSet of the file
        """
        path = config.get_key(ConfigurationValues.Keys.data_base_path)
        if os.path.isfile(path):
            logging.info(f"opening NetCDF file at '{path}'")
            return Dataset(path, mode="r+", format=DataBase.Constants.NETCDF_FORMAT)

        logging.warning(f"creating NetCDF file at '{path}'")
        ds = Dataset(path, mode="r+", format=DataBase.Constants.NETCDF_FORMAT)
        DataBase.__create_file(ds, config)
        return ds

    def insert(self, data_batch: DataBatch):
        """
        insert a new data batch to database, if the data already exists it should be overwritten
        :param data_batch: the batch of data to enter
        :return: None
        """

        for coord, data in data_batch.data:
            print(data)
            lat_ind, lon_ind, time_ind = self.calc_axis_values(coord)
            print(lat_ind, lon_ind, time_ind)
            for var in data.keys():
                v = self.__nc_file[var.name][:]
                v[lat_ind][lon_ind][time_ind] = data[var]

    def load(self, data_range: DataRange, vars):
        """
        load data from the database
        :param data_range: the range of data to load
        :param vars: list of the vars to load
        :return: batch of data with the coordinates that were found in the database and there values
        """

        data_batch = DataBatch()

        min_indices = self.calc_axis_values(data_range.min_coord)
        max_indices = self.calc_axis_values(data_range.max_coord)

        # TODO: validate indices
        for var in vars:
            d = self.__nc_file[var.name][
                min_indices[0]:max_indices[0],
                min_indices[1]:max_indices[1],
                min_indices[2]:max_indices[2]
                ]
            print(d)

    @property
    def root_coordinate(self):
        """
        get a coordinate whose coordinate at the db is (0,0,0)
        :return: an arbitrary coordinate from the database
        """
        return self.__root_coord

    def calc_axis_values(self, coord: DataBaseCoordinate):
        """
        calc the axis values of the given coordinate
        :param coord:
        :return:
        """

        lat_samples = (coord.lat - self.root_coordinate.lat) / self.__lat_res
        lon_samples = (coord.lon - self.root_coordinate.lon) / self.__lon_res
        time_samples = 0
        if coord.time is not None:
            time_samples = (coord.time - self.root_coordinate.time) / self.__time_res

        return int(lat_samples), int(lon_samples), int(time_samples)
