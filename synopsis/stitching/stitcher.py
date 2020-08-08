import heapq
from datetime import datetime, timedelta
from typing import List, NoReturn, Set, Dict, Tuple, Optional

import numpy as np
from nptyping import Array

from background.selection.abstract_bg_selector import AbstractBGSelector
from object.activity.activity_tube import ActivityTube

from synopsis.stitching.abstract_stitcher import AbstractStitcher

import cv2 as cv


class Stitcher(AbstractStitcher):
    active_tubes: Set[ActivityTube]
    activity_tubes_state: Dict[ActivityTube, int]
    activity_schedule: List[Tuple[int, ActivityTube]]
    frame_count: int
    input_frame_count: int
    input_fps: int
    start_time: datetime
    current_frame: Array[np.uint8]

    def __init__(self, segmentation=False):
        super(Stitcher, self).__init__()
        self.segmentation = segmentation

    def initialize(self, activity_tubes: List[ActivityTube], schedule: List[int], bg_selector: AbstractBGSelector,
                   input_frame_count: int, input_fps: int, start_time: datetime) -> NoReturn:
        self.activity_tubes = activity_tubes
        self.schedule = schedule
        self.bg_selector = bg_selector

        self._set_synopsis_length()
        self.activity_tubes_state = {}
        self.active_tubes = set()

        self.activity_schedule = list(zip(schedule, range(len(activity_tubes)), activity_tubes))
        heapq.heapify(self.activity_schedule)

        self.frame_count = 0
        self.input_frame_count = input_frame_count
        self.input_fps = input_fps
        self.start_time = start_time

        self.current_frame = self.process_frame()

    def get_foreground(self, back_ground: Array[np.uint8], y1, y2, x1, x2, object_frame: Array[np.uint8]) -> Array[np.uint8]:

        object_frame[np.where(object_frame == 0)] = 1
        temp = back_ground[y1:y2, x1:x2]
        newmask = object_frame - temp
        newmask[np.where(newmask > 240)] = 0
        newmask[np.where(newmask < 10)] = 0
        try:
            # newmask = cv.morphologyEx(newmask, cv.MORPH_TOPHAT, (5, 5))
            newmask = cv.erode(newmask, (10, 10), 10)
            # newmask2[np.where(newmask2 >= 200)] = 100
            # newmask = newmask1 - newmask2
            # x1_new = int(0.2 * newmask.shape[1])
            # y1_new = int(0.1 * newmask.shape[0])
            # x2_new = int(0.8 * newmask.shape[1])
            # y2_new = int(0.9 * newmask.shape[0])
            # newmask[y1_new:y2_new, x1_new:x2_new, :] = 255
        except Exception as e:
            print(str(e))
        mask = np.zeros(object_frame.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)

        # whereever it is marked white (sure foreground), change mask=1
        # whereever it is marked black (sure background), change mask=0
        mask[np.where(newmask == 0)[:2]] = 0
        mask[np.where(newmask != 0)[:2]] = 1

        try:
            mask, bgdModel, fgdModel = cv.grabCut(object_frame, mask, None, bgdModel, fgdModel, 3,
                                                  cv.GC_INIT_WITH_MASK)
            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            object_frame = object_frame * mask2[:, :, np.newaxis]
            indices = np.where(object_frame == 0)
            object_frame[indices] = temp[indices]
        except Exception as e:
            print(str(e))
        return object_frame        
        
    def process_frame(self) -> Optional[Array[np.uint8]]:
        if self.frame_count == self.synopsis_length:
            return None

        while len(self.activity_schedule) != 0 and self.frame_count == self.activity_schedule[0][
            0]:  # Mark new tubes to be active
            _, __, new_tube = heapq.heappop(self.activity_schedule)
            self.active_tubes.add(new_tube)
            self.activity_tubes_state[new_tube] = 0

        frame = np.array(
            self.bg_selector.map(max(10, int(self.frame_count / self.synopsis_length * self.input_frame_count))))
        
        back_ground = np.copy(frame)
        tubes_marked_for_deletion = set()
        for active_tube in self.active_tubes:
            # Get tube partial frame to be added in the current frame and increment its state
            trackable = active_tube.get_data()[self.activity_tubes_state[active_tube]]
            self.activity_tubes_state[active_tube] += 1

            # Add tube partial frame to the current frame
            x1, y1 = trackable.box.upper_left
            x2, y2 = trackable.box.lower_right

            if self.segmentation:
                frame[y1:y2, x1:x2] = self.get_foreground(back_ground, y1, y2, x1, x2, trackable.data)
            else:
                frame[y1:y2, x1:x2] = trackable.data

            # Compute and attach timestamp
            center = int((x1 + x2) / 2) - 10, int((y1 + y2) / 2)
            delta_seconds = (self.activity_tubes_state[active_tube] + active_tube.start_frame) / self.input_fps
            timestamp = self.start_time + timedelta(0, int(delta_seconds))
            time_str = str(timestamp.hour).zfill(2) + ":" + str(timestamp.minute).zfill(2)
            cv.putText(frame, time_str, center, cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 5  , cv.LINE_4)
            cv.putText(frame, time_str, center, cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2, cv.LINE_4)

            # For debugging
            # cv.putText(frame, str(self.activity_tubes.index(active_tube)), center, cv.FONT_HERSHEY_PLAIN, 3,(0, 0, 0), 5, cv.LINE_4)
            # cv.putText(frame, str(self.activity_tubes.index(active_tube)), center, cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4, cv.LINE_4)
            # cv.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), thickness=2)

            # Check tube state and mark for deletion if all its contents are processed
            if self.activity_tubes_state[active_tube] == active_tube.get_num_frames():
                tubes_marked_for_deletion.add(active_tube)

        for marked_tube in tubes_marked_for_deletion:
            self.active_tubes.remove(marked_tube)

        self.frame_count += 1
        return frame

    def has_next_frame(self) -> bool:
        if self.current_frame is None:
            return False
        return True

    def next_frame(self) -> Array[np.uint8]:
        frame = np.array(self.current_frame)
        self.current_frame = self.process_frame()
        return frame

    def _set_synopsis_length(self):
        length = 0
        for tube, start_frame in list(zip(self.activity_tubes, self.schedule)):
            tube_end_frame = len(tube.get_data()) + start_frame
            length = max(length, tube_end_frame)

        self.synopsis_length = length
