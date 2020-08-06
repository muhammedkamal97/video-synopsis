from synopsis.scheduling.abstract_scheduler import AbstractScheduler
from synopsis.scheduling.schedule import Schedule
from synopsis.scheduling.scheduler_utils import *


class FirstInFirstOutScheduler(AbstractScheduler):

    def __init__(self, sort_by="None", max_boxes=0, intersection_ratio=0):
        self.max_boxes = max_boxes
        self.intersection_ratio = intersection_ratio
        self.sort_by = sort_by
        if sort_by == "None" or sort_by == "Sorted":
            self.__sort_function = None
        elif sort_by == "Longest":
            self.__sort_function = lambda x: -x[0].get_num_frames()
        elif sort_by == "Total Area":
            def get_total_area(x) -> int:
                sum = 0
                for trackable in x[0].get_data():
                    sum += get_box_area(trackable.box)
                return -sum

            self.__sort_function = get_total_area
        elif sort_by == "Avg Area":
            def get_avg_area(x) -> int:
                sum = 0
                for trackable in x[0].get_data():
                    sum += get_box_area(trackable.box)
                return -sum / x[0].get_num_frames()

            self.__sort_function = get_avg_area

    def __can_put_activity_tube_in_frame(self, act: ActivityTube, frame_num: int, schedule: Schedule) -> bool:
        frame_boxes = schedule.get_frame_boxes()
        for i in range(frame_num, frame_num + act.get_num_frames()):
            if i >= len(frame_boxes):
                break
            boxes = frame_boxes[i]
            if self.max_boxes != 0 and len(boxes) + 1 > self.max_boxes:
                return False
            for box in boxes:
                if get_boxes_int_rate(box, act.get_data()[i - frame_num].box) > self.intersection_ratio:
                    return False
        return True

    def schedule(self, activity_tubes: List[ActivityTube]) -> Schedule:
        new_activity_tubes = [(act, i) for i, act in enumerate(activity_tubes)]
        if self.__sort_function is not None:
            new_activity_tubes.sort(key=self.__sort_function)
        schedule = Schedule(activity_tubes)
        schedule.set_activity_tube_num_at(new_activity_tubes[0][1], 0)
        cur_frame = 0
        for i in range(1, len(new_activity_tubes)):
            if self.sort_by != "None":
                cur_frame = 0
            while not self.__can_put_activity_tube_in_frame(new_activity_tubes[i][0], cur_frame, schedule):
                cur_frame += 1
            schedule.set_activity_tube_num_at(new_activity_tubes[i][1], cur_frame)
        return schedule.get_start_frames()
