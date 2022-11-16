from abc import ABC, abstractmethod
from typing import TypeVar, List, TypedDict, Any
import math

from processes.crossover.core import Crossover
from processes.selection.core import Selection
from processes.mutation.core import Mutation
from models.valuer import Valuer
from processes.elite import Eliter

C = TypeVar("C")


class Props(TypedDict):
    amount: int
    crossover: Crossover
    mutation: Mutation
    selection: Selection
    eliter: Eliter


class Config(TypedDict):
    fitness: Any
    left_limit: float
    right_limit: float
    type: str


class Population(ABC):
    def __init__(self, props: Props, config: Config):
        self._amount = props["amount"]
        self._crossover = props["crossover"]
        self._mutation = props["mutation"]
        self._selection = props["selection"]
        self._eliter = props["eliter"]
        self._config = config

        # generate init population
        self._generate()

    def _pick_the_best(self, valuers: List[Valuer]):
        return sorted(
            valuers,
            key=lambda valuer: valuer.value
            if self._config["type"] == "min"
            else -valuer.value,
        )[0]

    def _avarage(self, valuers: List[Valuer]):
        avarage = sum(map(lambda valuer: valuer.value, valuers)) / len(valuers)
        standard_deviation = math.sqrt(
            sum([(valuer.value - avarage) ** 2 for valuer in valuers]) / len(valuers)
        )

        return avarage, standard_deviation

    @abstractmethod
    def _generate(self):
        pass

    @abstractmethod
    def _evolve(self):
        pass

    @abstractmethod
    def run(self, epochs: int):
        pass
