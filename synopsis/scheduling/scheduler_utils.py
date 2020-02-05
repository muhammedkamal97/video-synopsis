from object.activity.activity_tube import ActivityTube
from object.activity.bounding_box import BoundingBox


def do_boxes_overlap(box1: BoundingBox, box2: BoundingBox) -> bool:
    if (box1.upper_left[0] > box2.lower_right[0] or box2.upper_left[0] > box1.lower_right[0]):
        return False
    if (box1.lower_right[1] < box2.upper_left[1] or box2.lower_right[1] < box1.upper_left[1]):
        return False
    return True

def do_ativities_colide(act1: ActivityTube, act2: ActivityTube, start_frame: int) -> bool:
    for i in range(min([act1.get_num_frames() - start_frame, act2.get_num_frames()])):
        if do_boxes_overlap(act1.get_data[start_frame+i].box, act2.get_data[i].box):
            return False
    return True

def get_uncolide_start_frame(act1, act2):
    for start_frame in range(act1.get_num_frames()):
        if not do_ativities_colide(act1, act2, start_frame):
            return start_frame
    return start_frame + 1