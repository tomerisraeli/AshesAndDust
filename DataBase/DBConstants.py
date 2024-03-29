import numpy as np

from DataBase.DataBaseDataTypes.data_base_variable import DBVariable


class DBConstants:
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
    VAR_LAT = DBVariable("lat", np.float32, (DIM_LAT,), "degrees north", "latitude")
    VAR_LON = DBVariable("lon", np.float32, (DIM_LON,), "degrees east", "longitude")
    VAR_TIME = DBVariable("time", np.float64, (DIM_TIME,), "hours since 1970-01-01", "time")
    VAR_TEMP = DBVariable("temp", np.float64, (DIM_TIME, DIM_LAT, DIM_LON), "C", "air temp")
    VAR_NDVI = DBVariable("NDVI", np.float64, (DIM_TIME, DIM_LAT, DIM_LON), "ndvi", "how green is the land")
    VAR_ELEV = DBVariable("elevation", np.float64, (DIM_LAT, DIM_LON),
                          "elevation", "the elevation in meters", default=0)
    VAR_DTWB = DBVariable("distance to water body", np.float64, (DIM_LAT, DIM_LON),
                          "the distance to closest water body", "the distance to closest water body")

    ALL_VARIABLES = [
        VAR_LAT, VAR_LON, VAR_TIME,
        VAR_TEMP, VAR_NDVI, VAR_ELEV, VAR_DTWB
    ]
