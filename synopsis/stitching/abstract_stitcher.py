import numpy as np
from typing import List, NoReturn
from nptyping import Array
from abc import ABC, abstractmethod

from background.selection.abstract_bg_selector import AbstractBGSelector
from object.activity.activity_tube import ActivityTube


class AbstractStitcher(ABC):
    # TODO: Modify class to use a separate data structure for background frames

    activity_tubes: List[ActivityTube]
    schedule: List[int]
    bg_selector: AbstractBGSelector

    def __init__(self):
        self.activity_tubes = None
        self.schedule = None
        self.bg_selector = None

    @abstractmethod
    def initialize(self, activity_tubes: List[ActivityTube], schedule: List[int], bg_selector: AbstractBGSelector
                   , input_frame_count: int) -> NoReturn:
        pass

    @abstractmethod
    def has_next_frame(self) -> bool:
        pass

    @abstractmethod
    def next_frame(self) -> Array[np.uint8]:
        pass

