# coding: utf8

import time


def compute_time():
    """
    Control time taken by a function to execute
    """

    def decorator(function):

        def modified_function(*unnamed, **named):
            tps_before = time.time()  # before executing function
            res = function(*unnamed, **named)
            tps_after = time.time()  # after executing function
            print("Function {0} took {1} to execute".format(
                        function, tps_after - tps_before))
            return res

        return modified_function

    return decorator


def control_type(*a_args, **a_kwargs):
    """
    Control type of arguments
    """

    def decorator(function):

        def modified_function(*args, **kwargs):
            # required parameters list (a_args) has to be same length as
            # received parameters list (args)
            if len(a_args) != len(args):
                raise TypeError("Number of required parameters different to "
                                "received number")

            # Unnamed arguments
            for i, arg in enumerate(args):
                if not isinstance(a_args[i], type(args[i])):
                    raise TypeError("Argument {0} is not of type "
                                    "{1}".format(i, a_args[i]))

            # Named arguments
            for key in kwargs:
                if key not in a_kwargs:
                    raise TypeError("Argument {0} has no specified "
                                    "type".format(repr(key)))
                if not isinstance(a_kwargs[key], type(kwargs[key])):
                    raise TypeError("Argument {0} is not of type "
                                    "{1}".format(repr(key), a_kwargs[key]))
            return function(*args, **kwargs)

        return modified_function

    return decorator
