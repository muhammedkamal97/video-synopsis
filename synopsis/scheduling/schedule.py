from typing import List

from object.activity.activity_tube import ActivityTube


class Schedule:

    def __init__(self, activity_tubes: List[ActivityTube]):
        self.__start_frames = [-1 for x in activity_tubes]
        self.__activity_tubes = activity_tubes
        self.__frame_boxes = []

    def set_activity_tube_num_at(self, tube_ind: int, frame_num: int):
        self.__start_frames[tube_ind] = frame_num
        activity_tube = self.__activity_tubes[tube_ind]
        while len(self.__frame_boxes) <= frame_num + activity_tube.get_num_frames():
            self.__frame_boxes.append([])
        for i in range(activity_tube.get_num_frames()):
            self.__frame_boxes[frame_num + i].append(activity_tube.get_data()[i].box)

    def get_start_frames(self):
        return self.__start_frames

    def get_activity_tubes(self):
        return self.__activity_tubes

    def get_video_length(self):
        output_length = 0
        for i in range(len(self.__activity_tubes)):
            output_length = max(output_length, self.__activity_tubes[i].get_num_frames() + self.__start_frames[i])
        return output_length

    def get_frame_boxes(self):
        return self.__frame_boxes