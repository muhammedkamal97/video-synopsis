from object.tracking.abstract_object_tracker import *
from object.tracking.sort import Sort
import numpy as np


class SortTracker(AbstractObjectTracker):

	def __init__(self):
		self.__tracker = Sort()

	def track(self, frame: Array[np.uint8], detected_boxes: List[BoundingBox]) -> List[int]:
		rectangles = [np.array([detected_box.upper_left[0], detected_box.upper_left[1], detected_box.lower_right[0],
								detected_box.lower_right[1]]) for detected_box in detected_boxes]
		tracked_objects = self.__tracker.update(np.array(rectangles))
		tracked_objects_ids = tracked_objects[:, 4]
		return tracked_objects_ids
