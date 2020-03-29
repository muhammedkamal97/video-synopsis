import cv2 as cv
from cv2 import VideoCapture, VideoWriter
from background.extraction.bg_extractor import BGExtractor
from background.selection.bg_selector import BGSelector
from object.preprocessing.abstract_preprocessor import AbstractPreprocessor
from object.activity.activity_aggreagator import ActivityAggregator
from object.detection.cach_detector import CachDetector
from object.preprocessing.abstract_preprocessor import AbstractPreprocessor
from object.tracking.sort_tracker import SortTracker
from synopsis.chopping.abstract_synopsis_chopper import AbstractSynopsisChopper
from synopsis.scheduling.basic_scheduler import BasicScheduler
from synopsis.stitching.abstract_stitcher import AbstractStitcher
from master.master import Master


cap = VideoCapture('12_47.mp4')
out = VideoWriter('output.mp4', 0x7634706d, 10, (400, 400))

bg_extractor = BGExtractor()
bg_selector = BGSelector()
# preprocessor = AbstractPreprocessor()
object_detector = CachDetector({'video_name': '12_47.json'})
object_tracker = SortTracker()
activity_aggregator = ActivityAggregator()
# chopper = AbstractSynopsisChopper()
scheduler = BasicScheduler()
# stitcher = AbstractStitcher()

slaves = {
    'bg_extractor': bg_extractor,
    'bg_selector': bg_selector,
    # 'preprocessor': preprocessor,
    'object_detector': object_detector,
    'object_tracker': object_tracker,
    'activity_aggregator': activity_aggregator,
    # 'chopper': chopper,
    'scheduler': scheduler,
    # 'stitcher': stitcher
}

master = Master(slaves)
master.run(cap, out)

