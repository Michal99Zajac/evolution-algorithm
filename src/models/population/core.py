from abc import ABC, abstractmethod
from typing import TypeVar, Type, List

from processes.crossover.core import Crossover
from processes.selection.core import Selection
from processes.mutation.core import Mutation
from models.valuer import Valuer

C = TypeVar("C")


class Population(ABC):
    def __init__(
        self,
        amount: int,
        SubjectCreator: Type[C],
        crossover: Crossover,
        mutation: Mutation,
        selection: Selection,
    ):
        self._amount = amount
        self._crossover = crossover
        self._mutation = mutation
        self._SubjectCreator = SubjectCreator
        self._selection = selection

        # generate init population
        self._generate()

    def _pick_the_best_value(self, valuers: List[Valuer]):
        return sorted(valuers, key=lambda valuer: valuer.value)[0].value

    @abstractmethod
    def _generate(self):
        pass

    @abstractmethod
    def _evolve(self):
        pass

    @abstractmethod
    def run(self, epochs: int):
        pass
