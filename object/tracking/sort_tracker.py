from object.tracking.abstract_object_tracker import *
from object.tracking.sort import Sort
import numpy as np


class SortTracker(AbstractObjectTracker):

	def __init__(self):
		self.__tracker = Sort(max_age=3)

	def track(self, frame: Array[np.uint8], detected_boxes: List[BoundingBox]) -> List[int]:
		rectangles = list(map(map_detected_box_to_rectangle, detected_boxes))
		tracked_objects = self.__tracker.update(np.array(rectangles))
		tracked_objects_ids = tracked_objects[:, 4]
		return tracked_objects_ids
