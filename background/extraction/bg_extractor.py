import numpy as np
from nptyping import Array
import cv2 as cv
from background.extraction.abstact_bg_extractor import AbstractBGExtractor


class BGExtractor(AbstractBGExtractor):
    def extract_background(self, frame: Array[np.int]) -> Array[np.int]:
        backSub = cv.createBackgroundSubtractorKNN()
        # backSub = cv.createBackgroundSubtractorMOG2()
        fgMask = backSub.apply(frame)
        return backSub.getBackgroundImage();