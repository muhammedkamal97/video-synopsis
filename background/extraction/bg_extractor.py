import numpy as np
from nptyping import Array
import cv2 as cv
from background.extraction.abstact_bg_extractor import AbstractBGExtractor


class BGExtractor(AbstractBGExtractor):
    
    def __init__(self, skip_frames: int):
        self.backSub = cv.createBackgroundSubtractorMOG2()
        self.i = 0
        self.skip_frames = skip_frames
        self.back_ground = None

    def extract_background(self, frame: Array[np.uint8]) -> Array[np.uint8]:
        if self.i in range(10) or self.i % self.skip_frames == 0:
            fgMask = self.backSub.apply(frame)
            self.back_ground = self.backSub.getBackgroundImage()
        self.i +=1
        return self.back_ground
