from abstract_scheduler import AbstractScheduler
from object.activity.activity_tube import ActivityTube


class BasicScheduler(AbstractScheduler):

    def schedule(self, activity_tubes: List[ActivityTube]) -> List[int]:
        start_frames = []
        for i in range(1, len(activity_tubes)):
            start_frame = -1
            for j in range(i):
                start_frame = max([_get_uncolide_start_frame(activity_tubes[j], activity_tubes[i]), start_frame])
            start_frames.append(start_frame)
        return start_frames
