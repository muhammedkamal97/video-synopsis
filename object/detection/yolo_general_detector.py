import cv2
import json
import os
from PIL import Image
from object.detection.abstract_object_detector import *
from object.detection.YOLO.yolo import *


class generalDetector(AbstractObjectDetector):
    
    def __init__(self,arg):
        super(generalDetector, self).__init__()
        self.yolo_model = YOLO_np()

    def detect(self, frame: Array[np.uint8], frame_count) -> List[BoundingBox]:
        boxes = []
        image = Image.fromarray(frame)
        out_boxes, out_classes = self.yolo_model.detect_image(image) 
        
        for box, cl in zip(out_boxes, out_classes):
            xmin, ymin, xmax, ymax = box
            #TODO change the number
            if cl == 14:#14 stand for person
                boxes.append(BoundingBox((xmin, ymin), (xmax, ymax)))
        
        return boxes
