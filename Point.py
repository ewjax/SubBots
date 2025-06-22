# this postpones evaluation in annotations, allowing type Point to be passed to Point member functions
from __future__ import annotations

import math

#
# class to hold cartesian (x,y) location coordinates
#
class Point:

    def __init__(self, x: int = 0, y: int = 0):
        # classic cartesian coordinates, i.e
        #   x increasing from west to east
        #   y increasing from south to north
        self.x = x
        self.y = y

    def distance_to(self, other_point: Point) -> float:
        """
        :param other_point: the other point
        :return: range from this point to another point
        """
        return math.sqrt((other_point.x - self.x) ** 2 + (other_point.y - self.y) ** 2)

    def bearing_to(self, other_point: Point) -> float:
        """
        Bearings in compass format, 0-360

        :param other_point: the other point
        :return: bearing from this point to another point
        """
        return (math.atan2((other_point.x - self.x), (other_point.y - self.y)) * 180.0/math.pi) % 360.0

def main():

    # do some basic testing of range
    p1 = Point()
    p2 = Point(3, 4)

    distance = p1.distance_to(p2)

    print(f'distance = {distance}')

    # do some basic testing of bearings
    x = 0
    y = 5
    bearing = p1.bearing_to(Point(x,y))
    print(f'bearing to ({x}, {y}) = {bearing}')

    x = 5
    y = 5
    bearing = p1.bearing_to(Point(x,y))
    print(f'bearing to ({x}, {y}) = {bearing}')

    x = 5
    y = 0
    bearing = p1.bearing_to(Point(x,y))
    print(f'bearing to ({x}, {y}) = {bearing}')

    x = 5
    y = -5
    bearing = p1.bearing_to(Point(x,y))
    print(f'bearing to ({x}, {y}) = {bearing}')

    x = 0
    y = -5
    bearing = p1.bearing_to(Point(x,y))
    print(f'bearing to ({x}, {y}) = {bearing}')

    x = -5
    y = -5
    bearing = p1.bearing_to(Point(x,y))
    print(f'bearing to ({x}, {y}) = {bearing}')

    x = -5
    y = 0
    bearing = p1.bearing_to(Point(x,y))
    print(f'bearing to ({x}, {y}) = {bearing}')

    x = -5
    y = 5
    bearing = p1.bearing_to(Point(x,y))
    print(f'bearing to ({x}, {y}) = {bearing}')

    x = -1
    y = 5
    bearing = p1.bearing_to(Point(x,y))
    print(f'bearing to ({x}, {y}) = {bearing}')

if __name__ == '__main__':
    main()
