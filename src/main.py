from models.chromosome import BinaryChromosome
from models.subject import X2Subject
import processes.crossover as crossover
from processes.mutation import EdgeMutation
from adapters import X2SubjectAdapter
from fitness.schaffer_N4 import schaffer_N4
from processes.selection import TheBestSelection

if __name__ == "__main__":
    chromosome_lenght = BinaryChromosome.chromosome_lenght(6, -10, 10)
    selection = TheBestSelection(0.33)
    subjects = [X2SubjectAdapter(
        [BinaryChromosome.generate(chromosome_lenght), BinaryChromosome.generate(chromosome_lenght)],
        length=chromosome_lenght,
        left_limit=-10,
        right_limit=10,
        fitness=schaffer_N4) for _ in range(10)]


    values = map(lambda subject: subject.value , selection.select(subjects))
    print(list(values))
