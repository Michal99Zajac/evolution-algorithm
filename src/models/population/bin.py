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

from .core import Population


class BinaryPopulation(Population):
    def __init__(
        self,
        amount: int,
        SubjectCreator: Type[BinarySubject],
        crossover: Crossover,
        mutation: Mutation,
        selection: Selection,
        inversion: Inversion,
    ):
        super().__init__(amount, SubjectCreator, crossover, mutation, selection)
        self._SubjectCreator = SubjectCreator
        self._inversion = inversion

    def _generate(self):
        chromosome_lenght = BinaryChromosome.chromosome_lenght(6, -1000, 1000)
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
            ValuerBinarySubject(subject, -1000, 1000, schaffer_N4)
            for subject in self._subjects
        ]
        parents: List[BinarySubject] = self._selection.select(valuerSubjects)
        self._subjects = parents  # assign to the next populaion

        # crossover
        while len(self._subjects) != self._amount:
            index_one, index_two = two_index(len(parents) - 1)
            offsprings = self._crossover.cross(parents[index_one], parents[index_two])

            if not offsprings:
                continue

            # subjects amount is odd
            if len(self._subjects) + 1 == self._amount:
                self._subjects.append(offsprings[0])
                continue

            self._subjects.extend(offsprings)

        # mutation
        for subject in self._subjects:
            self._mutation.mutate(subject)

        # inversion
        for subject in self._subjects:
            self._inversion.inverse(subject)

    def run(self, epochs: int):
        evolution = [
            {
                "epoch": 0,
                "value": self._pick_the_best_value(
                    [
                        ValuerBinarySubject(subject, -1000, 1000, schaffer_N4)
                        for subject in self._subjects
                    ]
                ),
            }
        ]

        for epoch in range(1, epochs):
            self._evolve()

            # set the data
            evolution.append(
                {
                    "epoch": epoch,
                    "value": self._pick_the_best_value(
                        [
                            ValuerBinarySubject(subject, -1000, 1000, schaffer_N4)
                            for subject in self._subjects
                        ]
                    ),
                }
            )

        return evolution
