from models.chromosome import BinaryChromosome
from models.subject import X2Subject
from processes.crossover import (
    HomogeneousCrossover,
    BinaryCrossoverFactory,
    BinaryCrossoverType,
)
from processes.mutation import EdgeMutation
from adapters import X2SubjectAdapter
from fitness.schaffer_N4 import schaffer_N4
from processes.selection import TournamentSelection, TheBestSelection, RoulettaSelection

if __name__ == "__main__":
    chromosome_lenght = BinaryChromosome.chromosome_lenght(6, -10, 10)
    selection = RoulettaSelection(0.5, type="min")
    # crossover = HomogeneousCrossover()
    crossoverFactory = BinaryCrossoverFactory(BinaryCrossoverType.ONE_POINT, X2Subject)
    crossover = crossoverFactory.createCrossover()
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
    print(subjects[1].chromosomes[0])
    [off1, off2] = crossover.cross(subjects[0], subjects[1])
    print(off1.chromosomes[0])
    print(off2.chromosomes[0])

    # print(list(map(lambda subject: subject.value , subjects)))
    # print(sum(selection.select(subjects)))
    # selection.select(subjects)
    # print(list(map(lambda subject: subject.value , subjects)))
    # print(list(map(lambda subject: subject.value , selection.select(subjects))))
