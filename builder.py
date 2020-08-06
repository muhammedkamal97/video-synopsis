from background.extraction.bg_extractor import BGExtractor
from background.selection.bg_selector import BGSelector
from object.preprocessing.abstract_preprocessor import AbstractPreprocessor
from object.activity.activity_aggreagator import ActivityAggregator
from object.detection.cach_detector import CachDetector
from object.tracking.sort_tracker import SortTracker
from object.tracking.deep_sort_tracker import DeepSortTracker
from synopsis.chopping.abstract_synopsis_chopper import AbstractSynopsisChopper
from synopsis.scheduling.first_in_first_out_scheduler import FirstInFirstOutScheduler
from synopsis.scheduling.sim_annealing_scheduler import SimAnnealingScheduler
from synopsis.stitching.stitcher import Stitcher
from object.detection.mov_object_detection import movObjectDetector
from object.detection.yolo_general_detector import generalDetector


def build_master(config):
    slaves = {}
    slaves['object_detector'] = get_object_detector(config['object_detector']['name'],
                                                    config['object_detector']['param'])
    slaves['object_tracker'] = get_object_tracker(config['object_tracker']['name'], config['object_tracker']['param'])
    slaves['bg_extractor'] = get_back_ground_extractor(config['back_ground_extractor']['name'],
                                                       config['back_ground_extractor']['param'])
    slaves['bg_selector'] = get_back_ground_selector(config['back_ground_selector']['name'],
                                                     config['back_ground_selector']['param'])
    slaves['activity_aggregator'] = get_activity_aggregator(config['activity_aggreagator']['name'],
                                                            config['activity_aggreagator']['param'])
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
    elif object_tracker == 'deepSortTracker':
        return DeepSortTracker()
    else:
        return SortTracker()


def get_back_ground_extractor(back_ground, param):
    return BGExtractor(1000)


def get_back_ground_selector(back_ground, param):
    return BGSelector(1000)


def get_activity_aggregator(name, param):
    return ActivityAggregator()


def get_scheduler(name, param):
    if name == "FirstInFirstOut":
        intersection_ratio = float(param[0]["IntersectionRatio"])
        sort_by = param[0]["SortBy"]
        max_boxes = param[0]["MaxBoxes"]
        return FirstInFirstOutScheduler(sort_by=sort_by, max_boxes=max_boxes, intersection_ratio=intersection_ratio)
    elif name == "SimulatedAnnealing":
        return SimAnnealingScheduler()


def get_stitcher(name, param):
    return Stitcher()
