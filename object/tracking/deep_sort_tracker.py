from object.tracking.abstract_object_tracker import *
import numpy as np
from .deep_sort import nn_matching
from .deep_sort.detection import Detection
from .deep_sort.tracker import Tracker


class DeepSortTracker(AbstractObjectTracker):
	def __init__(self):
		metric = nn_matching.NearestNeighborDistanceMetric("cosine", 1)
		self.__tracker = Tracker(metric)

	def track(self, frame: Array[np.uint8], detected_boxes: List[BoundingBox]) -> List[int]:
		rectangles = [np.array([detected_box.upper_left[0], detected_box.upper_left[1], detected_box.lower_right[0],
								detected_box.lower_right[1]]) for detected_box in detected_boxes]
		# features = encoder(frame, rectangles)
		detections = [Detection(rectangle, 1.0, None) for rectangle in rectangles]

		self.__tracker.predict()
		self.__tracker.update(detections)

		results = []
		for track in self.__tracker.tracks:
			# if not track.is_confirmed() or track.time_since_update > 1:
			# 	continue
			results.append(track.track_id)
		return results
