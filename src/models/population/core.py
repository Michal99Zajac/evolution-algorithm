from abc import ABC, abstractmethod
from typing import TypeVar, Type

from models.chromosome import BinaryChromosome
from processes.crossover.core import CrossoverFactory
from models.subject import BinarySubject

C = TypeVar("C")


class Population(ABC):
    def __init__(
        self,
        amount: int,
        SubjectCreator: Type[C],
        crossover_factory: CrossoverFactory,
    ):
        self._amount = amount
        self._crossover_factory = crossover_factory
        self._SubjectCreator = SubjectCreator
        self._subjects = []

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


class BinaryPopulation(Population):
    def __init__(
        self,
        amount: int,
        SubjectCreator: Type[BinarySubject],
        crossover_factory: CrossoverFactory,
    ):
        super().__init__(amount, SubjectCreator, crossover_factory)
        self._SubjectCreator = SubjectCreator

    def _generate(self):
        chromosome_lenght = BinaryChromosome.chromosome_lenght(6, -10, 10)
        self._subjects = [
            self._SubjectCreator(
                [
                    BinaryChromosome.generate(chromosome_lenght)
                    for _ in range(self._SubjectCreator.chromosome_number)
                ],
                length=chromosome_lenght,
            )
            for _ in range(self._amount)
        ]

    def _evolve(self):
        return super()._evolve()

    def run(self, epochs: int):
        print(self._subjects)
        print(epochs)
