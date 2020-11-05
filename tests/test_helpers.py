import pytest

from helpers import find_in_locals_globals_builtins

VAR = 1


def test_find_in_locals_globals_builtins():
    a = "test"
    assert find_in_locals_globals_builtins("a", locals(), globals()) == "test"
    assert find_in_locals_globals_builtins("VAR", locals(), globals()) == 1
