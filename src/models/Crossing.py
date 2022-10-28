from abc import ABC, abstractmethod
import random
from typing import List

from .Chromosome import Chromosome

def match_parents(parent1: Chromosome, parent2: Chromosome):
    if len(parent1) != len(parent2):
        raise Exception("Error: chromosomes lengths are not equal")

class Crossing(ABC):
    @abstractmethod
    def cross(self, parent1: Chromosome, parent2: Chromosome):
        pass

class OnePointCrossing(Crossing):
    def cross(self, parent1: Chromosome, parent2: Chromosome):
        match_parents(parent1, parent2)
        position = random.randint(0, len(parent1))
        offspring1 = Chromosome(parent1.gens[0:position] + parent2.gens[position:len(parent2)])
        offspring2 = Chromosome(parent2.gens[0:position] + parent1.gens[position:len(parent1)])
        return offspring1, offspring2

class TwoPointCrossing(Crossing):
    def cross(self, parent1: Chromosome, parent2: Chromosome):
        match_parents(parent1, parent2)
        position1 = random.randint(0, len(parent1))
        position2 = random.randint(position1, len(parent1))
        offspring1 = Chromosome(parent1.gens[0:position1] + parent2.gens[position1:position2] + parent1.gens[position2:len(parent1)])
        offspring2 = Chromosome(parent2.gens[0:position1] + parent1.gens[position1:position2] + parent2.gens[position2:len(parent1)])
        return offspring1, offspring2

class HomogeneousCrossing(Crossing):
    def cross(self, parent1: Chromosome, parent2: Chromosome):
        match_parents(parent1, parent2)
        offspring1_gens: List[bool] = parent1.gens.copy()
        offspring2_gens: List[bool] = parent2.gens.copy()

        for index, (gen1, gen2) in enumerate(zip(parent1.gens, parent2.gens)):
            if index % 2 != 0:
                offspring1_gens[index] = gen2
                offspring2_gens[index] = gen1

        return Chromosome(offspring1_gens), Chromosome(offspring2_gens)

