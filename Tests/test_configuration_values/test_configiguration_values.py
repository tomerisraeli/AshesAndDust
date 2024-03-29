import os
import unittest
from copy import copy

from support.configuration_values import ConfigurationValues

file_path = "test.ini"


class TestConfigurationValues(unittest.TestCase):

    def test_create_new_file(self):
        # we first make sure the file really is missing
        if os.path.isfile(file_path):
            os.remove(file_path)

        # create a new __config file
        _ = ConfigurationValues(file_path)

        self.assertTrue(os.path.isfile(file_path), "the file is missing")

    def test_get_value_from_missing_section(self):
        default = "DEFAULT"

        # create a new __config file
        config = ConfigurationValues(file_path)
        self.assertEqual(
            config.get_key({"section": "missing section", "key": "key", "default": default}),
            default,
            "value from missing section didnt yield the default value"
        )

    def test_get_value_from_missing_key(self):
        default = "DEFAULT"

        # create a new __config file
        config = ConfigurationValues(file_path)
        invalid_key = copy(ConfigurationValues.Keys.data_base_path)  # taking a random valid key
        invalid_key["key"] = "missing key"
        invalid_key["default"] = default

        self.assertEqual(
            config.get_key(invalid_key),
            default,
            "value from missing key didnt yield the default value"
        )

    def test_getting_a_value_other_than_default(self):
        wrong_value = "this is the wrong value"

        # create a new __config file
        config = ConfigurationValues(file_path)
        valid_key = copy(ConfigurationValues.Keys.data_base_path)  # taking a random valid key
        valid_key["default"] = wrong_value

        self.assertNotEqual(
            config.get_key(valid_key),
            wrong_value,
            "an existing key returned the default value with no reason"
        )

    def test_wrong_format_key(self):
        # create a new __config file
        config = ConfigurationValues(file_path)
        try:
            config.get_key({})
            self.fail("program didnt failed when entering key with missing values")
        except Exception as e:
            self.assertIsInstance(
                e,
                KeyError,
                "program failed with wrong exception"
            )


if __name__ == '__main__':
    unittest.main()
