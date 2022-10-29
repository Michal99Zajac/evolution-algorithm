from __future__ import annotations
import random
from abc import ABC, abstractmethod
from typing import Callable
from typing import TypeVar

TMutation = TypeVar("TMutation", bound="Mutation")

from models.Chromosome import Chromosome

class Mutation(ABC):
    def __init__(self, probability: float):
        if probability > 1: raise Exception('Error: probability can\'t be bigger then 100%')
        self.__probability = probability

    def checker(function: Callable[[TMutation, Chromosome], Chromosome]):
        def mutate(self: TMutation, chromosome: Chromosome):
            if self.__probability >= random.random():
                return function(self, chromosome)
            return chromosome

        return mutate

    @checker
    @abstractmethod
    def mutate(self, chromosome: Chromosome):
        pass

class EdgeMutation(Mutation):
    @Mutation.checker
    def mutate(self, chromosome: Chromosome):
        index = 0 if random.random() < 0.5 else len(chromosome) - 1
        chromosome.mutate(index)
