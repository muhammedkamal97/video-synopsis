import cv2
from pydarknet import Detector, Image
from object.detection.abstract_object_detector import *

class YoloDetector(AbstractObjectDetector):

	def __init__(self,arg):
		super(YoloDetector, self).__init__()
		self.net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), 
                      bytes("weights/yolov3.weights", encoding="utf-8"), 0,
                   bytes("cfg/coco.data", encoding="utf-8"))



	def detect(self, frame: Array[np.int]) -> List[BoundingBox]:
		fr = Image(frame)
		results = self.net.detect(fr)
		del fr
		detections = []
		for cat, score, bounds in results:
			clss = str(cat.decode("utf-8"))
			print(clss)
			if clss == 'person':
				x, y, w, h = bounds
				detections.append(BoundingBox((int(x-w/2),int(y-h/2)),(int(x+w/2),int(y+h/2))))
		return detections

  

      