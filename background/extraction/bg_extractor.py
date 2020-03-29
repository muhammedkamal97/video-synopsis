import numpy as np
from nptyping import Array
import cv2 as cv
from background.extraction.abstact_bg_extractor import AbstractBGExtractor


class BGExtractor(AbstractBGExtractor):
    
    def __init__(self):
        self.backSub = cv.createBackgroundSubtractorKNN()
        
    def extract_background(self, frame: Array[np.int]) -> Array[np.int]:
        fgMask = self.backSub.apply(frame)
        return self.backSub.getBackgroundImage()
    pass
