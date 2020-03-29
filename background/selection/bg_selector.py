import numpy as np
from nptyping import Array
from skimage.metrics import structural_similarity
from background.selection.abstract_bg_selector import AbstractBGSelector


class BGSelector(AbstractBGSelector):

    def __init__(self):
        self.background_mapper = {}
        self.list_of_bgs = []
        self.is_first_frame = True
        self.count = 0
        self.frame_no = 0

    def consume(self, background_frame: Array[np.int]):
        
        if self.is_first_frame:
            self.background_mapper[self.frame_no] = self.count
            self.list_of_bgs.append(background_frame)
            self.count += 1
            self.is_first_frame = False
        else:
            (score, diff) = structural_similarity(
                background_frame, self.list_of_bgs[self.count-1],
                full=True,
                multichannel=True)
            if score >= 0.9:  # to be tuned
                self.background_mapper[self.frame_no] = self.count - 1
            else :
                self.background_mapper[self.frame_no] = self.count
                self.list_of_bgs.append(background_frame)
                self.count += 1
        self.frame_no += 1
        
    def map(self, frame_no: int) -> Array[np.int]:
        return self.list_of_bgs[self.background_mapper[frame_no]]
    
    def clear(self):
        self.__init__()
