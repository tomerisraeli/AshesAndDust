import logging
import os

import numpy as np
from netCDF4 import Dataset

from DataBase.DataBaseDataTypes.data_base_data_batch import DBBatch
from DataBase.DataBaseDataTypes.data_base_range import DBRange
from DataBase.DataBaseDataTypes.data_base_variable import DataBaseVariable
from data_base_errors import DataBatchResolutionInvalid
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
        VAR_NDVI = DataBaseVariable("NDVI", np.float64, (DIM_TIME, DIM_LAT, DIM_LON), "ndvi", "how green is the land")

        ALL_VARIABLES = [
            VAR_LAT, VAR_LON, VAR_TIME,
            VAR_TEMP, VAR_NDVI
        ]

    def __init__(self, config: ConfigurationValues):
        """
        :param config:
        """

        self.__nc_file = DataBase.__open_or_create_netcdf_file(config)

        self.__lat_res = self.__nc_file.lat_res
        self.__lon_res = self.__nc_file.lon_res
        self.__time_res = self.__nc_file.time_res
        self.__root_time = self.__nc_file.min_time
        self.__root_lat = self.__nc_file.min_lat
        self.__root_lon = self.__nc_file.min_lon

    @staticmethod
    def __create_file(ds, config):
        """
        create the file with all the data and variables
        :return:
        """

        # insert size and resolution
        ds.lat_res = float(config.get_key(ConfigurationValues.Keys.lat_res))
        ds.lon_res = float(config.get_key(ConfigurationValues.Keys.lon_res))
        ds.time_res = float(config.get_key(ConfigurationValues.Keys.time_res))
        ds.min_lon = float(config.get_key(ConfigurationValues.Keys.data_base_min_lon))
        ds.min_lat = float(config.get_key(ConfigurationValues.Keys.data_base_min_lat))
        ds.min_time = float(config.get_key(ConfigurationValues.Keys.data_base_min_time))
        ds.max_lon = float(config.get_key(ConfigurationValues.Keys.data_base_max_lon))
        ds.max_lat = float(config.get_key(ConfigurationValues.Keys.data_base_max_lat))
        ds.max_time = float(config.get_key(ConfigurationValues.Keys.data_base_max_lat))

        # calc number of samples in lat and lon dimensions
        lat_samples = int((ds.max_lat - ds.min_lat) / ds.lat_res) + 1
        lon_samples = int((ds.max_lon - ds.min_lon) / ds.lon_res) + 1

        # create the dimensions of the file
        ds.createDimension(DataBase.Constants.DIM_TIME, None)
        ds.createDimension(DataBase.Constants.DIM_LAT, lat_samples)
        ds.createDimension(DataBase.Constants.DIM_LON, lon_samples)

        # add all variables
        for var in DataBase.Constants.ALL_VARIABLES:
            file_var = ds.createVariable(var.name, var.var_type, var.dimensions)
            file_var.units = var.units
            file_var.long_name = var.full_name

        ds[DataBase.Constants.VAR_LON.name][:] = np.arange(ds.min_lon, ds.max_lon + ds.lon_res, ds.lon_res)
        ds[DataBase.Constants.VAR_LAT.name][:] = np.arange(ds.min_lat, ds.max_lat + ds.lat_res, ds.lat_res)
        ds[DataBase.Constants.VAR_TIME.name][:] = [0] + np.arange(ds.min_time, ds.max_time + ds.time_res, ds.time_res)

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

    def resolution_check(self, data_batch: DBBatch):
        if [self.__time_res, self.__lon_res, self.lat_res] != data_batch.range.resolution_vector():
            raise DataBatchResolutionInvalid

    def insert(self, data_batch: DBBatch):
        """
        insert a new data batch to database, if the data already exists it should be overwritten
        :param data_batch: the batch of data to enter
        :return: None
        """

        self.resolution_check(data_batch)

        time_samples, lat_samples, lon_samples = data_batch.range.shape

        offset_time, offset_lat, offset_lon = data_batch.range.relative_root
        offset_time_index, offset_lat_index, offset_lon_index = self.calc_indices_values(offset_time,
                                                                                         offset_lat,
                                                                                         offset_lon)
        self.__nc_file[data_batch.var.name][
        offset_time_index: offset_time + time_samples,
        offset_lat_index: offset_lat_index + lat_samples,
        offset_lon_index: offset_lon_index + lon_samples
        ] = data_batch.data

    def load(self, data_range: DBRange, var):
        """
        load data from the database
        :param data_range: the range of data to load
        :param var: the var to load
        :return: batch of data with the given range and var values
        """

        data_batch = DBBatch(var, data_range)

        time_samples, lat_samples, lon_samples = data_batch.range.shape

        offset_time, offset_lat, offset_lon = data_batch.range.relative_root
        offset_time_index, offset_lat_index, offset_lon_index = self.calc_indices_values(offset_time,
                                                                                         offset_lat,
                                                                                         offset_lon)
        data_batch.data = self.__nc_file[data_batch.var.name][
                          offset_time_index: offset_time + time_samples,
                          offset_lat_index: offset_lat_index + lat_samples,
                          offset_lon_index: offset_lon_index + lon_samples
                          ]

        return data_batch

    def calc_indices_values(self, time: float, lat: float, lon: float):
        """
        calc the indices of the given coordinate
        :return: the said indices as tuple of floats - (time, lat, lon)
        """

        lat_samples = (lat - self.__root_lat) / self.__lat_res
        lon_samples = (lon - self.__root_lon) / self.__lon_res
        time_samples = (time - self.__root_time) / self.__time_res

        return int(time_samples), int(lat_samples), int(lon_samples)
