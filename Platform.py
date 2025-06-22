
import Point
# import json
import pickle

#
# data class for all data for this platform, maintained by the simulation umpire
#
class PlatformStatus:

    def __init__(self):
        self.location = Point.Point(3,4)    # cartesian (x,y) location

        self.course = 0.0           # in degrees
        self.course_ordered = 0.0   # in degrees
        self.turn_rate = 10.0       # rate course changes, degrees/unit time

        self.depth = 0              # in feet, 0 = surfaced
        self.depth_ordered = 0      # in feet
        self.depth_change_rate = 10 # rise/dive rate, feet/unit time

        self.speed = 0              # in knots
        self.speed_ordered = 0      # in knots
        self.acceleration = 5       # rate speed changes/unit time

        self.timestamp = ''         # timestamp for this data point

        self.hull = 100             # damage, 0 = sunk


class Platform:

    def __init__(self):
        self.platform_id = 0        # unique ID

        self.platform_status = PlatformStatus()
        self.baseline_sound_level = 50  # sound power level, in decibels, at all stop






def main():
    platform_status = PlatformStatus()
    # print(f'{json.dumps(platform_status)}')
    # print(f'{json.dumps(platform_status.__dict__)}')

    for entry in platform_status.__dict__:
        print(f'{entry}: {platform_status.__dict__[entry]}')

    print(f'original = {platform_status}')
    pd = pickle.dumps(platform_status)
    print(f'pickled = {pd}')
    pu = pickle.loads(pd)
    print(f'unpickled = {pu}')



if __name__ == '__main__':
    main()
