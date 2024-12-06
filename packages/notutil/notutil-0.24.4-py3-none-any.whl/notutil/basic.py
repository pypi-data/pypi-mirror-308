from typing import Callable

class on_travel():
    def __init__(self, *target):
        self._list = target
    
    def __call__(self, func: Callable):
        def wrapper(start:int = 0):
            for i, (args) in enumerate(zip(*self._list), start):
                yield from func(i, *args)
        return wrapper