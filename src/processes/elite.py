from typing import List, Callable, Union
import math

from models.valuer import Valuer


class Eliter:
    def __init__(self, percentage: float, type: str):
        if percentage > 1 or percentage < 0:
            raise Exception("Error: percentage have to be float number between 0 and 1")
        self._percentage = percentage
        self._type = type

    def keep(self, valuers: List[Valuer]):
        to_keep = math.ceil(len(valuers) * self._percentage)
        return self.__sort(valuers)[0:to_keep]

    def __sort(self, valuers: List[Valuer]):
        sorter: Union[None, Callable[[Valuer], float]] = None

        if self._type == "min":
            sorter = lambda valuer: valuer.value
        else:
            sorter = lambda valuer: -valuer.value

        return sorted(valuers, key=sorter)
