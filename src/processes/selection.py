from abc import ABC, abstractmethod
from typing import List
import math

from adapters import X2SubjectAdapter


class BinarySelection(ABC):
    @abstractmethod
    def select(self, subjects: List[X2SubjectAdapter]):
        pass

class TheBestSelection(BinarySelection):
    def __init__(self, percentage: float):
        if percentage > 1 or percentage < 0:
            raise Exception("Error: percentage should be number between 0 and 1")
        self.__percentage = percentage

    def select(self, subjects: List[X2SubjectAdapter]):
        the_best = sorted(subjects, key=self.__sorter)
        size = math.floor(len(subjects) * self.__percentage)
        return the_best[0:size]

    def __sorter(self, subject: X2SubjectAdapter):
        return subject.value
