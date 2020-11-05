#! /usr/bin/python3.8

"""Common profiler tool, useful to compare results of 2 or more similar function with different implementation"""
import typing
from timeit import timeit
import cProfile, pstats
from io import StringIO
from types import FunctionType
from prettytable import PrettyTable

from prettytable import PrettyTable

printout = PrettyTable()
printout.field_names = ["Function", "Timeit", "Profile"]
printout.align = "l"


def _timeit(func, *args, **kwargs) -> float:
    """ timeit wrapper

    :param func: function to run
    :param args:
    :param kwargs:
    :return: execution time
    """

    def _wrapper(func, *args, **kwargs):
        def _wrapped():
            return func(*args, **kwargs)

        return _wrapped

    return timeit(_wrapper(func, *args, **kwargs))


def _profile(func: typing.Callable, numruns: int, *args, **kwargs) -> str:
    """ Run profile
    :param func: function to test
    :param numruns: number of runs to perform
    :param args: arguments
    :param kwargs: kw arguments
    :return: result
    """
    pr = cProfile.Profile()
    pr.enable()
    for _ in range(numruns):
        func(*args, **kwargs)
    pr.disable()
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats()
    return s.getvalue()


def fprofile(funclist: tuple, numruns=10000, *args, **kwargs):
    """ Print out profiling results
    :param funclist: list of function to test
    :param numruns: number of runs to perform
    :param args: arguments
    :param kwargs: kw arguments
    :return: None
    """
    for func in funclist:
        printout.add_row([func.__name__, _timeit(func, *args, **kwargs), _profile(func, numruns, *args, **kwargs)])
    print(printout)


if __name__ == "__main__":
    import numpy as np


    def _a(nparr):
        sum = 0
        for n in nparr:
            sum += n
        return sum


    def _b(nparr):
        return nparr.sum()


    arr = np.random.rand(1, 10) * 100
    fprofile((_a, _b), nparr=arr)
