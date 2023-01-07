import logging
import os

import numpy as np
from netCDF4 import Dataset

from DataBase.DBConstants import DBConstants
from support import loggers
from support.configuration_values import ConfigurationValues


def db_session(session):
    """
    a wrapper for funcs that need an open db.
    :param session:
    :return:
    """
    def wrapper(*args, **kwargs):
        loggers.db_logger.info("starting a db session")
        with __open_or_create_netcdf_file(args[0].config) as nc_file:
            val = session(args[0], nc_file, *args[1:], **kwargs)
            loggers.db_logger.info("closing db session")
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
        loggers.db_logger.info(f"opening NetCDF file at '{path}'")
        return Dataset(path, mode="r+", format=DBConstants.NETCDF_FORMAT)

    loggers.db_logger.warning(f"creating NetCDF file at '{path}'")
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
    loggers.db_logger.info(f"created dimensions of db with {lat_samples} lat samples and {lon_samples} lon samples")

    # add all variables
    for var in DBConstants.ALL_VARIABLES:
        file_var = ds.createVariable(var.name, var.var_type, var.dimensions)
        file_var.units = var.units
        file_var.long_name = var.full_name
        loggers.db_logger.info(f"added {var.name}")

    ds[DBConstants.VAR_LON.name][:] = np.linspace(ds.min_lon, ds.max_lon, lon_samples, endpoint=True)
    ds[DBConstants.VAR_LAT.name][:] = np.linspace(ds.min_lat, ds.max_lat, lat_samples, endpoint=True)
    ds[DBConstants.VAR_TIME.name][:] = np.arange(ds.min_time, ds.max_time + ds.time_res, ds.time_res)

