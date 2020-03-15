class BoundingBox:
    def __init__(self, upper_left, lower_right):
        """"
        The center point is in the upper left corner.
        upper_left: (x:int, y:int)
        lower_right: (x:int, y:int)
        """
        self.upper_left = upper_left
        self.lower_right = lower_right
