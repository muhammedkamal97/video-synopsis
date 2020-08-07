import string
import time
from datetime import datetime
import multiprocessing

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

	def run(self, video_path: string, writer: VideoWriter, start_time: datetime):
		if not writer.isOpened():
			raise Exception("Writer not open")

		self.start_time = start_time

		pid = os.getpid()
		print("master pid=", pid)

		manager = multiprocessing.Manager()
		resources = manager.dict()

		background_process = multiprocessing.Process(target=self.background_extractor_worker, args=(video_path, resources))
		synopsis_process = multiprocessing.Process(target=self.synopsis_processor_worker, args=(video_path, resources))

		background_process.start()
		synopsis_process.start()

		background_process.join()
		synopsis_process.join()

		self.activity_aggregator = resources['activity_aggregator']
		self.bg_selector = resources['bg_selector']
		self.fps = resources['fps']

		print("****** Frame Count: ", resources['frame_count'])
		print("****** Activity Tubes: ", len(self.activity_aggregator.get_activity_tubes()))

		self.construct_synopsis(writer, resources['frame_count'], start_time)

	def background_extractor_worker(self, video_path: string, resources):
		capture = VideoCapture(video_path)
		if not capture.isOpened():
			raise Exception("Capture not open")
		resources['fps'] = capture.get(cv.CAP_PROP_FPS)

		pid = os.getpid()
		print("background pid=", pid)
		ps = psutil.Process(pid)

		t = time.time()

		count = 0
		while True:
			try:
				ret, frame = capture.read()

				if not ret:
					resources['bg_selector'] = self.bg_selector
					resources['frame_count'] = count
					return

				self.model_background(frame, count)
				count += 1

				if count % 1000 == 0:
					print("--------- Checkpoint: Background -----------")
					print("number of frames ", count)
					print("memory: ", int(ps.memory_info().rss / (1024 * 1024)), "MB")
					print("time from start: %.2f minutes" % ((time.time() - t) / 60))

				if frame is None:
					continue

				del frame

			# if self.chop_synopsis():
			#     self.construct_synopsis(writer, frame_count, start_time)

			except KeyboardInterrupt:
				resources['bg_selector'] = self.bg_selector
				resources['frame_count'] = count
				return

	def synopsis_processor_worker(self, video_path: string, resources):
		capture = VideoCapture(video_path)
		if not capture.isOpened():
			raise Exception("Capture not open")

		pid = os.getpid()
		print("synopsis pid=", pid)
		ps = psutil.Process(pid)

		t = time.time()

		frame_count = 0
		while True:
			try:
				ret, frame = capture.read()

				if not ret:
					resources['activity_aggregator'] = self.activity_aggregator
					return

				frame_count += 1

				if frame_count % 1000 == 0:
					print("--------- Checkpoint: Synopsis -----------")
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
				resources['activity_aggregator'] = self.activity_aggregator
				return

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

		self.log_synopsis_tubes(schedule, activity_tubes)

		t1 = time.time()
		while self.stitcher.has_next_frame():
			n = self.stitcher.next_frame()
			writer.write(n)
		print("stitching time : %.2f minutes" % ((time.time() - t1) / 60))

		self.activity_aggregator.clear()
		self.bg_selector.clear()

	def log_synopsis_tubes(self, schedule, activity_tubes):
		tubes_lengths = list(map(lambda x: x.get_num_frames(), activity_tubes))

		print('=============================')
		print('Number of activity tubes = ' + str(len(activity_tubes)))
		fmt = '{:<8}{:<20}{}'
		print(fmt.format('', 'Start Frame', 'Length'))
		for i, (start_frame, frame_count) in enumerate(zip(schedule, tubes_lengths)):
			print(fmt.format(i, start_frame, frame_count))
