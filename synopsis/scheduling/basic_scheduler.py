from typing import List

from synopsis.scheduling.abstract_scheduler import AbstractScheduler
from synopsis.scheduling.scheduler_utils import *


class BasicScheduler(AbstractScheduler):

    def schedule(self, activity_tubes: List[ActivityTube]) -> List[int]:
        start_frames = [0]
        for i in range(1, len(activity_tubes)):
            start_frame = -1
            for j in range(i):
                start_frame = max([get_uncollide_start_frame(activity_tubes[j], activity_tubes[i]), start_frame])
            start_frames.append(start_frame)
        return start_frames
