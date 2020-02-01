import numpy as np
from nptyping import Array
from typing import List
from abc import ABC, abstractmethod

from object.activity.bounding_box import BoundingBox


class AbstractObjectTracker(ABC):
    # TODO: add return type hints for methods

    @abstractmethod
    def track(self, frame: Array[np.int], detected_boxes: List[BoundingBox]):
        pass

    @abstractmethod
    def get_active_objects(self):
        pass

