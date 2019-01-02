from bintrees import AVLTree as AVL

from bintrees import AVLTree as AVL

from objects.geometric_objects import Point3, Sphere

points = [
    Point3(-6, 3, 0),
    Point3(-5, 2, 0.8),
    Point3(4.72, 2.01, 0.2),
    Point3(-4.24, 6.33, 0),
    Point3(-2, 4, 0),
    Point3(-1.76, -3.15, 0),
    Point3(-2, -1.19, 0.3),
    Point3(4.76, 3.69, 0.1),
]

spheres = [Sphere(center=x, radius=1) for x in points]

start_points_map = {}
end_points_map = {}

for index, sphere in enumerate(spheres):
    start_points_map[(sphere.center.x - sphere.radius, sphere.center.y)] = index
    end_points_map[(sphere.center.x + sphere.radius, sphere.center.y)] = index

event_points = [x for x in start_points_map.keys()]
event_points.extend(x for x in end_points_map.keys())
event_points.sort()

start_points = sorted(start_points_map.keys(), reverse=True)
end_points = sorted(end_points_map.keys(), reverse=True)

tree = AVL()

while len(start_points) > 0 and len(end_points) > 0:

    if start_points[-1] <= end_points[-1]:
        sphere = spheres[start_points_map[start_points[-1]]]
        tree.insert(sphere.center, sphere)

        try:
            key = sphere.center

            while True:
                prev = tree.prev_item(key)[1]

                if prev.intersects(sphere):
                    print('Intersection found: {} and {}'.format(prev, sphere))
                key = prev.center

        except KeyError:
            pass

        try:
            key = sphere.center

            while True:
                prev = tree.succ_item(key)[1]

                if prev.intersects(sphere):
                    print('Intersection found: {} and {}'.format(prev, sphere))
                key = prev.center

        except KeyError:
            pass

        start_points.pop()

    else:
        tree.remove(spheres[end_points_map[end_points[-1]]].center)
        end_points.pop()


while len(end_points) > 0:
    tree.remove(spheres[end_points_map[end_points[-1]]].center)
    end_points.pop()
