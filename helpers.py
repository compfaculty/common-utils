import builtins
from collections import ChainMap


def print_locals_globals_builtins():
    """ Print env variables using ChainMap

    :return: None
    """
    pylookup = ChainMap(locals(), globals(), vars(builtins))
    for k, v in pylookup.items():
        print(f"KEY: {k}, VALUE: {v}")


def find_in_locals_globals_builtins(key, localz, globalz):
    """ Find env variable in locals, globals, builtin

    :param localz: locals dict
    :param globalz: globals dict
    :param key: key to search
    :return: value or None
    """
    pylookup = ChainMap(localz, globalz, vars(builtins))
    return pylookup.get(key, None)
