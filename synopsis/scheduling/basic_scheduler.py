from typing import List

from synopsis.scheduling.abstract_scheduler import AbstractScheduler
from synopsis.scheduling.scheduler_utils import *


class BasicScheduler(AbstractScheduler):

    def schedule(self, activity_tubes: List[ActivityTube]) -> List[int]:
        start_frames = [0]
        for i in range(1, len(activity_tubes)):
            cur_frame = start_frames[i-1]
            while not can_put_activity_tube_in_frame(activity_tubes[i], cur_frame, activity_tubes[:i], start_frames[:i]):
                cur_frame += 1
            start_frames.append(cur_frame)
        return start_frames
