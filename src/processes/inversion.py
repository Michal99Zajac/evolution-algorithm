from __future__ import annotations
from typing import TypeVar
import random

from models.subject.bin import BinarySubject
from utils.two_index import two_index

TInversion = TypeVar("TInversion", bound="Inversion")


def checker(function):
    def inverse(self: TInversion, subject: BinarySubject):
        if self._probability >= random.random():
            return function(self, subject)
        return subject

    return inverse


class Inversion:
    def __init__(self, probability: float):
        if probability > 1 or probability < 0:
            raise Exception(
                "Error: probability can't be bigger then 100% and smaller then 0%"
            )
        self._probability = probability

    @checker
    def inverse(self, subject: BinarySubject):
        [left, right] = sorted(list(two_index(len(subject))))
        subject.inverse(left, right)
