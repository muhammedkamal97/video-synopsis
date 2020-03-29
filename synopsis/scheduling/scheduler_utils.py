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
            return False
    return True


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
