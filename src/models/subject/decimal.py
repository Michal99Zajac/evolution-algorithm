from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

from models.chromosome.decimal import DecimalChromosome


class DecimalSubject:
    chromosome_number = 1

    def __init__(self, chromosomes: List[DecimalChromosome]):
        if len(chromosomes) == 0:
            raise Exception("Error: Subject has to have at least on chromosome")

        self._chromosomes = chromosomes

    @property
    def chromosomes(self):
        return self._chromosomes

    def mutate(self, *values: float):
        if len(values) != len(self._chromosomes):
            raise Exception("Error: too few or too much values were provided")

        for index, chromosome in enumerate(self._chromosomes):
            chromosome.mutate(values[index])


class X2__DecimalSubject(DecimalSubject):
    chromosome_number = 2

    def __init__(self, chromosomes: List[DecimalChromosome]):
        if len(chromosomes) != self.chromosome_number:
            raise Exception("Error: constructor didn't get two chromosomes")
        super().__init__(chromosomes)
