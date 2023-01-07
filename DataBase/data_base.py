import logging

from DataBase.DataBaseDataTypes.data_base_data_batch import DBBatch
from DataBase.DataBaseDataTypes.data_base_range import DBRange
from DataBase.db_session import db_session
from support import loggers

from support.configuration_values import ConfigurationValues


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
            loggers.db_logger.info(
                f"updating {data_batch.var.name} (spatial), "
                f"lat index {offset_lat_index} to {offset_lat_index + lat_samples} and "
                f"lon index {offset_lon_index} to {offset_lon_index + lon_samples} "
            )

            nc_file[data_batch.var.name][
            offset_lat_index: offset_lat_index + lat_samples,
            offset_lon_index: offset_lon_index + lon_samples
            ] = data_batch.data[0]
        else:
            loggers.db_logger.info(
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
            loggers.db_logger.info(f"loading spatial data for {data_range}")
            data_batch.data = [
                nc_file[data_batch.var.name][
                offset_lat_index: offset_lat_index + lat_samples,
                offset_lon_index: offset_lon_index + lon_samples
                ]
            ]
        else:
            loggers.db_logger.info(f"loading timed data for {data_range}")
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
