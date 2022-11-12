from abc import ABC, abstractmethod
from typing import TypeVar, Type, List, TypedDict, Any

from processes.crossover.core import Crossover
from processes.selection.core import Selection
from processes.mutation.core import Mutation
from models.valuer import Valuer

C = TypeVar("C")


class Props(TypedDict):
    amount: int
    SubjectCreator: Type[C]
    crossover: Crossover
    mutation: Mutation
    selection: Selection


class Config(TypedDict):
    fitness: Any
    left_limit: float
    right_limit: float
    precision: int


class Population(ABC):
    def __init__(self, props: Props, config: Config):
        self._amount = props["amount"]
        self._crossover = props["crossover"]
        self._mutation = props["mutation"]
        self._SubjectCreator = props["SubjectCreator"]
        self._selection = props["selection"]
        self._config = config

        # generate init population
        self._generate()

    def _pick_the_best_value(self, valuers: List[Valuer]):
        # FIXME: add min/max param
        return sorted(valuers, key=lambda valuer: valuer.value)[0].value

    @abstractmethod
    def _generate(self):
        pass

    @abstractmethod
    def _evolve(self):
        pass

    @abstractmethod
    def run(self, epochs: int):
        pass
