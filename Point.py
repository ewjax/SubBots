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
        self.x: int = x
        self.y: int = y

    def distance_to(self, other_point: Point) -> float:
        """
        :type other_point: Point
        :param other_point: the other point
        :return: distance from this point to another point
        """
        return math.sqrt((other_point.x - self.x) ** 2 + (other_point.y - self.y) ** 2)

    def bearing_to(self, other_point: Point) -> float:
        """
        Bearings in compass format, 0-360

        :type other_point: Point
        :param other_point: the other point
        :return: bearing from this point to another point
        """
        rv = -1
        if self != other_point:
            rv = (math.atan2((other_point.x - self.x), (other_point.y - self.y)) * 180.0/math.pi) % 360.0
        return rv


def main():

    # do some basic testing of range
    p1 = Point()
    p2 = Point(3, 4)

    distance1 = p1.distance_to(p2)
    distance2 = p2.distance_to(p1)

    print(f'distance = {distance1}')
    print(f'distance = {distance2}')


    # do some basic testing of bearings
    p2 = Point(0,5)
    bearing1 = p1.bearing_to(p2)
    bearing2 = p2.bearing_to(p1)
    print(f'bearing and reciprocal to/from ({p2.x}, {p2.y}) = {bearing1} / {bearing2}')

    p2 = Point(5,0)
    bearing1 = p1.bearing_to(p2)
    bearing2 = p2.bearing_to(p1)
    print(f'bearing and reciprocal to/from ({p2.x}, {p2.y}) = {bearing1} / {bearing2}')

    p2 = Point(5, -5)
    bearing1 = p1.bearing_to(p2)
    bearing2 = p2.bearing_to(p1)
    print(f'bearing and reciprocal to/from ({p2.x}, {p2.y}) = {bearing1} / {bearing2}')

    p2 = Point(0,-5)
    bearing1 = p1.bearing_to(p2)
    bearing2 = p2.bearing_to(p1)
    print(f'bearing and reciprocal to/from ({p2.x}, {p2.y}) = {bearing1} / {bearing2}')

    p2 = Point(-5,-5)
    bearing1 = p1.bearing_to(p2)
    bearing2 = p2.bearing_to(p1)
    print(f'bearing and reciprocal to/from ({p2.x}, {p2.y}) = {bearing1} / {bearing2}')

    p2 = Point(-5,0)
    bearing1 = p1.bearing_to(p2)
    bearing2 = p2.bearing_to(p1)
    print(f'bearing and reciprocal to/from ({p2.x}, {p2.y}) = {bearing1} / {bearing2}')

    p2 = Point(-5,5)
    bearing1 = p1.bearing_to(p2)
    bearing2 = p2.bearing_to(p1)
    print(f'bearing and reciprocal to/from ({p2.x}, {p2.y}) = {bearing1} / {bearing2}')

    p2 = Point(-1,5)
    bearing1 = p1.bearing_to(p2)
    bearing2 = p2.bearing_to(p1)
    print(f'bearing and reciprocal to/from ({p2.x}, {p2.y}) = {bearing1} / {bearing2}')

    # test error condition
    bearing1 = p1.bearing_to(p1)
    bearing2 = p1.bearing_to(p1)
    print(f'bearing and reciprocal to/from same point ({p1.x}, {p1.y}) = {bearing1} / {bearing2}')

if __name__ == '__main__':
    main()
