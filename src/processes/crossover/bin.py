import random
from typing import Type, List, Tuple
from models.chromosome import BinaryChromosome

from models.subject import BinarySubject
from processes.crossover.core import Crossover


ZipedSubjectGens = List[Tuple[bool]]


class BinaryCrossover(Crossover):
    def __init__(self, SubjectCreator: Type[BinarySubject], probability: float):
        super().__init__(probability)
        self.SubjectCreator = SubjectCreator

    def _zip_subject_gens(self, *subjects: BinarySubject):
        ziped_subjects_gens: List[ZipedSubjectGens] = []
        for subject in subjects:
            # copy all chromosomes gens
            chromosomes_gens = map(
                lambda chromosome: chromosome.gens.copy(),
                subject.chromosomes,
            )

            # zip them all and convert to the list
            ziped_chromosomes_gens = list(zip(*chromosomes_gens))

            # add to list
            ziped_subjects_gens.append(ziped_chromosomes_gens)

        return ziped_subjects_gens

    def _create_subjects(self, *ziped_subjects_gens: ZipedSubjectGens):
        subjects: List[BinarySubject] = []

        for ziped_subject_gens in ziped_subjects_gens:
            # unzip gens
            chromosomes_gens = map(
                lambda ziped_subject_gen: list(ziped_subject_gen),
                zip(*ziped_subject_gens),
            )

            # transform to list
            chromosomes_gens = list(chromosomes_gens)

            # create chromosomes
            chromosomes = [
                BinaryChromosome(chromosome_gens)
                for chromosome_gens in chromosomes_gens
            ]

            # get subject length from first chromosome length
            length = len(chromosomes[0])

            # create subject
            subjects.append(self.SubjectCreator(chromosomes, length))

        return subjects


class HomogeneousCrossover(BinaryCrossover):
    @Crossover.checker
    def cross(self, parent_A: BinarySubject, parent_B: BinarySubject):
        # zip subjects gens
        [ziped_subject_A_gens, ziped_subject_B_gens] = self._zip_subject_gens(
            parent_A, parent_B
        )

        # cross
        for index, (zip_A, zip_B) in enumerate(
            zip(ziped_subject_A_gens, ziped_subject_B_gens)
        ):
            if index % 2 != 0:
                ziped_subject_A_gens[index] = zip_B
                ziped_subject_B_gens[index] = zip_A

        # return new subjects
        return self._create_subjects(ziped_subject_A_gens, ziped_subject_B_gens)


class OnePointCrossover(BinaryCrossover):
    @Crossover.checker
    def cross(self, parent_A: BinarySubject, parent_B: BinarySubject):
        # zip subject gens
        [ziped_subject_A_gens, ziped_subject_B_gens] = self._zip_subject_gens(
            parent_A, parent_B
        )

        # calc positions - pointcut
        position = random.randint(0, len(ziped_subject_A_gens))

        # cross
        ziped_offspring_A_gens = (
            ziped_subject_A_gens[0:position]
            + ziped_subject_B_gens[position : len(ziped_subject_A_gens)]
        )
        ziped_offspring_B_gens = (
            ziped_subject_B_gens[0:position]
            + ziped_subject_A_gens[position : len(ziped_subject_A_gens)]
        )

        return self._create_subjects(ziped_offspring_A_gens, ziped_offspring_B_gens)


class TwoPointCrossover(BinaryCrossover):
    @Crossover.checker
    def cross(self, parent_A: BinarySubject, parent_B: BinarySubject):
        # zip subject gens
        [ziped_subject_A_gens, ziped_subject_B_gens] = self._zip_subject_gens(
            parent_A, parent_B
        )

        # calc pointcut
        position1 = random.randint(0, len(ziped_subject_A_gens))
        position2 = random.randint(position1, len(ziped_subject_A_gens))

        # cross
        ziped_offspring_A_gens = (
            ziped_subject_A_gens[0:position1]
            + ziped_subject_B_gens[position1:position2]
            + ziped_subject_A_gens[position2 : len(ziped_subject_A_gens)]
        )
        ziped_offspring_B_gens = (
            ziped_subject_B_gens[0:position1]
            + ziped_subject_A_gens[position1:position2]
            + ziped_subject_B_gens[position2 : len(ziped_subject_A_gens)]
        )

        return self._create_subjects(ziped_offspring_A_gens, ziped_offspring_B_gens)


class ThreePointCrossover(BinaryCrossover):
    def cross(self, parent_A: BinarySubject, parent_B: BinarySubject):
        # zip subject gens
        [ziped_subject_A_gens, ziped_subject_B_gens] = self._zip_subject_gens(
            parent_A, parent_B
        )

        # calc pointcut
        position1 = random.randint(0, len(ziped_subject_A_gens))
        position2 = random.randint(position1, len(ziped_subject_A_gens))
        position3 = random.randint(position2, len(ziped_subject_A_gens))

        # cross
        ziped_offspring_A_gens = (
            ziped_subject_A_gens[0:position1]
            + ziped_subject_B_gens[position1:position2]
            + ziped_subject_A_gens[position2:position3]
            + ziped_subject_B_gens[position3 : len(ziped_subject_A_gens)]
        )
        ziped_offspring_B_gens = (
            ziped_subject_B_gens[0:position1]
            + ziped_subject_A_gens[position1:position2]
            + ziped_subject_B_gens[position2:position3]
            + ziped_subject_A_gens[position3 : len(ziped_subject_A_gens)]
        )

        return self._create_subjects(ziped_offspring_A_gens, ziped_offspring_B_gens)
