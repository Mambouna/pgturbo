def validate_position_tuple(value):
    error_msg = ("Positions must be tuples or lists with two integer or float "
                 "values for the X and Y coordinates, e.g. (10, 25). You "
                 "used: ")
    try:
        x, y = value
    except (TypeError, ValueError):
        raise TypeError(error_msg + str(value))
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise TypeError(error_msg + str(value))


def validate_limit_tuple(value):
    if not (isinstance(value, (tuple, list)) and len(value) == 2
            and value[0] is None or isinstance(value[0], (int, float))
            and value[1] is None or isinstance(value[1], (int, float))):
        raise TypeError("Limits must be given as a tuple of two ints, "
                        "floats or None, not {}.".format(value))

def validate_color_tuple(value):
    error_msg = ("Colors must be given either as a string name like 'red' or "
                 "as a tuple with three numbers between 0 and 255.")

    if not isinstance(value, tuple):
        raise TypeError(error_msg + " You gave a {}.".format(type(value)))
    try:
        a, b, c = value
        try:
            if not (0 <= a <= 255 and 0 <= b <= 255 and 0 <= c <= 255):
                raise TypeError(error_msg + " You had values outside of 0 to"
                                "255.")
        except:
            raise TypeError(error_msg + " You had non number values in the "
                            "tuple.")
    except:
        raise TypeError(error_msg + " Given tuple has {}.".format(len(value)))
