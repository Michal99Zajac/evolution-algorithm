from __future__ import annotations
from math import ceil, log2
import random


class DecimalChromosome:
    def __init__(self, value: float, left_limit: float, right_limit: float):
        self._value = value
        self._left_limit = left_limit
        self._right_limit = right_limit

    def mutate(self, value: float):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def gens(self, value: float):
        self._value = value

    @staticmethod
    def generate(left_limit: float, right_limit: float):
        value = random.uniform(left_limit, right_limit)
        return DecimalChromosome(value, left_limit, right_limit)
