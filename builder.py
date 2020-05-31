from background.extraction.bg_extractor import BGExtractor
from background.selection.bg_selector import BGSelector
from object.preprocessing.abstract_preprocessor import AbstractPreprocessor
from object.activity.activity_aggreagator import ActivityAggregator
from object.detection.cach_detector import CachDetector
from object.tracking.sort_tracker import SortTracker
from synopsis.chopping.abstract_synopsis_chopper import AbstractSynopsisChopper
from synopsis.scheduling.basic_scheduler import BasicScheduler
from synopsis.stitching.stitcher import Stitcher
from object.detection.mov_object_detection import movObjectDetector
from object.detection.yolo_general_detector import generalDetector


def build_master(config):
	slaves = {}
	slaves['object_detector'] = get_object_detector(config['object_detector']['name'], config['object_detector']['param'])
	slaves['object_tracker'] = get_object_tracker(config['object_tracker']['name'], config['object_tracker']['param'])
	slaves['bg_extractor'] = get_back_ground_extractor(config['back_ground_extractor']['name'], config['back_ground_extractor']['param'])
	slaves['bg_selector'] = get_back_ground_selector(config['back_ground_selector']['name'], config['back_ground_selector']['param'])	
	slaves['activity_aggregator'] = get_acitivity_aggregator(config['activity_aggreagator']['name'], config['activity_aggreagator']['param'])
	slaves['scheduler'] = get_scheduler(config['scheduler']['name'], config['scheduler']['param'])
	slaves['stitcher'] = get_stitcher(config['stitcher']['name'], config['stitcher']['param']) 
	return slaves


def get_object_detector(object_detector, param):
	if object_detector == 'movObjectDetector':
		return movObjectDetector(None)
	elif object_detector == 'generalDetector':
		return generalDetector(None)
	elif object_detector == 'cacheDetector':
		return CachDetector(param[0])
	else:
		return movObjectDetector(None)

def get_object_tracker(object_tracker, param):
	if object_tracker == 'sortTracker':
		return SortTracker()
	else:
		return SortTracker()

def get_back_ground_extractor(back_ground, param):
	return BGExtractor(1000)

def get_back_ground_selector(back_ground, param):
	return BGSelector(1000)

def get_acitivity_aggregator(name, param):
	return ActivityAggregator()

def get_scheduler(name, param):
	return BasicScheduler()

def get_stitcher(name, param):
	return Stitcher()
