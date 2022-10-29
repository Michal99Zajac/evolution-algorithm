from models.Chromosome import Chromosome
import processes.crossover as crossover
from processes.mutation import EdgeMutation

if __name__ == "__main__":
    chromosome_lenght = Chromosome.chromosome_lenght(6, -10, 10)
    chromosome_a = Chromosome.generate(chromosome_lenght)
    chromosome_b = Chromosome.generate(chromosome_lenght)
    mutation = EdgeMutation(0.3)

    print(chromosome_a.gens)
    mutation.mutate(chromosome_a)
    print(chromosome_a.gens)
