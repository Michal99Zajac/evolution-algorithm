from fitness import schaffer_N4
from models.Chromosome import Chromosome

if __name__ == "__main__":
    result = schaffer_N4(0, 1.25313)
    chromosome_lenght = Chromosome.chromosome_lenght(6, -10, 10)
    chromosome_a = Chromosome.generate(chromosome_lenght)
    chromosome_b = Chromosome.generate(chromosome_lenght)
    new_chromosome = chromosome_a.cross(chromosome_b, 3)

    print(chromosome_a.gens)
    print(chromosome_b.gens)
    print(new_chromosome.gens)
