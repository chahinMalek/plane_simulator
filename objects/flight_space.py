from typing import List
from objects.geometric_objects import Point2, Polygon


class FlightSpace(object):

    def __init__(self, vertices: List[Point2], min_altitude: float = 0.0, max_altitude: float = 0.0):

        self.vertices = Polygon(vertices)
        self.min_altitude = min_altitude
        self.max_altitude = max_altitude

