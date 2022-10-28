from fitness import schaffer_N4
from models.Chromosome import Chromosome
from models.Crossing import HomogeneousCrossing

if __name__ == "__main__":
    result = schaffer_N4(0, 1.25313)
    chromosome_lenght = Chromosome.chromosome_lenght(6, -10, 10)
    chromosome_a = Chromosome.generate(4)
    chromosome_b = Chromosome.generate(4)
    crossing = HomogeneousCrossing()
    offspring1, offspring2 = crossing.cross(chromosome_a, chromosome_b)

    print(chromosome_a.gens)
    print(chromosome_b.gens)
    print(offspring1.gens)
    print(offspring2.gens)
