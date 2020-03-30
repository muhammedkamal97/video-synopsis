from typing import List
from abc import ABC, abstractmethod

from object.activity.activity_tube import ActivityTube


class AbstractScheduler(ABC):
    # TODO: add return type hints for methods

    @abstractmethod
    def schedule(self, activity_tubes: List[ActivityTube]) -> List[int]:
        """Schedule the given activity tubes and compute their starting frame in the synopsis video.

        Parameters
        ----------
        activity_tubes : List[ActivityTube]
            The list of activity tubes to be scheduled.

        Returns
        ------
        List[int]
            List of integers with same length as the activity_tubes list.
            Each integer represents the starting frame of the activity tube -with the same index- in the synopsis video.
        """
        pass
