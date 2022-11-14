from models.chromosome.decimal import DecimalChromosome
from models.subject.decimal import X2__DecimalSubject
from models.subject.decorators import ValuerDecimalSubject
from fitness.schaffer_N4 import schaffer_N4

chromosomes = [
    DecimalChromosome.generate(-10, 10)
    for _ in range(X2__DecimalSubject.chromosome_number)
]

subject = X2__DecimalSubject(chromosomes)

subjectValuer = ValuerDecimalSubject(subject, -10, 10, schaffer_N4)

print(subjectValuer.value)
