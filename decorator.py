from typing import Callable
from ansii import colorize
import time


def try_it(func: Callable) -> Callable:
    def wrapper(self, *args, **kwargs):

        start = time.perf_counter()
        func_n = colorize(func.__name__, 'YELLOW')

        print(
            f"trying to compile given {func_n} function with \nargs:{colorize(args, 'blue')}\nand\nkwargs:{colorize(kwargs, "blue")}")

        try:
            result = func(self, *args, **kwargs)
            end = time.perf_counter()
            print(f'{func_n} is compiled in {end-start:.4f}')
            return result
        except Exception as e:
            print(f'error in \n{colorize(f'{func_n}\n{e}', 'red')}')
            raise
    return wrapper
