def discrete_approximation(res, reference, value):
    """
    get a discrete approximation ot the given value relative to the reference with the given res
    :param res: the resumption of the approximation
    :param reference: the reference value
    :param value: the value to approximate
    :return: the calculated approximation
    """

    return round((reference - value) / res) * res + reference


def discrete_approximation_up(res, reference, value):
    """
    get a discrete approximation ot the given value relative to the reference with the given res.
    the returned value is bigger or equal to the original
    :param res: the resumption of the approximation
    :param reference: the reference value
    :param value: the value to approximate
    :return: the calculated approximation
    """

    return (int((reference - value) / res) + 1) * res + reference


def round2res(value, resolution):
    """
    round the given value  mult of the resolution
    :param value:
    :param resolution:
    :return:
    """

    return round(value / resolution) * resolution


def index_approximation(base_value, resolution, value):
    """
    get the matching index of the given value
    :param base_value: the value of index 0
    :param resolution: the dist between two indices
    :param value:
    :return:
    """

    if value < base_value:
        return None

    return int((value - base_value) / resolution)
