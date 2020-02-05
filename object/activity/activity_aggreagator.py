from typing import List
import numpy as np
from nptyping import Array

from object.activity.bounding_box import BoundingBox


class ActivityAggregator:

    def __init__(self):
        self.__activity_tubes = {}

    def aggregate(self, frame: Array[np.int], detected_boxes: List[BoundingBox], object_ids: List[int]):
        pass

    def get_activity_tubes(self):
        return self.__activity_tubes

    def clear(self):
        self.__activity_tubes = {}
