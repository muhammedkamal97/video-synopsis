from object.activity.object_trackable import ObjectTrackable


class ActivityTube:
    def __init__(self):
        self.__data = []

    def get_data(self):
        return self.__data

    def add_trackable(self, trackable: ObjectTrackable):
        self.__data.append(trackable)
