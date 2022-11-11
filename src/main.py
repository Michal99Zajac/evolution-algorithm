from models.chromosome import BinaryChromosome
from models.subject import X2Subject
from processes.crossover.factory import BinaryCrossoverFactory, BinaryCrossoverType
from processes.mutation.bin import EdgeMutation, SinglePointMutation
from fitness.schaffer_N4 import schaffer_N4
from processes.selection.bin import (
    TournamentSelection,
    TheBestSelection,
    RoulettaSelection,
)
from models.subject import X2Subject
from models.subject.decorators import ValuerBinarySubject
from models.population.bin import BinaryPopulation
from processes.inversion import Inversion

if __name__ == "__main__":
    crossover = BinaryCrossoverFactory(BinaryCrossoverType.ONE_POINT).create_crossover(
        X2Subject, 0.3
    )
    mutation = SinglePointMutation(0.3)
    inversion = Inversion(0.3)

    pop = BinaryPopulation(
        100,
        X2Subject,
        crossover,
        mutation,
        TournamentSelection(0.5, 3, type="min"),
        inversion,
    )
    data = pop.run(1000)
    print(data)
