from __future__ import annotations
import random
from abc import ABC, abstractmethod
from typing import Callable, TypeVar

TMutation = TypeVar("TMutation", bound="Mutation")

from models.chromosome import BinaryChromosome


class Mutation(ABC):
    def __init__(self, probability: float):
        if probability > 1:
            raise Exception("Error: probability can't be bigger then 100%")
        self.__probability = probability

    def checker(function: Callable[[TMutation, BinaryChromosome], BinaryChromosome]):
        def mutate(self: TMutation, chromosome: BinaryChromosome):
            if self.__probability >= random.random():
                return function(self, chromosome)
            return chromosome

        return mutate

    @checker
    @abstractmethod
    def mutate(self, chromosome: BinaryChromosome):
        pass


class EdgeMutation(Mutation):
    @Mutation.checker
    def mutate(self, chromosome: BinaryChromosome):
        index = 0 if random.random() < 0.5 else len(chromosome) - 1
        print(f"index: {index}")
        chromosome.mutate(index)
        return chromosome


class SinglePointMutation(Mutation):
    @Mutation.checker
    def mutate(self, chromosome: BinaryChromosome):
        index = random.randint(0, len(chromosome) - 1)
        chromosome.mutate(index)
        return chromosome


class TwoPointMutation(Mutation):
    @Mutation.checker
    def mutate(self, chromosome: BinaryChromosome):
        point1 = random.randint(0, len(chromosome) - 1)
        point2 = random.randint(point1, len(chromosome) - 1)
        chromosome.mutate(point1, point2)
        return chromosome
