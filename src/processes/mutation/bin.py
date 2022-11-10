import random
from models.chromosome import BinaryChromosome
from processes.mutation.core import Mutation


class EdgeMutation(Mutation):
    @Mutation.checker
    def mutate(self, chromosome: BinaryChromosome):
        index = 0 if random.random() < 0.5 else len(chromosome) - 1
        chromosome.mutate(index)
        return chromosome


class SinglePointMutation(Mutation):
    @Mutation.checker
    def mutate(self, chromosome: BinaryChromosome):
        index = random.randint(0, len(chromosome) - 1)
        chromosome.mutate(index)
        return chromosome


class TwoPointMutation(Mutation):
    @Mutation.checker
    def mutate(self, chromosome: BinaryChromosome):
        point1 = random.randint(0, len(chromosome) - 1)
        point2 = random.randint(point1, len(chromosome) - 1)
        chromosome.mutate(point1, point2)
        return chromosome
