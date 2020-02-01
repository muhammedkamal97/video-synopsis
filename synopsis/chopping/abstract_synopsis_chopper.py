from abc import ABC, abstractmethod


class AbstractSynopsisChopper(ABC):
    # TODO: add return type hints for methods

    @abstractmethod
    def to_chop(self, activity_tubes) -> bool:
        pass
