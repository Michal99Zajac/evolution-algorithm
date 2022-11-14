from typing import Type, List
import time

from models.chromosome.bin import BinaryChromosome
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
        valuerSubjects = self._generate_valuers(self._subjects)
        parents: List[BinarySubject] = self._selection.select(valuerSubjects)

        if len(parents) < 2:
            raise Exception("Error: selected less then 2 parents")

        # clear subjects (offsprings)
        self._subjects = []

        # keep the best
        kept: List[BinarySubject] = self._eliter.keep(valuerSubjects)

        # crossover
        # subtract kept subjects
        while len(self._subjects) - len(kept) < self._amount:
            index_one, index_two = two_index(len(parents) - 1)
            offsprings = self._crossover.cross(parents[index_one], parents[index_two])

            if not offsprings:
                continue

            self._subjects.extend(offsprings)

        # cut unnecessary offsprings
        self._subjects = self._subjects[0 : self._amount - len(kept)]

        # mutation
        for subject in self._subjects:
            self._mutation.mutate(subject)

        # inversion
        for subject in self._subjects:
            self._inversion.inverse(subject)

        # add kept subjects
        self._subjects.extend(kept)

    def run(self, epochs: int):
        start_time = time.time()
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

        end_time = time.time()

        return {
            "evolution": evolution,
            "time": end_time - start_time,
            "best": {"value": the_best.value, "xx": the_best.values},
        }
