import numpy as np
from typing import List, NoReturn
from nptyping import Array
from abc import ABC, abstractmethod

from object.activity.activity_tube import ActivityTube


class AbstractStitcher(ABC):
    # TODO: add return type hints for methods

    @abstractmethod
    def initialize(self, activity_tubes: List[ActivityTube], schedule: List[int]) -> NoReturn:
        pass

    @abstractmethod
    def has_next_frame(self) -> bool:
        pass

    @abstractmethod
    def next_frame(self) -> Array[np.int]:
        pass
