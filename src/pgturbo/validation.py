def validate_position_tuple(value):
    error_msg = ("Positions must be tuples or lists with two integer or float "
                 "values for the X and Y coordinates, e.g. (10, 25). You "
                 "used: ")
    try:
        x, y = value
    except TypeError:
        raise TypeError(error_msg + str(value))
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise TypeError(error_msg + str(value))


def validate_limit_tuple(value):
    if not (isinstance(value, (tuple, list)) and len(value) == 2
            and value[0] is None or isinstance(value[0], (int, float))
            and value[1] is None or isinstance(value[1], (int, float))):
        raise TypeError("Limits must be given as a tuple of two ints, "
                        "floats or None, not {}.".format(value))
