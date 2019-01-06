from random import randint, randrange
from typing import List, Optional

from objects.geometric_objects import Segment3, Point3


class Plane(object):

    __COUNTER = 0

    def __init__(self, velocity: float, radius: float):

        self.id = Plane.__COUNTER
        self.velocity = velocity
        self.radius = radius
        Plane.__COUNTER += 1


class Flight(object):

    __TYPE = {
        0: 'ex',
        1: 'in',
        2: 'hi'
    }

    def __init__(self, paths: List[Segment3], velocity: float, radius: float, type: int):
        self.plane = Plane(velocity, radius)
        self.paths = paths
        self.type = type

    def __eq__(self, other: 'Flight'):
        return self.plane.id == other.plane.id

    @classmethod
    def get_external_flight(cls, c_start: Point3, c_end: Point3, velocity: float, radius: float):
        flight = Flight([Segment3(c_start, c_end)], velocity, radius, 0)
        return flight

    @classmethod
    def get_internal_flight(cls, to_point: Point3, c_start: Point3, c_end: Point3,
                            l_point: Point3, velocity: float, radius: float):

        path = [Segment3(to_point, c_start), Segment3(c_start, c_end), Segment3(c_end, l_point)]
        flight = Flight(path, velocity, radius, 1)
        return flight

    @classmethod
    def get_h_internal_flight(cls, velocity: float, radius: float, c_start: Point3, c_end: Point3,
                              to_point: Optional[Point3] = None, l_point: Optional[Point3] = None):

        if (to_point is None) == (l_point is None):
            raise AttributeError('Half internal flight must have either a takeoff point or a landing point.')

        if to_point is None:
            path = [Segment3(c_start, c_end), Segment3(c_end, l_point)]
        else:
            path = [Segment3(to_point, c_start), Segment3(c_start, c_end)]

        flight = Flight(path, velocity, radius, 2)
        return flight

    @classmethod
    def get_random_flight(cls, min_x, max_x, min_y, max_y, min_h, max_h, velocity, radius) -> 'Flight':

        flight_type = randint(0, 2)
        c_start = Point3(randint(min_x, max_x), randint(min_y, max_y), randint(min_h, max_h))
        c_end = Point3(randint(min_x, max_x), randint(min_y, max_y), c_start.z)

        if flight_type == 0:
            return Flight.get_external_flight(c_start, c_end, velocity, radius)

        elif flight_type == 1:
            c_segment = Segment3(c_start, c_end)
            to_point = c_segment.get_point(randrange(-2, 0))
            l_point = c_segment.get_point(randrange(1, 2) + 0.1)
            to_point.z, l_point.z = 0, 0
            return Flight.get_internal_flight(to_point, c_start, c_end, l_point, velocity, radius)

        else:
            c_segment = Segment3(c_start, c_end)
            choice = randint(0, 1)

            if choice == 0:
                to_point = c_segment.get_point(randrange(-2, 0))
                l_point = None
                to_point.z = 0
            else:
                to_point = None
                l_point = c_segment.get_point(randrange(1, 2) + 0.1)
                l_point.z = 0

            return Flight.get_h_internal_flight(to_point=to_point, c_start=c_start, c_end=c_end,
                                                l_point=l_point, velocity=velocity, radius=radius)

    def get_plane_position(self):

        for path in self.paths:

            t: float = 0
            coefficient = self.plane.velocity / path.length()

            while t <= 1:
                current_position = path.get_point(t)
                yield current_position
                t += coefficient

            t %= 1

        return None
