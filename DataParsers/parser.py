from DataBase.DataBaseDataTypes.data_base_data_batch import DBBatch
from DataBase.DataBaseDataTypes.data_base_range import DBRange
from support.configuration_values import ConfigurationValues
import pandas as pd
import xarray
import netCDF4 as nc


class Parser:
    """
    this class implements the basic structure of a parser. you should create a new parser for each file type
    """

    def __init__(self, config: ConfigurationValues):
        self._config = config

    def parse(self, data_range: DBRange) -> DBBatch:
        """
        parse the data from the relevant resource
        :return: a DataBatch storing the new parsed data
        """
        pass


    def cvs_to_netcdf(cvs_file_path, netcdf_file_path):
        df = pd.read_csv(cvs_file_path)
        xr = df.to_xarray()
        xr.to_netcdf(netcdf_file_path)

    def netcdf_to_cvs(netcdf_file_path, cvs_file_path):
        net = nc.Dataset(netcdf_file_path, mode='r')
        cols = list(net.variables.keys())
        list_nc = []
        for c in cols:
            list_nc.append(list(net.variables[c][:]))
        df_nc = pd.DataFrame(list_nc)
        df_nc = df_nc.T
        df_nc.columns = cols
        df_nc.to_csv(cvs_file_path, index = False)
