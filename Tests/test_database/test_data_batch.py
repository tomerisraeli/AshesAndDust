import unittest

import numpy as np

from DataBase.DataBaseDataTypes.data_base_coordinate import DataBaseCoordinate
from DataBase.DataBaseDataTypes.data_base_data_batch import DataBatch
from DataBase.DataBaseDataTypes.data_base_data_range import DataRange
from DataBase.DataBaseDataTypes.data_base_variable import DataBaseVariable


class TestDataBatch(unittest.TestCase):
    var = DataBaseVariable(name="test_var", var_type=np.float32, units="units", full_name="test var", dimensions=())

    def test_insert_data(self):
        batch = DataBatch(TestDataBatch.var)

        test_data = [(DataBaseCoordinate(i, 2 * 1, i), i) for i in range(10)]
        for coord, val in test_data:
            batch.insert(coord, val)

        for coord, val in test_data:
            self.assertEqual(batch[coord], val, "value is incorrect")

    def test_load_data(self):
        # this test assumes that the min value of all dimensions is 0
        res = 0.5
        batch = DataBatch(TestDataBatch.var)

        test_data = [(DataBaseCoordinate(i, res * i, i), i) for i in range(20)]
        for coord, val in test_data:
            batch.insert(coord, val)
        data_range = DataRange(
            (0, 20),
            (0, 20),
            (0, 20)
        )
        data_loaded, _ = batch.get(res, res, res, data_range)

        for coord, val in test_data:
            self.assertEqual(
                data_loaded[int(coord.time/res)][int(coord.lat/res)][int(coord.lon/res)],
                val
                , f"value is incorrect at ({coord.time}, {coord.lat}, {coord.lon})")

