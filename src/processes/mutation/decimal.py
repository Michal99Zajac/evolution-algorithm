import random
from enum import Enum
import numpy as np

from models.subject.decimal import DecimalSubject
from processes.mutation.core import Mutation


class BinMutation(Enum):
    UNIFORM = "UNIFORM"
    GAUSS = "GAUSS"


class DecimalMuatation(Mutation):
    def __init__(self, probability: float, left_limit: float, right_limit: float):
        super().__init__(probability)
        self._left_limit = left_limit
        self._right_limit = right_limit

    def mutate(self, subject: DecimalSubject):
        return super().mutate(subject)

    def _is_overflow(self, value: float):
        return False if self._left_limit <= value <= self._right_limit else True


class UniformMutation(DecimalMuatation):
    @Mutation.checker
    def mutate(self, subject: DecimalSubject):
        new_value = random.uniform(self._left_limit, self._right_limit)

        while self._is_overflow(new_value):
            new_value = random.uniform(self._left_limit, self._right_limit)

        index = random.randint(0, len(subject.chromosome_number) - 1)
        subject.chromosomes[index].mutate(new_value)
        return subject


class GaussMutation(DecimalMuatation):
    @Mutation.checker
    def mutate(self, subject: DecimalSubject):
        [chromosome_x, chromosome_y] = subject.chromosomes

        saved_x_value = chromosome_x.value
        saved_y_value = chromosome_y.value

        chromosome_x.mutate(saved_x_value + np.random.normal(0, 1))
        chromosome_y.mutate(saved_y_value + np.random.normal(0, 1))

        while self._is_overflow(chromosome_x.value) or self._is_overflow(
            chromosome_y.value
        ):
            chromosome_x.mutate(saved_x_value + np.random.normal(0, 1))
            chromosome_y.mutate(saved_y_value + np.random.normal(0, 1))

        return subject
