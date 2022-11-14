from typing import List

from models.chromosome.decimal import DecimalChromosome
from models.subject.decimal import X2__DecimalSubject
from models.subject.decorators import ValuerDecimalSubject
from fitness.schaffer_N4 import schaffer_N4
from processes.crossover.decimal import ArithmeticCrossover

crossover = ArithmeticCrossover(1, -10, 10, 0.5)

chromosomes_a = [
    DecimalChromosome.generate(-10, 10)
    for _ in range(X2__DecimalSubject.chromosome_number)
]
chromosomes_b = [
    DecimalChromosome.generate(-10, 10)
    for _ in range(X2__DecimalSubject.chromosome_number)
]

subject_a = X2__DecimalSubject(chromosomes_a)
subject_b = X2__DecimalSubject(chromosomes_b)

subjectValuer_a = ValuerDecimalSubject(subject_a, -10, 10, schaffer_N4)
subjectValuer_b = ValuerDecimalSubject(subject_b, -10, 10, schaffer_N4)

offsprings: List[X2__DecimalSubject] = crossover.cross(subject_a, subject_b)

print(off_a.chromosomes)
