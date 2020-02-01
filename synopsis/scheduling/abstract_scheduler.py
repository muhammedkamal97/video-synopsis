from typing import List
from abc import ABC, abstractmethod

from object.activity.activity_tube import ActivityTube


class AbstractScheduler(ABC):
    # TODO: add return type hints for methods

    @abstractmethod
    def schedule(self, activity_tubes: List[ActivityTube]):
        pass
