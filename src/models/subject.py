from __future__ import annotations
from abc import ABC, abstractmethod

from models.chromosome import BinaryChromosome

class Subject(ABC):
    def  __init__(self,  *args: BinaryChromosome):
        self.__chromosomes = list(args)

    @property
    def chromosomes(self):
        return self.__chromosomes

    @abstractmethod
    def inverse(self):
        pass

    @abstractmethod
    def mutate(self):
        pass

class X2FunctionSubject(Subject):
    def __init__(self, *args: BinaryChromosome):
        if len(args) != 2:
            raise Exception("Error: constructor didn't get two chromosmes")
        super().__init__(*args)

    def inverse(self, left: int, right: int):
        for chromosome in self.chromosomes:
            chromosome.inverse(left=left, right=right)

    def mutate(self, *args: int):
        for chromosome in self.chromosomes:
            chromosome.mutate(args)
