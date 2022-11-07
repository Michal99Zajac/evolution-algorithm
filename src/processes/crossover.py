import random

from models.chromosome import BinaryChromosome


def match_parents(parent1: BinaryChromosome, parent2: BinaryChromosome):
    if len(parent1) != len(parent2):
        raise Exception("Error: chromosomes lengths are not equal")


def one_point(parent1: BinaryChromosome, parent2: BinaryChromosome):
    match_parents(parent1, parent2)
    position = random.randint(0, len(parent1))
    offspring1 = BinaryChromosome(
        parent1.gens[0:position] + parent2.gens[position : len(parent2)]
    )
    offspring2 = BinaryChromosome(
        parent2.gens[0:position] + parent1.gens[position : len(parent1)]
    )
    return offspring1, offspring2


def two_point(parent1: BinaryChromosome, parent2: BinaryChromosome):
    match_parents(parent1, parent2)
    position1 = random.randint(0, len(parent1))
    position2 = random.randint(position1, len(parent1))
    offspring1 = BinaryChromosome(
        parent1.gens[0:position1]
        + parent2.gens[position1:position2]
        + parent1.gens[position2 : len(parent1)]
    )
    offspring2 = BinaryChromosome(
        parent2.gens[0:position1]
        + parent1.gens[position1:position2]
        + parent2.gens[position2 : len(parent1)]
    )
    return offspring1, offspring2


def homogeneous(parent1: BinaryChromosome, parent2: BinaryChromosome):
    match_parents(parent1, parent2)
    offspring1_gens = parent1.gens.copy()
    offspring2_gens = parent2.gens.copy()

    for index, (gen1, gen2) in enumerate(zip(parent1.gens, parent2.gens)):
        if index % 2 != 0:
            offspring1_gens[index] = gen2
            offspring2_gens[index] = gen1

    return BinaryChromosome(offspring1_gens), BinaryChromosome(offspring2_gens)


__all__ = ["one_point", "two_point", "homogeneous"]
