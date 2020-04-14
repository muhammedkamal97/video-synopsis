import numpy as np
from nptyping import Array
from typing import List
from abc import ABC, abstractmethod

from object.activity.bounding_box import BoundingBox


class AbstractObjectTracker(ABC):

	@abstractmethod
	def track(self, frame: Array[np.uint8], detected_boxes: List[BoundingBox]) -> List[int]:
		pass
