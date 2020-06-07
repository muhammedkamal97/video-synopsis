from datetime import datetime

import cv2 as cv
import json
from builder import build_master
from cv2 import VideoCapture, VideoWriter
from background.extraction.bg_extractor import BGExtractor
from background.selection.bg_selector import BGSelector
from object.preprocessing.abstract_preprocessor import AbstractPreprocessor
from object.activity.activity_aggreagator import ActivityAggregator
from object.detection.cach_detector import CachDetector
from object.tracking.sort_tracker import SortTracker
from object.tracking.deep_sort_tracker import DeepSortTracker
from synopsis.chopping.abstract_synopsis_chopper import AbstractSynopsisChopper
from synopsis.scheduling.basic_scheduler import BasicScheduler
from synopsis.scheduling.longest_first_scheduler import LongestFirstScheduler
from synopsis.scheduling.longest_first_int_scheduler import LongestFirstIntScheduler
from synopsis.stitching.stitcher import Stitcher
from master.master import Master
from object.detection.mov_object_detection import movObjectDetector
from object.detection.yolo_general_detector import generalDetector


config = {}
with open('config.json') as json_file:
    config = json.load(json_file)



cap = VideoCapture(config['video_input'])

width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv.CAP_PROP_FPS)

codec = cv.VideoWriter_fourcc('M', 'J', 'P', 'G')
out = cv.VideoWriter(config['video_output'], cv.VideoWriter_fourcc(*'XVID'), fps, (width, height))
start_time = datetime.strptime('22/10/2019 12:47:38', '%d/%m/%Y %H:%M:%S')


bg_extractor = BGExtractor(1000)
bg_selector = BGSelector(1000)
# preprocessor = AbstractPreprocessor()
object_detector = CachDetector({'video_name': '12_47.json'})
object_tracker = DeepSortTracker()
activity_aggregator = ActivityAggregator()
# chopper = AbstractSynopsisChopper()
scheduler = LongestFirstScheduler()
stitcher = Stitcher(segmentation=True)
#object_detector = movObjectDetector(None)

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


slaves = build_master(config)
master = Master(slaves)
master.run(cap, out, start_time)

