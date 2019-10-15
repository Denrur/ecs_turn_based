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


def debug_info(Cls):
    # todo : make a valid debug decorator
    class NewCls(object):
        def __init__(self, *args, **kwargs):
            self.oInstance = Cls(*args, **kwargs)

        def __getattribute__(self, s):
            """
            this is called whenever any attribute of a NewCls object is accessed. This function first tries to
            get the attribute off NewCls. If it fails then it tries to fetch the attribute from self.oInstance (an
            instance of the decorated class). If it manages to fetch the attribute from self.oInstance, and
            the attribute is an instance method then `time_this` is applied.
            """
            try:
                x = super(NewCls, self).__getattribute__(s)
            except AttributeError:
                pass
            else:
                return x

    return NewCls
