import heapq
from typing import List, NoReturn, Set, Dict, Tuple, Optional

import numpy as np
from nptyping import Array

from background.selection.abstract_bg_selector import AbstractBGSelector
from object.activity.activity_tube import ActivityTube

from synopsis.stitching.abstract_stitcher import AbstractStitcher


class Stitcher(AbstractStitcher):
    active_tubes: Set[ActivityTube]
    activity_tubes_state: Dict[ActivityTube, int]
    activity_schedule: List[Tuple[int, ActivityTube]]
    frame_count: int
    input_frame_count: int
    current_frame: Array[np.int]

    def initialize(self, activity_tubes: List[ActivityTube], schedule: List[int],
                   bg_selector: AbstractBGSelector, input_frame_count) -> NoReturn:
        self.activity_tubes = activity_tubes
        self.schedule = schedule
        self.bg_selector = bg_selector

        self._set_synopsis_length()
        self.activity_tubes_state = {}
        self.active_tubes = set()

        self.activity_schedule = list(zip(schedule, activity_tubes))
        heapq.heapify(self.activity_schedule)

        self.frame_count = 0
        self.input_frame_count = input_frame_count

        self.current_frame = self.process_frame()

    def process_frame(self) -> Optional[Array[np.int]]:
        if self.frame_count == self.synopsis_length:
            return None

        while len(self.activity_schedule) != 0 and self.frame_count == self.activity_schedule[0][0]:  # Mark new tubes to be active
            _, new_tube = heapq.heappop(self.activity_schedule)
            self.active_tubes.add(new_tube)
            self.activity_tubes_state[new_tube] = 0

        frame = self.bg_selector.map(max(10, int(self.frame_count / self.synopsis_length * self.input_frame_count)))

        tubes_marked_for_deletion = set()
        for active_tube in self.active_tubes:
            # Get tube partial frame to be added in the current frame and increment its state
            trackable = active_tube.get_data()[self.activity_tubes_state[active_tube]]
            self.activity_tubes_state[active_tube] += 1

            # Add tube partial frame to the current frame
            x1, y1 = trackable.box.upper_left
            x2, y2 = trackable.box.lower_right
            frame[y1:y2, x1:x2] = trackable.data

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

    def next_frame(self) -> Array[np.int]:
        frame = np.array(self.current_frame)
        self.current_frame = self.process_frame()
        return frame

    def _set_synopsis_length(self):
        length = 0
        for tube, start_frame in list(zip(self.activity_tubes, self.schedule)):
            tube_end_frame = len(tube.get_data()) + start_frame
            length = max(length, tube_end_frame)

        self.synopsis_length = length
