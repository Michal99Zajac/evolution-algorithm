from abc import ABC, abstractmethod


class Valuer(ABC):
    """
    Interface for subjects class with value property
    """

    @property
    @abstractmethod
    def value(self) -> float:
        pass
