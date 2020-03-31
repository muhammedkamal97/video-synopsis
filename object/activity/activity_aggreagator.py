from typing import List, Dict
import numpy as np
from nptyping import Array
from object.activity.activity_tube import ActivityTube
from object.activity.bounding_box import BoundingBox
from object.activity.object_trackable import ObjectTrackable


class ActivityAggregator:
    __activity_tubes: Dict[int, ActivityTube]

    def __init__(self):
        self.__activity_tubes = {}

    def aggregate(self, frame: Array[np.uint8], detected_boxes: List[BoundingBox], object_ids: List[int], frame_count: int):

        for obj_id, box in list(zip(object_ids, detected_boxes)):
            if obj_id not in self.__activity_tubes:
                self.__activity_tubes[obj_id] = ActivityTube(frame_count)

            # get box
            x1, y1 = box.upper_left
            x2, y2 = box.lower_right
            data = frame[y1:y2, x1:x2].astype(np.uint8)
            self.__activity_tubes[obj_id].add_trackable(ObjectTrackable(box, data))

    def get_activity_tubes(self):
        return list(self.__activity_tubes.values())

    def clear(self):
        self.__activity_tubes = {}
