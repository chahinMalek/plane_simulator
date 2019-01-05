from typing import List

from bintrees import AVLTree as AVL

from objects.geometric_objects import Sphere


def get_intersections(spheres: List[Sphere]):

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
    s = set()

    while len(start_points) > 0 and len(end_points) > 0:

        if start_points[-1] <= end_points[-1]:
            sphere = spheres[start_points_map[start_points[-1]]]
            tree.insert(sphere.center, sphere)

            try:
                key = sphere.center

                while True:
                    prev = tree.prev_item(key)[1]

                    if prev.intersects(sphere):
                        # print('Intersection found: {} and {}'.format(prev, sphere))
                        s.add(prev.center.to_tuple())
                        s.add(sphere.center.to_tuple())

                    key = prev.center

            except KeyError:
                pass

            try:
                key = sphere.center

                while True:
                    prev = tree.succ_item(key)[1]

                    if prev.intersects(sphere):
                        # print('Intersection found: {} and {}'.format(prev, sphere))
                        s.add(prev.center.to_tuple())
                        s.add(sphere.center.to_tuple())

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

    return s
