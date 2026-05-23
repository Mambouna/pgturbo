def validate_position_value(value):
    error_msg = ("Positions must be tuples or lists with two integer or float "
                 "values for the X and Y coordinates, e.g. (10, 25). You "
                 "used: ")
    try:
        x, y = value
    except TypeError:
        raise TypeError(error_msg + str(value))
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise TypeError(error_msg + str(value))
