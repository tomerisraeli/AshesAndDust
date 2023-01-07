import logging
import os

import numpy as np
from netCDF4 import Dataset

from DataBase.DBConstants import DBConstants
from DataBase.DataBaseDataTypes.data_base_data_batch import DBBatch
from DataBase.DataBaseDataTypes.data_base_range import DBRange
from support.configuration_values import ConfigurationValues


def db_session(session):
    def wrapper(*args, **kwargs):
        logging.info("starting a db session")
        with __open_or_create_netcdf_file(args[0].config) as nc_file:
            val = session(args[0], nc_file, *args[1:], **kwargs)
            logging.info("closing db session")
            return val

    return wrapper


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
        return Dataset(path, mode="r+", format=DBConstants.NETCDF_FORMAT)

    logging.warning(f"creating NetCDF file at '{path}'")
    ds = Dataset(path, mode="r+", format=DBConstants.NETCDF_FORMAT)
    __create_file(ds, config)
    return ds


def __create_file(ds, config):
    """
    create the file with all the data and variables
    :return:
    """

    # insert size and resolution
    # TODO: make a oneliner
    ds.lat_res = float(config.get_key(ConfigurationValues.Keys.lat_res))
    ds.lon_res = float(config.get_key(ConfigurationValues.Keys.lon_res))
    ds.time_res = float(config.get_key(ConfigurationValues.Keys.time_res))
    ds.min_lon = float(config.get_key(ConfigurationValues.Keys.data_base_min_lon))
    ds.min_lat = float(config.get_key(ConfigurationValues.Keys.data_base_min_lat))
    ds.min_time = float(config.get_key(ConfigurationValues.Keys.data_base_min_time))
    ds.max_lon = float(config.get_key(ConfigurationValues.Keys.data_base_max_lon))
    ds.max_lat = float(config.get_key(ConfigurationValues.Keys.data_base_max_lat))
    ds.max_time = float(config.get_key(ConfigurationValues.Keys.data_base_max_time))

    # calc number of samples in lat and lon dimensions
    lat_samples = round((ds.max_lat - ds.min_lat) / ds.lat_res) + 1
    lon_samples = round((ds.max_lon - ds.min_lon) / ds.lon_res) + 1

    # create the dimensions of the file
    ds.createDimension(DBConstants.DIM_TIME, None)
    ds.createDimension(DBConstants.DIM_LAT, lat_samples)
    ds.createDimension(DBConstants.DIM_LON, lon_samples)

    # add all variables
    for var in DBConstants.ALL_VARIABLES:
        file_var = ds.createVariable(var.name, var.var_type, var.dimensions)
        file_var.units = var.units
        file_var.long_name = var.full_name

    ds[DBConstants.VAR_LON.name][:] = np.linspace(ds.min_lon, ds.max_lon, lon_samples, endpoint=True)
    ds[DBConstants.VAR_LAT.name][:] = np.linspace(ds.min_lat, ds.max_lat, lat_samples, endpoint=True)
    ds[DBConstants.VAR_TIME.name][:] = [0] + np.arange(ds.min_time, ds.max_time + ds.time_res, ds.time_res)


class DataBase:
    """
    manage the access to the database which is saved as Netcdf
    you may want to learn more about NetCDF at
        'https://unidata.github.io/python-training/workshop/Bonus/netcdf-writing'
    """

    def __init__(self, config: ConfigurationValues):
        """
        :param config:
        """

        self.__config = config
        self.__range = self.__get_range()

    @db_session
    def __get_range(self, nc_file):
        return DBRange(
            time_range=(nc_file.min_time, nc_file.max_time, nc_file.time_res),
            lat_range=(nc_file.min_lat, nc_file.max_lat, nc_file.lat_res),
            lon_range=(nc_file.min_lon, nc_file.max_lon, nc_file.lon_res)
        )

    @db_session
    def insert(self, nc_file, data_batch: DBBatch):
        """
        insert a new data batch to database, if the data already exists it should be overwritten
        :param nc_file: the nc file, given by the wrapper
        :param data_batch: the batch of data to enter
        :return: None
        """

        time_samples, lat_samples, lon_samples = data_batch.range.shape
        # TODO: make sure the res on the db and the batch range are the same

        offset_time, offset_lat, offset_lon = data_batch.range.relative_root
        offset_time_index, offset_lat_index, offset_lon_index = self.calc_indices_values(offset_time,
                                                                                         offset_lat,
                                                                                         offset_lon)

        if data_batch.var.is_spatial_only:
            logging.info(
                f"updating {data_batch.var.name} (spatial), "
                f"lat index {offset_lat_index} to {offset_lat_index + lat_samples} and "
                f"lon index {offset_lon_index} to {offset_lon_index + lon_samples} "
            )

            nc_file[data_batch.var.name][
            offset_lat_index: offset_lat_index + lat_samples,
            offset_lon_index: offset_lon_index + lon_samples
            ] = data_batch.data[0]
        else:
            logging.info(
                f"updating {data_batch.var.name} at time index {offset_time_index} to {offset_time_index + time_samples}, "
                f"lat index {offset_lat_index} to {offset_lat_index + lat_samples} and "
                f"lon index {offset_lon_index} to {offset_lon_index + lon_samples} "
            )

            nc_file[data_batch.var.name][
            offset_time_index: offset_time_index + time_samples,
            offset_lat_index: offset_lat_index + lat_samples,
            offset_lon_index: offset_lon_index + lon_samples
            ] = data_batch.data

    @db_session
    def load(self, nc_file, data_range: DBRange, var):
        """
        load data from the database
        :param nc_file: the nc file, given by the wrapper
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

        if var.is_spatial_only:
            data_batch.data = [
                nc_file[data_batch.var.name][
                offset_lat_index: offset_lat_index + lat_samples,
                offset_lon_index: offset_lon_index + lon_samples
                ]
            ]
        else:
            data_batch.data = nc_file[data_batch.var.name][
                              offset_time_index: offset_time_index + time_samples,
                              offset_lat_index: offset_lat_index + lat_samples,
                              offset_lon_index: offset_lon_index + lon_samples
                              ]

        return data_batch

    def calc_indices_values(self, time: float, lat: float, lon: float):
        """
        calc the indices of the given coordinate
        :return: the said indices as tuple of floats - (time, lat, lon)
        """

        return self.__range.get_indices_approximation(time, lat, lon)

    @property
    def range(self):
        return self.__range

    @property
    def config(self):
        return self.__config
