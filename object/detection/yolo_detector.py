import sys
sys.path.append('/home/muhammed-kamal/Desktop/darkflow')
import cv2
from darkflow.net.build import TFNet
from object.detection.abstract_object_detector import *

class YoloDetector(AbstractObjectDetector):

	def __init__(self,arg):
		super(YoloDetector, self).__init__()
		options = {
    		'model': 'cfg/yolo.cfg',
    		'load': 'bin/yolo.weights',
    		'threshold': 0.3
		}
		self.tfnet = TFNet(options)



	def detect(self, frame: Array[np.int]) -> List[BoundingBox]:
		img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		result = self.tfnet.return_predict(img)
		detections = []
		for res in result:
			if res['label'] == 'person':
				tl = (res['topleft']['x'], res['topleft']['y'])
				br = (res['bottomright']['x'], res['bottomright']['y'])
				detections.append(BoundingBox(tl,br))
		return detections