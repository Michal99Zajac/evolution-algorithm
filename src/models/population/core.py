from abc import ABC, abstractmethod
from typing import TypeVar, Type, List
import random

from models.chromosome import BinaryChromosome
from processes.crossover.core import Crossover, CrossoverFactory
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
        crossover: Crossover,
        selection: Selection,
    ):
        self._amount = amount
        self._crossover = crossover
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
        crossover: Crossover,
        selection: Selection,
    ):
        super().__init__(amount, SubjectCreator, crossover, selection)
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
        parents: List[BinarySubject] = self._selection.select(
            valuerSubjects
        )  # select parents
        self._subjects = parents  # assign to the next populaion

        # crossover
        while len(self._subjects) != self._amount:
            index_one = 0
            index_two = 0

            while index_one == index_two:
                index_one = random.randint(0, len(parents) - 1)
                index_two = random.randint(0, len(parents) - 1)

            offsprings = self._crossover.cross(parents[index_one], parents[index_two])
            # subjects amount is odd
            if len(self._subjects) + 1 == self._amount:
                self._subjects.append(offsprings[0])
                continue

            self._subjects.extend(offsprings)

        # mutation

    def run(self, epochs: int):
        for _ in range(epochs):
            self._evolve()

            print(
                list(
                    map(
                        lambda x: ValuerBinarySubject(x, -10, 10, schaffer_N4).value,
                        self._subjects,
                    )
                )
            )
            # the_bests = [
            #     ValuerBinarySubject(subject, -10, 10, schaffer_N4)
            #     for subject in self._subjects
            # ]
            # the_bests.sort(key=lambda x: x.value)
            # print(the_bests[0].value)
