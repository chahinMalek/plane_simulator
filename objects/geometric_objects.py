from math import atan2, pi, sqrt
from typing import List
from typing import Tuple


class Point2(object):

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @classmethod
    def from_tuple(cls, p_tuple: Tuple) -> 'Point2':
        return cls(*p_tuple[:2])

    @classmethod
    def from_point3(cls, point: 'Point3', freeze_coordinate: int = 2) -> 'Point2':

        if freeze_coordinate == 2:
            return cls(point.x, point.y)
        elif freeze_coordinate == 1:
            return cls(point.x, point.z)
        else:
            return cls(point.y, point.z)

    @staticmethod
    def orientation(p1: 'Point2', p2: 'Point2', p3: 'Point2') -> int:

        v1: 'Point2' = p2 - p1
        v2: 'Point2' = p3 - p1
        theta: float = v1.x * v2.y - v2.x * v1.y

        if theta > 0:
            return 1
        elif theta < 0:
            return -1
        return 0

    def __repr__(self) -> str:
        return '({}, {})'.format(self.x, self.y)

    def __lt__(self, p: 'Point2') -> bool:
        return self.x < p.x or (self.x == p.x and self.y < p.y)

    def __gt__(self, p: 'Point2') -> bool:
        return self.x > p.x or (self.x == p.x and self.y > p.y)

    def __eq__(self, p: 'Point2') -> bool:
        return self.x == p.x and self.y == p.y

    def __cmp__(self, other: 'Point2'):

        if self < other:
            return -1
        elif self > other:
            return 1
        return 0

    def __le__(self, p: 'Point2') -> bool:
        return self < p or self == p

    def __ge__(self, p: 'Point2') -> bool:
        return self > p or self == p

    def __add__(self, p: 'Point2') -> 'Point2':
        return Point2(self.x + p.x, self.y + p.y)

    def __sub__(self, p: 'Point2') -> 'Point2':
        return self + (-p)

    def __neg__(self) -> 'Point2':
        return Point2(-self.x, -self.y)

    def __mul__(self, value: float) -> 'Point2':
        return Point2(self.x * value, self.y * value)

    def __rmul__(self, value: float) -> 'Point2':
        return self.__mul__(value)

    def to_tuple(self) -> Tuple:
        return self.x, self.y

    def distance_between(self, p: 'Point2') -> float:
        return sqrt((self.x - p.x) ** 2 + (self.y - p.y) ** 2)

    def slope(self) -> float:

        theta: float = atan2(self.y, self.x)
        theta *= 180 / pi
        return theta if self.y >= 0.0 else 360.0 + theta

    def angle_between(self, p: 'Point2') -> float:

        angle = (p - self).slope()
        return angle if angle >= 0.0 else 360.0 + angle


class Point3(Point2):

    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y)
        self.z = z

    def __repr__(self) -> str:
        return '({}, {}, {})'.format(self.x, self.y, self.z)

    def __add__(self, p: 'Point3') -> 'Point3':
        return Point3(self.x + p.x, self.y + p.y, self.z + p.z)

    def __sub__(self, p: 'Point3') -> 'Point3':
        return self + (-p)

    def __neg__(self) -> 'Point3':
        return Point3(-self.x, -self.y, -self.z)

    def __mul__(self, value: float) -> 'Point3':
        return Point3(self.x * value, self.y * value, self.z * value)

    def __rmul__(self, value: float) -> 'Point3':
        return self.__mul__(value)

    def to_tuple(self) -> Tuple:
        return self.x, self.y, self.z

    def distance_between(self, p: 'Point3'):
        return sqrt((self.x - p.x) ** 2 + (self.y - p.y) ** 2 + (self.z - p.z) ** 2)


class Segment2(object):

    def __init__(self, start: Point2, end: Point2):
        self.start = start
        self.end = end

    def get_point(self, t: float) -> Point2:
        return self.start + t * (self.end - self.start)

    def is_vertical(self):
        return self.start.x == self.end.x

    def __contains__(self, point: 'Point2'):

        if Point2.orientation(self.start, self.end, point) != 0:
            return False

        if self.is_vertical():
            return min(self.start.y, self.end.y) <= point.y <= max(self.start.y, self.end.y)

        return min(self.start.x, self.end.x) <= point.x <= max(self.start.x, self.end.x)

    def intersects(self, s: 'Segment2') -> bool:

        o1 = Point2.orientation(self.start, self.end, s.start)
        o2 = Point2.orientation(self.start, self.end, s.end)
        o3 = Point2.orientation(s.start, s.end, self.start)
        o4 = Point2.orientation(s.start, s.end, self.end)

        if o1 != o2 and o3 != o4:
            return True

        if o1 == 0 and s.start in self:
            return True

        if o2 == 0 and s.end in self:
            return True

        if o3 == 0 and self.start in s:
            return True

        if o4 == 0 and self.end in s:
            return True

        return False

    def length(self) -> float:
        return self.start.distance_between(self.end)


class Segment3(object):

    def __init__(self, start: 'Point3', end: 'Point3'):
        self.start = start
        self.end = end

    def get_point(self, t: float) -> Point3:

        point = self.start + t * (self.end - self.start)

        point.x = round(point.x)
        point.y = round(point.y)
        point.z = round(point.z)

        return point

    def length(self) -> float:
        return self.start.distance_between(self.end)


class Polygon(object):

    def __init__(self, vertices: List[Point2] = None):

        if len(vertices) <= 2:
            raise ValueError('Cannot create poly with less than two vertices.')

        self.vertices = Polygon.simplify_poly(vertices) if vertices is not None else []
        self.is_convex = self.is_convex()

    def __getitem__(self, index: int) -> Point2:
        return self.vertices[index]

    def __repr__(self):
        return self.vertices.__repr__()

    def is_convex(self):

        if len(self.vertices) <= 2:
            return True

        ori: int = Point2.orientation(self.vertices[0], self.vertices[1], self.vertices[2])
        n: int = len(self.vertices)

        for i in range(n):
            if Point2.orientation(self.vertices[i], self.vertices[(i+1) % n], self.vertices[(i+2) % n]) != ori:
                return False

        return True

    def __contains__(self, point: 'Point2') -> bool:

        if self.is_convex:

            def is_in_convex_poly(points: List[Point2], point: Point2) -> bool:

                if len(points) == 3:

                    p1 = points[0]
                    p2 = points[1]
                    p3 = points[2]

                    ori = True

                    ori &= Point2.orientation(p1, p2, point) >= 0
                    ori &= Point2.orientation(p2, p3, point) >= 0
                    ori &= Point2.orientation(p3, p1, point) >= 0

                    return ori

                mid = len(points) // 2

                if Point2.orientation(points[0], points[mid], point) >= 0:
                    return is_in_convex_poly(points[mid:] + [points[0]], point)

                return is_in_convex_poly(points[:mid + 1], point)

            return is_in_convex_poly(self.vertices, point)

        else:
            min_p = min(self.vertices, key=lambda p: p.x)
            ref_p = Point2(min_p.x - 1, point.y)

            n: int = len(self.vertices)
            seg = Segment2(point, ref_p)
            counter: int = 0

            for i in range(n):
                if Segment2(self.vertices[i], self.vertices[(i+1)%n]).intersects(seg):
                    counter += 1

            return counter % 2 == 1

    @staticmethod
    def simplify_poly(vertices: List[Point2]) -> List[Point2]:

        index, _ = min(enumerate(vertices), key=lambda p: (p[1].y, -p[1].x))

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

    def __lt__(self, other: 'Circle'):
        return self.center < other.center or (self.center == other.center and self.radius <= other.radius)

    def __eq__(self, other: 'Circle'):
        return self.center == other.center and self.radius == other.radius

    def __cmp__(self, other):

        if self == other:
            return 0
        elif self < other:
            return -1
        return 1

    def __hash__(self):
        return self.center, self.radius

    # todo remove
    def __str__(self):
        return 'c: {}, r: {}'.format(self.center, self.radius)

    def __repr__(self):
        return self.__str__()


class Sphere(Circle):

    def __init__(self, center: Point3, radius: float):
        super().__init__(center, radius)
        self.center = center
        self.radius = radius

    def __contains__(self, point: Point3) -> bool:
        return point.distance_between(self.center) <= self.radius

    def intersects(self, s: 'Sphere'):
        return self.center.distance_between(s.center) <= self.radius + s.radius
