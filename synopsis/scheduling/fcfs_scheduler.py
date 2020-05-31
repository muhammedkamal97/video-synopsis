from typing import List

from synopsis.scheduling.abstract_scheduler import AbstractScheduler
from synopsis.scheduling.scheduler_utils import *

class FCFSScheduler(AbstractScheduler):

    def schedule(self, activity_tubes: List[ActivityTube]) -> List[int]:
        frame_boxes = []
        start_frames = [0]
        add_activity_to_frame_boxes(activity_tubes[0], 0, frame_boxes)
        for i in range(1, len(activity_tubes)):
            cur_frame = 0
            while not can_put_activity_tube_in_frame_boxes(activity_tubes[i], cur_frame, frame_boxes):
                cur_frame += 1
            start_frames.append(cur_frame)
            add_activity_to_frame_boxes(activity_tubes[i], cur_frame, frame_boxes)
        return start_frames
