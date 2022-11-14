from typing import List

from models.chromosome.decimal import DecimalChromosome
from models.chromosome.bin import BinaryChromosome
from models.subject.bin import BinarySubject
from models.subject.decimal import DecimalSubject
from models.valuer import Valuer


class ValuerDecimalSubject(DecimalSubject, Valuer):
    def __init__(
        self, subject: DecimalSubject, left_limit: float, right_limit: float, fitness
    ):
        self.subject = subject
        self.__values = self.__get_values(subject.chromosomes)
        self.__value = fitness(*self.__values)

    @property
    def value(self):
        return self.__value

    @property
    def values(self):
        return self.__values

    @property
    def chromosomes(self):
        return self.subject.chromosomes

    def mutate(self, *values: float):
        return self.subject.mutate(values)

    def __get_values(self, chromosomes: List[DecimalChromosome]):
        return [chromosome.value for chromosome in chromosomes]


class ValuerBinarySubject(BinarySubject, Valuer):
    def __init__(
        self,
        subject: BinarySubject,
        left_limit: float,
        right_limit: float,
        fitness,
    ):
        self.subject = subject

        # calc value of the subject
        self.__values = self.__transform(subject.chromosomes, left_limit, right_limit)
        self.__value: float = fitness(*self.__values)

    @property
    def value(self):
        return self.__value

    @property
    def values(self):
        return self.__values

    @property
    def chromosomes(self):
        return self.subject.chromosomes

    def __len__(self):
        return len(self.subject)

    def mutate(self, *args: int):
        self.subject.mutate(args)

    def inverse(self, left: int, right: int):
        self.subject.inverse(left, right)

    def __transform(
        self, chromosomes: List[BinaryChromosome], left_limit: float, right_limit: float
    ):
        """
        transform binary to decimal
        """
        transformator = lambda chromosome: left_limit + int(str(chromosome), 2) * (
            right_limit - left_limit
        ) / (2 ** len(self) - 1)

        return [transformator(chromosome) for chromosome in chromosomes]
