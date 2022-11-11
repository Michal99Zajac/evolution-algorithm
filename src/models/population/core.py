from abc import ABC, abstractmethod
from typing import TypeVar, Type, List
import random

from models.chromosome import BinaryChromosome
from processes.crossover.core import Crossover
from models.subject import BinarySubject
from processes.selection.core import Selection
from models.subject.decorators import ValuerBinarySubject
from fitness.schaffer_N4 import schaffer_N4
from processes.mutation.core import Mutation
from utils.two_index import two_index
from processes.inversion import Inversion

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

    @abstractmethod
    def _generate(self):
        pass

    @abstractmethod
    def _evolve(self):
        pass

    @abstractmethod
    def run(self, epochs: int):
        pass
