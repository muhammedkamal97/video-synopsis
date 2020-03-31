import numpy as np
from nptyping import Array
import cv2 as cv
from background.extraction.abstact_bg_extractor import AbstractBGExtractor


class BGExtractor(AbstractBGExtractor):
    
    def __init__(self):
        self.backSub = cv.createBackgroundSubtractorMOG2()
        self.i = 0

    def extract_background(self, frame: Array[np.uint8]) -> Array[np.uint8]:
        fgMask = self.backSub.apply(frame)
        return self.backSub.getBackgroundImage()
    pass
