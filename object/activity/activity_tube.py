from typing import List

from object.activity.object_trackable import ObjectTrackable


class ActivityTube:
    def __init__(self, trackables: List[ObjectTrackable] = None):
        if trackables is None:
            trackables = []
        self.__data = list(trackables)

    def get_data(self):
        return self.__data

    def add_trackable(self, trackable: ObjectTrackable):
        self.__data.append(trackable)
