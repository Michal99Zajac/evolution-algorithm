import random
from enum import Enum

from models.subject.bin import BinarySubject
from processes.mutation.core import Mutation


class BinMutation(Enum):
    EDGE = "EDGE"
    SINGLE = "SINGLE"
    TWO_POINT = "TWO_POINT"


class EdgeMutation(Mutation):
    @Mutation.checker
    def mutate(self, subject: BinarySubject):
        index = 0 if random.random() < 0.5 else len(subject) - 1
        subject.mutate(index)
        return subject


class SinglePointMutation(Mutation):
    @Mutation.checker
    def mutate(self, subject: BinarySubject):
        index = random.randint(0, len(subject) - 1)
        subject.mutate(index)
        return subject


class TwoPointMutation(Mutation):
    @Mutation.checker
    def mutate(self, subject: BinarySubject):
        point1 = random.randint(0, len(subject) - 1)
        point2 = random.randint(point1, len(subject) - 1)
        subject.mutate(point1, point2)
        return subject
