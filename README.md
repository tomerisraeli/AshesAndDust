# Ashes And Dust

## Importing The Data

### NDVI 

#### importing the data
- source - we got the NDVI data from the [earthdata website](https://appeears.earthdatacloud.nasa.gov)
- dates range: 01.01.2010 - 31.12.2020
- relavent value: _1_km_16_days_EVI (MOD13A2.006)
- data format: NetCDF-4
- projection: MODIS Sinusoidal

#### data preprocessing
as the data is downloaded as a netCDF-4 file which we can easily open and at lat\lon coordinates we haven't made any preprocessing and used it as downloaded 


### elevation data

#### importing the data
- source - we got the elevationdata from the [aster earthdata website](https://www.earthdata.nasa.gov/sensors/aster)
- data format: .tif
- projection: ??

#### data preprocessing
the relevant data is downloaded over 9 separate tif files. using arcgis we...