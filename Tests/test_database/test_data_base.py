import os
import unittest

from DataBase.DataBaseDataTypes.data_base_data_batch import DBBatch
from DataBase.DataBaseDataTypes.data_base_range import DBRange
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

        data_range = DBRange(time_range=(0, 1, 1),
                             lat_range=(0, 30, 0.01),
                             lon_range=(0, 30, 0.01)
                             )
        batch = DBBatch(DataBase.Constants.VAR_TEMP, data_range)
        for i in range(30):
            batch.insert(1, i, i, i*10)
        db.insert(batch)

        data_loaded = db.load(data_range, DataBase.Constants.VAR_TEMP)
        for i in range(30):
            self.assertEqual(data_loaded[(1, i, i)], i*10,
                             "loaded data is missing coordinates")

    def test_res_validation(self):
        """
        check if the db allow the user to insert data with the wrong resolution
        :return:
        """
        pass
