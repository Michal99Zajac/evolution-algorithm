from abc import ABC, abstractmethod
from typing import TypeVar, Type

from models.chromosome import BinaryChromosome
from processes.crossover.core import CrossoverFactory
from models.subject import BinarySubject
from processes.selection.core import Selection
from models.subject.decorators import ValuerBinarySubject
from fitness.schaffer_N4 import schaffer_N4

C = TypeVar("C")


class Population(ABC):
    def __init__(
        self,
        amount: int,
        SubjectCreator: Type[C],
        crossover_factory: CrossoverFactory,
        selection: Selection,
    ):
        self._amount = amount
        self._crossover_factory = crossover_factory
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


class BinaryPopulation(Population):
    def __init__(
        self,
        amount: int,
        SubjectCreator: Type[BinarySubject],
        crossover_factory: CrossoverFactory,
        selection: Selection,
    ):
        super().__init__(amount, SubjectCreator, crossover_factory, selection)
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
        # selection
        valuerSubjects = [
            ValuerBinarySubject(subject, -10, 10, schaffer_N4)
            for subject in self._subjects
        ]
        selected = self._selection.select(valuerSubjects)

        print(selected)

    def run(self, epochs: int):
        for _ in range(epochs):
            self._evolve()
