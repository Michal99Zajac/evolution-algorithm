from __future__ import annotations
import random
from abc import ABC, abstractmethod
from typing import Callable, TypeVar

from models.chromosome import BinaryChromosome

TMutation = TypeVar("TMutation", bound="Mutation")
T = TypeVar("T", BinaryChromosome, any)


class Mutation(ABC):
    def __init__(self, probability: float):
        if probability > 1:
            raise Exception("Error: probability can't be bigger then 100%")
        self.__probability = probability

    def checker(function: Callable[[TMutation, T], T]):
        def mutate(self: TMutation, chromosome: T):
            if self.__probability >= random.random():
                return function(self, chromosome)
            return chromosome

        return mutate

    @checker
    @abstractmethod
    def mutate(self, chromosome: T):
        pass
