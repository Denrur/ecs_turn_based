from functools import wraps
from bearlibterminal import terminal as blt
from time import time


def open_in_blt(fn):
    @wraps(fn)
    def open_blt_terminal(*args, **kwargs):
        # print('Open blt')
        blt.open()
        blt.composition(True)
        # print('start game')

        fn(*args, **kwargs)
        blt.close()
    return open_blt_terminal


def refresh(fn):
    def wrapper_refresh(*args, **kwargs):
        blt.clear()
        fn(*args, **kwargs)
        blt.refresh()
    return wrapper_refresh


def benchmark(fn):
    @wraps(fn)
    def wrapper_bench(*args, **kwargs):
        start = time()
        res = fn(*args, **kwargs)
        print(fn.__name__, time() - start)
        return res
    return wrapper_bench
