import numpy as np
from typing import List, NoReturn
from nptyping import Array

from object.activity.bounding_box import BoundingBox


class ObjectTrackable:
    def __init__(self, bounding_box: BoundingBox, data: Array[np.uint8]):
        self.box = bounding_box
        self.data = data
