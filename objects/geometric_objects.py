from math import atan2, pi, sqrt
from typing import List
from typing import Tuple


class Point2(object):

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @classmethod
    def from_tuple(cls, p_tuple: Tuple[float, float]) -> 'Point2':
        return cls(*p_tuple)

    def __repr__(self) -> str:
        return '({}, {})'.format(self.x, self.y)

    def __lt__(self, p: 'Point2') -> bool:
        return self.x < p.x or (self.x == p.x and self.y < p.y)

    def __gt__(self, p: 'Point2') -> bool:
        return self.x > p.x or (self.x == p.x and self.y > p.y)

    def __eq__(self, p: 'Point2') -> bool:
        return self.x == p.x and self.y == p.y

    def __le__(self, p: 'Point2') -> bool:
        return self < p or self == p

    def __ge__(self, p: 'Point2') -> bool:
        return self > p or self == p

    def to_tuple(self) -> Tuple:
        return self.x, self.y

    def distance_between(self, p: 'Point2') -> float:
        return sqrt((self.x - p.x) ** 2 + (self.y - p.y) ** 2)

    def slope(self) -> float:

        theta: float = atan2(self.y, self.x)
        theta *= 180 / pi
        return theta if self.y >= 0.0 else 360.0 + theta

    def angle_between(self, p: 'Point2') -> float:

        angle = p.slope() - self.slope()
        return angle if angle >= 0.0 else 360.0 + angle


class Point3(Point2):

    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y)
        self.z = z

    def __repr__(self) -> str:
        return '({}, {}, {})'.format(self.x, self.y, self.z)

    def to_tuple(self) -> Tuple:
        return self.x, self.y, self.z

    def distance_between(self, p: 'Point3'):
        return sqrt((self.x - p.x) ** 2 + (self.y - p.y) ** 2 + (self.z - p.z) ** 2)


class Polygon(object):

    def __init__(self, vertices: List[Point2]):
        self.vertices = Polygon.simplify_poly(vertices)

    def __repr__(self):
        return self.vertices.__repr__()

    @staticmethod
    def simplify_poly(vertices: List[Point2]) -> List[Point2]:

        index, _ = min(enumerate(vertices), key=lambda p: (p[1].y, p[1].x))

        # swap only if necessary
        if index != 0:
            vertices[0], vertices[index] = vertices[index], vertices[0]

        sorted_p = sorted(vertices[1:], key=lambda x: (vertices[0].angle_between(x), vertices[0].distance_between(x)))

        index = len(sorted_p) - 1

        while index > 0 and sorted_p[index].angle_between(vertices[0]) == sorted_p[index-1].angle_between(vertices[0]):
            index -= 1

        return [vertices[0], *sorted_p[:index], *reversed(sorted_p[index:])]


class Circle(object):

    def __init__(self, center: Point2, radius: float):
        self.center = center
        self.radius = radius

    def __contains__(self, point: Point2) -> bool:
        return point.distance_between(self.center) <= self.radius

    def intersects(self, c: 'Circle') -> bool:
        return self.center.distance_between(c.center) <= self.radius + c.radius


class Sphere(Circle):

    def __init__(self, center: Point3, radius: float):

        super().__init__(center, radius)
        self.center = center
        self.radius = radius

    def __contains__(self, point: Point3) -> bool:
        return point.distance_between(self.center) <= self.radius

    def intersects(self, s: 'Sphere'):
        return self.center.distance_between(s.center) <= self.radius + s.radius


print(Point3(0, 0, 1) in Sphere(Point3(0, 0, 0), 1))
