from typing import List

from objects.geometric_objects import Point3, Sphere, Polygon, Point2


class FlightSpace(object):

    def __init__(self, vertices: List[Point2], min_altitude: float = 0.0, max_altitude: float = 0.0):
        self.vertices = Polygon(vertices)
        self.min_altitude = min_altitude
        self.max_altitude = max_altitude


class Plane(object):

    def __init__(self, tag: str, position: Point3, velocity: float, radius: float):

        self.tag = tag
        self.position = position
        self.velocity = velocity
        self.cd_sphere = Sphere(self.position, radius)
