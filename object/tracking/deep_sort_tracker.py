from object.tracking.abstract_object_tracker import *
import numpy as np
from .deep_sort import nn_matching
from .deep_sort.detection import Detection
from .deep_sort.tracker import Tracker
from .deep_sort import generate_detections
from .deep_sort import preprocessing


class DeepSortTracker(AbstractObjectTracker):
	def __init__(self):
		metric = nn_matching.NearestNeighborDistanceMetric("cosine", 0.3, None)
		self.__tracker = Tracker(metric)
		self.__encoder = generate_detections.create_box_encoder('deep_sort/model/mars-small128.pb', batch_size=1)

	def track(self, frame: Array[np.uint8], detected_boxes: List[BoundingBox]) -> List[int]:
		results = []
		try:
			rectangles = [
				np.array(
					[
						detected_box.upper_left[0],
						detected_box.upper_left[1],
						abs(detected_box.upper_left[0] - detected_box.lower_right[0]),
						abs(detected_box.upper_left[1] - detected_box.lower_right[1])
					]
				) for detected_box in detected_boxes
			]
			features = self.__encoder(frame, rectangles)

			detections = [Detection(box, 0.9, feature) for box, feature in zip(rectangles, features)]

			boxes = np.array([d.tlwh for d in detections])
			scores = np.array([d.confidence for d in detections])
			indices = preprocessing.non_max_suppression(boxes, 1.0, scores)
			detections = [detections[i] for i in indices]

			self.__tracker.predict()
			self.__tracker.update(detections)

			for track in self.__tracker.tracks:
				if not track.is_confirmed() or track.time_since_update > 1:
					continue
				results.append(track.track_id)
		except np.AxisError:
			print("ERROR occurred!")
			pass

		return results
