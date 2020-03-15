import numpy as np
from nptyping import Array
import cv2 as cv
from skimage.measure import compare_ssim
from background.extraction.abstract_bg_selector import AbstractBGSelector

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
        else :
            (score, diff) = compare_ssim(background_frame, self.list_of_bgs[self.count-1], full = True,  multichannel=True)
            if score >= 0.9: # to be tunned
                self.background_mapper[self.frame_no] = self.count - 1
            else :
                self.background_mapper[self.frame_no] = self.count
                self.list_of_bgs.append(background_frame)
                self.count +=1
        self.frame_no +=1
        
    def map(self, frame_no: int) -> Array[np.int]:
        return self.list_of_bgs[self.background_mapper[frame_no]]
    
    def clear(self):
        self.__init__()