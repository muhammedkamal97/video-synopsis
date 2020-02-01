import numpy as np
from nptyping import Array
from typing import List
from abc import ABC, abstractmethod

from object.activity.bounding_box import BoundingBox


class AbstractObjectTracker(ABC):

    @abstractmethod
    def detect(self, frame: Array[np.int]) -> List[BoundingBox]:
        pass
