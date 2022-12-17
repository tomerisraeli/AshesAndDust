from DataBase.DataBaseDataTypes.data_base_coordinate import DataBaseCoordinate
from DataBase.DataBaseDataTypes.data_base_data_batch import DataBatch
from DataBase.DataBaseDataTypes.data_base_data_range import DataRange
from DataBase.data_base import DataBase
from support.configuration_values import ConfigurationValues

if __name__ == '__main__':
    config = ConfigurationValues("../data_base_test_config.ini")
    db = DataBase(config)

    b = DataBatch()
    b.insert(DataBaseCoordinate(0,0,0), {DataBase.Constants.VAR_TEMP: 10})
    db.insert(b)

    print(db.load(DataRange((0, 10), (0, 10), (1, 10)), [DataBase.Constants.VAR_TEMP]))