from typing import List

from synopsis.scheduling.abstract_scheduler import AbstractScheduler
from synopsis.scheduling.scheduler_utils import *


class LongestFirstIntScheduler(AbstractScheduler):

    def __init__(self, rate):
        self.rate = rate

    def schedule(self, activity_tubes: List[ActivityTube]) -> List[int]:
        new_activity_tubes = [(act, i) for i, act in enumerate(activity_tubes)]
        new_activity_tubes.sort(key=lambda x: x[0].get_num_frames(), reverse=True)
        frame_boxes = []
        start_frames = [0 for i in activity_tubes]
        start_frames[new_activity_tubes[0][1]] = 0
        add_activity_to_frame_boxes(new_activity_tubes[0][0], 0, frame_boxes)
        for i in range(1, len(new_activity_tubes)):
            cur_frame = 0
            while not can_put_activity_tube_in_frame_boxes_int(new_activity_tubes[i][0], cur_frame, frame_boxes, self.rate):
                cur_frame += 1
            start_frames[new_activity_tubes[i][1]] = cur_frame
            add_activity_to_frame_boxes(new_activity_tubes[i][0], cur_frame, frame_boxes)
        return start_frames
