import numpy as np
from nptyping import Array
from typing import List
from abc import ABC, abstractmethod

from object.activity.bounding_box import BoundingBox


def map_detected_box_to_rectangle(detected_box: BoundingBox):
	return [detected_box.upper_left[:], detected_box.lower_right[:]]


class AbstractObjectTracker(ABC):

	@abstractmethod
	def track(self, frame: Array[np.int], detected_boxes: List[BoundingBox]) -> List[int]:
		pass
