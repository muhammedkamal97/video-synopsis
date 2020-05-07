import itertools
from typing import List

from object.activity.activity_tube import ActivityTube
from object.activity.bounding_box import BoundingBox


def do_boxes_overlap(box1: BoundingBox, box2: BoundingBox) -> bool:
    """Check if the two bounding boxes overlap.

    Parameters
    ----------
    box1 : BoundingBox
        The first bounding box.
    box2 : BoundingBox
        The second bounding box.

    Returns
    -------
    bool
        boolean that is true if the two boxes overlap and false otherwise.
    """
    if box1.upper_left[0] > box2.lower_right[0] or box2.upper_left[0] > box1.lower_right[0]:
        return False
    if box1.lower_right[1] < box2.upper_left[1] or box2.lower_right[1] < box1.upper_left[1]:
        return False
    return True


def do_activities_collide(act1: ActivityTube, act2: ActivityTube, start_frame: int) -> bool:
    """Check if the two activity tubes collide if "act2" is set after "start_frame" frames with "act1".

    Parameters
    ----------
    act1 : ActivityTube
        The first activity tube.
    act2 : ActivityTube
        The second activity tube.
    start_frame : int
        The number of frame that "act2" will start from it.

    Returns
    -------
    bool
        boolean that is true if the two activities collides given start_frame and false otherwise.
    """
    for i in range(min([act1.get_num_frames() - start_frame, act2.get_num_frames()])):
        if do_boxes_overlap(act1.get_data()[start_frame + i].box, act2.get_data()[i].box):
            return True
    return False


def get_uncollide_start_frame(act1: ActivityTube, act2: ActivityTube) -> int:
    """Get the starting frame to put the second activity "act2" with the first activity "act1" without colliding.

    Parameters
    ----------
    act1 : ActivityTube
        The first activity tube.
    act2 : ActivityTube
        The second activity tube.

    Returns
    -------
    int
        The number of frame to start the second activity.
    """
    for start_frame in range(act1.get_num_frames()):
        if not do_activities_collide(act1, act2, start_frame):
            return start_frame
    return start_frame + 1


def can_put_activity_tube_in_frame_boxes(act: ActivityTube, frame_num: int, frame_boxes: List[List[BoundingBox]]):
    for i in range(frame_num, frame_num + act.get_num_frames()):
        if i >= len(frame_boxes):
            continue
        boxes = frame_boxes[i]
        for box in boxes:
            if do_boxes_overlap(box, act.get_data()[i - frame_num].box):
                return False
    return True


def get_box_area(box: BoundingBox) -> float:
    x1 = box.upper_left[0]
    y1 = box.upper_left[1]
    x2 = box.lower_right[0]
    y2 = box.lower_right[1]
    return (y2 - y1) * (x2 - x1)


def get_boxes_int_rate(box1: BoundingBox, box2: BoundingBox) -> float:
    inter = compute_boxes_intersection(box1, box2)
    return max(inter / get_box_area(box1), inter / get_box_area(box2))


def add_activity_to_frame_boxes(activity_tube: ActivityTube, start_frame: int, frame_boxes: List[List[BoundingBox]]):
    while len(frame_boxes) <= start_frame + activity_tube.get_num_frames():
        frame_boxes.append([])
    for i in range(activity_tube.get_num_frames()):
        frame_boxes[start_frame + i].append(activity_tube.get_data()[i].box)

def can_put_activity_tube_in_frame_boxes_int(act: ActivityTube, frame_num: int, frame_boxes: List[List[BoundingBox]],
                                             rate: float) -> bool:
    for i in range(frame_num, frame_num + act.get_num_frames()):
        if i >= len(frame_boxes):
            continue
        boxes = frame_boxes[i]
        for box in boxes:
            if get_boxes_int_rate(box, act.get_data()[i - frame_num].box) > rate:
                return False
    return True


def can_put_activity_tube_in_frame(act: ActivityTube, frame_num: int,
                                   activity_tubes: List[ActivityTube], start_frames: List[int]) -> bool:
    """
    Check if the "act" activity tube can be put in frame "frame_num" without itersecting with other activity tubes
    :param act: The activity tube to be checked.
    :param frame_num: The frame number that the activity tube "act" will start from.
    :param activity_tubes: The list of activity tubes to be scheduled.
    :param start_frames: List of integers with same length as the activity_tubes list.
            Each integer represents the starting frame of the activity tube -with the same index- in the synopsis video.
    :return: boolean value : true if the activity tube "act" can be put in frame "frame_num" without any intersection
        with other activity tubes starting at "start_frames"
    :rtype: bool
    """
    for a, f in zip(activity_tubes, start_frames):
        if do_activities_collide(a, act, frame_num - f):
            return False
    return True


def get_video_length(activity_tubes: List[ActivityTube], start_frames: List[int]) -> int:
    """Get the output video length in frames.

    Parameters
    ----------
    activity_tubes : List[ActivityTube]
            The list of activity tubes to be scheduled.
    start_frames : List[int]
            List of integers with same length as the activity_tubes list.
            Each integer represents the starting frame of the activity tube -with the same index- in the synopsis video.

    Returns
    -------
    int
        The number of frames in the synopsis video.
    """
    output_length = 0
    for i in range(len(activity_tubes)):
        output_length = max(output_length, activity_tubes[i].get_num_frames() + start_frames[i])
    return output_length


def compute_total_intersection(activity_tubes: List[ActivityTube], start_frames: List[int]) -> int:
    """
    Compute the total intersection in a video.
    Total intersection the sum of intersected pixels between each two boxes.

    :param activity_tubes: the activity tubes in the video
    :param start_frames:
    :return: total intersection in the video.
    :rtype: int
    """
    # Initialize the frame array
    video_length = get_video_length(activity_tubes, start_frames)
    frame_boxes = [[] for i in range(video_length)]

    # Put all boxes in their frame
    for i in range(len(activity_tubes)):
        activity_tube = activity_tubes[i]
        for j in range(activity_tube.get_num_frames()):
            frame_boxes[start_frames[i] + j].append(activity_tube.get_data()[j].box)

    # Compute intersections
    intersections = 0
    for boxes in frame_boxes:
        for box1, box2 in itertools.combinations(boxes, 2):
            intersections += compute_boxes_intersection(box1, box2)

    return intersections


def compute_boxes_intersection(box1: BoundingBox, box2: BoundingBox) -> int:
    """
    Compute number of pixels that are in the intersection of two bounding boxes.
    If the two activities don't intersect returns zero.

    :param box1: First bounding box.
    :param box2: Second bounding box.
    :return: Number of pixels in the intersection (if exist otherwise zero).
    :rtype: int
    """

    # Compute the rectangle that is formalized because of the intersection.
    x1 = max(box1.upper_left[0], box2.upper_left[0])
    y1 = max(box1.upper_left[1], box2.upper_left[1])
    x2 = min(box1.lower_right[0], box2.lower_right[0])
    y2 = min(box1.lower_right[1], box2.lower_right[1])

    if x1 >= x2 or y1 >= y2:  # If the two boxes don't intersect
        return 0
    else:
        return (x2 - x1) * (y2 - y1)
