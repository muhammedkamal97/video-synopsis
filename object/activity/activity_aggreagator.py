from typing import List, Dict
import numpy as np
from nptyping import Array
from object.activity.activity_tube import ActivityTube
from object.activity.bounding_box import BoundingBox
from object.activity.object_trackable import ObjectTrackable


class ActivityAggregator:
    __activity_tubes: Dict[int, ActivityTube]

    def __init__(self, alpha_size=0.9, alpha_loc=0.5):
        self.__activity_tubes = {}
        self.alpha_size = alpha_size
        self.alpha_loc = alpha_loc

    def aggregate(self, frame: Array[np.uint8], detected_boxes: List[BoundingBox], object_ids: List[int],
                  frame_count: int):

        for obj_id, box in list(zip(object_ids, detected_boxes)):
            if obj_id not in self.__activity_tubes:
                self.__activity_tubes[obj_id] = ActivityTube(frame_count)

            smoothed_box = box

            # smooth box size using exponential averaging
            if self.__activity_tubes[obj_id].get_num_frames() > 0:  # Skip first box as we have no history
                old_box = self.__activity_tubes[obj_id].get_data()[-1].box
                smoothed_box = self.smooth_box(old_box, box)

            # get box
            x1, y1, x2, y2 = *smoothed_box.upper_left, *smoothed_box.lower_right

            data = frame[y1:y2, x1:x2].astype(np.uint8)
            self.__activity_tubes[obj_id].add_trackable(ObjectTrackable(smoothed_box, data))

    def get_activity_tubes(self):
        return list(self.__activity_tubes.values())

    def clear(self):
        self.__activity_tubes = {}

    def smooth_box(self, old_box, current_box):
        box = current_box

        if self.alpha_size > 0:
            box = self.smooth_box_size(old_box, current_box)
        if self.alpha_loc > 0:
            box = self.smooth_box_location(old_box, box)
        return box

    def smooth_box_size(self, old_box, current_box):
        alpha = self.alpha_size

        x1, y1, x2, y2 = *current_box.upper_left, *current_box.lower_right
        coordinates = np.array([x1, y1, x2, y2])

        x1_old, y1_old, x2_old, y2_old = *old_box.upper_left, *old_box.lower_right

        v_dist, h_dist = x2 - x1, y2 - y1
        v_dist_old, h_dist_old = x2_old - x1_old, y2_old - y1_old

        v_dist_new = alpha * v_dist_old + (1 - alpha) * v_dist
        h_dist_new = alpha * h_dist_old + (1 - alpha) * h_dist

        v_dist_delta = v_dist - v_dist_new
        h_dist_delta = h_dist - h_dist_new

        deltas = np.array([-v_dist_delta, -h_dist_delta, v_dist_delta, h_dist_delta])
        x1, y1, x2, y2 = (coordinates - deltas / 2).astype(int)     # TODO clip values to not exceed frame boundaries
        box = BoundingBox((x1, y1), (x2, y2))

        return box

    def smooth_box_location(self, old_box, current_box):
        alpha = self.alpha_loc

        x1, y1, x2, y2 = *current_box.upper_left, *current_box.lower_right
        coordinates = np.array([x1, y1, x2, y2])

        x1_old, y1_old, x2_old, y2_old = *old_box.upper_left, *old_box.lower_right
        old_coordinates = np.array([x1_old, y1_old, x2_old, y2_old])

        x1, y1, x2, y2 = (alpha * old_coordinates + (1 - alpha) * coordinates).astype(int)
        box = BoundingBox((x1, y1), (x2, y2))

        return box
