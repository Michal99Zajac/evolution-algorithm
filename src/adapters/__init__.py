from typing import List, Callable
from abc import ABC, abstractmethod
from models.chromosome import BinaryChromosome

from models.subject import X2Subject

class Valuer(ABC):
    @property
    @abstractmethod
    def value(self) -> float:
        pass

class X2SubjectAdapter(X2Subject, Valuer):
    def __init__(self, chromosomes: List[BinaryChromosome], length: int, left_limit: float, right_limit: float, fitness: Callable[[float, float], float]):
        super().__init__(chromosomes, length)
        indicators = [self.__transform(chromosome, left_limit, right_limit) for chromosome in chromosomes]
        self.__value: float = fitness(*indicators)

    @property
    def value(self):
        return self.__value

    def __transform(self, chromosome: BinaryChromosome, left_limit: float, right_limit: float):
        return left_limit + int(str(chromosome), 2) * (right_limit - left_limit) / (2**len(self) - 1)
