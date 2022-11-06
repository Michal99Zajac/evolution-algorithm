from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
import math
import random

from adapters import X2SubjectAdapter

helper = lambda x: list(map(lambda subject: subject.value , x))

class BinarySelection(ABC):
    @abstractmethod
    def select(self, subjects: List[X2SubjectAdapter]):
        pass

    def __sorter(self, subject: X2SubjectAdapter):
        return subject.value

    def _sort(self, subjects: List[X2SubjectAdapter]):
        return sorted(subjects, key=self.__sorter)

class TheBestSelection(BinarySelection):
    def __init__(self, percentage: float):
        if percentage > 1 or percentage < 0:
            raise Exception("Error: percentage should be number between 0 and 1")
        self.__percentage = percentage

    def select(self, subjects: List[X2SubjectAdapter]):
        the_best = self.__sort(subjects)
        size = math.floor(len(subjects) * self.__percentage)
        return the_best[0:size]

class TournamentSelection(BinarySelection):
    def __init__(self, editions_number: int, group_size: int):
        self.__group_size = group_size
        self.__editions_number = editions_number

    def select(self, subjects: List[X2SubjectAdapter]):
        selected: List[X2SubjectAdapter] = []
        __subjects = subjects.copy()

        for _ in range(self.__editions_number):
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
