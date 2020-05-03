import time
from datetime import datetime

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

import os, psutil


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

    start_time: datetime

    MODULES = [
        'bg_extractor',
        'bg_selector',
        # 'preprocessor',
        'object_detector',
        'object_tracker',
        'activity_aggregator',
        # 'chopper',
        'scheduler',
        'stitcher'
    ]

    def __init__(self, slaves: dict):
        for m in Master.MODULES:
            setattr(self, m, slaves[m])
        self.fps = 0

    def run(self, capture: VideoCapture, writer: VideoWriter, start_time: datetime):
        if not capture.isOpened():
            raise Exception("Capture not open")
        if not writer.isOpened():
            raise Exception("Writer not open")

        self.fps = capture.get(cv.CAP_PROP_FPS)
        self.start_time = start_time

        pid = os.getpid()
        print("pid=", pid)
        ps = psutil.Process(pid)

        t = time.time()

        frame_count = 0
        while True:
            try:
                ret, frame = capture.read()

                if not ret or frame_count == 25000:
                    print("time from start: %.2f minutes" % ((time.time() - t) / 60))
                    self.construct_synopsis(writer, frame_count, start_time)
                    break

                self.model_background(frame, frame_count)

                frame_count += 1

                if frame_count % 1000 == 0:
                    print("--------- Checkpoint -----------")
                    print("number of frames ", frame_count)
                    print("memory: ", int(ps.memory_info().rss / (1024 * 1024)), "MB")
                    print("time from start: %.2f minutes" % ((time.time() - t) / 60))

                # frame = self.preprocessor.process(frame)
                if frame is None:
                    continue

                self.process_frame(frame, frame_count)
                del frame

                # if self.chop_synopsis():
                #     self.construct_synopsis(writer, frame_count, start_time)

            except KeyboardInterrupt:
                print("Handling KeyboardInterrupt. Generating Synopsis...")
                self.construct_synopsis(writer, frame_count, start_time)
                raise

    def model_background(self, frame: Array[np.uint8], frame_count: int):
        bg_frame = self.bg_extractor.extract_background(frame)
        self.bg_selector.consume(bg_frame, frame_count)
        pass

    def process_frame(self, frame: Array[np.uint8], frame_count: int = 1):
        detected_boxes = self.object_detector.detect(frame, frame_count)
        object_ids = self.object_tracker.track(frame, detected_boxes)
        self.activity_aggregator.aggregate(frame, detected_boxes, object_ids, frame_count)

    def chop_synopsis(self):
        self.chopper.to_chop(self.activity_aggregator)

    # TODO: use a separate data structure for background frames with stitcher
    def construct_synopsis(self, writer: VideoWriter, frame_count: int, start_time: datetime):
        activity_tubes = self.activity_aggregator.get_activity_tubes()
        schedule = self.scheduler.schedule(activity_tubes)
        self.stitcher.initialize(activity_tubes, schedule, self.bg_selector, frame_count, self.fps, start_time)
        print(len(activity_tubes))
        print(schedule)

        t1 = time.time()
        while self.stitcher.has_next_frame():
            n = self.stitcher.next_frame()
            writer.write(n)
        print("stitching time : %.2f minutes" % ((time.time() - t1) / 60))

        self.activity_aggregator.clear()
        self.bg_selector.clear()
