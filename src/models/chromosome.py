from __future__ import annotations
from math import ceil, log2
import random
from typing import List

class BinaryChromosome:
    _gens: List[bool] = []

    def __init__(self, gens: List[bool]):
        self._gens = gens

    def __len__(self):
        return len(self._gens)

    def __str__(self):
        return ''.join(map(lambda gen: '1' if gen else '0', self._gens))

    def mutate(self, *args: int):
        for index in args:
            self._gens[index] = not self._gens[index]

    def inverse(self, left: int, right: int):
        if left < 0 or right > len(self._gens):
            raise Exception("Error: left or right is out of range")

        inversed_subgens = reversed(self._gens[left:right])
        self._gens[left:right] = inversed_subgens

    @property
    def gens(self):
        return self._gens

    @gens.setter
    def gens(self, new_gens: List[bool]):
        self.gens = new_gens

    @staticmethod
    def generate(lenght: int):
        gens = [bool(random.getrandbits(1)) for _ in range(lenght)]
        return BinaryChromosome(gens)

    @staticmethod
    def chromosome_lenght(precision: int, left_border: float, right_border: float):
        return ceil(log2((right_border - left_border) * 10 ** precision) + log2(1))
