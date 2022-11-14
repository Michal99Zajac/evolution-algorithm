import math
import random
from typing import Callable, Tuple, Any, List
from enum import Enum

from models.subject.decorators import ValuerBinarySubject
from processes.selection.core import Selection


class SelectionEnum(Enum):
    THE_BEST = "THE_BEST"
    TOURNAMENT = "TOURNAMENT"
    ROULETTE = "ROULETTE"


class TheBestSelection(Selection):
    def __init__(self, percentage: float, type: str = "min"):
        if percentage > 1 or percentage < 0:
            raise Exception("Error: percentage should be number between 0 and 1")
        self.__percentage = percentage
        self._type = type

    def select(self, valuers: List[ValuerBinarySubject]):
        the_best = self._sort(valuers)
        size = math.floor(len(valuers) * self.__percentage)
        return the_best[0:size]


class TournamentSelection(Selection):
    def __init__(self, percentage: float, group_size: int, type: str = "min"):
        if percentage > 1 or percentage < 0:
            raise Exception("Error: percentage should be number between 0 and 1")
        self.__group_size = group_size
        self.__percentage = percentage
        self._type = type

    def select(self, valuers: List[Any]):
        selected: List[ValuerBinarySubject] = []
        __subjects = valuers.copy()
        editions = math.floor(len(valuers) * self.__percentage)

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

    def __draw(self, subjects: List[ValuerBinarySubject]):
        selected: List[ValuerBinarySubject] = []
        BORDER = 0.05  # probability scope

        # tournament group size is bigger then whole population
        if self.__group_size >= len(subjects):
            return subjects

        # draw subject to tournament
        index = 0
        while len(selected) != self.__group_size:
            probability = random.random()
            if probability < BORDER:
                selected.append(subjects.pop(index))
            index = (index + 1) % len(subjects)

        return selected


class RouletteSelection(Selection):
    def __init__(self, percentage: float, type: str = "min"):
        if percentage > 1 or percentage < 0:
            raise Exception("Error: percentage should be number between 0 and 1")
        self.__percentage = percentage
        self._type = type

    def select(self, valuers: List[ValuerBinarySubject]):
        __subjects__ = valuers.copy()
        selected: List[ValuerBinarySubject] = []

        for _ in range(math.floor(len(valuers) * self.__percentage)):
            distributanta = self.__make_distributanta(__subjects__)
            index = self.__twist(distributanta)
            selected.append(__subjects__.pop(index))

        return selected

    def __make_distributanta(self, subjects: List[ValuerBinarySubject]):
        totaliser: Callable[[ValuerBinarySubject], float] = (
            lambda subject: subject.value if self._type == "max" else 1 / subject.value
        )
        total = sum(map(totaliser, subjects))
        fractioner: Callable[[ValuerBinarySubject], float] = (
            lambda subject: (
                subject.value if self._type == "max" else 1 / subject.value
            )
            / total
        )
        fractions = list(map(fractioner, subjects))
        distributanta = [sum(fractions[0:index]) for index in range(len(fractions))]
        return list(zip(distributanta, subjects))

    def __twist(self, distributanta: List[Tuple[float, ValuerBinarySubject]]):
        chance = random.random()
        index = 0
        is_found = False
        while not is_found:
            if chance < distributanta[index][0] or index == len(distributanta) - 1:
                is_found = True
            else:
                index += 1

        return index
