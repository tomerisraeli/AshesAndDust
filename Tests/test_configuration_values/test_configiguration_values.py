import os
from copy import copy

from support.configuration_values import ConfigurationValues

file_path = "test.ini"


def test_create_new_file():
    # we first make sure the file really is missing
    if os.path.isfile(file_path):
        os.remove(file_path)

    # create a new config file
    _ = ConfigurationValues(file_path)

    assert os.path.isfile(file_path) is True, "the file is missing"


def test_get_value_from_missing_section():
    default = "DEFAULT"

    # create a new config file
    config = ConfigurationValues(file_path)
    assert config.get_key({"section": "missing section", "key": "key", "default": default}) == default, \
        "value from missing section didnt yield the default value"


def test_get_value_from_missing_key():
    default = "DEFAULT"

    # create a new config file
    config = ConfigurationValues(file_path)
    invalid_key = copy(ConfigurationValues.Keys.data_base_path)  # taking a random valid key
    invalid_key["key"] = "missing key"
    invalid_key["default"] = default

    assert config.get_key(invalid_key) == default, "value from missing key didnt yield the default value"


def test_getting_a_value_other_than_default():
    wrong_value = "this is the wrong value"

    # create a new config file
    config = ConfigurationValues(file_path)
    valid_key = copy(ConfigurationValues.Keys.data_base_path)  # taking a random valid key
    valid_key["default"] = wrong_value

    assert config.get_key(valid_key) != wrong_value, "an existing key returned the default value with no reason"

def test_wrong_format_key():
    # create a new config file
    config = ConfigurationValues(file_path)
    try:
        config.get_key({})
        assert False, "program didnt failed when entering key with missing values"
    except Exception as e:
        print(e)
        assert isinstance(e, KeyError), "program failed with wrong exception"


if __name__ == '__main__':
    test_create_new_file()
    test_get_value_from_missing_section()
    test_get_value_from_missing_key()
    test_getting_a_value_other_than_default()
    test_wrong_format_key()

    print("\n\npassed all tests")
