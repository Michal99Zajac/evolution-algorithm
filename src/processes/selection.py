from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Callable
import math
import random

from adapters import X2SubjectAdapter

class BinarySelection(ABC):
    _type: str = 'min'

    @abstractmethod
    def select(self, subjects: List[X2SubjectAdapter]):
        pass

    def __min_sorter(self, subject: X2SubjectAdapter):
        return subject.value

    def __max_sorter(self, subject: X2SubjectAdapter):
        return -subject.value

    def _sort(self, subjects: List[X2SubjectAdapter]):
        return sorted(subjects, key=self.__max_sorter if self._type == 'max' else self.__min_sorter)

class TheBestSelection(BinarySelection):
    def __init__(self, percentage: float, type: str = 'min'):
        if percentage > 1 or percentage < 0:
            raise Exception("Error: percentage should be number between 0 and 1")
        self.__percentage = percentage
        self._type = type

    def select(self, subjects: List[X2SubjectAdapter]):
        the_best = self._sort(subjects)
        size = math.floor(len(subjects) * self.__percentage)
        return the_best[0:size]

class TournamentSelection(BinarySelection):
    def __init__(self, percentage: float, group_size: int, type: str = 'min'):
        if percentage > 1 or percentage < 0:
            raise Exception("Error: percentage should be number between 0 and 1")
        self.__group_size = group_size
        self.__percentage = percentage
        self._type = type

    def select(self, subjects: List[X2SubjectAdapter]):
        selected: List[X2SubjectAdapter] = []
        __subjects = subjects.copy()
        editions = math.floor(len(subjects) * self.__percentage)

        for _ in range(editions):
            # draw and selection
            draw = self.__draw(__subjects)
            sorted_draw = self._sort(draw)
            the_best = sorted_draw.pop(0)

            # select the best
            selected.append(the_best)

            # add the losers to the pot again
            __subjects.extend(sorted_draw)

        return selected

    def __draw(self, subjects: List[X2SubjectAdapter]):
        selected: List[X2SubjectAdapter] = []
        BORDER = 0.05 # probability scope

        # tournament group size is bigger then whole population
        if self.__group_size >= len(subjects): return subjects

        # draw subject to tournament
        index = 0
        while len(selected) != self.__group_size:
            probability = random.random()
            if (probability < BORDER): selected.append(subjects.pop(index))
            index = (index + 1) % len(subjects)

        return selected

class RoulettaSelection(BinarySelection):
    def __init__(self, percentage: float, type: str = 'min'):
        if percentage > 1 or percentage < 0:
            raise Exception("Error: percentage should be number between 0 and 1")
        self.__percentage = percentage
        self._type = type

    def select(self, subjects: List[X2SubjectAdapter]):
        __subjects__ = subjects.copy()
        selected: List[X2SubjectAdapter] = []

        for _ in range(math.floor(len(subjects) * self.__percentage)):
            distributanta = self.__make_distributanta(__subjects__)
            index = self.__twist(distributanta)
            selected.append(__subjects__.pop(index))

        return selected

    def __make_distributanta(self, subjects: List[X2SubjectAdapter]):
        totaliser: Callable[[X2SubjectAdapter], float] = lambda subject: subject.value if self._type == "max" else 1 / subject.value
        total = sum(map(totaliser, subjects))
        fractioner: Callable[[X2SubjectAdapter], float] = lambda subject: (subject.value if self._type == "max" else 1 / subject.value) / total
        fractions = list(map(fractioner, subjects))
        distributanta = [sum(fractions[0:index]) for index in range(len(fractions))]
        return list(zip(distributanta, subjects))

    def __twist(self, distributanta: List[tuple[float | int, X2SubjectAdapter]]):
        chance = random.random()
        index = 0
        is_found = False
        while not is_found:
            if chance < distributanta[index][0] or index == len(distributanta) - 1:
                is_found = True
            else:
                index += 1

        return index
