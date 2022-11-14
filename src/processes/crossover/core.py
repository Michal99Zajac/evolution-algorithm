from __future__ import annotations
from typing import Type, TypeVar
from abc import ABC, abstractmethod
import random

from models.subject.bin import BinarySubject

T = TypeVar("T", BinarySubject, any)
TCrossover = TypeVar("TCrossover", bound="Crossover")


class CrossoverFactory(ABC):
    @abstractmethod
    def create_crossover(self, SubjectCreator: Type[T], probability: float):
        pass


class Crossover(ABC):
    def __init__(self, probability: float):
        if probability > 1 or probability < 0:
            raise Exception(
                "Error: probability can't be bigger then 100% and smaller then 0%"
            )
        self._probability = probability

    def checker(function):
        def cross(self: TCrossover, parent_A: T, parent_B: T):
            if self._probability >= random.random():
                return function(self, parent_A, parent_B)
            return None

        return cross

    @abstractmethod
    def cross(self, parent_A: T, parent_B: T):
        pass
