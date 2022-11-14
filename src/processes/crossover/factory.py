from enum import Enum
from typing import Type
from models.subject.bin import BinarySubject

from processes.crossover.bin import (
    HomogeneousCrossover,
    OnePointCrossover,
    TwoPointCrossover,
    ThreePointCrossover,
)
from processes.crossover.decimal import (
    ArithmeticCrossover,
    AveragingCrossover,
    BlendCrossoverAlpha,
    BlendCrossoverAlphaBeta,
    LinearCrossover,
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


class DecimalCrossoverType(Enum):
    ARITHMETIC = "ARITHMETIC"
    BLEND_ALPHA = "BLEND_ALPHA"
    BLEND_ALPHA_BETA = "BLEND_ALPHA_BETA"
    AVERAGING = "AVERAGING"
    LINEAR = "LINEAR"


class DecimalCrossoverFactory(CrossoverFactory):
    def __init__(self, type: DecimalCrossoverType):
        if type == DecimalCrossoverType.ARITHMETIC:
            self.CrossoverCreator = ArithmeticCrossover
        elif type == DecimalCrossoverType.AVERAGING:
            self.CrossoverCreator = AveragingCrossover
        elif type == DecimalCrossoverType.BLEND_ALPHA:
            self.CrossoverCreator = BlendCrossoverAlpha
        elif type == DecimalCrossoverType.BLEND_ALPHA_BETA:
            self.CrossoverCreator = BlendCrossoverAlphaBeta
        elif type == DecimalCrossoverType.LINEAR:
            self.CrossoverCreator = LinearCrossover
        else:
            raise Exception("Error: type doesnt exist")

    def create_crossover(
        self, probability: float, left_limit, right_limit, k, alpha, beta, fitness, type
    ):
        return self.CrossoverCreator(
            probability,
            left_limit=left_limit,
            right_limit=right_limit,
            k=k,
            alpha=alpha,
            beta=beta,
            fitness=fitness,
            type=type,
        )
