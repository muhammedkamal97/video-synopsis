import cv2
import json
import os
from object.detection.abstract_object_detector import *


class CachDetector(AbstractObjectDetector):
    
    def __init__(self,arg):
        super(CachDetector, self).__init__()
        with open(os.path.sep.join(['cach_detector', arg['video_name']])) as json_file:
            self.detections = json.load(json_file)
        

    def detect(self, frame: Array[np.uint8], frame_count) -> List[BoundingBox]:
        boxes = []
        if str(frame_count) not in self.detections:
            return None 
        for box in self.detections[str(frame_count)]:
            l = (box['upper_left'][0], box['upper_left'][1])
            r = (box['lower_right'][0], box['lower_right'][1])
            boxes.append(BoundingBox(l, r))
        return merge_boxes(boxes,frame.shape[1],frame.shape[0])
