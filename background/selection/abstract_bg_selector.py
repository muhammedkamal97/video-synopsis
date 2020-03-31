import numpy as np
from nptyping import Array
from abc import ABC, abstractmethod


class AbstractBGSelector(ABC):

    @abstractmethod
    def consume(self, background_frame: Array[np.uint8]):
        pass

    @abstractmethod
    def map(self, frame_no: int) -> Array[np.uint8]:
        pass
