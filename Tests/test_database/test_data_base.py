import os
import unittest

from DataBase.DataBaseDataTypes.data_base_coordinate import DataBaseCoordinate
from DataBase.DataBaseDataTypes.data_base_data_batch import DataBatch
from DataBase.DataBaseDataTypes.data_base_data_range import DataRange
from DataBase.data_base import DataBase
from support.configuration_values import ConfigurationValues


class TestDataBase(unittest.TestCase):
    config_path = "config.ini"
    db_path = "db.nc"

    def test_create_new_file(self):
        # we first make sure the file really is missing
        if os.path.isfile(TestDataBase.db_path):
            os.remove(TestDataBase.db_path)

        _ = DataBase(ConfigurationValues(TestDataBase.config_path))
        self.assertTrue(os.path.isfile(TestDataBase.db_path), "the file is missing")

    def test_insert_and_load_temp(self):
        db = DataBase(ConfigurationValues(TestDataBase.config_path))
        batch = DataBatch(DataBase.Constants.VAR_TEMP)
        for i in range(30):
            batch.insert(DataBaseCoordinate(0.1*i, 0.1*i, 0.1*i), i)
        db.insert(batch)

        data_loaded = db.load(batch.batch_range, DataBase.Constants.VAR_TEMP)
        for i in range(30):
            self.assertEqual(data_loaded[DataBaseCoordinate(0.1*i, 0.1*i, 0.1*i)], i, "loaded data is missing coordinates")

