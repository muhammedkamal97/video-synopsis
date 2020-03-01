import numpy as np
from nptyping import Array
import cv2 as cv
from cv2 import VideoCapture, VideoWriter

from background.extraction.abstact_bg_extractor import AbstractBGExtractor
from background.selection.abstract_bg_selector import AbstractBGSelector
from object.activity.activity_aggreagator import ActivityAggregator
from object.detection.abstract_object_detector import AbstractObjectDetector
from object.preprocessing.abstract_preprocessor import AbstractPreprocessor
from object.tracking.abstract_object_tracker import AbstractObjectTracker
from synopsis.chopping.abstract_synopsis_chopper import AbstractSynopsisChopper
from synopsis.scheduling.abstract_scheduler import AbstractScheduler
from synopsis.stitching.abstract_stitcher import AbstractStitcher


class Master:
    bg_extractor: AbstractBGExtractor
    bg_selector: AbstractBGSelector

    preprocessor: AbstractPreprocessor
    object_detector: AbstractObjectDetector
    object_tracker: AbstractObjectTracker
    activity_aggregator: ActivityAggregator

    chopper: AbstractSynopsisChopper
    scheduler: AbstractScheduler
    stitcher: AbstractStitcher

    MODULES = [
        'bg_extractor',
        'bg_selector',
        'preprocessor',
        'object_detector',
        'object_tracker',
        'activity_aggregator',
        'chopper',
        'scheduler',
        'stitcher'
    ]

    def __init__(self, slaves: dict):
        for m in Master.MODULES:
            setattr(self, m, slaves[m])

    def run(self, capture: VideoCapture, writer: VideoWriter):
        if not capture.isOpened():
            raise Exception("Capture not open")
        if not writer.isOpened():
            raise Exception("Writer not open")

        while True:
            ret, frame = capture.read()
            if not ret:
                self.construct_synopsis(writer)
                break

            self.model_background(frame)

            frame = self.preprocessor.process(frame)
            if frame is None:
                continue

            self.process_frame(frame)
            if self.chop_synopsis():
                self.construct_synopsis(writer)

            if cv.waitKey(1) == ord('q'):
                self.construct_synopsis(writer)
                break

    def model_background(self, frame: Array[np.int]):
        bg_frame = self.bg_extractor.extract_background(frame)
        self.bg_selector.consume(bg_frame)

    def process_frame(self, frame: Array[np.int]):
        detected_boxes = self.object_detector.detect(frame)
        object_ids = self.object_tracker.track(frame, detected_boxes)
        self.activity_aggregator.aggregate(frame, detected_boxes, object_ids)

    def chop_synopsis(self):
        self.chopper.to_chop(self.activity_aggregator)

    def construct_synopsis(self, writer: VideoWriter):
        activity_tubes = self.activity_aggregator.get_activity_tubes()
        schedule = self.scheduler.schedule(activity_tubes)
        # TODO: pass background selector to stitcher?
        self.stitcher.initialize(activity_tubes, schedule)

        while self.stitcher.has_next_frame():
            writer.write(self.stitcher.next_frame())

        self.activity_aggregator.clear()
        # TODO: clear background selector?
