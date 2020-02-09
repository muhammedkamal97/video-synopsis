from object.tracking.abstract_object_tracker import *
from object.tracking.sort import Sort
import numpy as np


class SortTracker(AbstractObjectTracker):

	def __init__(self):
		self.__tracker = Sort()

	def track(self, frame: Array[np.int], detected_boxes: List[BoundingBox]) -> List[int]:
		tracked_objects = self.__tracker.update(np.array(detected_boxes))
		return tracked_objects
