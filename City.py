import math

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        xDis = abs(self.x - city.x)
        yDis = abs(self.y - city.y)
        distance = math.hypot(xDis,yDis)
        return distance

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"