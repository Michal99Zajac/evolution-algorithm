from enum import Enum
from typing import Type
from models.subject import BinarySubject

from processes.crossover.bin import (
    HomogeneousCrossover,
    OnePointCrossover,
    TwoPointCrossover,
    ThreePointCrossover,
)
from processes.crossover.core import CrossoverFactory


class BinaryCrossoverType(Enum):
    HOMOGENEOUS = "HOMOGENEOUS"
    ONE_POINT = "ONE_POINT"
    TWO_POINT = "TWO_POINT"
    THREE_POINT = "THREE_POINT"


class BinaryCrossoverFactory(CrossoverFactory):
    def __init__(self, type: BinaryCrossoverType):
        if type == BinaryCrossoverType.HOMOGENEOUS:
            self.CrossoverCreator = HomogeneousCrossover
        elif type == BinaryCrossoverType.ONE_POINT:
            self.CrossoverCreator = OnePointCrossover
        elif type == BinaryCrossoverType.TWO_POINT:
            self.CrossoverCreator = TwoPointCrossover
        elif type == BinaryCrossoverType.THREE_POINT:
            self.CrossoverCreator = ThreePointCrossover
        else:
            raise Exception("Error: type doesnt exist")

    # make as generic
    def create_crossover(self, SubjectCreator: Type[BinarySubject], probability: float):
        return self.CrossoverCreator(SubjectCreator, probability)
