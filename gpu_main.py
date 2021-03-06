import cv2 as cv
from cv2 import VideoCapture, VideoWriter
from background.extraction.bg_extractor import BGExtractor
from background.selection.bg_selector import BGSelector
from object.preprocessing.abstract_preprocessor import AbstractPreprocessor
from object.activity.activity_aggreagator import ActivityAggregator
from object.detection.yolo_detector import YoloDetector
from object.tracking.sort_tracker import SortTracker
from synopsis.chopping.abstract_synopsis_chopper import AbstractSynopsisChopper
from synopsis.scheduling.basic_scheduler import BasicScheduler
from synopsis.stitching.stitcher import Stitcher
from master.master import Master
from datetime import datetime


cap = VideoCapture('12_47.mp4')
# out = VideoWriter('output.mp4', 0x7634706d, 10, (400, 400))
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
# fps = cap.get(cv.CAP_PROP_XI_FRAMERATE)

codec = cv.VideoWriter_fourcc('M', 'J', 'P', 'G')
out = cv.VideoWriter('output.avi', codec, 25, (width, height))
start_time = datetime.strptime('22/10/2019 12:47:38', '%d/%m/%Y %H:%M:%S')

bg_extractor = BGExtractor(1000)
bg_selector = BGSelector(1000)
# preprocessor = AbstractPreprocessor()
object_detector = YoloDetector(None)
object_tracker = SortTracker()
activity_aggregator = ActivityAggregator()
# chopper = AbstractSynopsisChopper()
scheduler = BasicScheduler()
stitcher = Stitcher()

slaves = {
    'bg_extractor': bg_extractor,
    'bg_selector': bg_selector,
    # 'preprocessor': preprocessor,
    'object_detector': object_detector,
    'object_tracker': object_tracker,
    'activity_aggregator': activity_aggregator,
    # 'chopper': chopper,
    'scheduler': scheduler,
    'stitcher': stitcher
}

master = Master(slaves)
master.run(cap, out, start_time)

