from typing import List

from object.activity.object_trackable import ObjectTrackable


class ActivityTube:
    def __init__(self, start_frame, trackables: List[ObjectTrackable] = None):
        self.start_frame = start_frame
        if trackables is None:
            trackables = []
        self.__data = list(trackables)

    def get_data(self) -> List[ObjectTrackable]:
        return self.__data

    def get_num_frames(self) -> int:
        return len(self.__data)

    def add_trackable(self, trackable: ObjectTrackable):
        self.__data.append(trackable)
