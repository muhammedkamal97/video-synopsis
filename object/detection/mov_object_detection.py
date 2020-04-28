from object.detection.abstract_object_detector import *
import cv2
class movObjectDetector(AbstractObjectDetector):
    def __init__(self,arg):
        self.prev_frame = None

    def detect(self, frame: Array[np.uint8], frame_count) -> List[BoundingBox]:
        if self.prev_frame is None:
            self.prev_frame = frame
            return []
        boxes = []
        diff = cv2.absdiff(self.prev_frame, frame)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)

            if cv2.contourArea(contour) < 700:
                continue
            boxes.append(BoundingBox((x,y),(x+w,y+h)))
        del self.prev_frame
        self.prev_frame = frame
        return boxes
