from models.chromosome import BinaryChromosome
from models.subject import X2Subject
from processes.crossover.factory import BinaryCrossoverFactory, BinaryCrossoverType
from processes.mutation.bin import EdgeMutation
from adapters import X2SubjectAdapter
from fitness.schaffer_N4 import schaffer_N4
from processes.selection import TournamentSelection, TheBestSelection, RoulettaSelection

if __name__ == "__main__":
    chromosome_lenght = BinaryChromosome.chromosome_lenght(6, -10, 10)
    selection = RoulettaSelection(0.5, type="min")
    crossoverFactory = BinaryCrossoverFactory(BinaryCrossoverType.ONE_POINT)
    crossover = crossoverFactory.create_crossover(X2Subject)
    mutation = EdgeMutation(1)
    subjects = [
        X2SubjectAdapter(
            [
                BinaryChromosome.generate(chromosome_lenght),
                BinaryChromosome.generate(chromosome_lenght),
            ],
            length=chromosome_lenght,
            left_limit=-10,
            right_limit=10,
            fitness=schaffer_N4,
        )
        for _ in range(6)
    ]

    print(subjects[0].chromosomes[0])
    mutation.mutate(subjects[0].chromosomes[0])
    print(subjects[0].chromosomes[0])
