import random
from enum import Enum

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
