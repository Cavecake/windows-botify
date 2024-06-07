class Rect:
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], (list,tuple)) and len(args[0]) == 4:
            self.__list_to_points(args[0])
        elif len(args) == 2 and all(isinstance(arg, (list, tuple)) and len(arg) == 2 for arg in args):
            self.__two_points_init(args[0], args[1])
        elif len(args) == 3 and isinstance(args[0], (list, tuple)) and len(args[0]) == 2 and all(isinstance(arg, (int, float)) for arg in args[1:]):
            self.__width_height_init(args[0], args[1], args[2])
        else:
            raise ValueError("Invalid arguments. Use either (point1, point2), (point1, width, height), or a list [x1, y1, x2, y2]")
        self.__verify_points()

    def __two_points_init(self, point1, point2):
        self.x1, self.y1 = point1
        self.x2, self.y2 = point2

    def __width_height_init(self, point1, width, height):
        self.x1, self.y1 = point1
        self.x2, self.y2 = self.x1 + width, self.y1 + height

    def __list_to_points(self, coords):
        self.x1, self.y1, self.x2, self.y2 = coords

    def __verify_points(self):
        # Ensure (x1, y1) is the upper-left and (x2, y2) is the bottom-right
        if self.x1 > self.x2:
            self.x1, self.x2 = self.x2, self.x1
        if self.y1 > self.y2:
            self.y1, self.y2 = self.y2, self.y1

    def __repr__(self):
        return f"Rect(({self.x1}, {self.y1}), ({self.x2}, {self.y2}))"

    def getCornerPoints(self):
        return (self.x1, self.y1), (self.x2, self.y2)

    def getDimensions(self):
        return [self.x1, self.y1, self.getWidth(), self.getHeight()]

    def getWidth(self):
        return self.x2 - self.x1

    def getHeight(self):
        return self.y2 - self.y1