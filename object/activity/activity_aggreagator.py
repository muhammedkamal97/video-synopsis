from typing import List
from object.activity.object_trackable import ObjectTrackable


class ActivityAggregator:
    def __init__(self):
        self.__activity_tubes = {}

    def aggregate(self, trackables: List[ObjectTrackable]):
        pass
