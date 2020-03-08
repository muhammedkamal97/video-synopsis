import numpy as np
from nptyping import Array
import cv2 as cv
from skimage.measure import compare_ssim
from background.extraction.abstract_bg_selector import AbstractBGSelector

class BGSelector(AbstractBGSelector):
   
    background_mapper = {}
    list_of_bgs = []
    is_first_frame = True
    count = 0 

    def consume(self, background_frame: Array[np.int], frame_no: int):
        
        if is_first_frame:
            background_mapper[frame_no] = count
            list_of_bgs.append(background_frame)
            count += 1
            is_first_frame = False
        else :
            (score, diff) = compare_ssim(background_frame, list_of_bgs[count-1], full = True,  multichannel=True)
            if score >= 0.75: # to be tunned
                background_mapper[frame_no] = count - 1
            else :
                background_mapper[frame_no] = count
                list_of_bgs.append(background_frame)
                count +=1
        
    def map(self, frame_no: int) -> Array[np.int]:
        return list_of_bgs[background_mapper[frame_no]]
