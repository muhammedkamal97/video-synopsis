import numpy as np
import cv2 as cv
from nptyping import Array
from skimage.metrics import structural_similarity
from background.selection.abstract_bg_selector import AbstractBGSelector


class BGSelector(AbstractBGSelector):

    def __init__(self):
        self.background_mapper = {}
        self.list_of_bgs = []
        self.is_first_frame = True
        self.count = 0
        self.top_frame = None

    def consume(self, background_frame: Array[np.int], frame_no: int):

        resized_image_curr = cv.resize(background_frame, (100, 100))
        
        if self.is_first_frame:
            self.background_mapper[frame_no] = self.count
            self.list_of_bgs.append(background_frame)
            self.count += 1
            self.is_first_frame = False
            self.top_frame = resized_image_curr
        else:
            (score, diff) = structural_similarity(
                resized_image_curr, self.top_frame, full=True, multichannel=True)
            if score >= 0.75:  # to be tuned
                self.background_mapper[frame_no] = self.count - 1
            else:
                self.background_mapper[frame_no] = self.count
                self.list_of_bgs.append(background_frame)
                self.count += 1
                self.top_frame = resized_image_curr

    def map(self, frame_no: int) -> Array[np.int]:
        return self.list_of_bgs[self.background_mapper[frame_no]]
    
    def clear(self):
        self.__init__()
