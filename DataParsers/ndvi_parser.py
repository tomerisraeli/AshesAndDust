import logging

from matplotlib import pyplot as plt
from netCDF4 import Dataset

from DataBase.DBConstants import DBConstants
from DataBase.DataBaseDataTypes.data_base_data_batch import DBBatch
from DataBase.DataBaseDataTypes.data_base_range import DBRange
from DataBase.data_base import DataBase
from DataParsers.parser import Parser
from support.configuration_values import ConfigurationValues


class NDVIParser(Parser):
    """
    parse the NDVI data saved as NetCDF file.
    you can collect the data from https://www.earthdata.nasa.gov/learn/find-data
    """

    # the data is saved as NetCDF file on the data_samples dir of our project

    def parse(self, data_range: DBRange) -> DBBatch:
        logging.info(f"parsing NDVI data from '{self.__file_path}'")

        batch = DBBatch(DBConstants.VAR_NDVI, data_range)
        with Dataset(self.__file_path, mode="r", format="NETCDF4_CLASSIC") as ds:
            time_values, lat_values, lon_values = ds["time"][:], ds["lat"][:], ds["lon"][:]
            data = ds["int16 _1_km_16_days_EVI"][:, :, :]
            for time_index, time in enumerate(time_values):
                for lat_index, lat in enumerate(lat_values):
                    for lon_index, lon in enumerate(lon_values):
                        batch.insert(time, lat, lon, data[time_index, lat_index, lon_index])
            logging.info("logged file successfully")
            return batch

    @property
    def __file_path(self):
        return self._config.get_key(ConfigurationValues.Keys.ndvi_data_path)


if __name__ == '__main__':
    range = DBRange((3640, 10000, 1), ())
