from typing import List
from abc import ABC, abstractmethod

from object.activity.activity_tube import ActivityTube


class AbstractStitcher(ABC):
    # TODO: add return type hints for methods

    @abstractmethod
    def stitch(self, schedule):
        pass
