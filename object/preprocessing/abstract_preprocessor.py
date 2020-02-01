import numpy as np
from nptyping import Array
from abc import ABC, abstractmethod


class AbstractPreprocessor(ABC):

    @abstractmethod
    def process(self, frame: Array[np.int]):
        """
        :param frame:
        :return processed frame or None if the frame is to be skipped:
        """
        pass
