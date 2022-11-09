from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, TypeVar

from models.valuer import Valuer

Type = TypeVar("Type", "min", "max")


class Selection(ABC):
    _type: Type = "min"

    @abstractmethod
    def select(self, valuers: List[Valuer]):
        pass

    def __min_sorter(self, valuer: Valuer):
        return valuer.value

    def __max_sorter(self, valuer: Valuer):
        return -valuer.value

    def _sort(self, valuers: List[Valuer]):
        return sorted(
            valuers,
            key=self.__max_sorter if self._type == "max" else self.__min_sorter,
        )
