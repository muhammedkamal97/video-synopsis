import numpy as np
from nptyping import Array
from abc import ABC, abstractmethod


class AbstractBGExtractor(ABC):

    @abstractmethod
    def extract_background(self, frame: Array[np.int]) -> Array[np.int]:

        pass
