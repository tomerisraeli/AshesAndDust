from DataBase.DataBaseDataTypes.data_base_data_batch import DBBatch
from DataBase.DataBaseDataTypes.data_base_range import DBRange
from DataParsers.parser import Parser

import rasterio
import rasterio.plot


class ElevationParser(Parser):

    def parse(self, data_range: DBRange) -> DBBatch:
        pass


if __name__ == '__main__':
    data_name = "/Users/tomerisraeli/Library/CloudStorage/GoogleDrive-tomer.israeli.43@gmail.com/My Drive/year_2/Magdad/data_samples/elevation/elevation final wgs/elevatinowgs.tif"
    tiff = rasterio.open(data_name)
    rasterio.plot.show(tiff, title="elevation data")
