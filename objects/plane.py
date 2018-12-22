from objects.geometric_objects import Point3, Sphere


class Plane(object):

    def __init__(self, tag: str, position: Point3, velocity: float, radius: float):

        self.tag = tag
        self.position = position
        self.velocity = velocity
        self.cd_sphere = Sphere(self.position, radius)
