from ast import List
import random
from typing import Type
from models.chromosome import BinaryChromosome

from models.subject import BinarySubject
from processes.crossover.core import Crossover

# def match_parents(parent1: BinaryChromosome, parent2: BinaryChromosome):
#     if len(parent1) != len(parent2):
#         raise Exception("Error: chromosomes lengths are not equal")


# def one_point(parent1: BinaryChromosome, parent2: BinaryChromosome):
#     match_parents(parent1, parent2)
#     position = random.randint(0, len(parent1))
#     offspring1 = BinaryChromosome(
#         parent1.gens[0:position] + parent2.gens[position : len(parent2)]
#     )
#     offspring2 = BinaryChromosome(
#         parent2.gens[0:position] + parent1.gens[position : len(parent1)]
#     )
#     return offspring1, offspring2


# def two_point(parent1: BinaryChromosome, parent2: BinaryChromosome):
#     # match_parents(parent1, parent2)
#     position1 = random.randint(0, len(parent1))
#     position2 = random.randint(position1, len(parent1))
#     offspring1 = BinaryChromosome(
#         parent1.gens[0:position1]
#         + parent2.gens[position1:position2]
#         + parent1.gens[position2 : len(parent1)]
#     )
#     offspring2 = BinaryChromosome(
#         parent2.gens[0:position1]
#         + parent1.gens[position1:position2]
#         + parent2.gens[position2 : len(parent1)]
#     )
#     return offspring1, offspring2


class BinaryCrossover(Crossover):
    def __init__(self, SubjectCreator: Type[BinarySubject]):
        self.SubjectCreator = SubjectCreator

    def _zip_gens(self, subject: BinarySubject):
        return list(
            zip(
                *map(
                    lambda chromosome: chromosome.gens.copy(),
                    subject.chromosomes,
                )
            )
        )

    def _unzip_gens(self, ziped_gens):
        return list(map(lambda x: list(x), list(zip(*ziped_gens))))

    def _create_subject(self, chromosomes_gens):
        length = len(chromosomes_gens[0])
        return self.SubjectCreator(
            [BinaryChromosome(gens) for gens in chromosomes_gens], length
        )


class HomogeneousCrossover(BinaryCrossover):
    def cross(self, parent_A: BinarySubject, parent_B: BinarySubject):
        # zip gens
        ziped_A_gens = self._zip_gens(parent_A)
        ziped_B_gens = self._zip_gens(parent_B)

        # cross
        for index, (zip_A, zip_B) in enumerate(zip(ziped_A_gens, ziped_B_gens)):
            if index % 2 != 0:
                ziped_A_gens[index] = zip_B
                ziped_B_gens[index] = zip_A

        # unzip gens
        unziped_A_gens = self._unzip_gens(ziped_A_gens)
        unziped_B_gens = self._unzip_gens(ziped_B_gens)

        # return new subjects
        return [
            self._create_subject(unziped_A_gens),
            self._create_subject(unziped_B_gens),
        ]


class OnePointCrossover(BinaryCrossover):
    def cross(self, parent_A: BinarySubject, parent_B: BinarySubject):
        # zip gens
        ziped_A_gens = self._zip_gens(parent_A)
        ziped_B_gens = self._zip_gens(parent_B)

        # cross
        position = random.randint(0, len(parent_A))
        print(f"Position: {position}")
        ziped_offspring_A_gens = (
            ziped_A_gens[0:position] + ziped_B_gens[position : len(ziped_A_gens)]
        )
        ziped_offspring_B_gens = (
            ziped_B_gens[0:position] + ziped_A_gens[position : len(ziped_A_gens)]
        )

        # unzip gens
        unziped_offspring_A_gens = self._unzip_gens(ziped_offspring_A_gens)
        unziped_offspring_B_gens = self._unzip_gens(ziped_offspring_B_gens)

        # return new subjects
        return [
            self._create_subject(unziped_offspring_A_gens),
            self._create_subject(unziped_offspring_B_gens),
        ]


class TwoPointCrossover(BinaryCrossover):
    def cross(self, parent_A: BinarySubject, parent_B: BinarySubject):
        # zip gens
        ziped_A_gens = self._zip_gens(parent_A)
        ziped_B_gens = self._zip_gens(parent_B)

        # cross
        position = random.randint(0, len(parent_A))
        ziped_offspring_A_gens = (
            ziped_A_gens[0:position] + ziped_B_gens[position : len(ziped_A_gens)]
        )
        ziped_offspring_B_gens = (
            ziped_B_gens[0:position] + ziped_A_gens[position : len(ziped_A_gens)]
        )

        # unzip gens
        unziped_offspring_A_gens = self._unzip_gens(ziped_offspring_A_gens)
        unziped_offspring_B_gens = self._unzip_gens(ziped_offspring_B_gens)

        # return new subjects
        return [
            self._create_subject(unziped_offspring_A_gens),
            self._create_subject(unziped_offspring_B_gens),
        ]


class ThreePointCrossover(BinaryCrossover):
    def cross(self, parent_A: BinarySubject, parent_B: BinarySubject):
        # zip gens
        ziped_A_gens = self._zip_gens(parent_A)
        ziped_B_gens = self._zip_gens(parent_B)

        # cross
        position = random.randint(0, len(parent_A))
        ziped_offspring_A_gens = (
            ziped_A_gens[0:position] + ziped_B_gens[position : len(ziped_A_gens)]
        )
        ziped_offspring_B_gens = (
            ziped_B_gens[0:position] + ziped_A_gens[position : len(ziped_A_gens)]
        )

        # unzip gens
        unziped_offspring_A_gens = self._unzip_gens(ziped_offspring_A_gens)
        unziped_offspring_B_gens = self._unzip_gens(ziped_offspring_B_gens)

        # return new subjects
        return [
            self._create_subject(unziped_offspring_A_gens),
            self._create_subject(unziped_offspring_B_gens),
        ]
