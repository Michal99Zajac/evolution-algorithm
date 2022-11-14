from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

from models.chromosome.bin import BinaryChromosome


class BinarySubject(ABC):
    chromosome_number = 0

    def __init__(self, chromosomes: List[BinaryChromosome], length: int):
        if len(chromosomes) == 0:
            raise Exception("Error: Subject has to have at least on chromosome")

        for chromosome in chromosomes:
            if length != len(chromosome):
                raise Exception("Error: chromosomes are not equal")

        self._length = length
        self._chromosomes = chromosomes

    def __len__(self):
        return self._length

    @property
    def chromosomes(self):
        return self._chromosomes

    @abstractmethod
    def inverse(self, left: int, right: int):
        pass

    @abstractmethod
    def mutate(self, *args: int):
        pass


class X2Subject(BinarySubject):
    chromosome_number = 2

    def __init__(self, chromosomes: List[BinaryChromosome], length: int):
        if len(chromosomes) != self.chromosome_number:
            raise Exception("Error: constructor didn't get two chromosomes")
        super().__init__(chromosomes, length)

    def inverse(self, left: int, right: int):
        for chromosome in self._chromosomes:
            chromosome.inverse(left=left, right=right)

    def mutate(self, *args: int):
        for chromosome in self._chromosomes:
            chromosome.mutate(*args)
