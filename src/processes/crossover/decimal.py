from typing import List
import random

from models.subject.decimal import X2__DecimalSubject
from models.chromosome.decimal import DecimalChromosome

from .core import Crossover


class DecimalCrossover(Crossover):
    def __init__(
        self,
        probability: float,
        left_limit: float = -10,
        right_limit: float = 10,
        k: float = 0.5,
        alpha: float = 0.25,
        beta: float = 0.5,
        fitness=None,
        type="min",
    ):
        super().__init__(probability)
        self._left_limit = left_limit
        self._right_limit = right_limit
        self._k = k
        self._alpha = alpha
        self._beta = beta
        self._fitness = fitness
        self._type = type

    def _estimate(self, subject: X2__DecimalSubject):
        return self._fitness(*[chromosome.value for chromosome in subject.chromosomes])

    def _check_overflow(self, subjects: List[X2__DecimalSubject]):
        def check(subject: X2__DecimalSubject):
            [x1, x2] = subject.chromosomes

            return not (self._left_limit <= x1.value <= self._right_limit) or not (
                self._left_limit <= x2.value <= self._right_limit
            )

        return any([check(subject) for subject in subjects])


class ArithmeticCrossover(DecimalCrossover):
    @Crossover.checker
    def cross(self, parent_A: X2__DecimalSubject, parent_B: X2__DecimalSubject):
        [x1, y1] = parent_A.chromosomes
        [x2, y2] = parent_B.chromosomes

        x1__new = DecimalChromosome(self._k * x1.value + (1 - self._k) * x2.value)
        y1__new = DecimalChromosome(self._k * y1.value + (1 - self._k) * y2.value)
        x2__new = DecimalChromosome((1 - self._k) * x1.value + self._k * x2.value)
        y2__new = DecimalChromosome((1 - self._k) * y1.value + self._k * y2.value)

        offsprings = [
            X2__DecimalSubject([x1__new, y1__new]),
            X2__DecimalSubject([x2__new, y2__new]),
        ]

        if self._check_overflow(offsprings):
            return None

        return offsprings


class LinearCrossover(DecimalCrossover):
    @Crossover.checker
    def cross(self, parent_A: X2__DecimalSubject, parent_B: X2__DecimalSubject):
        [x1, y1] = parent_A.chromosomes
        [x2, y2] = parent_B.chromosomes

        subject_Z = X2__DecimalSubject(
            [
                DecimalChromosome(0.5 * (x1.value + x2.value)),
                DecimalChromosome(0.5 * (y1.value + y2.value)),
            ]
        )
        subject_V = X2__DecimalSubject(
            [
                DecimalChromosome(1.5 * x1.value - 0.5 * x2.value),
                DecimalChromosome(1.5 * y1.value - 0.5 * y2.value),
            ]
        )
        subject_W = X2__DecimalSubject(
            [
                DecimalChromosome(-0.5 * x1.value + 1.5 * x2.value),
                DecimalChromosome(-0.5 * y1.value + 1.5 * y2.value),
            ]
        )
        raw_offsprings = [subject_Z, subject_V, subject_W]

        if self._check_overflow(raw_offsprings):
            return None

        min_sorter = lambda subject: self._estimate(subject)
        max_sorter = lambda subject: -self._estimate(subject)
        offsprings = sorted(
            raw_offsprings, key=min_sorter if self._type == "min" else max_sorter
        )[0:2]

        return offsprings


class BlendCrossoverAlpha(DecimalCrossover):
    @Crossover.checker
    def cross(self, parent_A: X2__DecimalSubject, parent_B: X2__DecimalSubject):
        [x1, y1] = parent_A.chromosomes
        [x2, y2] = parent_B.chromosomes

        d1 = abs(x1.value - x2.value)
        d2 = abs(y1.value - y2.value)

        x__new_lb = min([x1.value, x2.value]) - self._alpha * d1
        x__new_rb = max([x1.value, x2.value]) + self._alpha * d1
        y__new_lb = min([y1.value, y2.value]) - self._alpha * d2
        y__new_rb = max([y1.value, y2.value]) + self._alpha * d2

        offsprings = [
            X2__DecimalSubject(
                [
                    DecimalChromosome(random.uniform(x__new_lb, x__new_rb)),
                    DecimalChromosome(random.uniform(y__new_lb, y__new_rb)),
                ]
            ),
            X2__DecimalSubject(
                [
                    DecimalChromosome(random.uniform(x__new_lb, x__new_rb)),
                    DecimalChromosome(random.uniform(y__new_lb, y__new_rb)),
                ]
            ),
        ]

        if self._check_overflow(offsprings):
            return None

        return offsprings


class BlendCrossoverAlphaBeta(DecimalCrossover):
    @Crossover.checker
    def cross(self, parent_A: X2__DecimalSubject, parent_B: X2__DecimalSubject):
        [x1, y1] = parent_A.chromosomes
        [x2, y2] = parent_B.chromosomes

        d1 = abs(x1.value - x2.value)
        d2 = abs(y1.value - y2.value)

        x__new_lb = min([x1.value, x2.value]) - self._alpha * d1
        x__new_rb = max([x1.value, x2.value]) + self._alpha * d1
        y__new_lb = min([y1.value, y2.value]) - self._beta * d2
        y__new_rb = max([y1.value, y2.value]) + self._beta * d2

        offsprings = [
            X2__DecimalSubject(
                [
                    DecimalChromosome(random.uniform(x__new_lb, x__new_rb)),
                    DecimalChromosome(random.uniform(y__new_lb, y__new_rb)),
                ]
            ),
            X2__DecimalSubject(
                [
                    DecimalChromosome(random.uniform(x__new_lb, x__new_rb)),
                    DecimalChromosome(random.uniform(y__new_lb, y__new_rb)),
                ]
            ),
        ]

        if self._check_overflow(offsprings):
            return None

        return offsprings


class AveragingCrossover(DecimalCrossover):
    @Crossover.checker
    def cross(self, parent_A: X2__DecimalSubject, parent_B: X2__DecimalSubject):
        [x1, y1] = parent_A.chromosomes
        [x2, y2] = parent_B.chromosomes

        x__new = DecimalChromosome((x1.value + x2.value) / 2)
        y__new = DecimalChromosome((y1.value + y2.value) / 2)

        offsprings = [
            X2__DecimalSubject(
                [
                    x__new,
                    y__new,
                ]
            )
        ]

        if self._check_overflow(offsprings):
            return None

        return offsprings
