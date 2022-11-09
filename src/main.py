from models.chromosome import BinaryChromosome
from models.subject import X2Subject
from processes.crossover.factory import BinaryCrossoverFactory, BinaryCrossoverType
from processes.mutation.bin import EdgeMutation
from fitness.schaffer_N4 import schaffer_N4
from processes.selection.bin import (
    TournamentSelection,
    TheBestSelection,
    RoulettaSelection,
)
from models.subject import X2Subject
from models.subject.decorators import ValuerBinarySubject

if __name__ == "__main__":
    chromosome_lenght = BinaryChromosome.chromosome_lenght(6, -10, 10)
    selection = TheBestSelection(0.5, type="min")
    crossoverFactory = BinaryCrossoverFactory(BinaryCrossoverType.ONE_POINT)
    crossover = crossoverFactory.create_crossover(X2Subject)
    mutation = EdgeMutation(0.9)

    subjects = [
        X2Subject(
            [
                BinaryChromosome.generate(chromosome_lenght),
                BinaryChromosome.generate(chromosome_lenght),
            ],
            length=chromosome_lenght,
        )
        for _ in range(6)
    ]

    valuerSubjects = list(
        map(
            lambda subject: ValuerBinarySubject(subject, -10, 10, schaffer_N4), subjects
        )
    )

    print(valuerSubjects[0].value)
    print(valuerSubjects[0].chromosomes)
    valuerSubjects[0].mutate(mutation)

    valuerSubjects = list(
        map(
            lambda subject: ValuerBinarySubject(subject, -10, 10, schaffer_N4),
            valuerSubjects,
        )
    )
    print(valuerSubjects[0].chromosomes)
    print(valuerSubjects[0].value)
