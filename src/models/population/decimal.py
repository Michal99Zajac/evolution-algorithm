from typing import List
import time

from models.chromosome.decimal import DecimalChromosome
from models.subject.decimal import X2__DecimalSubject
from models.subject.decorators import ValuerDecimalSubject
from utils.two_index import two_index

from .core import Population, Props, Config


class DecimalPopulation(Population):
    def __init__(self, props: Props, config: Config):
        super().__init__(props, config)

    def _generate_valuers(self, subjects: List[X2__DecimalSubject]):
        return [
            ValuerDecimalSubject(
                subject,
                self._config["left_limit"],
                self._config["right_limit"],
                self._config["fitness"],
            )
            for subject in subjects
        ]

    def _generate(self):
        self._subjects = [
            X2__DecimalSubject(
                [
                    DecimalChromosome.generate(
                        self._config["left_limit"], self._config["right_limit"]
                    )
                    for _ in range(X2__DecimalSubject.chromosome_number)
                ]
            )
            for _ in range(self._amount)
        ]

    def _evolve(self):
        # selection
        valuerSubjects = self._generate_valuers(self._subjects)
        parents: List[X2__DecimalSubject] = self._selection.select(valuerSubjects)

        if len(parents) < 2:
            raise Exception("Error: selected less then 2 parents")

        # clear subjects (offsprings)
        self._subjects = []

        # keep the best
        kept: List[X2__DecimalSubject] = self._eliter.keep(valuerSubjects)

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

        # add kept subjects
        self._subjects.extend(kept)

    def run(self, epochs: int):
        start_time = time.time()
        valuers = self._generate_valuers(self._subjects)
        the_best: ValuerDecimalSubject = self._pick_the_best(valuers)
        average, standard_deviation = self._average(valuers)
        evolution = [
            {
                "epoch": 0,
                "average": average,
                "x": the_best.values,
                "value": the_best.value,
                "standard_deviation": standard_deviation,
            }
        ]

        for epoch in range(1, epochs):
            self._evolve()

            valuers = self._generate_valuers(self._subjects)
            the_best: ValuerDecimalSubject = self._pick_the_best(valuers)

            # set the data
            average, standard_deviation = self._average(valuers)
            evolution.append(
                {
                    "epoch": epoch,
                    "x": the_best.values,
                    "average": average,
                    "value": the_best.value,
                    "standard_deviation": standard_deviation,
                }
            )

        end_time = time.time()

        return {
            "evolution": evolution,
            "time": end_time - start_time,
            "best": {"value": the_best.value, "x": the_best.values},
        }
