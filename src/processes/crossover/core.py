from __future__ import annotations
from typing import Type, TypeVar
from abc import ABC, abstractmethod

from models.subject import BinarySubject

T = TypeVar("T", BinarySubject, any)


class CrossoverFactory(ABC):
    @abstractmethod
    def create_crossover(self, SubjectCreator: Type[T]):
        pass


class Crossover(ABC):
    @abstractmethod
    def cross(self, parent_A: T, parent_B: T):
        pass
