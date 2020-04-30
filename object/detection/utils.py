from object.activity.bounding_box import BoundingBox
def merge_boxes(boxes):
	merged_boxes = []
	que = [b for b in boxes]
	while len(que) != 0:
		box1 = que.pop(0)
		# calculate distance between box and every other box in que
		merge_happen = False
		index = 0
		for i in range(len(que)):
			if distance(box1,que[i]) < 20000:
				merge_happen = True
				index = i
				break
		if merge_happen:
			box2 = que.pop(index)
			que.append(merge(box1,box2))
		else:
			merged_boxes.append(box1)
	return merged_boxes

def distance(b1,b2):
	l1, r1 = b1.upper_left, b1.lower_right
	p11, p12, p13, p14 = l1, (r1[0],l1[1]), (l1[0],r1[1]), r1
	l2, r2 = b2.upper_left, b2.lower_right
	p21, p22, p23, p24 = l2, (r2[0],l2[1]), (l2[0],r2[1]), r2
	minimum = (p11[0] - p21[0])**2 + (p11[1] - p21[1])**2
	for p1 in [p11,p12,p13,p14]:
		for p2 in [p21, p22, p23, p24]:
			minimum = min(minimum, (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
	return minimum


def merge(b1,b2):
	l1, r1 = b1.upper_left, b1.lower_right
	l2, r2 = b2.upper_left, b2.lower_right
	l_x = min(l1[0],l2[0])
	l_y = min(l1[1],l2[1])
	r_x = max(r1[0],r2[0])
	r_y = max(r1[1],r2[1])
	return BoundingBox((l_x,l_y),(r_x, r_y))



