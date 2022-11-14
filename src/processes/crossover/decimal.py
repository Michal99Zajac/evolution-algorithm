from models.subject.decimal import X2__DecimalSubject
from models.chromosome.decimal import DecimalChromosome

from .core import Crossover


class DecimalCrossover(Crossover):
    def __init__(self, probability: float, left_limit: float, right_limit: float):
        super().__init__(probability)
        self._left_limit = left_limit
        self._right_limit = right_limit


class ArithmeticCrossover(DecimalCrossover):
    def __init__(
        self, probability: float, k: float, left_limit: float, right_limit: float
    ):
        super().__init__(probability, left_limit, right_limit)
        self._k = k

    @Crossover.checker
    def cross(self, parent_A: X2__DecimalSubject, parent_B: X2__DecimalSubject):
        [x1, y1] = parent_A.chromosomes
        [x2, y2] = parent_B.chromosomes

        x1__new = DecimalChromosome(self._k * x1.value + (1 - self._k) * x2.value)
        y1__new = DecimalChromosome(self._k * y1.value + (1 - self._k) * y2.value)
        x2__new = DecimalChromosome((1 - self._k) * x1.value + self._k * x2.value)
        y2__new = DecimalChromosome((1 - self._k) * y1.value + self._k * y2.value)

        return [
            X2__DecimalSubject([x1__new, y1__new]),
            X2__DecimalSubject([x2__new, y2__new]),
        ]
