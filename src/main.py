from models.chromosome import BinaryChromosome
import processes.crossover as crossover
from processes.mutation import EdgeMutation

if __name__ == "__main__":
    chromosome_lenght = BinaryChromosome.chromosome_lenght(6, -10, 10)
    chromosome_a = BinaryChromosome.generate(chromosome_lenght)
    chromosome_b = BinaryChromosome.generate(chromosome_lenght)
    mutation = EdgeMutation(0.3)

    print(chromosome_a.gens)
    mutation.mutate(chromosome_a)
    print(chromosome_a.gens)
