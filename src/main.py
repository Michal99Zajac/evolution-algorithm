from models.Chromosome import Chromosome
import processes.crossing as cross

if __name__ == "__main__":
    chromosome_lenght = Chromosome.chromosome_lenght(6, -10, 10)
    chromosome_a = Chromosome.generate(chromosome_lenght)
    chromosome_b = Chromosome.generate(chromosome_lenght)
    offspring1, offspring2 = cross.one_point(chromosome_a, chromosome_b)

    print(chromosome_a.gens)
    print(chromosome_b.gens)
    print(offspring1.gens)
    print(offspring2.gens)
