from math import ceil, log2
import random
from typing import List

class Chromosome:
    _gens: List[bool] = []

    def __init__(self, length: int):
        self.__generate(length)

    def __len__(self):
        return len(self._gens)

    def __str__(self):
        return ''.join(map(lambda gen: '1' if gen else '0', self._gens))

    def inverse(self, left: int, right: int):
        inversed_subgens = reversed(self._gens[left:right])
        self._gens[left:right] = inversed_subgens

    @property
    def gens(self):
        return self._gens

    @gens.setter
    def gens(self, new_gens: List[bool]):
        self.gens = new_gens

    def __generate(self, lenght: int):
        self._gens = [bool(random.getrandbits(1)) for _ in range(lenght)]

    @staticmethod
    def chromosome_lenght(precision: int, left_border: float, right_border: float):
        return ceil(log2((right_border - left_border) * 10 ** precision) + log2(1))
