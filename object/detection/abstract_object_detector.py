import numpy as np
from nptyping import Array
from typing import List
from abc import ABC, abstractmethod

from object.activity.bounding_box import BoundingBox
from object.detection.utils import *

class AbstractObjectDetector(ABC):

    @abstractmethod
    def detect(self, frame: Array[np.uint8]) -> List[BoundingBox]:
        pass
