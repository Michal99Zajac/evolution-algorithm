from fitness import schaffer_N4
from models.Chromosome import Chromosome

if __name__ == "__main__":
    result = schaffer_N4(0, 1.25313)
    chromosome_lenght = Chromosome.chromosome_lenght(6, -10, 10)
    chromosome = Chromosome(chromosome_lenght)
    print(chromosome.gens)
    chromosome.inverse(23, 25)
    print(chromosome.gens)
