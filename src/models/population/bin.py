from typing import Type, List

from models.chromosome import BinaryChromosome
from models.subject import BinarySubject
from models.subject.decorators import ValuerBinarySubject
from utils.two_index import two_index
from processes.inversion import Inversion

from .core import Population, Props, Config


class BinaryProps(Props):
    inversion: Inversion


class BinaryPopulation(Population):
    _SubjectCreator: Type[BinarySubject]

    def __init__(self, props: BinaryProps, config: Config):
        super().__init__(props, config)
        self._inversion = props["inversion"]

    def _generate_valuers(self, subjects: List[BinarySubject]):
        return [
            ValuerBinarySubject(
                subject,
                self._config["left_limit"],
                self._config["right_limit"],
                self._config["fitness"],
            )
            for subject in subjects
        ]

    def _generate(self):
        chromosome_lenght = BinaryChromosome.chromosome_lenght(
            self._config["precision"],
            self._config["left_limit"],
            self._config["right_limit"],
        )
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
            ValuerBinarySubject(
                subject,
                self._config["left_limit"],
                self._config["right_limit"],
                self._config["fitness"],
            )
            for subject in self._subjects
        ]
        parents: List[BinarySubject] = self._selection.select(valuerSubjects)

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
        valuers = self._generate_valuers(self._subjects)
        the_best: ValuerBinarySubject = self._pick_the_best(valuers)
        evolution = [
            {
                "epoch": 0,
                "avg": self._avarage(valuers),
                "x": the_best.values,
                "value": the_best.value,
            }
        ]

        for epoch in range(1, epochs):
            self._evolve()

            valuers = self._generate_valuers(self._subjects)
            the_best: ValuerBinarySubject = self._pick_the_best(valuers)

            # set the data
            evolution.append(
                {
                    "epoch": epoch,
                    "x": the_best.values,
                    "avg": self._avarage(valuers),
                    "value": the_best.value,
                }
            )

        return evolution
