from random import randint

from objects.geometric_objects import Segment3, Point3


class Plane(object):

    __COUNTER = 0

    def __init__(self, velocity: float, radius: float):

        self.id = Plane.__COUNTER
        self.velocity = velocity
        self.radius = radius
        Plane.__COUNTER += 1


class Flight(object):

    def __init__(self, path: Segment3, velocity: float, radius: float):

        self.path = path
        self.plane = Plane(velocity, radius)

    def __eq__(self, other: 'Flight'):
        return self.plane.id == other.plane.id

    @classmethod
    def get_random_flight(cls, min_x, max_x, min_y, max_y, min_h, max_h, velocity, radius) -> 'Flight':

        return Flight(
            Segment3(
                Point3(randint(min_x, max_x), randint(min_y, max_y), randint(min_h, max_h)),
                Point3(randint(min_x, max_x), randint(min_y, max_y), randint(min_h, max_h))
            ),
            velocity,
            radius
        )

    def get_plane_position(self):

        t: float = 0
        coefficient = self.plane.velocity / self.path.length()

        while t <= 1:
            current_position = self.path.get_point(t)
            yield current_position
            t += coefficient

        return None
